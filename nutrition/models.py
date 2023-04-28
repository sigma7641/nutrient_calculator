from django.db import models

class Nutrient(models.Model):
    name = models.CharField(max_length=255)
    calories = models.IntegerField()
    protein = models.IntegerField()
    fat = models.IntegerField()
    carbohydrate = models.IntegerField()

    def __str__(self):
        return self.name
    class Meta:
        app_label = 'nutrition'
