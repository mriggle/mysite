# Generated by Django 4.2.6 on 2023-11-02 19:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_response'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='response',
            name='choice_text',
        ),
        migrations.AddField(
            model_name='response',
            name='choice',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.choice'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='response',
            name='question',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='polls.question'),
            preserve_default=False,
        ),
    ]
