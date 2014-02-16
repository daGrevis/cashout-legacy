import httplib
from decimal import Decimal

from faker import Factory

from django.test import TestCase
from django.core.urlresolvers import reverse

from core.factories import fake_tags, PaymentFactory, CategoryFactory
from core.models import Payment, Category
from core.utils import filter_by_keys


fake_factory = Factory.create()


class PaymentTestCase(TestCase):
    def test_add_payment(self):
        data = filter_by_keys(PaymentFactory.attributes(), ["title", "price"])
        tags = fake_tags()
        data["tags"] = ", ".join(tags)

        response = self.client.post(reverse("core.index"), data)

        self.assertEqual(response.status_code, httplib.FOUND)

        payment = Payment.objects.first()

        self.assertEqual(payment.title, data["title"])
        self.assertEqual(payment.price, Decimal(data["price"]))
        self.assertEqual(sorted(payment.get_tags_as_list()), sorted(tags))

    def test_edit_payment(self):
        payment = PaymentFactory.create()
        payment.tags.add(*fake_tags())

        data = PaymentFactory.attributes()
        tags = fake_tags()
        data["tags"] = ", ".join(tags)
        payment_url = reverse("core.payment_item",
                              kwargs={"payment_pk": payment.pk})
        response = self.client.post(payment_url, data)

        self.assertEqual(response.status_code, httplib.FOUND)

        payment = Payment.objects.first()

        self.assertEqual(payment.title, data["title"])
        self.assertEqual(payment.description, data["description"])
        self.assertEqual(payment.price, Decimal(data["price"]))
        self.assertEqual(payment.currency, data["currency"])
        self.assertEqual(sorted(payment.get_tags_as_list()), sorted(tags))

        payment = PaymentFactory.create()
        payment.tags.add(*fake_tags())

    def test_delete_payment(self):
        payment = PaymentFactory.create()
        payment.tags.add(*fake_tags())

        payment_url = reverse("core.payment_item",
                              kwargs={"payment_pk": payment.pk})
        response = self.client.get(payment_url, {"delete": True})

        self.assertEqual(response.status_code, httplib.FOUND)

        self.assertFalse(Payment.objects.exists())


class CategoryTestCase(TestCase):
    def test_add_category(self):
        data = CategoryFactory.attributes()

        response = self.client.post(reverse("core.category_list"), data)

        self.assertEqual(response.status_code, httplib.OK)

        self.assertTrue(Category.objects.filter(title=data["title"]).exists())

    def test_delete_category(self):
        category = CategoryFactory.create()

        category_url = reverse("core.category_item",
                               kwargs={"category_pk": category.pk})
        response = self.client.get(category_url, {"delete": True})

        self.assertEqual(response.status_code, httplib.OK)

        self.assertFalse(Category.objects.exists())
