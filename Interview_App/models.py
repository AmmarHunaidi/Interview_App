from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        swappable = 'AUTH_USER_MODEL'
    
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    DOB = models.DateField(null=True , blank= True)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    city = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50, blank=True)

class AuthToken(models.Model):
    user = models.ForeignKey(User, related_name='auth_tokens', on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user}"

class Company(models.Model):
    company_name = models.CharField(max_length=100)
    website = models.URLField()
    description = models.TextField()

class Job(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    description = models.TextField()
    experience_years = models.IntegerField()
    role = models.CharField(max_length=100)

class Simulation(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)

class SimulationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()

class Questions(models.Model):
    topic = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()

class SimulationQuestions(models.Model):
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)

class QuestionsSources(models.Model):
    source = models.TextField()

class AnswerTip(models.Model):
    simulation_question_answer = models.ForeignKey('SimulationQuestionsAnswer', on_delete=models.CASCADE)
    tip = models.TextField()

class SimulationQuestionsAnswer(models.Model):
    simulation_question = models.ForeignKey(SimulationQuestions, on_delete=models.CASCADE)
    answer = models.TextField()
    score = models.DecimalField(max_digits=5, decimal_places=2)

class ExperienceLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

class Skills(models.Model):
    skill = models.CharField(max_length=100)

class SkillLog(models.Model):
    skill = models.ForeignKey(Skills, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class AudioFile(models.Model):
    question = models.ForeignKey(Questions , on_delete=models.SET_NULL, null=True)
    recording = models.FileField(upload_to='recordings')