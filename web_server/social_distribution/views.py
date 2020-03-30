from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse


def home(request):
    if request.method == 'GET':
        # return redirect(reverse('stream'))
        if request.user.is_authenticated:
            return redirect(reverse('home'))
        else:
            return redirect(reverse('login'))
    else:
        return HttpResponse('404 Error', status=404)


def github(request):
    if request.method == 'GET':
        context = {}
        context['github'] = request.user.github.split('github.com/')[1]
        return JsonResponse(context)

def landing_page(request):
    context = {
        'post_viewing_url': reverse('post', args=['00000000000000000000000000000000']).replace('00000000000000000000000000000000/', '')
    }
    return render(request, 'home.html', context)