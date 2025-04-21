from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    name= models.CharField(max_length=100)
    description = models.TextField()
    user= models.ForeignKey(User, on_delete=models.CASCADE)
    created_at =models.DateTimeField(auto_now_add=True)

    def progress(self):
        total_tasks = self.tasks.count()
        if total_tasks == 0:
            return 0
        completed_tasks = self.tasks.filter(status='Completed').count()
        return (completed_tasks / total_tasks) * 100

    def __str__(self):
        return self.name
    

class Task(models.Model):
    STATUS_CHOICES = (
    ('Not Started', 'Not Started'),
    ('In Progress', 'In Progress'),
    ('Completed', 'Completed'),
)   
    project= models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    title =models.CharField(max_length=100)
    description=models.TextField()
    due_date=models.DateField()
    status=models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
