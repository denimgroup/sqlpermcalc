<?php
    session_start();
?>
<html>
    <head>
        <title>Crap-E-Commerce - Checkout</title>
    </head>
    <body>
        <p> 
            <a href="index.php">Home</a>
        </p>
<?php
	if(isset($_SESSION["user_data"])) {
		//	Have a logged-in user.
		if(!isset($_POST["number"])) {
			// No payment data in request. Need to display the order form
?>
		<p>
			Please enter payment information:
		</p>
		<form action="checkout.php" method="POST">
			Credit Card Number: <input name="number" /><br />
			Credit Card Type: <input name="type" /><br />
			Expiration (MMYY): <input name="expiration" /><br />
			CVV (code on back): <input name="cvv" /><br />
			<input type="submit" value="Place My Order" />
		</form>
<?php
		} else {
			//	Payment data is in request. Place the order
			$number = $_POST["number"];
			$type = $_POST["type"];
			$expiration = $_POST["expiration"];
			$cvv = $_POST["cvv"];

			include 'includes/db_connection.php';

			//	Create the credit card entry

			$query = "INSERT INTO CreditCard (number, type,  expiration, cvv) VALUES ('"
				. $number . "', '"
				. $type . "', '"
				. $expiration . "', '"
				. $cvv . "')";

			echo($query . "<br />");

			mysql_query($query);

			$credit_card_id = mysql_insert_id();

			//	Create the main Order entry

			$user_data = $_SESSION["user_data"];
			$cart = $_SESSION["cart"];

			$subtotal = 0;
			foreach($cart as &$value) {
				$subtotal += $value["quantity"] * $value["price"];
			}

			$shipping = 10;
    		$tax = $subtotal * 0.08;
    		$total = $subtotal + $shipping + $tax;

			$query = "INSERT INTO CommerceOrder (user_id, credit_card_id, tax, shipping) VALUES (" . $user_data["id"] . ", " . $credit_card_id . ", " . $tax . ", " . $shipping . ")";
			echo($query . "<br />");

			mysql_query($query);

			$order_id = mysql_insert_id();

			//	Create the line item entries

			foreach($cart as &$value) {
				$query = "INSERT INTO OrderItem (order_id, product_id, product_name, quantity, price) VALUES ("
					. $order_id . ", "
					. $value["product_id"]
					. ", '" . $value["name"]
					. "', " . $value["quantity"]
					. ", " . $value["price"] . ")";
				echo($query . "<br />");
			
				mysql_query($query);
			}

			unset($_SESSION["cart"]);
			
			echo("Thank you for your order. Your Order ID is: " . $order_id . "<br />");
		}

	} else {
		//	User needs to log in or create account
		echo("<p>You are not logged in. You should either <a href='login.php'>Log In</a> or <a href='create_user.php'>Create an Account</a>.</p>");
	}
?>
		<p><a href="products.php">Back to Shopping</a></p>
	</body>
</html>
