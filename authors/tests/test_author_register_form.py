from unittest import TestCase
from django.test import TestCase as DTC
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Type your imagination here'),
        ('email', 'e-mail or temp-mail, whatever'),
        ('first_name', 'Ex.: Hondão'),
        ('last_name', 'Ex.: Civicão'),
        ('password', 'Type a good one here!'),
        ('password2', 'Repeat your good one here!')
        
    ])
    
    
    def test_first_name_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    
    @parameterized.expand([
        ('username',('Make sure your imagination is good enough for at least 4 '
                   'characters and do not imagine that super so ' 
                   "you won't trespass 150 of them.")),
    ])
    def test_fields_help_text(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)
    
    

class AuthorRegisterFormIntegrationTest(DTC):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'user',
            'first_name': 'first',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'SuperStrongImp0ssibletoR3@(h',
            'password2': 'SuperStrongImp0ssibletoR3@(h'
        }
        return super().setUp(*args, **kwargs)


    @parameterized.expand([
        ('username', 'You need to type the best of your imagination here!'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('email', 'E-mail is required'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get(field))


    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'mar'
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'make sure it has at least 4 chars!'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
       
        
    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = '67' * 80
        url = reverse('authors:register_create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        msg = 'make sure you are not kidding'
        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get('username'))
       

    def test_email_field_must_be_unique(self):
        url = reverse('authors:register_create')
        
        self.client.post(url, data=self.form_data, follow=True)
        response = self.client.post(url, data=self.form_data, follow=True)


        msg = 'e-mail alredy registered, try another one'
        self.assertIn(msg, response.context['form'].errors.get('email'))
        self.assertIn(msg, response.content.decode('utf-8'))


    def test_author_created_can_login(self):
            url = reverse('authors:register_create')

            self.form_data.update({
                'username': 'testuser',
                'password': '@SuperStrongImp0ssibletoR3h',
                'password2': '@SuperStrongImp0ssibletoR3h',
            })

            self.client.post(url, data=self.form_data, follow=True)

            is_authenticated = self.client.login(
                username='testuser',
                password='@SuperStrongImp0ssibletoR3h'
            )

            self.assertTrue(is_authenticated)
