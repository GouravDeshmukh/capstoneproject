from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator



class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    team_members = models.TextField()  # You can handle team members as a text field or create a separate model
    faculty_members = models.TextField()
    department = models.CharField(max_length=100)
    university = models.CharField(max_length=200)
    description = models.TextField()
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    document = models.FileField(upload_to='documents/', blank=True, null=True)
    # Add multiple ImageFields to the Project model
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='projects', blank=True)  # Add this line
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # To associate project with the user
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    @property
    def average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            return sum([review.rating for review in reviews]) / reviews.count()
        return 0

class Review(models.Model):
    project = models.ForeignKey(Project, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['project', 'user']  # Ensure a user can review a project only once

    def __str__(self):
        return f"{self.user.username} - {self.project.title} ({self.rating} stars)"