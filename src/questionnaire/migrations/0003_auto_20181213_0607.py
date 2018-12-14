# Generated by Django 2.0.8 on 2018-12-13 06:07

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0002_auto_20181212_0816'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('system_name', models.TextField(verbose_name='システム名')),
                ('diag_when', models.DateField(blank=True, verbose_name='診断月')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('updated_by', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='diagnosis',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='questionnaire.Diagnosis'),
            preserve_default=False,
        ),
    ]