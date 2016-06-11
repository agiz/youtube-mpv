function secondsToHms(d) {
  d = Number(d);
  if (d === -1) {
    return '?';
  }
  var h = Math.floor(d / 3600);
  var m = Math.floor(d % 3600 / 60);
  var s = Math.floor(d % 3600 % 60);
  return ((h > 0 ? h + ":" + (m < 10 ? "0" : "") : "") + m + ":" + (s < 10 ? "0" : "") + s);
}

function pad(n) {
  return (n < 10) ? ("0" + n) : n;
}

function append_el(el, i, download_time, video_url, title, extractor, duration, thumbnail) {
  var str = title;

  var li = document.createElement('li');
  li.className = 'entry';

  var div_container = document.createElement('div');
  div_container.className = 'entry-box-container';

  var div_box = document.createElement('div');
  div_box.className = 'entry-box';
  div_box.setAttribute('for', 'checkbox-' + i);

  var input = document.createElement('input');
  input.type = 'checkbox';
  input.id = 'checkbox-' + i;
  input.className = 'entry-box';
  input.setAttribute('aria-label', str);
  input.setAttribute('focus-type', 'checkbox');
  input.tabIndex = -1;

  var span = document.createElement('span');
  span.className = 'time';
  var t = document.createTextNode(download_time);
  span.appendChild(t);

  var button = document.createElement("button");
  button.className = 'bookmark-section custom-appearance';

  var div_visit = document.createElement('div');
  div_visit.className = 'visit-entry';
  div_visit.setAttribute('style', 'background-image: -webkit-image-set(url("' + thumbnail + '") 1x, url("' + thumbnail + '") 2x)');

  var div_title = document.createElement('div');
  div_title.className = 'title';

  var a_href = document.createElement('a');
  a_href.href = video_url;
  a_href.id = 'id-' + i;
  a_href.target = '_top';
  a_href.title = str;
  a_href.setAttribute('focus-type', 'title');
  a_href.tabIndex = -1;
  a_href.textContent = '[' + secondsToHms(duration) + '] ' + str;

  var div_domain = document.createElement('div');
  div_domain.className = 'domain';
  div_domain.textContent = extractor;

  var button_dd = document.createElement("button");
  button_dd.className = 'drop-down custom-appearance menu-button';
  button_dd.value = 'Open action menu';
  button_dd.title = 'Actions';
  button_dd.setAttribute('aria-haspopup', 'true');
  button_dd.setAttribute('focus-type', 'menu');
  a_href.tabIndex = -1;

  div_title.appendChild(a_href);
  div_visit.appendChild(div_title);
  div_visit.appendChild(div_domain);

  div_box.appendChild(input);
  div_box.appendChild(span);
  div_box.appendChild(button);
  div_box.appendChild(div_visit);
  div_box.appendChild(button_dd);

  div_container.appendChild(div_box);

  li.appendChild(div_container);

  el.appendChild(li);
}

var format = [];

for (var i in format_arr) {
  format[format_arr[i][0] + ''] = format_arr[i][1];
}

var vf = [];
for (var i in video_format_arr) {
  var vfvid = video_format_arr[i][0] + '';
  var vftid = video_format_arr[i][1] + '';

  if (!(vfvid in vf)) {
    vf[vfvid] = [];
  }

  vf[vfvid].push(format[vftid]);
}

if (video_arr.length > 0) {
  date_separator = new Date(video_arr[0][1]);
  date_separator = date_separator.getDate() + 1;

  var rd = document.getElementById('results-display');

  for (var i in video_arr) {
    var tmp_d = new Date(video_arr[i][1]);

    if (tmp_d.getDate() < date_separator) {
      date_separator = tmp_d.getDate();

      var h3 = document.createElement('h3');
      h3.className = 'day';
      h3.textContent = tmp_d.toDateString();

      var ol = document.createElement('ol');
      ol.className = 'day-results';

      rd.appendChild(h3);
      rd.appendChild(ol);
    }

    tmp_d = pad(tmp_d.getHours()) + ':' + pad(tmp_d.getMinutes());
    append_el(ol, i, tmp_d, video_arr[i][4], video_arr[i][5], video_arr[i][2], video_arr[i][8], video_arr[i][7]);
  }
}
