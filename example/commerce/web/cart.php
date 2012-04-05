<?php
    session_start();

	//	Create a cart if we don't have one
	if(isset($_SESSION["cart"])) {
		$cart = $_SESSION["cart"];
	} else { 
		$cart = array();
		$_SESSION["cart"] = $cart;
	}

	if(isset($_POST["product_id"])) {
		//	Adding an item before displaying
		
		$product_id = $_POST["product_id"];
		$product_quantity = $_POST["quantity"];
		
		include 'includes/db_connection.php';

		$query = "SELECT name, price FROM Product WHERE id = " . $product_id;

		$result = mysql_query($query);

		if(mysql_num_rows($result) > 0) {
            $row = mysql_fetch_array($result);
			$cart_item = array(
				"product_id" => $product_id,
				"name" => $row["name"],
				"quantity" => $product_quantity,
				"price" => $row["price"]
			);

			array_push($cart, $cart_item);
			$_SESSION["cart"] = $cart;

		} else {
			echo("Bad product ID passed in: " . $product_id . "<br />");
		}
	}
?>
<html>
    <head>
        <title>Crap-E-Commerce - Cart</title>
    </head>
    <body>
        <p> 
            <a href="index.php">Home</a>
        </p>
		<p>
			<table>
				<tr>
					<td>Product ID</td>
					<td>Name</td>
					<td>Quantity</td>
					<td>Price</td>
					<td>Extended Price</td>
				</tr>
<?php
	$subtotal = 0;

	foreach($cart as &$value) {
		$line = "<tr><td>" . $value["product_id"]
			. "</td><td>" . $value["name"]
			. "</td><td>" . $value["quantity"]
			. "</td><td>" . $value["price"]
			. "</td><td>" . $value["quantity"] * $value["price"]
			. "</td></tr>";

		$subtotal += $value["quantity"] * $value["price"];

		echo($line . "\n");
	}

	$shipping = 10;
	$tax = $subtotal * 0.08;
	$total = $subtotal + $shipping + $tax;

	echo("<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>Subtotal:</td><td>" . $subtotal . "</td></tr>");
	echo("<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>Shipping:</td><td>" . $shipping . "</td></tr>");
	echo("<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>Tax:</td><td>" . $tax . "</td></tr>");
	echo("<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>Total:</td><td>" . $total . "</td></tr>");
?>
			
			</table>
		</p>
		<p>
			<a href="products.php">Back to Shopping</a>
		</p>
		<p>
			<a href="checkout.php">Checkout</a>
		</p>
	</body>
</html>
