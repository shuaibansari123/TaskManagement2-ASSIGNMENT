from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase

from .models import Task
from .factories import TaskFactory

class TaskAPITest(APITestCase):
    def setUp(self):
        self.task = TaskFactory()

    def test_task_creation(self):
        url = reverse('task-list')
        data = {
            'title': 'New Task',
            'description': 'A new task description',
            'status': 'todo',
            'priority': 'high',
            'due_date': '2024-12-31',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Task.objects.count(), 2)

    def test_task_list(self):
        url = reverse('task-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        
    def test_completed_tasks(self):
        url = reverse('task-completed-tasks')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)


class TaskTests(TestCase):

    def test_create_task(self):
        # Create a single task instance
        task = TaskFactory()
        self.assertEqual(task.status, 'To Do') 
        self.assertIsInstance(task.title, str)
        self.assertIsInstance(task.description, str)
        self.assertIsNotNone(task.due_date)