"""View module for handling requests about meetings"""
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from bookclubapi.models import Book, Meeting, Reader
from bookclubapi.views.book import BookSerializer


class MeetingView(ViewSet):
    """book club meetings"""

    def create(self, request):
        """Handle POST operations for meetings

        Returns:
            Response -- JSON serialized meeting instance
        """
        reader = Reader.objects.get(user=request.auth.user)

        meeting = Meeting()
        meeting.time = request.data["time"]
        meeting.date = request.data["date"]
        meeting.location = request.data["location"]
        meeting.organizer = reader

        book = Book.objects.get(pk=request.data["book"])
        meeting.book = book

        try:
            meeting.save()
            serializer = MeetingSerializer(meeting, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single meeting

        Returns:
            Response -- JSON serialized meeting instance
        """
        try:
            meeting = Meeting.objects.get(pk=pk)
            serializer = MeetingSerializer(meeting, context={'request': request})
            return Response(serializer.data)
        except Exception:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a meeting

        Returns:
            Response -- Empty body with 204 status code
        """
        # organizer = Reader.objects.get(user=request.auth.user)

        meeting = Meeting.objects.get(pk=pk)
        meeting.description = request.data["description"]
        meeting.date = request.data["date"]
        meeting.time = request.data["time"]
        # meeting.organizer = organizer

        book = Book.objects.get(pk=request.data["bookId"])
        meeting.book = book
        meeting.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single meeting

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            meeting = Meeting.objects.get(pk=pk)
            meeting.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Meeting.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

   
    def list(self, request):
        """Handle GET requests to meetings resource

        Returns:
            Response -- JSON serialized list of meetings
        """
        # Get the current authenticated user
        reader = Reader.objects.get(user=request.auth.user)
        meetings = Meeting.objects.all()

        # Set the `joined` property on every meeting
        for meeting in meetings:
            # Check to see if the reader is in the attendees list on the meeting
            meeting.joined = reader in meeting.readers.all()

        # Support filtering meetings by book
        book = self.request.query_params.get('bookId', None)
        if book is not None:
            meetings = meetings.filter(book__id=type)

        serializer = MeetingSerializer(
            meetings, many=True, context={'request': request})
        return Response(serializer.data)


    @action(methods=['post', 'delete'], detail=True)
    def signup(self, request, pk=None):
        """Managing readers signing up for meetings"""
        # Django uses the `Authorization` header to determine
        # which user is making the request to sign up
        reader = Reader.objects.get(user=request.auth.user)

        try:
            # Handle the case if the client specifies a book
            # that doesn't exist
            meeting = Meeting.objects.get(pk=pk)
        except Meeting.DoesNotExist:
            return Response(
                {'message': 'Event does not exist.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # A reader wants to sign up for a meeting
        if request.method == "POST":
            try:
                # Using the attendees field on the meeting makes it simple to add a reader to the meeting
                # .add(reader) will insert into the join table a new row the reader_id and the meeting_id
                meeting.attendees.add(reader)
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception as ex:
                return Response({'message': ex.args[0]})

        # User wants to leave a previously joined meeting
        elif request.method == "DELETE":
            try:
                # The many to many relationship has a .remove method that removes the reader from the attendees list
                # The method deletes the row in the join table that has the reader_id and meeting_id
                meeting.attendees.remove(reader)
                return Response(None, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return Response({'message': ex.args[0]})

    
class MeetingUserSerializer(serializers.ModelSerializer):
    """JSON serializer for meeting organizer's related Django user"""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class MeetingReaderSerializer(serializers.ModelSerializer):
    """JSON serializer for meeting organizer"""
    user = MeetingUserSerializer(many=False)

    class Meta:
        model = Reader
        fields = ['user']  
        
class MeetingSerializer(serializers.ModelSerializer):
    """JSON serializer for meetings"""
    organizer = MeetingReaderSerializer(many=False)
    book = BookSerializer(many=False)

    class Meta:
        model = Meeting
        fields = ('id', 'reader', 'book',
                 'date', 'time', 'location',
                'joined')


class BookSerializer(serializers.ModelSerializer):
    """JSON serializer for books"""
    class Meta:
        model = Book
        fields = ('id', 'title', 'author')
