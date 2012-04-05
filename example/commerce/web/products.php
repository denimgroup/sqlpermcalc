<?php
    session_start();
?>
<html>
    <head>
        <title>Crap-E-Commerce - Product Catalog</title>
    </head>
    <body>
		<p>
            <a href="index.php">Home</a>
        </p>
		<p>
			<b>Products:</b><br />
			<table>
				<tr>
					<td>Product ID</td>
					<td>Name</td>
					<td>Description</td>
					<td>Price</td>
					<td>Quantity</td>
					<td>Purchase</td>
				</tr>

<?php
	include 'includes/db_connection.php';

	$query = "SELECT * FROM Product";
	$result = mysql_query($query);
	while($row = mysql_fetch_array($result)) {
		$line = "<form action='cart.php' method='POST'><tr><td><input type='hidden' name='product_id' value='" . $row["id"] . "' />" . $row["id"]
			. "</td><td>" . $row["name"]
			. "</td><td>" . $row["description"]
			. "</td><td>" . $row["price"]
			. "</td><td><input name='quantity' value='1' /></td><td><input type='submit' value='Add to Cart' /></td></tr></form>\n";
		echo($line);
	}

	mysql_close();
?>
			</table>
		</p>
	</body>
</html>
