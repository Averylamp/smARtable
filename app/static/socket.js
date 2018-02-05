var socket = io.connect('http://' + document.domain + ':' + location.port);

function display_info(data) {
	var pointDir = data['direction'];
	console.log(pointDir);
	var topOffset = data.top;
	var leftOffset = data.left;
	var info = "";
	$.each(data.data, function(k, v) {
		info += k + ": " + v + "\n";
	});
	$("#callouts").append('<div class="callout ' + pointDir + '" style="top:' + topOffset + 'px; left:' + leftOffset + 'px">' + info + '</div>')
}

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
		ctx.strokeStyle = "#FFFFFF";
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
