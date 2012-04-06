#!/bin/bash

# Copyright (c) 2012 Denim Group, Ltd.
# http://www.denimgroup.com/
# http://blog.denimgroup.com/

export PATH=$PATH:/usr/local/mysql/bin

# Stop Apache
echo "Stopping Apache"
sudo apachectl stop

# Flush and DELETE existing MySQL logs
echo "Flushing MySQL logs"
mysqladmin --user=root flush-logs
mysql -e "TRUNCATE TABLE mysql.general_log" --user=root mysql

# Turn on MySQL logging
echo "Starting MySQL query logging"
mysql -e "SET GLOBAL log_output = 'TABLE'" --user=root mysql
mysql -e "SET GLOBAL general_log = 'ON'" --user=root mysql

# Start Apache
echo "Starting Apache"
sudo apachectl start
