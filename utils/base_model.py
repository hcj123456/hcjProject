from django.db import models
from utils.common import datetime_fmt


class BaseModel(models.Model):

    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='更新时间', auto_now=True)

    class Meta:

        abstract = True