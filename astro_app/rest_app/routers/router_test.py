from rest_framework import routers

from rest_app.viewsets.test import TestViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'test', TestViewSet, basename='test')
