from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password

from .models import User, ProfilePicture

class LoginForm(forms.Form):
    """ The user login form
    """
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)
    user = None

    def clean(self):
        """ Gets the data from the login form 
            and authenticates the user.
        """
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        auth = authenticate(email=email, password=password)
        if not auth:
            raise forms.ValidationError("Wrong Email or Password!")
        else:
            self.user = auth

        return cleaned_data


class RegistrationForm(forms.ModelForm):
    """ Contains the fields of the registration form
    """
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('email','password')


    def clean_confirm_password(self):
        """ Checks if the password are matched
        """
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password did not match!"
            )
        return confirm_password

    def clean_email(self):
        """ Checks if the email is already taken
        """
        getclean_email = self.cleaned_data['email']
        emails = User.objects.filter(email=getclean_email)
        if len(emails) != 0:
            raise forms.ValidationError("Sorry but the Email is already TAKEN")
        return getclean_email

    def save(self, commit=True):
        """ Saves the user data
        """
        instance = super(RegistrationForm, self).save(commit=False)
        instance.set_password(self.cleaned_data['password'])
        instance.save()
        return instance


class UpdateProfileForm(forms.ModelForm):
    """ Form for updating the user's profile
    """
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        filter_email = User.objects.filter(email=email).exclude(email=self.instance.email)
        if len(filter_email) != 0:
            raise forms.ValidationError("Someone's already using this email")
        return email



class UpdatePasswordForm(forms.Form):
    """ Form for updating the user's password
    """
    old_password = forms.CharField(required=True, widget=forms.PasswordInput)
    new_password = forms.CharField(required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(required=True, widget=forms.PasswordInput)
    user = None

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        return super(UpdatePasswordForm, self).__init__(*args,**kwargs)

    def clean_old_password(self):
        password = self.cleaned_data.get('old_password')
        # validate the passwords
        if not check_password(password, self.user.password):
            raise forms.ValidationError("Invalid Old Password")
        return password

    def clean_confirm_password(self):
        # check the new password and confirm password
        new_pass = self.cleaned_data.get('new_password')
        confirm_pass = self.cleaned_data.get('confirm_password')

        if new_pass != confirm_pass:
            raise forms.ValidationError("Passwords do not match!")
        return new_pass

    def save(self, *args, **kwargs):
        """save function
        """
        # data from the form
        password = self.cleaned_data.get('new_password')

        # set and save the new password
        user = User.objects.get(id=kwargs['user'].id)
        user.set_password(password)
        user.save()
        return user


class ProfilePicForm(forms.ModelForm):
    """ Form for uploading profile picture
    """

    class Meta:
        model = ProfilePicture
        fields = ('imagefile',)