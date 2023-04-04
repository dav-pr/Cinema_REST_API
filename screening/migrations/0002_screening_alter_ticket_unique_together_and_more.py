# Generated by Django 4.1.7 on 2023-04-01 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cinema_hall', '0001_initial'),
        ('screening', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Screening',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('screening_date', models.DateField()),
                ('screening_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='screenings', to='screening.screeningsession')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='screening',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='screening.screening'),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together={('screening', 'seat')},
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='session_date_time',
        ),
    ]
