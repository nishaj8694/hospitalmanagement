# Create your views here.
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render, redirect,reverse
from django.contrib.auth import logout,login
from django.views.decorators.cache import cache_control
from home.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from home.models import Cart,Order,orderItem,Refund
from home.forms import Patient_form,refund_form
from patient.models import patientProfile,wallet
from admn.models import Product,varient,coupen
from home.models import Appointment,treatment,TreatMedicine,Address
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Prefetch
from docter.models import DoctorProfile
from .forms import adrs_form,patient_form
from django.template.loader import get_template
from io import BytesIO
from django.http import HttpResponse
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch
from xhtml2pdf import pisa
import uuid
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django_otp import devices_for_user
# from django_otp.plugins.otp_totp.models import TOTPDevice
from twilio.rest import Client
import random
import razorpay
from django.conf import settings
from home.templatetags.filt import discount,totalprice


# import sweetify
# from django.utils.datastructures import MultiValueDictKeyError


@login_required(login_url='home:signin')
def exam(request):
    return render(request,'invoice.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Pat_signup(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('dashboard')
        if request.user.is_patient:
            person=patientProfile.objects.get(user=request.user)
            if person:
                print("your are in person")
            if person.is_verify is None:
                print("person")
                

            

            if request.user.block is None:
                return redirect('patient:Pat_dashboard')
            
            messages.error(request,'User is block by admin') 
            return redirect('signin')
        
        messages.error(request,'User is block by admin') 
        return redirect('signin')

    if request.method == 'POST':
        fullname = request.POST['name']
        username = request.POST['username']
        email=request.POST['email']
        number = request.POST['number']
        password = request.POST['password']
        comf_password = request.POST['comf-password']

        if fullname == '' and username == '' and password == '' and email =='' and number =='':
            messages.error(request, "Fields can't be blank")
            return redirect('patient:Pat_signup')

        if password != comf_password:
            messages.error(request, "Password dosen't match")
            return redirect('patient:Pat_signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('patient:Pat_signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Requested email already exists')
            return redirect('patient:Pat_signup')

        try:
            validate_password(password)

        except ValidationError as e:
            messages.error(request, e)
            return redirect('patient:Pat_signup')
        
        user = User.objects.create_user(username=username, password=password)
        user.first_name = fullname
        user.is_patient=True
        user.email=email
        crt=Cart.objects.create(user=user)
        profile=patientProfile.objects.create(user=user)
        walt=wallet.objects.create(PatientProfile=profile)
        walt.amount=0
        walt.save()
        if len(number)>10:
            profile.contact_number='+91'+number
        else:
            profile.contact_number=number

        profile.save()
        crt.save()
        user.save()

        messages.success(request, 'User created successfully')
        return redirect('home:signin')

    return render(request, 'new-user.html')
      
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def appoiment(request,id):
    id=id
    if request.method=='POST':
        time=request.POST.get('time')
        print('this is time ',time)
        form=Patient_form(request.POST)
        if form.is_valid():
            user=Appointment.objects.filter(appointment_time=time, appointment_date=form.instance.appointment_date)
            if user:
                messages.error(request,"take another time or date")
                return redirect('patient:appoiment',id)
            pat=patientProfile.objects.get(user=request.user)
            if pat:
                 form.save()
                 person=Appointment.objects.get(id=form.instance.id)
                 person.patient_id=pat.id
                 person.appointment_time=time
                 person.save()
                #  messages.success(request,"success")
                 messages.success(request,f'You Appointment for dr {person.docter.user} is made at {person.appointment_time}')
                 return redirect('patient:appoiment',id)

            messages.error(request,"Profile not verified")    
            return redirect('patient:appoiment',id)
            
        messages.error(request,"form is invaled")        
        return redirect('patient:appoiment',id)

    else:
        form=Patient_form()
        if id==2:
            return render(request,'new.html',{'form':form,})
        if id==1:
            return render(request,'new_Pat.html',{'form':form,'page':"book"})

def get_available_time_slots(request):
    if request.method == 'GET':
        selected_date = request.GET.get('date')
        doc=request.GET.get('doctor')
        print('hallo',doc)
        docte=Appointment.objects.filter(docter_id=doc).distinct('docter').values('docter')
        doc1=DoctorProfile.objects.get(id=int(doc))
        start = doc1.consult_start
        end = doc1.consult_end
        print(start,end)
        start_minutes = start.hour * 60 + start.minute
        end_minutes = end.hour * 60 + end.minute
        dif_time=end_minutes-start_minutes
        time_slot_interval = 30 
        total_time_slots=dif_time//time_slot_interval
        # total_slots = int(time_diff.total_seconds() / (time_slot_interval * 60))
        # start_time = datetime(2023, 4, 18, 14, 0) 
        # end_time = datetime(2023, 4, 18, 20, 0)  
        # total_time_slots = int((end_time - start_time).seconds / (time_slot_interval * 60))
        # print(total_time_slots)
        current_date = datetime.now().date()
        star = datetime.combine(current_date, datetime.min.time()) + timedelta(hours=doc1.consult_start.hour, minutes=doc1.consult_start.minute)
        print(star)
        if datetime.now() > star + timedelta(minutes=dif_time):
            star += timedelta(days=1)
        available_time_slots = []
        for i in range(total_time_slots):
            time_slot = star + timedelta(minutes=i * time_slot_interval)
            print(time_slot)
            if not Appointment.objects.filter(docter_id=doc,appointment_date=selected_date, appointment_time=time_slot).exists():
                available_time_slots.append(time_slot.strftime("%H:%M")) 
                
        data = {
            'time_slots': available_time_slots
        }
        return JsonResponse(data)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')
def Patient_appointment(request):
    try:
        Patient=patientProfile.objects.get(user=request.user.id)
        print(Patient.id)
        Patient_list=Appointment.objects.filter(patient_id=Patient.id)
        context={'Appointment':Patient_list,'page':"appoiment"}
        return render(request,'Patient_appointment.html',context)
    except:
        return render(request,'Patient_appointment.html')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')
def copn(request,id):
    if request.method=='POST':
        coupon=request.POST.get('coupon')
        today=datetime.now().date()
        if request.session.has_key('coupen'):
            del request.session['coupen']
            return redirect('patient:check',id)
        try:
            try:
               a=coupen.objects.get(name=coupon)
            except:
                messages.error(request,'Coupon Does not Exixts')
                return redirect('patient:check',id) 
            cp=Order.objects.filter(discount_id=a.id,user=request.user)
            print('hii')
            if cp:
                messages.error(request,'Your Coupon is already used ! Try another one')
                return redirect('patient:check',id)
            
            else:
                item=a.id

                if a.expairy_date<today:
                    messages.error(request,'Your Coupon is expaired ! Try another one')
                    return redirect('patient:check',id)
                if a:
                    request.session['coupen']=item            
                    messages.success(request,'coupon added')
                    return redirect('patient:check',id)
        except:
            print('else')
            return redirect('home:check',id)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))
def treat(request):
    Patient_list=Appointment.objects.filter(patient__user_id=request.user.id)
    list=treatment.objects.prefetch_related(Prefetch('treat',queryset=TreatMedicine.objects.all())).filter(appointment__patient__user=request.user)
    return render(request,'prescrption.html',{'list':list,'page':"med"})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Pat_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_patient:
              user=patientProfile.objects.get(user_id=request.user.id)
              wal=wallet.objects.get(PatientProfile=user)

              context={'prof':user,'page':'dashboard','wallet':wal}
              return render(request,'user-admin.html',context )    
        
        return redirect('signin')      
       
    return redirect('signin')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))
def p_profile(request):
    if request.method=='POST':
        form=patient_form(request.POST,request.FILES)
        if form.is_valid():
            Person=patientProfile.objects.get(user_id=request.user.id)
            if len(form.instance.contact_number)>10:
                Person.contact_number=form.instance.contact_number
            else:
                Person.contact_number='+91'+form.instance.contact_number
                
            Person.gender=form.instance.gender
            Person.image=form.instance.image
            Person.save()
            messages.success(request,'Profile is updated')
            return redirect('home:signin') 
        else:
            messages.error(request,'something went wrong')
            return redirect('patient:p_profile')
    else:
        try:
            Person=patientProfile.objects.get(user_id=request.user.id)
            print(Person)
            form=patient_form(instance=Person)
            if Person.contact_number:
               return render(request,'Patient_Profile.html',{'form':form})
            else:
               return render(request,'Patient_Profileverify.html',{'form':form})
        except:
            messages.error(request,'no user is found')
            return render(request,'Patient_Profile.html',{'form':form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))
def check(request,id):
    print('hii')
    list=TreatMedicine.objects.filter(Treatment_id=id)
    sum=0
    for i in list:
        sum+=i.medicine.price*i.quantity 
    # test=list.medicine
    # print(list.medicine_id)
    # print(list.quantity) 
    walt=wallet.objects.get(PatientProfile__user__id=request.user.id) 
    print(walt.amount)         
    adress=Address.objects.filter(Patient__user__id=request.user.id)
    context={'list':list,'adress':adress,'money':sum,'id':id ,'walt':walt.amount}
    return render(request,'check.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))
def delete_coupen(request,id):
    if request.session.has_key('coupen'):
        del request.session['coupen'] 
        return redirect('patient:check',id)
    else:
        return redirect('patient:check',id)
     
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))
def d_order(request,id):     
    if request.method =='POST':
        address=request.POST.get('address')
        pay=request.POST.get('payment')
        if address =='':
            messages.error(request,'adrees must be selected')
            return redirect('patient:check',id)

        ord=Order(user_id=request.user.id)
        ord.save()
        list=TreatMedicine.objects.filter(Treatment_id=id)
        sum=0
        for i in list:
            s=0
            sum+=i.medicine.price*i.quantity 
            s=i.medicine.price*i.quantity
            items=orderItem(order=ord,price=s,quantity=i.quantity,product=i.medicine.product,Varient=i.medicine)
            items.save()
            subject=varient.objects.get(id=i.medicine_id)
            subject.stock=int(subject.stock)- int(i.quantity)
            subject.save()
        
        if request.session.has_key('coupen'):
            id=int(request.session['coupen'])
            cp=coupen.objects.get(id=id)
            sum=sum-cp.discount_price
            ord.discount=cp


        
        ord.Total_Price=sum
        ord.address_id=address
        ord.Pay_option=pay
        ord.save()
        trt=treatment.objects.get(id=id)
        trt.ordstatus=True
        trt.save()
        

        if pay=='online':
            raz_client=razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_SECRET_KEY))
            payment=raz_client.order.create({'amount': int(s)*100, 'currency': 'INR', 'payment_capture': '1'})  
            ord.razor_orderid=payment['id']
            ord.save()
            context={'payment':payment,'order':ord,'treat':trt.id}
            return render(request,'Pay.html',context)
        elif pay=='wallet':
            try:          
                walt=wallet.objects.get(PatientProfile__user__id=request.user.id) 
            except:
                messages.success(request, f'you order #{ord.id} is placed but cash on delivery method Processed')
                return redirect('patient:treatment')
            
            walt.amount=walt.amount-ord.Total_Price
            walt.save()
            messages.success(request, f'you order #{ord.id} is placed successfully')
            return redirect('patient:treatment') 
        else:             
            messages.success(request, f'you order #{ord.id} is placed successfully')
            return redirect('patient:treatment')
    else:
        return redirect('patient:check',id)
            
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))
def ord_success(request):
    id=request.GET.get('razororder')
    try:
       ord=Order.objects.get(razor_orderid=id)
       if ord:
            messages.success(request,'Your order Successfully placed')
            return redirect('patient:Pat_dashboard')
    except:
        messages.error(request,'Your order is canceled try againe')
        return redirect('patient:Pat_dashboard')
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))    
def pay_cancel(request,id,item):
    order=Order.objects.get(id=id)
    items=orderItem.objects.filter(order_id=order.id)
    for i in items:
        subject=varient.objects.get(id=i.Varient_id)
        subject.stock=int(subject.stock) + int(i.quantity)
        subject.save()    
    treat=treatment.objects.get(id=item)
    if treat:
        treat.ordstatus=False
        treat.save()
    order.delete()
    messages.success(request, " Your  order item is canceled")
    return redirect('patient:Pat_dashboard')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))
def pat_chat(request):
    Patient_list=Appointment.objects.filter(patient__user_id=request.user.id,status='finish').distinct('docter')    
    return render(request,'pat_chat.html',{'pat':Patient_list,'page':'chat'})




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))
def adres(request,id):
    if request.method=='POST':
        form=adrs_form(request.POST)
        if form.is_valid():
            form.save() 
            usr=patientProfile.objects.get(user__id=request.user.id) 
            if usr:
                adress=Address.objects.get(id=form.instance.id)
                print('address',adress)
                print('user',usr)
                adress.Patient=usr
                adress.save()
                print(adress.Patient)
                return redirect('patient:check',id)
            
            else:
                form=adrs_form()
                return render(request, 'address.html',{'form':form})

    else:
        form=adrs_form()
        return render(request, 'address.html',{'form':form,'id':id})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))
def edit_adres(request,id,item):
    if request.method=='POST':
        form=adrs_form(request.POST)
        if form.is_valid(): 
            usr=patientProfile.objects.get(user__id=request.user.id) 
            if usr:
                adr=Address.objects.get(id=id)
                adr.address=form.instance.address
                adr.Name=form.instance.Name
                adr.city=form.instance.city
                adr.district=form.instance.district
                adr.state=form.instance.state
                adr.country=form.instance.country
                adr.Pin_code=form.instance.Pin_code
                adr.contact=form.instance.contact
                adr.email=form.instance.email
                adr.Patient=usr
                adr.save()
                return redirect('patient:check',item)
            
            else:
                messages.error(request,"your profile not verified")
                return render(request, 'address.html',{'form':form})

    else:
        thing=Address.objects.get(id=id)
        form=adrs_form(instance=thing)
        return render(request, 'ed_address.html',{'form':form,'id':id,'item':item})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))          
def delete_adres(request,id,item):
    thing=Address.objects.get(id=id) 
    if thing:
        thing.delete()
        return redirect('patient:check',item)
    


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))
def ord(request):
    order_list=Order.objects.prefetch_related(Prefetch('order_items',queryset=orderItem.objects.all()) ,Prefetch('order_refund',queryset=Refund.objects.all())).filter(user=request.user).exclude(status='deliverd')
    context={'order_list':order_list ,'page':'order'}
    return render(request,'myorder.html',context)

def ord_hys(request):
    stat=['deliverd','cancel']
    order_list=Order.objects.prefetch_related(Prefetch('order_items',queryset=orderItem.objects.all()) ,
            Prefetch('order_refund',queryset=Refund.objects.all())).filter(user=request.user , delivery_date__isnull=False,status__in=stat)
    context={'order_list':order_list,'page':'order'}
    return render(request,'myorder_hs.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))
def cancel_order(request):
    if request.method=='POST':
        id=request.POST.get('dele')
        try:
            order=Order.objects.get(id=int(id))
            if order.Pay_option =='cash':
                if order.status =='deliverd' or 'cancel' and order.delivery_date!=None:
                    form=refund_form()
                    return render(request,'refund.html',{'id':id,'form':form})
                
                order.status='cancel'
                order.save()
                messages.success(request,'Your order is canceled')
                return redirect('patient:ord')    

            else:     
                form=refund_form()
                return render(request,'refund.html',{'id':id,'form':form})
        except:
            messages.error(request,"order can't delete try againe")
            return redirect('patient:ord')
            
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url=('home:signin'))       
def refund(request,id):
    if request.method=='POST':
        form=refund_form(request.POST)
        if form.is_valid():
            order=Order.objects.get(id=int(id))
            try:
               adr=Refund.objects.get(order=order)
               adr.refund_option=form.instance.refund_option
               adr.refund_reason=form.instance.refund_reason
               adr.save()
            except:    
                form.save()
                adr=Refund.objects.get(id=form.instance.id)
                adr.order=order
                adr.save()

            if order.status =='deliverd' or 'cancel' and order.delivery_date!=None:
                order.status='cancel'
                order.cancel_date=datetime.now()
                order.save()
                if adr.cancelby == '':
                    adr.cancelby='user'

                adr.save()
                messages.success(request,'Your amount will be refunded within 7 days')
                return redirect('patient:ord')
            else:
                if adr.cancelby == '':
                    adr.cancelby='user'        
                adr.save()
                order.status='cancel'
                order.save()
                messages.success(request,'Your amount will be refunded within 7 days')
                return redirect('patient:ord')
    else:
            return redirect('patient:refund',id)


@login_required(login_url=('home:signin'))
def invoice(request,id):
    order=Order.objects.get(id=id)
    item=orderItem.objects.filter(order=order)
    template = get_template('invoice.html')
    context={'order':order,'item':item}
    html = template.render(context)
    # method1
    buffer = BytesIO()
    pisa.CreatePDF(BytesIO(html.encode("UTF-8")), buffer)
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(content_type='application/pdf')
    name=uuid.uuid4()
    response['Content-Disposition'] = f'attachment; filename="{name}.pdf"'
    response.write(pdf)
    return response
    

