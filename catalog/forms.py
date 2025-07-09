import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from catalog.models import BookInstance

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Digite uma data entre agora e 4 semanas (padrão 3)")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Data no passado?
        if data < datetime.date.today():
            raise ValidationError(_('Data inválida - renovação no passado'))

        # Data dentro do intervalo de tempo permitido?
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Data inválida - renovação com mais de 4 semanas adiante'))

        # Retorna data limpa/sanitizada
        return data

# Teste de ModelForm, não utilizado
# class RenewBookForm_(forms.ModelForm):
#     # Perceba como clean_<NOME> usa o nome vindo da classe e não o
#     # nome do campo criado por forms.DateField
#     def clean_due_back(self):
#         # Data no passado?
#         if data < datetime.date.today():
#             raise ValidationError(_('Data inválida - renovação no passado'))
        
#         # Data maior que o intervalor de tempo permitido?
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_('Data inválida - renovação com mais de 4 semana adiante'))
        
#         return data

#     class Meta:
#         model = BookInstance
#         fields = ['due_back']
#         labels = {'due_back': _('Nova data de devolução.')}
#         help_texts = {'due_back': _('Digite uma data entre agora e 4 semanas (padrão 3)')}