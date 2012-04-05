<?php
    session_start();
?>
<html>
    <head>
        <title>Crap-E-Commerce - Login</title>
    </head>
    <body>
		<p>
			<a href="index.php">Home</a>
		</p>
<?php
	if (isset($_POST["email"])) {
		include 'includes/db_connection.php';
		$query = "SELECT * FROM CommerceUser WHERE email = '" . $_POST["email"] . "' AND password = '" . $_POST["password"] . "'";
		// echo($query . "<br />");
		$result = mysql_query($query);

		if(mysql_num_rows($result) > 0) {
			$row = mysql_fetch_array($result);
			//	Successful login
			$user_data = array (
    			"id" => $row["id"],
    			"email" => $row["email"],
    			"first_name" => $row["first_name"],
    			"last_name" => $row["last_name"]
			);
			$_SESSION["user_data"] = $user_data;

			$dont_show_form = 1;

			$greeting = "Welcome " . $user_data["first_name"] . " " . $user_data["last_name"];
			echo($greeting . "<br />");

		} else {
			//	Bad login
			echo("Sorry your username or password was incorrect" . "<br />");
		}

		mysql_close();
	}
?>

<?php
	//	Double negative! :)
	if(!isset($dont_show_form)) {
?>
        <p>
            Login:
            <form method="POST" action="login.php">
                Email: <input name="email" /><br />
                Password: <input type="password" name="password" /><br />
                <input type="submit" value="Login" />
            </form>
        </p>
<?php
	}
?>
    </body>
</html>

