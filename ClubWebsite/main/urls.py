
from django.conf.urls import url,include
from .views import myprofileview,getprofile_apiview,editprofileview,home,register,index,create_event,login_view,event_list_view,event_detailview

urlpatterns = [
    url(r'^$',home,name='home'),
    url(r'^home/$',index,name="index"),
    url(r'^register/$',register,name="register"),
    url(r'^create_event/$',create_event,name="add_event"),
    url(r'^login/$',login_view,name="login_view"),
    url(r'^events/$',event_list_view,name="events-list"),
    url(r'^profile/$',myprofileview,name="profile"),
    url(r'^api/getprofile/$',getprofile_apiview.as_view(),name="get-userprofile"),
    url(r'^event/detail/(?P<pk>(\d+)+)/$',event_detailview,name="detailview-event"),
]
