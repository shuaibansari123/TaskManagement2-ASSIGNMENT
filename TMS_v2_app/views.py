from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Taskss, Project, TasksAssignment, Comment
from .serializers import TasksSerializer, ProjectSerializer, TasksAssignmentSerializer, CommentSerializer, ProjectProgressSerializer
from .exceptions import TasksNotFoundException
from django.core.cache import cache
import logging
from rest_framework.pagination import PageNumberPagination
from datetime import date

logger = logging.getLogger(__name__)

class CustomLoggingMixin:
    def log_request(self, request):
        logger.info(f"Request method: {request.method}, path: {request.path}, user: {request.user}")

class TasksPagination(PageNumberPagination):
    page_size = 10

class TasksViewSet(CustomLoggingMixin, viewsets.ModelViewSet):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority']
    filterset_fields = ['status', 'priority']
    pagination_class = TasksPagination

    def list(self, request, *args, **kwargs):
        self.log_request(request)
        queryset = cache.get('Taskss_list')
        if not queryset:
            queryset = self.filter_queryset(self.get_queryset())
            cache.set('Taskss_list', queryset, timeout=60*5)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        self.log_request(request)
        cache.delete('Taskss_list')
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        self.log_request(request)
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        self.log_request(request)
        cache.delete('Taskss_list')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.log_request(request)
        cache.delete('Taskss_list')
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], url_path='complete')
    def complete_Task(self, request, pk=None):
        # Mark a Tasks as completed.
        Tasks = self.get_object()
        if Tasks.status != 'in_progress':
            return Response({'error': 'Only Taskss in progress can be marked as completed.'}, status=status.HTTP_400_BAD_REQUEST)
        Tasks.status = 'completed'
        Tasks.save()
        logger.info(f"Tasks '{Tasks.title}' marked as completed.")
        return Response({'status': 'Tasks marked as completed.'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='overdue')
    def overdue_Tasks(self, request):
        #Retrieve overdue Taskss.
        self.log_request(request)
        today = date.today()
        overdue_Taskss = Tasks.objects.filter(due_date__lt=today, status__in=['not_started', 'in_progress'])
        serializer = self.get_serializer(overdue_Taskss, many=True)
        return Response(serializer.data)

    def get_object(self):
        try:
            return super().get_object()
        except Tasks.DoesNotExist:
            raise TasksNotFoundException()

    def perform_create(self, serializer):
        Tasks = serializer.save()
        logger.info(f"Tasks '{Tasks.title}' created with ID {Tasks.id}")

    def perform_update(self, serializer):
        Tasks = serializer.save()
        logger.info(f"Tasks '{Tasks.title}' updated with ID {Tasks.id}")

class ProjectViewSet(CustomLoggingMixin, viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'end_date']
    filterset_fields = ['name', 'start_date']

    @action(detail=True, methods=['get'], url_path='progress')
    def project_progress(self, request, pk=None):
        #Calculate project progress.#
        project = self.get_object()
        total_Taskss = project.Taskss.count()
        completed_Taskss = project.Taskss.filter(status='completed').count()
        if total_Taskss > 0:
            progress_percentage = (completed_Taskss / total_Taskss) * 100
        else:
            progress_percentage = 0.0
        serializer = ProjectProgressSerializer({'project_id': project.id, 'progress_percentage': progress_percentage})
        return Response(serializer.data)

class TasksAssignmentViewSet(CustomLoggingMixin, viewsets.ModelViewSet):
    queryset = TasksAssignment.objects.all()
    serializer_class = TasksAssignmentSerializer

    @action(detail=True, methods=['post'], url_path='assign')
    def assign_Tasks(self, request, pk=None):
        #Assign a Tasks to a user.#
        Tasks = self.get_object()
        user_id = request.data.get('user_id')
        user = User.objects.get(id=user_id)
        TasksAssignment.objects.create(Tasks=Tasks, user=user)
        logger.info(f"Tasks '{Tasks.title}' assigned to user '{user.username}'.")
        return Response({'status': f'Tasks assigned to {user.username}.'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='unassign')
    def unassign_Tasks(self, request, pk=None):
        #Unassign a Tasks from a user.#
        Tasks = self.get_object()
        user_id = request.data.get('user_id')
        TasksAssignment.objects.filter(Tasks=Tasks, user_id=user_id).delete()
        logger.info(f"Tasks '{Tasks.title}' unassigned from user with ID {user_id}.")
        return Response({'status': 'Tasks unassigned.'}, status=status.HTTP_200_OK)

class CommentViewSet(CustomLoggingMixin, viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        self.log_request(request)
        return super().create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        self.log_request(request)
        return super().destroy(request, *args, **kwargs)
