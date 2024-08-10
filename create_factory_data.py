import os
import django
from django.utils import timezone

# Set up Django environment otherwise this script wont run
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TMS_v1.settings')  
django.setup()

from TaskManagement.factories import TaskFactory 


def create_fake_tasks(count=100):
    for _ in range(count):
        TaskFactory()


if __name__ == "__main__":
    create_fake_tasks()