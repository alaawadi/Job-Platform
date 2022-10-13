from django.db import models
from django.db.models.enums import Choices
from django.db.models.fields import CharField
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.
JOB_TYPE=(
         ('full time','full time'),
         ('part time','part time')
         )
# فنكشن لتخزين الصور جوا ملف باسم المودل الي بعمل منه ابلود
#  والصورة بتضل بنفس الصيغة الي هي عليها لكن اسمها بصير ترقيم تسلسلي


def image_upload(instance,filename):
    imagename , extension = filename.split(".")
    return "jobs/%s.%s"%(instance.id,extension)

class Job(models.Model):
    owner = models.ForeignKey(User, related_name='job_owner', on_delete=models.CASCADE)
    title=models.CharField(max_length=50)
    job_type=models.CharField(max_length=20 , choices=JOB_TYPE)
    discription=models.TextField(max_length= 1000)
    published_at=models.DateTimeField(auto_now=True)
    vacancy=models.IntegerField(default=1)
    salary=models.IntegerField(default=0)
    experience=models.IntegerField(default=1)
    category= models.ForeignKey('Category',on_delete=models.CASCADE)
    image=models.ImageField(upload_to=image_upload)
    location=models.CharField(max_length=25,blank=True,null=True)
    map= models.URLField(blank=True,null=True)
    slug = models.SlugField(blank=True, null=True)
    # like=models.ManyToManyField(User,blank=True,null=True)

    def save(self,*args, **kwargs):
        self.slug = slugify(self.title)
        super(Job,self).save(*args, **kwargs)
    # بهادي الطريقة بعمل سلج، يعني بستبدل الفواصل الي في اسم الجوب بسلاش عشان استخدمها بدل الاي دي 
    
    def __str__(self):
        return self.title
    
    
    
    
class Category(models.Model):
    name=models.CharField(max_length=25)
    def __str__(self):
        return self.name
    
    
    
    
class Apply(models.Model):
    job = models.ForeignKey(Job, related_name='apply_job', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    webiste = models.URLField()
    cv = models.FileField(upload_to='apply/')
    cover_letter = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name
    
    
    