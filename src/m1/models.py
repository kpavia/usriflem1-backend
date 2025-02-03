from django.db import models


class SRSVolume(models.Model):
    source = models.CharField(max_length=16)

    def __str__(self):
        return f'SRS {self.source}'


class Srs(models.Model):
    FIREARMS_CHOICES = {
        'M1': 'M1 Garand',
        'M1903': 'M1903 Springfield',

    }
    serial_number = models.PositiveIntegerField()
    firearm = models.CharField(max_length=32, choices=FIREARMS_CHOICES)
    model = models.CharField(max_length=20, null=True, blank=True)
    date = models.CharField(max_length=6)
    usage = models.CharField(max_length=64)
    srs_volume = models.ForeignKey(SRSVolume, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f'{self.firearm} {self.serial_number}, {self.srs_volume}'


class Receiver(models.Model):
    MAKER_CHOICES = {
        'SA': 'Springfield Armory',
        'W': 'Winchester Repeating Arms',
    }
    maker = models.CharField(max_length=32, choices=MAKER_CHOICES)
    month = models.CharField(max_length=16)
    year = models.IntegerField(null=True)
    starting_serial = models.IntegerField()
    ending_serial = models.IntegerField()

    def __str__(self):
        return f'{self.maker}, {self.month} {self.year}'


class OpRod(models.Model):
    MAKER_CHOICES = {
        'SA': 'Springfield Armory',
        'W': 'Winchester Repeating Arms',
    }
    maker = models.CharField(max_length=32, choices=MAKER_CHOICES)
    drawing_number = models.CharField(max_length=20)
    starting_serial = models.PositiveIntegerField(null=True, blank=True)
    ending_serial = models.PositiveIntegerField(null=True, blank=True)
    year_range_start = models.IntegerField(null=True, blank=True)
    year_range_end = models.IntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.maker} {self.drawing_number}'


class Bolt(models.Model):
    MAKER_CHOICES = {
        'SA': 'Springfield Armory',
        'W': 'Winchester Repeating Arms',
        'IHC': 'International Harvester',
        'HR': 'Harrington & Richardson'
    }
    maker = models.CharField(max_length=32, choices=MAKER_CHOICES)
    drawing_number = models.CharField(max_length=30)
    starting_serial = models.PositiveIntegerField(null=True, blank=True)
    ending_serial = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f'{self.maker} bolt {self.drawing_number}'


class BulletGuide(models.Model):
    MAKER_CHOICES = {
        'SA': 'Springfield Armory',
        'W': 'Winchester Repeating Arms',
        'IHC': 'International Harvester',
        'HR': 'Harrington & Richardson'
    }
    maker = models.CharField(max_length=32, choices=MAKER_CHOICES)
    drawing_number = models.CharField(max_length=30)
    starting_serial = models.PositiveIntegerField(null=True, blank=True)
    ending_serial = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.maker} bullet guide {self.drawing_number}'


class TriggerHousing(models.Model):
    MAKER_CHOICES = {
        'SA': 'Springfield Armory',
        'W': 'Winchester Repeating Arms',
        'IHC': 'International Harvester',
        'HR': 'Harrington & Richardson'
    }
    maker = models.CharField(max_length=32, choices=MAKER_CHOICES)
    drawing_number = models.CharField(max_length=30)
    starting_serial = models.PositiveIntegerField(null=True, blank=True)
    ending_serial = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.maker} trigger housing {self.drawing_number}'


class TriggerGuard(models.Model):
    MAKER_CHOICES = {
        'SA': 'Springfield Armory',
        'W': 'Winchester Repeating Arms',
        'IHC': 'International Harvester',
        'HR': 'Harrington & Richardson'
    }
    maker = models.CharField(max_length=32, choices=MAKER_CHOICES)
    drawing_number = models.CharField(max_length=30)
    starting_serial = models.PositiveIntegerField(null=True, blank=True)
    ending_serial = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.maker} trigger guard {self.drawing_number}'


class Trigger(models.Model):
    MAKER_CHOICES = {
        'SA': 'Springfield Armory',
        'W': 'Winchester Repeating Arms',
        'IHC': 'International Harvester',
        'HR': 'Harrington & Richardson'
    }
    maker = models.CharField(max_length=32, choices=MAKER_CHOICES)
    drawing_number = models.CharField(max_length=30)
    starting_serial = models.PositiveIntegerField(null=True, blank=True)
    ending_serial = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.maker} trigger {self.drawing_number}'


class Safety(models.Model):
    MAKER_CHOICES = {
        'SA': 'Springfield Armory',
        'W': 'Winchester Repeating Arms',
        'IHC': 'International Harvester',
        'HR': 'Harrington & Richardson'
    }
    maker = models.CharField(max_length=32, choices=MAKER_CHOICES)
    drawing_number = models.CharField(max_length=30)
    starting_serial = models.PositiveIntegerField(null=True, blank=True)
    ending_serial = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.maker} safety {self.drawing_number}'


class Hammer(models.Model):
    MAKER_CHOICES = {
        'SA': 'Springfield Armory',
        'W': 'Winchester Repeating Arms',
        'IHC': 'International Harvester',
        'HR': 'Harrington & Richardson'
    }
    maker = models.CharField(max_length=32, choices=MAKER_CHOICES)
    drawing_number = models.CharField(max_length=30)
    starting_serial = models.PositiveIntegerField(null=True, blank=True)
    ending_serial = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.maker} hammer {self.drawing_number}'


class Cartouche(models.Model):
    MAKER_CHOICES = {
        'SA': 'Springfield Armory',
        'W': 'Winchester Repeating Arms',
        'IHC': 'International Harvester',
        'HR': 'Harrington & Richardson'
    }
    maker = models.CharField(max_length=32, choices=MAKER_CHOICES)
    cartouche = models.CharField(max_length=16)
    starting_serial = models.PositiveIntegerField(null=True, blank=True)
    ending_serial = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.maker} stock cartouche - {self.cartouche}'
