var type;
var size = [];
size["Small"] = "7pt";
size["Medium"] = "12pt";
size["Large"] = "24pt";
var fontsize;
var animations;
var t;
var index = 0;
var speed = 200;
function start(){
    type = $("animation").value;
    var typevalue = $("radioform").getInputs('radio','size').find(function(radio){return radio.checked;}).value;
    fontsize = size[typevalue]; 
    if (type != "Custom")
      animations = ANIMATIONS[type].split("\n");
    else{
      //seems just for IE file seems too fuzzy .....to be done later
      var fso = new ActiveXObject("Scripting.FileSystemObject");
      var f = fso.OpenTextFile("asciimation.txt",1);
      var s = "";
      while (!f.AtEndOfStream)
        s += f.ReadLine() + "\n";
      animations = s.split("\n");
    }
    t = setInterval("play()",speed);
}
function Turbo(){
  if (speed == 200)
     speed = 50;
   else
     speed = 200;
   clearInterval(t);
   t = setInterval("play()",speed);
}
function play(){
  var text = "";
  if (animations.length != 0)
    index = index%(animations.length);
  else
    index = 0;

  if (index == 0){
    text = "";
  }
  $("displayarea").style.fontSize = fontsize;
    
  while (animations[index] != "=====" && index < animations.length){
    text = text + animations[index] + "\n";
    index ++;
  }
  $("displayarea").value = text;
  index += 1;

}
function stop(){
  
  clearInterval(t);
  if (animations.length == 0)
    $("displayarea").value = "";
  else
    $("displayarea").value = animations[index%animations.length];
}

function changesize(){
  var typevalue = $("radioform").getInputs('radio','size').find(function(radio){return radio.checked;}).value;
  fontsize = size[typevalue]; 
  //return fontsize;
}

function makeString(text) {
    var lines = text.split("\n");

    // trim any trailing blank lines
    while (lines.length > 0 && lines[lines.length - 1] == "") {
        lines.pop();
    }
    
    var newText = "";
    for (var i = 0; i < lines.length; i++) {
        lines[i] = lines[i].replace(/\\/gi, "\\\\");
        lines[i] = lines[i].replace(/\"/gi, "\\\"");
        lines[i] = lines[i].replace(/\'/gi, "\\\'");
        // lines[i] = lines[i].replace(/\&/gi, "\\&");
        lines[i] = lines[i].replace(/\t/gi, "\\t");
        lines[i] = "\"" + lines[i] + "\\n\"";
    }
    return lines.join(" + \n") + ";";
}
