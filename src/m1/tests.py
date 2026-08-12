from unittest import expectedFailure

from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from m1.forms import RifleDateForm
from m1.models import (
    Bolt,
    BulletGuide,
    Cartouche,
    Follower,
    Hammer,
    OpRod,
    Receiver,
    Safety,
    Trigger,
    TriggerGuard,
    TriggerHousing,
    Video,
)
from m1.tasks import (
    get_bolt,
    get_bullet_guide,
    get_cartouche,
    get_followers,
    get_hammers,
    get_op_rod,
    get_safeties,
    get_trigger_guards,
    get_trigger_housing,
    get_triggers,
    rifle_data,
)

REQUIRED_EDUCATION_VIDEO_TITLES = [
    'M1 Garand Firearm Maintenance: Part 1 Disassembly',
    'M1 Garand Firearm Maintenance: Part 2 Cleaning',
    'M1 Garand Firearm Maintenance: Part 3 Lubrication',
    'M1 Garand Firearm Maintenance: Part 4 Reassembly',
    'The 7th Round Stoppage',
    'Rifle Marksmanship with the M1 Rifle (1942), Part 1',
    'Rifle Marksmanship with the M1 Rifle (1942), Part 2',
    'US Army Rifle Cleanliness (1943)',
    'Principles of Operation (1943)',
    'Early M1 Rifle Production',
    'Navy M1 Garand Conversions to 7.62mm',
    'Navy 7.62mm Conversion M1 Garand - Mk2 Mod1',
    'Gas Trap M1 Garand',
    'C&Rsenal: M1 Garand',
]


class GetOpRodTests(TestCase):

    def setUp(self):
        OpRod.objects.create(
            maker='SA', drawing_number='D1', starting_serial=100, ending_serial=200
        )
        OpRod.objects.create(
            maker='SA', drawing_number='D2', starting_serial=201, ending_serial=300
        )
        OpRod.objects.create(
            maker='SA', drawing_number='NO-RANGE', starting_serial=None, ending_serial=None
        )
        OpRod.objects.create(
            maker='W', drawing_number='W1', starting_serial=100, ending_serial=200
        )

    def test_serial_within_range_matches(self):
        result = get_op_rod(150, 'SA')
        self.assertEqual([r['drawing_number'] for r in result], ['D1'])

    def test_bounds_are_inclusive(self):
        self.assertEqual(get_op_rod(100, 'SA')[0]['drawing_number'], 'D1')
        self.assertEqual(get_op_rod(200, 'SA')[0]['drawing_number'], 'D1')

    def test_no_match_returns_empty_list(self):
        self.assertEqual(get_op_rod(9999, 'SA'), [])

    def test_rows_without_a_serial_range_are_excluded(self):
        result = get_op_rod(150, 'SA')
        self.assertNotIn('NO-RANGE', [r['drawing_number'] for r in result])

    def test_other_maker_is_excluded(self):
        result = get_op_rod(150, 'SA')
        self.assertNotIn('W1', [r['drawing_number'] for r in result])


class GetBoltTests(TestCase):

    def setUp(self):
        Bolt.objects.create(maker='SA', drawing_number='D1', starting_serial=100, ending_serial=200)
        Bolt.objects.create(maker='W', drawing_number='W1', starting_serial=100, ending_serial=200)

    def test_serial_within_range_matches(self):
        result = get_bolt(150, 'SA')
        self.assertEqual(result, [{'drawing_number': 'D1', 'sn_range': '100 - 200'}])

    def test_bounds_are_inclusive(self):
        self.assertEqual(get_bolt(100, 'SA')[0]['drawing_number'], 'D1')
        self.assertEqual(get_bolt(200, 'SA')[0]['drawing_number'], 'D1')

    def test_no_match_returns_empty_list(self):
        self.assertEqual(get_bolt(9999, 'SA'), [])

    def test_no_bolts_for_maker_returns_empty_list(self):
        self.assertEqual(get_bolt(150, 'IHC'), [])

    @expectedFailure
    def test_null_serial_range_crashes_instead_of_being_skipped(self):
        # Known bug: unlike get_op_rod, get_bolt never excludes rows with a
        # null starting/ending serial before comparing against sn, so any
        # Bolt row missing its range blows up the lookup for every serial
        # number of that maker (TypeError: '>=' not supported between
        # instances of 'int' and 'NoneType'). This test documents that; if
        # it starts failing (i.e. passing), the bug has been fixed and the
        # decorator should be removed.
        Bolt.objects.create(maker='SA', drawing_number='NO-RANGE')
        get_bolt(150, 'SA')


class GetBulletGuideTests(TestCase):

    def setUp(self):
        BulletGuide.objects.create(
            maker='SA', drawing_number='D1', starting_serial=100, ending_serial=200, notes='early type'
        )
        BulletGuide.objects.create(maker='W', drawing_number='W1', starting_serial=100, ending_serial=200)

    def test_serial_within_range_matches(self):
        result = get_bullet_guide(150, 'SA')
        self.assertEqual(
            result, [{'drawing_number': 'D1', 'sn_range': '100 - 200', 'notes': 'early type'}]
        )

    def test_no_match_returns_empty_list(self):
        self.assertEqual(get_bullet_guide(9999, 'SA'), [])

    @expectedFailure
    def test_null_serial_range_crashes_instead_of_being_skipped(self):
        # Same underlying bug as GetBoltTests.test_null_serial_range_crashes_instead_of_being_skipped.
        BulletGuide.objects.create(maker='SA', drawing_number='NO-RANGE')
        get_bullet_guide(150, 'SA')


class GetCartoucheTests(TestCase):

    def setUp(self):
        Cartouche.objects.create(
            maker='SA', cartouche='Flat Bolt', starting_serial=100, ending_serial=200, notes='p-proof'
        )

    def test_serial_within_range_returns_cartouche_and_notes(self):
        result = get_cartouche(150, 'SA')
        self.assertEqual(result, {'cartouche': 'Flat Bolt', 'notes': 'p-proof'})

    def test_no_match_returns_empty_dict(self):
        self.assertEqual(get_cartouche(9999, 'SA'), {})

    def test_other_maker_returns_empty_dict(self):
        self.assertEqual(get_cartouche(150, 'W'), {})


class GetFollowersTests(TestCase):

    def setUp(self):
        Follower.objects.create(
            maker='SA', drawing_number='F1', starting_serial=100, ending_serial=200, notes='steel'
        )

    def test_match_is_keyed_as_revision_number(self):
        # get_followers exposes the model's drawing_number field under the
        # key 'revision_number', unlike every other lookup in tasks.py which
        # uses 'drawing_number'. Documented here so a refactor doesn't
        # silently change the rifle_data output shape.
        result = get_followers(150, 'SA')
        self.assertEqual(result, [{'revision_number': 'F1', 'notes': 'steel'}])

    def test_no_match_returns_empty_list(self):
        self.assertEqual(get_followers(9999, 'SA'), [])


class RangeFilteredLookupTests(TestCase):
    """Covers get_trigger_housing, get_trigger_guards, get_triggers,
    get_safeties, and get_hammers - all four filter at the DB level and
    return [{'drawing_number', 'notes'}, ...]."""

    LOOKUPS = [
        (get_trigger_housing, TriggerHousing),
        (get_trigger_guards, TriggerGuard),
        (get_triggers, Trigger),
        (get_safeties, Safety),
        (get_hammers, Hammer),
    ]

    def test_match_bounds_no_match_and_other_maker(self):
        for lookup_fn, model in self.LOOKUPS:
            with self.subTest(model=model.__name__):
                model.objects.create(
                    maker='SA', drawing_number='D1', starting_serial=100,
                    ending_serial=200, notes='fits here'
                )
                model.objects.create(
                    maker='W', drawing_number='W1', starting_serial=100, ending_serial=200
                )

                result = lookup_fn(150, 'SA')
                self.assertEqual(result, [{'drawing_number': 'D1', 'notes': 'fits here'}])

                self.assertEqual([r['drawing_number'] for r in lookup_fn(100, 'SA')], ['D1'])
                self.assertEqual([r['drawing_number'] for r in lookup_fn(200, 'SA')], ['D1'])

                self.assertEqual(lookup_fn(9999, 'SA'), [])
                self.assertEqual([r['drawing_number'] for r in lookup_fn(150, 'W')], ['W1'])

                model.objects.all().delete()


class RifleDataTests(TestCase):

    def setUp(self):
        Receiver.objects.create(
            maker='SA', month='June', year=1944, starting_serial=1000, ending_serial=2000
        )
        OpRod.objects.create(maker='SA', drawing_number='D-OPROD', starting_serial=1000, ending_serial=2000)
        Bolt.objects.create(maker='SA', drawing_number='D-BOLT', starting_serial=1000, ending_serial=2000)

    def test_matching_serial_returns_full_rifle_dict(self):
        rifle = rifle_data({'serial_number': '1500', 'maker': 'SA'})
        self.assertEqual(rifle['month'], 'June')
        self.assertEqual(rifle['year'], 1944)
        self.assertEqual(rifle['sn'], 1500)
        self.assertEqual(rifle['maker'], 'SA')
        self.assertEqual([r['drawing_number'] for r in rifle['op_rods']], ['D-OPROD'])
        self.assertEqual([r['drawing_number'] for r in rifle['bolts']], ['D-BOLT'])

    def test_serial_outside_any_receiver_range_returns_empty_dict(self):
        self.assertEqual(rifle_data({'serial_number': '999999', 'maker': 'SA'}), {})

    def test_wrong_maker_for_serial_returns_empty_dict(self):
        self.assertEqual(rifle_data({'serial_number': '1500', 'maker': 'W'}), {})


class RifleDateFormTests(TestCase):

    def test_valid_data(self):
        form = RifleDateForm(data={'serial_number': '123456', 'maker': 'SA'})
        self.assertTrue(form.is_valid())

    def test_invalid_maker_choice_rejected(self):
        form = RifleDateForm(data={'serial_number': '123456', 'maker': 'BOGUS'})
        self.assertFalse(form.is_valid())
        self.assertIn('maker', form.errors)

    def test_missing_serial_number_rejected(self):
        form = RifleDateForm(data={'maker': 'SA'})
        self.assertFalse(form.is_valid())
        self.assertIn('serial_number', form.errors)

    def test_serial_number_over_max_length_rejected(self):
        form = RifleDateForm(data={'serial_number': '1' * 11, 'maker': 'SA'})
        self.assertFalse(form.is_valid())
        self.assertIn('serial_number', form.errors)


class IndexViewTests(TestCase):

    def setUp(self):
        Receiver.objects.create(
            maker='SA', month='March', year=1943, starting_serial=100, ending_serial=200
        )
        Cartouche.objects.create(
            maker='SA', cartouche='P', starting_serial=100, ending_serial=200, notes='flat'
        )

    def test_get_renders_blank_form(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], RifleDateForm)
        self.assertNotIn('rifle', response.context)

    def test_post_with_matching_serial_number_renders_rifle_details(self):
        response = self.client.post(reverse('homepage'), {'serial_number': '150', 'maker': 'SA'})
        self.assertEqual(response.status_code, 200)
        rifle = response.context['rifle']
        self.assertEqual(rifle['Maker'], 'Springfield Armory')
        self.assertEqual(rifle['Serial Number'], 150)
        self.assertEqual(rifle['Month'], 'March')
        self.assertEqual(rifle['Year'], 1943)
        self.assertNotIn('error', response.context)

    def test_post_with_unmatched_serial_number_shows_error(self):
        response = self.client.post(reverse('homepage'), {'serial_number': '999999', 'maker': 'SA'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['error'])
        self.assertFalse(response.context['rifle'])

    def test_display_ga_false_for_localhost_host(self):
        response = self.client.get(reverse('homepage'), HTTP_HOST='localhost')
        self.assertFalse(response.context['display_ga'])

    def test_display_ga_true_for_production_host(self):
        response = self.client.get(reverse('homepage'), HTTP_HOST='usriflem1.com')
        self.assertTrue(response.context['display_ga'])


class EducationViewTests(TestCase):

    def _create_video(self, title, order):
        return Video.objects.create(
            link=f'https://youtu.be/{order}', title=title, category=Video.MILITARY, order=order
        )

    def test_renders_when_all_required_videos_exist(self):
        for order, title in enumerate(REQUIRED_EDUCATION_VIDEO_TITLES):
            self._create_video(title, order)

        response = self.client.get(reverse('education'))
        self.assertEqual(response.status_code, 200)

    def test_raises_when_a_required_video_is_missing(self):
        # get_videos() looks up each of the 14 hardcoded titles with .get(),
        # so deleting or renaming any one of them 500s the education page.
        for order, title in enumerate(REQUIRED_EDUCATION_VIDEO_TITLES[:-1]):
            self._create_video(title, order)

        with self.assertRaises(Video.DoesNotExist):
            self.client.get(reverse('education'))


class VideoModelTests(TestCase):

    def test_category_and_order_must_be_unique_together(self):
        Video.objects.create(link='a', title='A', category=Video.MILITARY, order=1)
        with self.assertRaises(IntegrityError):
            Video.objects.create(link='b', title='B', category=Video.MILITARY, order=1)


class VideoListAPITests(TestCase):

    def setUp(self):
        Video.objects.create(link='m2', title='Military 2', category=Video.MILITARY, order=2)
        Video.objects.create(link='m1', title='Military 1', category=Video.MILITARY, order=1)
        Video.objects.create(link='p', title='Production', category=Video.PRODUCTION_HISTORY, order=1)
        Video.objects.create(link='mt', title='Maintenance', category=Video.MAINTENANCE, order=1)

    def test_returns_all_videos(self):
        response = self.client.get(reverse('v1-videos'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)

    def test_orders_military_then_maintenance_then_production(self):
        response = self.client.get(reverse('v1-videos'))
        categories = [v['category'] for v in response.json()]
        self.assertEqual(
            categories,
            [Video.MILITARY, Video.MILITARY, Video.MAINTENANCE, Video.PRODUCTION_HISTORY],
        )

    def test_orders_by_order_within_category(self):
        response = self.client.get(reverse('v1-videos'))
        military_titles = [v['title'] for v in response.json() if v['category'] == Video.MILITARY]
        self.assertEqual(military_titles, ['Military 1', 'Military 2'])

    def test_serializer_exposes_expected_fields_only(self):
        response = self.client.get(reverse('v1-videos'))
        self.assertEqual(set(response.json()[0].keys()), {'link', 'title', 'category', 'order'})

    def test_field_values_round_trip_exactly(self):
        response = self.client.get(reverse('v1-videos'))
        military_one = next(v for v in response.json() if v['title'] == 'Military 1')
        self.assertEqual(
            military_one, {'link': 'm1', 'title': 'Military 1', 'category': Video.MILITARY, 'order': 1}
        )

    def test_returns_empty_list_when_no_videos_exist(self):
        Video.objects.all().delete()
        response = self.client.get(reverse('v1-videos'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_post_is_not_allowed(self):
        response = self.client.post(
            reverse('v1-videos'),
            {'link': 'x', 'title': 'New', 'category': Video.MILITARY, 'order': 3},
        )
        self.assertEqual(response.status_code, 405)

    def test_resolves_at_documented_path(self):
        # Guards against the /api/ prefix (core/urls.py) or the v1/videos/
        # path (m1/urls.py) drifting without the URL name being updated.
        response = self.client.get('/api/v1/videos/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 4)
