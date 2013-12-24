// Javascript File
// AUTHOR:   apple
// FILE:     ajax.js
// 2013 @laosiaudi All rights reserved
// CREATED:  2013-12-23 18:22:48
// MODIFIED: 2013-12-24 11:32:23

window.onload = function(){
  $("commit").addEventListener("onclick",commit);
  
}

function commit(){
  var form = $("form");
  var input = form['comment_submit'];
  var data = $(input).getValue();
  new Ajax.Updater('form','/some',{
      method:'post',
      parameters:{'comment_submit':data},
      onSuccess:function (ajax){
        var form = $("form");
        form.reset();
      },
      insertion:'top'
  });
}
