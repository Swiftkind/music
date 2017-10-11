from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LoginForm, RegistrationForm, ProfilePicForm

from .forms import LoginForm, UpdateProfileForm, UpdatePasswordForm
from .models import User, ProfilePicture
from playlist.models import Playlist, Song

class UserLoginView(TemplateView):
    """ User login account
    """
    template_name = 'auth/login.html'

    def get(self, *args, **kwargs):
        """ Renders the login form
        """
        if self.request.user.is_authenticated():
            return redirect('all_playlist')
        form = LoginForm()
        return render(self.request, self.template_name, {'form':form})

    def post(self, *args, **kwargs):
        """ submits the data
        """
        form = LoginForm(self.request.POST)
        if form.is_valid():
            login(self.request, form.user)
            return redirect('all_playlist')

        return render(self.request, self.template_name, {'form':form})


class UserLogoutView(View):
    """ Logout the user account
    """
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('user_login')


class RegisterView(TemplateView):
    """ Registers the new user
    """
    template_name = 'registration.html'

    def get(self, *args, **kwargs):
        """ Renders the registration form
        """
        form = RegistrationForm()
        return render(self.request, self.template_name, {'form':form})

    def post(self, *args, **kwargs):
        """ Gets the data
        """
        form = RegistrationForm(self.request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(self.request, email=self.request.POST['email'], 
                                              password=self.request.POST['password'])
            login(self.request, user)
            return redirect('all_playlist')
            
        return render(self.request, self.template_name, {'form':form})


class UserProfileView(LoginRequiredMixin, View):
    """ display a user's profile
    """
    template_name = 'user/profile.html'

    def get(self, *args, **kwargs):
        """ render a user's profile
        """
        picture_form = ProfilePicForm()
        playlists = Playlist.objects.filter(user=self.request.user)
        return render(self.request, self.template_name, {'playlists':playlists,
                                                        'picture_form':picture_form
                                                        })

    def post(self, *args, **kwargs):
        """ update the user's picture
        """
        picture_form = ProfilePicForm(self.request.POST, self.request.FILES)
        playlists = Playlist.objects.filter(user=self.request.user)
        if picture_form.is_valid():
            photo = picture_form.save(commit=False)
            photo.user = self.request.user
            photo.save()
            return redirect('user_profile')
        return render(self.request, self.template_name, {'playlists':playlists,
                                                        'picture_form':picture_form
                                                        })


class UpdateProfileView(LoginRequiredMixin, TemplateView):
    """ Update the user's first and last names
    """
    template_name = 'user/edit.html'

    def get(self, *args, **kwargs):
        """ display
        """
        
        form = UpdateProfileForm(instance=self.request.user)
        return render(self.request, self.template_name, {'form':form})

    def post(self, *args, **kwargs):
        """update the user's profile (first name, last name, email)
        """
        form = UpdateProfileForm(self.request.POST, instance=self.request.user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
        return render(self.request, self.template_name, {'form':form})


class UpdatePasswordView(LoginRequiredMixin, TemplateView):
    """ Updates the user's password
    """
    template_name = 'user/editpassword.html'

    def get(self, *args, **kwargs):
        """display the form
        """
        form = UpdatePasswordForm(user=self.request.user)
        return render(self.request, self.template_name, {'form':form})

    def post(self, *args, **kwargs):
        """save the changes
        """
        form = UpdatePasswordForm(self.request.POST, user=self.request.user)
        if form.is_valid():
            # save the form and relogin the user, using the new credentials
            form.save(user=self.request.user)
            user = authenticate(self.request, email=form.user.email,
                                password=form.cleaned_data['new_password'])
            login(self.request, user)
            return redirect('user_profile')
        return render(self.request, self.template_name, {'form':form})
