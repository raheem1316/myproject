# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.decorators import api_view
from rest_framework.response import Response

import datetime
import user

import os
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.core import mail
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from queriesapp.forms import SignupForm, LoginForm, UserForm, Profile, ProfileForm, ChangepasswordForm, CommentsForm
from queriesapp.models import Post, Comments
from queriesapp.models import Product_details, Seller_details, Orders


def home(request):
    data=Post.objects.all().order_by('-id')
    return render(request,'base.html',{'post':data})

def signup(request):
    if request.method =='POST':
        form= SignupForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:

                check_email=User.objects.filter(email=form.cleaned_data['email'])
                if len(check_email)==0:
                    data={
                    'first_name':form.cleaned_data['first_name'],
                    'last_name':form.cleaned_data['last_name'],
                    'email':form.cleaned_data['email'],
                    'password':make_password(form.cleaned_data['password']),
                    'username':form.cleaned_data['email']
                    }
                    user=User.objects.create(**data)

                    profile= Profile()
                    profile.user_details_id= user.id
                    profile.save()

                    login(request,user)

                    messages.success(request, 'you are regesterd successfully')

                    subject = 'signup info'
                    message = 'hi my dear {}'.format(request.user.email)
                    from_email = settings.EMAIL_HOST_USER
                    to_list = [request.user.email, ]
                    send_mail(subject, message, from_email, to_list, fail_silently=True)

                    return redirect('/queries/')
                else:
                    messages.error(request, 'This email is already Exist')
                    form = SignupForm()
                    return render(request, 'signup.html', {'signupform': form})
            else:
                messages.error(request, 'password must be same')
                form = SignupForm()
                return render(request, 'signup.html', {'signupform': form})

        else:
            messages.error(request, 'please enter valid details')
            form = SignupForm()
            return render(request, 'signup.html', {'signupform': form})
    else:

        form= SignupForm()
        return render(request,'signup.html',{'signupform':form})



def signin(request):
    if request.method =='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            user=authenticate(request,username=form.cleaned_data['email'],password=form.cleaned_data['password'])
            if user is not None:
                login(request,user)
                messages.success(request,'you are logged in successfully')

                subject = 'signup info'
                message = 'hi my dear {} .you are logged in succefully'.format(request.user.first_name)
                from_email = settings.EMAIL_HOST_USER
                to_list= [request.user.email,]
                send_mail(subject, message, from_email,to_list,fail_silently=True)

                return redirect('/queries/')
            else:
                messages.error(request, 'please enter valid details')
                form = LoginForm()
                return render(request, 'login.html', {'loginform': form})
        else:
            form = LoginForm()
            return render(request, 'login.html', {'loginform': form})
    else:
        form= LoginForm()
        return render(request,'login.html',{'loginform':form})


def addpost(request):
    if request.method == 'POST':
        post= request.POST['text']

        data=Post()
        data.post= post
        data.posted_by = request.user
        data.posted_time= datetime.datetime.now()
        data.save()

        return redirect('/queries/')


def editprofile(request):
    user = request.user
    if request.method == 'POST':
        userform=UserForm(request.POST,instance=user)
        profileform=ProfileForm(request.POST,files=request.FILES,instance=user.profile)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()

            messages.success(request, 'your profile is updated successfully')

            return redirect('/queries/')
        else:
            form1 = UserForm(instance=user)
            form2 = ProfileForm(instance=user.profile)
            messages.success(request, 'please enter valid data')

            return render(request, 'editprofile.html', {'UserForm': form1, 'ProfileForm': form2})
    else:
        form1 = UserForm(instance=user)

        form2 = ProfileForm(instance=user.profile)
        #print request.user.profile.profile_pic

        #print user.last_name
        return render(request,'editprofile.html',{'UserForm':form1,'ProfileForm': form2})

def change_password(request):
    if request.method == 'POST':
        form=ChangepasswordForm(request.POST)
        if form.is_valid():
            if check_password(form.cleaned_data['Old_password'], request.user.password):
                if form.cleaned_data['New_password'] == form.cleaned_data['Confirm_Newpassword']:
                    user = request.user
                    user.set_password(form.cleaned_data['New_password'])
                    user.save()
                    logout(request)
                    messages.success(request, 'your password is updated successfully. ')
                    return redirect('/queries/login/')

                else:
                    messages.error(request, 'password must be same')
                    form = ChangepasswordForm()
                    return render(request, 'change_password.html', {'form': form})

            else:
                messages.error(request, 'you enterd old password is wrong. please give correct details')
                form = ChangepasswordForm()
                return render(request, 'change_password.html', {'form': form})
    else:
        form=ChangepasswordForm()
        return render(request,'change_password.html',{'form':form})

def all_answers(request,id):
    post=get_object_or_404(Post,pk=id)

    if request.method == 'POST':
        form=CommentsForm(request.POST,files=request.FILES)
        #form2=Picform(request.POST,files=request.FILES)
        if form.is_valid():
            data=Comments()
            data.comment=form.cleaned_data['comment']
            data.commented_by=request.user
            data.post_details= post
            data.upload_time=datetime.datetime.now()
            if request.FILES:
                data.upload_file=request.FILES['upload_file']
            data.save()
            data2= Comments.objects.filter(post_details=post).order_by('-id')
            qus = Post.objects.filter(id=post.id)

            form1 = CommentsForm()
            #print request.FILES['upload_file']
            messages.success(request, 'you are commented successfully')

            connection = mail.get_connection()
            connection.open()
            subject = 'comment info'
            message = '{} is commented to your post'.format(request.user.email)
            from_email = settings.EMAIL_HOST_USER
            to_list = [post.posted_by.email, ]
            email=EmailMessage(subject, message, from_email, to_list)
            if request.FILES:
                email.attach_file(os.path.join(settings.MEDIA_ROOT,str(request.FILES['upload_file'])))
            #connection=get_connection(fail_silently=False)
            connection.send_messages([email],)
            connection.close()

            return render(request, 'all_answers.html', {'post': qus,'comment':data2, 'commentform': form1})
    else:
        form = CommentsForm()
        qus = Post.objects.filter(id=post.id)
        data2 = Comments.objects.filter(post_details=post).order_by('-id')
        return render(request, 'all_answers.html', {'post': qus,'comment':data2,'commentform': form})

def delete_comment(request,id):
    comment=get_object_or_404(Comments,pk=id)
    data1=Comments.objects.get(id=id).delete()
    data = Post.objects.filter(id=comment.post_details_id)
    data2 = Comments.objects.filter(post_details=comment.post_details).order_by('-id')
    # print data.ccount()
    form = CommentsForm()
    #return HttpResponse(data1)
    messages.success(request, 'your comment is deleted successfully')

    return render(request, 'all_answers.html', {'commentform': form, 'post': data, 'comment': data2})


def signout(request):
    logout(request)
    return redirect('/queries/')


def adskite(request):
    return render(request,'adskite_bot.html')

def hotel_booking(request):
    return render(request,'hotel_booking.html')

def course_details(request):
    return render(request,'course-details.html')

def weather_details(request):
    return render(request,'weather-details.html')

def sample(request):
    #x=str(data)
    return HttpResponse('raheem')

@api_view(['POST'])
def webhook(request):
    #print 'ok'
    if request.method == 'POST':
        data = request.data
        seller_details = Seller_details.objects.all()
        product_details = Product_details.objects.all()
        if data['result']['action']=='details':
            result=data['result']
            parameters=result['parameters']
            #contact_details =parameters['contact-details']
            #all=parameters['all-details']
            #client_details=Client_details.objects.all()
            if 'contact-details' in parameters:
                for i in range(len(seller_details)):
                    if parameters['contact-details']==seller_details[i].name:
                        #print 'ok'
                        #post1=post[i].number
                        speech = "The contact details of %s :: %s ,%s,%s" % (seller_details[i].name,seller_details[i].address,seller_details[i].number,'https://ibb.co/n4oQhR')
                        output = {"speech": speech, "display Text": speech, "source": "bankintrestrates"}
                        print output
                        return Response(output)
            elif 'staff-details' in parameters:
                details={}
                for i in range(len(seller_details)):
                    details[seller_details[i].name]=seller_details[i].number
                speech = "All contact details of adskite %s" % (details)
                output = {"speech": speech, "display Text": speech, "source": "bankintrestrates"}
                return Response(output)

        elif data['result']['action']=='products_information':
            result = data['result']
            parameters=result['parameters']
            product_information = Product_details.objects.filter(product_name=parameters['product_details'])
            if len(product_information) != 0:
                x = []
                for i in range(len(product_information)):

                    listing = "[Product-name :: %s ,, Product-Quantity :: %s ,, Product-price :: %s ,,Seller-name :: %s ,, Seller-address :: %s ,,Seller-number :: %s ]--->>>>"%(product_information[i].product_name,product_information[i].product_quantity,product_information[i].product_price,product_information[i].seller.name,product_information[i].seller.address,product_information[i].seller.number)
                    x.append(listing)
                #print product_information[0].product_name
                speech = "List of %s details and seller details are ::: %s"%(parameters['product_details'],x)
                output = {"speech": speech, "display Text": speech, "source": "bankintrestrates"}
                print speech
                return Response(output)
            else:
                output = {"speech": "sorry, we don't have that product currently..we will update it soon..", "display Text":"sorry, we don't have that product currently..we will update it soon.." , "source": "bankintrestrates"}
                return Response(output)

        elif data['result']['action']=='ordering':
            result = data['result']
            parameters = result['parameters']
            checking = Product_details.objects.filter(product_name=parameters['product_details'])
            if len(checking)!= 0:
                count = []

                for i in range(len(checking)):
                    if checking[i].seller.name == parameters['contact-details']:
                        count.append(i)

                if count:

                    orders = Orders()
                    orders.order_name = parameters['product_details']
                    orders.order_quantity = parameters['number']
                    orders.seller_name = parameters['contact-details']
                    orders.buyer_name = parameters['given-name']
                    orders.buyer_address = parameters['address']
                    orders.save()

                    speech = 'success .%s You orderd %s successfully' % (parameters['given-name'], parameters['product_details'])
                    output = {"speech": speech, "display Text": speech, "source": "ordering"}
                    print 'ordered'
                    return Response(output)

                else:
                    speech = 'Error.. you entered wrong seller details , please give properly '
                    output = {"speech": speech, "display Text": speech, "source": "ordering"}
                    print 'no seller'
                    return Response(output)


            else:
                speech = "sorry, we don't have that product currently..we will update it soon.."
                output = {"speech": speech, "display Text": speech, "source": "ordering"}
                print 'not ordered'
                return Response(output)

        elif data['result']['action']=='canceling':
            result = data['result']
            parameters = result['parameters']
            cancel_order = Orders.objects.filter(order_name=parameters['product_details'],seller_name=parameters['contact-details'],buyer_name=parameters['given-name'])
            if cancel_order:
                cancel_order.delete()
                speech = '%s Your order is cancelled successfully' % (parameters['given-name'])
                output = {"speech": speech, "display Text": speech, "source": "ordering"}
                print 'cancelled'
                return Response(output)
            else:
                speech = 'Error.. you entered wrong details , please give properly '
                output = {"speech": speech, "display Text": speech, "source": "ordering"}
                print 'not cancelled'
                return Response(output)
