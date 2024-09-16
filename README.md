# QuizMaster

QuizMaster is a Django-based web application for creating and taking quizzes. It's designed to provide an interactive and engaging platform for users to test their knowledge across various topics.

## Features

- Create and manage quizzes with multiple-choice questions
- Take quizzes and receive instant feedback
- User profiles with quiz history and statistics
- Responsive design for desktop and mobile devices
- HTMX integration for dynamic content loading
- Dark mode support

## Technologies Used

- Django 5.1.1
- Python 3.x
- HTMX for dynamic interactions
- Tailwind CSS for styling
- SQLite database (default)

## Setup and Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/quizmaster.git
   cd quizmaster
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Apply the database migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Visit `http://127.0.0.1:8000` in your web browser to see the application.

## Usage

- Use the admin interface (`http://127.0.0.1:8000/admin/`) to create quizzes and manage users.
- Register a new account or log in to an existing one to start taking quizzes.
- Create your own quizzes and share them with others.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Django documentation
- HTMX documentation
- Tailwind CSS documentation

## Contact

For any queries or support, please contact [Your Name] at [your.email@example.com].

