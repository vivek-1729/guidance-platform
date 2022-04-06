from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class ResourceLink(models.Model):
    """
    Model for links to resources (on resources page)
    """
    title = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)
    topic = models.CharField(max_length=500)
    rating = models.TextField(null=True, default="[]")

    def __str__(self):
        return self.title

class VideoLink(models.Model):
    """
    Model for embdedded videos (on videos page)
    """
    name = models.CharField(max_length=1000)
    link = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Student(models.Model):
    """
    Extended user model. This has all the data for each user. 
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    seen_resource = models.TextField(null=True)
    resource_rating = models.TextField(null=True)
    points = models.IntegerField(default=0)
    grade = models.CharField(max_length=20)
    nk_id = models.CharField(max_length=100)


    def __str__(self):
        return self.user.username

class Bucket(models.Model):
    """
    Model for category of resource
    """
    buckets = models.TextField(default="['general', 'english', 'engineering', 'business', 'governing', 'seen']")

class Scholarship(models.Model):
    name = models.CharField(max_length=1001)
    link = models.CharField(max_length=1000)
    description = models.CharField(max_length=5000)


class Messages(models.Model):
    """
    Messages model
    """
    description = models.TextField()
    sender_name = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='sender')
    receiver_name = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='receiver')
    time = models.TimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.receiver_name} From: {self.sender_name}"

    class Meta:
        ordering = ('timestamp',)

class Friends(models.Model):
    """
    Friends model
    """

    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    friend = models.IntegerField()

    def __str__(self):
        return f"{self.friend}"

