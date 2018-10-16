from django.db import models

# Create your models here.

# Class 와 DB를 모델링
class Guestbook(models.Model):
    name = models.CharField(max_length=50,default='')
    password = models.CharField(max_length=10)
    message = models.CharField(max_length=4096)
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Guestbook(%s,  %s)' %(self.name, self.message)


