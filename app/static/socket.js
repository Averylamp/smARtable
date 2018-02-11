var socket = io.connect('http://' + document.domain + ':' + location.port);

function display_info(data) {
	console.log(data);
	console.log("Here");
	var points = data.points;
	if (points[0] != -1) {
		var canvas = document.getElementById("myCanvas");
		var ctx = canvas.getContext("2d");
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		ctx.beginPath();
		var radius = 100;
		ctx.arc(points[0],points[1],radius,0,2*Math.PI);
		ctx.lineWidth = 5;
		ctx.strokeStyle = "#000";
		ctx.stroke();
		ctx.fillStyle = 'white';
		ctx.fill();
		ctx.lineWidth = 2;
		ctx.moveTo(points[0] + 120, points[1])
		ctx.lineTo(points[0] + 149, points[1] + 30)
		ctx.stroke();
		ctx.moveTo(points[0] + 120, points[1])
		ctx.lineTo(points[0] + 149, points[1] - 30)
		ctx.stroke();
	}
	var topOffset = Math.min(points[1], 250);

	var leftOffset = points[0] + 150;
	var info = "";
	$("#callouts").html("");
	var detailItems = data.details;
	var detailHeaders = "";
	for (i = 0; i < detailItems.length; i++) {
		detailHeaders += "<h3>" + detailItems[i] + "</h3>";
	}
	console.log(points)
	// $("#callouts").append('<div class="callout ' + pointDir + '" style="top:' + topOffset + 'px; left:' + leftOffset + 'px">' + info + '</div>')
	$("#callouts").append("<div id=\"item\" style=\"left:" + leftOffset + "px; top:" + topOffset + "px;\"><h1>" + data.title + "</h1><img src=\"" + data.image_path + "\"></img>" + detailHeaders + "<div id=\"nutritionalButton\"><h2>Nutritional Info</h2></div></div>");
	// $("#callouts").append("");
	// $("#callouts").append("");
	
	// ("#callouts").append("<div id=\"nutritionalButton\">");
	// ("#callouts").append("<h2>Nutritional Info</h2>");
	// ("#callouts").append("</div>");
	// ("#callouts").append("</div>");
}
// <div id="item">
//   	<h1>Doritos Nacho Cheese</h1>
//   	<img src="{{url_for('static', filename='images/doritos.jpg')}}"></img>
//   	<h3>Product Category: Chips</h3>
// 	<h3>Price: $1.00</h3>
// 	<h3>Store: La Verdes</h3>
// 	<div id="nutritionalButton">
// 		<h2>Nutritional Info</h2>
// 	</div>
//   </div>


socket.on("connect", function() {
	console.log("New connection");
	socket.emit("message", {"data":"testing"})
});

socket.on("get_point", function(data) {
	console.log(data)
	var point = data.result;
	if (point[0] != -1) {
		var canvas = document.getElementById("myCanvas");
		var ctx = canvas.getContext("2d");
		ctx.clearRect(0, 0, canvas.width, canvas.height);
		// ctx.fillStyle = "#FFFFFF";
		ctx.beginPath();
		var radius = 100;
		ctx.arc(point[0],point[1],radius,0,2*Math.PI);
		ctx.lineWidth = 5;
		ctx.strokeStyle = "#000";
		ctx.stroke();
		// ctx.fill();
		// console.log(point);
	};
});

socket.on("get_screen", function(data) {
	console.log(data)
	var corners = data.result;
	var canvas = document.getElementById("myCanvas");
	var ctx = canvas.getContext("2d");
	ctx.clearRect(0, 0, canvas.width, canvas.height);
	ctx.fillStyle = "#FFFFFF";
	ctx.fillRect(corners[0],corners[1],corners[2],corners[3]);
	console.log(corners);
});

socket.on("information", display_info);

socket.on("message", function(data) {
	console.log(data);
});
