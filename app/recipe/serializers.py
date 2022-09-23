"""
Serializers for recipe APIs
"""
from rest_framework import serializers

from core.models import (
    Recipe,
    Tag,
)


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tags."""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes."""
    #many=True means tags is a list of tage, required=False means tag is optional
    tags = TagSerializer(many=True, required=False)
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id'] #you don't want user to edit it, just view it

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', []) #remove tags from validated_data, if not exsited then return []
        recipe = Recipe.objects.create(**validated_data) #create recipe without tag
        auth_user = self.context['request'].user
        for tag in tags:
            #create tags with validated tags
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj) #you can only add tags to recipe once it's a instance in model

        return recipe

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']


