import factory
from factory import Faker
from .models import Task
from django.utils import timezone
import random

class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = Faker('sentence', nb_words=4)
    description = Faker('text', max_nb_chars=200)
    status = factory.Iterator(['To Do', 'In Progress', 'Completed'])
    priority = factory.Iterator(['Low', 'Medium', 'High'])
    due_date = factory.LazyAttribute(lambda _: timezone.now() + timezone.timedelta(days=random.randint(1, 30)))