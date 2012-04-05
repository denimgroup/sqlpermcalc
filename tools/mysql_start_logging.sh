#!/bin/bash

# Copyright (c) 2012 Denim Group, Ltd.
# http://www.denimgroup.com/
# http://blog.denimgroup.com/

export PATH=$PATH:/usr/local/mysql/bin

# Stop Apache
echo "Stopping Apache"
sudo apachectl stop

# Flush MySQL logs
echo "Flushing MySQL logs"
mysqladmin --user=root flush-logs

# Turn on MySQL logging
echo "Starting MySQL query logging"
mysql --user=root < start_logging_mysql.sql

# Start Apache
echo "Starting Apache"
sudo apachectl start
