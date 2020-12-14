from django.test import TestCase

# WARNING before running the script below, make sure the db account has the permission
# to create database (because in testing, django creates a db and destroy it after testing)
# > python3 manage.py test

# the command to allow account to create db
# > sudo -u postgres psql
# > ALTER USER <django-db-account> CREATEDB;

from django.urls import resolve
from django.http import HttpRequest
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
import monitor_app.views
from monitor_app.views_collection.handlers.PiCpuTempStatusHander import PiCpuTempStatusHander
from monitor_app.views_collection.handlers.WateringStatusHander import WateringStatusHander
from monitor_app.views_collection.handlers.CameraTaskStatusHander import CameraTaskStatusHander
from monitor_app.views_collection.handlers.WarningStatusHander import WarningStatusHander

# test url resolves to dashboard view
class DashboardPageTest(TestCase):
    def test_root_url_resolves_to_dashboard_view(self):
        found = resolve('/')
        self.assertEqual(found.func.view_class, monitor_app.views_collection.Dashboard.Dashboard)

    def test_dashboard_html_with_fake_data(self):
        piTempHandler = PiCpuTempStatusHander()
        piTempHandler.create_fake_data("1000c")
        wateringHandler = WateringStatusHander()
        wateringHandler.create_fake_data("DDone")
        cameraTaskHandler = CameraTaskStatusHander()
        cameraTaskHandler.create_fake_data("87%")
        warningHandler = WarningStatusHander()
        warningHandler.create_fake_data("1000")

        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        view = monitor_app.views_collection.Dashboard.Dashboard.as_view()
        response = view(request)

        self.assertIn(b'<span>1000c</span></div>', response.content)
        self.assertIn(b'<span>DDone</span></div>', response.content)
        self.assertIn(b'<div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">87%</div>', response.content)
        self.assertIn(b'<div class="h5 mb-0 font-weight-bold text-gray-800">1000</div>', response.content)
        self.assertTrue(response.content.strip().endswith(b'</html>'))
