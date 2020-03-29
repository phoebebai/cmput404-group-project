from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth import views as auth_views
from django.urls import reverse
from users.models import Author
from django.conf import settings

class CustomLogin(auth_views.LoginView):
    def form_valid(self, form):
        login(self.request, form.get_user())
        # set expiration of the current login session
        # a single login is alive for 10hrs
        self.request.session.set_expiry(36000)
        return HttpResponseRedirect(self.get_success_url())


@login_required
def profile(request, user_id):
    """
    Local handler for viewing author profiles, the author in question might be local or foreign,
    both should be supported
    """
    if Author.is_uid_local(user_id):
        # @todo , this template expects a uuid in order to render, it should be able to handle a uid
        return render(request, 'users/profile.html', {
            'user_id': Author.extract_uuid_from_uid(user_id),  # uuid
            'user_full_id': user_id,  # uid

            'post_view_url': reverse('view_post', args=['00000000000000000000000000000000']).replace('00000000000000000000000000000000/', '')
        })
    # @todo, see above, we dont yet have a profile viewing template that handles uids
    return HttpResponse('The profile you are attempting to view is for a foreign author, which is unsupported at this time', status=404)

def view_post(request, post_path):
    """
    Local handler for viewing a post, the post might be local or foreign, and the path should determine that.
    """
    path = post_path.split('/')
    host = path[0]

    if host == settings.HOSTNAME:
        # Local post, handle as normal by redirecting them to the current post viewer
        return redirect(reverse('post', args=[path[-1]]))

    # Foreign post
    # @todo foreign post viewing
    return HttpResponse('Foreign posts cannot be viewed from our local server at this time', status=404)

@login_required
def add_friend(request):
    return render(request, 'users/add_friend.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # wait for admin permission to activate account
            user.is_active = False
            host = request.get_host()
            url = host + "/author/" + str(user.id.hex)
            # set user url
            user.url = url
            # set user id
            # format: 127.0.0.1:5454/author/de305d54-75b4-431b-adb2-eb6b9e546013
            user.uid = url
            # set user host
            user.host = host

            # update database entry of current user
            user.save()
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def mandala(request):
    return render(request, 'users/mandala.html')
