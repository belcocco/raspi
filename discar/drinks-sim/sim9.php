<html> 
	<head> 
		<script type="text/javascript"src="Drinks.js"></script> 

	</head> 
	<body>
		<div style="border: 2px outset #ddd; float:left; width:60px; height:200px; background-color:#333;">
			<led type="rect" width="60" height="20" id="led1" style="float:left;" color="red"></led> 
			<led type="rect" width="60" height="20" id="led2" style="float:left;" color="red"></led> 
			<led type="rect" width="60" height="20" id="led3" style="float:left;" color="red"></led> 
			<led type="rect" width="60" height="20" id="led4" style="float:left;" color="red"></led> 
			<led type="rect" width="60" height="20" id="led5" style="float:left;" color="yellow"></led> 
			<led type="rect" width="60" height="20" id="led6" style="float:left;" color="yellow"></led> 
			<led type="rect" width="60" height="20" id="led7" style="float:left;" color="yellow"></led> 
			<led type="rect" width="60" height="20" id="led8" style="float:left;" color="green"></led> 
			<led type="rect" width="60" height="20" id="led9" style="float:left;" color="green"></led> 
			<led type="rect" width="60" height="20" id="led10" style="float:left;" color="green"></led> 
		</div>

		<knob id="k1" radius="60" onchange="for(var i in Drinks.leds){if(i<this.value){Drinks.leds[9-i].on();}else{Drinks.leds[9-i].off();}}">
	</body> 
</html> 