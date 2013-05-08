// Copyright (c) 2013 Ziga Zupanec. All rights reserved.
// http://developer.chrome.com/extensions/samples.html#ea5374398da2255f743fd37964100fed
// Bug: Selectable + url triggers multiple menu choices.

var trigger_url = 'http://127.0.0.1:9000/p?i=';

function genericOnClick(info, tab) {
  yt_url = info.linkUrl || info.pageUrl;
  console.log(yt_url);
  yt_url = yt_url.replace(/^http:\/\//i, 'https://');
  var image = new Image();
  image.src = trigger_url + yt_url;
}

//var contexts = ["page", "selection", "link", "editable", "image", "video", "audio"];
var contexts = ["page", "link"];

for (var i = 0; i < contexts.length; i++) {
  var context = contexts[i];
  var title = "Play with mplayer";
  var id = chrome.contextMenus.create({
    "title": title,
    "contexts": [context],
    "onclick": genericOnClick
  });
}
