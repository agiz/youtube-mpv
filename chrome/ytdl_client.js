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
