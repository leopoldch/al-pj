import pymysql

# Make pymysql behave like MySQLdb for Django compatibility
pymysql.install_as_MySQLdb()

# Patch version info to satisfy Django's mysqlclient version check
# Django >= 4.2 requires mysqlclient >= 2.2.1
pymysql.version_info = (2, 2, 7, "final", 0)
