from django.forms import ModelForm, ImageField
from .models import (Room, Lesson, User, Topic, Message, Course, LessonCorrection, Resign, Availability, Report,
                     BankInformation, NewStudents)
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta, datetime

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~USER-CREATION~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

def validate_username_length(value):
    if len(value) > 10:
        raise ValidationError(_("Nazwa użytkownika nie może przekraczać 10 znaków."))

class MyUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label=_("Nazwa użytkownika (maks. 10 znaków)"),
        validators=[validate_username_length],
        help_text=_("Maksymalnie 10 znaków."),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~KNOWLEDGE-ZONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

    level = forms.ChoiceField(choices=Room.LEVEL_CHOICES, widget=forms.Select, required=True)


class RoomMessageForm(forms.ModelForm):
    image_clear = forms.BooleanField(required=False, initial=False)

    class Meta:
        model = Message
        fields = ['body', 'image', 'file']

    body = forms.CharField(widget=forms.Textarea, required=False)


class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['reason', 'description']
        widgets = {
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class UserForm(forms.ModelForm):
    username = forms.CharField(
        validators=[MaxLengthValidator(limit_value=10, message="Nazwa użytkownika nie może przekraczać 10 znaków.")]
    )
    class Meta:
        model = User
        labels = {
            'avatar': 'Zdjęcie profilowe',
            'username': 'Nazwa użytkownika (maks. 10 znaków)',
            'email': 'Email',
            'bio': 'Bio',
            'interests': 'Zainteresowania'
        }
        fields = ['avatar', 'username', 'email', 'bio', 'interests']

    bio = forms.CharField(widget=forms.Textarea, required=False)

'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TUTORING-ZONE~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~'''

class WriterDataForm(forms.ModelForm):
    user_type = forms.ChoiceField(
        choices=[('teacher', 'Korepetytor'), ('student', 'Uczeń')],
        label="Wybierz rolę"
    )
    referral_code_input = forms.CharField(
        max_length=10,
        required=False,
        label="Kod polecenia",
    )

    class Meta:
        model = User
        fields = ['phone_number', 'level', 'subject']
        labels = {
            'phone_number': 'Numer telefonu',
            'subject': 'Przedmiot',
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if not phone_number or phone_number == 'N/A':
            raise forms.ValidationError("Numer telefonu jest wymagany.")
        return phone_number

    def clean_user_type(self):
        user_type = self.cleaned_data.get('user_type')
        if user_type not in ['teacher', 'student']:
            raise forms.ValidationError("Wybierz prawidłową rolę.")
        return user_type


class ApplyUserForm(UserCreationForm):
    ROLE_CHOICES = [
        ('student', 'Uczeń'),
        ('teacher', 'Korepetytor'),
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="Wybierz rolę")
    phone_number = forms.CharField(max_length=20, required=True, label="Numer telefonu")
    subject = forms.ModelChoiceField(queryset=Topic.objects.all(), label="Wybierz przedmiot", required=False)
    level = forms.ChoiceField(choices=User.LEVEL_CHOICES, required=True, label="Poziom zajęć", initial="podstawa")
    terms_and_privacy = forms.BooleanField(required=True)
    age_confirmation = forms.BooleanField(required=True, label="Potwierdzam ukończenie 18 lat lub zgoda na założenie konta jest wyrażona w moim imieniu przez rodzica/opiekuna prawnego.")
    referral_code_input = forms.CharField(
        max_length=10,
        required=False,
        label="Kod polecenia",
    )

    username = forms.CharField(
        max_length=10,
        label="Nazwa użytkownika (maks. 10 znaków)",
        validators=[MaxLengthValidator(10, message="Nazwa użytkownika nie może mieć więcej niż 10 znaków.")],
    )

    class Meta:
        model = User
        fields = ['role', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'subject', 'level',
                  'referral_code_input', 'password1', 'password2']



class BankInformationForm(forms.ModelForm):
    expiration_month = forms.ChoiceField(label='Miesiąc', choices=[(i, f'{i:02}') for i in range(1, 13)])
    expiration_year = forms.ChoiceField(label='Rok', choices=[(year, year) for year in range(datetime.now().year, datetime.now().year + 6)])

    class Meta:
        model = BankInformation
        fields = ['card_number', 'cvv', 'cardholder_name', 'expiration_month', 'expiration_year']
        labels = {
            'card_number': 'Numer karty',
            'cvv': 'CVV',
            'cardholder_name': 'Imię i nazwisko',
        }
        widgets = {
            'card_number': forms.TextInput(attrs={'maxlength': '16', 'placeholder': '16-cyfrowy numer karty'}),
            'cvv': forms.TextInput(attrs={'maxlength': '3', 'placeholder': 'CVV'}),
            'cardholder_name': forms.TextInput(attrs={'placeholder': 'Imię i nazwisko właściciela'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        month = cleaned_data.get('expiration_month')
        year = cleaned_data.get('expiration_year')

        if month and year:
            cleaned_data['expiration_date'] = f'{year}-{month}-01'
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        expiration_month = self.cleaned_data.get('expiration_month')
        expiration_year = self.cleaned_data.get('expiration_year')
        instance.expiration_date = f'{expiration_year}-{expiration_month}-01'
        if commit:
            instance.save()
        return instance


class ResignationForm(forms.ModelForm):
    course_info = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Nazwa kursu, imie i nazwisko ucznia/ów, numeru telefonu/ów, przedmiot, częstotliwość zajęć, dodatkowe informacje itd.'}))
    rating = forms.ChoiceField(choices=Resign.RATING_CHOICES, label='Ocena platformy SchoolWeb', required=True)
    consider_return = forms.ChoiceField(choices=Resign.RETURN_OPTIONS, label='Czy rozważasz powrót na SchoolWeb', required=True)
    reason_details = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Podaj dodatkowe informacje dotyczące powodu rezygnacji/przerwy'}),required=False)

    class Meta:
        model = Resign
        fields = ['email', 'reason', 'start_date', 'end_date', 'course_info', 'rating', 'consider_return', 'reason_details']


class LessonFormCreate(forms.ModelForm):
    event_datetime = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Data',
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LessonFormCreate, self).__init__(*args, **kwargs)

        if user:
            self.fields['course'].queryset = Course.objects.filter(teacher=user)
            self.fields['course'].label_from_instance = lambda obj: f"{obj.name}"

    def clean_event_datetime(self):
        event_datetime = self.cleaned_data['event_datetime']
        minimum_datetime = timezone.now() + timedelta(minutes=15)

        if event_datetime <= minimum_datetime:
            raise ValidationError("Wybierz datę i godzinę co najmniej 15 minut od teraźniejszego czasu.")

        return event_datetime

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'course', 'event_datetime']


class LessonFormEdit(forms.ModelForm):
    event_datetime = forms.DateTimeField(
        widget=forms.TextInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        label='Data',
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Lesson
        fields = ['title', 'description', 'event_datetime']

    def clean_event_datetime(self):
        event_datetime = self.cleaned_data['event_datetime']
        minimum_datetime = timezone.now() + timedelta(minutes=15)

        if event_datetime <= minimum_datetime:
            raise ValidationError("Wybierz datę i godzinę co najmniej 15 minut od teraźniejszego czasu.")

        return event_datetime


class NewStudentForm(forms.ModelForm):
    class Meta:
        model = NewStudents
        fields = ['subject', 'level']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-control'}),
        }


class LessonFeedbackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        post_instance = kwargs.pop('post_instance')
        super(LessonFeedbackForm, self).__init__(*args, **kwargs)

        self.fields['attended_teachers'].queryset = User.objects.filter(
            courses_taught=post_instance.course
        )

        self.fields['attended_students'].queryset = post_instance.course.students.all()

    class Meta:
        model = Lesson
        fields = ['feedback', 'points', 'schoolweb_rating', 'attended_students', 'attended_teachers']

    attended_teachers = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Nauczyciele, którzy dołączyli'
    )

    attended_students = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Uczniowie, którzy dołączyli'
    )

    feedback = forms.CharField(
        label='Dodatkowe informacje na temat lekcji:',
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        required=False,
        initial="-",
    )


class LessonCorrectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        course = kwargs.pop('course', None)
        super(LessonCorrectionForm, self).__init__(*args, **kwargs)

        if course:
            self.fields['attended_teachers'].queryset = User.objects.filter(
                courses_taught=course
            )

            self.fields['attended_students'].queryset = course.students.all()

    class Meta:
        model = LessonCorrection
        fields = ['attended_teachers', 'attended_students', 'feedback', 'lesson_image']

    attended_teachers = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Nauczyciele, którzy dołączyli'
    )

    attended_students = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Uczniowie, którzy dołączyli'
    )

    feedback = forms.CharField(
        label='Dodatkowe informacje:',
        widget=forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        required=False
    )

    lesson_image = forms.ImageField(
        label='Zdjęcie lekcji',
        required=False
    )


class AvailabilityForm(forms.ModelForm):
    class Meta:
        model = Availability
        fields = ['day', 'hour_6_7', 'hour_7_8', 'hour_8_9', 'hour_9_10', 'hour_10_11', 'hour_11_12',
                  'hour_12_13', 'hour_13_14', 'hour_14_15', 'hour_15_16', 'hour_16_17', 'hour_17_18',
                  'hour_18_19', 'hour_19_20', 'hour_20_21', 'hour_21_22']

    def __init__(self, *args, **kwargs):
        super(AvailabilityForm, self).__init__(*args, **kwargs)
        tomorrow = timezone.now() + timezone.timedelta(days=1)
        seven_days_later = tomorrow + timezone.timedelta(days=7)
        self.fields['day'].widget = forms.DateInput(attrs={'type': 'date', 'min': tomorrow.date(), 'max': seven_days_later.date()})
