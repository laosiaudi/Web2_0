// Javascript File
// AUTHOR:   apple
// FILE:     comment.js
// 2013 @laosiaudi All rights reserved
// CREATED:  2013-12-26 14:52:36
// MODIFIED: 2013-12-26 16:09:52

window.onload = function(){
  $("getCommentBtn").addEventListener("click",commentshow);
}

function commentshow(){
  new Ajax.Request('/comment',{
    method:"get",
    onSuccess:function(data){
      var butt = $("getCommentBtn");
      butt.parentNode.removeChild(butt);
      var jsonlist = data.responseText.evalJSON(true);
      jsonlist.each(function(commentdata){

        name = commentdata["name"];
        time = commentdata["time"];
        content = commentdata["content"];
        var new_div = document.createElement('div'); 
        Element.extend(new_div);
        new_div.addClassName('comment').show();
        var new_name = document.createElement('p');
        new_name.addClassName('name');
        new_name.update(name);
        new_div.appendChild(new_name);
        var new_time = document.createElement('span');
        new_time.addClassName('time');
        new_time.update(time);
        new_name.appendChild(new_time);
        var new_p = document.createElement('p');
        new_p.update(content);
        new_div.appendChild(new_p);
        $("commentsList").appendChild(new_div);

      }
      );
    }
  });
}

function sho(){
  alert("hii");
}
