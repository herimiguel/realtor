from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import locale

def index(request):
    return render(request, 'my_app/index.html')

def register(request):
    if request.method=='POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        email= request.POST['email']
        password= request.POST['password']
        isValid=True
        minVal= 2
        maxVP= 8
    if len(request.POST['first_name']) < minVal:
        messages.error(request, 'Name needs to be at least 2 characters!')
        isValid = False
    if len(request.POST['last_name']) < minVal:
        messages.error(request, 'Last Name needs to be at least 2 characters!')
        isValid = False
    if len(request.POST['email']) < minVal:
        messages.error(request, 'Email is required!')
        isValid = False
    if request.POST['email'] != email:
        messages.error(request, 'Email is already registered!')
        isValid = False
    if len(request.POST['password']) < minVal:
        messages.error(request, 'Password is required!')
        isValid = False
    if request.POST['conPassword'] != request.POST['conPassword']:
        messages.error(request, 'Password confirmation failed!')
        isValid = False

    if not isValid:
        return redirect('/')

    if request.POST['conPassword'] == password:
        try:
            user=User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password )
        except IntegrityError:
            messages.error(request, 'This Email is already registered!')
            return redirect('/')
        request.session['user.id']= user.id
    return redirect('my_app:dashboard')        
    # return render(request,'my_app/success.html')

def login(request):
    if request.method=='POST':
        email = request.POST['email']
        password= request.POST['password']
        isValid= True
        minVal= 2
    if len(request.POST['email']) < minVal:
        messages.error(request, 'Email is required!')
        isValid = False
    if len(request.POST['password']) < minVal:
        messages.error(request, 'Password is required!')
        isValid = False
    try:
        User.objects.get(email=request.POST['email'], password= request.POST['password'])
    except ObjectDoesNotExist:
        messages.error(request, "Email and Password don't match!")
        isValid = False
    else:
        messages.error(request, "YOU ARE NOW LOGGED IN!")

    if not isValid:
        return redirect('/')
    else:
        request.session['user.id'] = (User.objects.get(email=request.POST['email'])).id
        return redirect('my_app:dashboard') 
    # return render(request, 'my_app/success.html')

def dashboard(request):
    user= request.session['user.id']
    context={
        'user': User.objects.get(id=request.session['user.id'])
    }
    return render(request, 'my_app/dashboard.html', context)

def learn(request):
    
    return render(request, 'my_app/learn.html')

def logOut(request):
    request.session.clear()
    messages.success(request, 'Successfully logged out')
    return redirect('/')

def finance(request):
    if request.method=='POST':
        isValid = True
        minVal = 1
        if len(request.POST['income']) < minVal:
            messages.error(request, 'Gross Income is required')
            isValid = False 
        if len(request.POST['carPayment']) < minVal:
            messages.error(request, 'Amount of car Payment is required! enter 0 if you do not have a payment')
            isValid = False
        if not isValid:
            return redirect('my_app:englishDash')
        else:
            income = request.POST['income']
            carPayment = request.POST['carPayment']
            request.session['downpayment'] = request.POST['downpayment']
            userObject = User.objects.get(id = request.session['user.id'])
            newInc = float(income)
            cPayment = float(carPayment)
            newIn = int(income) - int(carPayment)
            moneyObject = Money.objects.create(income = income, carPayment = carPayment, newIncome = newIn)
            moneyObject.save()
            newAddition = Addition.objects.create(user = userObject, money = moneyObject)
            newAddition.save()
            request.session['currentAddition'] = newAddition.id
            return redirect('my_app:showBuyer')
    

def showBuyer(request):
    currentUser = User.objects.get(id = request.session['user.id'])
    currentAddition = Addition.objects.get(id = request.session['currentAddition'])
    newIncome = currentAddition.money.newIncome
    carPayment = currentAddition.money.carPayment
    carPayment = float(carPayment)
    newIncome = float(newIncome)
    income = currentAddition.money.newIncome
    locale.setlocale( locale.LC_ALL, 'en_CA.UTF-8' )
    downpayment = request.session['downpayment']
    downpayment1 = float(downpayment)
    downpayment = (downpayment1 / 100)
    income = float(income)
    income = (income * .42) * 100
    downpayment = float(income) * float(downpayment)
    income = locale.currency( income, grouping=True )
    downpayment = locale.currency( downpayment, grouping=True )
    newIncome = locale.currency( newIncome, grouping=True )
    carPayment = locale.currency( carPayment, grouping=True )
    context={
        'user': currentUser,
        'newIncome':newIncome,
        'carPayment':carPayment,
        'income':income,
        'downpayment':downpayment,
        'percentage':request.session['downpayment']
    }
    return render(request, 'my_app/showBuyer.html', context)

def englishDash(request):
    user = request.session['user.id']
    context={
        'user': User.objects.get(id=request.session['user.id']),
        'money': Money.objects.all()
    }
    return render(request, 'my_app/englishDash.html', context)

def delete(request, id):
    money = Money.objects.get(id=id)
    money.delete()
    return redirect('my_app:englishDash')

def spanishDash(request):
    return render(request, 'my_app/spanishDash.html')