from django.db import models                                        # import the model base class from django library
#from Banks import models as Bank_models


class Users_bank_details(models.Model):                              # bank details of the bank user
#    bank_name = models.ForeignKey(Bank_models.Banks)
    account_no = models.CharField(max_length=10,primary_key=True,db_column='Account No.')
    pin_no = models.CharField(max_length=8,db_column='Pin No.')
    current_balance = models.IntegerField(max_length=20,db_column='Current Balance')


class Bank_users(models.Model):                                    #personal profile of the bank user
    bank_details = models.ForeignKey(Users_bank_details, db_column='Bank User')
    name = models.CharField(max_length=60,db_column='Name')
    username = models.CharField(max_length=32,primary_key=True,db_column='Username')
    password = models.CharField(max_length=64,db_column='Password')
#    def __unicode__(self):
#        return self.name


class Statements(models.Model):                                    # statements table of a user
    user = models.ForeignKey(Bank_users , db_column='User')
    statement_des = models.CharField(max_length=100,db_column='Statement Description')
    date = models.CharField(max_length=100,db_column='Date')
    time = models.CharField(max_length=100,db_column='Time')


class Outgoing_pends(models.Model):
    from_account = models.CharField(max_length=10,db_column='From Account No.')
    to_account = models.CharField(max_length=10, db_column='To Account No.')
    to_bank = models.CharField(max_length=20, db_column='To Bank')
    amount = models.IntegerField(db_column='Amount')
    status = models.BooleanField(db_column='Status of Transaction')

class Incoming_pends(models.Model):
    from_account = models.CharField(max_length=10,db_column='From Account No.')
    to_account = models.CharField(max_length=10,db_column='To Account No.')
    from_bank = models.CharField(max_length=20,db_column='From Bank')
    amount = models.IntegerField(db_column='Amount')
    status = models.BooleanField(db_column='Status of Transaction')
