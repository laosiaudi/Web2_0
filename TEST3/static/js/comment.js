// Javascript File
// AUTHOR:   apple
// FILE:     comment.js
// 2013 @laosiaudi All rights reserved
// CREATED:  2013-12-26 14:52:36
// MODIFIED: 2013-12-28 11:55:06


function commentshow(element){
  var bigdiv = element.parentNode.parentNode;
  element = element.parentNode.parentNode.cleanWhitespace();
  element = element.firstChild;
  var name = element.firstChild.innerHTML;
  element = element.nextSibling;
  var content = element.innerHTML;
  new Ajax.Request('/comment',{
    method:"get",
    parameters: {"username":name,
                "content":content},
    onSuccess:function(data){
      var e1 = bigdiv.lastChild;
      e1.style.display = "block";
      var e2 = e1.previousSibling
      e2.style.display = "block";
      var jsonlist = data.responseText.evalJSON(true);
      jsonlist.each(function(commentdata){
        var date = commentdata["comment_date"];
        var name = commentdata["comment_by"];
        var content = commentdata["comment_content"];
        var new_div = document.createElement('div'); 
        Element.extend(new_div);
        new_div.addClassName('comment');
        var new_name = document.createElement('p');
        new_name.update(name);
        new_div.appendChild(new_name);
        var new_time = document.createElement('span');
        new_time.addClassName('time');
        new_time.update(date);
        new_name.appendChild(new_time);
        var new_p = document.createElement('p');
        new_p.update(content);
        new_div.appendChild(new_p);
        

        bigdiv.appendChild(new_div);

      }
      );
    }
  });
}
function submitcomment(element){
    var ee = element.previousSibling;
    var el = element.nextSibling;
    var text = ee.value;
    var bigdiv = ee.parentNode.cleanWhitespace();
    var usr  = bigdiv.firstChild.firstChild.innerHTML;
    var content = bigdiv.firstChild.nextSibling.innerHTML
    new Ajax.Request('/commit',{
      method:"post",
      parameters:{"newcomment":text,
                  "username":usr,
                  "content":content},
      onSuccess:function(data){
        var new_div = document.createElement('div'); 
        Element.extend(new_div);
        new_div.addClassName('comment');
        var new_name = document.createElement('p');
        var newp = document.createElement('span');
        newp.addClassName('name');
        newp.update(usr);
        new_name.appendChild(newp);
        new_div.appendChild(new_name);
        var new_time = document.createElement('span');
        new_time.addClassName('time');
        //var timeline = new Date().getMonth() +' ' +  new Date().getDay() +' ' +  new Date().getDate()
        var timeline = new Date().toLocaleString();
        new_time.update(timeline);
        new_name.appendChild(new_time);
        var new_p = document.createElement('p');
        new_p.update(text);
        new_div.appendChild(new_p);
        if (element.nextSibling == null) 
          bigdiv.appendChild(new_div);
        else
          element.insertBefore(element.nextSibling);
      }
    });

}
