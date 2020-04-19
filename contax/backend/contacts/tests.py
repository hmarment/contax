from django.test import TestCase
from .models import Contact

# # views (uses reverse)
# def create_whatever(self, title="only a test", body="yes, this is only a test"):
# 		return Whatever.objects.create(title=title, body=body, created_at=timezone.now())


class ContactViewTests(TestCase):
    fixtures = ["contacts/contact.json"]

    def test_should_create_group(self):
        contact = Contact.objects.get(pk=1)
        self.assertEqual(contact.first_name, "Henry") and self.assertEqual(
            contact.last_name, "Marment"
        )


# def test_contact_list_view(self):
#     w = self.create_whatever()
#     url = reverse("whatever.views.whatever")
#     resp = self.client.get(url)

#     self.assertEqual(resp.status_code, 200)
#     self.assertIn(w.title, resp.content)
