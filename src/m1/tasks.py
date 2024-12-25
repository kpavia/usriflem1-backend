from m1.models import Receiver


def rifle_data(data):
    sn = int(data.get('serial_number'))
    maker = data.get('maker')
    receiver = Receiver.objects.filter(
        maker=maker,
        starting_serial__lte=sn,
        ending_serial__gte=sn
    ).first()
    if receiver:
        return {'month': receiver.month, 'year': receiver.year, 'sn': sn, 'maker': receiver.maker}
    return {}
