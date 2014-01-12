// Javascript File
// AUTHOR:   LaoSi
// FILE:     refresh.js
// 2013 @laosiaudi All rights reserved
// CREATED:  2014-01-10 20:46:44
// MODIFIED: 2014-01-10 21:25:49

function refresh(){
  var mainbody = $("questionbody");
  var match = $("search").value; 
  new Ajax.Request('/tag',{
    method :"post",
    parameters:{"search":match},
    onSuccess:function(data){
      var jsonlist = data.responseText.evalJSON(true);
      mainbody.innerHTML = "";
      jsonlist.each(function(commentdata){

        var title = commentdata["title"];
        var content = commentdata["content"];
        var date = commentdata["post_date"];
        var taglist = commentdata["tags"];
        var newdiv = document.createElement("div");
        var pp = document.createElement("p");
        pp.innerHTML = title;
        pp.addClassName("title");
        var pc = document.createElement("p");
        pc.innerHTML = content;
        pc.addClassName ("content");
        newdiv.appendChild(pp);
        newdiv.appendChild(pc);
        var pd = document.createElement("p");
        pd.innerHTML = date;
        pd.addClassName ("date");
        for (var i = 0;i <taglist.length;i ++){
          var pt = document.createElement("div");
          pt.innerHTML = taglist[i];
          pt.addClassName("tag");
          newdiv.appendChild(pt);
        }
        newdiv.appendChild(pd);
        newdiv.addClassName("question");
        var line = document.createElement("div");
        line.innerHTML = "<hr/>";
        line.addClassName("line");
        newdiv.appendChild(line);
        mainbody.appendChild(newdiv);
        
      });
    }
  }
  );
}
