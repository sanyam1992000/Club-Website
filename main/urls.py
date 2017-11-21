
from django.conf.urls import url,include
from django.contrib.auth.views import logout
from django.conf import settings
from .views import dp_APIview,ProjectHostAPIView,change_password,contactus,project_list_view,add_project,eventfeedbacksView,FeedbackAPIView,edit_event,getevent_apiview,eventregistrationsView,editmemberprofileview,member_list_view,RegistrationAPIView,memberprofileview,nearestEventsAPIView,EventlistAPIView,getprofile_apiview,editprofileview,home,register,create_event,login_view,event_list_view,event_detailview

urlpatterns = [
    url(r'^$',home,name='home'),
    url(r'^member/(?P<username>[\w\-]+)/',memberprofileview,name="member-detail"),
    url(r'^api/events/$',EventlistAPIView.as_view(),name="get-eventslist"),
    url(r'^api/event/feedback/$',FeedbackAPIView.as_view(),name='event-feedback'),
    url(r'^api/event/register/$',RegistrationAPIView.as_view(),name='event-register'),
    url(r'^api/nearevents/$',nearestEventsAPIView.as_view(),name="get-nearevents"),
    url(r'^home/$',register,name="index"),
    url(r'^password/$',change_password, name='change_password'),
    url(r'^members/$',member_list_view,name="members-list"),
    url(r'^projects/$',project_list_view,name="project-list"),
    url(r'^add_project/$',add_project,name="add_project"),
    url(r'^create_event/$',create_event,name="add_event"),
    url(r'^login/$',login_view,name="login_view"),
    url(r'^events/$',event_list_view,name="events-list"),
    url(r'^profile/$',editprofileview,name="profile"),
    url(r'^event/(?P<pk>(\d+)+)/feedbacks/$',eventfeedbacksView,name="event-feedbacks"),
    url(r'^event/(?P<pk>(\d+)+)/registrations/$',eventregistrationsView,name="event_registration"),
    url(r'^api/getevent/$',getevent_apiview.as_view(),name="get-eventdetail"),
    url(r'^api/hosts/$',ProjectHostAPIView.as_view(),name="get-projecthosts"),
    url(r'^api/UpdateProfilePicture/$',dp_APIview.as_view(),name="post-dp"),
    url(r'^api/getprofile/$',getprofile_apiview.as_view(),name="get-userprofile"),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^event/detail/(?P<pk>(\d+)+)/$',event_detailview,name="detailview-event"),
    url(R'^update_event/$',edit_event,name="update_event"),
    url(r'^update_member/$',editmemberprofileview,name="update_member"),
    url(r'^contactus/$',contactus,name='contactus'),
]
