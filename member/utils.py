from captcha.image import ImageCaptcha
from django.shortcuts import redirect


def must_login_decorator(func):
    def wrapper_func(request, *args, **kwargs):
        if ('logedin' not in request.session):
            request.session['data'] = {
                'error': 'you should login', 'show': False}
            return redirect('/login/')

        return func(request, *args, **kwargs)
        # Do something after the function.
    return wrapper_func


def has_role(role):
    def decorator_role(func):
        def wrapper_func(request, *args, **kwargs):
            if (request.session.get('logedin') and request.session.get('logedin')['role'] != role):
                request.session['data'] = {
                    'error': 'you dont have permission for this action', 'show': False}
                return redirect('/')

            return func(request, *args, **kwargs)
            # Do something after the function.
        return wrapper_func
    return decorator_role


def generate_cap_image(txt, ccid):
    image = ImageCaptcha(width=280, height=90)
    captcha_text = txt
    image.generate(captcha_text)
    return image.write(captcha_text, 'static/' + ccid + '.png')


class CustomFlashMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        try:
            if (request.session['data']['show']):
                del request.session['data']

            if (request.session['data']):
                request.session['data']['show'] = True
            
        except KeyError:
            pass
        
        response = self.get_response(request)

        return response
