from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
import monitor_app.views
from monitor_app.views_collection.handlers.PiCpuTempStatusHander import PiCpuTempStatusHander
from monitor_app.views_collection.handlers.WateringStatusHander import WateringStatusHander
from monitor_app.views_collection.handlers.CameraTaskStatusHander import CameraTaskStatusHander
from monitor_app.views_collection.handlers.WarningStatusHander import WarningStatusHander
from monitor_app.views_collection.handlers.TemperatureHandler import TemperatureHandler
from monitor_app.views_collection.handlers.HumidityHandler import HumidityHandler

# test url resolves to dashboard view
class DashboardTest(TestCase):
    def setUp(self):
        piTempHandler = PiCpuTempStatusHander()
        piTempHandler.create_fake_data("1000c")
        wateringHandler = WateringStatusHander()
        wateringHandler.create_fake_data("DDone")
        cameraTaskHandler = CameraTaskStatusHander()
        cameraTaskHandler.create_fake_data("87%")
        warningHandler = WarningStatusHander()
        warningHandler.create_fake_data("1000")
        temperatureHandler = TemperatureHandler()
        temperatureHandler.insertData(778.3)
        temperatureHandler.insertData(778.2)
        humidityHandler = HumidityHandler()
        humidityHandler.insertData(777.3)
        humidityHandler.insertData(777.2)

    def test_root_url_resolves_to_dashboard_view(self):
        found = resolve('/')
        self.assertEqual(found.func.view_class, monitor_app.views_collection.Dashboard.Dashboard)

    def test_root_url_resolves_to_dashboard_view(self):
        found = resolve('/')
        self.assertEqual(found.func.view_class, monitor_app.views_collection.Dashboard.Dashboard)

    def test_piCpuTemperature(self):
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        view = monitor_app.views_collection.Dashboard.Dashboard.as_view()
        response = view(request)
        self.assertIn(b'<span>1000c</span></div>', response.content)

    def test_wateringStatus(self):
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        view = monitor_app.views_collection.Dashboard.Dashboard.as_view()
        response = view(request)
        self.assertIn(b'<span>DDone</span></div>', response.content)

    def test_cameraTask(self):
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        view = monitor_app.views_collection.Dashboard.Dashboard.as_view()
        response = view(request)
        self.assertIn(b'<div class="h5 mb-0 mr-3 font-weight-bold text-gray-800">87%</div>', response.content)

    def test_warningCount(self):
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        view = monitor_app.views_collection.Dashboard.Dashboard.as_view()
        response = view(request)
        self.assertIn(b'<div class="h5 mb-0 font-weight-bold text-gray-800">1000</div>', response.content)

    def test_temperatureChart(self):

        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        view = monitor_app.views_collection.Dashboard.Dashboard.as_view()
        response = view(request)
        self.assertIn(b'[778.3, 778.2]', response.content)

    def test_humidityChart(self):
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        view = monitor_app.views_collection.Dashboard.Dashboard.as_view()
        response = view(request)
        self.assertIn(b'[777.3, 777.2]', response.content)

    def test_notLoginRingButton(self):
        request = RequestFactory().get('/')
        request.user = AnonymousUser()
        view = monitor_app.views_collection.Dashboard.Dashboard.as_view()
        response = view(request)
        self.assertNotIn(b'id="messageCenter"', response.content)

    def test_loginRingButton(self):
        #see functional test
        pass
