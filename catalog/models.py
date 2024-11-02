from django.db import models
from django.db.models import UniqueConstraint # P/ valores únicos
from django.db.models.functions import Lower # Ret. letras minúsculas de um campo
from django.urls import reverse # get_absolute_url() recolhe URL de um ID
from django.conf import settings
from django.contrib.auth.models import User
from datetime import date
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
    
    # Um livro pode ter mais de um autor, mas esse tutorial assume apenas um.
    # Author é declarado como String ao invés de objeto pois esse não foi
    #  declarado ainda no arquivo.  RESTRICT impede o autor de ser removido
    #  da base caso tenha algum livro no seu nome
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

    def display_genre(self):
        """Retorna texto mostrando os três primeiros gêneros para o painel Adm.
           Necessário para campos tipo muitos para muitos na base de dados"""
        return ', '.join(genre.name for genre in self.genre.all()[:3])

    # Nome da coluna no painel Adm dessa classe
    display_genre.short_description = 'Genre'
    
class BookInstance(models.Model):
    """Manifestação física de um livro"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                          help_text="Identificador único para esse " \
                          "livro em toda biblioteca.")
    book = models.ForeignKey('Book', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200, help_text='Editora')
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

    borrower = models.ForeignKey(User,
                                 on_delete=models.SET_NULL,
                                 null=True, blank=True)

    @property
    def is_overdue(self):
        """Determina se um livro esta atrasado com base no dia atual."""
        # Necessário validar se a data de retorno existe
        return bool(self.due_back and date.today() > self.due_back)

    # Funcionalidade substituida por is_overdue, deixado aqui para referencia
    # def display_expected_return(self):
    #     """Dias que faltam para o retorno ou se já expirou"""
    #     today = date.today()

    #     # Ainda no prazo
    #     if self.status == 'e' and self.due_back >= today:
    #         time_left = self.due_back - today
    #         day_msg = ''
    #         match time_left:
    #             case 0:
    #                 day_msg = 'para hoje'
    #             case 1:
    #                 day_msg = 'para amanhã'
    #             case _:
    #                 day_msg = f'em {time_left.days} dias'

    #         msg = f'Retorno esperado {day_msg}'
    #         return msg

    #     # Atrasado
    #     elif self.status == 'e' and self.due_back < today:
    #         overtime = today - self.due_back
    #         day_msg = 'desde ontem' if overtime.days == 1 else f'em {overtime.days} dias'
    #         msg = f'Entrega atrasada {day_msg}'
    #         return msg

    #     return '-'

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Marcar livro como devolvido"),)

    def __str__(self):
        """Texto que representa a instância"""
        return f'{self.id} ({self.book.title})'

    #display_expected_return.short_description = 'Devolução'
            

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

    def __str__(self):
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
