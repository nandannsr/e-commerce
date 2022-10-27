from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('login',views.index,name='login'),
    path('home',views.adminhome,name='home'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    
    #Admin panel views for management of Brand , products and categories
    path('addadmincategory', views.addcategory, name='addcategory'),
    path('editcategory/<int:id>/', views.editcategory, name='edit-category'),
    path('deletecategory/<int:id>/', views.deletecategory, name='delete-category'),
    path('admincategory', views.categoryList, name='categorylist'),
    path('addadminbrand', views.addbrand, name='addbrand'),
    path('editbrand/<int:id>/', views.editbrand, name='edit-brand'),
    path('deletebrand/<int:id>/', views.deletebrand, name='delete-brand'),
    path('adminbrand', views.brandList, name='brandlist'),
    path('adminproduct', views.productList, name='productlist'),
    path('editproduct/<int:id>', views.editproduct, name='edit-product'),
    path('addadminproduct', views.addproduct, name='addproduct'),
    path('deleteproduct/<int:id>', views.deleteproduct, name='delete-product'),
    
    #Admin panel views for managing users
    path('adminuser', views.userlist, name='userlist'),
    path('blockuser/<int:id>', views.blockuser, name='blockuser'),
    path('unblockuser/<int:id>', views.unblockuser, name='unblockuser'),
    
    #Admin Offer management 
    path('brandoffers',views.brandofferlist,name='brandoffers'),
    path('addbrandoffer',views.addbrandoffer,name='addbrandoffer'),
    path('editbrandoffer/<int:id>', views.editbrandoffer, name='editbrandoffer'),
    path('deletebrandoffer/<int:id>', views.deletebrandoffer,name='deletebrandoffer'),
    path('categoryoffers',views.categoryofferlist,name='categoryoffers'),
    path('addcategoryoffer',views.addcategoryoffer,name='addcategoryoffer'),
    path('editcategoryoffer/<int:id>', views.editcategoryoffer, name='editcategoryoffer'),
    path('deletecategoryoffer/<int:id>', views.deletecategoryoffer,name='deletecategoryoffer'),
    path('productoffers',views.productofferlist,name='productoffers'),
    path('addproductoffer',views.addproductoffer,name='addproductoffer'),
    path('editproductoffer/<int:id>', views.editproductoffer, name='editproductoffer'),
    path('deleteproductoffer/<int:id>', views.deleteproductoffer,name='deleteproductoffer'),
    
    #Admin Coupon management
    path('couponlist',views.couponlist,name='couponlist'),
    path('editcoupons/<int:id>', views.editcoupons, name='editcoupons'),
    path('addcoupons', views.addcoupons, name='addcoupons'),
    path('deletecoupon/<int:id>', views.deletecoupon, name='deletecoupon'),
    
    #Admin Order management
    path('admin-orders',views.order_list,name='admin-orders'),
    path("delivery-status/", views.delivered_status, name="delivery-status"),
    path('cancel-status/',views.cancel_status,name='cancel-status'),
    path('return-status/',views.return_status,name='return-status'),
    path('order-search/',views.order_search,name='order-search'),
    
    #Sales Report
    path("sales-report/", views.sales_report, name="sales-report"),
    path("sales-report-csv",views.sales_export_csv,name='sales-report-csv'),
]