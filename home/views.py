from django.shortcuts import render,HttpResponse
from django.db.models import Prefetch
from admn.models import Product,varient,coupen
from django.shortcuts import render,redirect
from .models import User
from admn.forms import pform,vform
from django.contrib.auth import logout,login
from django.views.decorators.cache import cache_control
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from docter.models import DoctorProfile
from patient.models import patientProfile,wallet
from admn.models import Product,varient,Medicine_type
from django.db.models import Prefetch
from patient.views import Pat_dashboard 
from django.core.mail import send_mail
import uuid
from datetime import datetime, timedelta
from patient.models import Address
from .models import Cart,CartItem,Order,orderItem
from decimal import Decimal
from .forms import Patient_form
from django.conf import settings
from django.db.models import Subquery, OuterRef
from django.core import serializers
import razorpay
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django_otp import devices_for_user
# from django_otp.plugins.otp_totp.models import TOTPDevice
from twilio.rest import Client
import random
from django.contrib import messages
from django.core.mail import EmailMessage


# User=settings.AUTH_USER_MODEL
# Create your views here.




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    return render(request,'index.html')

def contact(request):
    return render(request,'cont.html')

def about(request):
    return render(request,'cont.html')

def docter(request):
    return render(request,'docindex.html')

def department(request):
    return render(request,'depart.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def item(request):
    product=Product.objects.filter(catagory=1).prefetch_related(Prefetch('item',queryset=varient.objects.all()))
    # print(product)
    cate=Medicine_type.objects.filter(medicine_type=None).prefetch_related(Prefetch('subcate',queryset=Medicine_type.objects.all()))
        # context={'page':'ad-mg'}
    context={'item_list':product ,'item':'none','category':cate,}
    return render(request,'shop.html',context)
def medicine(request,med):
    product=Product.objects.filter(medicine_type__name=med,catagory=1).prefetch_related(Prefetch('item',queryset=varient.objects.all()))
    cate=Medicine_type.objects.filter(medicine_type=None).prefetch_related(Prefetch('subcate',queryset=Medicine_type.objects.all()))
    context={'item_list':product,'category':cate, 'item':med}
    return render(request,'shop.html',context)
# def tablet(request):
#     product=Product.objects.filter(medicine_type__name='tablet',catagory=1).prefetch_related(Prefetch('item',queryset=varient.objects.all()))
#     context={'item_list':product, 'item':'tablet'}
#     return render(request,'shop.html',context)
# def capsule(request):
#     product=Product.objects.filter(medicine_type__name='capsule',catagory=1).prefetch_related(Prefetch('item',queryset=varient.objects.all()))
#     context={'item_list':product ,'item':'capsule'}
#     return render(request,'shop.html',context)
# def syrup(request):
#     product=Product.objects.filter(medicine_type__name='syrup',catagory=1).prefetch_related(Prefetch('item',queryset=varient.objects.all()))
#     context={'item_list':product ,'item':'syrup'}
#     return render(request,'shop.html',context)
# def oiment(request):
#     product=Product.objects.filter(medicine_type__name='powder' and 'gel' ,catagory=1).prefetch_related(Prefetch('item',queryset=varient.objects.all()))
#     context={'item_list':product, 'item':'oinment'}
#     return render(request,'shop.html',context)
# def powder(request):
#     product=Product.objects.filter(medicine_type__name='powder',catagory=1).prefetch_related(Prefetch('item',queryset=varient.objects.all()))
#     context={'item_list':product, 'item':'powder'}
#     return render(request,'shop.html',context)
# def gel(request):
#     product=Product.objects.filter(medicine_type__name='gel',catagory=1).prefetch_related(Prefetch('item',queryset=varient.objects.all()))
#     context={'item_list':product ,'item':'gel'}
#     return render(request,'shop.html',context)

def high(request,item):
    cate=Medicine_type.objects.filter(medicine_type=None).prefetch_related(Prefetch('subcate',queryset=Medicine_type.objects.all()))

    if item=='none':
        subquery = varient.objects.filter(product=OuterRef('pk')).order_by('price').values('price')[:1]
        product = Product.objects.filter(catagory=1).annotate(min_price=Subquery(subquery)).order_by('min_price')
    else:
        subquery = varient.objects.filter(product=OuterRef('pk')
        ).order_by('price').values('price')[:1]
        product = Product.objects.filter(medicine_type__name=item, catagory=1).annotate(
        min_price=Subquery(subquery)
        ).order_by('min_price')
    context={'item_list':product ,'item':item,'category':cate,}
    return render(request,'shop.html',context)
def low(request,item):
    cate=Medicine_type.objects.filter(medicine_type=None).prefetch_related(Prefetch('subcate',queryset=Medicine_type.objects.all()))
    if item=='none':
        subquery = varient.objects.filter(product=OuterRef('pk')).order_by('price').values('price')[:1]
        product = Product.objects.filter(catagory=1).annotate(min_price=Subquery(subquery)).order_by('-min_price')
    else:    
        first_variant_subquery = varient.objects.filter(product=OuterRef('pk')).order_by('price').values('price')[:1]
        product = Product.objects.filter(medicine_type__name=item , catagory=1).annotate(max_price=Subquery(first_variant_subquery)).order_by('-max_price')
    
    context={'item_list':product ,'item':item,'category':cate}
    return render(request,'shop.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True) 
def product_page(request,id):
    product=Product.objects.filter(id=id).prefetch_related(Prefetch('item',queryset=varient.objects.all()))
    print(product)
    context={'product':product}
    return render(request,'product-details.html',context)


  
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    response = HttpResponse('login success.')
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
        if request.user.is_patient:
            person=patientProfile.objects.get(user_id=request.user.id)
            if person.email_verify is False:
                         user=request.user
                         email_otp(user)
                         return redirect('home:verify_email') 
                    
                    
            elif person.is_verify is False:
                         user=request.user  
                         send_otp(user)
                         return redirect('home:verify_otp')
                    
                    
                         
            else:     
                       if request.user.block is False:
                            return redirect('patient:Pat_dashboard')

                       messages.error(request,'User is block by admin') 
                       return redirect('home:signin')
            # if request.user.block is False:
            #     return redirect('patient:Pat_dashboard')

            # messages.error(request,'User is block by admin') 
            # return redirect('home:signin')

        if request.user.is_docter:
            if request.user.block is False:
                return redirect('docter:doc_dashboard')
        
            messages.error(request,'User is block by admin')
            return redirect('home:signin')



    
    else:    
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            # remember=request.POST.get('remember')
            if username == '' and password == '':
                    messages.error(request, "Username and password can't be blank")
                    return redirect('home:signin')
    
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, 'No such user Please check Furthor more')
                return render(request, 'login.html')
            if user is not None:
                
                if user.is_superuser:
                    login(request, user)    
                    return redirect('dashboard')
                
                if user.is_patient:
                    person=patientProfile.objects.get(user_id=user.id)
                  
                    if  person.email_verify is False:
                         user_id=user.id
                         email_otp(user_id)
                         return redirect('home:verify_email',user_id) 
                    
                    
                    # elif person.is_verify is False:
                    #      user=user  
                    #      send_otp(user)
                    #      return redirect('home:verify_otp')
                    
                    
                         
                    else:
                       login(request, user)    
                       if request.user.block is False:
                            return redirect('patient:Pat_dashboard')

                       messages.error(request,'User is block by admin') 
                       return redirect('home:signin')

                if user.is_docter:
                    person=DoctorProfile.objects.get(user_id=user.id)
                  
                    if  person.email_verify is False:
                         user_id=user.id
                         email_otp(user_id)
                         return redirect('home:verify_email',user_id) 
                    else:
                        if user.block is False:
                            login(request, user)  
                            return redirect('docter:doc_dashboard')
                    
                        messages.error(request,'User is block by admin') 
                        return redirect('home:signin')


            else:
                
                messages.error(request, 'Wrong username or password')
                return render(request, 'login.html')
        else:
            return render(request, 'login.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def lout(request):
    logout(request)
    return redirect('home:signin')


def verification(request):
    user=request.user
    send_otp(user)
    return redirect('home:verify_otp')

def email_otp(user):
        try:  
            otp= str(random.randint(100000, 999999))
            Person=User.objects.get(id=user)
            Person.f_passw=otp
            Person.save()
            message= f'Your OTP : {otp}'
            subject= 'Email Verification'
            sender= settings.EMAIL_HOST_USER
            recipient_email= Person.email
            send_mail(subject, message, sender, [recipient_email])
            return True
        except:
            print('emil not')
            return False

def verify_email(request,id):
        if request.method == 'POST':
            otp_1 = request.POST.get('first')
            otp_2 = request.POST.get('second')
            otp_3 = request.POST.get('third')
            otp_4 = request.POST.get('fourth')
            otp_5 = request.POST.get('fifth')
            otp_6 = request.POST.get('sixth')
            
            otp_list=[otp_1,otp_2,otp_3,otp_4,otp_5,otp_6]
            otp_token=0
            
            for i in otp_list:
               if otp_token == 0:
                   otp_token+=int(i)
               else:   
                   otp_token=otp_token*10+int(i)

            id=int(id)

            if otp_token:    
                otp = User.objects.get(id=id)
                ot=otp.f_passw
                if otp_token == int(otp.f_passw):
                    try:
                        if otp.is_patient:
                            person=patientProfile.objects.get(user_id=id)
                        if otp.is_docter:
                            person=DoctorProfile.objects.get(user_id=id)
                            
                        person.email_verify=True
                        person.save()
                        messages.success(request,'Email is verified')
                        return redirect('home:signin')
                                    
                    except:
                        print("else")
                        messages.success(request,'Profile is not Verified some thing went wrong')
                        return redirect('home:signin')
                else:
                    print("else2")
                    messages.error(request,'your enter no such user')
                    return redirect('home:signin')
            else:
                print("else3")
                messages.error(request,'no OTP included')
                return redirect('home:signin')    

        else:
            return render(request, 'email_verify.html',{'id':id})              


def send_otp(user):
            otp_token = str(random.randint(100000, 999999))
            Person=User.objects.get(id=user.id)
            if Person.is_patient:
                    customer=patientProfile.objects.get(user=user)

            if Person.is_docter:
                    customer=DoctorProfile.objects.get(user=user)
            Person.f_passw=otp_token
            Person.save()
           
            client = Client(settings.ACCOUNT_SID , settings.AUTH_TOKEN)
            message = client.messages.create(
                body=f'Your OTP code is: {otp_token}',
                from_='+12056108526',  
                to=customer.contact_number,  
            )

      
def verify_otp(request):
        if request.method == 'POST':
            otp_1 = request.POST.get('first')
            otp_2 = request.POST.get('second')
            otp_3 = request.POST.get('third')
            otp_4 = request.POST.get('fourth')
            otp_5 = request.POST.get('fifth')
            otp_6 = request.POST.get('sixth')
            
            otp_list=[otp_1,otp_2,otp_3,otp_4,otp_5,otp_6]
            otp_token=0
            
            for i in otp_list:
               if otp_token == 0:
                   otp_token+=int(i)
               else:   
                   otp_token=otp_token*10+int(i)

            if otp_token:    
                otp = User.objects.get(id=request.user.id)
                print(otp.f_passw)
                print(otp_token)
                if otp_token == int(otp.f_passw):
                    try:
                        if otp.is_patient:
                            person=patientProfile.objects.get(user=request.user)

                        if otp.is_docter:
                            person=DoctorProfile.objects.get(user=request.user)

                        person.is_verify=True
                        person.save()
                        messages.success(request,'Profile is verified')
                        return redirect('home:signin')
                    except:
                        messages.success(request,'Profile is not Verified some thing went wrong')
                        return redirect('home:signin')
                else:
                    messages.error(request,'no user')
                    return redirect('home:signin')
            else:
                messages.error(request,'no OTP included')
                return redirect('home:signin')    
        else:
            return render(request, 'verify_otp.html')
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')
def cart(request):
    cart_itm=CartItem.objects.filter(cart__user=request.user)
    context={'cart_itm':cart_itm}
    return render(request,'shop-cart.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')
def decr(request,id):
    item=CartItem.objects.get(id=id)
    if  item.quantity >1:
        item.quantity=item.quantity-1
        item.save()

    return redirect('home:cart')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')
def incr(request,id):
    item=CartItem.objects.get(id=id)
    item.quantity=item.quantity+1
    item.save()
    return redirect('home:cart')
    
def delet_cartItem(request,id):
    item=CartItem.objects.get(id=id)
    item.delete()
    return redirect('home:cart')




def add_cart(request,id):
    if request.method=='POST':
        price=request.POST.get('price')
        qty=request.POST.get('qty')
        action=request.POST.get('action')
        size=request.POST.get('item')
        prod=Product.objects.get(id=id)
        varnt=varient.objects.get(id=size)
        if action == 'cart':
                if varnt.stock>0:
                    try:
                        cat=Cart.objects.get(user_id=request.user.id)
                        crt=CartItem.objects.create(cart=cat)
                        crt.product=prod
                        crt.price=price
                        crt.quantity=qty
                        crt.Varient=varnt
                        crt.save()
                        messages.success(request,'Your item is added to cart')
                        return redirect('home:item')
                    except:
                        messages.error(request,'Your are not autherised')
                        return redirect('home:item')


                else:
                    messages.error(request,'Your item is out of stock')
                    return redirect('home:item')
                 
                 
        elif action == 'buy':  
            try:
                cat=Cart.objects.get(user_id=request.user.id)
                crt=CartItem.objects.create(cart=cat)
                crt.product=prod
                crt.price=price
                crt.quantity=qty
                crt.Varient=varnt
                crt.save() 
                adress=Address.objects.filter(Patient__user__id=request.user.id)
                cart_itm=CartItem.objects.filter(id=crt.id)
                context={'cart_itm':cart_itm,'adress':adress,'item':crt.id}
                return render(request,'checkout.html',context)
            except:
                messages.error(request,'Your are not autherised')
                return redirect('home:item')

        else:
            messages.error(request,'Your are form submitting is wrong ! try againe')
            return redirect('home:product_page',id)

    else:
        return redirect('home:product_page',id)


def checkout(request):
    adress=Address.objects.filter(Patient__user__id=request.user.id)
    cart_itm=CartItem.objects.filter(cart__user=request.user)
    walt=wallet.objects.get(PatientProfile__user__id=request.user.id) 
    context={'cart_itm':cart_itm,'adress':adress,'item':1,'walt':walt.amount}
    return render(request,'checkout.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')
def order(request,item):
    if request.method == 'POST':
        address=request.POST.get('address')
        pay=request.POST.get('payment')
        if address =='':
            messages.error(request,'adrees must be selected')
            return redirect('home:checkout')
        if item !=1:
            cart_itm=CartItem.objects.filter(id=item)
        else:
            cart_itm=CartItem.objects.filter(cart__user=request.user)           
        ord=Order(user_id=request.user.id)
        ord.save()
        s=0
        for i in cart_itm:
            s+=i.price*i.quantity
            sum=i.price*i.quantity
            items=orderItem(order=ord,price=sum,quantity=i.quantity,product=i.product,Varient=i.Varient)
            items.save()
        

        if request.session.has_key('coupen'):
            id=int(request.session['coupen'])
            cp=coupen.objects.get(id=id)
            s=s-cp.discount_price
            ord.discount=cp
               
        ord.Total_Price=s
        ord.address_id=address
        ord.Pay_option=pay
        ord.save()

        for i in cart_itm:
            subject=varient.objects.get(id=i.Varient_id)
            subject.stock=int(subject.stock)- int(i.quantity)
            subject.save()

        if pay=='online':     
            raz_client=razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_SECRET_KEY))
            payment=raz_client.order.create({'amount': int(s)*100, 'currency': 'INR', 'payment_capture': '1'})
            print(payment)
            ord.razor_orderid=payment['id']
            ord.save()
            if request.session.has_key('coupen'):
                del request.session['coupen'] 
            context={'payment':payment,'order':ord}
            return render(request,'Payments.html',context)
        
        elif pay=='wallet':
            try:
               walt=wallet.objects.get(PatientProfile__user__id=request.user.id) 
            except:
                cart_itm.delete()
                if request.session.has_key('coupen'):
                     del request.session['coupen']
                messages.success(request, f'You order #{ord.id} is placed but cash on delivery method Processed')
                return redirect('home:item')    
            
            walt.amount=walt.amount-ord.Total_Price
            walt.save() 
            cart_itm.delete()
            if request.session.has_key('coupen'):
                del request.session['coupen']   
            messages.success(request, " Your  item is ordered successfully")
            return redirect('home:item')
        else:
            cart_itm.delete()
            if request.session.has_key('coupen'):
                 del request.session['coupen']   
            messages.success(request, " Your  item is ordered successfully")
            return redirect('home:item')
    else:
        return redirect('home:checkout')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')
def payment_cancel(request,id):
    order=Order.objects.get(id=id)
    items=orderItem.objects.filter(order_id=order.id)
    for i in items:
        subject=varient.objects.get(id=i.Varient_id)
        subject.stock=int(subject.stock) + int(i.quantity)
        subject.save()    

    order.delete()
    messages.success(request, " Your  order item is canceled")
    return redirect('home:item')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def success(request):
    id=request.GET.get('razororder')
    try:
       try:
           cart_itm=CartItem.objects.filter(cart__user=request.user)
       except:
           cart_itm=None

       cart_itm.delete()        
       ord=Order.objects.get(razor_orderid=id)
       if ord:
            messages.success(request,'Your order Successfully placed')
            return redirect('home:item')
    except:
        messages.error(request,'Your order is canceled try againe')
        return redirect('home:item') 
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')
def coup(request):
    if request.method=='POST':
        coupon=request.POST.get('coupon')
        today=datetime.now().date()
        try:
            try:
               a=coupen.objects.get(name=coupon)
            except:
                messages.error(request,'Coupon Does not Exixts')
                return redirect('home:checkout') 
            cp=Order.objects.filter(discount_id=a.id,user=request.user)
            print('hii')
            if cp:
                messages.error(request,'Your Coupon is already used ! Try another one')
                return redirect('home:checkout')
            
            else:
                id=a.id

                if a.expairy_date<today:
                    messages.error(request,'Your Coupon is expaired ! Try another one')
                    return redirect('home:checkout')
                if a:
                    request.session['coupen']=id            
                    messages.success(request,'coupon added')
                    return redirect('home:checkout')
        except:
            print('else')
            return redirect('home:checkout')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')        
def delete_session(request,id):
    if request.session.has_key('coupen'):
        del request.session['coupen']
        messages.error(request,'coupen deleted') 
        return redirect('home:checkout')

    else:
        return redirect('home:checkout')
        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')
def adres(request):
    if request.method =='POST':
        name=request.POST.get('name')
        address=request.POST.get('address')
        country=request.POST.get('country')
        city=request.POST.get('city')
        district=request.POST.get('district')
        state=request.POST.get('state')
        code=request.POST.get('code')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        if name =='' and address =='' and country =='' and city=='' and district =='' and  code =='' and phone=='' and email=='':
            messages.error(request,"Field can't be blank")
            return render(request,'adress.html')
        usr=patientProfile.objects.get(user__id=request.user.id) 
        if usr:
            addres=Address(Patient=usr,Name=name,address=address,country=country,city=city,district=district,state=state,Pin_code=code,contact=phone,email=email)
            addres.save()
            adress=Address.objects.filter(Patient__user__id=request.user.id)
            cart_itm=CartItem.objects.filter(cart__user=request.user)
            context={'cart_itm':cart_itm,'adress':adress,'item':1}
            messages.success(request, "Your Address is added successfully")
            return render(request,'checkout.html',context)
        else:
            messages.error(request, "Your Profile is not completed")
            return redirect('home:checkout')
    else:
        return render(request,'adress.html')
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')
def edit_address(request,id):
    if request.method =='POST':
        name=request.POST.get('name')
        address=request.POST.get('address')
        country=request.POST.get('country')
        city=request.POST.get('city')
        district=request.POST.get('district')
        state=request.POST.get('state')
        code=request.POST.get('code')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        if name =='' and address =='' and country =='' and city=='' and district =='' and  code =='' and phone=='' and email=='':
            messages.error(request,"Field can't be blank")
            return redirect('edit_address',id) 
        usr=Address.objects.get(id=id)
        if usr:
            usr.Name=name
            usr.address=address
            usr.country=country
            usr.city=city
            usr.district=district
            usr.state=state
            usr.Pin_code=code
            usr.contact=phone
            usr.email=email
            usr.save()
            adress=Address.objects.filter(Patient__user__id=request.user.id)
            cart_itm=CartItem.objects.filter(cart__user=request.user)
            context={'cart_itm':cart_itm,'adress':adress,'item':1}
            messages.success(request, "Your Address is edited successfully")
            return render(request,'checkout.html',context)
        else:
            messages.error(request, "Your Profile is not completed")
            return redirect('home:checkout')
    else:
        instance=Address.objects.get(id=id)
        context={'instance':instance,'id':id}
        return render(request,'edit_address.html',context)
        
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')
def delete_address(request):
    if request.method=='POST':
        id=request.POST['dele']
        usr=Address.objects.get(id=int(id))
        if usr:
          usr.delete()
          return redirect("home:checkout")
        
            
def changeP(request,token):
    token=token
    user=User.objects.filter(f_passw=token).first()

    if request.method == 'POST':
        passw=request.POST.get('passw')
        con_passw=request.POST.get('con_passw')
        
        if passw =='' and con_passw == '':
            messages.error(request,'its not valid')
            return redirect('home:changeP')

        if passw != con_passw:
            messages.error(request,'Password should be equal')
            return redirect('home:changeP')
        
        try:
            validate_password(passw)

        except ValidationError as e:
            messages.error(request, e)
            return redirect('home:signin')


        if user:
            user.set_password(passw)
            user.save()
            print(user.password)
            messages.success(request,'Password is change')
            return redirect('home:signin')


    else:
        context={'user':id,'token':token}
        return render(request,'change.html',context)    
    
def forgetP(request):
    if request.method =='POST':
        print('worked')
        fP=request.POST.get('username')
        print(fP)
        user_obj=User.objects.filter(username=fP).first()
        user_obj1=User.objects.filter(username=fP)

        print(user_obj)
        print(user_obj1)

        if user_obj:
            token=str(uuid.uuid4())
            print(token)
            user_obj.f_passw=token
            user_obj.save()   
            send_forgot(user_obj.email,token)
            return redirect('home:signin')
        else:
            messages.error(request,'No such username')
            return render(request,'forgot.html')


    else:
        return render(request,'forgot.html')
        
def send_forgot(email,item):
    try:
        message='forgot password'
        subject=f'click to Password rest  http://127.0.0.1:8000/changeP/{item}'
        email_from=settings.EMAIL_HOST_USER
        recipient_list=[email]
        send_mail(message,subject,email_from,recipient_list)     
        return True
    except:
        return False


def message(request):
    return render(request,'chat.html')

def index(request):
    return render(request, "msg.html")
