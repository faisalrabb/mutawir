# Generated by Django 3.1 on 2021-01-09 08:17

import autoslug.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import forum.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='thread',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='board',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='forum.category'),
        ),
        migrations.AddField(
            model_name='board',
            name='country',
            field=models.CharField(blank=True, choices=[('DZ', 'Algeria'), ('BH', 'Bahrain'), ('EG', 'Egypt'), ('IQ', 'Iraq'), ('JO', 'Jordan'), ('KW', 'Kuwait'), ('LB', 'Lebanon'), ('LY', 'Libya'), ('MR', 'Mauritania'), ('MA', 'Morocco'), ('OM', 'Oman'), ('PS', 'Palestine'), ('SY', 'Syria'), ('QA', 'Qatar'), ('KSA', 'Saudi Arabia'), ('SD', 'Sudan'), ('TN', 'Tunisia'), ('UAE', 'United Arab Emirates'), ('WS', 'Western Sahara'), ('YE', 'Yemen')], default=None, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='board',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='board',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='board',
            name='moderators',
            field=models.ManyToManyField(blank=True, related_name='moderates', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='board',
            name='name',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='board',
            name='rules',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='board',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', editable=False, populate_from='name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='category',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='forum.comment'),
        ),
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='thread',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='forum.thread'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_comments', to='accounts.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thread',
            name='board',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='threads', to='forum.board'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thread',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='hot_score',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='thread',
            name='image',
            field=models.ImageField(blank=True, upload_to=forum.models.upload_dest_forum),
        ),
        migrations.AddField(
            model_name='thread',
            name='last_edited',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='thread',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='', editable=False, populate_from='title', unique_with=('board',)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thread',
            name='text',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thread',
            name='title',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='thread',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to='accounts.user'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='thread',
            unique_together={('slug', 'board')},
        ),
        migrations.CreateModel(
            name='Upvote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='forum.comment')),
                ('thread', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='upvotes', to='forum.thread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
