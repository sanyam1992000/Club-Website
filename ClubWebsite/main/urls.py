
from django.conf.urls import url,include
from django.contrib.auth.views import logout
from django.conf import settings
from .views import member_list_view,RegistrationAPIView,memberprofileview,nearestEventsAPIView,EventlistAPIView,myprofileview,getprofile_apiview,editprofileview,home,register,index,create_event,login_view,event_list_view,event_detailview

urlpatterns = [
    url(r'^$',home,name='home'),
    url(r'^member/(?P<username>[\w\-]+)/',memberprofileview,name="member-detail"),
    url(r'^api/events/$',EventlistAPIView.as_view(),name="get-eventslist"),
    url(r'^api/event/register/$',RegistrationAPIView.as_view(),name='event-register'),
    url(r'^api/nearevents/$',nearestEventsAPIView.as_view(),name="get-nearevents"),
    url(r'^home/$',index,name="index"),
    url(r'^members/$',member_list_view,name="members-list"),
    url(r'^register/$',register,name="register"),
    url(r'^create_event/$',create_event,name="add_event"),
    url(r'^login/$',login_view,name="login_view"),
    url(r'^events/$',event_list_view,name="events-list"),
    url(r'^profile/$',myprofileview,name="profile"),
    url(r'^api/getprofile/$',getprofile_apiview.as_view(),name="get-userprofile"),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^event/detail/(?P<pk>(\d+)+)/$',event_detailview,name="detailview-event"),
    url(r'^update_user/$',editprofileview,name="profile"),
]
