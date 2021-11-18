from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
	path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('user/logout/', views.logoutUser, name="logout"),
    path('user/prescription/logout/', views.logoutUser, name="logout"),
    path('user/prescription_allice_optic/logout', views.logoutUser, name="logout"),

    path('', views.home, name="home"),
    path('user/', views.userPage, name="user-page"),

    path('account/', views.accountSettings, name="account"),

    path('prescription/', views.prescription, name='prescription2'),
    path('user/prescription/', views.prescription, name='prescription2'),

##========== Upgradation for Alies Optics =====================================##
    path('prescription_alliance_optic/', views.prescription_allies_optic, name='prescription_allice_optics_yo'),
    path('user/prescription_alliance_optic/', views.prescription_allies_optic, name='prescription_allice_optics_yo'),
##========== Upgradation for Alies Optics =====================================##

##========== Upgradation for Alies Optics =====================================##
    path('api_cast_oci_Alise_optics/', views.Get_all_orders_by_oci_alies_optics, name="api-Overview_cast_oci_alise_optics"),
    path('user/api_cast_oci_Alise_optics/', views.Get_all_orders_by_oci_alies_optics, name="user_api-Overview_cast_oci_alise_optics"),
##========== Upgradation for Alies Optics =====================================##

    path('prescription/oci_print/', views.report, name='ociprint'),
    path('prescription_alliance_optic/ociprint_alliance_optic/', views.report_alliance_optic, name='ociprint1'),
    path('user/prescription/oci_print/', views.report, name='ociprint'),
    path('user/prescription_alliance_optic/ociprint_alliance_optic/', views.report_alliance_optic, name='ociprint1'),

    path('products/', views.products, name='products'),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('ploat_data/', views.Ploting_data, name='plotdata'),

    path('create_order/<str:pk>/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order"),

    path('api/', views.Get_all_orders, name="api-Overview"),
    path('api_cast/', views.Get_all_orders_by_customer, name="api-Overview_cast"),
    path('api_cast_oci/', views.Get_all_orders_by_oci, name="api-Overview_cast_oci"),
    path('user/api_cast_oci/', views.Get_all_orders_by_oci, name="user_api-Overview_cast_oci"),

    # path('api_cast_cdrff/', views.Get_all_orders_by_refno, name="api-Overview_cast_oci"),
    # path('user/api_cast_cdrff/', views.Get_all_orders_by_refno, name="user_api-Overview_cast_oci"),

    # anirudha =============================
    path('api_cast_cdrff/', views.Get_all_orders_by_refno_oci, name="api-Overview_cast_oci"),
    path('user/api_cast_cdrff/', views.Get_all_orders_by_refno_oci, name="user_api-Overview_cast_oci"),

    path('api_cast_by_date/', views.Get_all_orders_by_entry_date, name="api-Overview_cast_oci_ed"),
    path('user/api_cast_by_date/', views.Get_all_orders_by_entry_date, name="user_api-Overview_cast_oci_ed"),

    path('api_cast_filter_date/', views.Get_all_orders_filter_by_date, name="api-Overview_cast_filter_date"),
    path('user/api_cast_filter_date/', views.Get_all_orders_filter_by_date, name="user_api-Overview_cast_filter_date"),

    path('api_cast_filter_ref_on/', views.Get_all_orders_filter_ref_no, name="api-Overview_cast_filter_ref_no"),
    path('user/api_cast_filter_ref_no/', views.Get_all_orders_filter_ref_no, name="user_api-Overview_cast_filter_ref_no"),

    #anirudha===========================
    path('api_year_month/', views.year_histry, name="api-year-month"),
    path('user/api_year_month/', views.year_histry, name="user_api-year-month"),
    # =============

    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
        name="reset_password"),
    
        path('login/reset_password/',
        auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
        name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
        name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),

        # ============================================ Api for LAB USER ================================
    path('dashboard_oci/', views.Get_all_orders_by_dashboard_oci_vrx_internal, name='Dashboard'),

    path('dashboard_ref/', views.Get_all_orders_by_dashboard_ref_vrx_internal, name='Dashboard_1'),

    path('prescription_labs/', views.prescription_labs, name='prescription'),

    path('api_cast_oci_lab/', views.Get_all_orders_by_oci_vrx_internal, name='priscription'),

    path('shape_text/', views.shape_text,name='shape_text'),
    path('user/prescription_allice_optic/shape_text/', views.shape_text,name='shape_text'),

    path('report_Download/', views.Lens_report_Api, name="api-report-Get"),
    path('user/report_Download/', views.Lens_report_Api, name="user_api-report-Get"),

]