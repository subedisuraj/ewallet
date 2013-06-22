# Create your views here.
__author__ = 'Suraz'

from django.http import *
import re
import datetime
from bank_1.models import *
from django.shortcuts import render_to_response,redirect
from bank_1.forms import *
import importlib
import hashlib

from bank_1 import forms
#from bank_1 import methods_defn
from django.core.exceptions import *


def sign_in(request):                                              #sign in page handler
    if request.method == 'POST':
        return sign_in_post(request)                               #directs to POST method handler for sign in page
    elif request.method == 'GET':
        return  sign_in_get(request)                               #directs to GET method handler for sign in page
    else:
        raise Http404



def help():
    render_to_response()


def sign_in_post(request):                                  #POST method handler for sign in page
    if  "sign_button" in  request.POST:                     #if user is signing in
        user, error = authenticate(request)                        #authenticate the user
        if user:
            return welcomepage(request, user)
        else:
            return render_to_response("Sign_in.html", {"bank":"ABC Bank","error": error})

    elif "register_button" in request.POST:                 #if registration request is obtained in sign in page
        return HttpResponseRedirect('/project/banks/bank_1/register/')
#    elif "transfer_button" in request.POST:
#        return transfer_to_ew(request)

    else:
        raise Http404


def sign_in_get(request):                                   #GET method handler for sign in page
    return render_to_response("Sign_in.html", {"bank":"ABC Bank","error": 0})


def register(request):                                      #registration page handler
    if request.method == 'POST':
        return register_post(request)
    elif request.method == 'GET':
        return register_get(request)


def register_post(request):
    if "sign_button" in request.POST:
        return HttpResponseRedirect('/project/banks/bank_1/signin/')
    elif "register_button" in request.POST:
        form_data, errors = check_all_validity(request)
        if form_data:
            user = create_user_account(form_data)

            return welcomepage(request, user)
        else:
            form = Bank_registration_form(request.POST)
            return render_to_response("Register.html ", {"bank":"ABC Bank","form": form, "empty_errors": errors[0],
                                                         "valid_errors": errors[1], })
    else:
        raise Http404


def register_get(request):
    form = Bank_registration_form()
    return render_to_response("Register.html", {"bank":"ABC Bank","form": form,})


def check_all_validity(request):
    form = Bank_registration_form(request.POST)        #create a form bounded form with request data
    form_data = get_formdata(request)                    #obtain form_data for manual checking

    error1, errors = validate_form(form_data, form)
    if not error1:
        error2, errors = validate_account_no(form_data['account_no'],form_data['pin_no'], errors)
        if not error2:
            error3, errors = validate_username(form_data['username'], errors)
            if not error3:
                return form_data, errors
    return None, errors


def validate_account_no(account_no,pin_no, errors):
#    return 0,errors
    error = 0
    if  len(Bank_users.objects.filter(bank_details=account_no)):
        error = 1
        errors[1]['unavailable_account'] = 1

    elif not len(Users_bank_details.objects.filter(account_no=account_no)):
        error = 1
        errors[1]['invalid_account_no'] = 1

    elif   not Users_bank_details.objects.filter(account_no=account_no)[0].pin_no==pin_no:
        error =1
        errors[1]['pin_mismatch']=1
    return error, errors


def validate_form(form_data, form):
    error = 0
    empty_errors = {'name_empty': 0, #error status checking for field-empty errors
                    'username_empty': 0,
                    'password_empty': 0,
                    'account_no_empty': 0,
                    'pin_empty': 0}

    invalid_errors = {'invalid_name': 0, #error status checking for invalid field-input errors
                      'invalid_username': 0,
                      'invalid_conf_password': 0,
                      'unknown': 0,
                      'unavailable_username': 0,
                      'invalid_account_no': 0,
                      'unavailable_account': 0,
                      'invalid_pin': 0,
                      'limit_username': 0,
                      'pin_mismatch':0,
                      'limit_password':0,}
    if not form_data['account_no']:
        empty_errors['account_no_empty'] = 1
        error = 1

    if not form_data['pin_no']:
        empty_errors['pin_empty'] = 1
        error = 1

    if not form_data['name']:
        empty_errors['name_empty'] = 1
        error = 1

    if not form_data['username']:
        empty_errors['username_empty'] = 1
        error = 2

    if not form_data['password']:
        empty_errors['password_empty'] = 1
        error = 3
    else:
        if form_data['conf_password'] != form_data['password']:
            invalid_errors['invalid_conf_password'] = 1
            error = 1



    if not re.match(".{6,32}", form_data['password']):
        invalid_errors['limit_password'] = 1
        error = 1

    if not re.match("^[a-zA-Z0-9_ ]+$", form_data['name']):
        invalid_errors['invalid_name'] = 1
        error = 5

    if not re.match("^[a-zA-Z0-9_.-]+$", form_data['username']):
        invalid_errors['invalid_username'] = 1
        error = 5

    if not re.match("^[a-zA-Z0-9_.-]{4,32}$", form_data['username']):
        invalid_errors['limit_username'] = 1
        error = 5

    if not re.match("^[0-9]{1,6}$", form_data['pin_no']):
        invalid_errors['invalid_pin'] = 1
        error = 1

    if not re.match("^[a-zA-Z0-9]+$", form_data['account_no']):
        invalid_errors['invalid_account_no'] = 1

    if not form.is_valid():                                 # check if there are unknown errors
        error = 1
        invalid_errors['unknown'] = 1

    errors = [empty_errors, invalid_errors]
    return  error, errors


def create_user_account(form_data):
    user = Users_bank_details.objects.get(account_no=form_data['account_no'], )
    password = str(hashlib.sha256(form_data['password']).hexdigest())
    #    password =  form_data['password']
    new_user = Bank_users(bank_details=user,
        name=form_data['name'],
        username=form_data['username'],
        password=password)
    try:
        new_user.save()
    except:
        #send email to the administrator about the server error
        pass
    write_statement(new_user, "Account Created")
    return new_user


def write_statement(user, description):
    current_date = datetime.datetime.now()
    s = Statements(user=user, statement_des=description, date=current_date.date, time=current_date.time)
    try:
        s.save()
    except:
        #send email to the administrator about the server error
        pass


def welcomepage(request, user):
    request.session['username'] = user.username
    request.session['password'] = user.password
    request.session['user'] = user
    page_redirect = '/project/banks/bank_1/' + user.username + '/'
    page_redirect = str(page_redirect)
#    return HttpResponseRedirect(page_redirect)
    return redirect( page_redirect , user)


def home(request, username  ):
    error=""
    if "logout" in request.POST:
        request.session['username'] = ""
        request.session['password'] = ""
#        request.session['balance'] = ""
        return HttpResponseRedirect('/project/banks/bank_1/signin/')


    try :
        Bank_users.objects.get(username = request.session['username'],password = request.session['password'])
    except Bank_users.DoesNotExist:
        return HttpResponseRedirect('/project/banks/bank_1/signin/')
    if "transfer_button" in request.POST:
        error = transfer_request(request)

    balance = Bank_users.objects.get(username=request.session['username']).bank_details.current_balance

    return render_to_response("Welcome.html", {"bank":"ABC Bank","user": username, "error":error, "bal":balance})





def transfer_request(request):
    bank_user = request.session['username']
    ew_user = request.POST['ewusername']
    from ewallet.models import Ewalletusers
    try:
        Ewalletusers.objects.get(username = ew_user)
    except Ewalletusers.DoesNotExist:
        return "Invalid Username"

    amount = request.POST['amount']
    try :
        amount = int(amount)
    except ValueError:
        return "Invalid Amount"
    bal = Bank_users.objects.get(username = bank_user).bank_details.current_balance
    if bal < amount:
        return "Insufficient Balance."
    from_bank = Bank_users._meta.app_label
    to_bank = "bank_2"
    from_acc_no = Bank_users.objects.get(username=bank_user).bank_details.account_no
    to_acc_no = "eWallet"
    transfer_to_ew(ew_user,amount,"ABC Bank")
    transfer_to_bank(to_acc_no, amount, from_acc_no, from_bank, to_bank)
    return 0


def transfer_to_bank(ew_acc_no, amount, users_acc_no, from_bank, to_bank):
    user = Users_bank_details.objects.get(account_no=users_acc_no)
    user.current_balance -= int(amount)
    user.save()
    pending_outgoing = Outgoing_pends(to_bank=to_bank,
        from_account=users_acc_no,
        to_account=ew_acc_no,
        amount=amount,
        status=True)
    pending_outgoing.save()


def get_formdata(request):
    account_no = request.POST['account_no']
    pin_no = request.POST['pin_no']
    name = request.POST['name']
    username = request.POST['username']
    password = request.POST['password']
    conf_password = request.POST['confirm_password']
    data = {"account_no": account_no,"pin_no":pin_no, "name": name, "username": username,
            "password": password, "conf_password": conf_password}
    return data


def authenticate(request):
    error = 0
    username = request.POST['username']
    current_user = Bank_users.objects.filter(username=username)

    if not current_user:
        error = 1
        return None, error
    form_pass = str(hashlib.sha256(request.POST['password']).hexdigest())
    #    password = request.POST['password']
    user_pass = str(current_user[0].password)

    if user_pass == form_pass:
        return current_user[0], error
    else:
        error = 1
        return None, error


def validate_username(user_name, errors):
#    return 0,errors
    if  not Bank_users.objects.filter(username=user_name).exists():
        return 0, errors                                                       #no error in username / username availabele
    else:
        errors[1]['unavailable_username'] = 1
        return 1, errors


def admin_page(request):
        error = 0
        username =''
        password =''
        try:
            username = request.session['username']
            password = request.session['password']
        except KeyError:
            pass
        if username == "admin" and password == "admin":

            if "incoming" in request.POST:
                return settle_incoming()
            elif "outgoing" in request.POST:
                return settle_outgoing()
            elif "deposit" in request.POST:
                return deposit(request)
            elif "logout" in request.POST:
                request.session['username'] = ''
                request.session['password'] = ''
                return render_to_response("admin_signin.html", {"bank":"ABC Bank","error": error})
            return render_to_response("admin.html",{"bank":"ABC Bank",})
        if request.method == 'POST':
            if request.POST["username"] == "admin" and request.POST['password'] == "admin":
                request.session['username'] = "admin"
                request.session['password'] = "admin"
                return render_to_response("admin.html",{"bank":"ABC Bank",})

        return render_to_response("admin_signin.html", {"bank":"ABC Bank","error": error})


def settle_incoming():
    incoming = Incoming_pends.objects.all().filter(status=1)
    for i in incoming:
        acc_no = i.to_account
        amt = i.amount
        if i.from_bank == "XYZ Bank":
            from_bank = "bank_2"
        if i.from_bank == "ABC Bank":
            from_bank = "bank_1"
        user = Users_bank_details.objects.get(account_no=acc_no)
#        try:
#            user = Users_bank_details.objects.get(account_no=acc_no)
#        except :
#            return render_to_response("admin.html", {'outgoing':0, "view_in": 0, 'view_out': 1})
        user.current_balance += amt
        user.save()
        i.status = False
        i.save()
    return render_to_response("admin.html",{"bank":"ABC Bank",} )


def settle_outgoing():
    outgoing = Outgoing_pends.objects.all().filter(status=1)
    from_bank = Outgoing_pends._meta.app_label

    for i in outgoing:
        from_acc_no = i.from_account
        to_acc_no = i.to_account
        amt = i.amount
        to_bank = "bank_2"
        if i.to_bank == "XYZ Bank":
            to_bank = "bank_2"
        if i.to_bank == "ABC Bank":
            to_bank = "bank_1"
        to_bank_module = __import__(to_bank, globals(), locals(), [], -1)
        incoming_pend = to_bank_module.models.Incoming_pends(from_bank=from_bank, from_account=from_acc_no,
            to_account=to_acc_no, amount=amt, status=True)

        incoming_pend.save()
        i.status = False
        i.save()
    return render_to_response("admin.html",{"bank":"ABC Bank",} )


def transfer_to_ew(to_user,amt,bank):
#    from_acc = request.session['account_no']

#    to_user = request.session['username']
#    amount = amt
    from ewallet.models import Ewalletusers,Statements,User_details




    ew_user = Ewalletusers.objects.get(username = to_user)
    ew_user.current_balance += int(amt)
    ew_user.save()
    from ewallet.views import  write_statement
    write_statement("ABC Bank", User_details.objects.get( username=  ew_user.username), "Fund Received", -1*amt)




    success = 1
    return render_to_response("Welcome.html", {"bank":"ABC Bank","success": success, })


def deposit(request):
    success = 0
    valuerror = 0
    amount = 0
    try:
        amount = int(request.POST['amount'])
    except ValueError:
        valuerror = 1
    if not valuerror:
        deposit = Users_bank_details(account_no=request.POST['account_no'],pin_no = request.POST['pin_no'],
            current_balance=amount)
        deposit.save()
        success = 1

    return render_to_response("admin.html", {"bank":"ABC Bank","success": success, "valuerror": valuerror})


def outgoing(request):
    if "logout" in request.POST:
        request.session['username'] = ''
        request.session['password'] = ''
        return render_to_response("admin_signin.html", {"bank":"ABC Bank",})
    outgoing_trans =[]
    if request.session['username'] == 'admin' and request.session['password'] == 'admin':
        if  'outgoing' in request.POST:
            settle_outgoing()
        outgoing_trans = Outgoing_pends.objects.filter(status=1)

        return render_to_response("admin.html", {"bank":"ABC Bank",'outgoing': outgoing_trans, "view_in": 0, 'view_out': 1})
    return HttpResponseRedirect('/project/banks/bank_1/admin')


def incoming(request):
#    if "back" in request.POST:
#        request.session['username'] = ''
#        request.session['password'] = ''
#        return HttpResponseRedirect("admin_signin.html", {"bank":"ABC Bank"})

    if "logout" in request.POST:
        request.session['username'] = ''
        request.session['password'] = ''
        return render_to_response("admin_signin.html", {"bank":"ABC Bank"})
    incoming_trans=[]
    if request.session['username'] == 'admin' and request.session['password'] == 'admin':
        if  'incoming' in request.POST:
            settle_incoming()
        incoming_trans = Incoming_pends.objects.filter(status=1)
        return render_to_response("admin.html", {"bank":"ABC Bank",'incoming': incoming_trans, 'view_in': 1, 'view_out': 0})
    return HttpResponseRedirect('/project/banks/bank_1/admin')