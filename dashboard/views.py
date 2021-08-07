from django.shortcuts import redirect, render
import requests
from django.views.decorators.csrf import csrf_exempt
from accounts.models import User
from . import models
from .checksum import generate_checksum, verify_checksum
import json
# Create your views here.

def PurchaseCourses(request):
    return render(request, 'purchase_courses.html')



@csrf_exempt
def MakePayment(request):
    id = request.POST.get('id')
    amount = request.POST.get('amount')
    print(amount)
    

    
    if request.user.username in [u['username'] for u in User.objects.all().values('username')]:
        if request.method == "POST":
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
            "CALLBACK_URL": 'http://127.0.0.1:8000/webkiosk/handlerequest/'+str(order_id)+'/' + str(student[0]['id']) + '/' + str(institute_amount) + '/' + str(hostel_amount)
        }

            checksum = generate_checksum(param_dict, MERCHANT_KEY)
            param_dict['CHECKSUMHASH'] = checksum

            json_param_dict = json.dumps(param_dict)
            print(param_dict)
            return render(request, 'paytm.html', {'param_dict': param_dict,'json_param_dict':json_param_dict})


    else:
        return redirect('fault', fault='ACCESS DENIED!')


# @csrf_exempt
# def handlerequest(request, order_id, student_pk,institute_amount, hostel_amount):
#     MERCHANT_KEY = '8xcMryK%LvX_hOHp'
#     form = request.POST
#     response_dictionary = {}
#     for i in form.keys():
#         response_dictionary[i] = form[i]
#         if i == 'CHECKSUMHASH':
#             checksum = form[i]
#     # verify = verify_checksum(response_dictionary, MERCHANT_KEY, checksum)
#     # print(response_dictionary['CHECKSUMHASH'])
#     # if verify:
#         # if response_dictionary['RESPCODE'] == '01':
#     param_dict = {
#                 "MID": "crFzoJ56550017024860",
#                 "ORDER_ID": str(order_id) ,
#                 "CUST_ID": str(order_id),
#                 "TXN_AMOUNT": str(institute_amount+hostel_amount),
#                 "CHANNEL_ID": "WEB",
#                 "INDUSTRY_TYPE_ID": "Retail",
#                 "WEBSITE": "WEBSTAGING",
#     }

#     student = stu_models.Register.objects.get(id__exact = student_pk)
#     checksum = generate_checksum(param_dict, MERCHANT_KEY)
#     response = requests.post('https://securegw-stage.paytm.in/order/status?JsonData={"MID":"crFzoJ56550017024860","ORDERID":"'+ str(order_id) +'","CHECKSUMHASH":"'+ str(checksum)+'"}', params  = request.POST)
#     status = response.content.decode('utf-8').split("RESPCODE")[1][3]+response.content.decode('utf-8').split("RESPCODE")[1][4]
#     if status == '01':
#         bank_ref_number = response_dictionary['BANKTXNID']
#         paytm_ref_number = response_dictionary['TXNID']
#         txn_status = response_dictionary['STATUS']
#         bank_name = response_dictionary['BANKNAME']
#         mode = response_dictionary['PAYMENTMODE']

#         receipt_no = fees_views.generateReceiptNumber(student.college_code)

#         if student.college_code == '1127':
#             models.ReceiptNumberJPIHM.objects.create(receipt_no = receipt_no, student_name = stu_models.Register.objects.get(pk__exact = student_pk))
#         if student.college_code == '282':
#             models.ReceiptNumberJPIET.objects.create(receipt_no = receipt_no, student_name = stu_models.Register.objects.get(pk__exact = student_pk))
#         if student.college_code == '1605':
#             models.ReceiptNumberJPIETDiploma.objects.create(receipt_no = receipt_no, student_name = stu_models.Register.objects.get(pk__exact = student_pk))
#         total_fee = institute_amount + hostel_amount
#         if bank_ref_number:
#             models.FeesDeposit.objects.create(student_name= stu_models.Register.objects.get(pk__exact = student_pk),session = stu_models.Session.objects.get(session__exact =stu_models.Register.objects.values('admission_session__session').filter(pk__exact = student_pk)[0]['admission_session__session']),  year = stu_models.Register.objects.filter(pk__exact = student_pk).values('year')[0]['year'],
#             receipt_no = receipt_no, rtgs = True, college_code = student.college_code,reg_fee = 0, tuition_fee = institute_amount, book_bank_fee = 0, exam_fee = 0, uniform_fee = 0,
#             sub_sem_fee = 0, sac_fee = 0, bus_fee = 0, back_paper_fee = 0, hostel_fee = hostel_amount,scholarship_amount = 0,total_fee = total_fee, transaction_dated = datetime.date.today(), remarks = 'Online Payment with ID -'+f'{order_id}', transaction_number = bank_ref_number)
#         else:
#             models.FeesDeposit.objects.create(student_name= stu_models.Register.objects.get(pk__exact = student_pk),session = stu_models.Session.objects.get(session__exact =stu_models.Register.objects.values('admission_session__session').filter(pk__exact = student_pk)[0]['admission_session__session']),  year = stu_models.Register.objects.filter(pk__exact = student_pk).values('year')[0]['year'],
#             receipt_no = receipt_no,  rtgs = True, college_code = student.college_code,reg_fee = 0, tuition_fee = institute_amount, book_bank_fee = 0, exam_fee = 0, uniform_fee = 0,
#             sub_sem_fee = 0, sac_fee = 0, bus_fee = 0, back_paper_fee = 0, hostel_fee = hostel_amount,scholarship_amount = 0,total_fee = total_fee, transaction_dated = datetime.date.today(), remarks = 'Online Payment with ID -'+f'{order_id}')
#             # email_list = []
#             # email_list.append(student.email)
#             # subject = 'PAYMENT SUCCESSFUL'
#             # body = f'Dear {student.name}, Your payment for {student.course} {student.branch} of Rs.{student.amount} is successful'
#             # message = EmailMultiAlternatives(subject= subject,body = body ,from_email='deansw.jpiet@gmail.com',to = email_list)
#             # html_template = get_template('email.html').render({'name': student.name, 'course': student.course, 'branch': student.branch, 'amount':student.amount, 'bank_ref_number':bank_ref_number, 'order_id': order_id, 'semester':student.semester})

#             # message.attach_alternative(html_template, "text/html")
#             # message.send()
#     else:
#             print('Order Unsuccessful because')

#     return render(request, 'payment_status.html',{'status': status, 'student':student, 'receipt_no': receipt_no})
