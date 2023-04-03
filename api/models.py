from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now as current_time


class Post(models.Model):
    content = models.TextField()
    creation_date = models.DateField(default=current_time)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author')
    likers = models.ManyToManyField(User, through='Like')


class Like(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_liked = models.DateField(default=current_time)

    class Meta:
        unique_together = ('post_id', 'user_id')
        index_together = ('post_id', 'user_id')
