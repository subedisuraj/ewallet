__author__ = 'Dell'



from django import forms

days=[]
for day in range(1,32):
    d = [(str(day),str(day)),]
    days += d

years=[]
for year in range(2021,1950,-1):
    y = [(str(year),str(year)),]
    years += y

months = [('1','Jan'),('2','Feb'),('3','Mar'),('4','Apr'),('5','May'),('6','Jun'),
         ('7','Jul'),('8','Aug'),('9','Sep'),('10','Oct'),('11','Nov'),('12','Dec')]



class Ew_registration_form(forms.Form):

    fname = forms.CharField()
    mname = forms.CharField(required = False)
    lname = forms.CharField()
#    address = forms.CharField()

    contact = forms.CharField(required = False)

    username = forms.CharField(label='My username')
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    citizenship_no = forms.CharField(required=False)
    dob_yr = forms.ChoiceField(choices = years,required=False)
    dob_mth = forms.ChoiceField(choices = months,required=False)
    dob_day = forms.ChoiceField(choices = days,initial="Day",required=False)

    b1_fname = forms.CharField(required = False)
    b1_mname = forms.CharField(required = False)
    b1_lname = forms.CharField(required = False)
    b1_citizenship_no = forms.CharField(required=False)

    b2_fname = forms.CharField(required = False)
    b2_mname = forms.CharField(required = False)
    b2_lname = forms.CharField(required = False)
    b2_citizenship_no = forms.CharField(required=False)




class Statement_form(forms.Form):
    stat_pp = forms.CharField(required = False ,widget=forms.TextInput(attrs={'class' : 'span1'}))
    sort = forms.ChoiceField(choices = [('date','Date'),('transaction_partner','Transaction Partner')],required=False)
    fyear = forms.ChoiceField(choices = years,required=False)
    fmth = forms.ChoiceField(choices = months,required=False)
    fday = forms.ChoiceField(choices = days,required=False)
    tyear = forms.ChoiceField(choices = years,required=False)
    tmth = forms.ChoiceField(choices = months,required=False)
    tday = forms.ChoiceField(choices = days,required=False)



