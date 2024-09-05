from django.urls import path
from .views import AboutView, RulesView, ServerErrorView

app_name = 'pages'

urlpatterns = [
    path('about/', AboutView.as_view(), name='about'),
    path('rules/', RulesView.as_view(), name='rules'),
    path('server-error/', ServerErrorView.as_view(), name='server_error'),
]
