setInterval(update_screen, 33);

function update_screen() {
  $.getJSON($SCRIPT_ROOT + '/get_point', {
  }, function(data) {
    var point = data.result;
    if (point[0] != -1) {
      var canvas = document.getElementById("myCanvas");
      var ctx = canvas.getContext("2d");
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillStyle = "#FFFFFF";
      ctx.beginPath();
      ctx.arc(point[0], point[1],50,0,2*Math.PI);
      ctx.fill();
      console.log(point)
    };
  });
}
