from django.shortcuts import render


# Create your views here.

def category(request):
    return render(request, 'main_page/index.html', {'title': 'EnePy'})
