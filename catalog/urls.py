from django.urls import path
from . import views

# Exemplo de correspondência de URL usando expressão regular
#  (?P<SIMB>\d+) dá o nome simbólico SIMB para futura referência (similar a \1, \2...)
#re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),

#path(r'book/year/(?P<year>\d+)/month/(?P<month>\d+)/day/(?P<day>\d+)',
#     views.BookDetailView.as_view(), name='book-detail-bydate')

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBookByUserListView.as_view(), name='my-borrowed'),
    #path('borrowed/', views.AllBorrowedBooks.as_view(), name='borrowed-books'),
    path('borrowed/', views.all_borrowed_books, name='borrowed-books'),
]
