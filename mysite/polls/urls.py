from django.urls import path

from . import views

# using Djangos 'generic views' system :
app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # DetailView generic view expects primary key value captured from URL to be called 'pk'
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

# using hard-coded views :
# app_name = 'polls'
# urlpatterns = [
#     # ex: /polls/
#     path('', views.index, name='index'),
#     # ex: /polls/5/
#     # once the URL requests this path, Django then goes to 'views' file & loads the detail view
#     # using angle brackets captures part of the URL & sends it as a keyword argument to the view function
#     # the 'question_id' portion is used when identifying match pattern of the argument in 'views'
#     # the 'name' value as called by the {% url %} template tag
#     path('<int:question_id>/', views.detail, name='detail'),
#     # ex: /polls/5/results/
#     path('<int:question_id>/results/', views.results, name='results'),
#     # ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]


