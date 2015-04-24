self.on('context', function(node) {
  if (node.href) {
    self.on('click', function(node, data) {
      return self.postMessage([node.href, Date.now()]);
    });
    return true;
  }
});
