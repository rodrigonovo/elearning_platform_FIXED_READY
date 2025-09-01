/*
Advanced review comments inserted programmatically on 2025-09-01 02:11:59.
Generic text-based artifact belonging to the eLearning platform.
*/

# eLearning Platform

This project is an eLearning platform built with Django, implementing the features specified in the final assignment. The application allows different user roles (students and teachers) to interact with courses, materials, and each other through a real-time chat system and status updates.

## Implemented Functionality

The eLearning platform offers the following main functionalities:

* **User Authentication and Profiles**: Users can create secure, password-protected accounts. The application distinguishes between `students` and `teachers` with different permissions. User profiles display information like name and photo, and also show status updates, which are visible to other users.
* **Course Management**: Teachers can create new courses and upload materials (like PDFs). Students can view a list of available courses and enroll in them.
* **Notifications**: The system sends notifications to a teacher when a student enrolls in a course, and to enrolled students when new materials are added.
* **Real-time Communication**: The application includes a real-time chat feature using WebSockets, built with Django Channels and Daphne.
* **Feedback System**: Students can leave feedback and a rating for courses they are enrolled in.
* **Search and Access Control**: Teachers can search for students and other teachers. They can also block students from their courses.

## Project Structure and Technologies

The project follows the Model-View-Controller (MVC) architectural pattern, a key concept covered in the course.

* **Models**: The database models (`User`, `Course`, `Enrollment`, `Feedback`, `StatusUpdate`, `Notification`) are defined in `core/models.py`. The `User` model extends Django's `AbstractUser` to include custom fields like `role`, `real_name`, and `photo`.
* **Views**: The application logic for rendering HTML pages is in `core/views.py`. These views use decorators and role-based redirects to control access.
* **API**: A RESTful API is implemented using the Django REST Framework (DRF) in `core/api.py`. It uses ViewSets for each model and includes custom permissions (`IsTeacher`, `IsStudent`, `IsEnrolledStudent`) to enforce access control.
* **Real-time Chat**: The `chat` application uses Django Channels for WebSockets. WebSocket routing is in `chat/routing.py`, and the consumer logic is in `chat/consumers.py`.

## Setup and Running the Application

This project was developed and tested in a Windows 11 environment using Python 3.12.

1.  **Clone the repository**:
    ```bash
    git clone [https://github.com/rodrigonovo/elearning_platform_fixed_ready.git](https://github.com/rodrigonovo/elearning_platform_fixed_ready.git)
    cd elearning_platform_fixed_ready
    ```
2.  **Create and activate the virtual environment**:
    ```powershell
    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```
3.  **Install dependencies**:
    ```powershell
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt
    ```
    - The dependencies are listed in `requirements.txt`.
4.  **Execute database migrations**:
    ```powershell
    python manage.py makemigrations
    python manage.py migrate
    ```
5.  **Create a superuser (admin) and demo data**:
    ```powershell
    python manage.py createsuperuser
    python manage.py seed_demo
    ```
    - The `seed_demo` command creates sample teachers and students with the password `password`.
6.  **Collect static files**:
    ```powershell
    python manage.py collectstatic --noinput
    ```
7.  **Run the ASGI server (Daphne)**:
    ```powershell
    daphne elearning_platform.asgi:application
    ```
    - The application uses `daphne` to serve both HTTP and WebSocket connections, as configured in `elearning_platform/asgi.py`.
    
    - **Login Credentials**: The `superuser` credentials are set with `createsuperuser`. The demo users have a `username` of `teacherX` or `studentY` and the password is `password` for all.

## Unit Testing

The application includes unit tests to ensure the functionality and robustness of the code, particularly for the API endpoints.

To run the tests, use the following command:
```powershell
python manage.py test