var length = 4;
var tileIndex = [];
var space = 15;
window.onload = function(){
	initialize();
	var change = $("shufflebutton");
  change.onclick = randomchange;

};

function initialize(){
  tileIndex = [];
  length = 4;
  space = 15;
	var puzzlearea = $("puzzlearea");
	var component = puzzlearea.getElementsByTagName("div");
  for (var i = 0;i < component.length;i ++){
		 component[i].className = "puzzlepiece";
     setLocation(component[i],i);		
     setBackground(component[i],i);
     setId(component[i],i);
     tileIndex[i] = i;
     component[i].addEventListener('click',Move);
     component[i].onmouseover = MouseOver;
     component[i].onmouseout = MouseOut;
	}
  tileIndex[component.length] = 15;
}
function changepic(){
  var pic = $("radioform").getInputs("radio","pictype").find(function(radio){return radio.checked;}).value; 
  var classList = $$(".puzzlepiece");
  for (var i = 0;i < classList.length;i ++){
    if (pic == "pic1")
      classList[i].style.backgroundImage = "url('./images/pic1.jpg')";
    else
      classList[i].style.backgroundImage = "url('./images/pic2.jpg')";
  }
  initialize();
}
function setId(element,index){
  element.id = index;
}

function Move(){
  var tempindex = tileIndex[getId(this)];
  var next = canMove(tempindex);
  if (next != -1){
      space = tempindex;
      tileIndex[getId(this)] = next;
      setLocation(this,next);
  }
}
function MouseOver(){
   var tempindex = tileIndex[getId(this)];
   if (canMove(tempindex) != -1){
      this.addClassName("movablepiece");  
   }
}

function MouseOut(){
    this.removeClassName("movablepiece");
}
function setLocation(element,index){
  var i = Math.floor(index / length), j = index % length;
  var x = i * (400 / length), y = j * (400 / length);
  element.style.top = x + "px";
  element.style.left = y + "px";
}
function setBackground(element,index){
  var i = Math.floor(index / length), j = index % length;
  var x = -i * (400 / length) + "px", y = -j * (400 / length) + "px";
  element.style.backgroundPosition = y + " " + x;

}

function getId(element){
  return parseInt(element.id);
}
function canMove(index){
  var variable = [];
  var count = 0;
  var dis = [1,-1,4,-4];
  for (var i = 0;i < 4;i ++){
    var temp = index + dis[i];
    if (temp >= 0 && temp <= 15 && temp == space){
       return temp;
    }
  }
  return -1;
}
var loca = [];
var arrayLength = 0;
function check(temp){
    for (var i = 0;i < arrayLength;i ++){
        if (loca[i] == temp)
          return false;
    }
    return true;
}
/*
function randomchange(){
  loca = [];
  arrayLength = 0;
  for (var i = 0;i < 16;){
    var temp = Math.floor(Math.random()*16);
    if (check(temp)){
      loca[arrayLength] = temp;
      arrayLength += 1;
      i ++;
    }
  }
  var tile = $$(".puzzlepiece");
  for (var i= 0;i < tile.length;i ++){
      setLocation(tile[i],loca[i]);
      tileIndex[getId(tile[i])] = loca[i];
  }
  space = loca[15];
}*/

function randomchange(){
  var time = 100;
  for (var i = 1;i <= time;i ++){
    var tile = $$(".puzzlepiece");  
    for (var j = 0;j < tile.length;j ++){
      var tempindex = tileIndex[getId(tile[j])];
      var temp = canMove(tempindex);
      if (temp != -1){
        setLocation(tile[j],temp);
        space = tileIndex[getId(tile[j]) ];
        tileIndex[getId(tile[j])] = temp;
      }
    }
  }

}
