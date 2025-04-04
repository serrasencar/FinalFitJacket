from django.shortcuts import render

def friends_view(request):
    return render(request, 'friends/social.html')

# Create your views here.
