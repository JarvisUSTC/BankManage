# 引入path
from django.urls import path
from django.conf.urls import url
from . import views
# 正在部署的应用的名称
app_name = 'bmanage'

urlpatterns = [
    url(r'^hello/', views.login, name='login'),
    url(r'^cusadd/', views.customer_manage_add, name='cusadd'),
    url(r'^cusdel/', views.customer_manage_del, name='cusdel'),
    url(r'^cusmod/', views.customer_manage_mod, name='cusmod'),
    url(r'^cusfod/', views.customer_manage_found, name='cusfod'),
    url(r'^accadd/', views.account_add, name='accadd'),
    url(r'^accdel/', views.account_del, name='accdel'),
    url(r'^accmod/', views.account_mod, name='accmod'),
    url(r'^accfod/', views.account_found, name='accfod'),
    url(r'^loanadd/', views.loan_add, name='loanadd'),
    url(r'^loandel/', views.loan_del, name='loandel'),
    url(r'^loanfound/', views.loan_found, name='loanfound'),
    url(r'^loanissue$', views.loan_issue, name='loanissue'),
    url(r'^savestatistic$', views.save_statistics, name='savestatistic'),
    url(r'^loanstatistic$', views.loan_statistics, name='loanstatistic')
    # 目前还没有urls
]
