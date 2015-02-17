from django.shortcuts import render
from datetime import datetime, timedelta
from django.views.generic import TemplateView
from profile.models import Center
from Sessions.models import NewSession
import csv
from django.http import HttpResponse



class ReportIndexView(TemplateView):
	template_name = "index.html"

	def get_context_data(self, **kwargs):		
		context = super(ReportIndexView, self).get_context_data(**kwargs)
		context['centers'] = Center.objects.all()
		return context

class CSVResponseMixin(object):
    csv_filename = 'csvfile.csv'

    def get_csv_filename(self):
        return self.csv_filename

    def render_to_csv(self, data):
        response = HttpResponse(content_type='text/csv')
        cd = 'attachment; filename="{0}"'.format(self.get_csv_filename())
        response['Content-Disposition'] = cd
        writer = csv.writer(response)
        for key, value in data.iteritems():
	        writer.writerow([key,value])

        return response

class AttendanceReportIndexView(TemplateView, CSVResponseMixin):
	template_name = "index.html"

	def get(self, request, *args, **kwargs):
		context = super(AttendanceReportIndexView, self).get_context_data(**kwargs)
		context['centers'] = Center.objects.all()
		center_id = int("".join(self.request.GET.get('center', '0')))

		start = "".join(self.request.GET.get('start', str(datetime.now())))
		if start.strip() == "":
			start = str(datetime.now().date())
		
		end = "".join(self.request.GET.get('end', str(datetime.now() + timedelta(days=7))))
		if end.strip() == "":
			end = str(datetime.now().date() + timedelta(days=7) ) 

		sessions_data = NewSession.objects.filter(center_name=Center.objects.get(id=center_id), start_date__gte=start, end_date__lte=end)
		data_csv = {}
		for data in sessions_data:
			data_csv[data] = NewSession.get_attendance(data)
		if 'Generate-btn' in request.GET:
			context['sessions'] = sessions_data
			response =render(request,'index.html',context) 
			return response 
		
		elif 'Download-btn' in request.GET:
			return self.render_to_csv(data_csv)



'''class DataView(CSVResponseMixin, TemplateView):
	#template_name = "index.html"	
    
    def get(self, request, *args, **kwargs):
		
		context = super(DataView, self).get_context_data(**kwargs)
		context['centers'] = Center.objects.all()
		#center_id = int("".join(self.request.GET.get('center', '0')))

		#start = "".join(self.request.GET.get('start', str(datetime.now())))
		##if start.strip() == "":
		#	start = str(datetime.now().date())
		
		#end = "".join(self.request.GET.get('end', str(datetime.now() + timedelta(days=7))))
		#if end.strip() == "":
		#	end = str(datetime.now().date() + timedelta(days=7) ) 

		context['sessions'] = NewSession.objects.filter(center_name=Center.objects.get(id=center_id), start_date__gte=start, end_date__lte=end)
		
	
        
		return self.render_to_csv(context['sessions'])'''

'''def export_as_csv(request):
    """
    Generic csv export admin action.
    """
    raw_data = AttendanceReportIndexView.get_context_data()
    for data in raw_data:
    	data_csv[data] = NewSession.get_attendance()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=hh.csv'
    writer = csv.writer(response)

    writer = csv.writer(response)
    for row in data_csv:
        writer.writerow([row])
    return response
    '''