# Monkey patch to bypass Django's version check for MariaDB/MySQL because XAMPP uses MariaDB 10.4
# Also disable RETURNING features because MariaDB < 10.5 does not support it.
try:
    from django.db.backends.mysql.base import DatabaseWrapper
    DatabaseWrapper.check_database_version_supported = lambda self: None

    from django.db.backends.mysql.features import DatabaseFeatures
    DatabaseFeatures.can_return_columns_from_insert = False
    DatabaseFeatures.can_return_rows_from_bulk_insert = False
except ImportError:
    pass
