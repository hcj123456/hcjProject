from django.db import models

# Create your models here.

from utils.base_model import BaseModel


class Debugtalks(BaseModel):
    objects = models.Manager()
    id = models.AutoField(verbose_name="id主键", primary_key=True, help_text="id主键")
    name = models.CharField(verbose_name="debugtalk文件名称", help_text="debugtalk文件名称", max_length=200, default="debugtalk.py")
    debugtalk = models.TextField(null=True, default="#debugtalk.py", help_text="debugtalk文件")
    project = models.OneToOneField("projects.Projects",
                                   on_delete=models.CASCADE,
                                   help_text="所属项目",
                                   related_name="debugtalks")

    class Meta:
        db_table = "tb_debugtalks"
        verbose_name = "debugtalk.py文件"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name