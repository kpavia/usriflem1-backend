from django.test import TestCase
from m1.models import (
    Receiver,
    OpRod
)
from m1.tasks import rifle_data, get_op_rod


class CustomUnitTests:

    def __init__(self):
        self.test_sn1 = 971531
        self.test_sn2 = 11358
        self.test_sn3 = 345121
        self.test_sn4 = 566924
        self.test_sn5 = 2154846
        self.test_sn6 = 3413278
        self.receivers = Receiver.objects.all()
        self.op_rods = OpRod.objects.filter(
            maker='SA',
            starting_serial__isnull=False,
            ending_serial__isnull=False
        )
    
    def test_receiver_date(self):
        # test 1
        receiver = rifle_data({'serial_number': self.test_sn1, 'maker': 'SA'})

        try:
            assert isinstance(receiver, dict)
            assert receiver.get('month', '') == 'November'
            assert receiver.get('year', 0) == 1942
        except AssertionError as ae:
            raise ae
        else:
            print('Unit tests 1 passed')

        # negative test
        try:
            assert receiver.get('month', '') == 'September'
            assert receiver.get('year', 0) == 1943
        except AssertionError as ae:
            print('Negative tests for test 1 passed')
        else:
            raise AssertionError('Negative tests 1 failed')
        
        # test 2
        receiver = rifle_data({'serial_number': self.test_sn2, 'maker': 'SA'})
        try:
            assert isinstance(receiver, dict)
            assert receiver.get('month', '') == 'May'
            assert receiver.get('year', 0) == 1939
        except AssertionError as ae:
            raise ae
        else:
            print('Unit tests 2 passed')

        # negative test
        try:
            assert receiver.get('month', '') == 'April'
            assert receiver.get('year', 0) == 1937
        except AssertionError as ae:
            print('Negative tests for test 2 passed')
        else:
            raise AssertionError('Negative test 2 failed')
        

        # test 3
        receiver = rifle_data({'serial_number': self.test_sn3, 'maker': 'SA'})
        try:
            assert isinstance(receiver, dict)
            assert receiver.get('month', '') == 'September'
            assert receiver.get('year', 0) == 1941
        except AssertionError as ae:
            raise ae
        else:
            print('Unit tests 3 passed')

        # negative test
        try:
            assert receiver.get('month', '') == 'April'
            assert receiver.get('year', 0) == 1937
        except AssertionError as ae:
            print('Negative tests for test 3 passed')
        else:
            raise AssertionError('Negative tests 3 failed')

        # test 4
        receiver = rifle_data({'serial_number': self.test_sn4, 'maker': 'SA'})
        try:
            assert isinstance(receiver, dict)
            assert receiver.get('month', '') == 'April'
            assert receiver.get('year', 0) == 1942
        except AssertionError as ae:
            raise ae
        else:
            print('Unit tests 4 passed')

        # negative test
        try:
            assert receiver.get('month', '') == 'April'
            assert receiver.get('year', 0) == 1937
        except AssertionError as ae:
            print('Negative tests for test 4 passed')
        else:
            raise AssertionError('Negative tests 4 failed')
        
        # test 5
        receiver = rifle_data({'serial_number': self.test_sn5, 'maker': 'SA'})
        try:
            assert isinstance(receiver, dict)
            assert receiver.get('month', '') == 'November'
            assert receiver.get('year', 0) == 1943
        except AssertionError as ae:
            raise ae
        else:
            print('Unit tests 5 passed')

        # negative test
        try:
            assert receiver.get('month', '') == 'April'
            assert receiver.get('year', 0) == 1937
        except AssertionError as ae:
            print('Negative tests for test 5 passed')
        else:
            raise AssertionError('Negative tests 5 failed')
        
        # test 6
        receiver = rifle_data({'serial_number': self.test_sn6, 'maker': 'SA'})
        try:
            assert isinstance(receiver, dict)
            assert receiver.get('month', '') == 'January'
            assert receiver.get('year', 0) == 1945
        except AssertionError as ae:
            raise ae
        else:
            print('Unit tests 6 passed')

        # negative test
        try:
            assert receiver.get('month', '') == 'April'
            assert receiver.get('year', 0) == 1937
        except AssertionError as ae:
            print('Negative tests for test 6 passed')
        else:
            raise AssertionError('Negative tests 6 failed')


    def test_op_rod(self):
        # test 1
        rod_1 = get_op_rod(self.test_sn1, 'SA')
        possible_rods = [
            'D35382 3SA',
            'D35382 6 SA',
            'D35382 8 SA'
        ]
        assert isinstance(rod_1, list)
        for rod in rod_1:
            try:
                print(rod)
                assert rod.get('drawing_number', '') in possible_rods
            except AssertionError:
                print(f'S/N: {self.test_sn1}')
                print(f'{rod.get("drawing_number", "")} not in possible rods')
                raise AssertionError
            else:
                print('Test 1 passed')
        
        # test 2
        rod_2 = get_op_rod(self.test_sn2, 'SA')
        possible_rods = [
            'D 35382-0',
        ]
        assert isinstance(rod_2, list)
        for rod in rod_2:
            try:
                assert rod.get('drawing_number', '') in possible_rods
            except AssertionError:
                print(f'S/N: {self.test_sn2}')
                print(f'{rod.get("drawing_number", "")} not in possible rods')
                raise AssertionError
            else:
                print('Test 2 passed')
 