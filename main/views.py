from django.contrib.messages.api import get_messages
from django.shortcuts import redirect, render, HttpResponse
from .models import Users, Messages, Comments
from .decorators import login_required
from django.contrib import messages
import bcrypt

@login_required
def index(request):
    comment_all = Comments.objects.all()
    messages = Messages.objects.all()
    data = {
        'messages':messages,
        'comments':comment_all
    }
    return render(request, 'index.html', data)
    
def signin(request):
    if request.method == 'GET':
        return render(request,'form.html')
    else:
        first = request.POST['first_name']
        last = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        pass_confirm = request.POST['password_confirm']

        if password != pass_confirm:
            messages.error(request,"passwords doesn't match")
            return redirect('/form')
        else:
            new_user = Users.objects.create(
            first_name = first,
            last_name = last,
            password= bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode(),
            email=email
            )
            request.session['user'] = {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last': new_user.last_name,
                'email': new_user.email
            }
            messages.success(request,'user created')
            return redirect('/')

def login(request):
    email_in = request.POST['email']
    pass_in = request.POST['password']
    #traer al usuario
    try:
        user_in = Users.objects.get(email = email_in)
    except Users.DoesNotExist:
        messages.error(request, 'User or password incorrect')
        return redirect('/form')

    if not bcrypt.checkpw(pass_in.encode(), user_in.password.encode()):
        messages.error(request, 'User or password incorrect')
        return redirect('/form')
    
    request.session['user'] ={
        'id' : user_in.id,
        'first_name' : user_in.first_name,
        'last_name' : user_in.last_name,
        'email': user_in.email
    }
    messages.success(request, f'Hola {user_in.first_name}')
    return redirect('/')

def logout(request):
    try:
        del request.session['user']
    except KeyError:
        messages.error(request,'Ooops something wrong')
    return redirect('/form')

@login_required
def post_message(request):
    incoming_message = request.POST['mensaje']
    bring_user = Users.objects.get(id = request.session['user']['id'])
    new_message = Messages.objects.create(message = incoming_message, user_m = bring_user)
    return redirect('/')

@login_required
def delete_message(request,id):
    get_message = Messages.objects.get(id=id)
    id_user = get_message.user_m.id
    if id_user == request.session['user']['id']:
        get_message.delete()
        messages.success(request,'Message deleted!')
        return redirect('/')
    else:
        messages.error(request,"Message can't be eliminated")
        return redirect('/')

def post_comment(request,id_m):
    incoming_comment = request.POST['comment']
    get_message = Messages.objects.get(id = id_m)
    get_user = Users.objects.get(id=request.session['user']['id'])
    new_comment = Comments.objects.create(comment = incoming_comment, user_c = get_user, message_c =get_message)
    return redirect('/')