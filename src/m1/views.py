from django.shortcuts import render
from m1.forms import RifleDateForm
from m1.tasks import rifle_data
from pprint import pprint


def index(request):
    context = {
        'title': 'US Rifle M1.com'
    }
    if request.headers.get('Host') in ['localhost', 'localhost:8000', '127.0.0.1', '127.0.0.1:8000']:
        display_ga = False
    else:
        display_ga = True
    context['display_ga'] = display_ga
    if request.method == 'POST':
        form = RifleDateForm(request.POST)
        if form.is_valid():
            try:
                rifle = rifle_data(form.cleaned_data)
            except Exception as e:
                print('=== problem getting rifle ===')
                print(e)
            
            if not rifle:
                print(f'FAILED TO FIND RIFLE: s/n {request.POST.get("serial_number")}, maker {request.POST.get("maker")}')
                form = RifleDateForm()
                return render(request, 'm1/index.html', {'rifle': False, 'error': True, 'form': form})

            if rifle.get('stock', {}).get('notes'):
                stock = f'{rifle.get("stock", {}).get("cartouche")} Note: {rifle.get("stock").get("notes")}'
            else:
                stock = f'{rifle.get("stock", {}).get("cartouche")}'
            
            context['rifle'] = {
                'Maker': 'Springfield Armory' if rifle.get('maker') == 'SA' else 'Winchester Repeating Arms',
                'Serial Number': rifle.get('sn'),
                'Month': rifle.get('month'),
                'Year': rifle.get('year'),
                'Stock Cartouche': stock,
                'Possible Op Rods': [f'{r["drawing_number"]} with a s/n range of {r["notes"]}' for r in rifle.get('op_rods', [])],
                'Possible Bolts': [f'{r["drawing_number"]} with a s/n range of {r["sn_range"]}' for r in rifle.get('bolts')],
                'Possible Bullet Guides': [f'{r["drawing_number"]} with a s/n range of {r["sn_range"]}. {r["notes"]}' for r in rifle.get('bullet_guides')],
                
            }
            form = RifleDateForm()
        else:
            form = RifleDateForm()
    else:
        form = RifleDateForm()
    context['form'] = form
    return render(request, 'm1/index.html', context)
