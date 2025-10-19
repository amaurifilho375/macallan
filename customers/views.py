from django.shortcuts import render, redirect
from .forms import CustomerForm
from django.urls import reverse

def macallan_form(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('macallan_success'))
    else:
        form = CustomerForm()
    return render(request, 'customers/macallan_form.html', {'form': form})

def macallan_success(request):
    return render(request, 'customers/macallan_success.html')
