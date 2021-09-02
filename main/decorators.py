from django.shortcuts import redirect, render, HttpResponse

def login_required(funct):
    def wrapper(request,*args,**kwargs):
        if 'user' not in request.session:
            return redirect('/form')
        resp = funct(request,*args,**kwargs)
        return resp
    return wrapper
