from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from yamdb_auth.permissions import (IsAdminOrReadOnly,
                                    IsAuthenticatedOrReadOnly,
                                    IsAuthorAdminModeratorOrReadOnly)

from .filters import TitleFilter
from .models import Category, Comment, Genre, Review, Title
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TitleSlugSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorAdminModeratorOrReadOnly
    ]

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(title=title, author=self.request.user)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        queryset = Review.objects.filter(title=title)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly, IsAuthorAdminModeratorOrReadOnly
    ]

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            title_id=self.kwargs['title_id'],
            id=self.kwargs['review_id']
        )
        serializer.save(review=review, author=self.request.user)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        comments = review.reviews_comments.all()
        return comments


class CategoryGenreViewSet(viewsets.GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin
                           ):
    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GenreViewSet(CategoryGenreViewSet):
    queryset = Genre.objects.all()
    lookup_field = 'slug'
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = PageNumberPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class CategoryViewSet(CategoryGenreViewSet):
    queryset = Category.objects.all()
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly, ]
    pagination_class = PageNumberPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().annotate(
        rating=Avg('titles_reviews__score')).order_by('-id')
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filter_class = TitleFilter
    filterset_fields = ['category', 'genre', 'year', 'name']

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSlugSerializer
        return TitleSerializer
