from rest_framework import routers
from .views import PerevalAddedViewSet

router = routers.SimpleRouter()
router.register(r'pereval', PerevalAddedViewSet)
urlpatterns = router.urls
