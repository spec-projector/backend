from apps.core.rest.routers import AppRouter
from . import views

app_name = 'projects'

router = AppRouter()

router.register('projects', views.ProjectsViewset, 'projects')

urlpatterns = [
    *router.urls
]
