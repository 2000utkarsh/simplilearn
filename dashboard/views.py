from django.http.response import JsonResponse
from django.shortcuts import redirect, render
import requests
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User
from . import models
from .checksum import generate_checksum, verify_checksum
import json
from . import forms
# Create your views here.

def PurchaseCourses(request):
    ids = models.BoughtCourses.objects.values('ids').filter(username = User.objects.get(username = request.user.username))
    data = {}
    for i in range(len(ids)):
        key = str('id' +'-'+ str(i))
        data[key] = ids[i]['ids']

    data = json.dumps(data)
    return render(request, 'purchase_courses.html', {'data': data})

def MakePayment(request,id,amount):
    
    
    if request.user.username in [u['username'] for u in User.objects.all().values('username')]:

        raw_id = models.OrderID.objects.values('order_id').order_by('id').last()
        if raw_id:
            for key,value in raw_id.items() :
                id_value = value
            id_value_int = int(id_value.split('SIMPLEARN')[-1])
            order_id_int = id_value_int + 1
            order_id_int = '{0:0=7d}'.format(order_id_int)
            order_id = 'SIMPLEARN' + str(order_id_int)
        else:
            order_id = 'SIMPLEARN' + '0000002'

        models.OrderID.objects.create(order_id = order_id)


        MERCHANT_KEY = '8xcMryK%LvX_hOHp'
        param_dict = {
        "MID": "crFzoJ56550017024860",
        "ORDER_ID": str(order_id) ,
        "CUST_ID": str(order_id),
        "TXN_AMOUNT": str(amount),
        "CHANNEL_ID": "WEB",
        "INDUSTRY_TYPE_ID": "Retail",
        "WEBSITE": "WEBSTAGING",
        "CALLBACK_URL": 'http://127.0.0.1:8000/dashboard/handlerequest/'+str(request.user.username)+'/'+ str(id)+'/'+str(order_id)+'/' + str(amount) + '/'
    }

        checksum = generate_checksum(param_dict, MERCHANT_KEY)
        param_dict['CHECKSUMHASH'] = checksum

        json_param_dict = json.dumps(param_dict)

        return render(request, 'paytm.html', {'param_dict': param_dict,'json_param_dict':json_param_dict})


    else:
        return render(request, 'fault.html', {'fault': "ACCESS DENIED"})



@csrf_exempt
def handlerequest(request, username, id,order_id, amount):
    MERCHANT_KEY = '8xcMryK%LvX_hOHp'
    form = request.POST
    response_dictionary = {}
    for i in form.keys():
        response_dictionary[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = verify_checksum(response_dictionary, MERCHANT_KEY, checksum)
    # print(response_dictionary['CHECKSUMHASH'])
    if verify:
        if response_dictionary['RESPCODE'] == '01':
            param_dict = {
                "MID": "crFzoJ56550017024860",
                "ORDER_ID": str(order_id) ,
                "CUST_ID": str(order_id),
                "TXN_AMOUNT": str(amount),
                "CHANNEL_ID": "WEB",
                "INDUSTRY_TYPE_ID": "Retail",
                "WEBSITE": "WEBSTAGING",
    }


    checksum = generate_checksum(param_dict, MERCHANT_KEY)
    response = requests.post('https://securegw-stage.paytm.in/order/status?JsonData={"MID":"crFzoJ56550017024860","ORDERID":"'+ str(order_id) +'","CHECKSUMHASH":"'+ str(checksum)+'"}', params  = request.POST)
    status = response.content.decode('utf-8').split("RESPCODE")[1][3]+response.content.decode('utf-8').split("RESPCODE")[1][4]
    if status == '01':
        bank_ref_number = response_dictionary['BANKTXNID']
        paytm_ref_number = response_dictionary['TXNID']
        txn_status = response_dictionary['STATUS']
        bank_name = response_dictionary['BANKNAME']
        mode = response_dictionary['PAYMENTMODE']

        models.BoughtCourses.objects.create(username = models.User.objects.get(username =username), ids = id)

    return render(request, 'payment_status.html',{'status': status})

def RegisterCard(request):
    
    if request.user.username in [u['username'] for u in User.objects.all().values('username')]:
        form = forms.RegisterCardForm(request.POST)

        if request.method == 'POST':
            if form.is_valid():
                name_on_card = form.cleaned_data['name_on_card']
                card_bank = form.cleaned_data['card_bank']
                card_number = form.cleaned_data['card_number']
                card_type = form.cleaned_data['card_type']
                expiry_month = form.cleaned_data['expiry_month']
                expiry_year = form.cleaned_data['expiry_year']
                otp = form.cleaned_data['otp']
                if(otp == 123456):
                    models.CardDetails.objects.create(username = models.User.objects.get(username =request.user.username), name_on_card = name_on_card, card_bank = card_bank, card_number = card_number, expiry_month = expiry_month, expiry_year = expiry_year, card_type = card_type)
                    return render(request, 'success.html', {'success': "Card Registered Successfully"})

                else:
                    return render(request, 'fault.html', {'fault': "OTP NOT VERIFIED"})
                    

            else:
                return render(request, 'fault.html', {'fault': "Please Check Credentials in"})

        else:
            form = forms.RegisterCardForm()
            return render(request, 'register_card.html', {'form': form})
            

    else:
        return render(request, 'fault.html', {'fault': "ACCESS DENIED"})



def BoughtCourses(request):
    if request.user.username in [u['username'] for u in User.objects.all().values('username')]:
    
        ids = models.BoughtCourses.objects.values('ids').filter(username = User.objects.get(username = request.user.username))
        data = {}
        for i in range(len(ids)):
            key = str('id' +'-'+ str(i))
            data[key] = ids[i]['ids']

        data = json.dumps(data)
        return render(request, 'bought_courses.html', {'data': data})
    
    else:
        return render(request, 'fault.html', {'fault': "ACCESS DENIED"})



def ViewCourse(request, ids):
    
    if request.user.username in [u['username'] for u in User.objects.all().values('username')]:
        ids = models.BoughtCourses.objects.values('ids').filter(username = User.objects.get(username = request.user.username), ids = ids)
        if ids:
            data = json.dumps({"ids": ids[0]['ids']})
            return render(request, 'view_course.html', {'data': data})

        else:
            return render(request, 'fault.html', {'fault':'ACCESS DENIED! You have to purchase this course'})
        
    else:
        return render(request, 'fault.html', {'fault': "ACCESS DENIED"})
