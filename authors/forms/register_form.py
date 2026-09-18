from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password
    
class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['email'], 'any e-mail address')
        add_placeholder(self.fields['first_name'], 'Ex.: Hondão')
        add_placeholder(self.fields['last_name'], 'Ex.: Civicão')
        add_placeholder(self.fields['username'], 'Type your imagination here')
        #add_attr(self.fields['username', 'css', 'a-css-class'])
    
    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        label='First name'
    )
    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        label='Last name'
    )
    email = forms.EmailField(
        error_messages={'required': 'E-mail is required'},
        label='E-mail',
        help_text='The e-mail must be valid.',
    )
    username = forms.CharField(
        required=True,
        label='Username',
        help_text=('Make sure your imagination is good enough for at least 4 '
                   'characters and do not imagine that super so ' 
                   "you won't trespass 150 of them."),
        error_messages={
            'required': 'You need to type the best of your imagination here!',
            'min_length': 'make sure it has at least 4 chars!',
            'max_length': 'make sure you are not kidding'
        },
        min_length=4,max_length=150
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Type a good one here!'
        }),
        error_messages={
            'required': 'Password must not be empty'
        },
        
        help_text=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
        ),
        validators=[strong_password]
    )
    
    
    password2 = forms.CharField(
            required=True,
            widget= forms.PasswordInput(attrs={
                'placeholder': 'Repeat your good one here!'
            })
        )
    
    
    class Meta:
        
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Type your imagination here',
                'class': 'input text-input'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Type a good one here!'
            })
        }
        
    
    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()
        
        if exists:
            raise ValidationError('e-mail alredy registered, try another one', code='invalid')
        return email
    
    
    def clean(self):
        cleaned_data = super().clean()
        
        self.password = cleaned_data.get('password')
        self.password2 = cleaned_data.get('password2')
        
        if self.password != self.password2:
            raise ValidationError({
               'password': "You didn't typed your good one twice!"
               
            })
