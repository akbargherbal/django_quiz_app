from django import forms
from django.forms import inlineformset_factory
from .models import Quiz, Question, Answer

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full p-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-slate-100 dark:bg-slate-800 focus:ring-2 focus:ring-sky-500 dark:focus:ring-sky-400'}),
            'description': forms.Textarea(attrs={'class': 'w-full p-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-slate-100 dark:bg-slate-800 focus:ring-2 focus:ring-sky-500 dark:focus:ring-sky-400', 'rows': 3}),
            'category': forms.Select(attrs={'class': 'w-full p-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-slate-100 dark:bg-slate-800 focus:ring-2 focus:ring-sky-500 dark:focus:ring-sky-400'}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'w-full p-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-slate-100 dark:bg-slate-800 focus:ring-2 focus:ring-sky-500 dark:focus:ring-sky-400'}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text', 'is_correct']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'w-full p-2 border border-slate-300 dark:border-slate-600 rounded-lg bg-slate-100 dark:bg-slate-800 focus:ring-2 focus:ring-sky-500 dark:focus:ring-sky-400'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-sky-500'}),
        }

QuestionFormSet = inlineformset_factory(Quiz, Question, form=QuestionForm, extra=1, can_delete=True)
AnswerFormSet = inlineformset_factory(Question, Answer, form=AnswerForm, extra=4, can_delete=True, max_num=4)