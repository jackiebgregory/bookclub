"""View module for handling requests about books"""
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from bookclubapi.models import Book, Reader
from rest_framework import status


class BookView(ViewSet):
    """book club books"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized book instance
        """

        # Uses the token passed in the `Authorization` header
        reader = Reader.objects.get(user=request.auth.user)

        # Create a new Python instance of the Book class
        # and set its properties from what was sent in the
        # body of the request from the client.
        book = Book()
        book.title = request.data["title"]
        book.author = request.data["author"]
        book.reader = reader


        # Try to save the new book to the database, then
        # serialize the book instance as JSON, and send the
        # JSON as a response to the client request
        try:
            book.save()
            serializer = BookSerializer(book, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)


        # If anything went wrong, catch the exception and
        # send a response with a 400 status code to tell the
        # client that something was wrong with its request data
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        """Handle GET requests for single book

        Returns:
            Response -- JSON serialized book instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/games/2
            #
            # The `2` at the end of the route becomes `pk`
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book, context={'request': request})
            return Response(serializer.data)

        except Book.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a book

        Returns:
            Response -- Empty body with 204 status code
        """

        reader = reader.objects.get(user=request.auth.user)

        # Do mostly the same thing as POST, but instead of
        # creating a new instance of Book, get the book record
        # from the database whose primary key is `pk`
        book = Book.objects.get(pk=pk)
        book.title = request.data["title"]
        book.author = request.data["author"]
        book.reader = reader
        
        # game_type = GameType.objects.get(pk=request.data["gameTypeId"])
        # game.game_type = game_type
        # game.save()

        book.save()

        # 204 status code means everything worked but the
        # server is not sending back any data in the response
        return Response({}, status=status.HTTP_204_NO_CONTENT)

      
    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single book

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            book = Book.objects.get(pk=pk)
            book.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Book.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to books resource

        Returns:
            Response -- JSON serialized list of games
        """
        # Get all book records from the database
        books = Book.objects.all()
        

        serializer = BookSerializer(
            books, many=True, context={'request': request})
        return Response(serializer.data)


class BookSerializer(serializers.ModelSerializer):
    """JSON serializer for books

    Arguments:
        serializer type
    """
    class Meta:
        model = Book
        fields = ('id', 'title', 'author')
        depth = 1
