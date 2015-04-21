// Copyright (c) 2015 Ziga Zupanec. All rights reserved.
// http://developer.chrome.com/extensions/samples.html#ea5374398da2255f743fd37964100fed
// Bug: Selectable + url triggers multiple menu choices.

var trigger_url = 'http://' + HOST + ':' + PORT + '/p?i=';

function genericOnClick(info, tab) {
  yt_url = info.linkUrl || info.pageUrl;
  var image = new Image();
  image.src = trigger_url + yt_url;
}

var contexts = ['page', 'link'];

for (var i = 0; i < contexts.length; i++) {
  var context = contexts[i];
  var title = 'Play with mpv';
  var id = chrome.contextMenus.create({
    'title': title,
    'contexts': [context],
    'onclick': genericOnClick
  });
}
