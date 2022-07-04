
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Usredetails(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    gender=models.CharField(max_length=50,choices=(("male","male"),("female","female"),("other","other")))
    hobbies=models.CharField(max_length=50,choices=(("Dance","Dance"),("Travling","Travling"),("Reading","Reading")))
    profile=models.ImageField(upload_to='profile')
    address=models.TextField(max_length=150)
    mobile_number=models.CharField(max_length=10)
    def __str__(self):
        return str(self.user)