# Generated by Django 4.2.4 on 2023-09-02 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0003_remove_document_signed_hash_alter_document_signature'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='hash',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='Hash'),
        ),
    ]
