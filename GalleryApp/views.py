from datetime import datetime
from django.contrib import messages
from django.shortcuts import render, redirect
import UserApp.models
from GalleryApp.models import ImageGallery
from ImageApp.models import ImageArt
from UserApp.views import gallery
# from django.shortcuts import get_object_or_404
from django.http import Http404


def add_gallery(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        cover = request.FILES.get('cover')
        if not title or not cover:
            messages.error(request, "Title and Cover Image are required.")
            return redirect('add_gallery')

        user = UserApp.models.User.objects.get(email=request.session['user_email'])
        gallery = ImageGallery(
            title=title,
            cover=cover,
            rating=0,
            created_at=datetime.now(),
            user=user
        )
        gallery.save()
        messages.success(request, 'Gallery added successfully!')
        return redirect('my_galleries')

    return render(request, 'add_gallery.html')


def add_to_gallery(request, id):
    data = ImageArt.objects.all()

    if request.method == 'POST':
        gallery_id = id
        selected_images_ids = request.POST.getlist('selected_images')  # Récupérer la liste des IDs des images sélectionnées
        gallery = ImageGallery.objects(id=gallery_id).first()

        if gallery:
            for image_id in selected_images_ids:
                image = ImageArt.objects(id=image_id).first()
                if image and image not in gallery.images:
                    gallery.images.append(image)
            gallery.save()
            messages.success(request, 'Selected images added to gallery successfully!')
        else:
            messages.error(request, 'Gallery not found.')

        return redirect('my_galleries')
    return render(request , 'add_to_gallery.html' , {'data':data})

def my_galleries(request):
    user = UserApp.models.User.objects.get(email=request.session['user_email'])
    galleries = ImageGallery.objects(user=user).all().order_by('created_at')
    # lahna supression
    if request.method == 'POST':
        gallery_id  = request.POST.get('id_gallery')
        gallery_to_delete = ImageGallery.objects.get(id=gallery_id)
        gallery_to_delete.delete()
    return render(request, 'my_galleries.html', {'galleries': galleries})


def add_img_to_gallery (request) :
    if request.method == 'POST':
        gallery_id = request.POST.get('selected_gallery')
        selected_images_ids = request.POST.getlist('selected_images')  # Récupérer la liste des IDs des images sélectionnées
        gallery = ImageGallery.objects(id=gallery_id).first()

        if gallery:
            for image_id in selected_images_ids:
                image = ImageArt.objects(id=image_id).first()
                if image and image not in gallery.images:
                    gallery.images.append(image)
            gallery.save()
            messages.success(request, 'Selected images added to gallery successfully!')
        else:
            messages.error(request, 'Gallery not found.')

    return redirect('my_galleries')


# def update_gallery(request, id):
#     gallery = get_object_or_404(ImageGallery, id=id)
#
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         cover = request.FILES.get('cover')
#
#         if title:
#             gallery.title = title
#         if cover:
#             gallery.cover = cover
#
#         gallery.save()
#         messages.success(request, 'Gallery updated successfully!')
#         return redirect('my_galleries')
#
#     return render(request, 'update_gallery.html', {'gallery': gallery})


def update_gallery(request, id):
    try:
        gallery = ImageGallery.objects.get(id=id)
    except ImageGallery.DoesNotExist:
        raise Http404("Gallery not found")

    # Continuer le traitement de mise à jour ici
    if request.method == 'POST':
        title = request.POST.get('title')
        cover = request.FILES.get('cover')

        if title:
            gallery.title = title
        if cover:
            gallery.cover = cover

        gallery.save()
        messages.success(request, "Gallery updated successfully!")
        return redirect('my_galleries')

    return render(request, 'update_gallery.html', {'gallery': gallery})


def gallery_details(request, id):
    try:
        gallery = ImageGallery.objects.get(id=id)
        images = gallery.images.all()  # Récupérez toutes les images associées à la galerie
    except ImageGallery.DoesNotExist:
        raise Http404("Gallery not found")

    return render(request, 'gallery_details.html', {
        'gallery': gallery,
        'images': images,
    })
