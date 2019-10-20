from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Student(models.Model):
    resume = models.CharField(max_length=500, blank=True)
    # TODO make this a validation
    GPA = models.FloatField()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    def __str__(self):
        return self.first_name + " " + self.last_name

class Company(models.Model):
    about_info = models.CharField(max_length=200)
    company_location = models.CharField(max_length=50)
    company_name = models.CharField(max_length=50)
    def __str__(self):
        return self.company_name

class Job(models.Model):
    description = models.CharField(max_length=200)
    location = models.CharField(max_length=50)
    compensation = models.IntegerField()
    name = models.CharField(max_length=50)
    number_of_positions = models.IntegerField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class StudentJob(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    rank = models.IntegerField(
        validators=[
            MaxValueValidator(5),
            MinValueValidator(1)
        ])
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

class CompanyStudent(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    rank = models.IntegerField(
        validators=[
            MinValueValidator(1)
        ])
