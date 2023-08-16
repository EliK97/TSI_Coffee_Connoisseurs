from django.shortcuts import render, redirect,HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Coffee, User_review
from django.urls import reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .forms import User_reviewForm

# Create your views here.


def home(request):
  return render(request, 'home.html')

def coffee_index(request):
  coffees = Coffee.objects.all()
  return render(request, 'coffee/index.html', {
    'coffees': coffees
  })

# class CoffeeDetail(DetailView):
    
def coffee_detail(request, coffee_id):
  coffee = Coffee.objects.get(id=coffee_id)
  review_form = User_reviewForm()
  return render(request, 'coffee/detail.html',{
    'coffee' : coffee, 'review_form' : review_form
  })

def add_review(request, coffee_id):
    coffee_instance = Coffee.objects.get(id=coffee_id)
    form = User_reviewForm(request.POST)

    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.coffee = coffee_instance
        new_review.user = request.user
        new_review.save()
    return redirect('detail', coffee_id=coffee_id)
  

def signup(request):
  error_message = ''
  if request.method == 'POST':
   
    form = UserCreationForm(request.POST)
    if form.is_valid():
      
      user = form.save()
      
      login(request, user)
      return redirect('/') # change back to index once we create the templae
    else:
      error_message = 'Invalid sign up - try again'
  
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


class CoffeeCreate(CreateView):
  model = Coffee
  fields = ['brand', 'roast', 'flavor_profile', 'rating',
            'review', 'price' 
            ]
  def form_valid(self, form):
    # Check if the user is a superuser
    if not self.request.user.is_superuser:
        # If the user isn't a superuser, return a forbidden response or handle as you see fit
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You don't have permission to perform this action.")
    
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the Coffee
    # Let the CreateView do its job as usual
    return super().form_valid(form)
  
class CoffeeUpdate(UpdateView):
  model = Coffee
  # Let's disallow the renaming of a Coffee by excluding the name field!
  fields = ['brand', 'flavor_profile', 'rating', 'review', 'price']
  def form_valid(self, form):
    # Check if the user is a superuser
    if not self.request.user.is_superuser:
        # If the user isn't a superuser, return a forbidden response or handle as you see fit
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You don't have permission to perform this action.")
    
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the Coffee
    # Let the CreateView do its job as usual
    return super().form_valid(form)

class CoffeeDelete(DeleteView):
  model = Coffee
  success_url = '/coffee'
  def form_valid(self, form):
    # Check if the user is a superuser
    if not self.request.user.is_superuser:
        # If the user isn't a superuser, return a forbidden response or handle as you see fit
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden("You don't have permission to perform this action.")
    
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the Coffee
    # Let the CreateView do its job as usual
    return super().form_valid(form)  
  
class ReviewUpdate(UpdateView):
  model = User_review
  fields = ['user_rating', 'user_review']  

class ReviewDelete(DeleteView):
   model = User_review
   success_url = '/coffee'
  
  
  


  
