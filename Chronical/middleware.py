from django.http import HttpResponse
from django.middleware.csrf import get_token

class StaticAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip auth for admin, static files
        if (request.path.startswith('/admin/') or 
            request.path.startswith('/static/') or 
            request.path.startswith('/media/')):
            return self.get_response(request)
        
        # Check session
        if not request.session.get('authenticated'):
            return self.auth_form(request)
        
        return self.get_response(request)
    
    def auth_form(self, request):
        if request.method == 'POST':
            if (request.POST.get('username') == 'ckauser' and 
                request.POST.get('password') == 'cka@123'):
                request.session['authenticated'] = True
                return HttpResponse('<script>window.location.reload()</script>')
        
        # Get CSRF token
        csrf_token = get_token(request)
        
        return HttpResponse(f'''
        <div style="display:flex;justify-content:center;align-items:center;height:100vh;background:#f5f5f5;font-family:Arial">
            <div style="background:white;padding:30px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1)">
                <h2 style="color:#863F3F;text-align:center">Launching Soon</h2>
                <form method="post">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                    <input type="text" name="username" placeholder="Username" required style="width:250px;padding:10px;margin:5px 0;border:1px solid #ddd;border-radius:4px"><br>
                    <input type="password" name="password" placeholder="Password" required style="width:250px;padding:10px;margin:5px 0;border:1px solid #ddd;border-radius:4px"><br>
                    <button type="submit" style="width:270px;padding:10px;background:#863F3F;color:white;border:none;border-radius:4px;cursor:pointer;margin-top:10px">Access</button>
                </form>
            </div>
        </div>
        ''')