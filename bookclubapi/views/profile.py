from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from bookclubapi.models import Meeting, Reader, Book


class Profile(ViewSet):
    """Reader can see profile information"""

    def list(self, request):
        """Handle GET requests to profile resource

        Returns:
            Response -- JSON representation of user info and meetings
        """
        reader = reader.objects.get(user=request.auth.user)
        meetings = Meeting.objects.filter(attendees=reader)

        meetings = MeetingSerializer(
            meetings, many=True, context={'request': request})
        reader = ReaderSerializer(
            reader, many=False, context={'request': request})

        # Manually construct the JSON structure you want in the response
        profile = {}
        profile["reader"] = reader.data
        profile["meetings"] = meetings.data

        return Response(profile)

class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for reader's related Django user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')


class ReaderSerializer(serializers.ModelSerializer):
    """JSON serializer for readers"""
    user = UserSerializer(many=False)

    class Meta:
        model = Reader
        fields = ('user', 'bio')


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
