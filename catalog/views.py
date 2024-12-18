import datetime

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

from .models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm

def index(request):
    """Tela inicial p/ Biblioteca Local"""

    # Gera a quantidade de alguns dos objetos principais
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Livros disponíveis (status = 'd')
    num_instances_available = BookInstance.objects.filter(status__exact='d').count()

    # 'all()' está implícito
    num_authors = Author.objects.count()

    # Número de visitantes dessa página, contado variável session
    num_visits = request.session.get('num_visits', 0)
    num_visits += 1
    request.session['num_visits'] =  num_visits

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }

    # Renderiza o modelo HTML index.html com os dados na variável context
    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    #context_object_name = 'book_list' # Nome próprio p/ a lista como uma variável modelo
    #queryset = Book.objects.filter(title__icontains='lord')[:5] # Recolhe 5 livros contendo a palavra no título
    #template_name = 'books/my_arbitrary_temple_name_list.html' # Especifique seu próprio caminho p/ o modelo

    # Também é possível sobrescrever get_context_data para passar variáveis de contexto adicionais
    #  para o modelo.  Exemplo a seguir mostra como adicionar a variável some_data p/ o
    #  contexto
    # def get_context_data(self, **kwargs):
    #     # Chama a implementação base para recolher o contexto
    #     context = super(BookListView, self).get_context_data(**kwargs)

    #     # Gera quaisquer dados e adiciona ao contexto
    #     context['some_data'] = 'Quaisquer dados'
    #     return context

    
class BookDetailView(generic.DetailView):
    model = Book


class AuthorDetailView(generic.DetailView):
    model = Author
    # Modelo html padrão em templates/catalog/author_detail.html


class AuthorListView(generic.ListView):
    model = Author
    # Template padrão em templates/catalog/author_list.html

    
class LoanedBookByUserListView(LoginRequiredMixin, generic.ListView):
    """Listagem de livros emprestados com base em classe genérica."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user)
            .filter(status__exact='e')
            .order_by('due_back')
        )


# Para a visualização de todos livros emprestados, quero fazer em forma
#  de função, mas deixarei a forma de classe implementada
class AllBorrowedBooks(PermissionRequiredMixin, generic.ListView):
    """Listagem de todos os livros emprestados."""
    permission_required = 'catalog.can_mark_returned'
    model = BookInstance
    template_name = 'catalog/all_borrowed_books.html'
    paginate_by = 10

    def get_queryset(self):
        return (
            BookInstance.objects.filter(status__exact='e')
            .order_by('due_back')
        )


@permission_required('catalog.can_mark_returned')
def all_borrowed_books(request):
    bookinstance_list = BookInstance.objects.filter(status__exact='e').order_by('due_back')

    paginator = Paginator(bookinstance_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'bookinstance_list': bookinstance_list,
        'page_obj': page_obj,
    }

    return render(request, 'catalog/all_borrowed_books.html', context=context)

def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # Caso seja POST, processe os dados do formulário
    if request.method == 'POST':

        # Crie uma instância de formulário e a popule com os dados da solicitação
        form = RenewBookForm(request.POST)

        # Verifique se o formulário é válido
        if form.is_valid():
            # Processe os dados em form.cleaned_data conforme necessário
            #  aqui é apenas verificado a data de renovação
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # Redirecione para uma nova URL
            return HttpResponseRedirect(reverse('all-borrowed'))

    # Caso seja GET (ou outros), produza um formulário padrão
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)
