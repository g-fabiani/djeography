from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from djeography.models import Address, Category, Contact, Entity, EvaluationLevel

# Create your tests here.


class EntityPopulatedTestCase(TestCase):
    def setUp(self) -> None:
        """Make an unpublished and a published entity."""
        self.cat = Category.objects.create(name='test')
        self.entity = Entity.objects.create(
            category=self.cat,
            title='Test title',
            description='Some description',
        )

        self.pub_entity = Entity.objects.create(
            category=self.cat,
            title='Second test title',
            description='Some description',
            published=True,
        )


class EntityModelTest(EntityPopulatedTestCase):
    def test_entity_title(self):
        self.assertEqual(f'{self.entity.title}', 'Test title')

    def test_entity_description(self):
        self.assertEqual(self.entity.description, 'Some description')

    def test_published(self):
        self.assertFalse(self.entity.published)

    def test_publish_method(self):
        self.entity.publish()
        self.assertTrue(self.entity.published)

    def test_unpublish_method(self):
        self.pub_entity.unpublish()
        self.assertFalse(self.pub_entity.published)

    def test_published_objects(self):
        self.assertEqual(Entity.published_objects.count(), 1)
        self.entity.publish()
        self.assertEqual(Entity.published_objects.count(), 2)

    def test_entity_objects(self):
        self.assertEqual(Entity.objects.count(), 2)


class EntityViewEmptyTest(TestCase):
    def test_entity_list_view_url_by_name(self):
        response = self.client.get(reverse('djeography:list'))
        self.assertEqual(response.status_code, 200)

    def test_entity_list_view_url_location(self):
        response = self.client.get('/map/entities/')
        self.assertEqual(response.status_code, 200)

    def test_entity_list_view_template(self):
        response = self.client.get(reverse('djeography:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'map/list.html')

    def test_entity_list_view_queryset(self):
        response = self.client.get(reverse('djeography:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['entities'], [])

    def test_entity_list_view_search(self):
        response = self.client.get(reverse('djeography:list'), {'search': 'test'})
        self.assertEqual(response.status_code, 200)


class EntityViewPopulatedTest(EntityPopulatedTestCase):
    def setUp(self) -> None:
        super().setUp()
        get_user_model().objects.create_user('test', password='test').save()

    def test_entity_list_view_url_by_name(self):
        response = self.client.get(reverse('djeography:list'))
        self.assertEqual(response.status_code, 200)

    def test_entity_list_view_url_location(self):
        response = self.client.get('/map/entities/')
        self.assertEqual(response.status_code, 200)

    def test_entity_list_view_template(self):
        response = self.client.get(reverse('djeography:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'map/list.html')

    def test_entity_list_view_queryset_unauth(self):
        response = self.client.get(reverse('djeography:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['entities'], [self.pub_entity])

    def test_entity_list_view_queryset_auth(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('djeography:list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['entities'],
            [self.entity, self.pub_entity],
        )

    def test_entity_list_view_published_entity_present(self):
        response = self.client.get(reverse('djeography:list'))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(f'{self.pub_entity.title}', response.content.decode())

    def test_entity_list_view_auth_unpublished_entity_present(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('djeography:list'))
        self.assertEqual(response.status_code, 200)
        self.assertInHTML(
            f'{self.entity.title}',
            response.content.decode(),
        )

    def test_entity_list_view_search_present(self):
        response = self.client.get(reverse('djeography:list'), {'search': 'test'})
        self.assertEqual(response.status_code, 200)
        # There is a entity in the search results
        self.assertQuerySetEqual(response.context['entities'], [self.pub_entity])

    def test_entity_list_view_search_absent(self):
        response = self.client.get(reverse('djeography:list'), {'search': 'zzz'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context['entities'], [])

    def test_published_detail_view_by_name(self):
        response = self.client.get(self.pub_entity.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_published_detail_view_location(self):
        response = self.client.get(f'/map/entities/{self.pub_entity.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_published_detail_view_template(self):
        response = self.client.get(self.pub_entity.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'map/detail.html')

    def test_unpublished_detail_view_404(self):
        response = self.client.get(self.entity.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_unpublished_detail_view_auth(self):
        self.client.login(username='test', password='test')
        response = self.client.get(self.entity.get_absolute_url())
        self.assertEqual(response.status_code, 200)


class MapViewEmptyTest(TestCase):
    def test_map_view_url_by_name(self):
        response = self.client.get(reverse('djeography:map_fullscreen'))
        self.assertEqual(response.status_code, 200)

    def test_map_view_url_location(self):
        response = self.client.get('/map/fullscreen/')
        self.assertEqual(response.status_code, 200)

    def test_map_view_template(self):
        response = self.client.get(reverse('djeography:map_fullscreen'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'map/map.html')


class MapViewPopulatedTest(EntityPopulatedTestCase):
    def test_map_view_url_by_name(self):
        response = self.client.get(reverse('djeography:map_fullscreen'))
        self.assertEqual(response.status_code, 200)

    def test_map_view_url_location(self):
        response = self.client.get('/map/fullscreen/')
        self.assertEqual(response.status_code, 200)

    def test_map_view_template(self):
        response = self.client.get(reverse('djeography:map_fullscreen'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'map/map.html')


class EntityPublishTest(EntityPopulatedTestCase):
    def setUp(self) -> None:
        super().setUp()
        get_user_model().objects.create_user('test', password='test')

    def test_publish_view_by_name(self):
        self.client.login(username='test', password='test')
        response = self.client.post(
            reverse('djeography:publish', kwargs={'pk': self.entity.pk}),
        )
        self.assertEqual(response.status_code, 302)

    def test_publish_view_by_location(self):
        self.client.login(username='test', password='test')
        response = self.client.post(f'/map/entities/{self.entity.pk}/publish/')
        self.assertEqual(response.status_code, 302)

    def test_publish_has_effect(self):
        self.assertFalse(self.entity.published)
        self.client.login(username='test', password='test')
        response = self.client.post(
            reverse('djeography:publish', kwargs={'pk': self.entity.pk}),
        )
        self.assertEqual(response.status_code, 302)
        entity = Entity.objects.get(pk=self.entity.pk)
        self.assertTrue(entity.published)

    def test_publish_redirect_correct_page(self):
        self.client.login(username='test', password='test')
        response = self.client.post(
            reverse('djeography:publish', kwargs={'pk': self.entity.pk}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.entity.get_absolute_url())

    def test_publish_unauth_redirects_to_login(self):
        response = self.client.post(
            reverse('djeography:publish', kwargs={'pk': self.entity.pk}),
        )
        self.assertEqual(response.status_code, 302)

    def test_publish_view_get_405(self):
        self.client.login(username='test', password='test')
        response = self.client.get(
            reverse('djeography:publish', kwargs={'pk': self.entity.pk}),
        )
        self.assertEqual(response.status_code, 405)


class EntityUnpublishTest(EntityPopulatedTestCase):
    def setUp(self) -> None:
        super().setUp()
        get_user_model().objects.create_user(username='test', password='test')

    def test_unpublish_view_by_name(self):
        self.client.login(username='test', password='test')
        response = self.client.post(
            reverse('djeography:unpublish', kwargs={'pk': self.pub_entity.pk}),
        )
        self.assertEqual(response.status_code, 302)

    def test_unpublish_view_by_location(self):
        self.client.login(username='test', password='test')
        response = self.client.post(f'/map/entities/{self.pub_entity.pk}/unpublish/')
        self.assertEqual(response.status_code, 302)

    def test_unpublish_has_effect(self):
        self.assertTrue(self.pub_entity.published)
        self.client.login(username='test', password='test')
        response = self.client.post(
            reverse('djeography:unpublish', kwargs={'pk': self.pub_entity.pk}),
        )
        self.assertEqual(response.status_code, 302)
        entity = Entity.objects.get(pk=self.pub_entity.pk)
        self.assertFalse(entity.published)

    def test_unpublish_redirect_correct_page(self):
        self.client.login(username='test', password='test')
        response = self.client.post(
            reverse('djeography:unpublish', kwargs={'pk': self.pub_entity.pk}),
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.pub_entity.get_absolute_url())

    def test_unpublish_unauth_redirects_to_login(self):
        response = self.client.post(
            reverse('djeography:unpublish', kwargs={'pk': self.pub_entity.pk}),
        )
        self.assertEqual(response.status_code, 302)

    def test_unpublish_view_get_405(self):
        self.client.login(username='test', password='test')
        response = self.client.get(
            reverse('djeography:unpublish', kwargs={'pk': self.pub_entity.pk}),
        )
        self.assertEqual(response.status_code, 405)


class TelephoneTest(EntityPopulatedTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.phone_spaces = Contact.objects.create(
            typology='P',
            contact='0464 241649',
            entity=self.pub_entity,
        )
        self.phone_dash = Contact.objects.create(
            typology='P',
            contact='331-7436495',
            entity=self.pub_entity,
        )

        # We need an address for the entity to be displayed on the map
        Address.objects.create(
            city='Pisa',
            province='PI',
            coords={'type': 'Point', 'coordinates': [0, 0]},
            entity=self.pub_entity,
        )

    def test_url_no_spaces_entity(self):
        response = self.client.get(self.pub_entity.get_absolute_url())
        phone_stripped = self.phone_spaces.contact.replace(' ', '')

        self.assertContains(response, self.phone_spaces.contact)
        self.assertContains(response, f'tel:{phone_stripped}')

    def test_url_no_dash_entity(self):
        response = self.client.get(self.pub_entity.get_absolute_url())
        phone_stripped = self.phone_dash.contact.replace('-', '')

        self.assertContains(response, self.phone_dash.contact)
        self.assertContains(response, f'tel:{phone_stripped}')


class EvaluationDataMigrationTest(TestCase):
    def test_evaluation_levels_present(self):
        count = EvaluationLevel.objects.count()
        self.assertEqual(count, 3)

    def test_evaluation_level_positive(self):
        eval_level = EvaluationLevel.objects.get(short_name='POS')
        self.assertEqual(eval_level.full_name, 'Positiva')

    def test_evaluation_level_mixed(self):
        eval_level = EvaluationLevel.objects.get(short_name='MIX')
        self.assertEqual(eval_level.full_name, 'Mista')

    def test_evaluation_level_negative(self):
        eval_level = EvaluationLevel.objects.get(short_name='NEG')
        self.assertEqual(eval_level.full_name, 'Negativa')

    def test_evaluation_level_does_not_exist(self):
        with self.assertRaises(EvaluationLevel.DoesNotExist):
            EvaluationLevel.objects.get(short_name='1')
