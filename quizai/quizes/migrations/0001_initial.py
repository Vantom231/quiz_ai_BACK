# Generated by Django 5.1.1 on 2024-12-10 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resoults',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accuracy', models.IntegerField()),
                ('questions_quantity', models.IntegerField()),
                ('creation_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name=255)),
                ('level', models.IntegerField()),
                ('difficulty', models.IntegerField()),
                ('number_finished', models.IntegerField(blank=True, default=0)),
                ('number_of_questions', models.IntegerField(default=5)),
                ('level_class', models.IntegerField(blank=True, null=True)),
                ('question', models.TextField(blank=True, null=True, verbose_name=255)),
            ],
        ),
    ]
