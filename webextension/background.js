/*
Create all the context menu items.
*/
browser.contextMenus.create({
  id: "play-page-with-mpv",
  title: browser.i18n.getMessage("contextMenuItemPlayPageWithMpv"),
  contexts: ["page"]
});

browser.contextMenus.create({
  id: "play-link-with-mpv",
  title: browser.i18n.getMessage("contextMenuItemPlayLinkWithMpv"),
  contexts: ["link"]
});

browser.contextMenus.onClicked.addListener(function(info, tab) {
  var urlToPlay = null;
  switch (info.menuItemId) {
    case "play-page-with-mpv":
      urlToPlay = tab.url;
      break;
    case "play-link-with-mpv":
      urlToPlay = info.linkUrl;
      break;
    default:
      console.log("Unknown context menu option: " + info.menuItemId);
      break;
  }

  if (urlToPlay) {
    var req = new XMLHttpRequest();
    if(req) {
      req.open('GET', 'http://localhost:9000/p?i='+urlToPlay, true);
      req.onreadystatechange =  function() {
        if (req.readyState == 4) {
          console.log("Response: " + req.responseText);
        }
      };
      req.send();
    }
  }
});
