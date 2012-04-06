#!/bin/bash

# Copyright (c) 2012 Denim Group, Ltd.
# http://www.denimgroup.com/
# http://blog.denimgroup.com/

export PATH=$PATH:/usr/local/mysql/bin

# Flush MySQL logs
echo "Flushing MySQL logs"
mysqladmin --user=root flush-logs

# Turn off MySQL logging
echo "Stopping MySQL query logging"
mysql -e "SET GLOBAL general_log = 'OFF'" --user=root mysql

