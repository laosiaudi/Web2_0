function initialize(){
  var list = $$(".boundary");
  for (var i = 0;i < list.length;i ++){
      if (list[i].className == "boundary example")
        continue;
      list[i].onmouseover = changecolor;
  }

  var endGame = $("end");
  endGame.onmouseover = end;

  var start = $("start");
  start.onclick = startGame;
}

function startGame(){
  var list = $$(".boundary");
  for (var i = 0;i < list.length;i ++){
    list[i].className = "boundary";
  }  
  hit = false;
  $("status").innerHTML = "restart!";
}
function end(){
  if (hit == false)
    $("status").innerHTML = "You win!";
}
function changecolor(){
  hit = true;
  var list = $$(".boundary");
  for (var i = 0;i < list.length;i ++){
    if (list[i].className == "boundary example")
      continue;
    list[i].addClassName("youlose");
  }
  $("status").innerHTML = "You lose!";
}

var hit = false;
window.onload = initialize;
