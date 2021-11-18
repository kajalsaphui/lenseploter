import io
from logging import NullHandler
import locale
import re
from typing import IO
from django.http import response
from django.views.decorators.csrf import ensure_csrf_cookie
import pdfkit
from django.http.response import JsonResponse
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
from fpdf import FPDF, HTMLMixin
from django_xhtml2pdf.utils import generate_pdf
# import cStringIO as StringIO
from xhtml2pdf import pisa
from django.template.loader import get_template, render_to_string
from django.template import Context
from django.http import HttpResponse
from cgi import escape

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm,CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user,allowed_users,admin_only

from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.response import Response
from . import DB_Transactions
import pyodbc
from . import Defaults
from . import plotter
import json
from rest_framework.parsers import JSONParser
from .serializers import YourSerializer
import csv


@unauthenticated_user
def registerPage(request):

	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			messages.success(request, 'Account was created for ' + username)

			return redirect('login')
		

	context = {'form':form}
	return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
	
	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.info(request, 'Username OR password is incorrect')

	# context = {}
	return render(request, 'accounts/login.html')

def logoutUser(request):
	logout(request)
	return redirect('login')




@login_required(login_url='login')
@admin_only
def home(request):
    # items  = []
    # resp = DB_Transactions.get_all_orders()
    # for row in resp:
    #     items.append({'customer_code': row[0], 'Application_name': row[1], 'order_nuber' : row[2], 'oci_no' : row[3], 'cast_name' : row[4],'order_date' : row[4]})
    # disc = {"status": "Success", "result":{"Node":items}}
    # # return Response(disc )


    # orders = Order.objects.all()
    # customers = Customer.objects.all()

    # total_customers = customers.count()

    # total_orders = orders.count()
    # delivered = orders.filter(status='Delivered').count()
    # pending = orders.filter(status='Pending').count()

    # context = {'orders':orders, 'customers':customers,
    # 'total_orders':total_orders,'delivered':delivered,
    # 'pending':pending }

    return render(request, 'accounts/dashboard.html')
    # return render(request, 'accounts/dashboard2.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
	
	
	orders = request.user.customer.order_set.all()
	print("orders",orders)
	castomer=Customer.objects.filter(user=request.user).first()
	# email =Customer.objects.email.filter(castomer_code=castomer_cd) 
	# castomer_email =request.user.customer.email()
	# cast_email = castomer.email
	# username =castomer.User
	# application_name = castomer.application_name
	# print(cast_email)
	print(castomer)
	user = castomer.user_name
	email= castomer.email
	# total_orders = orders.count()
	# delivered = orders.filter(status='Delivered').count()
	# pending = orders.filter(status='Pending').count()

	# print('ORDERS:', orders)

	# context = {'Application_name':application_name, 'email':cast_email}
	# 'delivered':delivered,'pending':pending}
	return render(request, 'accounts/user.html')

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == 'POST':
		form = CustomerForm(request.POST, request.FILES,instance=customer)
		if form.is_valid():
			form.save()


	context = {'form':form}
	return render(request, 'accounts/account_settings.html', context)
	

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()

	return render(request, 'accounts/products.html', {'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
	customer = Customer.objects.get(id=pk_test)

	orders = customer.order_set.all()
	order_count = orders.count()

	# myFilter = OrderFilter(request.GET, queryset=orders)
	# orders = myFilter.qs 

	context = {'customer':customer}
	return render(request, 'accounts/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method ==  'POST':
		#print('Printing POST:', request.POST)
		form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)

@api_view(['GET'])
@login_required(login_url='login')
def Get_all_orders(request):
    items  = []
    resp = DB_Transactions.get_all_orders()
    for row in resp:
        items.append({'customer_code': row[0], 'Application_name': row[1], 'order_nuber' : row[2], 'oci_no' : row[3], 'cast_name' : row[4],'order_date' : row[5]})
    disc = {"status": "Success", "result":{"Node":items}}
    return Response(disc )

@api_view(['GET'])
@allowed_users(allowed_roles=['customer'])
def Get_all_orders_by_customer(request):
    # castomer= Customer.objects.filter(username=username).first()
    castomer=Customer.objects.filter(user=request.user).first()
    cast_cd = castomer.castomer_code
    user = castomer.user_name
    email= castomer.email
    # user='anirudha'
    # email = 'ani@gmail.com'
    # cast_cd ="DB_396"
    print("cast_cd",cast_cd)
    
    items  = []
    resp = DB_Transactions.get_all_orders_by_castomer(cast_cd)
    for row in resp:
        items.append({'customer_code': row[0], 'Application_name': row[1], 'order_nuber' : row[2], 'oci_no' : row[3], 'cast_name' : row[4],'order_date' : row[5]})
    disc = {"status": "Success", "result":{"Node":items},'username':user,'email':email}
	# disc = {"status": "Success", "result":{"Node":items},'username':user,'email':email}
    print(disc)
    return Response(disc )
    # return None

@api_view(['POST'])
@allowed_users(allowed_roles=['customer'])
@ensure_csrf_cookie
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def Get_all_orders_by_oci(request):
    if request.method == 'POST':
        castomer=Customer.objects.filter(user=request.user).first()
        cast_cd = castomer.castomer_code
        user = castomer.user_name
        email= castomer.email
		# image_data =''
		# data = request.body.decode('utf-8')
		# data = JSONParser().parse(request)
        oci_no =request.data.get("oci_no")
        print(oci_no)
		# try:
		#image_data = Ploting_data(oci_no)
		# except:Device and server Communication through HTTPS protocolDevice and server Communication through HTTPS protocolDevice and server Communication through HTTPS protocolDevice and server Communication through HTTPS protocol
		# 	print("failour")
		# oci_no=json.loads(request.body[data])
		# oci_no=request.data('oci_no')
		# oci_no = request.form
		# print ("data",data)
		# NON_TRACER_data =DB_Transactions.get_tracevalue(oci_no)
		# print("tracevalue",NON_TRACER_data)
        db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+Defaults.host_ms+';DATABASE='+Defaults.schema_ms+';UID='+Defaults.user_ms+';PWD='+ Defaults.password_ms)
        cursor = db.cursor()
		# items  = []
        try:
            sql = """\
            EXEC SP_WEBSHOP_ORDER_SERARCHING @OCINUMBER=?, @CUSTCODE=?,@ORDERNUMBER=?,@ORDERDATE=? 
            """
            params = (oci_no,'','','')
            cursor.execute(sql, params)
			# print(cursor.execute(sql, params))
			# cursor.execute('[dbo].[SP_WEBSHOP_ORDER_SERARCHING] @OCINUMBER=%s,@CUSTCODE=%s,@ORDERNUMBER=%s,@ORDERDATE=%s',(oci_no,'','',''))
			# cursor.execute("{call SP_WEBSHOP_ORDER_SERARCHING(oci_no,'','','')}")
			# if cursor.return_value==1:
            result = cursor.fetchall()
			# result = result1[0][0].split()
            print("result",result)
        finally:
            cursor.close()
        # disc = {"data":result}
        print("result",result)
        for row in result:
            items= {'CUSTCODE':row[0],'REFNUMBER':row[1],'PATIENTFIRSTNAME':row[2],'PATIENTLASTNAME':row[3],'PATIENTADDRESS1':row[4],'PATIENTADDRESS2':row[5],'PATIENTCITY':row[6],'PATIENTCOUNTRY':row[7],'RECODE':row[8],'REDESC':row[9],'RECOMMDIA':row[10],'REQTY':row[11],'RESPHERE':row[12],'RECYLINDER':row[13],'READDITION':row[14],'REAXIS':row[15],'REREQDIA':row[16],'REBASE':row[17],'RECT':row[18],'REET':row[19],'REPRISM1':row[20],'REPRISM1DIA':row[21],'REPRISM2':row[22],'REPRISM2DIA':row[23],'REHEIGHT':row[24],'REPD':row[25],'RENPD':row[26],'LECODE':row[27],'LEDESC':row[28],'LECOMMDIA':row[29],'LEQTY':row[30],'LESPHERE':row[31],'LECYLINDER':row[32],'LEADDITION':row[33],'LEAXIS':row[34],'LEREQDIA':row[35],'LEBASE':row[36],'LECT':row[37],'LEET':row[38],'LEPRISM1':row[39],'LEPRISM1DIA':row[40],'LEPRISM2':row[41],'LEPRISM2DIA':row[42],'LEHEIGHT':row[43],'LEPD':row[44],'LENPD':row[45],'COATINGCOADE':row[46],'COATINGDESC':row[47],'TINTCOADE':row[48],'TINTDESC':row[49],'BOXA':row[50],'BOXB':row[51],'DBL':row[52],'FRAMETYPE':row[53],'ORDERDATE':row[54],'OCINUMBER':row[55],'VERTEXDIST':row[56],'WRAPANGLE':row[57],'PANTOANGLE':row[58],'SPLINSTRUCTION':row[59],'OMADATA':row[60],'EDGINGTYPE':row[61],'FRAMECODE':row[62],'FRAMEDESC':row[63]}
        # disc = {"status": "Success", "result":{"Node":items},"shape":image_data}
        disc = {"status": "Success", "result":{"Node":items},'username':user,'email':email}
        print("final disc:",disc)
        return JsonResponse(disc)
        # return None
    # return render(request, 'accounts/prescription2.html')

##========== Upgradation for Alies Optics =====================================##
@api_view(['POST'])
@allowed_users(allowed_roles=['customer'])
@ensure_csrf_cookie
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def Get_all_orders_by_oci_alies_optics(request):
    if request.method == 'POST':
        castomer=Customer.objects.filter(user=request.user).first()
        cast_cd = castomer.castomer_code
        user = castomer.user_name
        email= castomer.email
        oci_no =request.data.get("oci_no")
        print(oci_no)
        db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+Defaults.host_ms+';DATABASE='+Defaults.schema_ms+';UID='+Defaults.user_ms+';PWD='+ Defaults.password_ms)
        cursor = db.cursor()
		# items  = []
        try:
            sql = """\
            EXEC SP_WEBSHOP_ORDER_SERARCHING_ALISE_OPTICS @OCINUMBER=?, @CUSTCODE=?,@ORDERNUMBER=?,@ORDERDATE=? 
            """
            params = (oci_no,'','','')
            cursor.execute(sql, params)
            result = cursor.fetchall()
            print("result",result)
        finally:
            cursor.close()
        # disc = {"data":result}
        print("result",result)
        for row in result:
            items= {'CUSTCODE':row[0],'REFNUMBER':row[1],'PATIENTFIRSTNAME':row[2],'PATIENTLASTNAME':row[3],'PATIENTADDRESS1':row[4],'PATIENTADDRESS2':row[5],'PATIENTCITY':row[6],'PATIENTCOUNTRY':row[7],'RECODE':row[8],'REDESC':row[9],'RECOMMDIA':row[10],'REQTY':row[11],'RESPHERE':row[12],'RECYLINDER':row[13],'READDITION':row[14],'REAXIS':row[15],'REREQDIA':row[16],'REBASE':row[17],'RECT':row[18],'REET':row[19],'REPRISM1':row[20],'REPRISM1DIA':row[21],'REPRISM2':row[22],'REPRISM2DIA':row[23],'REHEIGHT':row[24],'REPD':row[25],'RENPD':row[26],'LECODE':row[27],'LEDESC':row[28],'LECOMMDIA':row[29],'LEQTY':row[30],'LESPHERE':row[31],'LECYLINDER':row[32],'LEADDITION':row[33],'LEAXIS':row[34],'LEREQDIA':row[35],'LEBASE':row[36],'LECT':row[37],'LEET':row[38],'LEPRISM1':row[39],'LEPRISM1DIA':row[40],'LEPRISM2':row[41],'LEPRISM2DIA':row[42],'LEHEIGHT':row[43],'LEPD':row[44],'LENPD':row[45],'COATINGCOADE':row[46],'COATINGDESC':row[47],'TINTCOADE':row[48],'TINTDESC':row[49],'BOXA':row[50],'BOXB':row[51],'DBL':row[52],'FRAMETYPE':row[53],'ORDERDATE':row[54],'OCINUMBER':row[55],'VERTEXDIST':row[56],'WRAPANGLE':row[57],'PANTOANGLE':row[58],'SPLINSTRUCTION':row[59],'OMADATA':row[60],'EDGINGTYPE':row[61],'FRAMECODE':row[62],'FRAMEDESC':row[63],'ACTUAL_LEFT_Lense_DESC':row[65],'ACTUAL_RIGHT_Lense_DESC':row[66],'ACTUAL_COARTING_DESC':row[67],'ACTUAL_TINTING_DESC':row[68]}
        # disc = {"status": "Success", "result":{"Node":items},"shape":image_data}
        disc = {"status": "Success", "result":{"Node":items},'username':user,'email':email}
        print("final disc:",disc)
        return JsonResponse(disc)


##========== Upgradation for Alies Optics =====================================##


# anirudha=====================
@api_view(['POST'])
@allowed_users(allowed_roles=['customer'])
# @csrf_exempt
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def Get_all_orders_by_refno_oci(request):
    if request.method == 'POST':
        oci_no =request.data.get("oci_no")
        castomer=Customer.objects.filter(user=request.user).first()
        customer_code = castomer.castomer_code
        print(oci_no)
        print(customer_code)
        items  = []
        resp = DB_Transactions.get_all_orders_by_oci_castomer(oci_no,customer_code)
        for row in resp:
            items.append({'customer_code': row[0], 'Application_name': row[1], 'order_nuber' : row[2], 'oci_no' : row[3], 'cast_name' : row[4],'order_date' : row[5]})
        disc = {"status": "Success", "result":{"Node":items}}
        print(disc)
        return Response(disc )

@api_view(['POST'])
@allowed_users(allowed_roles=['customer'])
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def Get_all_orders_by_entry_date(request):
    if request.method == 'POST':
        Entrydate =request.data.get("entry_date")
        # Entrydate_end =request.data.get("entry_date_end")
        castomer=Customer.objects.filter(user=request.user).first()
        customer_code = castomer.castomer_code
        Entrydate = Entrydate.split('-')
        ED_year = Entrydate[2]
        ED_month = Entrydate[1]
        ED_day = Entrydate[0]
        print(ED_year)
        print(ED_month)
        print(ED_day)
        items  = []
        resp = DB_Transactions.get_all_orders_by_oci_entrydate(ED_day,ED_month,ED_year,customer_code)
        for row in resp:
            items.append({'customer_code': row[0], 'Application_name': row[1], 'order_nuber' : row[2], 'oci_no' : row[3], 'cast_name' : row[4],'order_date' : row[5]})
        disc = {"status": "Success", "result":{"Node":items}}
        print(disc)
        return Response(disc )

@api_view(['POST'])
@allowed_users(allowed_roles=['customer'])
@csrf_exempt
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def Get_all_orders_filter_by_date(request):
    if request.method == 'POST':
        Entrydate =request.data.get("entry_date")
        castomer=Customer.objects.filter(user=request.user).first()
        customer_code = castomer.castomer_code
        print(Entrydate)
        Entrydate = Entrydate.split('-')
        ED_year = Entrydate[0]
        ED_Month = Entrydate[1]
        print(customer_code)
        items  = []
        resp = DB_Transactions.get_all_orders_filter_by_entrydate(ED_year,ED_Month,customer_code)
        for row in resp:
            items.append({'customer_code': row[0], 'Application_name': row[1], 'order_nuber' : row[2], 'oci_no' : row[3], 'cast_name' : row[4],'order_date' : row[5]})
        disc = {"status": "Success", "result":{"Node":items}}
        # print("dinary data",disc)
        return JsonResponse(disc )

@api_view(['POST'])
@allowed_users(allowed_roles=['customer'])
# @csrf_exempt
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def Get_all_orders_filter_ref_no(request):
    if request.method == 'POST':
        ref_no =request.data.get("ref_no")
        castomer=Customer.objects.filter(user=request.user).first()
        customer_code = castomer.castomer_code
        print(ref_no)
        print(customer_code)
        items  = []
        resp = DB_Transactions.get_all_orders_filter_by_ref_no_val(ref_no,customer_code)
        for row in resp:
            items.append({'customer_code': row[0], 'Application_name': row[1], 'order_nuber' : row[2], 'oci_no' : row[3], 'cast_name' : row[4],'order_date' : row[5]})
        disc = {"status": "Success", "result":{"Node":items}}
        print(disc)
        return Response(disc )


		
# anirudha==========================================================================



@api_view(['POST'])
# @csrf_exempt
def Ploting_data(request):
	# data = JSONParser().parse(request)
	# oci_no =data.get("oci_no")
	oci_no =request.data.get("oci_no")
	NON_TRACER_data =DB_Transactions.get_tracevalue(oci_no)
	print("tested_data",NON_TRACER_data)
	lsdata = NON_TRACER_data[0][0].split()
	trcfmt = lsdata[0]
	del lsdata[0]
	type=lsdata[0]
	del lsdata[0]
	ln = len(lsdata)
	red, angle = ([] for i in range(2))
	for i in range(ln):
		tsdata = lsdata[i].split('=')
		if(tsdata[0] == 'R'):
			del tsdata[0]
			vals = tsdata[0].split(';')
			[red.append(int(x)) for x in vals]
			len2 = len(red)
		elif(tsdata[0] == 'A'):
			del tsdata[0]
			vals = tsdata[0].split(';')
			[angle.append(int(x)/100) for x in vals]
		# else:
			# first_angle = 360/len2
			# incriment = 360/len2
			# print(incriment)
			# print(first_angle)
			# angle = [range(first_angle,len2,incriment)]



	print(red)
	print(angle)
	last_angle = angle[0]
	last_red = red[0]
	print(int(last_red))
	print(int(last_angle))
	red.append(last_red)
	angle.append(last_angle)
	print("final_red",red)
	print("final_angle",angle)	

	response = plotter.plot_data(red,angle)

	print("response_final",response)
	disc = {"status": "Success","shape":response}
	# return response
	return JsonResponse(disc)
	# return immage file after ploting




@api_view(['GET'])
def prescription(request):

    return render(request, 'accounts/prescription2.html')

@api_view(['GET'])
def prescription_allies_optic(request):

    return render(request, 'accounts/prescription_alliance.html')

@api_view(['GET'])
def report(request):
	# tem = render(request,'accounts/ociprint.html')
	# template = get_template('accounts/ociprint.html')
	# html  = template.render()
	# result = io.BytesIO()
	# pdf = pisa.pisaDocument(io.BytesIO(html.encode("utf-8")), result, encoding='UTF-8')
	# if pdf:

	# # return HttpResponse(result.getvalue(), content_type='application/pdf')
	# # response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
	# # response['Content-Type'] = 'application/pdf'
	return render(request,'accounts/ociprint.html')
	# # pdf = render_to_pdf(tem)
	# 	return HttpResponse(result.getvalue(), mimetype='application/pdf')
	# return response

@api_view(['GET'])
def report_alliance_optic(request):
    return render(request,'accounts/ociprint_alliance_optic.html')

# ==========aniruha ====== 20 july =============
@api_view(['GET','POST'])
# @allowed_users(allowed_roles=['customer'])
def year_histry(request):
	# castomer=Customer.objects.filter(user=request.user).first()
	# print(castomer)
	# customer_code = castomer.castomer_code
	customer_code = 'DB_396'
	if request.method == 'POST':
		year =request.data.get("year_data")
		resp = DB_Transactions.get_month_by_year(year,customer_code)
		items= []
		for row in resp:
			items.append({"Month":row[0]})
		disc = {"status": "Success", "result":{"Node":items}}
		print(disc)
		return Response(disc )
	resp = DB_Transactions.get_all_year_history(customer_code)
	for row in resp:
		items = {"Year":row[0]}
	disc = {"status": "Success", "result":{"Node":items}}
	return Response(disc )




#===============================================





# def render_to_pdf(template_src):
#     template = get_template(template_src)
#     # context = Context(context_dict)
#     html  = template.render()
#     result = io.BytesIO()

#     pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type='application/pdf')
#     return None

# class HtmlPdf(FPDF, HTMLMixin):
#     pass
# @api_view(['GET'])
# def report(request):    
#     pdf = HtmlPdf()
#     pdf.add_page()
	
#     pdf.write_html(render_to_string('accounts/ociprint.html'))

#     response = HttpResponse(pdf.output(dest='S').encode('latin-1'))
#     response['Content-Type'] = 'application/pdf'

#     return response
# @api_view(['GET'])
# def report(request):
#     # resp = HttpResponse(content_type='application/pdf')
#     # # dynamic_variable = request.user.some_special_something
#     # # context = {'some_context_variable':dynamic_variable}
#     # # tem = render(request,'accounts/ociprint.html')
#     # result = generate_pdf('accounts/ociprint.html', file_object=resp)
#     result  = pdfkit.from_file(['accounts/ociprint.html'], 'out.pdf')
#     return result

#####========================= Api for Production================================########
@api_view(['GET'])
def prescription_labs(request):

    return render(request, 'accounts/priscription.htm')


@api_view(['POST'])
@allowed_users(allowed_roles=['admin'])
@ensure_csrf_cookie
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def Get_all_orders_by_oci_vrx_internal(request):
    if request.method == 'POST':
        cust_code =request.data.get("cust_code")
        oci_no =request.data.get("oci_no")
        print(cust_code)
        print(oci_no) 
        sql_RxNetOrder = """\
        EXEC SP_WEBSHOP_ORDER_SERARCHING_ON_RXNETORDER @OCINUMBER=?, @CUSTCODE=?,@ORDERNUMBER=?,@ORDERDATE=? 
        """

        sql_NewRxOrder = """\
        EXEC SP_WEBSHOP_ORDER_SERARCHING_NEWRXORDER @OCINUMBER=?, @CUSTCODE=?,@ORDERNUMBER=?,@ORDERDATE=? 
        """

        sql_optileks = """\
        EXEC SP_WEBSHOP_ORDER_SERARCHING_OPTILEKS @OCINUMBER=?, @CUSTCODE=?,@ORDERNUMBER=?,@ORDERDATE=? 
        """
        sql_essaustriaorders = """\
        EXEC SP_WEBSHOP_ORDER_SERARCHING_ESSAUSTRIAORDERS @OCINUMBER=?, @CUSTCODE=?,@ORDERNUMBER=?,@ORDERDATE=? 
        """
        sql_OPHTHALMICFRANCE = """\
        EXEC SP_WEBSHOP_ORDER_SERARCHING_OPTHALMICFRANCE @OCINUMBER=?, @CUSTCODE=?,@ORDERNUMBER=?,@ORDERDATE=? 
        """
        sql_RxNetOrder_Ocuco = """\
        EXEC SP_WEBSHOP_ORDER_SERARCHING @OCINUMBER=?, @CUSTCODE=?,@ORDERNUMBER=?,@ORDERDATE=? 
        """
        #image_data = Ploting_data(oci_no)
        data = master.objects.filter(Cust_code = cust_code).first()
        table_name = data.Table_name
        print(table_name)
        db = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+Defaults.host_ms+';DATABASE='+Defaults.schema_ms+';UID='+Defaults.user_ms+';PWD='+ Defaults.password_ms)
        cursor = db.cursor()
        # items  = []
        try:
            if table_name == 'RxNetOrder':
                sql = sql_RxNetOrder 
                params = (oci_no,'','','')
                cursor.execute(sql, params)
                result = cursor.fetchall()
                print("result",result)
                print('sql:',sql)
                if result == '':
                    sql = sql_RxNetOrder_Ocuco
                    print('sql:',sql) 
            elif table_name == 'NewRxOrder':
                sql = sql_NewRxOrder 
                params = (oci_no,'','','')
                cursor.execute(sql, params)
                result = cursor.fetchall()
                print("result",result)
                print('sql:',sql)
            elif table_name == 'optileks':
                sql = sql_optileks 
                params = (oci_no,'','','')
                cursor.execute(sql, params)
                result = cursor.fetchall()
                print("result",result)
                print('sql:',sql)
            elif table_name == 'essaustriaorders':
                sql = sql_essaustriaorders 
                params = (oci_no,'','','')
                cursor.execute(sql, params)
                result = cursor.fetchall()
                print("result",result)
                print('sql:',sql)
            elif table_name == 'OPHTHALMICFRANCE':
                sql = sql_OPHTHALMICFRANCE 
                params = (oci_no,'','','')
                cursor.execute(sql, params)
                result = cursor.fetchall()
                print("result",result)
                print('sql:',sql)
            elif table_name == 'RxNetOrder_Ocuco':
                sql = sql_RxNetOrder_Ocuco 
                params = (oci_no,'','','')
                cursor.execute(sql, params)
                result = cursor.fetchall()
                print("result",result)
                print('sql:',sql)
        finally:
            cursor.close()
        # disc = {"data":result}
        print("result",result)
        for row in result:
            items= {'CUSTCODE':row[0],'REFNUMBER':row[1],'PATIENTFIRSTNAME':row[2],'PATIENTLASTNAME':row[3],'PATIENTADDRESS1':row[4],'PATIENTADDRESS2':row[5],'PATIENTCITY':row[6],'PATIENTCOUNTRY':row[7],'RECODE':row[8],'REDESC':row[9],'RECOMMDIA':row[10],'REQTY':row[11],'RESPHERE':row[12],'RECYLINDER':row[13],'READDITION':row[14],'REAXIS':row[15],'REREQDIA':row[16],'REBASE':row[17],'RECT':row[18],'REET':row[19],'REPRISM1':row[20],'REPRISM1DIA':row[21],'REPRISM2':row[22],'REPRISM2DIA':row[23],'REHEIGHT':row[24],'REPD':row[25],'RENPD':row[26],'LECODE':row[27],'LEDESC':row[28],'LECOMMDIA':row[29],'LEQTY':row[30],'LESPHERE':row[31],'LECYLINDER':row[32],'LEADDITION':row[33],'LEAXIS':row[34],'LEREQDIA':row[35],'LEBASE':row[36],'LECT':row[37],'LEET':row[38],'LEPRISM1':row[39],'LEPRISM1DIA':row[40],'LEPRISM2':row[41],'LEPRISM2DIA':row[42],'LEHEIGHT':row[43],'LEPD':row[44],'LENPD':row[45],'COATINGCOADE':row[46],'COATINGDESC':row[47],'TINTCOADE':row[48],'TINTDESC':row[49],'BOXA':row[50],'BOXB':row[51],'DBL':row[52],'FRAMETYPE':row[53],'ORDERDATE':row[54],'OCINUMBER':row[55],'VERTEXDIST':row[56],'WRAPANGLE':row[57],'PANTOANGLE':row[58],'SPLINSTRUCTION':row[59],'OMADATA':row[60],'EDGINGTYPE':row[61],'FRAMECODE':row[62],'FRAMEDESC':row[63]}
        # disc = {"status": "Success", "result":{"Node":items},"shape":image_data}
        disc = {"status": "Success", "result":{"Node":items}}
        print("final disc:",disc)
        return JsonResponse(disc)


@api_view(['POST'])
@allowed_users(allowed_roles=['admin'])
# @csrf_exempt
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def Get_all_orders_by_dashboard_oci_vrx_internal(request):
    if request.method == 'POST':
        oci_no =request.data.get("oci_no")
        rf_customer_code = request.data.get("rf_customer_code")
        print(rf_customer_code)
        data = master.objects.filter(Ref_cust_code = rf_customer_code).first()
        table_name = data.Table_name
        print(table_name)
        items  = []
        resp = DB_Transactions.get_all_orders_by_oci_vrx_labworker(table_name,oci_no)
        for row in resp:
            items.append({'customer_code': row[0], 'Application_name': row[1], 'order_nuber' : row[2], 'oci_no' : row[3], 'cast_name' : row[4],'order_date' : row[5]})
        disc = {"status": "Success", "result":{"Node":items}}
        print(disc)
        return Response(disc )

@api_view(['POST'])
@allowed_users(allowed_roles=['admin'])
# @csrf_exempt
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def Get_all_orders_by_dashboard_ref_vrx_internal(request):
    if request.method == 'POST':
        ref_no =request.data.get("ref_no")
        rf_customer_code = request.data.get("rf_customer_code")
        print(rf_customer_code)
        table_name =DB_Transactions.Cridential_mapping_vrxlab_ref_cast_code(rf_customer_code)
        print(table_name)
        items  = []
        resp = DB_Transactions.get_all_orders_by_ref_vrx_labworker(table_name,ref_no)
        for row in resp:
            items.append({'customer_code': row[0], 'Application_name': row[1], 'order_nuber' : row[2], 'oci_no' : row[3], 'cast_name' : row[4],'order_date' : row[5]})
        disc = {"status": "Success", "result":{"Node":items}}
        print(disc)
        return Response("discnary",disc )


# @api_view(['POST'])
# @allowed_users(allowed_roles=['customer'])
# # @csrf_exempt
# @renderer_classes((TemplateHTMLRenderer, JSONRenderer))
# def Get_all_orders_by_dashboard_entrydate_vrx_internal(request):
#     if request.method == 'POST':
#         entry_date =request.data.get("entry_date")
#         rf_customer_code = request.data.get("rf_customer_code")
#         print(rf_customer_code)
#         table_name =DB_Transactions.Cridential_mapping_vrxlab_ref_cast_code(rf_customer_code)
#         print(table_name)
#         items  = []
#         resp = DB_Transactions.get_all_orders_by_ref_vrx_labworker(table_name,entry_date)
#         for row in resp:
#             items.append({'customer_code': row[0], 'Application_name': row[1], 'order_nuber' : row[2], 'oci_no' : row[3], 'cast_name' : row[4],'order_date' : row[5]})
#         disc = {"status": "Success", "result":{"Node":items}}
#         print(disc)
#         return Response(disc )

# genarate text file ######## for Allice Optics##############
@api_view(['POST'])
# @api_view(['GET'])
# @allowed_users(allowed_roles=['customer'])
def shape_text(request):
    oci_no = request.data.get("oci_no")
    print("oci-no:-",oci_no)
    # response = HttpResponse(content_type='application/octet-stream')
    # response = HttpResponse(content_type='text/plain')
    # response['Content-Disposition'] = 'attachment; filename = test.txt'

    # lines = ["this is line one\n",
    #         "this is line Tow\n",
    #         "this is line Three\n"
    # ]
    # items = []
    lines =  DB_Transactions.get_OMA_DATA(oci_no)
    print(lines[0][0])
    if lines[0][0] == None:
        print("in if condition")
        lines =  DB_Transactions.get_NON_TRACE_DATA(oci_no) 
    for row in lines:

        items =row[0]
    # lines =  DB_Transactions.get_OMA_DATA()
    # for items in lines:
    #     response.writelines(items)
    #     response.writelines("\n")
    # print(response)
    json1= {"key":items}
    print (json1)
    return JsonResponse(json1)

@api_view(['POST'])
@allowed_users(allowed_roles=['customer'])
def Lens_report_Api(request):
    castomer=Customer.objects.filter(user=request.user).first()
    customer_code = castomer.castomer_code
    Entrydate =request.data.get("entry_date")
    Exitdate =request.data.get("exit_date")
    print("entry_date",Entrydate)
    print("exit_date",Exitdate)
    Entrydate = Entrydate.split('-')
    ED_year = Entrydate[2]
    ED_month = Entrydate[1]
    ED_day = Entrydate[0]
    Exitdate = Exitdate.split('-')
    ED_year_to = Exitdate[2]
    ED_month_to = Exitdate[1]
    ED_day_to = Exitdate[0]
    result = DB_Transactions.get_all_orders_report_entrydate(ED_day,ED_month,ED_year,ED_day_to,ED_month_to,ED_year_to,customer_code)
    result = list(result)
    print(result)
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename=ThePythonDjango.csv'
    

    writer = csv.writer(response)
    writer.writerow(['ORDERDATE','OCINUMBER','CUSTCODE','REFNUMBER','RECODE','REREFINDEX','REFOCALITY','RELENSMAT','RE_PRODUCT_DESCRIPTION','RECOMMDIA','REREQDIA','RESPHERE','RECYLINDER','REAXIS','READDITION','REQTY','REBASE','RECT','REET','REPRISM1','REPRISM1DIA','REPRISM2','REPRISM2DIA','REPD','RENPD','REHEIGHT','LECODE','LEREFINDEX','LEFOCALITY','LELENSMAT','LE_PRODUCT_DESCRIPTION','LECOMMDIA','LEREQDIA','LESPHERE','LECYLINDER','LEAXIS','LEADDITION','LEQTY','LEBASE','LECT','LEET','LEPRISM1','LEPRISM1DIA','LEPRISM2','LEPRISM2DIA','LEPD','LENPD','LEHEIGHT','COATINGCOADE','COATINGDESC', 'TINTCOADE','TINTDESC','BOXA','BOXB','DBL','FRAMETYPE','VERTEXDIST','WRAPANGLE','PANTOANGLE','SPLINSTRUCTION','EDGINGTYPE']) 
   
    for row in result:
        row1 = DB_Transactions.get_Extra_DATA_Axcepta(row.OCINUMBER)
        # print("totaldata",row1)
        row1 = list(row1[0])
        # print(row1)
        # print(row1[8])
        if row1[8] == 0:
            row1[8]='Single Vision'
        else:
            row1[8]='Multi Focal'
        # print(row1[2])
        if row1[2] == 0:
            row1[2]='Single Vision'
        else:
            row1[2]='Multi focal'
        # print(row1[4])
        # print(row1[5])
        writer.writerow([row.ORDERDATE,row.OCINUMBER,row.CUSTCODE,row.REFNUMBER,row.RECODE,row1[7],row1[8],row1[9],row1[10],row.RECOMMDIA,row.REREQDIA,row.RESPHERE,row.RECYLINDER,row.REAXIS,row.READDITION,row.REQTY,row.REBASE,row.RECT,row.REET,row.REPRISM1,row.REPRISM1DIA,row.REPRISM2,row.REPRISM2DIA,row.REPD,row.RENPD,row.REHEIGHT,row.LECODE,row1[1],row1[2],row1[3],row1[4], row.LECOMMDIA,row.LEREQDIA,row.LESPHERE,row.LECYLINDER,row.LEAXIS,row.LEADDITION,row.LEQTY,row.LEBASE,row.LECT,row.LEET,row.LEPRISM1,row.LEPRISM1DIA,row.LEPRISM2,row.LEPRISM2DIA,row.LEPD,row.LENPD,row.LEHEIGHT,row.COATINGCOADE,row.COATINGDESC, row.TINTCOADE,row.TINTDESC,row.BOXA,row.BOXB,row.DBL,row.FRAMETYPE,row.VERTEXDIST,row.WRAPANGLE,row.PANTOANGLE,row.SPLINSTRUCTION,row.EDGINGTYPE])

    return response
