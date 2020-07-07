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
	list_display = ('tt_id','is_rescheduled','rescheduled_id','is_deleted','is_absent','topic_discussed','description','date')
@admin.register(rescheduled_classes)
class rescheduled_classes_admin(admin.ModelAdmin):
	list_display = ('rescheduled_id','resc_username', 'resc_sem_section', 'resc_subject_id','resc_day_name','resc_hour_no','resc_date','resc_topic_discussed','resc_description')
	formfield_overrides = {
        models.DateTimeField: {'input_formats': ('%Y-%m-%D',)},
    }