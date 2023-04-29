from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Nutrient(models.Model):
    name = models.CharField(max_length=255)
    calories = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    carbohydrate = models.IntegerField()
    price = models.IntegerField()
    #ratio = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        app_label = 'nutrition'
