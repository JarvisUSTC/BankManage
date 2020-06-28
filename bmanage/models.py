# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Accounts(models.Model):
    accountid = models.CharField(db_column='accountID', primary_key=True, max_length=6)  # Field name made lowercase.
    money = models.FloatField()
    settime = models.DateTimeField(blank=True, null=True)
    accounttype = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'accounts'


class Bank(models.Model):
    bankname = models.CharField(primary_key=True, max_length=20)
    city = models.CharField(max_length=20)
    money = models.FloatField()

    class Meta:
        managed = True
        db_table = 'bank'


class Checkacc(models.Model):
    accountid = models.OneToOneField(Accounts, models.DO_NOTHING, db_column='accountID', primary_key=True)  # Field name made lowercase.
    overdraft = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'checkacc'


class Cusforacc(models.Model):
    accountid = models.OneToOneField(Accounts, models.DO_NOTHING, db_column='accountID', primary_key=True)  # Field name made lowercase.
    bank = models.ForeignKey(Bank, models.DO_NOTHING, db_column='bank', blank=True, null=True)
    cusid = models.ForeignKey('Customer', models.DO_NOTHING, db_column='cusID')  # Field name made lowercase.
    visit = models.DateTimeField(blank=True, null=True)
    accounttype = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'cusforacc'
        unique_together = (('accountid', 'cusid'), ('bank', 'cusid', 'accounttype'),)


class Cusforloan(models.Model):
    loanid = models.OneToOneField('Loan', models.DO_NOTHING, db_column='loanID', primary_key=True)  # Field name made lowercase.
    cusid = models.ForeignKey('Customer', models.DO_NOTHING, db_column='cusID')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'cusforloan'
        unique_together = (('loanid', 'cusid'),)


class Customer(models.Model):
    cusid = models.CharField(db_column='cusID', primary_key=True, max_length=18)  # Field name made lowercase.
    cusname = models.CharField(max_length=10)
    cusphone = models.CharField(max_length=11)
    address = models.CharField(max_length=50, blank=True, null=True)
    contact_phone = models.CharField(max_length=11)
    contact_name = models.CharField(max_length=10)
    contact_email = models.CharField(db_column='contact_Email', max_length=20, blank=True, null=True)  # Field name made lowercase.
    relation = models.CharField(max_length=10)
    loanres = models.ForeignKey('Employee', models.DO_NOTHING, db_column='loanres', blank=True, null=True, related_name='loan')
    accres = models.ForeignKey('Employee', models.DO_NOTHING, db_column='accres', blank=True, null=True, related_name='acc')

    class Meta:
        managed = True
        db_table = 'customer'


class Department(models.Model):
    departid = models.CharField(db_column='departID', primary_key=True, max_length=4)  # Field name made lowercase.
    departname = models.CharField(max_length=20)
    departtype = models.CharField(max_length=15, blank=True, null=True)
    manager = models.CharField(max_length=18)
    bank = models.ForeignKey(Bank, models.DO_NOTHING, db_column='bank')

    class Meta:
        managed = True
        db_table = 'department'


class Employee(models.Model):
    empid = models.CharField(db_column='empID', primary_key=True, max_length=18)  # Field name made lowercase.
    empname = models.CharField(max_length=20)
    empphone = models.CharField(max_length=11, blank=True, null=True)
    empaddr = models.CharField(max_length=50, blank=True, null=True)
    emptype = models.CharField(max_length=1, blank=True, null=True)
    empstart = models.DateField()
    depart = models.ForeignKey(Department, models.DO_NOTHING, db_column='depart', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'employee'


class Loan(models.Model):
    loanid = models.CharField(db_column='loanID', primary_key=True, max_length=4)  # Field name made lowercase.
    money = models.FloatField(blank=True, null=True)
    bank = models.ForeignKey(Bank, models.DO_NOTHING, db_column='bank', blank=True, null=True)
    state = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'loan'


class Payinfo(models.Model):
    loanid = models.OneToOneField(Loan, models.DO_NOTHING, db_column='loanID', primary_key=True)  # Field name made lowercase.
    cusid = models.ForeignKey(Customer, models.DO_NOTHING, db_column='cusID')  # Field name made lowercase.
    money = models.FloatField()
    paytime = models.DateTimeField()

    class Meta:
        managed = True
        db_table = 'payinfo'
        unique_together = (('loanid', 'cusid', 'money', 'paytime'),)


class Saveacc(models.Model):
    accountid = models.OneToOneField(Accounts, models.DO_NOTHING, db_column='accountID', primary_key=True)  # Field name made lowercase.
    interestrate = models.FloatField(blank=True, null=True)
    savetype = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'saveacc'
