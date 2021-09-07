from django.db import models
from utils.base_model import BaseModel


# Create your models here.
class Projects(BaseModel):

    objects = models.Manager()
    name = models.CharField(max_length=200, verbose_name='项目名称', help_text='项目名称', unique=True)
    leader = models.CharField(max_length=50, verbose_name='项目负责人', help_text='项目负责人')
    desc = models.CharField(max_length=200, verbose_name='项目描述', help_text='项目描述', blank=True, null=True, default='')

    class Meta:
        db_table = "tb_projects"
        verbose_name = "项目信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name