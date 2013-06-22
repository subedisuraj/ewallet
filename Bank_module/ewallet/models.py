from django.db import models

# Create your models here.





class Ewalletusers(models.Model):
    username = models.CharField(max_length=32,db_column='Username')
    current_balance = models.IntegerField(db_column='Current Balance')
#    code = models.CharField(max_length=6,blank=True,null=True)
#    status = models.BooleanField()



class User_details(models.Model):
#    user_id = models.CharField(max_length=32) # primary key for the database ; hash value of username and password
    fname = models.CharField(max_length=32,db_column='First Name')
    mname = models.CharField(max_length=32,blank=True,db_column='Middle Name')
    lname = models.CharField(max_length=32,db_column='Last Name')
    username = models.CharField(max_length=32  , primary_key=True,db_column='Username')
    email = models.EmailField(max_length = 100,db_column='Email')
    password = models.CharField(max_length=64,db_column='Password')
    contact = models.CharField(max_length=13,blank=True,db_column='Contact No.')


    def __unicode__(self):
        return (self.fname + " " + self.lname)


class Statements(models.Model):                                    # statements table of a user
    user = models.ForeignKey(User_details, db_column='User')
    transaction_partner = models.CharField(max_length=20, db_column = 'Transaction Partner')
    statement_des = models.CharField(max_length=100,db_column='Statement Description')
    date = models.CharField(max_length=100,db_column='Date')
    time = models.CharField(max_length=100,db_column='Time')
    amount = models.IntegerField(max_length=10,db_column='Amount')


class Beneficiary(models.Model):
    user = models.ForeignKey(User_details,db_column="Username",)
    ctzen = models.CharField(max_length=50,db_column="Citizenship No",blank= True)
    dob = models.DateField(db_column="DOB",blank = True)
    b1_fname = models.CharField(max_length=100,db_column= "1.First Name",blank=True)
    b1_mname = models.CharField(max_length=100,db_column= "1.Middle Name",blank=True)
    b1_lname = models.CharField(max_length=100,db_column= "1.Last Name",blank=True)
    b1_ctzen = models.CharField(max_length=50,db_column="1.Citizenship No",blank= True)
    b2_fname = models.CharField(max_length=100,db_column= "2.First Name",blank=True)
    b2_mname = models.CharField(max_length=100,db_column= "2.Middle Name",blank=True)
    b2_lname = models.CharField(max_length=100,db_column= "2.Last Name",blank=True)
    b2_ctzen = models.CharField(max_length=50,db_column="2.Citizenship No",blank= True)


class Adslusers(models.Model):
    username = models.CharField(max_length=7,db_column= "Telephone Number",blank=True)

