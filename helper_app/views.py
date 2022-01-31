from django.shortcuts import render, redirect
from django.contrib import messages
from . models import *
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name = request.POST['first_name'], last_name = request.POST['last_name'], email = request.POST['email'], password = pw_hash)
        request.session['user_id'] = new_user.id
        return redirect('/dashboard')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        this_user = User.objects.get(email = request.POST['email'])
        request.session['user_id'] = this_user.id
        return redirect('/dashboard')
    return redirect('/')

def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:   
        context = {
        'current_user': User.objects.get(id = request.session['user_id']),
        'all_jobs': Job.objects.all()
    }
        return render(request, 'dashboard.html', context)
    

def logout(request):
    request.session.flush()
    return redirect('/')

def add_job(request):
    return render(request, 'add_job.html')

def job_create(request):
    if request.method == 'POST':
        errors = Job.objects.job_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/add_job')
        job_to_create = Job.objects.create(title = request.POST['title'], description = request.POST['description'], location = request.POST['location'], added_by = User.objects.get(id = request.session['user_id']))
        return redirect('/dashboard')
    return redirect('/add_job')

def job_details(request, job_id):
    context = {
        'current_job': Job.objects.get(id = job_id)
    }
    return render(request, 'job_details.html', context)

def claim_job(request, job_id):
    job_to_claim = Job.objects.get(id = job_id)
    current_user = User.objects.get(id = request.session['user_id'])
    job_to_claim.belongs_to_user= current_user
    job_to_claim.save()
    return redirect('/dashboard')

def edit(request, job_id):
    context = {
        'current_job': Job.objects.get(id = job_id)
    }
    return render(request, 'edit.html', context)

def edit_job(request, job_id):
    if request.method == 'POST':
        errors = Job.objects.job_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/edit/{job_id}')
        job_to_edit = Job.objects.get(id = job_id)
        job_to_edit.title = request.POST['title']
        job_to_edit.description = request.POST['description']
        job_to_edit.location = request.POST['location']
        job_to_edit.save()
    return redirect('/dashboard')
    
def delete(request, job_id):
    job_to_delete = Job.objects.get(id = job_id)
    job_to_delete.delete()
    return redirect('/dashboard')



# Create your views here.

# Create your views here.
