<?
	if(count($_GET)>0){   //input section
//		send_to_db($_GET["an1"]);
//		send_to_db($_GET["an2"]);
//		send_to_db($_GET["an3"]);
	}
	else{	//output section
		$values["dis1"] = 5;
		$values["dis2"] = 20;
		$values["dis3"] = 10;
		echo json_encode($values); 
	}
?>