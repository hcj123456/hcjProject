from django.db import models
from utils.base_model import BaseModel


# Create your models here.
class Interfaces(BaseModel):
     objects = models.Manager()
     id = models.AutoField(verbose_name="id主键", primary_key=True, help_text="id主键")
     name = models.CharField(verbose_name='接口名称', help_text='接口名称', max_length=200, unique=True)
     project = models.ForeignKey('projects.Projects',
                                 on_delete=models.CASCADE,
                                 related_name='interfaces',
                                 help_text="所属项目")
     tester = models.CharField(verbose_name='测试人员名称', help_text='测试人员名称', max_length=50)
     desc = models.CharField(verbose_name="简要描述", help_text="简要描述", max_length=200, null=True, blank=True)

     class Meta:
          db_table = "tb_interfaces"
          verbose_name = "接口信息"
          verbose_name_plural = verbose_name

     def __str__(self):
          return self.name