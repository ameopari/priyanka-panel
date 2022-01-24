from typing_extensions import final
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.views import View
from django.contrib import messages
from django.urls import reverse
import re
from .models import *
import json
from django.http import JsonResponse
from time import sleep
from django.core.mail import send_mail
from NewProject.settings import *
import random
from datetime import datetime  
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from social_django.models import UserSocialAuth
from django.contrib.auth import update_session_auth_hash


# Create your views here.



@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def settings(request):
    user = request.user

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'settings.html', {
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'password.html', {'form': form})


# def update_user_social_data(strategy, *args, **kwargs):
#   response = kwargs['response']
#   backend = kwargs['backend']
#   user = kwargs['user']

#   if response['picture']:
#     # user_data = user.user_social_data_set.filter(provider='google')[0].extra_data
#     url = response['picture']
#     userProfile_obj = UserProfile()
#     userProfile_obj.user = user
#     userProfile_obj.picture = url
#     userProfile_obj.save()
    

def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    url = None
    profile, created = UserProfile.objects.get_or_create(user=user)

    if backend.name == "google-oauth2":

        # ------------------google image -------------------------
        url = response.get('picture')
        final_url = url[:url.index('=s96')] + "=s432-c"
        profile.social_img = final_url
        profile.save()
        print("profile saved with picture - google")



def Home(request):
    return render(request,'header.html')

def Base(request):
    return render(request,'header.html')

class Register(View):
    # template_name="register.html"
    def get(self,request):
        return render(request,'register.html')

    def post(self,request):
        print(request.POST,'---rrrppppp')
        data = {
            'status' : False
        }
        username= request.POST.get('username')
        email= request.POST.get('email')
        password=request.POST.get('pasword')
        confirmpass=request.POST.get('re_pasword')

        try:
            User.objects.get(email=email)
            return HttpResponse("email already exists")

        except User.DoesNotExist:
            if password == confirmpass:
                u=User.objects.create(username=username,email=email)
                u.set_password(password)
                u.save()
                data['status'] = True
                data['message'] = 'updated!'
                messages.success(request, 'Now you can login')
                return HttpResponseRedirect('login')
                # return HttpResponse("REGISTERRRRR")
            else:
                messages.error(request, 'password doesnt match')
        except Exception as e:
            print(e)
            data['status'] = False
            data['message'] = 'Error'
        finally:
            return HttpResponse(json.dumps(data), content_type="application/json")


           # print(e,'-no user exists')
            #return HttpResponse(e)

class Login(View):
    def get(self,request):
        print("in get method")
      
        return render(request,'login.html')
    def post(self,request):
        
        print(request.POST)
        email= request.POST['email']
        password = request.POST['password']
        print("in post method")
        print("email",email,"password",password)

        try:
            user = User.objects.get(email=email)
            print("user value",user)
            user = authenticate(username= user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'logged in')
                print("logged in user is ",user)
                return render(request,'index.html',locals())
            else:
                 messages.error(request, "Invalid Credentials")
                 return HttpResponseRedirect("login")
        except Exception as e:
            print(e)
            messages.error(request, 'User not exists with given username')
            return HttpResponseRedirect("login")

class Logout(View):
    # def post(self,request):
    #     logout(request)
    #     return HttpResponseRedirect('home')

    def get(self,request):
        logout(request)
        return HttpResponseRedirect('/')
    
class Create(View):
    def get(self,request):
        if request.user.is_staff:
            return render(request,'create.html')
        return HttpResponse("you cannot access this page!")

    def post(self,request):
        print(request.POST)
        name = request.POST.get('name')
        standard = request.POST.get('standard ')
        roll_no = request.POST.get('roll_no')
        obj = Student(name=name,standard=standard,roll_no=roll_no)
        obj.save()
       
        return HttpResponse('CREATED')
         # return render(request,'create.html')
    

def show(request):
    s=Student.objects.all()
    return render(request,'show.html',locals())


def upd(request,id):
    if request.method == "POST":
        print(request.POST)
        data = {
            'status' : False
        }
        try:
            s = Student.objects.get(id = id)
            s.name = request.POST.get('username')
            s.standard = request.POST.get('std')
            s.roll_no = request.POST.get('roll')
            s.save()
            data['status'] = True
            data['message'] = 'updated!'
        
        except Exception as e:
            data['message'] = "not-updated!"
        
        finally:
            # print("b4 sleep")
            # sleep(10)
            # print("after sleepo")
            return HttpResponse(json.dumps(data), content_type="application/json")

    else:
        s = Student.objects.get(id = id)
        return render(request,"update.html",locals())


def delete(request,id):
    # s= Student.objects.get(id=id)
    # s.delete()
    # messages.info(request,'User Delete')
    # return HttpResponseRedirect(reverse('show'))
    if request.method == 'POST':
        data = {'status':False}
        try:
            s=Student.objects.get(id=id)
            s.delete()
            
            data['status']=True
            data['message']= 'Deleted !'
        except Exception as e:
            data['message'] = 'Failed to Delete'
        finally:
            return HttpResponse(json.dumps(data),content_type="application/json")
    else:
        s = Student.objects.all()
        return render(request,'show.html',locals())
    

# def Update(request,id):
#     if request.method == "POST":
#         return HttpResponse("update post")
#     else :
#         return HttpResponse("running else statement")
    

    # if request.method == "POST":
    #     print(request.POST,'---rpppp')
    #     # data={
    #     #     'status':False,
    #     # }
    #     try:
    #         s = Student.objects.get(id = id)
    #         s.name = request.POST.get('username')
    #         s.standard = request.POST.get('std')
    #         s.roll_no = request.POST.get('roll')
    #         s.save()
    #         # data['status'] = True
    #         # data['message'] = 'updated'
    #         # print(data,'-----data')
    #     except Exception as e:
    #         print(e)

    #     return HttpResponse(json.dumps(data), content_type="application/json")
    
    # try:
    #     s = Student.objects.get(id = id)
    #     return render(request,"update.html",locals())
    # except Exception as e:
    #     return HttpResponse("student doesnt exist")
            
def forgotPassword(request):
    if request.method=='POST':
        email=request.POST.get('email')
        print(email,'----eeeee')

        try:
            e=User.objects.get(email=email)
            print('user email',e.email)
            e_=e.email
            n = str(random.randint(0,10000))
            print(n)
           
            send_mail(
                'Now you can Reset Password',
                'http://127.0.0.1:8000/changepass/{}'.format(n),
                'damanpreetkaurameotech@gmail.com',
                [e_],
                fail_silently=False,
            )
            # return HttpResponse('email found')
            messages.success(request,'Email Sent')
            data = ForgetPassword.objects.create(user=e,code=n)
            data.save()
            print('saveddd------')
            return HttpResponseRedirect(reverse('forgot'))
        except Exception as e:
            print(e)
            messages.info(request,'Email does not exist.')
            return HttpResponseRedirect(reverse('forgot'))
        

    else:
        return render(request,'forgot.html')

    


class changePassword(View):
    def get(self,request,code):
        print(code,'---------code')
       
        try:
            forgot_pass=ForgetPassword.objects.get(code=code)
            old=forgot_pass.time
            cur = datetime.now()
            
            print(old,'----olddd')
            print(cur,'----newwwww')
            v=cur.minute - old.minute
            h=old.hour - cur.hour 
            print(v,'----v')
            print(h,'----h')

            if h>0 or h<0 :
                messages.info(request,'link expire!')
                return HttpResponseRedirect(reverse('forgot'))

            elif(v>=10) :
                messages.info(request,'Time expire! Please verify again.')
                return HttpResponseRedirect(reverse('forgot'))

            else:            


                print(forgot_pass,'forgot---------')
                return render(request,'changepass.html',locals())
        except Exception as e:
            print(e)
            messages.info(request,'Enter valid url.....')
          
            return HttpResponseRedirect(reverse('forgot'))
        
     

    def post(self,request,code):
        print(request.POST,'-requestpost----')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        

        if password == confirm_password:
            try:
                forgot_pass=ForgetPassword.objects.get(code=code)
                forgot_pass.user.set_password(password)
                forgot_pass.user.save()
                forgot_pass.delete()
                messages.success(request,'Password Updated')
                return HttpResponseRedirect(reverse('login'))
            
            except ForgetPassword.DoesNotExist:
                messages.info(request,'Invalid otp')
        else:
            return HttpResponse("User not save")


class Products(View):
    def post(self,request):
            print(request.POST)
            name = request.POST.get('product_name')
            desc= request.POST.get('product_desc')
            img = request.FILES.get('product_img')
            status =request.POST.get('status')
            price = request.POST.get('product_price')
            print(status)
            obj = Product.objects.create(product_name=name,product_desc=desc,product_img=img,product_price=price)
            if status == 'available':
                obj.product_status=True
            else:
                obj.product_status=False
            obj.save()
        
            return HttpResponse('PRODUCT ADDED') 

    def get(self,request):
        return render(request,'product.html')
    

class AllProduct(View):
    def get(self,request):
        products=Product.objects.all()
        return render(request,'pshow.html',locals())
      


def Edit(request,id):
    if request.method == "POST":
        print(request.POST)
     
        try:
            P = Product.objects.get(id = id)
            P.name = request.POST.get('product_name')
            P.desc = request.POST.get('product_desc')
            P.img = request.POST.get('product_img')
            P.status = request.POST.get('product_status')
            P.price = request.POST.get('product_price')
            P.save()
           
        
        except Exception as e:
           print(e)
        
        finally:
            return render(request,'pshow.html')



    else:
        p = Product.objects.get(id = id)

        return render(request,"edit.html",locals())


# def Search(request):
#     users = User.objects.all()
#     final_list = []
#     for user in users:
#         final_list.append(
#             {
#                 'username' :user.username.lower(),
#                 'email' :user.email.lower()
#             }
#         )
    
#     final_list = json.dumps(final_list)
#     return render(request,'search.html',locals())


def Search(request):
   
        data = User.objects.all()
        # if 'q' in request.GET:
        q = request.GET.get('q', None)
        if q is not None:
            print(q,'========================q')
            # test = request.POST.get('q')
            data = data.filter(Q(username__icontains=q)|Q(email__icontains=q))
            return render(request,'search.html',{'data':data})
        else:
            return render(request,'search.html')
    

def UserEdit(request):
    if request.method == "POST":
        print(request.POST)
        id = request.POST.get('user_id')

        try:
            u = User.objects.get(id = id)
            username = request.POST.get('username')
            email = request.POST.get('email')   
            u.username=username
            u.email=email
            u.save()
            # return HttpResponse('EDITED')
        except Exception as e:
           print(e)

        return redirect('search')



      
