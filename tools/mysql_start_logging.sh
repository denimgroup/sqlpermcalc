#!/bin/bash

# Copyright (c) 2012 Denim Group, Ltd.
# http://www.denimgroup.com/
# http://blog.denimgroup.com/

# Stop Apache
echo "Stopping Apache"
sudo apache2ctl stop

# Flush MySQL logs
echo "Flushing MySQL logs"
mysqladmin --user=root --password=password flush-logs

# Turn on MySQL logging
echo "Starting MySQL query logging"
mysql --user=root --password=quickstart < start_logging.sql

# Start Apache
echo "Starting Apache"
sudo apache2ctl start
