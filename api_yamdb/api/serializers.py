import datetime

from django.db.models import Avg
from django.forms import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comments, Genre, Review, Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=False,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = ('__all__')

    def validate_year(self, value):
        if value > datetime.date.today().year:
            raise serializers.ValidationError('Год больше текущего')
        return value


class ReviewSerializer(serializers.ModelSerializer):

    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())

    class Meta:
        exclude = ['title']
        model = Review
        validators = []

    def validate(self, attrs):
        method = self.context.get('request').method
        if method == 'POST':
            title_id = (self.context.get('request').
                        parser_context.get('kwargs').get('title_id'))
            title = get_object_or_404(Title, pk=title_id)
            user = self.context.get('request').user
            title_review_pair = (user.reviews.
                                 filter(title__exact=title).exists())
            if title_review_pair:
                raise ValidationError('Нельзя создать более одного ревью.')
        return attrs


class CommentsSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True,
                              default=serializers.CurrentUserDefault())

    class Meta:
        exclude = ['review']
        model = Comments


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, required=True)
    genre = GenreSerializer(many=True, required=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )

    def get_rating(self, obj):
        avg_score = obj.reviews.all().aggregate(Avg('score'))
        rating = round(avg_score['rating'], 0)
        return rating
