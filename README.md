# Django Task Management System API

## Overview

This project is a RESTful API for a Task Management System built with Django and Django REST Framework (DRF). It allows users to perform CRUD operations on tasks with properties such as title, description, status, priority, and due date. The project includes advanced features like custom filters and efficient logging.

## Features

- **Task Management:** Create, read, update, and delete tasks.
- **Filtering:** Filter tasks based on status, priority, and due date.
- **Logging:** Detailed logging setup for development and production environments.
- **HIGHLY CUSTOMIZABLE:**  highly costomizable class based views, serializers, 
- **Advance Modular and Reusable Code:** by use of Mixins, Method Overriding, Custom TestCases, and many more
- **Caching:** i have used caching for reduce database load in production we can use distributed cache like redis or memcach with connection pooling
- **Faker:**  Generate fake data for testing purpose. using "python create_fake_data.py" or "python manage.py create_fake_data" 
- **Pagination:** for large response data, i implemeneted pagination for quick response
- **Documentation:** API documentation using DRF-YASG.


### Prerequisites

- Python 3.8+

### Setup

1. **Clone the Repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
Install Dependencies:

Create a virtual environment (recommended) and install the required packages:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
Configure Environment:

Ensure your .env file or environment variables are set up for database and secret key settings.

Run Migrations:
python manage.py  makemigrations
python manage.py migrate

Create a Superuser:
python manage.py createsuperuser

Run the Development Server:
Start the development server to run the API:

python manage.py runserver

optional:
  in other ternimal use can use this to Generate fake data for testing purpose. 
    "python create_fake_data.py" or "python manage.py create_fake_data" 


API Endpoints

Base URL
  http://localhost:8000/

Endpoints
  List Tasks
      URL: /tasks/
      Method: GET
      Description: Retrieve a list of tasks with pagination.
      Query Parameters:
      search: Search by title or description.
      ordering: Order by due_date or priority.
      status: Filter by task status.
      priority: Filter by task priority.
      Response:
      200 OK: Returns a paginated list of tasks.

  Create Task
      URL: /tasks/
      Method: POST
      Description: Create a new task.
      Request Body:
      {
        "title": "string",
        "description": "string",
        "status": "string",
        "priority": "string",
        "due_date": "YYYY-MM-DD"
      }
      Response:
      201 Created: Returns the created task.

  Retrieve Task
      URL: /tasks/{id}/
      Method: GET
      Description: Retrieve details of a specific task by its ID.
      Response:
      200 OK: Returns the task details.
      404 Not Found: If the task does not exist.

  Update Task
      URL: /tasks/{id}/
      Method: PUT
      Description: Update an existing task.
      Request Body:
      {
        "title": "string",
        "description": "string",
        "status": "string",
        "priority": "string",
        "due_date": "YYYY-MM-DD"
      }
      Response:
      200 OK: Returns the updated task.
      404 Not Found: If the task does not exist.
      

  Delete Task
      URL: /tasks/{id}/
      Method: DELETE
      Description: Delete a specific task.
      Response:
      204 No Content: If the task is successfully deleted.
      404 Not Found: If the task does not exist.

  Retrieve Completed Tasks
      URL: /tasks/completed/
      Method: GET
      Description: Retrieve a list of tasks with status 'completed'.
      Response:
      200 OK: Returns a list of completed tasks.


** API Usage **

Pagination
The API supports pagination with a page size of 10 tasks per page. You can navigate through pages using query parameters.

Caching
The API caches the list of tasks for 5 minutes to improve performance. The cache is invalidated on task creation, update, or deletion.

Logging
I used Custom Mixin to Requests logged with details such as method, path, and user for debugging and monitoring purposes and this project uses Django’s logging framework with both file and console handlers. Logs are stored in the logs/django.log file.

API Documentation
API documentation is available at /swagger/ (configured using DRF-YASG).

Testing
Ensure you have all dependencies installed and run tests with:

python manage.py test
or 
pytest

For any questions or comments, please contact shuaibansari4044@gmail.com.

### Key Points

- **Setup Instructions:** Step-by-step guide to getting the project up and running.
- **API Endpoints:** Basic information on available endpoints.
- **Logging Configuration:** Basic information on logging.
- **Documentation URL:** Where to find the auto-generated API documentation.
- **Contributing:** Instructions for contributing to the project.





