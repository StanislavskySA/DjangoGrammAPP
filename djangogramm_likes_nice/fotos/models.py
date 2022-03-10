from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Fotos(models.Model):
    title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/")
    description = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='fotos')
    liked = models.IntegerField(default=0, null=True, blank=True)


LIKE_CHOICES = (
    ('Like', 'Like'),
    ('Unlike', 'Unlike'),
)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ForeignKey(Fotos, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, max_length=8)
    updated = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}-{self.photo}-{self.value}"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='authors',
                               on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    time_create = models.DateTimeField(auto_now_add=True)
