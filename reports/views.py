from datetime import datetime, timedelta
from django.views.generic import TemplateView
from profile.models import Center
from Sessions.models import NewSession

class ReportIndexView(TemplateView):
	template_name = "index.html"

	def get_context_data(self, **kwargs):		
		context = super(ReportIndexView, self).get_context_data(**kwargs)
		context['centers'] = Center.objects.all()
		return context

class AttendanceReportIndexView(TemplateView):
	template_name = "index.html"

	def get_context_data(self, **kwargs):
		context = super(AttendanceReportIndexView, self).get_context_data(**kwargs)
		context['centers'] = Center.objects.all()
		center_id = int("".join(self.request.GET.get('center', '0')))

		start = "".join(self.request.GET.get('start', str(datetime.now())))
		if start.strip() == "":
			start = str(datetime.now().date())
		
		end = "".join(self.request.GET.get('end', str(datetime.now() + timedelta(days=7))))
		if end.strip() == "":
			end = str(datetime.now().date() + timedelta(days=7) ) 

		context['sessions'] = NewSession.objects.filter(center_name=Center.objects.get(id=center_id), start_date__gte=start, end_date__lte=end)

		return context
