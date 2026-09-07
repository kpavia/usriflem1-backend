from django.shortcuts import render
from django.db.models import (Case, When, Value, IntegerField)
from m1.forms import RifleDateForm
from m1.tasks import rifle_data, get_videos
from m1.models import Video
from m1.serializers import (VideoSerializer, SerialNumberMakerSerializer)
from rest_framework import (generics, status)
from rest_framework.views import APIView
from rest_framework.response import Response


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
                'Possible Trigger Housings': [f'{r["drawing_number"]} {r["notes"]}' for r in rifle.get('trigger_housings')],
                'Possible Trigger Guards': [f'{r["drawing_number"]}, Notes: {r["notes"]}' for r in rifle.get('trigger_guards')],
                'Possible Triggers': [f'{r["drawing_number"]}, Notes: {r["notes"]}' for r in rifle.get('triggers')],
                'Possible Safeties': [f'{r["drawing_number"]}, Notes: {r["notes"]}' for r in rifle.get('safeties')],
                'Possible Hammers': [f'{r["drawing_number"]}, Notes: {r["notes"]}' for r in rifle.get('hammers')],
                'Possible followers': [f'{r["revision_number"]}, Notes: {r["notes"]}' for r in rifle.get('followers')]
            }
            form = RifleDateForm()
        else:
            form = RifleDateForm()
    else:
        form = RifleDateForm()
    context['form'] = form
    return render(request, 'm1/index.html', context)


def education_view(request):
    videos = get_videos()
    pprint(videos.get('principles_of_operation').title)
    return render(request, 'm1/base_education.html', videos)


class VideoListView(generics.ListAPIView):
    serializer_class = VideoSerializer

    def get_queryset(self):
        category_order = Case(
            When(category=Video.MILITARY, then=Value(0)),
            When(category=Video.MAINTENANCE, then=Value(1)),
            When(category=Video.PRODUCTION_HISTORY, then=Value(2)),
            output_field=IntegerField(),
        )
        return Video.objects.annotate(category_rank=category_order).order_by('category_rank', 'order')


class SerialNumberView(APIView):

    def get(self, request):
        serial_number = request.query_params.get('serial_number')
        maker = request.query_params.get('maker')
        serializer = SerialNumberMakerSerializer(data={'serial_number': serial_number, 'maker': maker})
        if serializer.is_valid(raise_exception=True):
            rifle = rifle_data(serializer.validated_data)
            return Response(rifle, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
