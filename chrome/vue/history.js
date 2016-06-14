var vm;
var doc;
var mod;
Vue.config.debug = true;

var thumbnail = Vue.extend({
    props: ['video', 'check'],
    template: thumbnail_template
});

var detail = Vue.extend({
    props: ['video', 'check'],
    template: detail_template
});

window.onload = function () {

vm = new Vue({
    el: '#history',
    data: {
        api: 'http://' + HOST + ':' + 'PORT' + '/?g=all',
        videos: [],
        currentTab: 'detail',
        searchQuery: '',
        sortKey: '',
        sortOrders: {},
        columns: ['time', 'title', 'src'],
        checked: []
    },

    ready() {
        this.columns.forEach((key) => {
            this.sortOrders[key] = 1;
        });
        this.getVideos();
    },

    components: {
        detail,
        thumbnail
    },

    methods: {

        sortBy: function (key) {
          this.sortKey = key
          this.sortOrders[key] = this.sortOrders[key] * -1
        },

        vid2Obj(id, time, src, short_url, long_url, title, description, thumb, dim) {
            return {
                id, time, src, short_url, long_url, title, description, thumb, dim
            };
        },

        getVideos() {
            var arr = [[3, 1465857739898.306, "youtube", "jU7GNQaOBhc", "https://www.youtube.com/watch?v=jU7GNQaOBhc", "MPP - Ps 139", "", "https://i.ytimg.com/vi/jU7GNQaOBhc/hqdefault.jpg", 182],
            [2, 1465855254479.9768, "youtube", "pidW3I9GQa8", "https://www.youtube.com/watch?v=pidW3I9GQa8", "Pi", "https://i.ytimg.com/vi/pidW3I9GQa8/hqdefault.jpg", 557],
            [1, 1465854452886.2075, "youtube", "scWdXPibXZg", "https://www.youtube.com/watch?v=scWdXPibXZg", "", "https://i.ytimg.com/vi/scWdXPibXZg/hqdefault.jpg", 448]]
            for (a of arr) {
                var video = this.vid2Obj(a[0], a[1], a[2], a[3], a[4], a[5], a[6], a[7])

                this.videos.push(video);
            }
        },

        clearAll() {
            this.videos = this.videos.filter((x, i) => {
                return i == null;
            });
        },

        clearChecked() {
            this.videos = this.videos.filter((item) => {
                return this.checked.indexOf(item.id.toString()) == -1;
            })
        },

        setTab(tab) {
            this.currentTab = tab;
        },

        httpGetAsync(theUrl, callback) {
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.onreadystatechange = function() {
                if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
                    callback(xmlHttp.responseText);
            }
            xmlHttp.open("GET", theUrl, true); // true for asynchronous
            xmlHttp.send(null);
        },

        humanDate(d) {
          return new Date(d).toLocaleString();
        }

    }
});

}
