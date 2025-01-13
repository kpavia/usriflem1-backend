from django.db import models


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
