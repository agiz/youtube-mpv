function loadGeneralSettings() {
  var e = document.querySelectorAll('#linksfoundindicator,#catchfrompage,#linkmatches')
  for (key in e) {
    getSetting(e[key]);
  }

  // load matches
  loadMatches();

  // set visibility
  flipVisibility('catchfrompage', 'linkmatches');
}

function flipVisibility(checkname, changename) {
  document.getElementById(changename).disabled = (document.getElementById(checkname).checked) ? false : true;
}

function setSetting(e, val) {
  localStorage[e.id] = (val === undefined) ? '' : val;
}

function getSetting(e) {
  if (e.type === 'text' || e.type === 'password') {
    document.getElementById(e.id).value = (localStorage[e.id] === undefined) ? '' : localStorage[e.id];
  }
  else if (e.type === 'checkbox') {
    document.getElementById(e.id).checked = (localStorage[e.id] === 'true') ? true : false;
  }
}

function saveMatches() {
  var opts = document.getElementById('linkmatches').getElementsByTagName('option');
  var destStr = ''; var i=0;
  for (key in opts)
    if (opts[key].text) {
      var sep = (i++ === 0) ? '' : '~';
      destStr += sep + opts[key].text;
    }
    localStorage['linkmatches'] = destStr;
}

function loadMatches() {
  var newSelEl = document.createElement('select');
  newSelEl.setAttribute('id', 'linkmatches');
  newSelEl.setAttribute('multiple', 'multiple');
  newSelEl.setAttribute('size', '5');
  if (localStorage['linkmatches'] !== '') {
    for (key in localStorage['linkmatches'].split('~')) {
      var newEl = document.createElement('option');
      newEl.text = localStorage['linkmatches'].split('~')[key];
      newSelEl.appendChild(newEl);
    }
    var selEl = document.getElementById('linkmatches');
    selEl.parentNode.appendChild(newSelEl);
    selEl.parentNode.removeChild(selEl);
  }
}

function addMatch() {
  var newMatch = prompt('Enter a partial string of a link that should be caught by the extension','');
  if (!newMatch) return;

  var newOpt = new Option(newMatch);
  document.getElementById('linkmatches').appendChild(newOpt);
  saveMatches();
}

function deleteMatches() {
  var list = document.getElementById('linkmatches');
  for (var i = list.length-1; i>=0; i--)
  if (list.options[i].selected) {
    list.removeChild(list.options[i]);
  }
  saveMatches();
}

Storage.prototype.setObject = function(key, val) {
  this.setItem(key, JSON.stringify(val));
}
Storage.prototype.getObject = function(key) {
  var value = this.getItem(key);
  return value && JSON.parse(value);
}

function registerGeneralSettingsEvents() {
  document.querySelector('#linksfoundindicator').onchange = function() {
    setSetting(this, (this.checked) ? 'true' : 'false');
  };

  document.querySelector('#catchfrompage').onchange = function() {
    setSetting(this, (this.checked) ? 'true' : 'false');
  };
  document.querySelector('#catchfrompage').onclick = function() {
    flipVisibility(this.id, 'linkmatches');
  };

  document.querySelector('#addfilterbtn').onclick = function() {
    addMatch();
  };

  document.querySelector('#delfilterbtn').onclick = function() {
    deleteMatches();
  };
}

registerGeneralSettingsEvents();
loadGeneralSettings();
