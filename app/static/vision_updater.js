// var canvas = document.getElementById("myCanvas");
// var ctx = canvas.getContext("2d");
// ctx.fillStyle = "#FFFFFF";
// ctx.fillRect(10,10,1000,500);

// setTimeout(update_screen, 3000);
//setInterval(update_screen, 33);
// setInterval(update_screen, 3000);

function update_screen() {
  $.getJSON($SCRIPT_ROOT + '/get_screen', {
  }, function(data) {
    var corners = data.result;
    var canvas = document.getElementById("myCanvas");
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.fillStyle = "#FFFFFF";
    ctx.fillRect(corners[0],corners[1],corners[2],corners[3]);
    console.log(corners);
  });
}
