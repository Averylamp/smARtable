// setInterval(update_screen, 33);
//setInterval(update_screen, 1000);

function update_screen() {
  $.getJSON($SCRIPT_ROOT + '/get_point', {
  }, function(data) {
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
}

// function update_screen() {
//   socket.emit('get_point', {
//   }, function(data) {
//     var point = data.result;
//     if (point[0] != -1) {
//       var canvas = document.getElementById("myCanvas");
//       var ctx = canvas.getContext("2d");
//       ctx.clearRect(0, 0, canvas.width, canvas.height);
//       // ctx.fillStyle = "#FFFFFF";
//       ctx.beginPath();
//       var radius = 100;
//       ctx.arc(point[0],point[1],radius,0,2*Math.PI);
//       ctx.lineWidth = 5;
//       ctx.strokeStyle = "#FFFFFF";
//       ctx.stroke();
//       // ctx.fill();
//       // console.log(point);
//     };
//   });
// }
