from django.contrib import admin
from m1.models import (
    Receiver,
    OpRod,
    Bolt,
    BulletGuide,
    TriggerHousing,
    TriggerGuard,
    Trigger,
    Safety,
    Hammer,
    Cartouche,
    Srs,
    SRSVolume,
    Follower
)


admin.site.register(Receiver)
admin.site.register(OpRod)
admin.site.register(Bolt)
admin.site.register(BulletGuide)
admin.site.register(TriggerHousing)
admin.site.register(TriggerGuard)
admin.site.register(Trigger)
admin.site.register(Safety)
admin.site.register(Hammer)
admin.site.register(Cartouche)
admin.site.register(Srs)
admin.site.register(SRSVolume)
admin.site.register(Follower)
