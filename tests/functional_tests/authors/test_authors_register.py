from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


class AuthorsRegisterTest(AuthorsBaseTest):
    def fill_form_dummy_data(self, form):

        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)


    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )


    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        callback(form)
        return form


    def test_empty_first_name_error_message(self):
        def callback(form):
            first_name_field = self.get_by_placeholder(form, 'Ex.: Hondão')
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your first name', form.text)
        self.form_field_test_with_callback(callback)


    def test_empty_last_name_error_message(self):
        def callback(form):
            last_name_field = self.get_by_placeholder(form, 'Ex.: Civicão')
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('Write your last name', form.text)
        self.form_field_test_with_callback(callback)


    def test_empty_username_error_message(self):
        def callback(form):
            username_field = self.get_by_placeholder(form, 'Type your imagination here')
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)
            form = self.get_form()
        self.form_field_test_with_callback(callback)


    def test_invalid_email_error_message(self):
        def callback(form):
            email_field = self.get_by_placeholder(form, 'e-mail or temp-mail, whatever')
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)
            form = self.get_form()
            self.assertIn('The e-mail must be valid.', form.text)
        self.form_field_test_with_callback(callback)


    def test_passwords_do_not_match(self):
        def callback(form):
            password1 = self.get_by_placeholder(form, 'Type a good one here!')
            password2 = self.get_by_placeholder(form, 'Repeat your good one here!')
            password1.send_keys('P@ssw0rd')
            password2.send_keys('P@ssw0rd_Different')
            password2.send_keys(Keys.ENTER)
            form = self.get_form()
        self.form_field_test_with_callback(callback)

