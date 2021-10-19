from django.db import models

# Create your models here.
from utils.base_model import BaseModel



class Testcases(BaseModel):
    objects = models.Manager()
    id = models.AutoField(verbose_name="id主键", help_text="id主键", primary_key=True)
    name = models.CharField(verbose_name="用例名称", help_text="用例名称", max_length=30, unique=True)
    interface = models.ForeignKey('interfaces.Interfaces',
                                  on_delete=models.CASCADE,
                                  help_text="所属接口",
                                  related_name="testcases")
    include = models.TextField(verbose_name="前置", null=True, help_text="用例执行前置顺序")
    author = models.CharField(verbose_name="编写人员", max_length=50, help_text="编写人员")
    request = models.TextField(verbose_name="请求信息", help_text="请求信息")

    class Meta:
        db_table = 'tb_testcases'
        verbose_name = "用例信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name