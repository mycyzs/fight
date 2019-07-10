# -*- coding: utf-8 -*-


from django.db import models


class MailReceiver(models.Model):
    account = models.CharField(max_length=100)
    mailbox = models.CharField(max_length=50)
    when_created = models.CharField(max_length=50)
    created_by = models.CharField(max_length=100, default="")
    app_id = models.IntegerField(default=0)
    server_id = models.TextField()
    app_name = models.CharField(max_length=100)
    server_list = models.TextField()

    def to_dic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


class OrgObj(models.Model):
    name = models.CharField(max_length=100)

    def to_dic(self):
        return dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]])


class UserObj(models.Model):
    name = models.CharField(max_length=100)
    org_obj = models.ForeignKey(OrgObj)

    def to_dic(self):
        key_list = ["org_obj"]
        return_data = dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields if f.name not in key_list]])
        for i in key_list:
            return_data[i] = getattr(self, i).to_dic()
        return return_data


class FileObj(models.Model):
    file_content = models.BinaryField()
    file_name = models.CharField(max_length=100)
