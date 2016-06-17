// Copyright (c) 2015, 2016 Ziga Zupanec. All rights reserved.
// http://developer.chrome.com/extensions/samples.html#ea5374398da2255f743fd37964100fed
// Bug: Selectable + url triggers multiple menu choices.

var context, genericOnClick, i, len, ref, title, triggerUrl;

triggerUrl = "http://" + HOST + ":" + PORT + "/p?i=";

function play_video(url) {
  //var image = new Image();
  //image.src = url;

  var xhr = new XMLHttpRequest();
  xhr.open('GET', url, true);
  xhr.onreadystatechange = function() {
    console.log(xhr.readyState);
    console.log(xhr.status);
    if (xhr.readyState == 4) {
      // JSON.parse does not evaluate the attacker's scripts.
      //var resp = JSON.parse(xhr.responseText);
      console.log(1234);
      console.log(xhr.responseText);
      console.log(5678);
    }
  }
  xhr.send();
}

genericOnClick = function(info, tab) {
  var image, youtubeUrl;
  youtubeUrl = info.linkUrl || info.pageUrl;
  return play_video(triggerUrl + youtubeUrl);
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

// Set default values for local storage.
if(localStorage.getItem('linkmatches') === null) {
  localStorage.setItem('linksfoundindicator', 'true');
  localStorage.setItem('catchfrompage', 'true');
  localStorage.setItem('linkmatches', 'http[s]?:\\/\\/www\\.youtube\\.com\\/watch\\?v=.*~http[s]?:\\/\\/youtu\\.be/.*');
}

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'playVideo') {
    play_video(triggerUrl + request.url);
    sendResponse({});
  }
  else if (request.action == 'getStorageData') {
    sendResponse(localStorage);
  }
  else if (request.action == 'setStorageData') {
    for (x in request.data) {
      localStorage.setItem(x, request.data[x]);
    }
    sendResponse({});
  }
  else if (request.action == 'pageActionToggle') {
    // color the menubar icon
    chrome.pageAction.show(sender.tab.id);
    sendResponse({});
  }
});
