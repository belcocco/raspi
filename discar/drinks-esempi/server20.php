<? 
	session_start(); 
	if(isset($_GET["get"])){ 
		if($_SESSION["sw"]=="1"){ 
			echo "1"; 
		}	 
	} 
	else{ 
		$_SESSION["sw"] = $_POST["sw"]; 
		$_SESSION["sl"] = $_POST["sl"]; 
		$_SESSION["kn"] = $_POST["kn"]; 
		echo $_SESSION["sw"].":".$_SESSION["sl"].":".$_SESSION["kn"];	 
	} 
?>