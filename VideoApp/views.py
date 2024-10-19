from django.shortcuts import render

# Create your views here.
def Add_Video(request):
    video="https://www.youtube.com/watch?v=668nUCeBHyY"
    return render(request, 'addVideo.html', {'video': video})