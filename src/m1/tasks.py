from m1.models import (
    Receiver, OpRod, Bolt, BulletGuide,
    TriggerHousing, TriggerGuard, Trigger,
    Safety, Hammer, Cartouche, Follower, Video
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
    if bolts:
        for bolt in bolts:
            if sn >= bolt.starting_serial and sn <= bolt.ending_serial:
                possible_bolts.append({
                    'drawing_number': bolt.drawing_number,
                    'sn_range': f'{bolt.starting_serial} - {bolt.ending_serial}'
                })
        return possible_bolts
    
    return []


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
    if stock:
        return {
            'cartouche': stock.cartouche,
            'notes': stock.notes
        }
    return {}


def get_trigger_housing(sn, maker):
    housings = TriggerHousing.objects.filter(
        maker=maker,
        starting_serial__lte=sn,
        ending_serial__gte=sn
    )
    if housings:
        return [
            {
                'drawing_number': housing.drawing_number,
                'notes': housing.notes
            } for housing in housings
        ]
    return []


def get_trigger_guards(sn, maker):
    guards = TriggerGuard.objects.filter(
        maker=maker,
        starting_serial__lte=sn,
        ending_serial__gte=sn
    )
    if guards:
        return [
            {
                'drawing_number': guard.drawing_number,
                'notes': guard.notes
            } for guard in guards
        ]
    return []


def get_triggers(sn, maker):
    triggers = Trigger.objects.filter(
        maker=maker,
        starting_serial__lte=sn,
        ending_serial__gte=sn
    )
    if triggers:
        return [{
            'drawing_number': trigger.drawing_number,
            'notes': trigger.notes
        } for trigger in triggers]
    return []


def get_safeties(sn, maker):
    safeties = Safety.objects.filter(
        maker=maker,
        starting_serial__lte=sn,
        ending_serial__gte=sn
    )
    if safeties:
        return [{
            'drawing_number': safety.drawing_number,
            'notes': safety.notes
        } for safety in safeties]
    return []


def get_hammers(sn, maker):
    hammers = Hammer.objects.filter(
        maker=maker,
        starting_serial__lte=sn,
        ending_serial__gte=sn
    )
    if hammers:
        return [{
            'drawing_number': hammer.drawing_number,
            'notes': hammer.notes
        } for hammer in hammers]
    return []


def get_followers(sn, maker):
    followers = Follower.objects.filter(
        maker=maker,
        starting_serial__lte=sn,
        ending_serial__gte=sn
    )
    if followers:
        return [{
            'revision_number': follower.drawing_number,
            'notes': follower.notes
        } for follower in followers]
    return []


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
        rifle['trigger_housings'] = get_trigger_housing(sn, maker)
        rifle['trigger_guards'] = get_trigger_guards(sn, maker)
        rifle['triggers'] = get_triggers(sn, maker)
        rifle['safeties'] = get_safeties(sn, maker)
        rifle['hammers'] = get_hammers(sn, maker)
        rifle['followers'] = get_followers(sn, maker)
        return rifle
    return {}


def get_videos():
    videos = Video.objects.all()
    return {
        'maintenance_one': videos.get(title='M1 Garand Firearm Maintenance: Part 1 Disassembly'),
        'maintenance_two': videos.get(title='M1 Garand Firearm Maintenance: Part 2 Cleaning'),
        'maintenance_three': videos.get(title='M1 Garand Firearm Maintenance: Part 3 Lubrication'),
        'maintenance_four': videos.get(title='M1 Garand Firearm Maintenance: Part 4 Reassembly'),
        'seventh_round': videos.get(title='The 7th Round Stoppage'),
        'marksmanship_one': videos.get(title='Rifle Marksmanship with the M1 Rifle (1942), Part 1'),
        'marksmanship_two': videos.get(title='Rifle Marksmanship with the M1 Rifle (1942), Part 2'),
        'us_army_cleanliness': videos.get(title='US Army Rifle Cleanliness (1943)'),
        'principles_of_operation': videos.get(title='Principles of Operation (1943)'),
        'production_video': videos.get(title='Early M1 Rifle Production'),
        'navy_one': videos.get(title='Navy M1 Garand Conversions to 7.62mm'),
        'navy_two': videos.get(title='Navy 7.62mm Conversion M1 Garand - Mk2 Mod1'),
        'gas_trap': videos.get(title='Gas Trap M1 Garand'),
        'c_r': videos.get(title='C&Rsenal: M1 Garand')
    }
