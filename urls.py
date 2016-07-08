from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SPM.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^spm$', 'SPM.views.SPM'),
    url(r'^spm_query$', 'SPM.views.SPM_Query'),
    url(r'^insp_query$', 'SPM.views.insp_query'),
    url(r'^insp$', 'SPM.views.insp'),
    url(r'^outsp$', 'SPM.views.outsp'),
    url(r'^queryspdata$', 'SPM.views.queryspdata'),
    url(r'^queryinspdata$', 'SPM.views.queryinspdata'),
    url(r'^queryrecorddata$', 'SPM.views.queryrecorddata'),
    url(r'^get_filter_data$', 'SPM.views.get_filter_data'),
    url(r'^reload_category$', 'SPM.views.reload_category'),
    url(r'^get_user_speciality$', 'SPM.views.get_user_speciality'),
    url(r'^get_speciality_category$', 'SPM.views.get_speciality_category'),
    url(r'^insert_database$', 'SPM.views.insert_database'),
    url(r'^out_database$', 'SPM.views.out_database'),
    url(r'^get_sp_data$', 'SPM.views.get_sp_data'),
    url(r'^read_excel$', 'SPM.views.read_excel'),
    url(r'^err_log$', 'SPM.views.err_log'),
    url(r'^logout$', 'SPM.views.logout_view'),
    url(r'^ttt$', 'SPM.views.ttt'),
   
    url(r'^manage_user$', 'SPM.views.Manage_User'),
    url(r'^manage_fac$', 'SPM.views.Manage_Fac'),
    url(r'^manage_cat$', 'SPM.views.Manage_Cat'),
    url(r'manage_org$', 'SPM.views.Manage_Org'),
    url(r'^get_org_data$', 'SPM.views.get_org_data'),
    url(r'^ods_spm_query$', 'SPM.views.ods_SPM_Query'),
    url(r'^out_org$', 'SPM.views.out_org'),
    url(r'^get_org_data_more$', 'SPM.views.get_org_data_more'),
    url(r'^out_org_common$', 'SPM.views.out_org_common'),
    url(r'^get_user_data', 'SPM.views.get_user_data'),
    url(r'^get_exa_user', 'SPM.views.get_exa_user'),
    url(r'^out_exa_user$', 'SPM.views.out_exa_user'),
    url(r'^get_common_org$', 'SPM.views.get_common_org'),
    url(r'^get_select_user_data$', 'SPM.views.get_select_user_data'),
    
    (r'^accounts/login/$', 'SPM.customauthentication.customlogin',{'template_name': 'spm/login.html'}),
)
handler404 = 'SPM.views.my_custom_page_not_found_view'
handler500 = 'SPM.views.my_custom_error_view'
