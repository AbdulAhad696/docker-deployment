from .models import Patient
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
# from .serializers import BookSerializer

# class BookListCreateView(generics.ListCreateAPIView):
#     serializer_class = BookSerializer 
    
#     def get_queryset(self):
#         return Book.objects.all() 
    
#     def get(self, request, *args, **kwargs):
#         # print(request.method)
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
    
    # def post(self, request, *args, **kwargs):
    #     print("idher aya mein heheheheh")

# class BookRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer


# class BookListCreateView(APIView):
#     def get(self, request):
#         books = Book.objects.all()
#         serializer = BookSerializer(books, many=True)
#         print("IDHER AYA MEIN")
#         print(serializer.data)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = BookSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# class BookRetrieveUpdateDeleteView(APIView):
#     def get(self, request, pk):
#         try:
#             book = Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = BookSerializer(book)
#         return Response(serializer.data)
    
#     def put(self, request, pk):
#         try:
#             book = Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         serializer = BookSerializer(book, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk):
#         try:
#             book = Book.objects.get(pk=pk)
#         except Book.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
        
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)