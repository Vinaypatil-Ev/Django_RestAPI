from api.views import ClassBasedApiDetails, ClassBasedApiShow, browsable_data, browsable_details, show_data, show_details
from django.urls import path

urlpatterns = [
    path("", show_data),
    path("<int:pk>", show_details),
    path("brows_api/", browsable_data),
    path("brows_api/<int:pk>", browsable_details),
    path("blog/", ClassBasedApiShow.as_view()),
    path("blog/<int:pk>", ClassBasedApiDetails.as_view())

]