var decode = function(t, e) {
        "use strict";
        function i() {
            return window.wbopen && ~(window.open + "").indexOf("wbopen")
        }
        function a(t) {
            if (!t || t.length % 4 == 1)
                return !1;
            for (var e, i, o = 0, a = 0, s = ""; i = t.charAt(a++); )
                i = r.indexOf(i),
                ~i && (e = o % 4 ? 64 * e + i : i,
                o++ % 4) && (s += String.fromCharCode(255 & e >> (-2 * o & 6)));
            return s
        }
        function s(t, e) {
            var i = t.length
              , o = [];
            if (i) {
                var a = i;
                for (e = Math.abs(e); a--; )
                    e = (i * (a + 1) ^ e + a) % i,
                    o[a] = e
            }
            return o
        }
        var r = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMN0PQRSTUVWXYZO123456789+/="
          , l = {
            v: function(t) {
                return t.split("").reverse().join("")
            },
            r: function(t, e) {
                t = t.split("");
                for (var i, o = r + r, a = t.length; a--; )
                    i = o.indexOf(t[a]),
                    ~i && (t[a] = o.substr(i - e, 1));
                return t.join("")
            },
            s: function(t, e) {
                var i = t.length;
                if (i) {
                    var o = s(t, e)
                      , a = 0;
                    for (t = t.split(""); ++a < i; )
                        t[a] = t.splice(o[i - 1 - a], 1, t[a])[0];
                    t = t.join("")
                }
                return t
            },
            i: function(t, e) {
                return l.s(t, e ^ vk.id)
            },
            x: function(t, e) {
                var i = [];
                return e = e.charCodeAt(0),
                each(t.split(""), function(t, o) {
                    i.push(String.fromCharCode(o.charCodeAt(0) ^ e))
                }),
                i.join("")
            }
        }
        return function o(t) {
            if (!i() && ~t.indexOf("audio_api_unavailable")) {
                var e = t.split("?extra=")[1].split("#")
                  , o = "" === e[1] ? "" : a(e[1]);
                if (e = a(e[0]),
                "string" != typeof o || !e)
                    return t;
                o = o ? o.split(String.fromCharCode(9)) : [];
                for (var s, r, n = o.length; n--; ) {
                    if (r = o[n].split(String.fromCharCode(11)),
                    s = r.splice(0, 1, e)[0],
                    !l[s])
                        return t;
                    e = l[s].apply(null, r)
                }
                if (e && "http" === e.substr(0, 4))
                    return e
            }
            return t
        }(t)
    };

// replace jQuery to $
var musicIds = jQuery("body").find(".audio_row").map(function(index) {
    return jQuery(this).attr('data-full-id');
}).toArray();

var musicPosts = []

var vkGetUrls = function(ids) {
    ids = ids.join("%2C")
    
    var vkSender = new XMLHttpRequest;
    vkSender.open("POST", "https://vk.com/al_audio.php", false);
    vkSender.withCredentials = !0;
    vkSender.setRequestHeader("content-type", "application/x-www-form-urlencoded");
    vkSender.send("act=reload_audio&al=1&ids="+ids);
    if (vkSender.readyState === 4 && vkSender.status === 200) {
        var resp = new RegExp("<!json>(.*)<!><").exec(vkSender.responseText);
        if (resp === null) {
            console.log("Fail", vkSender.responseText);
        } else {
            var music = JSON.parse(resp[1]);
            music = music.map(function(a) {
                if (40 <= a[5] && a[5] < 300) { // download only songs that last not more than 5 minutes
                    var info = [a[1]+'_'+a[0], a[4], a[3], decode(a[2])]; // id, artist, title, url
                    return info.join('\t');
                }
            })
            musicPosts = musicPosts.concat(music);
        }
    }
}

var batchSize = 10;
for (var i = 0; i < musicIds.length; i += batchSize) {
    var subSongs = musicIds.slice(i, i + batchSize);
    vkGetUrls(subSongs);
}
