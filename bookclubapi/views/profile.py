from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from bookclubapi.models import Meeting, Reader, Book
from bookclubapi.views.book import BookSerializer

class Profile(ViewSet):
    """Reader can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and meetings
        """
        me = request.auth.user.reader
        meetings = Meeting.objects.filter(organizer=me)
        books = Book.objects.filter()

        meetings = MeetingSerializer(
            meetings, many=True, context={'request': request})
        reader = ReaderSerializer(
            me, many=False, context={'request': request})
        books = BookSerializer(
            books, many=True, context={'request': request})

        # Manually construct the JSON structure you want in the response
        profile = {}
        profile["reader"] = reader.data
        profile["mymeetings"] = meetings.data
        profile["mybooks"] = books.data

        return Response(profile)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for reader's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')

class BookSerializer(serializers.ModelSerializer):
    """JSON serializer for books"""
    class Meta:
        model = Book
        fields = ('title','author')


class MeetingSerializer(serializers.ModelSerializer):
    """JSON serializer for meetings"""
    book = BookSerializer(many=False)

    class Meta:
        model = Meeting
        fields = ('id', 'book',
                 'date', 'time', 
                 'location', 'organizer', 'joined')


class ReaderSerializer(serializers.ModelSerializer):
    """JSON serializer for readers"""
    user = UserSerializer(many=False)
    attending = MeetingSerializer(many=True)
    class Meta:
        model = Reader
        fields = ('user', 'bio', 'attending')
