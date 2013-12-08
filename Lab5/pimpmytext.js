function onButtonClicked(){
  alert("Hello World!");
  $("input").style.color="red";
  time = setInterval("increase()",500);
}

var size = "10pt";
var time;
function increase(){
    $("input").style.fontSize = size;
    size = parseInt(size);
    size = (size + 2) + "pt";
}

function onCheckBoxClicked(){
   if ($("checkbox").checked == true){
       $("body").style.background = "url(http://www.cs.washington.edu/education/courses/190m/09sp/labs/5-pimpify/hundred-dollar-bill.jpg)";
       $("input").style.fontWeight = "bold";
       $("input").style.textDecoraiton = "underline";
       $("input").style.color = "green";
   }
   else{
       $("input").style.fontWeight = "normal";
       $("input").style.background = "none";
       $("input").style.color = "none";
       $("input").style.textDecoraiton = "none";
   }
}

function Snoopify(){
   var str = $("input").value.toUpperCase();
   var strAfterSplit = str.split(".");
   strAfterSplit = strAfterSplit.join("-izzle.");
   $("input").value = strAfterSplit;
}

function Mal(){
   //var words = new Array();
   var words = $("input").value.match(/[A-Za-z0-9]+/g);
   var origin = $("input").value;
   var i;
   for(i = 0;i < words.length;i ++){
       if (words[i].length >= 5){
         var temp = words[i];
         var regs = new RegExp(temp,"g");
         origin = origin.replace(regs,"Malkovich");
       }
   }
   $("input").value = origin;

}


function isCon( cr){
  if(!(cr == 'a' || cr == 'e' || cr == 'i' || cr == 'o' || cr == 'u')){
    return true;
  }
}
function Igpay(){
   var words = $("input").value.match(/[A-Za-z0-9]+/g);
   var origin = $("input").value;
   var i;
   for(i = 0;i < words.length;i ++){
       if (!/^[a-zA-Z]+$/.test(words[0].charAt(0)))
          continue;
       if (isCon(words[i].charAt(0))){
         var temp = words[i].substr(1);
         temp = temp + words[i].charAt(0) + "-ay";
         var regs = new RegExp(words[i],"g");
         origin = origin.replace(regs,temp);
       }
       else{
         var temp = words[i] + "-ay";
         var regs = new RegExp(words[i],"g")
         origin = origin.replace(regs,temp);
       }
   }
   $("input").value = origin;
}
