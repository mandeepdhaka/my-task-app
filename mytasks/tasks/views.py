from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Task
from .serializers import MyTokenObtainPairSerializer, TaskSerializer, UserSerializer


class CheckAuthenticationView(generics.ListCreateAPIView): 
    """
    Used to landing page 
    """ 
    def get(
        self,
        request,
        *args,
        **kwargs
    ):
        if request.user.is_authenticated:
            # Render the home page if the user is authenticated
            return render(
                request,
                'tasks/home.html'
            )
        else:
            # Redirect to the login page if the user is not authenticated
            return redirect('/login/') 
        
class RegisterView(generics.CreateAPIView):
    """
    This view is used to register the user in My task app
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)


class MyTokenObtainPairView(TokenObtainPairView):
    """
    This view is used to get the token of the logging in user
    """
    serializer_class = MyTokenObtainPairSerializer



class AddTaskView(generics.CreateAPIView):
    """
    This view is used to add the tasks of the user 
    """
    
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(
        self,
        serializer
    ):
        serializer.save(user=self.request.user)

class ListTaskView(generics.ListAPIView):
    """
    This view is used to reterive task list of the user
    """
    
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('due_date')
    

class TaskSearchView(generics.ListAPIView):
    """
    This view is used to search the task of the user on the basis of title
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = TaskSerializer

    def get_queryset(self):
        
        queryset = Task.objects.filter(
            user=self.request.user,
        )
        
        title = self.request.query_params.get('title', None)
        if title:
            queryset = queryset.filter(title__icontains=title)
            
        return queryset
    

class TaskDeleteView(generics.DestroyAPIView):
    """
    This view is used to delete the created tasks
    """
    
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != request.user:
            return Response(
                {
                    "error": "You do not have permission to delete this task."
                },
                status=status.HTTP_403_FORBIDDEN
            )
            
        task.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
        
        
class LogoutView(APIView):
    """
    This view is used to logut the user 
    """
    
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            access_token = request.data.get("access")


            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()

            if access_token:
                access_token_obj = AccessToken(access_token)
                access_token_obj.blacklist()

            return Response(
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                status=status.HTTP_400_BAD_REQUEST
            )