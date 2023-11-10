from django.db import models

# Create your models here.


'''记录用户的信息'''
class UserInfo(models.Model):

    stu_id = models.CharField(verbose_name="学号",max_length=7)
    name = models.CharField(verbose_name="姓名", max_length=32)
    pwd = models.CharField(verbose_name="密码",max_length=64)
    wechat_id = models.CharField(verbose_name="微信号",max_length=64)


'''关联表，记录用户的时间'''
class UserVenueTime(models.Model):
    stu_id = models.CharField(verbose_name="学号",max_length=7)
    day_of_week = models.SmallIntegerField(verbose_name="日期", null=True,blank=True)
    venus_id = models.SmallIntegerField(verbose_name="场地号",null=True,blank=True)

    campus_choices=(
        (1,"四平"),
        (2,"嘉定"),
    )
    campus = models.SmallIntegerField(verbose_name="校区",choices=campus_choices,null=True,blank=True)
    start_time = models.SmallIntegerField(verbose_name="场地起始时间",null=True,blank=True)
    end_time = models.SmallIntegerField(verbose_name="场地结束时间", null=True, blank=True)
