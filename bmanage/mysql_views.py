from .models import *


class CheckAccounts(models.Model):
    accountid = models.CharField(db_column='accountID', primary_key=True, max_length=6)
    bank = models.CharField(max_length=20)
    accounttype = models.CharField(max_length=10, blank=True, null=True)
    money = models.FloatField()
    settime = models.DateTimeField(blank=True, null=True)
    overdraft = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'checkaccounts'


class CheckStat(models.Model):
    bank = models.CharField(primary_key=True, max_length=20)
    totalmoney = models.FloatField()
    totalcustomer = models.DurationField()

    class Meta:
        db_table = 'checkstat'


class LoanStat(models.Model):
    bank = models.CharField(primary_key=True, max_length=20)
    totalmoney = models.FloatField()
    totalcustomer = models.DurationField()

    class Meta:
        db_table = 'loanstat'


class SaveStat(models.Model):
    bank = models.CharField(primary_key=True, max_length=20)
    totalmoney = models.FloatField()
    totalcustomer = models.DurationField()

    class Meta:
        db_table = 'savestat'


class SaveAccounts(models.Model):
    accountid = models.CharField(db_column='accountID', primary_key=True, max_length=6)
    bank = models.CharField(max_length=20)
    accounttype = models.CharField(max_length=10, blank=True, null=True)
    money = models.FloatField()
    settime = models.DateTimeField(blank=True, null=True)
    interestrate = models.FloatField(blank=True, null=True)
    savetype = models.CharField(max_length=1, blank=True, null=True)

    class Meta:
        db_table = 'saveaccounts'