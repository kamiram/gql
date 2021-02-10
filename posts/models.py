from django.db import models
from users.models import ApiUser


class Post(models.Model):
    owner = models.ForeignKey(ApiUser, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField('Title', max_length=255)
    descr = models.TextField('Description', blank=True, default='')

    def __str__(self):
        return f'{self.id}: {self.title}'

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
