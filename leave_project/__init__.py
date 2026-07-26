try:
    import pymysql
    pymysql.version_info = (2, 2, 4, "final", 0)
    pymysql.__version__ = "2.2.4"
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

# Monkey patch to bypass Django's version check for MariaDB/MySQL
try:
    from django.db.backends.mysql.base import DatabaseWrapper
    DatabaseWrapper.check_database_version_supported = lambda self: None

    from django.db.backends.mysql.features import DatabaseFeatures
    DatabaseFeatures.can_return_columns_from_insert = False
    DatabaseFeatures.can_return_rows_from_bulk_insert = False
except ImportError:
    pass
