import datetime

from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(
        help_text="Digite uma data entre agora e 4 semanas (padrão 3).")

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
