<?php
    session_start();
?>
<html>
<head>
<title>Crap-E-Commerce - Create a User</title>
</head>
<body>
<p>
	<a href="index.php">Home</a>
</p>
<?php
if (isset($_POST["email"])) {

// echo("Creating new user<br />");

include 'includes/db_connection.php';

$query = "INSERT INTO CommerceUser (email, password, first_name, last_name) VALUES ('" . $_POST["email"] . "', '" . $_POST["password"] . "', '" . $_POST["first_name"] . "', '" . $_POST["last_name"] . "')";

// echo($query . "<br />");

mysql_query($query);

$user_id = mysql_insert_id();

$user_data = array (
	"id" => $user_id,
	"email" => $_POST["email"],
	"first_name" => $_POST["first_name"],
	"last_name" => $_POST["last_name"]
);

$_SESSION["user_data"] = $user_data;

mysql_close();

?>
	<p>
		User created!<br />
	</p>
<?php

} else {
?>

<p>
	Create a User:
	<form method="POST" action="create_user.php">
		Email: <input name="email" /><br />
		Password: <input type="password" name="password" /><br />
		First Name:: <input name="first_name" /><br />
		Last Name: <input name="last_name" /><br />
		<input type="submit" value="Create User" />
	</form>
</p>
<?php
	}
?>
    </body>
</html>

