from django.db import models
from django.db.models import UniqueConstraint # P/ valores únicos
from django.db.models.functions import Lower # Ret. letras minúsculas de um campo
from django.urls import reverse # get_absolute_url() recolhe URL de um ID
import uuid # Necessário para instância de livros

class Genre(models.Model):
    """Gênero de um livro."""
    name = models.CharField(
        max_length = 200,
        unique = True,
        help_text = "Insira o gênero do livro (ex.: Romance, Ação, "\
        "Ficção científica...)"
    )

    def __str__(self):
        """Retorna o nome do gênero"""
        return self.name

    def get_absolute_url(self):
        """Retorna a URL para acessar os detalhes do gênero."""
        return reverse('genre-detail', args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='genre_name_case_insensitive_unique',
                violation_error_message="Gênero já existe (ignora " \
                "distinção entre maiúscula e minúscula)"
            ),
        ]

class Book(models.Model):
    """Entidade livro, não uma cópia/instância."""
    title = models.CharField(max_length = 200)
    
    # Um livro pode ter mais de um autor, mas esse tutorial assume apenas um
    # Author é declarado como String ao invés de objeto pois esse não foi
    #  declarado ainda no arquivo.  RESTRICT impede o autor de ser removido
    #  da base case tenha algum livro no seu nome
    author = models.ForeignKey('Author', on_delete=models.RESTRICT, null=True)
    
    summary = models.TextField(
        max_length = 1000, help_text = "Breve descrição do livro.")
    isbn = models.CharField('ISBN', max_length=13,
                            unique=True,
                            help_text='13 caracteres <a href="https://' \
                            'www.isbn-international.org/content/what-isbn' \
                            '">número ISBN</a>')
    genre = models.ManyToManyField(
        Genre, help_text = "Escolha um gênero para esse livro.")

    language = models.ForeignKey(
        'Language', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """Retorna o título do livro"""
        return self.title

    def get_absolute_url(self):
        """Retorna a URL para acessar os detalhes desse livro."""
        return reverse('book-detail', args=[str(self.id)])
    
class BookInstance(models.Model):
    """Manigestação física do livro, que pode ser emprestada."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Identificador único para esse " \
                          "livro em toda biblioteca.")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    # Situação do empréstimo
    LOAN_STATUS = (
        ('m', 'Em manuteção'),
        ('e', 'Emprestado'),
        ('d', 'Disponível'),
        ('r', 'Reservado'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Disponibilidade do livro.',
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """Texto representando o objeto Model"""
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    """Modelo que representa o autor"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Retorna a URL para acessar os detalhes desse autor"""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """Texto que representa o modelo objeto"""
        return f'{self.last_name}, {self.first_name}'

class Language(models.Model):
    """Modelo que representa um idioma"""
    name = models.CharField(max_length=200,
                            unique=True,
                            help_text="Insira o idioma original do livro.")

    def get_absolute_url(self):
        """Retorna a URL com os detalhes do idioma"""
        return reverse('language-detail', args=[str(self.id)])

    def __str__():
        """Texto representado o objeto Model"""
        return self.name

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower('name'),
                name='language_name_case_insensitive_unique',
                violation_error_message="Idioma já existe (ignora " \
                "distinção entre maiúscula e minúsculas)"
                ),
            ]
