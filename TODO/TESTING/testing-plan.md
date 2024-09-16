# Testing Plan for QuizMaster

## 1. Manual Testing

### 1.1 Home Page
- Verify that the home page loads correctly
- Check that the list of quizzes is displayed
- Test pagination (if implemented)
- Ensure all links are working (e.g., to individual quizzes, user profile)

### 1.2 Quiz Creation
- Test creating a new quiz with valid data
- Test creating a quiz with invalid data (form validation)
- Check if questions and answers can be added dynamically
- Verify that the quiz is saved correctly in the database

### 1.3 Quiz Taking
- Start a quiz and verify that questions are displayed correctly
- Test answering questions and moving to the next question
- Check that the quiz can be completed
- Verify that the results are calculated and displayed correctly

### 1.4 User Profile
- View a user profile and check if all information is displayed correctly
- Test editing user profile information (if implemented)
- Verify that quiz history is displayed accurately

### 1.5 Error Handling
- Test accessing non-existent quizzes or user profiles
- Check for appropriate error messages

## 2. Automated Testing with Django Test Tools

### 2.1 Set Up Test Environment
```python
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Quiz, Question, Answer, QuizAttempt

class QuizMasterTestCase(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        
        # Create test quiz
        self.quiz = Quiz.objects.create(
            title='Test Quiz',
            description='A quiz for testing',
            creator=self.user
        )
        
        # Create test question and answers
        self.question = Question.objects.create(
            quiz=self.quiz,
            text='What is the capital of France?'
        )
        Answer.objects.create(question=self.question, text='London', is_correct=False)
        Answer.objects.create(question=self.question, text='Paris', is_correct=True)
        Answer.objects.create(question=self.question, text='Berlin', is_correct=False)
        
        self.client = Client()
```

### 2.2 Test Views
```python
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Quiz')

    def test_quiz_detail_view(self):
        response = self.client.get(reverse('quiz_detail', args=[self.quiz.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Quiz')
        self.assertContains(response, 'What is the capital of France?')

    def test_quiz_take_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('quiz_take', args=[self.quiz.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'What is the capital of France?')

    def test_profile_view(self):
        response = self.client.get(reverse('profile', args=[self.user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
```

### 2.3 Test Forms
```python
    def test_quiz_creation_form(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('quiz_create'), {
            'title': 'New Quiz',
            'description': 'A new quiz for testing',
            'questions-TOTAL_FORMS': '1',
            'questions-INITIAL_FORMS': '0',
            'questions-MIN_NUM_FORMS': '0',
            'questions-MAX_NUM_FORMS': '1000',
            'questions-0-text': 'Test question',
            'questions-0-answers-TOTAL_FORMS': '3',
            'questions-0-answers-INITIAL_FORMS': '0',
            'questions-0-answers-MIN_NUM_FORMS': '0',
            'questions-0-answers-MAX_NUM_FORMS': '1000',
            'questions-0-answers-0-text': 'Answer 1',
            'questions-0-answers-0-is_correct': 'on',
            'questions-0-answers-1-text': 'Answer 2',
            'questions-0-answers-2-text': 'Answer 3',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful creation
        self.assertTrue(Quiz.objects.filter(title='New Quiz').exists())

    def test_quiz_taking_form(self):
        self.client.login(username='testuser', password='testpass123')
        correct_answer = self.question.answers.get(is_correct=True)
        response = self.client.post(reverse('quiz_results', args=[self.quiz.id]), {
            f'question_{self.question.id}': correct_answer.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your Score: 1/1')
```

### 2.4 Test Models
```python
    def test_quiz_model(self):
        self.assertEqual(str(self.quiz), 'Test Quiz')
        self.assertEqual(self.quiz.questions.count(), 1)

    def test_question_model(self):
        self.assertEqual(str(self.question), 'What is the capital of France?')
        self.assertEqual(self.question.answers.count(), 3)

    def test_answer_model(self):
        correct_answer = self.question.answers.get(is_correct=True)
        self.assertEqual(str(correct_answer), 'Paris')
```

## 3. Running Tests
To run these tests, use the following command:
```
python manage.py test quizzes
```

## 4. Additional Test Cases to Consider
- Test user authentication and authorization
- Test quiz result calculation for various scenarios
- Test pagination of quiz lists
- Test form validation for all input fields
- Test CSRF protection on forms
- Test handling of concurrent quiz attempts

## 5. Performance Testing
- Test loading times for pages with many quizzes or questions
- Test database query performance for complex quiz result calculations

## 6. Browser Compatibility Testing
- Test the application on different browsers (Chrome, Firefox, Safari, Edge)
- Test responsive design on various screen sizes

## 7. Accessibility Testing
- Use tools like aXe or WAVE to check for accessibility issues
- Test keyboard navigation throughout the application

