# Task Management System API

## Overview

The Task Management System API is a RESTful service designed to manage projects, tasks, task assignments, and comments. It allows users to create, retrieve, update, and delete projects and tasks, as well as assign tasks to users and add comments. The API also includes advanced features such as task completion workflows, overdue task notifications, and project progress calculations.

## Table of Contents

- [Installation](#installation)
- [Authentication](#authentication)
- [API Endpoints](#api-endpoints)
  - [Task Endpoints](#task-endpoints)
  - [Project Endpoints](#project-endpoints)
  - [Task Assignment Endpoints](#task-assignment-endpoints)
  - [Comment Endpoints](#comment-endpoints)
  - [Advanced Features like mixin,overring](#advanced-features)
- [Error Handling](#error-handling)
- [Logging](#logging)
- [Caching](#caching)
- [Filtering]
- [Searching]


## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/shuaibansari123/TaskManagement-Assignment.git
    ```

2. Navigate to the project directory:
    ```bash
    cd TaskManagement-Assignment
    ```

3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

4. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5. Run migrations:
    ```bash
    python manage.py migrate
    ```

6. Start the development server:
    ```bash
    python manage.py runserver
    ```



## API Endpoints
### Task Endpoints

- **GET /tasks2/**: Retrieve a list of tasks.
  - **Parameters**: Supports filtering by `status` and `priority`, searching by `title` and `description`, and ordering by `due_date` and `priority`.

- **GET /tasks2/{id}/**: Retrieve details of a specific task by its ID.

- **POST /tasks2/**: Create a new task.
  - **Body**: 
    ```json
    {
      "title": "Task Title",
      "description": "Task Description",
      "due_date": "YYYY-MM-DD",
      "status": "not_started",
      "priority": 1,
      "project": 1
    }
    ```

- **PUT /tasks2/{id}/**: Update an existing task.
  - **Body**: Similar to task creation.

- **DELETE /tasks2/{id}/**: Delete a specific task.

- **POST /tasks2/{id}/complete/**: Mark a task as completed.
  - **Business Logic**: Only tasks with a status of "In Progress" can be marked as completed.

- **GET /tasks/overdue/**: Retrieve a list of tasks that are overdue.

### Project Endpoints

- **GET /projects/**: Retrieve a list of projects.
  - **Parameters**: Supports searching by `name` and `description`, ordering by `start_date` and `end_date`.

- **GET /projects/{id}/**: Retrieve details of a specific project by its ID.

- **POST /projects/**: Create a new project.
  - **Body**: 
    ```json
    {
      "name": "Project Name",
      "description": "Project Description",
      "start_date": "YYYY-MM-DD",
      "end_date": "YYYY-MM-DD"
    }
    ```

- **PUT /projects/{id}/**: Update an existing project.
  - **Body**: Similar to project creation.

- **DELETE /projects/{id}/**: Delete a specific project.

- **GET /projects/{id}/progress/**: Retrieve the progress of a specific project.
  - **Business Logic**: Calculates the percentage of completed tasks out of the total tasks in the project.

### Task Assignment Endpoints

- **POST /tasks/{id}/assign/**: Assign a task to a user.
  - **Body**:
    ```json
    {
      "user_id": 1
    }
    ```

- **POST /tasks/{id}/unassign/**: Unassign a task from a user.
  - **Body**:
    ```json
    {
      "user_id": 1
    }
    ```

### Comment Endpoints

- **POST /tasks/{id}/comments/**: Add a comment to a task.
  - **Body**:
    ```json
    {
      "user": 1,
      "text": "This is a comment."
    }
    ```

- **GET /tasks/{id}/comments/**: Retrieve all comments on a task.

- **DELETE /tasks/{task_id}/comments/{comment_id}/**: Delete a specific comment.

## Error Handling

The API provides robust error handling with meaningful messages for each scenario:

- `404 Not Found`: Returned when a resource is not found.
- `400 Bad Request`: Returned when request validation fails.
- `500 Internal Server Error`: Returned for unexpected server errors.

## Logging

The API includes comprehensive logging for requests, responses, and business logic events. Logs are written to the console and a log file `task_management.log`, capturing important details without exposing sensitive information.

