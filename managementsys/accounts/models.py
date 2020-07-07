from django.db import models
from  django.contrib.auth.models import User
from recurrence.fields import RecurrenceField
# Create your models here.
from django.db.models.signals import post_save

	
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


def records(sender,sdate,instance, **kwargs):
	#print(sdate)
	#print(instance.day_name)
	tt_records = tt_record.objects.create(tt_id = instance.id,is_rescheduled = False,is_deleted = False,is_absent = False,topic_discussed = "Null",description = "NULL",date =sdate)
	tt_records.save()

class rescheduled_classes(models.Model):
	rescheduled_id = models.AutoField(primary_key = True)
	resc_username = models.ForeignKey(User,db_column="username", on_delete=models.CASCADE,)
	resc_sem_section = models.ForeignKey(sem_sections, db_column = "sem_section",on_delete=models.CASCADE,)
	resc_subject_id = models.ForeignKey(subjects,db_column="subject_id", on_delete=models.CASCADE,)
	resc_day_name = models.ForeignKey(days_ref, db_column = "days_ref",on_delete=models.CASCADE,)
	resc_hour_no = models.ForeignKey(hours, db_column = "hour_no",on_delete=models.CASCADE,)
	resc_date = models.DateField()
	resc_topic_discussed  = models.CharField(blank=True,max_length=30)
	resc_description = models.CharField(blank=True,max_length=30,help_text = "Leave Blank if not Applicable")
	def __str__(self):
		ret = str(self.resc_username) +' takes ' + str(self.resc_sem_section) + " RESC class " + str(self.resc_subject_id) + " on " + str(self.resc_hour_no) + " on " + str(self.resc_day_name) + str(self.resc_date);
		return ret
	class Meta:
		constraints = [
				models.UniqueConstraint(fields=['resc_sem_section', 'resc_day_name', 'resc_hour_no'], name='RESC_Allotment_check')
			]

def reschedule_class(sender,**kwargs):
	if kwargs['created']:
		changerecord = tt_record.objects.filter(tt__sem_section = str(kwargs['instance'].resc_sem_section),tt__day_name = str(kwargs['instance'].resc_day_name),tt__hour_no = kwargs['instance'].resc_hour_no,date = str(kwargs['instance'].resc_date))
		#changerecord = tt_record.objects.select_related('tt').filter(tt__sem_section = str(kwargs['instance'].resc_sem_section))
		print(changerecord)
		changerecord.update(is_rescheduled = True,is_deleted = True,rescheduled_id = kwargs['instance'].rescheduled_id)

def create_tt_record(sender,**kwargs):
	if kwargs['created']:
		from datetime import date
		from datetime import time
		from datetime import datetime
		from datetime import timedelta
		print(type(kwargs['instance'].day_name))
		testdate = date.today()
		days =["Monday", "Tuesday", "Wednesday", "Thursday", 
                         "Friday", "Saturday", "Sunday"]
		for j in range(7):
			if(days[testdate.weekday()] == str(kwargs['instance'].day_name)):
				print("VOILAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
				print(testdate)
				break
			#print(days[testdate.weekday()],testdate)
			testdate = testdate + timedelta(1)

		sdate = testdate# start date !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
		enddate = testdate + timedelta(60)  # end date is 60 ddays from start date !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

		while(sdate <= enddate)	:
			#print(j)
			#print(tuples)
			#print(sdate)
			records(sender,sdate = sdate,instance = kwargs['instance'])
			sdate = sdate + timedelta(7)
			
post_save.connect(create_tt_record,sender = time_table)
post_save.connect(reschedule_class,sender = rescheduled_classes)



class tt_record(models.Model):
	id = models.AutoField(primary_key = True)
	tt = models.ForeignKey(time_table,default = 0,on_delete = models.CASCADE,related_name="tt_id_value")
	rescheduled_id = models.ForeignKey( rescheduled_classes, default = None,null = True,on_delete = models.CASCADE)
	is_rescheduled = models.BooleanField(default = False)
	is_deleted = models.BooleanField(default = False)
	is_absent = models.BooleanField(default = False)
	topic_discussed  = models.CharField(max_length=30)
	description = models.CharField(blank=True,max_length=30,help_text = "Leave Blank if not Applicable")
	date = models.DateField()
	class Meta:
		constraints = [
				models.UniqueConstraint(fields=['tt_id','date'], name='Record_check')
			]
	def __str__(self):
		ret = str(self.tt_id)
		return ret
	#@property
	#ef tt_values(self):
    #ategory = time_table.objects.get('username','sem_section','day_name','Hr_no','username')
    #return self.update_set.filter(category=my_category).order_by('-id')[0]
'''	@classmethod
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
				
	'''




