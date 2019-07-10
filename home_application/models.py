# -*- coding: utf-8 -*-


from django.db import models


class Host(models.Model):
    name = models.CharField(max_length=30,null=True)
    age = models.CharField(max_length=30,null=True)
    text = models.TextField(null=True)
    when_created = models.DateTimeField(null=True)


class Server(models.Model):
    host = models.ForeignKey(Host)
    background_img = models.BinaryField(null=True)


class File(models.Model):
    file_content = models.BinaryField(null=True)
    file_name = models.CharField(max_length=100, null=True)


# 周期表
class Book(models.Model):
    ip = models.CharField(max_length=30, null=True)
    biz = models.IntegerField(null=True)
    bk_cloud_id = models.IntegerField(null=True)


class Log(models.Model):
    host = models.ForeignKey(Book)
    mem = models.CharField(max_length=30, null=True)
    disk = models.CharField(max_length=30, null=True)
    cpu = models.CharField(max_length=30, null=True)
    date_time = models.CharField(max_length=120, null=True)



# 巡检数据库表

# class TaskDetail(models.Model):
#     task = models.ForeignKey(Task,related_name='task_detail')
#     act_time = models.DateTimeField(null=True)
#     describe = models.TextField(null=True)
#     check_host = models.CharField(max_length=64, null=True)
#
#
# class Export(models.Model):
#     task_obj = models.ForeignKey(TaskDetail,related_name="export")
#     task_name = models.CharField(max_length=64, null=True)
#     default_area = models.CharField(max_length=64, null=True)
#     host_ip = models.CharField(max_length=64, null=True)
#     script = models.TextField(null=True)
#     max_num = models.CharField(max_length=64, null=True)
#     result = models.CharField(max_length=64, null=True)
#     is_normal = models.BooleanField(default=False)