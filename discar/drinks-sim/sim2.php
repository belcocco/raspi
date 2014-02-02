<?
	session_start();
	if(!empty($_POST)){
		$_SESSION["an1"] = $_POST["an1"];
		$_SESSION["an2"] = $_POST["an2"];
	}else if(isset($_GET["get"])){
		$val["lev1"] = $_SESSION["an1"];
		$val["lev2"] = $_SESSION["an2"];	
		echo json_encode($val);
	}
	else{
echo"		<html>
			<head>
				<script type=\"text/Javascript\" src=\"Drinks.js\"></script>
				<script type=\"text/Javascript\">
					var man = Drinks.createManager();
					man.href = \"sim2.php?get\";
					man.refresh = \"2\";
					man.start();
					
				</script>

			</head>
			<body style=\"background-image:url(polyester.png);\">	
				<display type=\"level\" id=\"lev1\" label=\"AMPERE\" max_range=\"2\" rounded=true></display>
				<display type=\"level\" id=\"lev2\" label=\"VOLT\" max_range=\"30\" rounded=true></display>
				<switch type=\"rect\" id=\"sw1\" onchange=\"lev2.max_range=2;\"></switch>
			</body>
		</html>";

	}
