from django.db import models
from blogger.models import blog_maker

class Blog(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    blogger_id = models.ForeignKey(blog_maker, on_delete=models.CASCADE)


class Like_blog(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    blogger_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(blog_maker, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class report(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='repoted')
    user = models.ForeignKey(blog_maker, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='report_images/', null=True, blank=True)