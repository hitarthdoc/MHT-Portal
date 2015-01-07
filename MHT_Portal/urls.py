from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.site.site_header = "MHT Portal administration"
admin.site.site_title = "MHT Portal site admin"
admin.autodiscover()
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView
from reports.views import ReportIndexView, AttendanceReportIndexView

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='admin/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^attendance', AttendanceReportIndexView.as_view()),
    url(r'^reports/', ReportIndexView.as_view()),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
