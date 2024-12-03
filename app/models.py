from django.db import models

class Login(models.Model):

    username=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    user_type=models.CharField(max_length=100)

class Register(models.Model):
    LOGIN=models.ForeignKey(Login,on_delete=models.CASCADE)
    firstname=models.CharField(max_length=100)
    place=models.CharField(max_length=200)
    gender=models.CharField(max_length=50)
    dob=models.CharField(max_length=100)
    address=models.CharField(max_length=250)
    photo=models.CharField(max_length=100)
    

class Notifications(models.Model):

    event=models.CharField(max_length=100)
    posted_date=models.CharField(max_length=100)
    venue=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    time=models.CharField(max_length=100)
    fees=models.CharField(max_length=100)
    available_ticket = models.CharField(max_length=100)
    
    
class Notes(models.Model):
    Register=models.ForeignKey(Register,on_delete=models.CASCADE)
    notes=models.CharField(max_length=150)
    reply=models.CharField(max_length=250)

