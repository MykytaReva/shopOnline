from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("", include("marketplace.urls")),
    path("shop-admin/", include("shop.urls")),
    path("customers/", include("customers.urls")),
    path("cart/", include("cart.urls")),
    path("payment/", include("payment.urls")),
    path("orders/", include("orders.urls")),
]
if settings.ADMIN_ENABLED:
    urlpatterns += [path("admin/", admin.site.urls)]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
