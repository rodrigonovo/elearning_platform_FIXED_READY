# eLearning Platform

This project is an eLearning platform built with Django, which implements the functionalities requested in the final assignment. The application allows different types of users (students and teachers) to interact with courses, materials, and with each other through a real-time chat system and status updates.

## Application Features

The eLearning platform offers the following main functionalities:

* **User Authentication and Profiles**: Users can create secure, password-protected accounts. The application distinguishes between two user types: `students` and `teachers`. Each user has a profile page that displays personal information, such as their name and photo, and any status updates they have posted. These profiles are visible to other users.
* **Course Management**: Teachers can create new courses and upload educational materials (like PDFs). Students can view a list of available courses and enroll in them.
* **Notifications**: The system sends notifications to a teacher when a student enrolls in their course. Similarly, all enrolled students are notified when new material is added to their course.
* **Real-time Communication**: The platform features a real-time chat application built with Django Channels and WebSockets. This functionality is a core requirement of the project and allows for instant messaging between users.
* **Feedback System**: Students can leave feedback and a rating for courses they are enrolled in.
* **Search and Access Control**: Teachers have the ability to search for other teachers and students on the platform. They can also block students from accessing their courses. Students can post status updates on their own profiles.

## Project Structure and Technologies

The project is structured according to the Model-View-Controller (MVC) architectural pattern, a key concept covered in the course.

* **Models**: The database schema is defined in `core/models.py`. It includes models for `User` (extending Django's `AbstractUser`), `Course`, `Enrollment`, `Feedback`, `StatusUpdate`, and `Notification` to appropriately model all data and relationships.
* **Views**: The application logic for serving HTML pages and handling user requests is located in `core/views.py`. These views use decorators and role-based permissions to control access.
* **API**: A RESTful API is implemented in `core/api.py` using the Django REST Framework (DRF). It provides endpoints with serializers and custom permissions (`IsTeacher`, `IsStudent`) to manage user and course data securely.
* **Real-time Chat**: The `chat` application uses Django Channels for handling WebSockets. The consumer logic is in `chat/consumers.py` and routing is defined in `chat/routing.py`.
* **Asynchronous Tasks**: The project leverages asynchronous programming concepts learned in class, such as using Celery for long-running tasks, to improve server responsiveness.

## Setup and Running the Application

This project was developed and tested in a Windows 11 environment using Python 3.12.

1.  **Clone the Repository**:
    ```bash
    git clone [https://github.com/rodrigonovo/elearning_platform_fixed_ready.git](https://github.com/rodrigonovo/elearning_platform_fixed_ready.git)
    cd elearning_platform_fixed_ready
    ```
2.  **Create and Activate a Virtual Environment**:
    ```bash
    py -m venv .venv
    .\.venv\Scripts\Activate.ps1
    ```
3.  **Install Dependencies**: The `requirements.txt` file lists all necessary packages and their versions, ensuring the application loads as required.
    ```bash
    pip install -r requirements.txt
    ```
4.  **Database Setup**:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py seed_demo
    ```
    * The `seed_demo` command populates the database with sample `teacher` and `student` users for demonstration purposes.
5.  **Run the Development Server**:
    ```bash
    python manage.py runserver
    ```
    * **Login Credentials**: The superuser credentials are set during the `createsuperuser` command. The demo users have a username like `teacherX` or `studentY` and the password `password`.

## Unit Testing

The project includes a suite of unit tests, which is a core requirement for a high-quality application. These tests cover the API functionality and ensure the application behaves as expected.

To run the tests, use the following command:

```bash
python manage.py test