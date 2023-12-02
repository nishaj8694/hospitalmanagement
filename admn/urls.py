"""hosp_mng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from admn import views 

urlpatterns = [
    # path('patient/', include(('patient.urls', 'patient'), namespace='patient')),
    path('ad_Product',views.ad_Product,name='ad_Product'),
    path('ad_varient/<int:id>',views.ad_varient,name='ad_varient'),
    path('dashboard',views.dashboard,name='dashboard'),
    path('show_Product',views.show_Product,name='show_Product'),
    path('delete',views.delete_item,name='delete-item'),
    path('block',views.block,name='block'),
    path('unblock',views.unblock,name='unblock'),
    path('show_users',views.show_users,name='show_users'),
    path('show_doct',views.show_doct,name='show_doct'),
    path('delet_varit/<int:id>',views.delet_varit,name='delet_varit'),
    path('del_va/<int:id>',views.del_va,name='del_va'),
    path('edit_prod/<int:id>',views.edit_prod,name='edit_prod'),
    path('pat_up',views.pat_up,name='pat_up'),
    path('delet_users',views.delet_users,name='delet_users'),
    path('doc_up',views.doc_up,name='doc_up'),
    path('catagory',views.catagory,name='catagory'),
    path('catagory_delet/<int:id>',views.catagory_delet,name='catagory_delet'),
    path('catagory_edit/<int:id>',views.catagory_edit,name='catagory_edit'),
    path('add_catagory',views.add_catagory,name='add_catagory'),
    path('medicine_type',views.medicine_type,name='medicine_type'),
    path('add_medicine_type',views.add_medicine_type,name='add_medicine_type'),
    path('medicine_delet',views.medicine_delet,name='medicine_delet'),
    path('medicine_type_edit/<int:id>',views.medicine_type_edit,name='medicine_type_edit'),
    path('search',views.search,name='search'),
    path('month',views.monthly_sales_report,name='month'),
    path('day',views.daily_sales_report,name='day'),
    path('today',views.today_report,name='today'),
    path('week',views.weekly_report,name='week'),
    path('year',views.yearly_report,name='year'),
    path('download',views.download,name='download'),
    path('admin_order',views.admin_order,name='admin_order'),
    path('admin_order_refund',views.admin_order_refund,name='admin_order_refund'),
    path('admin_order_specific',views.admin_order_specific,name='admin_order_specific'),
    path('admin_c',views.admin_ord_c,name='admin_c'),
    path('get_subcategories/', views.get_subcategories, name='get_subcategories'),
    path('orderstatus',views.orderstatus,name='orderstatus'),
    path('refundstatus',views.refundstatus,name='refundstatus'),
    path('order_summery<int:id>',views.order_summery,name='order_summery'),
    path('coupn',views.coupn,name='coupn'),
    path('coupnedit/<int:id>',views.coupnedit,name='coupnedit'),
    path('coupndelete',views.coupndelete,name='coupndelete'),
    path('coupnshow',views.coupnshow,name='coupnshow'),
    path('sales_search',views.sales_search,name='sales_search'),
    path('department',views.department_show,name='department'),
    path('department_add',views.department_add,name='department_add'),
    path('department_edit/<int:id>',views.department_edit,name='department_edit'),
    path('department_delete',views.department_delete,name='department_delete'),







]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

