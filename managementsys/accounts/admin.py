from django.contrib import admin
from .models import *
admin.site.register(subjects)
admin.site.register(hours)
admin.site.register(teacher_subjects)
admin.site.register(days_ref)
admin.site.register(sem_sections)
#admin.site.register(tt_record)

@admin.register(time_table)
class time_table_admin(admin.ModelAdmin):
	list_display = ('username', 'sem_section', 'subject_id','day_name','hour_no')
	fields = ('username', 'sem_section', 'subject_id',('day_name','hour_no'))
	list_filter = ('username', 'sem_section', 'subject_id','day_name','hour_no')
	ordering = ('username', 'sem_section', 'subject_id','day_name','hour_no')
	search_fields = ('sem_section__sem_section','username__username','subject_id__subject_name',)
@admin.register(tt_record)
class tt_record_admin(admin.ModelAdmin):
	list_display = ('time_table','is_rescheduled','is_deleted','is_populated','date')

