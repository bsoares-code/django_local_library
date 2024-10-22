from django.shortcuts import render
from django.views import generic
from .models import Book, Author, BookInstance, Genre

def index(request):
    """Tela inicial p/ Biblioteca Local"""

    # Gera a quantidade de alguns dos objetos principais
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Livros disponíveis (status = 'd')
    num_instances_available = BookInstance.objects.filter(status__exact='d').count()

    # 'all()' está implícito
    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    # Renderiza o modelo HTML index.html com os dados na variável context
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    #context_object_name = 'book_list' # Nome próprio p/ a lista como uma variável modelo
    #queryset = Book.objects.filter(title__icontains='lord')[:5] # Recolhe 5 livros contendo a palavra no título
    #template_name = 'books/my_arbitrary_temple_name_list.html' # Especifique seu próprio caminho p/ o modelo

    # É possível sobrescrever métodos para mudar a lista de registros retornados
    #  o código a seguir é um exemplo e não possui nenhum benefício comparado
    #  ao outro método usado na variável "queryset" acima
    #def get_queryset(self):
    #    return Book.objects.filter(tittle__icontains='lord')[:5]

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