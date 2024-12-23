from django.db import models


class Receiver(models.Model):
    MAKER_CHOICES = {
        'SA': 'Springfield Armory',
        'W': 'Winchester Repeating Arms',
        'HR': 'Harrington & Richardson Arms Co',
        'IH': 'International Harvester'
    }
    maker = models.CharField(max_length=32, choices=MAKER_CHOICES)
    month = models.CharField(max_length=16)
    year = models.IntegerField(null=True)
    starting_serial = models.IntegerField()
    ending_serial = models.IntegerField()

    def __str__(self):
        return f'{self.maker}, {self.month} {self.year}'


