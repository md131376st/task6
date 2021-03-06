from django.db import models
from django.core.files.storage import FileSystemStorage
fs = FileSystemStorage(location='/media')

# مدل بزای کزقتن اطلاعات اسم الگرریتم و فابل bash که فرمت csv  دارد
class CsvDoc(models.Model):
    name= models.CharField(max_length=1000)
    csv_file = models.FileField(upload_to='csv/%Y/%m/%d')

    def __str__(self):
        return self.csv_file.name
# Create your models here.
