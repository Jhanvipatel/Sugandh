"""ProjectSugandh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from Sugandh import views
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
import debug_toolbar



urlpatterns = [
    path('',views.index,name='index'),
    path('setting.html', views.globalsetting, name='home'),
    path('settingcollection', views.setting_coll, name='setting_coll'),
    path('settingwomen',views.setting_women,name='setting_women'),
    path('settingupcycled',views.setting_upcycled,name='setting_upcycled'),
    path('settingsale',views.setting_sale,name='setting_sale'),
    path('settingtrending',views.setting_trending,name='setting_trending'),
    path('About-Us',views.aboutus,name='about_us'),
    path('updateabout-us',views.updateaboutus,name="update_aboutus"),
    path('admin/', admin.site.urls),
    path('collection.html',views.showcoll),
    # path('showsize',views.showcsize),
    # path('edit/<slug:id>', views.editcoll, name='edit_view'),
    # path('update/<int:id>', views.updatecoll),
    path('deletecoll/<slug:collectionID>/', views.deletecoll, name='delete_view_collection'),
    path('updatecollection/', views.updatecoll, name='update_coll'),
    path('addcollection/', views.addcoll, name='add_collection'),
    path('deletesize/<slug:sizeID>/', views.deletesize, name='delete_view'),
    path('updatesize/', views.updatesize, name='update_size'),
    path('addsize/', views.addsize, name='add_size'),
    path('deletefabric/<slug:fabricID>/', views.deletefabric, name='delete_view_fabric'),
    path('updatefabric/', views.updatefabric, name='update_fabric'),
    path('addfabric/', views.addfabric, name='add_fabric'),
    path('product.html',views.showproduct, name='product_display'),
    path('add-product.html/', views.addproduct, name='add_product'),
    path('product-details.html',views.productdetail, name='product_detail'),
    path('storeproduct.html',views.storeproduct,name='store_product'),
    path('display.html',views.display,name='display_product'),
    path('finish.html',views.finish,name='finish'),
    path('update-product.html/', views.updateproduct, name='update_product'),
    path('add-product-detail.html/', views.addproductdetail, name='add_product_detail'),
    path('deleteproduct/<slug:productID>/', views.deleteproduct, name='delete_product'),
    path('reseller.html',views.showreseller),
    path('add-reseller.html',views.addreseller,name='add_reseller'),
    path('add-reseller-detail.html',views.addresellerdetail,name='add_reseller_detail'),
    path('deletereseller/<slug:resellerID>', views.deletereseller, name="delete_reseller"),
    path('updatereseller.html',views.updatereseller, name='update_reseller'),
    path('blogs.html',views.showblogs),
    path('add-blogs.html',views.addblog,name='add_blog'),
    path('add-blog-detail.html',views.addblogdetail,name='add_blog_detail'),
    path('updateblog.html',views.updateblog,name='update_blog'),
    path('deleteblog/<slug:blogID>', views.deleteblog, name="delete_blog"),
    path('customers.html',views.customer,name='view_customer'),
    path('customers-detail.html/<slug:customerID>',views.customerdetail,name='view_customers_detail'),
    path('updatecustomer.html',views.updatecustomer,name='update_customer'),
    path('pushfacebook',views.push,name='push_facebook'),
    path('websitemessage.html',views.showwebsitemessage),
    path('updatewebmsg.html',views.updatewebmsg,name='update_webmsg'),
    path('deletewebmsg.html/<slug:webID>',views.deletewebmsg,name='delete_webmessage'),
    path('brand.html',views.showbrand),
    path('updatebrand.html',views.updatebrand,name='update_brand'),
    path('add-brand.html',views.addbrand,name='add_brand'),
    path('deletebrand.html/<slug:brandID>',views.deletebrand,name='delete_brand'),
    path('stock.html',views.stock,name='display_stock'),
    path('__debug__/', include(debug_toolbar.urls))
]
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# + static(settings.MESIA_URL,document_root=settings.MEDIA_ROOT)
