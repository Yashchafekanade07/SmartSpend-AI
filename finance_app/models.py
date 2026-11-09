from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.title} - {self.amount}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    monthly_limit = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.IntegerField()
    year = models.IntegerField()
    class Meta:
        unique_together = ('user', 'category', 'month', 'year')
