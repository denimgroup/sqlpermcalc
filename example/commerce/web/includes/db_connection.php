<?php

	$username = "spc_default";	//	16 char username limit from MySQL
	$password = "sqlpermcalc_default_password";
	$database = "sqlpermcalc_commerce";

	mysql_connect('127.0.0.1', $username, $password);
	mysql_select_db($database) or die ("Unable to connect to database");

?>
