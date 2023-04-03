from rest_framework import serializers

from api.models import Post, Like


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'creation_date', 'author', 'likers']

    @staticmethod
    def get_author(obj):
        return obj.author.username


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user_id', 'post_id', 'date_liked']


class PostAnalyticsSerializer(serializers.ModelSerializer):
    like_date = serializers.DateField()
    likes_amount = serializers.IntegerField()

    class Meta:
        model = Post
        fields = ('date_liked', 'likes_amount')
