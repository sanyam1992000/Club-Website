from django.contrib import admin
from .models import Profile,Event,registration,feedback,project
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

admin.site.site_header = 'MANAN - A Techno Surge'


class ProfileAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ('user', 'fname', 'email', 'batch', 'location', 'company')
    list_display_links = ('user', 'fname', 'email', 'batch', 'location', 'company')
    list_filter = ('batch', 'label')
    search_fields = ('user', 'fname', 'email', 'batch', 'location', 'company', 'label')
    list_max_show_all = 100


class EventAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ('title', 'description', 'venue', 'fee', 'start_date')
    list_display_links = ('title', 'description', 'venue', 'fee', 'start_date')
    list_filter = ('venue', 'host')
    search_fields = ('title', 'description', 'venue', 'fee', 'host', 'start_date')
    list_max_show_all = 100


class RegistrationAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ('eventid', 'fname', 'College', 'email', 'mobile')
    list_display_links = ('eventid', 'fname', 'College', 'email', 'mobile')
    list_filter = ('eventid', 'College')
    search_fields = ('eventid', 'fname', 'College', 'email', 'mobile')
    list_max_show_all = 100


class FeedbackAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ('eventid', 'name', 'star', 'comment')
    list_display_links = ('eventid', 'name', 'star', 'comment')
    list_filter = ('eventid', 'star')
    search_fields = ('eventid', 'name', 'star', 'comment')
    list_max_show_all = 100


class ProjectAdmin(ImportExportModelAdmin, ImportExportActionModelAdmin):
    list_display = ('title', 'description', )
    list_display_links = ('title', 'description')
    list_filter = ('owner',)
    search_fields = ('title', 'description', 'owner', 'source', 'technologies')
    list_max_show_all = 100


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(registration, RegistrationAdmin)
admin.site.register(feedback, FeedbackAdmin)
admin.site.register(project, ProjectAdmin)
