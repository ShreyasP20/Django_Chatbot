from django.shortcuts import render, redirect
from django.http import JsonResponse
import google.generativeai as genai
import json
from django.contrib import auth
from django.contrib.auth.models import User
# Create your views here.

genai.configure(api_key='Google_APIKEY')
model = genai.GenerativeModel('gemini-pro')

def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = model.generate_content(message)
        return JsonResponse({'message':message, 'response':response})
    return render(request, 'Chabot/chabot.html')

def login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password= password)
        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = 'Invalid Username or password'
            return render(request, 'Chabot/login.html', {'error_message':error_message})
    else:
        return render(request, 'Chabot/login.html')



def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        
        if password1 == password2:
            try:
                user = User.objects.create_user(username, email, password1)
                user.save
                auth.login(request, user)
                return redirect('chatbot')
            except:
                error_message = 'Error Creating Acc'
                return render(request, 'Chabot/register.html', {'error_message':error_message})    
        else:
            error_message = "PASSWORD dont Match"
            return render(request, 'Chabot/register.html', {'error_message':error_message})
    return render(request, 'Chabot/register.html')

def logout(request):
    auth.logout(request)
