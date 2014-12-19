import csv
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template.defaultfilters import slugify

def export(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
    writer = csv.writer(response)
    # Write headers to CSV file
    headers = []
    for field in modeladmin._meta.fields:
        headers.append(field.name)
    writer.writerow(headers)
    # Write data to CSV file
    print modeladmin.objects.all()
    for obj in modeladmin.objects.all().order_by("id"):
        row = []
        for field in modeladmin._meta.fields:
            row.append(getattr(obj, field.name))
        writer.writerow(row)
    # Return CSV file to browser as download
    return response

def export_as_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.
    """
    if not request.user.is_staff:
        raise PermissionDenied
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')
    writer = csv.writer(response)
    field_names = [field.name for field in opts.fields]
    # Write a first row with header information
    writer.writerow(field_names)
    # Write data rows
    for obj in queryset:
        writer.writerow([getattr(obj, field) for field in field_names])
    return response
export_as_csv.short_description = "Export selected objects as CSV"
