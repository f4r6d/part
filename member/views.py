import random

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.db import IntegrityError
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.hashers import make_password, check_password

from .models import Member
from .utils import must_login_decorator, has_role, generate_cap_image


def index(request):
    try:
        username = request.session['logedin']['name']
    except KeyError:
        username = 'anonymous'
    return render(request, 'member/index.html', {'name': username})


@has_role('admin')
@must_login_decorator
def admins(request):
    return render(request, 'member/admin_index.html')


@must_login_decorator
def logout(request):
    del request.session['logedin']
    return redirect('/')


def login(request):
    if request.method == 'POST':
        username = request.POST['username'].lower()
        password = request.POST['password']
        cap = request.POST['cap']

        if (cap != request.session['cap'][0] or request.COOKIES['cap_id'] != request.session['cap'][1]):
            request.session['data'] = {
                'error': 'wrong reCaptcha', 'show': False}
            return redirect('/login/')

        try:
            user = get_object_or_404(Member, username=username)
        except:
            request.session['data'] = {'error': 'wrong username', 'show': False}
            return redirect('/login/')

        if (check_password(password, user.password)):
            request.session['logedin'] = {
                'name': user.username, 'role': user.role}
            return redirect('/')
        else:
            request.session['data'] = {'error': 'wrong password', 'show': False}

    cap_text = random.randint(10000, 99999)
    ccid = str(random.random())
    request.session['cap'] = (str(cap_text), ccid)

    generate_cap_image(str(cap_text), ccid)

    context = {
        'cap_image': ccid + '.png'
    }
    resp = render(request, 'member/login_form.html', context=context)
    resp.set_cookie('cap_id', ccid)
    return resp


def register(request):
    if request.method == "POST":
        username = request.POST['username'].lower()
        email = request.POST['email']
        hashed_password = make_password(request.POST['password'])

        if (not username or not email):
            request.session['data'] = {
                'error': 'please fill the form', 'show': False}
            return redirect('/register/')

        user = Member(username=username, password=hashed_password, email=email)
        try:
            user.save()
        except IntegrityError as e:
            request.session['data'] = {
                'error': 'error duplicate email or username', 'show': False}
            return redirect('/register/')

        request.session['data'] = {
            'error': user.username + ' registered', 'show': False}
        request.session['logedin'] = {'name': user.username, 'role': user.role}
        return redirect('/')

    return render(request, 'member/register_form.html')


@must_login_decorator
def members(request):
    members = Member.objects.all()
    context = {'members': members}

    return render(request, 'member/list.html', context=context)


@must_login_decorator
def show(request, member_id):
    member = get_object_or_404(Member, pk=member_id)
    context = {'member': member}

    return render(request, 'member/show.html', context=context)


@has_role('admin')
@must_login_decorator
def delete(request, member_id):
    member = Member.objects.get(pk=member_id)
    member.delete()

    return HttpResponseRedirect(reverse('member:members.index'))


class MemberCreateView(CreateView):
    model = Member
    fields = '__all__'
    success_url = "/members/"

    # TODO: hash password before save


class MemberUpdateView(UpdateView):
    model = Member
    fields = '__all__'

    success_url = "/members/"

    # TODO: hash password before save
    # TODO: when update user role; change role in session too :(
