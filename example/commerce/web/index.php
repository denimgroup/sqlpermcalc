<?php
	session_start();
?>
<html>
	<head>
		<title>Crap-E-Commerce - Home</title>
	</head>
	<body>
<?php
	if(isset($_SESSION["user_data"])) {
		$has_session = 1;
		$user_data = $_SESSION["user_data"];
		$greeting = "Welcome " . $user_data["first_name"] . " " . $user_data["last_name"];
		echo($greeting . "<br />");
	}
?>
		<p>
			Stuff you can do:
			<ul>
				<li><a href="products.php">Shop Online</a></li>
				<li><a href="cart.php">View Cart</a></li>
<?php
	if(!isset($has_session)) {
?>
				<li><a href="create_user.php">Create a User</a></li>
				<li><a href="login.php">Log In</a></li>
<?php
	} else {
?>
				<li><a href="orders.php">View Orders</a></li>
				<li><a href="logout.php">Log Out</a></li>
<?php
	}
?>
			</ul>
		</p>
	</body>
</html>
