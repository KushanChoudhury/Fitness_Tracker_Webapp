from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    height = models.IntegerField()
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    age = models.IntegerField()
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()




class DailyData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    steps = models.PositiveIntegerField()
    calories_burned = models.DecimalField(max_digits=6, decimal_places=2,default=0.0)
    calories_intake = models.DecimalField(max_digits=6, decimal_places=2,default=0.0)

    def __str__(self):
        return f"{self.user.username}'s Daily Data - {self.date}"

class ModuleCompletion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.module} ({'Completed' if self.completed else 'Not Completed'})"


