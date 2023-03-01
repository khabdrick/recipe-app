from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Recipe
from .producer import publish
from .serializers import RecipeSerializer
import random


class RecipeView(viewsets.ViewSet):
    def list(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('recipe_created', serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        recipe = Recipe.objects.get(id=pk)
        serializer = RecipeSerializer(instance=recipe, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('recipe_updated', serializer.data)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        recipe = Recipe.objects.get(id=pk)
        recipe.delete()
        publish('recipe_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
