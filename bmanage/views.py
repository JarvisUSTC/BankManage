from django.shortcuts import render
from django.db.models import Count
# 导入 HttpResponse 模块
from django.http import HttpResponse
from .models import Customer, Cusforloan
from .models import Accounts, Checkacc, Saveacc, Cusforacc
from .models import Employee
from django.contrib import messages
from django.utils import timezone  # 引入timezone模块
from .models import Bank
from .models import Loan, Payinfo
from .mysql_views import SaveAccounts
import datetime


# 视图函数


def login(request):
    return render(request, 'base.html')


def customer_manage_add(request):
    res_list = Employee.objects.all()
    if request.method == "POST":
        cus_id = request.POST.get('cusID')
        cus_name = request.POST.get('cusName')
        cus_phone = request.POST.get('cusPhone')
        address = request.POST.get('address', None)
        contact_phone = request.POST.get('contactPhone')
        contact_name = request.POST.get('contactName')
        contact_email = request.POST.get('contactEmail', None)
        relation = request.POST.get('relation')
        loan_res = request.POST.get('loanRes', None)
        acc_res = request.POST.get('accRes', None)
        loan_object = Employee.objects.filter(empid=loan_res).first()
        acc_object = Employee.objects.filter(empid=acc_res).first()
        # if len(loan_res) == 0:
        #     loan_res = None
        # if len(acc_res) == 0:
        #     acc_res = None
        if Customer.objects.filter(cusid=cus_id):
            # 主键冲突
            messages.success(request, 'This customer id has already existed')
        else:
            Customer.objects.create(cusid=cus_id, cusname=cus_name, cusphone=cus_phone,
                                    address=address, contact_phone=contact_phone, contact_name=contact_name,
                                    contact_email=contact_email, relation=relation, loanres=loan_object,
                                    accres=acc_object)
            messages.success(request, 'Add Successfully')
    return render(request, 'customerAdd.html', locals())


def customer_manage_del(request):
    cus_list = Customer.objects.all()
    if request.method == "POST":
        cus_id = request.POST.get('cusID')
        obj = Customer.objects.filter(cusid=cus_id)
        if Cusforloan.objects.filter(cusid=cus_id) or Cusforacc.objects.filter(cusid=cus_id):
            messages.success(request, 'This customer is in the relevant accounts and loans, delete false')
        elif obj:
            obj.delete()
            messages.success(request, 'Delete Successfully')
        else:
            messages.success(request, 'This id does not exist')
    return render(request, 'customerDel.html', locals())


def customer_manage_mod(request):
    cus_list = Customer.objects.all()
    res_list = Employee.objects.all()
    if request.method == "POST":
        cus_id = request.POST.get('cusID')
        cus_name = request.POST.get('cusName')
        cus_phone = request.POST.get('cusPhone')
        address = request.POST.get('address', None)
        contact_phone = request.POST.get('contactPhone')
        contact_name = request.POST.get('contactName')
        contact_email = request.POST.get('contactEmail', None)
        relation = request.POST.get('relation')
        loan_res = request.POST.get('loanRes', None)
        acc_res = request.POST.get('accRes', None)
        loan_object = Employee.objects.filter(empid=loan_res).first()
        acc_object = Employee.objects.filter(empid=acc_res).first()
        Customer.objects.filter(cusid=cus_id).update(cusname=cus_name, cusphone=cus_phone, address=address,
                                                     contact_phone=contact_phone, contact_name=contact_name,
                                                     contact_email=contact_email, relation=relation,
                                                     loanres=loan_object, accres=acc_object)
        messages.success(request, 'Update Successfully')
        return render(request, 'customerMod.html', locals())
    return render(request, 'customerMod.html', locals())


def customer_manage_found(request):
    cus_list = Customer.objects.all()
    if request.method == "POST":
        res_list = Employee.objects.all()
        cus_id = request.POST.get('cusID')
        cus_obj = Customer.objects.filter(cusid=cus_id).first()
        if cus_obj:
            return render(request, 'customerMod2.html', locals())
        else:
            messages.success(request, 'This id does not exist')
    return render(request, 'customerfound.html', locals())


def account_add(request):
    obj_list = Customer.objects.all()
    bank_list = Bank.objects.all()
    if request.method == "POST":
        acc_id = request.POST.get('accID')
        money = request.POST.get('money')
        acc_type = request.POST.get('accType')
        cus_id_list = request.POST.getlist('cusIDList')
        bank = request.POST.get('bank')
        bank_obj = Bank.objects.filter(bankname=bank).first()
        if len(bank) == 0:
            bank = None
        settime = request.POST.get('settime')
        if Accounts.objects.filter(accountid=acc_id):
            messages.success(request, 'This account id has existed')
            return render(request, 'accountAdd.html', locals())
        obj = Accounts.objects.create(accountid=acc_id, money=money, accounttype=acc_type, settime=settime)
        for cus_id in cus_id_list:
            cus_obj = Customer.objects.filter(cusid=cus_id).first()
            Cusforacc.objects.create(accountid=obj, bank=bank_obj, cusid=cus_obj, accounttype=acc_type)
        if acc_type == "SavingAccount":
            interestrate = request.POST.get('interestrate')
            if len(interestrate) == 0:
                interestrate = 0
            savetype = request.POST.get('savetype')
            Saveacc.objects.create(accountid=obj, interestrate=interestrate, savetype=savetype)
        else:
            overdraft = request.POST.get('overdraft')
            if len(overdraft) == 0:
                overdraft = 0
            Checkacc.objects.create(accountid=obj, overdraft=overdraft)
        messages.success(request, 'Add Account Successfully')
    return render(request, 'accountAdd.html', locals())


def account_del(request):
    accID_list = Accounts.objects.all()
    if request.method == 'POST':
        acc_id = request.POST.get('accID')
        obj = Accounts.objects.filter(accountid=acc_id)
        if not obj:
            messages.success(request, 'This account id doesn\'t exist')
            return render(request, 'accountDel.html')
        acc_type = obj[0].accounttype
        if acc_type == "SavingAccount":
            Saveacc.objects.filter(accountid=obj[0].accountid).delete()
        else:
            Checkacc.objects.filter(accountid=obj[0].accountid).delete()
        Cusforacc.objects.filter(accountid=obj[0].accountid).delete()
        obj.delete()
        messages.success(request, 'Delete Account Successfully')
    return render(request, 'accountDel.html', locals())


def account_mod(request):
    accID_list = Accounts.objects.all()
    if request.method == 'POST':
        acc_id = request.POST.get("accID")
        acc_type = request.POST.get("accType")
        money = request.POST.get("money")
        Accounts.objects.filter(accountid=acc_id).update(money=money)
        if acc_type == "SavingAccount":
            interestrate = request.POST.get("interestrate")
            savetype = request.POST.get("savetype")
            Saveacc.objects.filter(accountid=acc_id).update(interestrate=interestrate, savetype=savetype)
        else:
            overdraft = request.POST.get("overdraft")
            Checkacc.objects.filter(accountid=acc_id).update(overdraft=overdraft)
        messages.success(request, 'Update Successfully')
    return render(request, 'accountMod.html', locals())


def account_found(request):
    accID_list = Accounts.objects.all()
    if request.method == "POST":
        time_now = timezone.now()  # 输出time_now即为当然日期和时间
        acc_id = request.POST.get('accID')
        acc_obj_list = Accounts.objects.filter(accountid=acc_id)
        Cusforacc.objects.filter(accountid=acc_id).update(visit=time_now.strftime("%Y-%m-%d %H:%M:%S"))
        cus_obj_list = Cusforacc.objects.filter(accountid=acc_id)
        if len(acc_obj_list) != 0:
            acc_obj = acc_obj_list[0]
            acc_type = cus_obj_list[0].accounttype
            bank = cus_obj_list[0].bank
            if acc_type == "SavingAccount":
                save_obj = Saveacc.objects.filter(accountid=acc_id)[0]
            else:
                check_obj = Checkacc.objects.filter(accountid=acc_id)[0]
            return render(request, 'accountMod2.html', locals())
        else:
            messages.success(request, 'This account id does not exist')
    return render(request, 'accountFound.html', locals())


def loan_add(request):
    obj_list = Customer.objects.all()
    bank_list = Bank.objects.all()
    if request.method == 'POST':
        loan_id = request.POST.get('loanID')
        if Loan.objects.filter(loanid=loan_id):
            messages.success(request, 'This loan id has existed')
            return render(request, 'loanAdd.html', locals())
        bank = request.POST.get('bank')
        bank_obj = Bank.objects.filter(bankname=bank).first()
        cus_id_list = request.POST.getlist('cusIDList')
        money = request.POST.get('money')
        loan_obj = Loan.objects.create(loanid=loan_id, money=money, bank=bank_obj, state='0')
        for cus_id in cus_id_list:
            cus_obj = Customer.objects.filter(cusid=cus_id).first()
            Cusforloan.objects.create(cusid=cus_obj, loanid=loan_obj)
        messages.success(request, 'Add Loan Successfully')
    return render(request, 'loanAdd.html', locals())


def loan_del(request):
    loanID_list = Loan.objects.all()
    if request.method == 'POST':
        loan_id = request.POST.get('loanID')
        loan_obj = Loan.objects.filter(loanid=loan_id).first()
        if loan_obj.state == '1':
            messages.success(request, 'This loan is issuing, can not delete')
        else:
            Cusforloan.objects.filter(loanid=loan_id).delete()
            loan_obj.delete()
            messages.success(request, 'Delete successfully')
    return render(request, 'loanDel.html', locals())


def loan_found(request):
    loanID_list = Loan.objects.all()
    if request.method == 'POST':
        load_id = request.POST.get('loanID')
        loan_obj = Loan.objects.filter(loanid=load_id).first()
        cus_obj_list = Cusforloan.objects.filter(loanid=load_id)
        state_loan = loan_obj.state
        if state_loan == '0':
            state = "贷款未发放"
        elif state_loan == '1':
            state = "贷款正在发放"
        else:
            state = "贷款发放完成"
    return render(request, 'loanFound.html', locals())


def loan_issue(request):
    loanID_list = Loan.objects.all()
    if request.method == 'GET':
        loan_id = request.GET.get('loanID')
        obj_list = Cusforloan.objects.filter(loanid=loan_id)
    if request.method == 'POST':
        loan_id = request.POST.get('loanID')
        cus_id = request.POST.get('cusID')
        money = request.POST.get('money')
        loan_obj = Loan.objects.filter(loanid=loan_id).first()
        cus_obj = Customer.objects.filter(cusid=cus_id).first()
        time_now = timezone.now()  # 输出time_now即为当然日期和时间
        try:
            Payinfo.objects.create(loanid=loan_obj, cusid=cus_obj, money=money,
                                   paytime=time_now.strftime("%Y-%m-%d %H:%M:%S"))
        except Exception as e:
            messages.error(request, '发放贷款金额超出应发金额')
    return render(request, 'loanIssue.html', locals())


def save_statistics(request):
    # 月/季/年使用GET 具体支行使用POST
    bank_list = Bank.objects.all()
    if request.method == 'POST':
        bank = request.POST.get("bank")
        year = int(request.POST.get("year"))
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
        month_money = []
        month_customer = []
        season_money = []
        season_customer = []
        for i in range(12):
            start_date = datetime.date(year, i+1, 1)
            end_date = datetime.date(year + int((i+1 - (i+1) % 12)/12), (i+1) % 12 + 1, 1)
            m_queryset = SaveAccounts.objects.filter(bank=bank, settime__range=(start_date, end_date))
            money = 0
            customer = 0
            for q in m_queryset:
                c = Cusforacc.objects.filter(accountid=q.accountid).aggregate(customer_num=Count('cusid', distinct=True))
                customer += c['customer_num']
                money += q.money
            month_money.append(money)
            month_customer.append(customer)
        print(month_customer)
        for i in range(0, 4):
            start_date = datetime.date(year, i*3+1, 1)
            end_date = datetime.date(year + int(((i+1)*3 - ((i+1)*3) % 12)/12), ((i+1)*3) % 12 + 1, 1)
            m_queryset = SaveAccounts.objects.filter(bank=bank, settime__range=(start_date, end_date))
            money = 0
            customer = 0
            for q in m_queryset:
                c = Cusforacc.objects.filter(accountid=q.accountid).aggregate(customer_num=Count('cusid', distinct=True))
                customer += c['customer_num']
                money += q.money
            season_money.append(money)
            season_customer.append(customer)
        bank_money_year = []
        bank_customer_year = []
        bank_names = []
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year + 1, 1, 1)
        for bank_obj in bank_list:
            bank_name = bank_obj.bankname
            acc_obj = SaveAccounts.objects.filter(bank=bank_name, settime__range=(start_date, end_date))
            bank_names.append(bank_name)
            money = 0
            customer = 0
            for acc in acc_obj:
                c = Cusforacc.objects.filter(accountid=acc.accountid).aggregate(
                    customer_num=Count('cusid', distinct=True))
                customer += c['customer_num']
                money += acc.money
            bank_money_year.append(money)
            bank_customer_year.append(customer)
        zip_month_money = zip(months, month_money)
        zip_month_customer = zip(months, month_customer)
        zip_season_money = zip(seasons, season_money)
        zip_season_customer = zip(seasons, season_customer)
        zip_year_money = zip(bank_names, bank_money_year)
        zip_year_customer = zip(bank_names, bank_customer_year)
        print(bank_money_year)
        print(bank_names)
        print(bank_customer_year)

    return render(request, 'saveStatistics.html', locals())


def loan_statistics(request):
    bank_list = Bank.objects.all()
    if request.method == 'POST':
        bank = request.POST.get("bank")
        year = int(request.POST.get("year"))
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
        seasons = ['Spring', 'Summer', 'Autumn', 'Winter']
        month_money = []
        month_customer = []
        season_money = []
        season_customer = []
        for i in range(12):
            start_date = datetime.date(year, i + 1, 1)
            end_date = datetime.date(year + int((i + 1 - (i + 1) % 12) / 12), (i + 1) % 12 + 1, 1)
            loan_queryset = Loan.objects.filter(bank=bank)
            money = 0
            customer = 0
            for loan in loan_queryset:
                payinfo_queryset = Payinfo.objects.filter(loanid=loan.loanid, paytime__range=(start_date, end_date))
                for payinfo in payinfo_queryset:
                    money += payinfo.money
                c = Payinfo.objects.filter(loanid=loan.loanid, paytime__range=(start_date, end_date)).aggregate(
                    customer_num=Count('cusid', distinct=True))
                customer += c['customer_num']
            month_money.append(money)
            month_customer.append(customer)
        print(month_customer)
        for i in range(0, 4):
            start_date = datetime.date(year, i * 3 + 1, 1)
            end_date = datetime.date(year + int(((i + 1) * 3 - ((i + 1) * 3) % 12) / 12), ((i + 1) * 3) % 12 + 1, 1)
            loan_queryset = Loan.objects.filter(bank=bank)
            money = 0
            customer = 0
            for loan in loan_queryset:
                payinfo_queryset = Payinfo.objects.filter(loanid=loan.loanid, paytime__range=(start_date, end_date))
                for payinfo in payinfo_queryset:
                    money += payinfo.money
                c = Payinfo.objects.filter(loanid=loan.loanid, paytime__range=(start_date, end_date)).aggregate(
                    customer_num=Count('cusid', distinct=True))
                customer += c['customer_num']
            season_money.append(money)
            season_customer.append(customer)
        bank_money_year = []
        bank_customer_year = []
        bank_names = []
        start_date = datetime.date(year, 1, 1)
        end_date = datetime.date(year + 1, 1, 1)
        for bank_obj in bank_list:
            bank_name = bank_obj.bankname
            loan_queryset = Loan.objects.filter(bank=bank_name)
            bank_names.append(bank_name)
            money = 0
            customer = 0
            for loan in loan_queryset:
                payinfo_queryset = Payinfo.objects.filter(loanid=loan.loanid, paytime__range=(start_date, end_date))
                for payinfo in payinfo_queryset:
                    money += payinfo.money
                c = Payinfo.objects.filter(loanid=loan.loanid, paytime__range=(start_date, end_date)).aggregate(
                    customer_num=Count('cusid', distinct=True))
                customer += c['customer_num']
            bank_money_year.append(money)
            bank_customer_year.append(customer)
        zip_month_money = zip(months, month_money)
        zip_month_customer = zip(months, month_customer)
        zip_season_money = zip(seasons, season_money)
        zip_season_customer = zip(seasons, season_customer)
        zip_year_money = zip(bank_names, bank_money_year)
        zip_year_customer = zip(bank_names, bank_customer_year)
        print(bank_money_year)
        print(bank_names)
        print(bank_customer_year)

    return render(request, 'loanStatistics.html', locals())