#!/bin/bash

# Copyright (c) 2012 Denim Group, Ltd.
# http://www.denimgroup.com/
# http://blog.denimgroup.com/

export PATH=$PATH:/usr/local/mysql/bin

STR_START="SELECT argument FROM mysql.general_log WHERE command_type = 'Query' AND user_host LIKE '%"
STR_END="%';"

TARGET_USERNAME=$1

STR_FINAL=$STR_START$TARGET_USERNAME$STR_END
echo SQL query to execute: $STR_FINAL

# sudo mv /usr/local/mysql/data/query_log_mysql.sql /usr/local/mysql/data/query_log_mysql.sql.bak

echo "About to dump logs from MySQL"
echo "Query will be: $STR_FINAL"

# echo $STR_FINAL | mysql --user=root mysql


mysql --skip-column-names -e "$STR_FINAL" --user=root mysql > query_log_mysql.sql

echo "About to copy MySQL log to local directory"

# sudo cp /usr/local/mysql/data/query_log_mysql.sql ./
