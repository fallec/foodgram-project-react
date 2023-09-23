import base64

from rest_framework import serializers
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404

from .models import Favorite, User, ShoppingList
from recipes.models import Recipe, RecipeTag, RecipeIngredient, Tag
from ingredients.models import Ingredient
from users.serializers import UserSerializer


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Recipe serializer for adding to favorite."""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class Base64ImageField(serializers.ImageField):
    """Serializer for converting base64 into image."""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]

            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class RecipeIngredientListSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')
    id = serializers.ReadOnlyField(source='ingredient.id')

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount',)


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField(min_value=1, max_value=100)

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount',)


class RecipeTagListSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='tag.name')
    color = serializers.ReadOnlyField(source='tag.color')
    slug = serializers.ReadOnlyField(source='tag.slug')
    id = serializers.ReadOnlyField(source='tag.id')

    class Meta:
        model = RecipeTag
        fields = ('id', 'name', 'color', 'slug',)


class RecipeTagField(serializers.Field):
    id = serializers.ListField()

    class Meta:
        fields = ('id',)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipes model."""
    image = Base64ImageField(required=True)
    ingredients = RecipeIngredientSerializer(required=True, many=True)
    author = UserSerializer(read_only=True)
    tags = serializers.ListField(required=True)

    class Meta:
        model = Recipe
        fields = ('tags',
                  'ingredients',
                  'author',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

    def to_representation(self, instance):
        return RecipeListSerializer(
            instance, context={'request': self.context.get('request')}).data

    def validate(self, data):
        ingredients = data.get('ingredients')
        tags = data.get('tags')
        if not (ingredients and tags):
            raise serializers.ValidationError()
        checklist = []
        for ingredient in ingredients:
            if ingredient.get('id') in checklist:
                raise serializers.ValidationError()
            checklist.append(ingredient.get('id'))
        checklist = []
        for tag in tags:
            if tag in checklist:
                raise serializers.ValidationError()
            if not Tag.objects.filter(id=tag).exists():
                raise serializers.ValidationError()
            checklist.append(tag)
        return data

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = []
        if 'ingredients' in self.initial_data:
            ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)

        for tag in tags:
            current_tag = get_object_or_404(Tag, id=tag)
            RecipeTag.objects.create(recipe=recipe, tag=current_tag)
        if not ingredients:
            return recipe
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            )
        return recipe

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.image = validated_data.get('image', instance.image)

        tags = validated_data.pop('tags')
        instance.tags.clear()
        for tag in tags:
            current_tag = get_object_or_404(Tag, id=tag)
            RecipeTag.objects.create(recipe=instance, tag=current_tag)

        if 'ingredients' not in validated_data:
            instance.save()
            return instance

        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=instance,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount')
            )

        instance.save()
        return instance


class RecipeListSerializer(serializers.ModelSerializer):
    """Serializer for list Recipes model."""
    ingredients = RecipeIngredientListSerializer(
        required=True, many=True, source='r_ingredients')
    author = UserSerializer(read_only=True)
    tags = RecipeTagListSerializer(required=True, many=True, source='r_tags')
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id',
                  'tags',
                  'author',
                  'ingredients',
                  'is_favorited',
                  'is_in_shopping_cart',
                  'name',
                  'image',
                  'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and Favorite.objects.filter(
            user=user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and ShoppingList.objects.filter(
            user=user,
            recipe=obj
        ).exists()


class SubscribeSerializer(UserSerializer):
    """Subscribe serializer."""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        recipes_limit = self.context[
            'request'
        ].query_params.get('recipes_limit', 'f')

        if not recipes_limit.isdigit():
            recipes_limit = None
        else:
            recipes_limit = int(recipes_limit)

        data = obj.recipes.all()[:recipes_limit]
        return FavoriteRecipeSerializer(instance=data, many=True).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
