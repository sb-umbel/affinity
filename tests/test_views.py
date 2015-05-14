from django.shortcuts import resolve_url

from affinity.models import Brand, Profile

from tests.testcases import ViewTestCase


class BrandListViewTestCase(ViewTestCase):

    def test_can_list_existing_brands(self):
        Brand.objects.create(name='Apple')
        Brand.objects.create(name='Microsoft')

        response = self.app.get(resolve_url('brand_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['name'], 'Apple')
        self.assertEqual(response.json[1]['name'], 'Microsoft')

        response = self.app.get(resolve_url('brand_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]['name'], 'Apple')
        self.assertEqual(response.json[1]['name'], 'Microsoft')

    def test_can_listing_no_brands(self):
        response = self.app.get(resolve_url('brand_list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)

    def test_can_create_new_brand(self):
        response = self.app.post(resolve_url('brand_list'), {
            'name': 'Apple',
        })

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.json['id'])
        self.assertEqual(response.json['name'], 'Apple')

    def test_busts_cache_when_brands_change(self):
        Brand.objects.create(name='Apple')

        response = self.app.get(resolve_url('brand_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], 'Apple')

        brand2 = Brand.objects.create(name='Microsoft')

        response = self.app.get(resolve_url('brand_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[1]['name'], 'Microsoft')

        brand2.name = 'Windows'
        brand2.save()

        response = self.app.get(resolve_url('brand_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[1]['name'], 'Windows')


class BrandProfileListView(ViewTestCase):

    def setUp(self):
        self.brand = Brand.objects.create(name='Apple')
        self.profile = Profile.objects.create()
        self.profile.brands.add(self.brand)

    def test_can_list_profiles_for_brand(self):
        response = self.app.get(resolve_url('brand_profile_list', brand_id=self.brand.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['id'], str(self.profile.id))

    def test_busts_cache_when_profile_added_to_brand(self):
        response1 = self.app.get(resolve_url('brand_profile_list', brand_id=self.brand.id))
        self.assertEqual(len(response1.json), 1)
        self.assertEqual(response1.json[0]['id'], str(self.profile.id))

        profile2 = Profile.objects.create()
        self.brand.profiles.add(profile2)

        response2 = self.app.get(resolve_url('brand_profile_list', brand_id=self.brand.id))
        self.assertEqual(len(response2.json), 2)
        self.assertEqual(response2.json[1]['id'], str(profile2.id))

    def test_cache_hit(self):
        response1 = self.app.get(resolve_url('brand_profile_list', brand_id=self.brand.id))
        self.assertEqual(len(response1.json), 1)
        self.assertEqual(response1.json[0]['id'], str(self.profile.id))

        response2 = self.app.get(resolve_url('brand_profile_list', brand_id=self.brand.id))
        self.assertEqual(len(response2.json), 1)
        self.assertEqual(response2.json[0]['id'], str(self.profile.id))


class ProfileListViewTestCase(ViewTestCase):

    def test_can_create_new_profile(self):
        response = self.app.post(resolve_url('profile_list'))

        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(response.json['id'])


class ProfileBrandListView(ViewTestCase):

    def setUp(self):
        self.brand = Brand.objects.create(name='Apple')
        self.profile = Profile.objects.create()
        self.profile.brands.add(self.brand)

    def test_can_list_brands_for_profile(self):
        response = self.app.get(resolve_url('profile_brand_list', profile_id=self.profile.id))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['id'], str(self.brand.id))
        self.assertEqual(response.json[0]['name'], self.brand.name)

    def test_busts_cache_when_brand_is_updated(self):
        response1 = self.app.get(resolve_url('profile_brand_list', profile_id=self.profile.id))
        self.assertEqual(response1.json[0]['name'], self.brand.name)

        self.brand.name = 'Microsoft'
        self.brand.save()

        response2 = self.app.get(resolve_url('profile_brand_list', profile_id=self.profile.id))
        self.assertEqual(response2.json[0]['name'], self.brand.name)

    def test_busts_cache_when_brand_added_to_profil(self):
        response1 = self.app.get(resolve_url('profile_brand_list', profile_id=self.profile.id))
        self.assertEqual(len(response1.json), 1)
        self.assertEqual(response1.json[0]['name'], self.brand.name)

        response1 = self.app.get(resolve_url('profile_brand_list', profile_id=self.profile.id))
        self.assertEqual(len(response1.json), 1)
        self.assertEqual(response1.json[0]['name'], self.brand.name)

        brand2 = Brand.objects.create(name='Microsoft')
        self.profile.brands.add(brand2)

        response2 = self.app.get(resolve_url('profile_brand_list', profile_id=self.profile.id))
        self.assertEqual(len(response2.json), 2)
        self.assertEqual(response2.json[1]['name'], brand2.name)


class ProfileBrandDetailView(ViewTestCase):

    def test_can_add_brand_to_profile(self):
        brand = Brand.objects.create(name='Apple')
        profile = Profile.objects.create()

        response = self.app.put(resolve_url(
            to='profile_brand_detail',
            profile_id=profile.id,
            brand_id=brand.id,
        ))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(profile.brands.all()), 1)
        self.assertEqual(profile.brands.all()[0].id, brand.id)
        self.assertEqual(profile.brands.all()[0].name, brand.name)

    def test_can_remove_brand_from_profile(self):
        brand = Brand.objects.create(name='Apple')
        profile = Profile.objects.create()

        profile.brands.add(brand)

        response = self.app.delete(resolve_url(
            to='profile_brand_detail',
            profile_id=profile.id,
            brand_id=brand.id,
        ))

        self.assertEqual(response.status_code, 204)
        self.assertEqual(len(profile.brands.all()), 0)
