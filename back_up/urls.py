from django.urls import path

from back_up.views import index , repositoryClone ,webhookss

urlpatterns =[
  path('index/',index, name= 'index'),
  path('repositoryClone/',repositoryClone, name= 'repositoryClone'),
  path('<str:repository_name>/',webhookss, name= 'webhookss'),

]




#path('/',, name= ''),