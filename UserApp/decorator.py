from django.shortcuts import redirect
from django.http import HttpResponseForbidden


def custom_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'user_id' in request.session:  # or any condition you define for checking user authentication
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login')  # Redirect to your login view

    return _wrapped_view
