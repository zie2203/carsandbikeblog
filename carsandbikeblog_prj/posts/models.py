from django.db import models
from django.contrib.auth.models import User
# Create your models here.
#create a model(python class)by extending the builtin model class
class postsm(models.Model):
    post_title=models.CharField(max_length=255)
    post_description=models.TextField()
    post_shortname=models.SlugField(max_length=255,unique=True)
    post_published_date_time= models.DateTimeField(auto_now_add=True)
    post_author=models.ForeignKey(User, on_delete=models.CASCADE)
    #the user is related to posts in one to many relationships
    #so user/author is the foreign key in the posts table
    post_image=models.ImageField(upload_to='posts/images',blank=True)
    def __str__(self):
          return self.post_title

class Reviews(models.Model):
    #declare a list of values that needs to be included in the drop down
    #As a tuple,the first value is the actual db value,next is the label
    STARS = (
        (1,'One Star'),
        (2, 'Two Star'),
        (3, 'Three Star'),
        (4, 'Four Star'),
        (5, 'Five Star'),
    )
    title=models.CharField(max_length=255)
    description=models.TextField()
    review_author=models.ForeignKey(User, on_delete=models.CASCADE)
    video_url = models.CharField(max_length=255,blank=True)
    rating = models.PositiveSmallIntegerField(choices=STARS, default=1)
    post = models.ForeignKey(postsm, related_name='reviewofpost' ,default=1, on_delete=models.CASCADE)
    #the user is related to posts in one to many relationships
    #so user/author is the foreign key in the posts table
    def __str__(self):
          return self.title