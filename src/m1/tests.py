from django.test import TestCase
from m1.models import Receiver


class SerialNumberDatingTests(TestCase):

    def setUp(self):
        self.sn1 = 10
        self.sn1_month = 'August'
        self.sn1_year = 1937

        self.sn2 = 300
        self.sn2_month = 'September'
        self.sn2_year = 1937

        self.sn3 = 1000
        self.sn3_month = 'December'
        self.sn3_year = 1937
    

    def get_receiver_date(self, maker, serial_number):
        receiver = Receiver.objects.filter(maker=maker, starting_serial__lte=serial_number, ending_serial__gte=serial_number).first()
        return receiver

        # for receiver in receivers:
        #     if serial_number >= receiver.starting_serial and serial_number <= receiver.ending_serial:
        #         return (receiver.month, receiver.year)
    

    def test_sa_sn_dates(self):
        maker = 'SA'
        
        sn1_receiver = self.get_receiver_date(maker, self.sn1)
        self.assertEqual(sn1_receiver.month, self.sn1_month)
        self.assertEqual(sn1_receiver.year, self.sn1_year)

        sn2_receiver = self.get_receiver_date(maker, self.sn2)
        self.assertEqual(sn2_receiver.month, self.sn2_month)
        self.assertEqual(sn2_receiver.year, self.sn2_year)

        sn3_receiver = self.get_receiver_date(maker, self.sn3)
        self.assertEqual(sn3_receiver.month, self.sn3_month)
        self.assertEqual(sn3_receiver.year, self.sn3_year)

