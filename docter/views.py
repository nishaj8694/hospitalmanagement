from django.shortcuts import render,redirect,HttpResponse
from .models import DoctorProfile
from django.db.models import Prefetch
from admn.models import Product,varient
from home.models import Appointment,treatment,TreatMedicine,User
from .forms import doc_form
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta,time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Case, When, Value, IntegerField
from django.views.decorators.cache import cache_control
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages


# Create your views here.



@login_required(login_url='home:signin')
def doc_dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_docter:
            Pr_no=Product.objects.count()
            My_no=Appointment.objects.filter(docter__user_id=request.user.id , status='finish').count()
            P_no=Appointment.objects.filter( status='finish').count()
            AP_no=Appointment.objects.filter(docter__user_id=request.user.id ).count()
            
            docter=DoctorProfile.objects.get(user_id=request.user.id)
            # print(docter.image,docter.badge_id)
            if docter is None:
                print('iam in docter')
                docter=DoctorProfile(user_id=request.user.id)
                docter.save()
                docter=DoctorProfile.objects.filter(user_id=request.user.id)
                context={'docter':docter,'Pr_no':Pr_no,'My_no':My_no,'P_no':P_no,'AP_no':AP_no ,'page':'dash'}
                return render(request,'doc_home.html',context)
            
            if docter.image !=None and docter.badge_id !=None:
                print('iam home doc') 
                context={'docter':docter,'Pr_no':Pr_no,'My_no':My_no,'P_no':P_no,'AP_no':AP_no,'page':'dash'}
                return render(request,'doc_home.html',context)
            
            if docter.image == None or docter.badge_id == None:
                print('iam home doc') 
                context={'docter':docter,'Pr_no':Pr_no,'My_no':My_no,'P_no':P_no,'AP_no':AP_no,'page':'dash'}
                return render(request,'doc_home.html',context)
            
            context={'docter':docter,'Pr_no':Pr_no,'My_no':My_no,'P_no':P_no,'AP_no':AP_no,'page':'dash'}
            return render(request,'doc.html',context)
             
        return redirect('signin')      
       
    return redirect('signin')      

@login_required(login_url='home:signin')
def exam(request):
    return render(request,'HospitalDocter.html')

@login_required(login_url='home:signin')
def doc_profile(request):
    if request.method=='POST':
        form=doc_form(request.POST , request.FILES)
        # print('halo')
        if form.is_valid():
            # print('halo')
            docter=DoctorProfile.objects.get(user_id=request.user.id)
            if docter:
                docter.specialization=form.instance.specialization
                docter.gender=form.instance.gender
                docter.image=form.instance.image
                docter.department=form.instance.department
                docter.address=form.instance.address
                docter.residence=form.instance.residence
                docter.contact_number='+91'+form.instance.contact_number
                docter.badge_id=form.instance.badge_id
                docter.save()
                return redirect('docter:doc_dashboard')
            else:
                return redirect('docter:doc_dashboard')
        else:
            print('else woe')    
            return redirect('docter:doc_dashboard')    
          

    else:
        docter=DoctorProfile.objects.get(user_id=request.user.id)
        form=doc_form()
        return render(request,'doc_profile.html',{'form':form,'docter':docter,'page':'dash'})

@login_required(login_url='home:signin')
def doc_edit_profile(request):
    if request.method=='POST':
        form=doc_form(request.POST , request.FILES)
        # print('halo')
        if form.is_valid():
            # print('halo')
            try:
                docter=DoctorProfile.objects.get(user_id=request.user.id)
            except:               
               return render(request,'doc_home.html')
                     
            if docter:
                docter.specialization=form.instance.specialization
                docter.gender=form.instance.gender
                docter.image=form.instance.image
                docter.department=form.instance.department
                docter.address=form.instance.address
                docter.residence=form.instance.residence
                docter.contact=form.instance.contact
                docter.badge_id=form.instance.badge_id
                docter.save()
                return redirect('docter:doc_dashboard')
                
        else:
            return redirect('docter:doc_dashboard')
            

    else:
        profile=DoctorProfile.objects.get(user_id=request.user.id)
        form=doc_form(instance=profile)
        return render(request,'doc_profile.html',{'form':form,'docter':profile,'page':'dash'})    
    
@login_required(login_url='home:signin')
def doc_Product(request):
      
      product=Product.objects.prefetch_related(Prefetch('item',queryset=varient.objects.all()))
      docter=DoctorProfile.objects.get(user_id=request.user.id)
      print(docter)
      context={'product':product,'docter':docter,'page':'medicine'} 
      return render(request,'doc_Product.html',context)


def doc_time_options():
    times = []
    for hour in range(0, 24):
        for minute in range(0, 60, 15):  
            time_obj = time(hour, minute)
            time_str = time_obj.strftime('%H:%M')
            times.append((time_str, time_str))
    return times



@login_required(login_url='home:signin')
def doc_appointment(request):
    today=datetime.now().date()
    doct=DoctorProfile.objects.get(user=request.user)
    print(doct.id)
    Patient_list=Appointment.objects.filter(docter_id=doct.id).order_by(
        Case(
        When(appointment_date__gt=today, then=Value(2)),
        When(appointment_date=today, then=Value(1)),
        default=Value(3),
        output_field=IntegerField(),
    ),
    Case(
        When(status='pending', then=Value(1)),
        When(status='accept', then=Value(2)),
        When(status='reject', then=Value(3)),
        When(status='finish', then=Value(4)),
        default=Value(5),
        output_field=IntegerField(),
    ),
        'appointment_date')
    print(Patient_list)
    docter=DoctorProfile.objects.get(user_id=request.user.id)
    context={'Appointment':Patient_list,'docter':docter,'page':'appoiment'}
    return render(request,'doc_appointment.html',context)

@login_required(login_url='home:signin')
def changeTime(request):
    if request.method == 'POST':
        start=request.POST.get('start_time')
        end=request.POST.get('end_time')
        start_time = datetime.strptime(start, "%H:%M").time()
        end_time = datetime.strptime(end, "%H:%M").time()
        doc = DoctorProfile.objects.get(user=request.user)
        doc.consult_start = start_time
        doc.consult_end = end_time
        doc.save()
        return redirect('docter:doc_appointment')
    else:
        docter = DoctorProfile.objects.get(user=request.user)
        time_options =doc_time_options()
        context={'docter':docter,'start':time_options,'end':time_options,'page':'time'}
        return render(request,'doc_time.html',context)
        
@login_required(login_url='home:signin')
@csrf_exempt
def update_is_available(request):
    if request.method=='POST':
        id=request.POST.get('item_id')
        is_available=request.POST.get('is_available')
        docter=DoctorProfile.objects.get(id=id)
        print(is_available)
        if is_available =='true':
            print("true")
            docter.is_available = True
            docter.save()
        else:
            print("false")
            docter.is_available = False
            docter.save()    
        return JsonResponse({'is_available': docter.is_available})
    
    else:
        return JsonResponse({'error': 'Invalid request method.'})



@login_required(login_url='home:signin')
def today_appointment(request):
    today=datetime.now().date()
    doct=DoctorProfile.objects.get(user=request.user)
    Patient_list=Appointment.objects.filter(docter_id=doct.id,appointment_date=today).order_by('appointment_time')
    docter=DoctorProfile.objects.filter(user_id=request.user.id)
    context={'Appointment':Patient_list,'docter':doct,'today':today,'page':'appoiment'}
    return render(request,'doc_appointment.html',context)


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')
def appointment_status(request,id,keyword):
    print(keyword)
    try:
       appoiment=Appointment.objects.get(id=id)
       if appoiment.status != 'finish':
            if keyword == 'finish':
                id=appoiment.id
                return redirect('docter:prescribe',id)
            appoiment.status=keyword
            appoiment.save() 
            return redirect('docter:doc_appointment')
       return redirect('docter:doc_appointment')
    except:
       return redirect('docter:doc_appointment')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')    
def prescribe(request,id):
    id=id
    if request.method=='POST':
        symtems= request.POST['symtems']
        selected_items = request.POST.getlist('selected_items[]')
        quantity = request.POST.getlist('quantities[]')
        tret = treatment(appointment_id=id, symtems=symtems)
        tret.save()
        for i in range(len(selected_items)):
            med=TreatMedicine(Treatment=tret,medicine_id=int(selected_items[i]),quantity=int(quantity[i]))
            med.save()
        appoiment=Appointment.objects.get(id=id)
        appoiment.status='finish'
        appoiment.save()
        product=Product.objects.prefetch_related(Prefetch('item',queryset=varient.objects.all()))
        context={'medicines':varient.objects.all(),'product':product,'id':id ,'page':'appoiment'}
        return render(request,'prescribe.html',context)
    else:
        product=Product.objects.prefetch_related(Prefetch('item',queryset=varient.objects.all()))
        docter=DoctorProfile.objects.get(user_id=request.user.id)
        context={'medicines':varient.objects.all(),'product':product,'id':id ,'docter':docter,'page':'appoiment'}
        return render(request,'prescribe.html',context)
    
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)    
# @login_required(login_url='home:signin')    
# def pre2(request,id):
#      list=TreatMedicine.objects.filter(Treatment_id=id)
#      docter=DoctorProfile.objects.get(user_id=request.user.id)
#      return render(request,'prescb2.html',{'list':list,'docter':docter,'page':'appoiment'})


@login_required(login_url='home:signin')    
def myPatient(request):
    docter=DoctorProfile.objects.get(user_id=request.user.id)
    Patients=Appointment.objects.filter(docter__user_id=request.user.id , status='finish')
    context={'Patients':Patients,'docter':docter,'page':'Patient'}
    return render(request,'myPatient.html',context)


@login_required(login_url='home:signin')    
def today_Patient(request):
    today=datetime.now().date()
    docter=DoctorProfile.objects.get(user_id=request.user.id)
    Patients=Appointment.objects.filter(docter__user_id=request.user.id , status='finish',appointment_date=today)
    context={'Patients':Patients,'docter':docter,'today':today,'page':'Patient'}
    return render(request,'myPatient.html',context)


@login_required(login_url='home:signin')    
def doc_chat(request):
    Patient_list=Appointment.objects.filter(docter__user_id=request.user.id,status='finish').distinct('patient')
    return render(request,'doc_chat.html',{'pat':Patient_list,'page':'chat'})



# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required(login_url='home:signin')    
# def decr(request,id):
#     item=TreatMedicine.objects.get(id=id)
#     if  item.quantity >1:
#         item.quantity=item.quantity-1
#         item.save()
#     tem=item.Treatment_id    
#     return redirect('docter:pre2',tem)


# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
# @login_required(login_url='home:signin')    
# def incr(request,id):
#     item=TreatMedicine.objects.get(id=id)
#     item.quantity=item.quantity+1
#     item.save()
#     tem=item.Treatment_id    
#     return redirect('docter:pre2',tem)
   
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='home:signin')    
def doc_Password(request):
     if request.method == 'POST':
        try:
            user=User.objects.get(id=request.user.id)
            passw=request.POST.get('passw')
            con_passw=request.POST.get('con_passw')
            
            if passw =='' and con_passw == '':
                messages.error(request,'its not valid')
                return redirect('docter:doc_Password')

            if passw != con_passw:
                messages.error(request,'Password should be equal')
                return redirect('docter:doc_Password')
            
            try:
                validate_password(passw)

            except ValidationError as e:
                messages.error(request, e)
                return redirect('docter:doc_Password')


            if user:
                user.set_password(passw)
                user.save()
                print(user.password)
                messages.success(request,'Password is change')
                return redirect('docter:doc_dashboard')
        except: 
                messages.error(request,'something went wrong')
                return redirect('docter:doc_Password')

     else:
         return render(request,'doc_Password.html',{'page':'password'})
             