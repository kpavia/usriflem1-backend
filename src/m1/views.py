from django.shortcuts import render
from m1.forms import RifleDateForm
from m1.tasks import rifle_data


def index(request):
    context = {
        'title': 'US Rifle M1.com'
    }
    if request.method == 'POST':
        form = RifleDateForm(request.POST)
        if form.is_valid():
            rifle = rifle_data(form.cleaned_data)
            context['rifle_month'] = rifle.get('month')
            context['rifle_year'] = rifle.get('year')
            context['rifle_sn'] = rifle.get('sn')
            form = RifleDateForm()
        else:
            form = RifleDateForm()
    else:
        form = RifleDateForm()
    context['form'] = form
    return render(request, 'm1/index.html', context)
