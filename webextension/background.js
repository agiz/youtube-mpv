/*
Create all the context menu items.
*/
browser.contextMenus.create({
  id: "play-with-mpv",
  title: browser.i18n.getMessage("contextMenuItemPlayWithMpv"),
  contexts: ["all"]
});

browser.contextMenus.onClicked.addListener(function(info, tab) {
  switch (info.menuItemId) {
    case "play-with-mpv":
      var req = new XMLHttpRequest();
      if(req) {
        req.open('GET', 'http://localhost:9000/p?i='+tab.url, true);
        req.onreadystatechange =  function() {
          if (req.readyState == 4) {
            console.log("Response: " + req.responseText);
          }
        };
        req.send();
      }
      break;
    default:
      console.log("Unknown context menu option: " + info.menuItemId);
      break;
  }
});
