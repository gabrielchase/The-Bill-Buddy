from django.urls import (path, include)
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import verify_jwt_token

from users.views import (UserViewSet, LoginAPIView)
from bills.views import (BillViewSet, ServiceList)
from payments.views import PaymentViewSet


router = DefaultRouter()
router.register('users', UserViewSet)
router.register('bills', BillViewSet)
router.register('payments', PaymentViewSet)


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/login/', LoginAPIView.as_view()),
    path('api/token-verify/', verify_jwt_token),

    path('api/services/', ServiceList.as_view())
]
