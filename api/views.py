import random

from faker import Faker
import yaml
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.models import Post, Like
from api.serializers import PostSerializer, LikeSerializer, PostAnalyticsSerializer
from api.services.update_activity import update_user_activity
from users.models import CustomUser


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author')
    serializer_class = PostSerializer

    permission_classes = (IsAuthenticated,)

    @action(methods=['POST'], detail=True)
    def like_post(self, request, pk=None):
        result_response = {'message': 'Something goes wrong'}

        if request.user.is_authenticated:
            user = request.user
            update_user_activity(self, CustomUser)
            post = Post.objects.get(pk=pk)
            like = Like.objects.create(post=post, user=user)
            serializer = LikeSerializer(like, many=False)
            result_response = {'message': 'Post liked', 'result': serializer.data}

        return Response(result_response)

    @action(methods=['POST'], detail=True)
    def unlike_post(self, request, pk=None):
        result_response = {'message': 'Something goes wrong'}

        if request.user.is_authenticated:
            user = request.user
            update_user_activity(self, CustomUser)
            post = Post.objects.get(pk=pk)
            Like.objects.filter(post=post, user=user).delete()
            result_response = {'message': 'Post unliked'}

        return Response(result_response)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        update_user_activity(self, CustomUser)

    def retrieve(self, request, *args, **kwargs):
        update_user_activity(self, CustomUser)
        return super(PostViewSet, self).retrieve(request)

    def list(self, request, *args, **kwargs):
        update_user_activity(self, CustomUser)
        return super(PostViewSet, self).list(request)

    def update(self, request, *args, **kwargs):
        update_user_activity(self, CustomUser)
        return super(PostViewSet, self).update(request)

    def partial_update(self, request, *args, **kwargs):
        update_user_activity(self, CustomUser)
        return super(PostViewSet, self).partial_update(request)

    def destroy(self, request, *args, **kwargs):
        update_user_activity(self, CustomUser)
        return super(PostViewSet, self).destroy(request)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.select_related('user')
    serializer_class = LikeSerializer

    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        update_user_activity(self, CustomUser)
        serializer.save(user_id=self.request.user.pk,
                        post_id=self.request.data['post_id'])

    def retrieve(self, request, *args, **kwargs):
        update_user_activity(self, CustomUser)
        return super(LikeViewSet, self).retrieve(request)

    def list(self, request, *args, **kwargs):
        update_user_activity(self, CustomUser)
        return super(LikeViewSet, self).list(request)

    def update(self, request, *args, **kwargs):
        update_user_activity(self, CustomUser)
        return super(LikeViewSet, self).update(request)

    def partial_update(self, request, *args, **kwargs):
        update_user_activity(self, CustomUser)
        return super(LikeViewSet, self).partial_update(request)

    def destroy(self, request, *args, **kwargs):
        update_user_activity(self, CustomUser)
        return super(LikeViewSet, self).destroy(request)


class AnalyticsViewSet(generics.ListAPIView):
    serializer_class = PostAnalyticsSerializer
    queryset = Post.objects.all()

    def get(self, request, *args, **kwargs):
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        likes_analytic = Like.objects.filter(
            like_date__range=[date_from, date_to]
        ).values('like_date').annotate(
            likes_amount=Count('id')
        ).values('id', 'like_date', 'likes_amount')

        context = [{'like_date': row.like_date, 'likes_amount': row.likes_amount} for row in likes_analytic]

        return Response(context)


def bot_run(request):
    response_log = []

    config = yaml.safe_load(open('bot_config.yml').read())
    fake = Faker()

    number_of_users = config.get('number_of_users', 0)
    max_posts_per_user = config.get('max_posts_per_user', 0)
    max_likes_per_user = config.get('max_likes_per_user', 0)

    users = []
    posts = []

    for _ in range(number_of_users):
        user_data = {
            "email": fake.email(),
            "username": fake.user_name(),
            "password": fake.password(),
        }
        user = User.objects.create(
            email=user_data['email'],
            username=user_data['username'],
            password=user_data['password'],
        )
        users.append(user)
        response_log.append(f'Created user with email: {user_data["email"]}')

        create_posts_number = random.randint(0, max_posts_per_user)
        for _ in range(create_posts_number):
            content = fake.text()
            post = Post.objects.create(content=content, author=user)
            posts.append(post)
            response_log.append(f'Created post {content[:20]}... by {user_data["email"]}')

    for user in users:
        posts_to_like_number = random.randint(0, max_likes_per_user)
        posts_to_like = random.sample(posts, posts_to_like_number)
        for post in posts_to_like:
            post.likers.add(user)
            response_log.append(f'Post {post.content[:15]}... liked by {user.email}')

    return JsonResponse(response_log, safe=False)
