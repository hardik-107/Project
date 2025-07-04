from django.db import models

# Create your models here.



class User(models.Model):
    name=models.CharField(max_length=70)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    
    def __str__(self):
     return self.name
 
class Student(models.Model): 
   name = models.CharField(max_length=100) 
   age = models.IntegerField() 
   grade = models.CharField(max_length=10) 
   email = models.EmailField(unique=True) 
   
   def __str__(self): 
       return self.name 