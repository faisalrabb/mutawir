from django.urls import path, include
from projects import views

urlpatterns = [
    path('<slug: project_name>/', views.view_project, name='view_project'),
    path('<slug: project_name>/products/', views.products_index, name='products_index'),
    path('<slug: project_name>/products/<int: id>/', views.view_product, name='view_product'),
    path('<slug: project_name>/proposal/', views.proposal, name='proposal'),
    path('<slug: project_name>/proposal/<int: num>/delete/', views.proposal, name='proposal_delete'),
    path('<slug: project_name>/proposal/goal/', views.motion_goal, name='proposal_goal'),
    path('<slug: project_name>/proposal/release/', views.motion_release, name='proposal_release'),
    path('<slug: project_name>/proposal/role/', views.motion_role., name='proposal_role'),
    path('<slug: project_name>/proposal/group/', views.motion_group, name='proposal_group'),
    path('<slug: project_name>/proposal/pool/', views.motion_pool, name='proposal_pool'),
    path('<slug: project_name>/proposal/project/', views.motion_project, name='proposal_project'),
    path('<slug: project_name>/proposal/product/', views.motion_product, name='proposal_product'),
    path('<slug: project_name>/proposal/members/', views.motion_members, name='proposal_members'),
    path('<slug: project_name>/proposal/<int: num>/delete/', views.proposal_delete, name='proposal_delete'),
    path('<slug: project_name>/motion/<int: num>/delete/', views.motion_delete, name='motion_delete'),
    path('<slug: project_name>/edit/', views.edit_project, name='edit_project'),
    path('<slug: project_name>/vote/<id: proposal_num>/', views.vote, name='vote'),
    path('<slug: project_name>/star/', views.star, name='star'),
    path('new/', views.new_project, name='new_project'), 
    path('search/', views.search, name='search'),
    path('licenses/', views.licenses, name='licenses'),
    path('/', views.index, name='index'),
]