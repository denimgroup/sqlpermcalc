#!/bin/bash

# Copyright (c) 2012 Denim Group, Ltd.
# http://www.denimgroup.com/
# http://blog.denimgroup.com/

# mysql --user=root "SELECT argument FROM mysql.general_log WHERE command_type = 'Query' AND user_host LIKE '%spc_default%' INTO OUTFILE 'query_log_mysql.sql';"

echo "SELECT argument FROM mysql.general_log WHERE command_type = 'Query' AND user_host LIKE '%spc_default%' INTO OUTFILE 'query_log_mysql.sql';" | mysql --user=root mysql

sudo cp /usr/local/mysql/data/query_log_mysql.sql ./
