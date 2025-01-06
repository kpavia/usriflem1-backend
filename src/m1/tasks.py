from m1.models import Receiver, OpRod


def get_op_rod(sn, maker):
    op_rods = OpRod.objects.all()
    ww2_rods = op_rods.filter(maker=maker, starting_serial__isnull=False, ending_serial__isnull=False)
    possible_op_rods = list()
    for rod in ww2_rods:
        if sn >= rod.starting_serial and sn <= rod.ending_serial:
            possible_op_rods.append({
                'drawing_number': rod.drawing_number,
                'sn_range': f'{rod.starting_serial} - {rod.ending_serial}'
            })
    return possible_op_rods


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
