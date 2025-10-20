from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import permission_required

from .forms import CustomerForm
from .models import Customer


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

@permission_required('customers.view_customer', login_url='/admin/login/', raise_exception=False)
def clients_list(request):
    qs = Customer.objects.all().order_by('-created_at')
    q = request.GET.get('q', '').strip()
    name = request.GET.get('name', '').strip()
    email = request.GET.get('email', '').strip()
    region = request.GET.get('region', '').strip()

    if q:
        qs = qs.filter(Q(customer_name__icontains=q) | Q(customer_email__icontains=q))
    else:
        if name:
            qs = qs.filter(customer_name__icontains=name)
        if email:
            qs = qs.filter(customer_email__icontains=email)

    if region:
        qs = qs.filter(region__iexact=region)

    paginator = Paginator(qs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'customers': page_obj,            
        'page_obj': page_obj,             
        'name_filter': name,
        'email_filter': email,
        'region_filter': region,
        'q': q,
        'regions': Customer.REGION_CHOICES,
    }
    return render(request, 'customers/clients_list.html', context)