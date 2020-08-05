from django.shortcuts import render
from django.http import HttpResponse
from .models import Patient
import datetime
from django import forms



'''def PRO(request):
    if request.method == 'POST':
        code = request.POST.get('t1', None)
        date = request.POST.get('t2', None)
        month = request.POST.get('t3', None)
        year = request.POST.get('t4', None)
        patients = Patient.objects.filter(pro_code = code, coupon_date = datetime.date(year, month, date))
        return render(request, 'main/display.html')

    else:
        return render(request, 'main/form1.html')
'''

class receptionDataForm(forms.Form):
    month = forms.IntegerField(label = 'month')
    year = forms.IntegerField(label = 'year')

def reception(request):
    if request.method == 'POST':
        form = receptionDataForm(request.POST)
        if form.is_valid():
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            patients = Patient.objects.filter(coupon_date__month = month, coupon_date__year = year)
            return render(request, 'main/display.html', {'patients': patients})
    else:
        form = receptionDataForm()
    return render(request, 'main/form1.html', {'form': form})

def new_patient(request):
    if request.method == 'POST':
        form = newPatientForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phNo = form.cleaned_data['phNo']
            code = form.cleaned_data['proCode']
            lastCouponNumber = len(Patient.objects.all())
            couponNumber = lastCouponNumber+1
            new_patient = Patient(patient_name = name, patient_ph = phNo, pro_code = code, coupon_number = couponNumber, coupon_status = False)
            new_patient.save()
            patients = Patient.objects.filter(pro_code = code, coupon_date = datetime.date.today())
            return render(request, 'main/display.html', {'patients': patients})
    else:
        form = newPatientForm() 
        return render(request, "main/form1.html", {'form': form})

def verify_patient(request):
    if request.method == 'POST':
        form = verifyPatientForm(request.POST)
        if form.is_valid():
            couponNumber = form.cleaned_data['couponNumber']
            phNo = form.cleaned_data['phNo']
            patients = Patient.objects.filter(coupon_number = couponNumber, patient_ph = phNo)
            if (len(patients) == 0):
                return render(request, "main/error.html", {'couponNumber': couponNumber, 'phNo': phNo})
            else:
                patients1 = Patient.objects.get(coupon_number = couponNumber, patient_ph = phNo)
                patients1.coupon_status = True
                patients1.save()
                patients = Patient.objects.filter(coupon_number = couponNumber, patient_ph = phNo)
                return render(request, "main/display.html", {'patients': patients})
    else:
        form = verifyPatientForm()
        return render(request, "main/form1.html", {'form': form})

class proDataForm(forms.Form):
    proCode = forms.CharField(label = 'PRO CODE', max_length = 5)
    month = forms.IntegerField(label = 'month')
    year = forms.IntegerField(label = 'year')


def get_proData(request):
    if request.method == 'POST':
        form = proDataForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['proCode']
            month = form.cleaned_data['month']
            year = form.cleaned_data['year']
            patients = Patient.objects.filter(pro_code = code, coupon_date__month = month, coupon_date__year = year)
            return render(request, 'main/display.html', {'patients': patients})
    else:
        form = proDataForm()
    return render(request, 'main/form1.html', {'form': form})

class newPatientForm(forms.Form):
    name = forms.CharField(label = 'Patient Name', max_length = 45)
    phNo = forms.IntegerField(label = 'Patient Phone Number')
    proCode = forms.CharField(label = 'PRO CODE', max_length = 5)


class verifyPatientForm(forms.Form):
    couponNumber = forms.IntegerField(label = 'Coupon Number')
    phNo = forms.IntegerField(label = 'Patient Phone Number')

