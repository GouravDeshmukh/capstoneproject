from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProjectForm
from .models import Project,Tag,Review
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ReviewForm

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

from django.shortcuts import render

def landing_page(request):
    return render(request, 'landing.html')

def home(request):
    return render(request, 'landing.html')

def about(request):
    return render(request, 'landing.html')

def contact(request):
    return render(request, 'landing.html')

def profile_view(request):
    return render(request, 'profile.html')

@login_required
def profile_view(request):
    return redirect('view_my_projects')  # Redirect to 'My Projects' by default

@login_required
def create_project_view(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)  # Create the project without saving to the database

            # Save the project instance first to get the project ID
            project.user = request.user  # Assuming you're associating the project with the logged-in user
            project.save()

            # Handle tags
            tags = form.cleaned_data.get('tags')
            for tag in tags:
                project.tags.add(tag)  # Associate selected tags with the project

            # If you want to create new tags as well, you can add logic here
            new_tag_names = request.POST.getlist('new_tags')
            for tag_name in new_tag_names:
                tag_name = tag_name.strip()
                if tag_name:  # Avoid creating empty tags
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    project.tags.add(tag)  # Associate the newly created tag with the project

            return redirect('view_my_projects')  # Redirect to the My Projects page after saving
    else:
        form = ProjectForm()
    
    return render(request, 'create_project.html', {'form': form})
@login_required
def view_my_projects_view(request):
    # Fetch the user's projects
    user_projects = Project.objects.filter(user=request.user)
    return render(request, 'my_projects.html', {'projects': user_projects})

@login_required
def view_all_projects_view(request):
    projects = Project.objects.all()  # Fetch all projects
    # Handle tag filtering
    tag_id = request.GET.get('tag_id')
    if tag_id:
        projects = projects.filter(tags__id=tag_id)

    tags = Tag.objects.all()  # Get all tags to display in the search form
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        projects = projects.filter(title__icontains=search_query)  # Filter by title

    # Sorting functionality
    sort_by = request.GET.get('sort', 'title')  # Default sorting by title
    projects = projects.order_by(sort_by)

    return render(request, 'all_projects.html', {'projects': projects, 'search_query': search_query,'tags': tags})

@login_required
def my_projects(request):
    projects = Project.objects.filter(user=request.user)  # Assuming projects are associated with a user
    return render(request, 'my_projects.html', {'projects': projects})

@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)  # Ensure the user owns the project
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully.')
        return redirect('view_my_projects')  # Redirect to the my_projects page after deletion
    
    return render(request, 'delete_project_confirm.html', {'project': project})

@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, user=request.user)  # Ensure the user owns the project

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('view_my_projects')  # Redirect to 'my_projects' page after editing
    else:
        form = ProjectForm(instance=project)  # Pre-fill the form with the current project data

    return render(request, 'edit_project.html', {'form': form, 'project': project})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    reviews = project.reviews.all()  # Get all reviews for this project

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Check if user has already rated this project
            if not Review.objects.filter(project=project, user=request.user).exists():
                review = form.save(commit=False)
                review.project = project
                review.user = request.user
                review.save()
                return redirect('project_detail', pk=project.pk)
    else:
        form = ReviewForm()

    # Check if the user has already rated this project
    user_review = None
    if request.user.is_authenticated:
        try:
            user_review = Review.objects.get(project=project, user=request.user)
        except Review.DoesNotExist:
            user_review = None

    return render(request, 'project_detail.html', {
        'project': project,
        'reviews': reviews,
        'form': form,
        'user_review': user_review,
    })