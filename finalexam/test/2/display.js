
var t;
var flag;
window.onload = function(){
  var startbutton = $("start");
  startbutton.onclick = play;
  var stopbutton = $("stop");
  stopbutton.onclick = stop;
  flag = true;
}

function play(){
  $("stop").disabled = "";
  $("start").disabled = "disabled";
  t = setInterval("change()",1000);
}
function change(){
  var content = $("content");
  var size = parseInt(content.style.fontSize);
  if (size < 500 && flag == true)
    size += 50;
  else{
    flag = false;
    if (size > 50)
      size -= 50;
    else
      flag = true;
  }
  var newsize = size.toString()+"px";
  content.style.fontSize = newsize;

}

function stop(){
  $("stop").disabled = "disabled";
  $("start").disabled = "";
  clearInterval(t);
}
