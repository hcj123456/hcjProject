from django.db import models
from utils.base_model import BaseModel


# Create your models here.
class Interfaces(BaseModel):

     objects = models.Manager()
     name = models.CharField(verbose_name='接口名称', help_text='接口名称', max_length=200, unique=True)
     tester = models.CharField(verbose_name='测试人员名称', help_text='测试人员名称', max_length=50)
     project = models.ForeignKey('projects.Projects', on_delete=models.CASCADE, related_name='interfaces')

     class Meta:
          db_table = "tb_interfaces"
          verbose_name = "接口信息"
          verbose_name_plural = verbose_name

     def __str__(self):
          return self.name