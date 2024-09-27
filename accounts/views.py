from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages  
import re
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
 return render(request,
 'accounts/dashboard.html',
 {'section': 'dashboard'})




def signin(request):
        if request.method =='POST' and 'btnlogin' in request.POST:

            username = request.POST['user']
            password = request.POST['pass']

            user = auth.authenticate(username = username, password = password )

            if user is not None:
                auth.login(request, user)
                # messages.success(request, 'you are now logged in')
            else:
                messages.error(request ,'Username or password invaild')
            return redirect('signin')
        else:   
            return render(request,'accounts/signin.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        messages.success(request ,'Logged out')
        return redirect('signin')



def signup(request):
        if request.method =='POST' and 'btnsignup' in request.POST:
        

         #متغيرات للحقول 
            fname = None
            lname= None
            address = None
            adderss2 = None
            city = None
            state = None
            zip_number = None
            email= None
            username= None
            password = None
            terms = None
            is_added=None


            #ناخذ المتغيرات من الفورم
            if 'fname' in request.POST: fname = request.POST['fname']
            else: messages.error(request, 'Erorr in first name')

            if 'lname' in request.POST: lname = request.POST['lname']
            else: messages.error(request, 'Erorr in last  name ')

            if 'address' in request.POST: address = request.POST['address']
            else: messages.error(request, 'Erorr in address  ')

            if 'address2' in request.POST: address2 = request.POST['address2']
            else: messages.error(request, 'Erorr in address2  ')
            
            if 'city' in request.POST: city = request.POST['city']
            else: messages.error(request, 'Erorr in city  ')

            if 'state' in request.POST: state = request.POST['state']
            else: messages.error(request, 'Erorr in state  ')

            if 'zip' in request.POST: zip_number = request.POST['zip']
            else: messages.error(request, 'Erorr in zip  ')

            if 'email' in request.POST: email = request.POST['email']
            else: messages.error(request, 'Erorr in email')

            if 'user' in request.POST: username = request.POST['user']
            else: messages.error(request, 'Erorr in username  ')

            if 'pass' in request.POST: password = request.POST['pass']
            else: messages.error(request, 'Erorr in password  ')
            if 'terms' in request.POST: terms = request.POST['terms']

            #نتحقق من لقيم 
            if fname and lname and  address and address2 and  city and state and zip_number and email and username and  password:
                if terms=='on':
                    #التحقق من ان اليوزر مأخوذ
                    if User.objects.filter(username=username).exists():
                         messages.error(request,'this username is taken ')
                    else:
                        #التحقق من الايميل 
                       if User.objects.filter(email=email).exists():
                        messages.error(request,'this email is taken ')
                       else:
                        patt ="^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                        if re.match(patt,email):
                            #add user 
                            user= User.objects.create_user(
                            first_name=fname,last_name=lname,
                            email=email,username=username,
                            password=password)
                            user.save()
                            #clear fileds
                            fname= '' 
                            lname ='' 
                            address=''  
                            address2='' 
                            city =''
                            state=''
                            zip_number =''
                            email='' 
                            user =''
                            password =''
                            terms=None
                            #success Message
                            messages.success(request,'You account is created')
                            is_added= True
                        else:
                            messages.error(request,'Invaild email')

                else:
                    messages.error(request,'you must agree to the terms')
            else:
                messages.error(request, 'check empty fileds') 
         
            return render (request,'accounts/signup.html',{
                'fname':fname,
                'lname':lname,
                'address':address,
                'address2':adderss2,
                'city':city,
                'state':state,
                'zip':zip_number,
                'email':email,
                'user':username,
                'pass':password,
                'is_added':is_added
            })
        else:   
            return render(request,'accounts/signup.html')
        

        
