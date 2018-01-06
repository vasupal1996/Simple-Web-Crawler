from django import forms

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


def ForbiddenUsernameValidator(value):
    forbidden_usernames = ['admin', 'settings', 'news', 'about', 'help', 'signin', 'signup', 
        'signout', 'terms', 'privacy', 'cookie', 'new', 'login', 'logout', 'administrator', 
        'join', 'account', 'username', 'root', 'blog', 'user', 'users', 'billing', 'subscribe',
        'reviews', 'review', 'blog', 'blogs', 'edit', 'mail', 'email', 'home', 'job', 'jobs', 
        'contribute', 'newsletter', 'shop', 'profile', 'register', 'auth', 'authentication',
        'campaign', 'config', 'delete', 'remove', 'forum', 'forums', 'download', 'downloads', 
        'contact', 'blogs', 'feed', 'faq', 'intranet', 'log', 'registration', 'search', 
        'explore', 'rss', 'support', 'status', 'static', 'media', 'setting', 'css', 'js',
        'follow', 'activity', 'library']

    if value.lower() in forbidden_usernames:
        raise ValidationError(_('Sorry, This Username Cannot Be Taken. Please Choose Another.'))

# def InvalidUsernameValidiator(value):
#     invalid_characters = '!#$%^&*()-=+/?><,\"\';:]}[{\|`~_'
#     if value in list(invalid_characters):
#         raise ValidationError(_('Enter A Valid Username Without Special Characters other than "@,_"'))

def UniqueUsernameValidiator(value):
    if User.objects.filter(username__iexact=value).exists():
        raise ValidationError(_('This Username Already Exists'))

def UniqueEmailValidiator(value):
    if User.objects.filter(email__iexact=value).exists():
        raise ValidationError(_('This Email Already Exists'))

class SignupForm(forms.ModelForm):  
    username = forms.CharField(widget=forms.TextInput(), validators=[UniqueUsernameValidiator, ForbiddenUsernameValidator])
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(validators=[UniqueEmailValidiator])

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password']


    def clean_confirm_password(self):
        passoword = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if passoword and passoword != confirm_password:
            self.add_error('password', 'Passwords Don\'t Match')
            self.add_error('confirm_password', 'Passwords Don\'t Match')

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label='Username/Email')
    password = forms.CharField(widget=forms.PasswordInput(), label='Password')