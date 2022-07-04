from email.headerregistry import Address
from django import views
from django.shortcuts import render,redirect
from django.views import View
from requests import request
from .forms import*
from django.contrib import auth
# Create your views here.
class AdminLoginView(View):
    def get(self,request,*args,**kwargs):
        form = LoginForm
        # if request.user.is_authenticated:
        #     return redirect('/userview')
        return render(request, 'login.html',{'form':form})

    def post(self,request,*args,**kwargs):
        form = LoginForm(request.POST or None)
        
        if form.is_valid():
            em = request.POST['email']
            user = User.objects.get(is_superuser=True , email=em)
            
            auth.login(request,user)
            return redirect('/userRegistration') 
        return render(request, 'login.html',{'form':form})


class AdminLogoutView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated | request.user.is_superuser == True :
           auth.logout(request)
           return redirect('/login/')
        return redirect('')


class UserRegistration(View):
    def get(self,request):
        form=Profileform()
        return render(request, 'userRegistration.html',context={'form':form,'active':'btn btn-primary'})
    def post(self,request):
        form=Profileform(request.POST,request.FILES)
        if form.is_valid():
            username=form.cleaned_data['username']
            first_name=form.cleaned_data['first_name']
            password2=form.cleaned_data['password2']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            hobbies=form.cleaned_data['hobbies']
            address=form.cleaned_data['address']
            gender=form.cleaned_data['gender']
            mobile_number=form.cleaned_data['mobile_number']
            profile=form.cleaned_data.get('profile')
            
            us=User()
            us.username=username
            us.set_password(password2)
            us.first_name=first_name
            us.last_name=last_name
            us.email=email
            us.save()

            res=Usredetails()
            res.user=us
            res.address=address
            res.gender=gender
            res.hobbies=hobbies
            res.mobile_number=mobile_number
            res.profile=profile 
            res.save()
            return redirect('/userview')
        return render(request, 'userRegistration.html',context={'form':form,'active':'btn btn-primary'})


class UserViews(View):
    def get(self,request):
        if request.user.is_authenticated:
            if request.GET.get("search") == 'username':
                us=Usredetails.objects.filter(user__username__icontains=request.GET.get('search1'))
            elif request.GET.get("search") == 'gender':
                us=Usredetails.objects.filter(gender__iexact=request.GET.get('search1'))
            elif request.GET.get("search") == 'hobbies':
                us=Usredetails.objects.filter(hobbies__icontains=request.GET.get('search1'))
            else:
                us=Usredetails.objects.all()
            return render(request,'userView.html',context={'data':us}) 
        return redirect('/login')
    
class UserDelete(View):
    def get(self,request,pk):
        if request.user.is_authenticated:
            us=User.objects.get(pk=pk)
            us.delete()
            return redirect(request.META['HTTP_REFERER'])
        return redirect('/login')

class UserEditView(View):
    def get(self, request,pk):
        if request.user.is_authenticated:
                user = request.user 
                form = AdminProfileEditForm
                userotherinfo = Usredetails.objects.get(pk=pk) 
                context = {
                    'form' : form,
                    'user' : userotherinfo,
                }
                return render(request, 'profileEdit.html',context)
        return redirect('/login')
        
    
    def post(self, request,pk):
        user = request.user
        if request.user.is_authenticated:
            form = AdminProfileEditForm(request.POST or None,request.FILES)
            userotherinfo = Usredetails.objects.get(pk=pk)
            context = {
                    'form' : form,
                    'user' : userotherinfo,
                }
            
            if form.is_valid():
                data            = form.cleaned_data
                first_name      = data['first_name']
                last_name       = data['last_name']
                email           = data['email']
                mobile_number   = data['mobile_number']
                gender          = data['gender']
                address         =data['address']
                hobbies         =data['hobbies']
                profile  = data.get('profile_image')
                
                userotherinfo.user.first_name = first_name                    
                userotherinfo.user.last_name  = last_name
                userotherinfo.user.email      = email
                userotherinfo.user.save()
                userotherinfo.mobile_number = mobile_number
                userotherinfo.address       =address
                userotherinfo.hobbies      =hobbies
                userotherinfo.gender        = gender
                if profile:
                    userotherinfo.profileimg = profile

                userotherinfo.save()

            return redirect('/userview')    

        return render(request, 'profileEdit.html',context)

