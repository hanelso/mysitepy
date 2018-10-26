from django.db import models

# Create your models here.
from django.db.models import Max

from user.models import User


class Board(models.Model):
    title = models.CharField(max_length=50, default='no title')
    content = models.CharField(max_length=4096, default='no content')
    hit = models.IntegerField(default=0)
    reg_date = models.DateTimeField(auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    g_no = models.IntegerField(default=0)
    o_no = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Board(%s, %s, %s, %s, %s)' % (self.title,self.g_no,self.o_no,self.depth, self.user_id)
