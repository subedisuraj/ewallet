__author__ = 'Dell'
from django.shortcuts import render_to_response

def about_page(request):
    return render_to_response("info_page.html",{"title":"eWallet:About",
                                                    "content":"eWallet is an online payment site."})

def faq_page(request):
    return render_to_response("info_page.html",{"title":"eWallet:FAQ",
                                                    "content":"What is e-Wallet? eWallet is an online payment site."})


def contact_page(request):
    return render_to_response("info_page.html",{"title":"eWallet:Contact",
                                                    "content":"info@ewallet.com"})


def security_page(request):
    return render_to_response("info_page.html",{"title":"eWallet:How Secure",
                                                    "content":"eWallet is an Django based project."})

def merchants_page(request):
    return render_to_response("info_page.html",{"title":"eWallet:Merchants",
                                                    "content":"ADSL \n Harilo"})

def partner_banks_page(request):
    return render_to_response("info_page.html",{"title":"eWallet:Banking Partners",
                                                    "content":"Nabil Bank \n Kumari Bank"})
