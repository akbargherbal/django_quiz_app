import os
import json
import pandas as pd
from django.core.management.base import BaseCommand
from quizzes.models import Quiz, Question, Answer
from django.contrib.auth.models import User
from django.db import transaction
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Import quizzes from CSV files in a specified directory'

    def add_arguments(self, parser):
        parser.add_argument('directory', type=str, help='Path to the directory containing CSV files')

    def handle(self, *args, **options):
        directory = options['directory']
        quiz_info_file = os.path.join(directory, 'quiz_info.json')

        try:
            with open(quiz_info_file, 'r') as f:
                quiz_info = json.load(f)
        except FileNotFoundError:
            logger.error(f"Quiz info file not found: {quiz_info_file}")
            return
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in quiz info file: {quiz_info_file}")
            return

        # Get or create a default user (you may want to adjust this)
        user, created = User.objects.get_or_create(username='admin')

        for quiz_data in quiz_info:
            file_name = quiz_data['file_name']
            topic_title = quiz_data['topic_title']
            category_description = quiz_data['category_description']

            csv_file = os.path.join(directory, file_name)

            try:
                self.import_quiz(csv_file, topic_title, category_description, user)
            except Exception as e:
                logger.error(f"Error importing quiz from {file_name}: {str(e)}")

    def import_quiz(self, csv_file, quiz_title, quiz_description, user):
        logger.info(f"Importing quiz: {quiz_title}")

        try:
            df = pd.read_csv(csv_file)
        except FileNotFoundError:
            logger.error(f"CSV file not found: {csv_file}")
            return
        except pd.errors.EmptyDataError:
            logger.error(f"CSV file is empty: {csv_file}")
            return
        except pd.errors.ParserError:
            logger.error(f"Error parsing CSV file: {csv_file}")
            return

        required_columns = ['question', 'option1', 'option2', 'option3', 'option4', 'correct_answer']
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            logger.error(f'CSV file is missing required columns: {", ".join(missing_columns)}')
            return

        try:
            with transaction.atomic():
                quiz = Quiz.objects.create(
                    title=quiz_title,
                    description=quiz_description,
                    category="Django Fundamentals",
                    creator=user
                )

                for _, row in df.iterrows():
                    question = Question.objects.create(
                        quiz=quiz,
                        text=row['question']
                    )

                    for i in range(1, 5):
                        option = row[f'option{i}']
                        if pd.notna(option):
                            Answer.objects.create(
                                question=question,
                                text=str(option),
                                is_correct=(i == row['correct_answer'])
                            )

                    if 'option5' in df.columns and pd.notna(row['option5']):
                        Answer.objects.create(
                            question=question,
                            text=str(row['option5']),
                            is_correct=(5 == row['correct_answer'])
                        )

            logger.info(f'Successfully imported quiz "{quiz_title}" with {quiz.questions.count()} questions')
        except Exception as e:
            logger.error(f"Error creating quiz {quiz_title}: {str(e)}")
            raise