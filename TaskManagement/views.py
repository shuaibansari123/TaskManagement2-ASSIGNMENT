from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Task
from .serializers import TaskSerializer
from .exceptions import TaskNotFoundException
from django.core.cache import cache
import logging
from rest_framework.pagination import PageNumberPagination


logger = logging.getLogger(__name__)

# Custom Mixin for common functionality like logging, alert system with async queue(celery)
class CustomLoggingMixin:
    def log_request(self, request):
        logger.info(f"Request method: {request.method}, path: {request.path}, user: {request.user}")

class TaskPagination(PageNumberPagination):
    page_size = 10  

class TaskViewSet(CustomLoggingMixin, viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter] 
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority']
    filterset_fields = ['status', 'priority']
    
    pagination_class = TaskPagination
    page_size = 10
    
    
     

    def list(self, request, *args, **kwargs):
        self.log_request(request)
        queryset = cache.get('tasks_list')
        if not queryset:
            queryset = self.filter_queryset(self.get_queryset())
            cache.set('tasks_list', queryset, timeout=60*5)  
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.log_request(request)
        cache.delete('tasks_list')  
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.log_request(request)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.log_request(request)
        print('worked....')
        cache.delete('tasks_list')  # Invalidate cache on update
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.log_request(request)
        cache.delete('tasks_list')  # Invalidate cache on delete
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'], url_path='completed')
    def completed_tasks(self, request):
        """Retrieve completed tasks only."""
        self.log_request(request)
        completed_tasks = Task.objects.filter(status='completed')
        serializer = self.get_serializer(completed_tasks, many=True)
        return Response(serializer.data)

    def get_object(self):
        try:
            return super().get_object()
        except Task.DoesNotExist:
            raise TaskNotFoundException()

    def perform_create(self, serializer):
        """Override to add custom behavior for object creation."""
        
        try:
            task = serializer.save()
            logger.info(f"Task '{task.title}' created with ID {task.id}")
        except Exception as e:
            logger.error(f"ERROR IN TASK CREATE = " , str(e))

            
    def perform_update(self, serializer):
        try:
            task = serializer.save()
            logger.info(f"Task '{task.title}' updated with ID {task.id}")
        except Exception as e:
            logger.error(f"ERROR IN TASK CREATE = " , str(e))
