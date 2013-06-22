# Create your views here.
__author__ = 'Suraz'

from django.http import *
import re
import random
import datetime
from ewallet.models import *
from django.shortcuts import render_to_response,redirect
from ewallet.forms import *
import importlib
import hashlib
from email import *
from infopage_contents import *
#from ewallet import forms
#from ewallet import methods_defn
from django.core.exceptions import *

alphanum = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def sign_in(request):                                              #sign in page handler
    if request.method == 'POST':
        return sign_in_post(request)                               #directs to POST method handler for sign in page
    elif request.method == 'GET':
        return  sign_in_get(request)                               #directs to GET method handler for sign in page
    else:
        raise Http404


def sign_in_post(request):                                  #POST method handler for sign in page
    if  "sign_button" in  request.POST:                     #if user is signing in
        user, error = authenticate(request)                        #authenticate the user
        if user:
            return welcomepage(request, user)
        else:
            return render_to_response("home.html", {"error": error})


    elif "register_button" in request.POST:                 #if registration request is obtained in sign in page
        return HttpResponseRedirect('/project/ewallet/register/')
#    elif "transfer_button" in request.POST:
#        return transfer_to_ew(request)

    else:
        raise Http404

contact = "Contact"
faq = "FAQ"
banks = "BANKS"



def transfer (request):
    return welcomepage(request)

def info_page(request, page):
    error1 = ""
    error2 = ""
    success1 = 0
    success2 =0
    if page == "pwreset":
        if "emailsubmit" in request.POST:
            try:
                user =  User_details.objects.get(email = str(request.POST['email']))
            except:
                error1 = "This email is not registered to our database."
            if not error1:
#                if str(user.username) == str(request.POST['username']):
                success1 = 1
#                rancode = ''.join(random.choice(alphanum) for i in range(6))
#                user.code = rancode
#
#                user.save()

                link = generate_pwrlink(user.username,user.password)


                msg = getResetMessage(user.username,link)

                if sendEmail("e-Wallet Password Reset",msg ,['srt983@gmail.com',]):
                    success1 = 1
                #send email to the address


#        if "codesubmit" in request.POST:
#            try:
#                user = User_details.objects.get(username = request.POST['username'] )
#            except:
#                error2 ="Invalid username."
#            if not error2:
#                if str(user.code) == str(request.POST['code']):
#                    pass
#                    success2 = 1
#                    user.code = None
##                    ranpass = ''.join(random.choice(alphanum) for i in range(8))
##                    user.password = str(hashlib.sha256(ranpass).hexdigest())
#                    user.save()
#                    sendEmail("subject","message",['srt983@gmail.com',])
#                    #send new password to emaiil address
#
#
#                else:
#                    error2 = "The code didnt match the username."



    return render_to_response("info_page.html",{"page":page,"error1":error1,"error2":error2,"success1":success1,"success2":success2,})

def generate_pwrlink(username,password):
    link = "project/ewallet/pwr/%s/"%username
    link += str(hashlib.sha256(str(password)).hexdigest())
    return link

def pwreset(request, username ,id):
    user = None
    error =""
    success =0
    try :

        user = User_details.objects.get(username = username)
    except :
        return HttpResponseRedirect('/project/ewallet/pwreset/')


    if str(hashlib.sha256(str(user.password)).hexdigest()) == str(id):
        if request.method == "POST":
            if "change" in request.POST:

                if request.POST['new_pass'] == request.POST['conf_pass']:
                    if not re.match(".{6,32}",request.POST['new_pass'] ):
                        error = "Password must be of 6-32 characters."
                    else:
                        user.password = str(hashlib.sha256(request.POST['new_pass']).hexdigest())
                        user.save()
#                        error = 0;
                        success =1;
                else:
                    error = "Passwords didn't match."
        return render_to_response("info_page.html",{"page":"pwr","error":error,"success":success})
    return HttpResponseRedirect('/project/ewallet/pwreset/')


#def checksession(request):
#    try :
#        user = User_details.objects.get(username = request.session['username'],password = request.session['password'])
#    except :
#    #        return HttpResponseRedirect('/project/banks/bank_2/signin/')
#        return render_to_response("home.html", {"error": 0})


def sign_in_get(request):                                  #GET method handler for sign in page
    try :
        user = User_details.objects.get(username = request.session['username'],password = request.session['password'])
    except :
    #        return HttpResponseRedirect('/project/banks/bank_2/signin/')
        return render_to_response("home.html", {"error": 0})
    return welcomepage(request,user)
##    balance = User_details.objects.get(username=request.session['username'])..current_balance
#    username = request.session['username']
#    return render_to_response("ewwelcome.html", {"user": username,})# "bal":balance})
##        return render_to_response("home.html", {"error": 0})


def register(request):                                      #registration page handler
    if request.method == 'POST':
        return register_post(request)
    elif request.method == 'GET':
        return register_get(request)


def register_post(request):
    if "sign_button" in request.POST:
        return HttpResponseRedirect('/project/ewallet/home/')
    elif "register_button" in request.POST:
        form_data, errors = check_all_validity(request,"register")
        if form_data:
            user = create_user_account(form_data)

            return welcomepage(request, user)
        else:
            form = Ew_registration_form(request.POST)
            return render_to_response("ewregister.html",{"form":form,"empty_errors":errors[0],"valid_errors":errors[1]})
#            return render_to_response("ewregister.html ", {"form": form, "empty_errors": errors[0],
#                                                         "valid_errors": errors[1], })
    else:
        raise Http404


def register_get(request):
    try :
        user = User_details.objects.get(username = request.session['username'],password = request.session['password'])
    except :
    #        return HttpResponseRedirect('/project/banks/bank_2/signin/')
        form = Ew_registration_form()
        return render_to_response("ewregister.html",{"form":form})

    return welcomepage(request,user)
#    return render_to_response("ewregister.html", {"form": form})


def check_all_validity(request, from_page ):
    form = Ew_registration_form(request.POST)        #create a form bounded form with request data
    form_data = get_formdata(request,from_page)                    #obtain form_data for manual checking

    error1, errors = validate_form(form_data, form ,from_page)

    if not error1:
        if from_page =="edit":
            return form_data , errors
        else:
#        error2, errors = validate_account_no(form_data['account_no'],form_data['pin_no'], errors)
#        if not error2:
            error3, errors = validate_username(form_data['username'], errors)
            if not error3:
                return form_data, errors
    return None, errors

#def pwreset(request):
#
#    return render_to_response("info_page.html",{"page":pwresetpage})




def validate_form(form_data, form, frompage):
    error = 0
    empty_errors = {'fname_empty': 0, #error status checking for field-empty errors
                    'lname_empty':0,
                    'username_empty': 0,
                    'email_empty':0,
                    'password_empty': 0,


                   }

    invalid_errors = {'invalid_fname': 0, #error status checking for invalid field-input errors
                      'invalid_mname': 0,
                      'invalid_lname': 0,
                      'invalid_contact':0,
                      'invalid_username': 0,
                      'invalid_email':0,
                      'invalid_conf_password': 0,
                      'unknown': 0,
                      'unavailable_username': 0,


                      'limit_username': 0,

                      'limit_password':0,}

#    if not form_data['account_no']:
#        empty_errors['account_no_empty'] = 1
#        error = 1
#
#    if not form_data['pin_no']:
#        empty_errors['pin_empty'] = 1
#        error = 1

    if not form_data['fname']:
        empty_errors['fname_empty'] = 1
        error = 1

    if not form_data['lname']:
        empty_errors['lname_empty'] = 1
        error = 1

    if not form_data['email']:
        empty_errors['email_empty'] = 1
        error = 2


    if frompage == "register":
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

    if not re.match("^[a-zA-Z0-9_]+$", form_data['fname']):
        invalid_errors['invalid_fname'] = 1
        error = 5


    if not re.match("^[a-zA-Z0-9_]*$", form_data['mname']):
        invalid_errors['invalid_mname'] = 1
        error = 5

    if not re.match("^[a-zA-Z0-9_]+$", form_data['lname']):
        invalid_errors['invalid_fname'] = 1
        error = 5


    if frompage == "register":
        if not re.match("^[a-zA-Z0-9_.-]+$", form_data['username']):
            invalid_errors['invalid_username'] = 1
            error = 5

    if not re.match("[^@]+@[^@]+\.[^@]+", form_data['email']):
        invalid_errors['invalid_email'] = 1
        error = 1

    if frompage == "register":
        if not re.match("^[a-zA-Z0-9_.-]{4,32}$", form_data['username']):
            invalid_errors['limit_username'] = 1
            error = 5
#
#    if not re.match("^[0-9]{1,6}$", form_data['pin_no']):
#        invalid_errors['invalid_pin'] = 1
#        error = 1
#
#    if not re.match("^[a-zA-Z0-9]+$", form_data['account_no']):
#        invalid_errors['invalid_account_no'] = 1

    if frompage == "register":
        if not form.is_valid():                                 # check if there are unknown errors
            error = 1
            invalid_errors['unknown'] = 1

    errors = [empty_errors, invalid_errors]
    return  error, errors


def create_user_account(form_data):
    fname= form_data['fname']
    mname = form_data['mname']
    lname = form_data['lname']
    username = form_data['username']
    try :
        contact = int (form_data['contact'])
    except ValueError:
        contact = 0
    email = form_data['email']
    password = str(hashlib.sha256(form_data['password']).hexdigest())


    pass
#    i ="fads"
    #Beneficiary details
    dob = datetime.date(int(form_data['dob_yr']),int(form_data['dob_mth']),int(form_data['dob_day']))


    new_user = User_details(
    fname=fname,mname = mname,lname=lname,username = username,email = email ,
    password=password,contact = contact)
    try:
        new_user.save()
    except:
        sendEmail("Site Error", "ewallet.views line no 361" ,["info.ewallet@gmail.com"])
        pass


    ben_detail = Beneficiary (user=new_user,ctzen = form_data["citizenship_no"],
                dob = dob,
                 b1_fname = form_data["b1_fname"],
                 b1_mname = form_data["b1_mname"],
                 b1_lname = form_data["b1_lname"],
                b2_fname = form_data["b2_fname"],
                 b2_mname = form_data["b2_mname"],
                b2_lname = form_data["b2_lname"],
              )
    ben_detail.save()

    ewuser = Ewalletusers(username=form_data['username'],current_balance = 0)
    ewuser.save()

    write_statement("e-Wallet", new_user, "Account Created",0)
    return new_user

def update_user_details(request,form_data):
    user = User_details.objects.get(username = request.session['username'])
    user.fname= form_data['fname']
    user.mname = form_data['mname']
    user.lname = form_data['lname']

    try :
        contact = int (form_data['contact'])
    except ValueError:
        contact = 0
    user.email = form_data['email']

    user.save()




    #    i ="fads"
    #Beneficiary details
    ben = Beneficiary.objects.get(user = request.session['username'])
    ben.dob = datetime.date(int(form_data['dob_yr']),int(form_data['dob_mth']),int(form_data['dob_day']))



    #    try:

    #    except:
    #send email to the administrator about the server error
    #        pass



    ben.b1_fname = form_data["b1_fname"]
    ben.b1_mname = form_data["b1_mname"]
    ben.b1_lname = form_data["b1_lname"]
    ben.b2_fname = form_data["b2_fname"]
    ben.b2_mname = form_data["b2_mname"]
    ben.b2_lname = form_data["b2_lname"]
    ben.b3_fname = form_data["b3_fname"]
    ben.b3_mname = form_data["b3_mname"]
    ben. b3_lname = form_data["b3_lname"]
    ben.save()









def write_statement(tran_part,user, description,amt):
    current_date = datetime.datetime.now()
    s = Statements(transaction_partner = tran_part, user=user, statement_des=description, date = current_date.date(), time = current_date.time(),amount=amt)

    s.save()

        #send email to the administrator about the server error
    pass


def welcomepage(request, user):
    request.session['username'] = user.username
    request.session['password'] = user.password
    request.session['user'] = user
    request.session['viewtype'] = "payment"
    request.session['subviewtype'] = "payonline"
    request.session['subprofilemenu'] = "view"
    page_redirect = '/project/ewallet/' + user.username + '/'
    page_redirect = str(page_redirect)
    return HttpResponseRedirect(page_redirect)


def show_statements(request):

    stat_pp = 10
    sort = "date"
    from_date = str(Statements.objects.get(user = request.session['username'], statement_des = "Account Created").date)
    to_date = str(datetime.datetime.now().date())
    page = 1
    if "show" in request.POST:
        request.session["eof"]= False
        try:
            request.session["stat_pp"] = stat_pp = int(request.POST["stat_pp"])
        except:
            request.session["stat_pp"] = stat_pp
        try:
                request.session["sort"] = sort = request.POST["sort"]
        except:
            request.session["sort"] = sort
        try:
            request.session["from_date"] = from_date = str(datetime.date(int(request.POST["fyear"]),int(request.POST["fmth"]),int(request.POST["fday"]),))
        except:
            request.session["from_date"] = from_date
        try:
            request.session["to_date"] = to_date = str(datetime.date(int(request.POST["tyear"]),int(request.POST["tmth"]),int(request.POST["tday"])))
        except:
            request.session["to_date"] = to_date

    elif ("next" in request.POST) or ("prev" in request.POST):
        try :
            stat_pp = int(request.session["stat_pp"])
        except:
            pass
        try:
            sort = request.session["sort"]
        except:
            pass
        try:
            from_date = str(request.session["from_date"])
        except:
            pass
        try:
            to_date = str(request.session["to_date"])
        except:
            pass
        page = request.session["page"]

        if "next" in request.POST:
            try:
                if  not request.session["eof"]:
                    page += 1
            except:
                page += 1

        elif ("prev" in request.POST) and (not request.session["page"]==1):
            request.session["eof"]= False
            page -= 1

    request.session["page"] = page
    start = (page - 1)* stat_pp
    end = page*int(stat_pp)

    statements = Statements.objects.filter(date__lte = to_date, date__gte = from_date , user = request.session['username']).order_by(sort)[start:end]
    if len(statements) < stat_pp:
         request.session["eof"] = True

    return statements


def show_profile(request):
    user = User_details.objects.get(username=request.session["username"])
    ben = Beneficiary.objects.get(user = request.session["username"])
    return user,ben




def changepassword(request):
    empty_error = 0
    limit_error = 0
    mismatch_error = 0
    incorrect_pass = 0
    error = 0
    current_user = User_details.objects.get(username=request.session["username"])


    form_pass = str(hashlib.sha256(request.POST['cur_pass']).hexdigest())
    #    password = request.POST['password']
    user_pass = str(current_user.password)

    if user_pass != form_pass:
        incorrect_pass = 1
        error = 1


    if not request.POST['new_pass']:
        empty_error = 1
        error = 1

    else:
        if request.POST['conf_pass'] != request.POST['new_pass']:
           mismatch_error = 1
           error = 1




    if not re.match(".{6,32}", request.POST['new_pass']):
        limit_error = 1
        error = 1

    errors ={"empty_error":empty_error,"limit_error":limit_error,"mismatch_error":mismatch_error,"incorrect_pass":incorrect_pass}

    if not error:
        current_user.password =  str(hashlib.sha256(request.POST['new_pass']).hexdigest())
        current_user.save()
        request.session['password'] = current_user.password
    return error,errors




def home(request, username  ):
    form = ""
    ben = ""
    user = ""
    form = ""
    error= ""
    errors = "  "
    statements = ""
    success = ""
    transfer_error = ""
    passerrors = ""
    if "logout" in request.POST:
        request.session['username'] = ""
        request.session['password'] = ""

        return HttpResponseRedirect('/project/ewallet/home/')


    try :

        cur_user = User_details.objects.get(username = request.session['username'],password = request.session['password'])
    except :
        return HttpResponseRedirect('/project/ewallet/home/')

    usersname = cur_user.fname +" " + cur_user.mname + " " + cur_user.lname
    balance = Ewalletusers.objects.get(username = cur_user.username).current_balance

    if request.session["subviewtype"] == "statement":
#        try:
            statements = show_statements(request)
#        except:
            pass
            form = Statement_form(request.POST)

    if request.session["subviewtype"] == "profile":
        if "edit" in request.POST:



            request.session["subprofilemenu"] = "edit"
        if "save" in request.POST:
            form_data, errors = check_all_validity(request,"edit")
            if form_data:
                update_user_details(request,form_data)
                request.session["subprofilemenu"] = "view"
        if "cancel" in request.POST:
            request.session["subprofilemenu"] = "view"




        userprofile = User_details.objects.get(username=request.session["username"])
        form = Ew_registration_form()


        user, ben = show_profile(request)

    if request.session["subviewtype"] == "changepass":
        if "change" in request.POST:
            error, passerrors= changepassword(request)

    if request.session["subviewtype"] == "tof":
        if "transfer_button" in request.POST:
            transfer_error = transfer_request(request,"ew")

    if request.session["subviewtype"] == "mpayment":
        if "transfer_button" in request.POST:
            transfer_error = transfer_request(request ,"adsl")

    if username!= request.session['username']:
        return HttpResponseRedirect('/project/ewallet/%s/'%request.session['username'])
#    balance = User_details.objects.get(username=request.session['username']).bank_details.current_balance

    return render_to_response("ewwelcome.html", {"empty_errors":errors[0],"valid_errors":errors[1],
                                                "transfer_error":transfer_error,
                                                 "users":user,"ben":ben,
                                                 "usersname":usersname,
                                                 "balance":balance,
                                                 "var":request.session,
                                                 "form":form ,"user": request.session['username'],
                                                 "error":error,"errors":passerrors,"menu":request.session["viewtype"],
                                                 "submenu":request.session["subviewtype"],
                                                 "subprofilemenu":request.session["subprofilemenu"],
                                                 "statements":statements})


def get_formdata(request , from_page):
#    account_no = request.POST['account_no']
#    pin_no = request.POST['pin_no']
    username =""
    password =""
    conf_password = ""
    fname = request.POST['fname']
    mname = request.POST['mname']
    lname = request.POST['lname']
    contact = request.POST['contact']
    email = request.POST['email']
    if from_page == "register":
        username = request.POST['username']

        password = request.POST['password']
        conf_password = request.POST['confirm_password']

    citizenship_no = request.POST['citizenship_no']
    dob_yr = request.POST['dob_yr']
    dob_mth = request.POST['dob_mth']
    dob_day = request.POST['dob_day']
    b1_fname = request.POST['b1_fname']
    b1_mname = request.POST['b1_mname']
    b1_lname = request.POST['b1_lname']
    b1_ctzen = request.POST['b1_citizenship_no']
    b2_fname = request.POST['b2_fname']
    b2_mname = request.POST['b2_mname']
    b2_lname = request.POST['b2_lname']
    b2_ctzen = request.POST['b2_citizenship_no']


    form_data = { "fname": fname,"mname":mname, "lname":lname,"contact":contact, "username": username, "email":email,

            "password": password, "conf_password": conf_password,
            "citizenship_no":citizenship_no, "dob_yr":dob_yr,"dob_mth":dob_mth,"dob_day":dob_day,
            "b1_fname":b1_fname,"b1_mname":b1_mname,"b1_lname":b1_lname,"b2_fname":b2_fname,"b2_mname":b2_mname,"b2_lname":b2_lname,"b1_ctzen":b1_ctzen,"b2_ctzen":b2_ctzen,}
    return form_data



def account(request,username):
    request.session["viewtype"] = "account"
    request.session["subviewtype"] = "statement"


    return HttpResponseRedirect("/project/ewallet/%s"%username)

def payment(request,username):
    request.session["viewtype"] = "payment"
    request.session["subviewtype"] = "mpayment"
    return HttpResponseRedirect("/project/ewallet/%s"%username)

def transfer(request,username):
    request.session["viewtype"] = "transfer"
    request.session["subviewtype"] = "tof"
    return HttpResponseRedirect("/project/ewallet/%s"%username)

def topup(request,username):
    request.session["subviewtype"] = "topup"
    return HttpResponseRedirect("/project/ewallet/%s"%username)

def tof(request,username):
    request.session["subviewtype"] = "tof"
    return HttpResponseRedirect("/project/ewallet/%s"%username)

def statement(request,username):
    request.session["subviewtype"] = "statement"
    return HttpResponseRedirect("/project/ewallet/%s"%username)

def profile(request,username):
    request.session["subviewtype"] = "profile"
    request.session["subprofilemenu"] = "view"
    return HttpResponseRedirect("/project/ewallet/%s"%username)

def changepass(request,username):
    request.session["subviewtype"] = "changepass"
    return HttpResponseRedirect("/project/ewallet/%s"%username)

def mpayment(request,username):
    request.session["subviewtype"] = "mpayment"
    return HttpResponseRedirect("/project/ewallet/%s"%username)

def buycards(request, username):
    request.session["subviewtype"] = "buycards"
    return HttpResponseRedirect("/project/ewallet/%s"%username)

def payonline(request, username):
    request.session["subviewtype"] = "payonline"
    return HttpResponseRedirect("/project/ewallet/%s"%username)


def authenticate(request):
    error = 0
    username = request.POST['username']
    current_user = User_details.objects.filter(username=username)

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
    if  not User_details.objects.filter(username=user_name).exists():
        return 0, errors                                                       #no error in username / username availabele
    else:
        errors[1]['unavailable_username'] = 1
        return 1, errors



def transfer_to_ew(request):
    from_acc = request.session['account_no']
    #    from_bank =
    to_user = request.POST['username']
    amount = request.POST['amount']
    success = 1
    return render_to_response("ewwelcome.html", {"success": success, })



#def admin_page(request):
#        error = 0
#        username =''
#        password =''
#        try:
#            username = request.session['username']
#            password = request.session['password']
#        except KeyError:
#            pass
#        if username == "admin" and password == "admin":
#
#            if "incoming" in request.POST:
#                return settle_incoming()
#            elif "outgoing" in request.POST:
#                return settle_outgoing()
#            elif "deposit" in request.POST:
#                return deposit(request)
#            elif "logout" in request.POST:
#                request.session['username'] = ''
#                request.session['password'] = ''
#                return render_to_response("admin_signin.html", {"error": error})
#            return render_to_response("admin.html")
#        if request.method == 'POST':
#            if request.POST["username"] == "admin" and request.POST['password'] == "admin":
#                request.session['username'] = "admin"
#                request.session['password'] = "admin"
#                return render_to_response("admin.html")
#
#        return render_to_response("admin_signin.html", {"error": error})

#
#def settle_incoming():
#    incoming = Incoming_pends.objects.all().filter(status=1)
#    for i in incoming:
#        acc_no = i.to_account
#        amt = i.amount
#        bank = i.from_bank
#        user = Users_bank_details.objects.get(account_no=acc_no)
##        try:
##            user = Users_bank_details.objects.get(account_no=acc_no)
##        except :
##            return render_to_response("admin.html", {'outgoing':0, "view_in": 0, 'view_out': 1})
#        user.current_balance += amt
#        user.save()
#        i.status = False
#        i.save()
#    return render_to_response("admin.html", )


#def settle_outgoing():
#    outgoing = Outgoing_pends.objects.all().filter(status=1)
#    from_bank = Outgoing_pends._meta.app_label
#
#    for i in outgoing:
#        from_acc_no = i.from_account
#        to_acc_no = i.to_account
#        amt = i.amount
#        to_bank = i.to_bank
#        to_bank_module = __import__(to_bank, globals(), locals(), [], -1)
#        incoming_pend = to_bank_module.models.Incoming_pends(from_bank=from_bank, from_account=from_acc_no,
#            to_account=to_acc_no, amount=amt, status=True)
#
#        incoming_pend.save()
#        i.status = False
#        i.save()
#    return render_to_response("admin.html", )




#
#def deposit(request):
#    success = 0
#    valuerror = 0
#    amount = 0
#    try:
#        amount = int(request.POST['amount'])
#    except ValueError:
#        valuerror = 1
#    if not valuerror:
#        deposit = Users_bank_details(account_no=request.POST['account_no'],pin_no = request.POST['pin_no'],
#            current_balance=amount)
#        deposit.save()
#        success = 1
#
#    return render_to_response("admin.html", {"success": success, "valuerror": valuerror})
#

#def outgoing(request):
#    outgoing_trans =[]
#    if request.session['username'] == 'admin' and request.session['password'] == 'admin':
#        if  'outgoing' in request.POST:
#            settle_outgoing()
#        outgoing_trans = Outgoing_pends.objects.filter(status=1)
#
#        return render_to_response("admin.html", {'outgoing': outgoing_trans, "view_in": 0, 'view_out': 1})
#    return HttpResponseRedirect('/projects/banks/bank_2/admin')


#def incoming(request):
#
#    if request.session['username'] == 'admin' and request.session['password'] == 'admin':
#        if  'incoming' in request.POST:
#            settle_incoming()
#        incoming_trans = Incoming_pends.objects.filter(status=1)
#        return render_to_response("admin.html", {'incoming': incoming_trans, 'view_in': 1, 'view_out': 0})
#    return HttpResponseRedirect('/projects/banks/bank_2/admin')

#def validate_account_no(account_no,pin_no, errors):
##    return 0,errors
#    error = 0
#    if  len(Bank_users.objects.filter(bank_details=account_no)):
#        error = 1
#        errors[1]['unavailable_account'] = 1
#
#    elif not len(Users_bank_details.objects.filter(account_no=account_no)):
#        error = 1
#        errors[1]['invalid_account_no'] = 1
#
#    elif   not Users_bank_details.objects.filter(account_no=account_no)[0].pin_no==pin_no:
#        error =1
#        errors[1]['pin_mismatch']=1
#    return error, errors








def transfer_request(request, transferto):


    ew_user = request.POST['ewusername']
    from ewallet.models import Ewalletusers
    try:
        if transferto =="ew":
            to_user = Ewalletusers.objects.get(username = ew_user)
        else :
            to_user = Adslusers.objects.get(username = ew_user)
    except Ewalletusers.DoesNotExist:
        return "Invalid Username"
    except Adslusers.DoesNotExist:
        return "Invalid Username"
    if to_user.username == request.session['username']:
        return "Invalid Username"


    amount = request.POST['amount']
    try :
        amount = int(amount)
    except ValueError:
        return "Invalid Amount"
    if amount< 0:
        return "Invalid Amount"
    current_user = Ewalletusers.objects.get(username = request.session["username"])

    if current_user.current_balance < amount:
        return "Insufficient Balance."

    current_user.current_balance -= amount
    current_user.save()

    if transferto =="ew":
        to_user.current_balance += amount
        to_user.save()
        write_statement("e-Wallet",User_details.objects.get(username=request.session['username']),"Fund Transfer" ,amount)
        write_statement("e-Wallet",User_details.objects.get(username=to_user.username),"Fund Received" ,-1*amount)

    else:

        from bank_2.views import transfer_to_bank
        transfer_to_bank("ADSL",amount,"eWallet","bank_2","bank_1")

        write_statement("ADSL",User_details.objects.get(username=request.session['username']),"ADSL Bill Payment" ,amount)

    #send to bank

    return 0


#def transfer_to_bank(ew_acc_no, amount, users_acc_no, from_bank, to_bank):
#    user = Users_bank_details.objects.get(account_no=users_acc_no)
#    user.current_balance -= int(amount)
#    user.save()
#    pending_outgoing = Outgoing_pends(to_bank=to_bank,
#        from_account=users_acc_no,
#        to_account=ew_acc_no,
#        amount=amount,
#        status=True)
#    pending_outgoing.save()

