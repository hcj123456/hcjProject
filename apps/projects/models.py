from django.db import models
from utils.base_model import BaseModel


# Create your models here.
class Projects(BaseModel):

    objects = models.Manager()
    id = models.AutoField(verbose_name="id主键", primary_key=True, help_text="id主键")
    name = models.CharField(max_length=200, verbose_name='项目名称', help_text='项目名称', unique=True)
    leader = models.CharField(max_length=50, verbose_name='项目负责人', help_text='项目负责人')
    tester = models.CharField(verbose_name="测试人员", help_text="测试人员", max_length=50)
    programmer = models.CharField(verbose_name="开发人员", help_text="开发人员", max_length=50)
    publish_app = models.CharField(verbose_name="发布应用", help_text="发布应用", max_length=100)
    desc = models.CharField(max_length=200, verbose_name='项目描述', help_text='项目描述', blank=True, null=True, default='')

    class Meta:
        db_table = "tb_projects"
        verbose_name = "项目信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name