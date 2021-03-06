# Generated by Django 2.0.8 on 2018-12-27 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionmaster',
            name='answer_len',
            field=models.IntegerField(blank=True, default=1, verbose_name='入力文字数'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionmaster',
            name='answer_regex',
            field=models.TextField(blank=True, verbose_name='チェック用正規表現'),
        ),
    ]
