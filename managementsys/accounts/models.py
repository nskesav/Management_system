from django.db import models
from  django.contrib.auth.models import User
from recurrence.fields import RecurrenceField
# Create your models here.

	
class subjects(models.Model):
	subject_id = models.AutoField(primary_key = True)
	subject_name = models.CharField(max_length = 30)
	def __str__(self):
		return self.subject_name
class hours(models.Model):
	hour_no = models.IntegerField(primary_key = True)
	start_time = models.TimeField(auto_now=False, auto_now_add=False)
	end_time = models.TimeField(auto_now=False, auto_now_add=False)
	def __str__(self):
		ret = str(self.hour_no) +' hr'
		return ret
class teacher_subjects(models.Model):
	subject_id = models.ForeignKey(subjects,db_column="subject_id",on_delete=models.CASCADE,)
	username = models.ForeignKey(User,db_column="username", on_delete=models.CASCADE,)
	def __str__(self):
		ret = str(self.username) +' - '+ str(self.subject_id);
		return ret
class days_ref(models.Model):
	day_no = models.IntegerField()
	day_name = models.CharField(max_length = 30,primary_key = True)
	def __str__(self):
		ret = self.day_name;
		return ret
class sem_sections(models.Model):
	sem_section = models.CharField(max_length = 10,primary_key = True)
	def __str__(self):
		return self.sem_section
class time_table(models.Model):
	username = models.ForeignKey(User,db_column="username", on_delete=models.CASCADE,)
	sem_section = models.ForeignKey(sem_sections, db_column = "sem_section",on_delete=models.CASCADE,)
	subject_id = models.ForeignKey(subjects,db_column="subject_id", on_delete=models.CASCADE,)
	day_name = models.ForeignKey(days_ref, db_column = "days_ref",on_delete=models.CASCADE,)
	hour_no = models.ForeignKey(hours, db_column = "hour_no",on_delete=models.CASCADE,)
	def __str__(self):
		ret = str(self.username) +' takes ' + str(self.sem_section) + " class " + str(self.subject_id) + " on " + str(self.hour_no) + " on " + str(self.day_name);
		return ret
	class Meta:
		constraints = [
				models.UniqueConstraint(fields=['sem_section', 'day_name', 'hour_no'], name='Allotment_check')
			]

class tt_record(models.Model):
	time_table = models.OneToOneField(time_table,on_delete = models.CASCADE)
	is_rescheduled = models.BooleanField(default = False)
	is_populated = models.BooleanField(default = False)
	is_deleted = models.BooleanField(default = False)
	date = models.DateField(auto_now_add=True,)
	class Meta:
		constraints = [
				models.UniqueConstraint(fields=['time_table','date'], name='Record_check')
			]
	def __str__(self):
		ret = str(self.time_table);
		return ret
	@classmethod
	def create(self):
		from datetime import date
		from datetime import time
		from datetime import datetime
		from datetime import timedelta
		non_populated = tt_record.objects.filter(is_populated = False)
		for i in non_populated:
			sdate = date(2020, 5, 6)   # start date !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
			instance = time_table(id = i)
			print(i.id)
			print(instance.id)
			for j in range(5):
				#print(j)
				tt_record.objects.bulk_create([
					tt_record(time_table = instance,is_rescheduled = False,is_deleted = False,is_populated = True,date = sdate )
				])
				#print(tuples)
				sdate = sdate + timedelta(5)
				#tuples.save(self)
				
	
