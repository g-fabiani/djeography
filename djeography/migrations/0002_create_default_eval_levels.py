# Generated by Django 5.2.1 on 2025-05-29 18:06

from django.db import migrations

from djeography import DEFAULT_EVAL_LEVELS


def create_default_evaluation_levels(apps, schema_editor):
    EvaluationLevel = apps.get_model('djeography', 'EvaluationLevel')
    for level in DEFAULT_EVAL_LEVELS:
        EvaluationLevel(**level).save()


class Migration(migrations.Migration):
    dependencies = [
        ('djeography', '0001_initial'),
    ]

    operations = [migrations.RunPython(create_default_evaluation_levels)]
