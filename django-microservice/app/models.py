from django.db import models

class Recipe(models.Model):
    """Recipe object"""
    title = models.CharField(max_length=255)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(max_length=1000)
    ingredients = models.TextField(max_length=500)
    def __str__(self):
        return self.title

class RecipeComment(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    comment_text = models.TextField()

    def __str__(self):
        return self.comment_text