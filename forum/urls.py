from django.urls import path, include
from forum import views

urlpatterns = [
    path('comment/new/<slug:thread_slug>/', views.new_comment, name='new_comment'), #new comment
    path('comment/new/<slug:thread_slug>/<int:parent_id>/', views.new_comment, name='new_comment_reply'), #new comment as a reply to another comment
    path('comment/edit/<int:comment_id>/', views.edit_comment, name='edit_comment'), #edit comment
    path('vote/', views.vote, name='vote'), #upvote
    path('search/', views.search, name='search'), #search
    path('new/', views.new_board, name='new_board'), #new board
    path('<slug:board_slug>/edit/', views.edit_board, name='edit_board'), #edit board 
    path('<slug:board_slug>/thread/<slug:thread_slug>', views.view_thread, name='view_thread'), #view thread
    path('<slug:board_slug>/new/', views.new_thread, name='new_thread'), #new thread
    path('<slug:board_slug>/thread/<slug:thread_slug>/edit/', views.edit_thread, name='edit_thread'), #edit thread
    path('<slug:board_slug>/<slug:method>/', views.view_board, name='view_board'), #view board (choosing method)
    path('<slug:board_slug>/', views.view_board, name='view_board_without_method'),
    path('/', views.index) #index
]
