from django.shortcuts import redirect

class RedirectUnauthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Allow authenticated users and unauthenticated users accessing the home or login
        if request.user.is_authenticated or request.path == '/' or request.path.startswith('/accounts/'):
            return self.get_response(request)

        # If unauthenticated user tries to access a protected route (like /dashboard/)
        if request.path.startswith('/dashboard/'):
            return redirect('/')

        return self.get_response(request)