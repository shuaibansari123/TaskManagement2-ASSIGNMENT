from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ProjectViewSet, TaskAssignmentViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'tasks2', TasksViewSet, basename='tasks')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'task-assignments', TasksAssignmentViewSet, basename='taskassignment')
router.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]