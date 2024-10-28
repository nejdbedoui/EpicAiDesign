from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import BlogForm, UpdateBlogForm
from .models import Blog
from SpeechApp.models import Speech
from UserApp.decorator import custom_login_required

@custom_login_required
def add_blog(request, speech_id):
    speech = Speech.objects.get(id=speech_id)
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            blog = Blog(
                text=data['text'],
                speech=speech_id,
                user=user_id
            )
            blog.save()

            speech.blogs.append(blog)
            speech.save()

            return redirect('get_speech', speech_id=speech_id)
        else:
            messages.error(request, "Form data is not valid.")
            form.add_error(None, 'Form data is not valid.')
    else:
        form = BlogForm()
    return render(request, 'speech_detail.html', {'form': form})

@custom_login_required
def delete_blog(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    speech = blog.speech
    if blog in speech.blogs:
        speech.blogs.remove(blog)
        speech.save()
    blog.delete()
    messages.success(request, "Blog Deleted")
    return redirect('get_speech', speech_id=speech.id)