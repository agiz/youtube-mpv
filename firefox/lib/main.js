exports.main = function() {
  var HOST, PORT, config, data, prevDate, prevUrl, self;
  self = require('sdk/self');
  data = self.data;
  config = data.load('ytdl_config');
  HOST = /HOST\ \=\ \'(.*?)\'/.exec(config)[1];
  PORT = /PORT\ \=\ ([0-9]+)/.exec(config)[1];
  prevUrl = null;
  prevDate = 0;
  return require('sdk/context-menu').Item({
    label: 'Play with mpv',
    context: require('sdk/context-menu').SelectorContext('a[href]'),
    contentScriptFile: data.url('trigger.js'),
    image: data.url('icons/mpv-logo-16.png'),
    onMessage: function(arg) {
      var date, req, url;
      url = arg[0], date = arg[1];
      if ((prevUrl === url) && (date - prevDate) < 200) {
        return;
      }
      prevUrl = url;
      prevDate = date;
      req = require('sdk/net/xhr').XMLHttpRequest();
      req.open('get', "http://" + HOST + ":" + PORT + "/p?i=" + url);
      return req.send();
    }
  });
};
