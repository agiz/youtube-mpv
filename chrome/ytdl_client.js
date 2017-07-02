// Copyright (c) 2015 Ziga Zupanec. All rights reserved.
// http://developer.chrome.com/extensions/samples.html#ea5374398da2255f743fd37964100fed
// Bug: Selectable + url triggers multiple menu choices.

var context, genericOnClick, i, len, ref, title, triggerUrl;

triggerUrl = "http://" + HOST + ":" + PORT + "/p?i=";

genericOnClick = function(info, tab) {
  var image, youtubeUrl;
  youtubeUrl = escape(info.linkUrl || info.pageUrl);
  image = new Image();
  return image.src = triggerUrl + youtubeUrl;
};

title = 'Play with mpv';

ref = ['page', 'link'];
for (i = 0, len = ref.length; i < len; i++) {
  context = ref[i];
  chrome.contextMenus.create({
    'title': title,
    'contexts': [context],
    'onclick': genericOnClick
  });
}


function getCurrentTabUrl(callback) {
  var queryInfo = {
    active: true,
    currentWindow: true
  };

  chrome.tabs.query(queryInfo, function(tabs) {
    var tab = tabs[0];
    var url = tab.url;
    callback(url);
  });
}


chrome.commands.onCommand.addListener(function (command) {
  if (command === "play") {
    getCurrentTabUrl(function (url) {
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open( "GET", triggerUrl + escape(url),false);
      xmlHttp.send(null);
    });
  }
});
