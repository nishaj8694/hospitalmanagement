from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from home.models import User,Order,orderItem,Cart,Refund
from patient.models import patientProfile,wallet
from docter.models import DoctorProfile,Department
from .forms import pform,vform,coupenform,medicineform
from django.contrib.auth import logout,login
from django.views.decorators.cache import cache_control
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Product,varient,Catagory
from django.db.models import Prefetch
from patient.views import Pat_dashboard 
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Sum
from django.core import serializers
import json
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.template.loader import get_template
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from xhtml2pdf import pisa
import uuid
from django.shortcuts import render
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from django.http import JsonResponse
from .models import Medicine_type,coupen
from django.views.decorators.csrf import csrf_exempt
from .forms import MonthYearForm 
from django.http import JsonResponse
from docter.forms import department_form
from django.views import View
import calendar
from django.db.models import Exists, OuterRef



@csrf_exempt
def sales_search(request):
    if request.method == 'POST':
        month = request.POST.get('month')
        year = request.POST.get('year')
        orders = Order.objects.filter(order_date__year=year)

        all_days = calendar.monthrange(int(year), int(month))[1]
        
        if month:
            orders = orders.filter(order_date__month=month)

        orders_by_month = orders.values('order_date__year', 'order_date__month','order_date__day').annotate(total_revenue=Sum('Total_Price')).order_by('order_date__year', 'order_date__month','order_date__day')
        i=0
        sales_data = []
        for day in range(1, all_days + 1):
            if len(orders_by_month) >i:   
                if day==orders_by_month[i]['order_date__day']:
                    sales_data.append({
                     'year': month,
                     'month': year,
                     'day': orders_by_month[i]['order_date__day'],
                     'total_revenue': float(orders_by_month[i]['total_revenue'])
                   })
                    i+=1
                else:
                  sales_data.append({
                    'year': month,
                    'month': year,
                    'day': day,
                    'total_revenue': float('0')
                 })
            else:
                  sales_data.append({
                    'year':month,
                    'month':year,
                    'day': day,
                    'total_revenue': float('0')
                 })       
  
        return JsonResponse({'success':True, 'sales_data': sales_data})
    else:
        return JsonResponse({'success':False})
   

def yearly_report(request):
    orders_by_year = Order.objects.values('order_date__year').annotate(total_revenue=Sum('Total_Price')).order_by('order_date__year')
    sales_data = []
    for order in orders_by_year:
        sales_data.append({
            'year': order['order_date__year'],
            'total_revenue': float(order['total_revenue'])
        })
    order=sales_data    
    sales_data=json.dumps(sales_data)  
    return render(request, 'yearly_sales.html', {'sales_data':sales_data,'order':order})

def monthly_sales_report(request):
    year = datetime.now().year
    orders_by_month = Order.objects.filter(order_date__year=year,status='finish').values('order_date__year', 'order_date__month').annotate(total_revenue=Sum('Total_Price')).order_by('order_date__year', 'order_date__month')
    sales_data = []
    for order in orders_by_month:
        sales_data.append({
            'year': order['order_date__year'],
            'month': order['order_date__month'],
            'total_revenue': float(order['total_revenue'])
        })
    order=sales_data
    # print(sales_data)
    sales_data=json.dumps(sales_data)
    return render(request, 'month.html', {'order':order })

def daily_sales_report(request):
    orders_by_day = Order.objects.values('order_date__date').annotate(total_revenue=Sum('Total_Price')).order_by('order_date__date')
    sales_data = []
    for order in orders_by_day:
       if order['order_date__date'] is not None:
           sales_data.append({
              'date': order['order_date__date'].strftime('%B %d %Y'),
              'total_revenue': float(order['total_revenue'])
          })
    sales_data=json.dumps(sales_data, cls=DjangoJSONEncoder)
    return render(request, 'day.html', {'sales_data': sales_data })



def today_report(request):
    today = datetime.now().date()
    orders_today = Order.objects.filter(order_date__date=today,status='finish').values(
        'order_date__time','Total_Price')
    sales_data = []
    print(orders_today)
    for order in orders_today:
        sales_data.append({
            'date': order['order_date__time'].strftime('%H:%M:%S'),
            'total_revenue': order['Total_Price']
        })
    sales_data_json = json.dumps(sales_data, cls=DjangoJSONEncoder)  
    return render(request, 'today.html', {'sales_data': sales_data_json})


def weekly_report(request):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    orders_by_day = Order.objects.filter(order_date__date__range=[start_date, end_date]) \
        .values('order_date__date').annotate(total_revenue=Sum('Total_Price')).order_by('order_date__date')
    sales_data = []
    k=0
    for i in range(8):
        if k<len(orders_by_day):
            if start_date == orders_by_day[k]['order_date__date']:
                sales_data.append({
                 'date': orders_by_day[k]['order_date__date'].strftime('%B %d %Y'),
                 'total_revenue': float(orders_by_day[k]['total_revenue'])
                })
                print(start_date)
                k+=1
               
            else:
                sales_data.append({
                'date': start_date.strftime('%B %d %Y'),
                'total_revenue': float('0')
            })
                 
        start_date=start_date+timedelta(days=1)         
        
    sales_data_json = json.dumps(sales_data, cls=DjangoJSONEncoder) 
    return render(request, 'week.html', {'sales_data': sales_data_json})

   


def download(request):
    if request.method == 'POST':
        action=request.POST.get('action')
        if action =='month':
            orders_by_month = Order.objects.values('order_date__year', 'order_date__month').annotate(total_revenue=Sum('Total_Price')).order_by('order_date__year', 'order_date__month')
            order_data = []
            for order in orders_by_month:
                order_data.append({
                    'year': order['order_date__year'],
                    'month': order['order_date__month'],
                    'total_revenue': float(order['total_revenue'])
                })
            data = [(order['year'], order['month'], order['total_revenue']) for order in order_data]
            colnames = ('Year', 'Month', 'Total Revenue')    

        if action == 'year':
            orders_by_year = Order.objects.values('order_date__year').annotate(total_revenue=Sum('Total_Price')).order_by('order_date__year')
            order_data = []
            for order in orders_by_year:
                order_data.append({
                    'year': order['order_date__year'],
                    'total_revenue': float(order['total_revenue'])
                })

            data = [(order['year'], order['total_revenue']) for order in order_data]
            colnames = ('Year', 'Total Revenue')       
             

    # print(type(order_data))
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
        table = Table([colnames]+ data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        doc.build([table])
        pdf = buffer.getvalue()
        buffer.close()
        response = HttpResponse(pdf, content_type='application/pdf')
        name=uuid.uuid4()
        response['Content-Disposition'] = f'attachment; filename="{name}.pdf"'
        return response

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    pdf_status = pisa.CreatePDF(html, dest=response)
    if pdf_status.err:
        return HttpResponse('Some errors were encountered <pre>' + html + '</pre>')
    return response

def order_summery(request,id):
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
    

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            orders_by_year = Order.objects.values('order_date__year').annotate(total_revenue=Sum('Total_Price')).order_by('order_date__year')
            sales_year = []
            for order in orders_by_year:
                sales_year.append({
                'year': order['order_date__year'],
                'total_revenue': float(order['total_revenue'])
                })
            sales_year=json.dumps(sales_year)     


            # c_year=datetime.now().year
            # orders_by_month = Order.objects.filter(order_date__year=c_year).values('order_date__year', 'order_date__month').annotate(total_revenue=Sum('Total_Price')).order_by('order_date__year', 'order_date__month')
            # sales_month = []
            # for order in orders_by_month:
            #     sales_month.append({
            #         'year': order['order_date__year'],
            #         'month': order['order_date__month'],
            #         'total_revenue': float(order['total_revenue'])
            #     })
            # sales_month=json.dumps(sales_month)


            year = datetime.now().year
            mnth=datetime(year, 1, 1)

            orders_by_month = Order.objects.filter(order_date__year=year,status='finish').values('order_date__year', 'order_date__month').annotate(total_revenue=Sum('Total_Price')).order_by('order_date__year', 'order_date__month')
            sales_month = []
            j=0
            for i in range(13):
                if j<len(orders_by_month):
                    if mnth.month==orders_by_month[j]['order_date__month']:
                      sales_month.append({
                        'year': orders_by_month[j]['order_date__year'],
                        'month': orders_by_month[j]['order_date__month'],
                        'total_revenue': float(order['total_revenue'])
                      })
                      j+=1
                    else:
                         sales_month.append({
                        'year': orders_by_month[j]['order_date__year'],
                        'month':mnth.strftime('%m'),
                        'total_revenue': float('0')
                   }) 
                mnth=mnth+relativedelta(months=1)              
                      
            # for order in orders_by_month:
            #     sales_month.append({
            #         'year': order['order_date__year'],
            #         'month': order['order_date__month'],
            #         'total_revenue': float(order['total_revenue'])
            #     })
            sales_month=json.dumps(sales_month)
            

            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=7)
            orders_by_day = Order.objects.filter(order_date__date__range=[start_date, end_date],status='finish') \
                .values('order_date__date').annotate(total_revenue=Sum('Total_Price')).order_by('order_date__date')
            sales_weak = []
            k=0
            for i in range(8):
                if k<len(orders_by_day):
                    if start_date == orders_by_day[k]['order_date__date']:
                        sales_weak.append({
                        'date': orders_by_day[k]['order_date__date'].strftime('%B %d %Y'),
                        'total_revenue': float(orders_by_day[k]['total_revenue'])
                        })
                        k+=1
                    
                    else:
                        sales_weak.append({
                        'date': start_date.strftime('%B %d %Y'),
                        'total_revenue': float('0')
                    })
                        
                start_date=start_date+timedelta(days=1)

            sales_weak = json.dumps(sales_weak, cls=DjangoJSONEncoder)
            
              
            

            today = datetime.now().date()
            orders_today = Order.objects.filter(order_date__date=today,status='finish').values(
                'order_date__time','Total_Price')
            sales_today = []
            print(orders_today)
            for order in orders_today:
                sales_today.append({
                    'date': order['order_date__time'].strftime('%H:%M:%S'),
                    'total_revenue': order['Total_Price']
                })
            sales_today = json.dumps(sales_today, cls=DjangoJSONEncoder) 



            c_month=datetime.now().month
            orders_cur_month = Order.objects.filter(order_date__month=c_month).values('order_date__date').annotate(total_revenue=Sum('Total_Price')).order_by('order_date__date')
            sales_cur_month = []
            for order in orders_cur_month:
                sales_cur_month.append({
                    'date': order['order_date__date'].strftime('%B %d %Y'),
                    'total_revenue': float(order['total_revenue'])
                })
            sales_cmonth = json.dumps(sales_cur_month, cls=DjangoJSONEncoder)    

            pat=User.objects.filter(is_patient=True)
            doc=User.objects.filter(is_docter=True)
            prod_no=Product.objects.all()                  # print(pat,doc,prod_no)
            context={'pat':pat,'doc':doc,'prod_no':prod_no,'sales_month':sales_month, 'sales_year':sales_year,'sales_weak':sales_weak,'sales_today':sales_today,'sales_cmonth':sales_cmonth}
            return render(request, 'admin.html',context)
        else:
            return redirect('home:home')
    else:
        return redirect('home:signin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def show_doct(request):
    users=User.objects.filter(is_docter=True)
    if users:
        context={'users':users,'page':'doc-s'}
        return render(request,'admin_doct.html',context)
    
    messages.error(request,'something wrong')
    return render(request,'admin.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def show_users(request):
    users=User.objects.filter(is_patient=True)
    if users:
        context={'users':users,'page':'ad-user'}
        return render(request,'admin_user.html',context)

    messages.error(request,'something wrong')
    return render(request,'admin.html')



def search(request):
    if request.method == 'POST':
        search=request.POST.get('search')
        
        if search =='':
            messages.error(request,'fill the search box') 
            return redirect('dashboard')
        product=Product.objects.filter(name__contains=search)
        if product:
            context={'product':product}
            return render(request,'search.html',context)
        
        messages.error(request,'fill the search box') 
        return redirect('dashboard')

    else:
        return redirect('dashboard')





def coupnshow(request):
    coupens=coupen.objects.all()
    context={'page':'ad-cp','coupens':coupens}
    return render(request,'coupenshow.html',context)
def coupn(request):
    if request.method=='POST':
        form=coupenform(request.POST)
        if form.is_valid():
            coop=coupen.objects.filter(name=form.instance.name) 
            if coop:
                messages.error(request,'coupen already exist try another one')
                return redirect('coupn')
            else:
               form.save()
               messages.success(request,'coupen added')
               return redirect('dashboard')
        else:
            messages.error(request,'form is not valid try agine')
            return redirect('coupn')   
    else:
        form=coupenform()
        return render(request,'coupen.html',{'form':form,'page':'ad-cp'})
    

@csrf_exempt
def coupndelete(request):
     if request.method=='POST':
        id=request.POST.get('id')
        try:
            coop=coupen.objects.get(id=id)
        except:
            # messages.error(request,'coupen doest exist')
            # return redirect('coupn')   
            return JsonResponse({'success':False})
        
        coop.delete()
        return JsonResponse({'success':True})
     else:
         return JsonResponse({'success':False})

        # messages.error(request,'coupen deleted')
        # return redirect('coupn') 


def coupnedit(request,id):
    if request.method=='POST':
        form=coupenform(request.POST)
        if form.is_valid():
            try:
              coop=coupen.objects.get(id=id)
            except:
                messages.error(request,'coupen doest exist')
                return redirect('coupn')  
            coop2=coupen.objects.filter(name=form.instance.name)
            if coop2:
                messages.error(request,'coupen already exist try another one')
                return redirect('coupn')
            else:
               coop.name=form.instance.name
               coop.discount_price=form.instance.discount_price
               coop.expairy_date=form.instance.expairy_date
               coop.save()
               messages.success(request,'coupen added')
               return redirect('dashboard')
        else:
            messages.error(request,'form is not valid try agine')
            return redirect('coupn')   
    else:
        try:
          coop=coupen.objects.get(id=id)
        except:
            messages.error(request,'invalied coupe')
            return redirect('coupnedit',id) 
         
        form=coupenform(instance=coop)
        return render(request,'coupen.html',{'form':form,'page':'ad-cp'})





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def block(request):
    if request.method=='POST':
        id=request.POST['dele']
        print('block',id)
        users=User.objects.get(id=int(id))
        if users:
            users.block=True
            users.save()
            if users.is_patient:
                    return redirect('show_users')
            else:
                    return redirect('show_doct')
        

    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def unblock(request):
    if request.method=='POST':
        id=request.POST['dele']
        print('un-blo',id)
        users=User.objects.get(id=int(id))
        if users:
            print("noth")
            users.block=False
            users.save()
            if users.is_patient:
                return redirect('show_users')
            else:
                return redirect('show_doct') 
        

@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def delet_users(request):
    if request.method=='POST':
        id=request.POST['dele']
        users=User.objects.get(id=int(id))  
        if users:
            if users.is_docter:
                users.delete()
                return redirect('show_doct')
            if users.is_patient:
                users.delete()
                return redirect('show_users')


    




def get_subcategories(request):
    category_id = request.GET.get('category_id')
    # print(category_id)
    subcategories = Medicine_type.objects.filter(medicine_type_id=category_id).values('id', 'name')
    # print(subcategories)
    return JsonResponse(list(subcategories), safe=False)



class ProductItem(View):
    def get(self,request,*args,**kwargs):
        product=Product.objects.prefetch_related(Prefetch('item',queryset=varient.objects.all()))
        context={'product':product,'page':'s-pr'}
        return render(request,'product_show.html',context)
    def post(self,request,*args,**kwargs):
       pass
    def put(self,request,*args,**kwargs):
       pass
    def delete(self,request,*args,**kwargs):            
       pass




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def show_Product(request):
    product=Product.objects.prefetch_related(Prefetch('item',queryset=varient.objects.all()))
    context={'product':product,'page':'s-pr'}
    return render(request,'product_show.html',context)       

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ad_Product(request):
    if request.method=='POST':
        sit=request.POST.get('med')
        form=pform(request.POST , request.FILES)
        if form.is_valid():
            form.save()
            if sit:
               form.instance.medicine_type_id=sit
               form.save()
            detaile=Product.objects.get(id=form.instance.id)
            context={'form':vform(),'detaile':detaile}
            return render(request,'ad_variations.html',context)
        else:
            messages.error(request, 'something went wrong')
            form=pform()
            return render(request,'ad_Product.html',{'form':form,'page':'ad-Pr'})
    else:
        form=pform()
        return render(request,'ad_Product.html',{'form':form,'page':'ad-Pr'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_prod(request,id):
    item=Product.objects.get(id=id)
    if request.method=='POST':
        form=pform(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('show_Product')              

        return redirect('show_Product')              
    else:
        detaile=Product.objects.get(id=id)
        context={'edit_form':pform(instance=detaile),'detaile':detaile}
        return render(request,'edit_product.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_item(request):
    if request.method=='POST':
        name=request.POST['dele']
        dl=Product.objects.get(id=int(name))
        dl.delete()
        return redirect('show_Product')






@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def ad_varient(request,id):
    if request.method=='POST':
        form=vform(request.POST)
        if form.is_valid():
            form.save(commit=False)
            si=request.POST.get('size')
            print(si)
            
            pr=request.POST.get('price')
            print(pr)
             
            if si == '' and  pr == '':
                  messages.error(request,'field must not blanks')
                  return HttpResponseRedirect(reverse('ad_varient', args=[id]))  
                    
            
            form.instance.product_id=id
            prod=varient.objects.select_related('product').filter(product_id=id,size=form.instance.size)
            for i in prod:
              if form.instance.size in i.size:
                  messages.error(request,'size is already exixts,choose another choice')
                  return HttpResponseRedirect(reverse('ad_varient', args=[id]))  
            form.save()
            return HttpResponseRedirect(reverse('ad_varient', args=[id]))
    else:
        itm=varient.objects.prefetch_related('product').filter(product_id=id)
        detaile=Product.objects.get(id=id)
        context={'form':vform(),'detaile':detaile,'itm':itm}
        return render(request,'ad_variations.html',context)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delet_varit(request,id):
    if request.method=='POST':
        pass
    else:
        product=Product.objects.prefetch_related(Prefetch('item',queryset=varient.objects.all())).filter(id=id)
        for i in product:
            print(i.name,i.catagory)
        context={'delprod':product}
        return render(request,'del_varient.html',context)
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def del_va(request,id):
    item=varient.objects.get(id=id)
    id=item.product_id
    item.delete()
    # return redirect('show_Product')
    
    # return redirect('delet_varit')
    return HttpResponseRedirect(reverse('delet_varit', args=[id]))





@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def pat_up(request):
    if request.method == 'POST':
        fullname = request.POST['name']
        username = request.POST['username']
        email=request.POST['email']
        password = request.POST['password']
        number = request.POST['number']

        comf_password = request.POST['comf-password']

        if fullname == '' and username == '' and password == '' and email =='' and number =='':
            messages.error(request, "Fields can't be blank")
            return redirect('pat_up')

        if password != comf_password:
            messages.error(request, "Password dosen't match")
            return redirect('pat_up')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('pat_up')

        try:
            validate_password(password)

        except ValidationError as e:
            messages.error(request, e)
            return redirect('pat_up')

        user = User.objects.create_user(username=username, password=password)
        user.first_name = fullname
        user.is_patient=True
        user.email=email
        user.save()
        crt=Cart.objects.create(user=user)
        profile=patientProfile.objects.create(user=user)
        if len(number)>10:
            profile.contact_number=number
        else:
            profile.contact_number='+91'+number

        walt=wallet.objects.create(PatientProfile=profile)
        walt.save()
        profile.save()
        crt.save()
        user.save()
        messages.success(request, 'User created successfully')
        return redirect('show_users')
    else:
        return render(request, 'admin_pat_sign.html',{'page':'ad-Pat'})
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def doc_up(request):
    if request.method == 'POST':
        fullname = request.POST['name']
        username = request.POST['username']
        email=request.POST['email']
        number = request.POST['number']
        password = request.POST['password']
        comf_password = request.POST['comf-password']

        if fullname == '' and username == '' and password == '' and email =='' and number =='':
            messages.error(request, "Fields can't be blank")
            return redirect('doc_up')

        if password != comf_password:
            messages.error(request, "Password dosen't match")
            return redirect('doc_up')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('doc_up')

        try:
            validate_password(password)

        except ValidationError as e:
            messages.error(request, e)
            return redirect('doc_up')

        user = User.objects.create_user(username=username, password=password,is_docter=True)
        user.first_name = fullname
        user.email=email
        user.save()
        Patient=DoctorProfile.objects.create(user=user)
        if len(number)>10:
            Patient.contact_number=number
        else:
            Patient.contact_number='+91'+number

        Patient.save()
        user.save()
        messages.success(request, 'User created successfully')
        return redirect('show_doct')
    else:
        return render(request, 'admin_doc_signin.html',{'page':'doc'})




def department_show(request):
    department=Department.objects.all()    
    return render(request, 'department_show.html',{'page':'depart','department':department})

def department_add(request):
    if request.method=='POST':
        form=department_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department')
    else:
        form=department_form()
        return render(request, 'department_add.html',{'page':'depart','form':form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def department_edit(request,id):
    if request.method=='POST':
        form=department_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('department')
    else:
        dep=Department.objects.get(id=id)
        print(dep)
        form=department_form(instance=dep)
        return render(request, 'department_edit.html',{'page':'depart','form':form,'id':id})    
         

# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt    
def department_delete(request):
    if request.method=='POST':
       id=request.POST.get('id')
       cate=Department.objects.filter(id=id)
       cate.delete()
       return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})
           







@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def catagory(request):
        cate=Catagory.objects.all()
        context={'category':cate,'page':'ad-cg'}
        return render(request, 'catagory.html',context)

def add_catagory(request):
    if request.method =='POST':
        name=request.POST.get('name')
        if name =='':
            return redirect('add_catagory')
        
        obj=Catagory.objects.create(name=name)
        obj.save()
        return redirect('catagory')
    
    return render(request, 'add_catagory.html')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)    
def catagory_delet(request,id):
    cate=Catagory.objects.filter(id=id)
    cate.delete()
    return redirect('catagory')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def catagory_edit(request,id):
    cate=Catagory.objects.get(id=id)
    if request.method=='POST':
        name=request.POST['name']

        if name=='':
            messages.error(request,'this field cant be blank ' )
            return HttpResponseRedirect(reverse('catagory_edit', args=[id]))
                
        cate.name=name
        cate.save()
        return redirect('catagory')
    
    else:
        context={'cate':cate,'id':id}
        return render(request, 'edit_catagory.html',context)








@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def medicine_type(request):
        cate=Medicine_type.objects.filter(medicine_type=None)
        context={'category':cate,'page':'ad-mg'}
        return render(request, 'medicine_type.html',context)

def add_medicine_type(request):
    if request.method =='POST':
        med=medicineform(request.POST)
        if med.is_valid():
            med.save()
            return redirect('medicine_type')
        else:
            return redirect('add_medcine_type') 

    else:
        form=medicineform()
        return render(request, 'add_medicine_type.html',{'form':form,'page':'ad-mg'})


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@csrf_exempt    
def medicine_delet(request):
    if request.method=='POST':
       id=request.POST.get('id')
       cate=Medicine_type.objects.filter(id=id)
       cate.delete()
       return JsonResponse({'success':True})
    else:
         return JsonResponse({'success':False})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def medicine_type_edit(request,id):
    if request.method=='POST':
        cate=Medicine_type.objects.get(id=id)
        name=request.POST['name']
        if name=='':
            messages.error(request,'this field cant be blank ' )
            return HttpResponseRedirect(reverse('medicine_type_edit', args=[id]))
        
        cate.name=name
        cate.save()
        return redirect('medicine_type')
    
    else:
        cate=Medicine_type.objects.get(id=id)
        context={'cate':cate,'id':id}
        return render(request, 'edit_medicine_type.html',context)





def orderstatus(request):
    if request.method=='POST':
        status=request.POST.get('status')
        id=request.POST.get('id')
        ord=Order.objects.get(id=id)
        if status=='deliverd':
            ord.delivery_date=datetime.now()
            ord.status=status
            ord.save()
            return JsonResponse({'success':True})
        if ord.status !='deliverd':    
                if status=='revoke':
                    if ord.Pay_option=='cash':
                        ord.status='cancel'
                        ord.save()
                        return JsonResponse({'success':True})
                    else:
                        ord.status='cancel'
                        refu=Refund.objects.create(order=ord)
                        refu.cancelby='admin'
                        wal=wallet.objects.get(PatientProfile__user=ord.user)
                        if wal.amount==None:
                            wal.amount=0 
                        wal.amount+=ord.Total_Price
                        wal.save()
                        refu.status='completed'
                        refu.save()   
                        ord.cancel_date=datetime.now()
                        ord.save()                    
                        return JsonResponse({'success':True}) 
                else:
                    ord.status=status
                    ord.save()
                    return JsonResponse({'success':True})

       
    else:
        return JsonResponse({'success':False})
    

def admin_order(request):
    order_list=Order.objects.prefetch_related(Prefetch('order_items',queryset=orderItem.objects.all())
                            ,Prefetch('order_refund',queryset=Refund.objects.all())).exclude(status='deliverd' or 'cancel', cancel_date=None)
    context={'order_list':order_list ,'page':'admn-ord'}
    return render(request,'adminorder.html',context)

def admin_order_specific(request):
    list_status=['deliverd','cancel']
    order_list=Order.objects.exclude(status__in=list_status).prefetch_related(Prefetch('order_items',
        queryset=orderItem.objects.all())).exclude(Exists(Refund.objects.filter(
                                       order=OuterRef('pk'))))
   
  
   
    context={'order_list':order_list ,'page':'admn-ord'}
    return render(request,'adminorder.html',context)

def admin_order_refund(request):
    refund=Refund.objects.exclude(status='completed' or 'cancel')
    ord=Order.objects.filter(order_refund__in=refund)
    order_list=ord.prefetch_related(Prefetch('order_items',queryset=orderItem.objects.all()),
                                    Prefetch('order_refund',queryset=Refund.objects.all()))
    context={'order_list':order_list ,'page':'admn-ord'}
    return render(request,'adminorder.html',context)


def refundstatus(request):
    if request.method=='POST':
        status=request.POST.get('status')
        id=request.POST.get('id')
        ord=Refund.objects.get(id=id)
        ord.save()
        if ord.cancelby =='':
            ord.cancelby='admin'
            ord.save()
        if status =='completed':
           ref=Order.objects.get(id=ord.order_id)
           if ref:
            if ord.refund_option=='wallet':
                try:
                    if ref.delivery_date!=None:
                        ref.delivery_date=None
                        ref.cancel_date=None
                    user=patientProfile.objects.get(user_id=ref.user_id)
                    wal=wallet.objects.get(PatientProfile=user)
                    if wal.amount==None:
                        wal.amount=0 
                    wal.amount+=ref.Total_Price
                    wal.save()
                    ord.refund_amount=ref.Total_Price
                    ord.status='completed'
                    ord.save() 
                    ref.save()    
                except:
                    return JsonResponse({'success':False})
            else:
               ord.refund_amount=ref.Total_Price
               ord.status='completed'
               ord.save()
            
           return JsonResponse({'success':True})
        
        elif status =='cancel':
            try:
              itm=Order.objects.get(id=ord.order_id)
              if itm.delivery_date !=None:
                    itm.status='deliverd'
                    itm.cancel_date=None
                    itm.save()
                    ord.delete()
                    ord.save()
                    return JsonResponse({'success':True})
              else:    
                    itm.status='pending'
                    itm.delivery_date=None
                    itm.cancel_date=None
                    itm.save()
                    ord.delete()
                    ord.save()
                    return JsonResponse({'success':True})

            except:

                return JsonResponse({'success':False})
                


        else:
            ord.status=status     
            ord.save()
            return JsonResponse({'success':True})
    else:
        return JsonResponse({'success':False})

def admin_ord_c(request): 
    list_status=['deliverd','cancel']
    order_list=Order.objects.prefetch_related(Prefetch('order_items',queryset=orderItem.objects.all()),Prefetch('order_refund',queryset=Refund.objects.all())).filter(status__in=list_status)
    context={'order_list':order_list ,'page':'ord-com'}
    return render(request,'adminorder-com.html',context)