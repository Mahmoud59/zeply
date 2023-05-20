# Generated by Django 4.1.7 on 2023-05-20 19:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('crypto', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('phone', models.TextField(validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format:'+999999999'.Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserBalance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('balance', models.DecimalField(decimal_places=8, default=0, max_digits=20, validators=[django.core.validators.MinValueValidator(0)])),
                ('currency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_balance_currency', to='crypto.cryptocurrency')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_balance', to='users.useraccount')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdminAccount',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('deleted', models.DateTimeField(db_index=True, editable=False, null=True)),
                ('deleted_by_cascade', models.BooleanField(default=False, editable=False)),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='%(class)s_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
