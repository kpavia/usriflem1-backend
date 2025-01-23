from m1.models import (
    Receiver, OpRod, Bolt, BulletGuide,
    TriggerHousing, TriggerGuard, Trigger,
    Safety, Hammer, Cartouche
)


def get_op_rod(sn, maker):
    op_rods = OpRod.objects.all()
    ww2_rods = op_rods.filter(maker=maker, starting_serial__isnull=False, ending_serial__isnull=False)
    possible_op_rods = list()
    for rod in ww2_rods:
        if sn >= rod.starting_serial and sn <= rod.ending_serial:
            possible_op_rods.append({
                'drawing_number': rod.drawing_number,
                'sn_range': f'{rod.starting_serial} - {rod.ending_serial}',
                'notes': rod.notes
            })
    return possible_op_rods


def get_bolt(sn, maker):
    bolts = Bolt.objects.filter(maker=maker)
    possible_bolts = list()
    for bolt in bolts:
        if sn >= bolt.starting_serial and sn <= bolt.ending_serial:
            possible_bolts.append({
                'drawing_number': bolt.drawing_number,
                'sn_range': f'{bolt.starting_serial} - {bolt.ending_serial}'
            })
    return possible_bolts


def get_bullet_guide(sn, maker):
    b_guides = BulletGuide.objects.filter(maker=maker)
    possible_guides = list()
    for b in b_guides:
        if sn >=  b.starting_serial and sn <= b.ending_serial:
            possible_guides.append({
                'drawing_number': b.drawing_number,
                'sn_range': f'{b.starting_serial} - {b.ending_serial}',
                'notes': b.notes
            })
    return possible_guides


def get_cartouche(sn, maker):
    stock = Cartouche.objects.filter(
        maker=maker,
        starting_serial__lte=sn,
        ending_serial__gte=sn
    ).first()
    return {
        'cartouche': stock.cartouche,
        'notes': stock.notes
    }


def rifle_data(data):
    sn = int(data.get('serial_number'))
    maker = data.get('maker')
    receiver = Receiver.objects.filter(
        maker=maker,
        starting_serial__lte=sn,
        ending_serial__gte=sn
    ).first()
    if receiver:
        rifle = {'month': receiver.month, 'year': receiver.year, 'sn': sn, 'maker': receiver.maker}
        rifle['op_rods'] = get_op_rod(sn, maker)
        rifle['bolts'] = get_bolt(sn, maker)
        rifle['bullet_guides'] = get_bullet_guide(sn, maker)
        rifle['stock'] = get_cartouche(sn, maker)
        return rifle
    return {}
