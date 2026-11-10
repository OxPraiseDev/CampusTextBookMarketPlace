from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .forms import StudentSignUpForm, StudentEditForm
from .models import Student

def register_view(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to Campus Textbook Exchange, {user.username}! Account created successfully.")
            return redirect('home')
    else:
        form = StudentSignUpForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            
            # If the user is an admin/staff, send them to the dashboard
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')
                
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('home')

# --- ADMIN EDIT USER VIEW ---
@staff_member_required
def edit_user_view(request, user_id):
    user_to_edit = get_object_or_404(Student, id=user_id)
    
    if request.method == 'POST':
        form = StudentEditForm(request.POST, instance=user_to_edit)
        if form.is_valid():
            form.save()
            messages.success(request, f"User '{user_to_edit.username}' has been updated successfully.")
            return redirect('admin_dashboard')
    else:
        form = StudentEditForm(instance=user_to_edit)
        
    return render(request, 'edit_user.html', {'form': form, 'edit_user': user_to_edit})