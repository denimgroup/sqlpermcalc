<?php
    session_start();
?>
<html>
    <head>
        <title>Crap-E-Commerce - Order Detail</title>
    </head>
    <body>
        <p>
            <a href="index.php">Home</a>
        </p>
        <p>
            <a href="orders.php">Back to Order History</a>
        </p>
<?php
	$order_id = $_GET["order_id"];

	include 'includes/db_connection.php';

	$query = "SELECT order_date, tax, shipping, order_status FROM CommerceOrder WHERE id = " . $order_id;
	// echo($query . "<br />");

	$result = mysql_query($query);

	if(mysql_num_rows($result) > 0) {
		$row = mysql_fetch_array($result);

		$order_date = $row["order_date"];
		$order_tax = $row["tax"];
		$order_shipping = $row["shipping"];
		$order_status = $row["status"];

		echo("Order ID: " . $order_id . "<br />");
		echo("Order Date: " . $order_date . "<br />");
		echo("Order Status: " . $order_status . "<br />");

		echo("<table><tr>");
		echo("<td>Product ID</td>");
		echo("<td>Name</td>");
		echo("<td>Quantity</td>");
		echo("<td>Price</td>");
		echo("<td>Extended Price</td>");
		echo("</tr>");

		$query = "SELECT * FROM OrderItem WHERE order_id = " . $order_id;
		// echo($query . "<br />");

		$subtotal = 0;

		$result = mysql_query($query);
        while($row = mysql_fetch_array($result)) {

			$line = "<tr><td>" . $row["product_id"] . "</td><td>"
				. $row["product_name"] . "</td><td>"
				. $row["quantity"] . "</td><td>"
				. $row["price"] . "</td><td>"
				. $row["quantity"] * $row["price"] . "</td></tr>";

			echo($line . "<br />");

			$subtotal += $row["quantity"] * $row["price"];

		}

		$total = $subtotal + $order_shipping + $order_tax;

		echo("<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>Subtotal:</td><td>" . $subtotal . "</td></tr>");
    	echo("<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>Shipping:</td><td>" . $order_shipping . "</td></tr>");
    	echo("<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>Tax:</td><td>" . $order_tax . "</td></tr>");
    	echo("<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>Total:</td><td>" . $total . "</td></tr>");


	} else {
		echo("Order ID: " . $order_id . " is invalid<br />");
	}
?>
	</body>
</html>
