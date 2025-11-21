from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0001_rawsql_tables'),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE posts ADD COLUMN is_rewarded INTEGER DEFAULT 0;"),
    ]