from django.db import models

# Create your models here.
from utils.base_model import BaseModel



class Reports(BaseModel):
    objects = models.Manager()
    id = models.AutoField(verbose_name="id主键", primary_key=True, help_text="id主键")
    name = models.CharField(verbose_name="报告名称", help_text="报告名称", max_length=200, unique=True)
    result = models.BooleanField(verbose_name="执行结果", default=1, help_text="执行结果")
    count = models.IntegerField(verbose_name="用例总数", help_text="用例总数")
    success = models.IntegerField(verbose_name="成功总数", help_text="成功总数")
    html = models.TextField(verbose_name="报告HTML源码", help_text="报告HTML源码", null=True, blank=True, default='')
    summary = models.TextField(verbose_name="报告详情", help_text="报告详情", null=True, blank=True, default='')

    class Meta:
        db_table = "tb_reports"
        verbose_name = "测试报告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name