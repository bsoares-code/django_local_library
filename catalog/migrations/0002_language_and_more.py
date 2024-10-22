# Generated by Django 4.2.16 on 2024-10-17 19:15

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.functions.text


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Insira o idioma original do livro.', max_length=200, unique=True)),
            ],
        ),
        migrations.RemoveConstraint(
            model_name='genre',
            name='genre_name_case_insensitive_unique',
        ),
        migrations.AddConstraint(
            model_name='genre',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='genre_name_case_insensitive_unique', violation_error_message='Gênero já existe (ignora distinção entre maiúscula e minúscula)'),
        ),
        migrations.AddConstraint(
            model_name='language',
            constraint=models.UniqueConstraint(django.db.models.functions.text.Lower('name'), name='language_name_case_insensitive_unique', violation_error_message='Idioma já existe (ignora distinção entre maiúscula e minúsculas)'),
        ),
        migrations.AddField(
            model_name='book',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.language'),
        ),
    ]
