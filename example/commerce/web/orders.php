<?php
    session_start();
?>
<html>
<head>
<title>Crap-E-Commerce - Order History</title>
</head>
<body>
<p>
    <a href="index.php">Home</a>
</p>
<?php
	if (isset($_SESSION["user_data"])) {
		$user_data = $_SESSION["user_data"];
		$user_id = $user_data["id"];
?>
		<table>
			<tr>
				<td>Order ID</td>
				<td>Order Date</td>
				<td>Order Status</td>
			</tr>
<?php
		include 'includes/db_connection.php';

		$query = "SELECT * FROM CommerceOrder WHERE user_id = " . $user_id;

		// echo($query . "<br />");

		$result = mysql_query($query);
		while($row = mysql_fetch_array($result)) {
			$line = "<tr><td><a href='order.php?order_id=" . $row["id"] . "'>" . $row["id"] . "</td><td>" . $row["order_date"] . "</td><td>" . $row["status"] . "</td></tr>";
			echo($line . "\n");
		}
?>
		</table>
<?php
	} else {
		//	User is not logged in - therefore no history
?>
		<p>You are not currently logged in. Please <a href="login.php">Log In</a> to see your order history.</p>
<?php

	}
?>
