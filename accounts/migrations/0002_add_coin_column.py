from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_rawsql_tables'),
    ]

    operations = [
        migrations.RunSQL("ALTER TABLE users ADD COLUMN coin INTEGER DEFAULT 0;"),
    ]