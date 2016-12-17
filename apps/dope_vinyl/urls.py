from django.conf.urls import url
from . import views
urlpatterns = [

    ########################## HOME #####################################
    url(r'^$', views.home),
    url(r'^show$', views.home),

    ########################## FRONT END #####################################
    # url(r'^dashboard/products$', views.products),
    url(r'^front_allproducts$', views.front_allproducts),
    url(r'^front_allproducts/page(?P<page>[0-9]+)/$', views.front_allproducts),
    url(r'^front_allproducts/category/(?P<id>\d+)$', views.front_allproducts_cat),
    # url(r'^sort_products/(?P<id>\w+)$', views.sort_products),
    url(r'^front_productpage/show/(?P<id>\d+)$', views.front_productpage, name="product_page"),
    url(r'^front_productpage/buy/(?P<id>\d+)$', views.buy),
    url(r'^carts$', views.carts),
    url(r'^deletecart_item/(?P<key_id>\d+)$', views.deletecart_item),
    url(r'^checkout$', views.checkout),
    url(r'^billing_shipping$', views.billing_shipping),

    ########################## ADMIN #####################################
    url(r'^admin$', views.admin),
    url(r'^adminlogin$', views.adminlogin),
    url(r'^adminlogout$', views.adminlogout),

    ########################## DASHBOARD #####################################
    url(r'^dashboard/products$', views.products, name = 'products'), #TEMPLATE
    url(r'^dashboard/products/add$', views.products_add),
    url(r'^dashboard/products/search$', views.products_search),
    url(r'^dashboard/products/edit/(?P<id>\d+)$', views.products_edit),
    url(r'^dashboard/products/delete/(?P<id>\d+)$', views.products_delete),
    url(r'^dashboard/orders$', views.orders),
    url(r'^dashboard/orders/show/(?P<id>\d+)$', views.show_orders),
    url(r'^dashboard/orders/order_status/(?P<id>\d+)$', views.order_status),
]
