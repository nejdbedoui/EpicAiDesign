from django.shortcuts import render


# Create your views here.
def Add_poem(request):
    return render(request, 'addPoem.html')
