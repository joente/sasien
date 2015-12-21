
'use strict';

(function () {
    var sasien = {};

    sasien.srepeat = function (s, num) {
        return new Array(num + 1).join(s);
    };

    sasien.zfill = function (s, size) {
        return sasien.srepeat('0', size - s.length) + s;
    };

    sasien.shuffle = function (o) {
        for (var j, x, i = o.length; i; j = Math.floor(Math.random() * i), x = o[--i], o[i] = o[j], o[j] = x);
        return o;
    };

    sasien.range = function (n) {
        var result = [];
        for (var i = 0; i < n; i++) {
            result.push(i);
        }
        return result;
    };

    sasien.take = function (list, n) {
        var result = [];
        for (var i = 0; i < n; i++) {
            var item = list.pop();
            result.push(item);
            list.unshift(item);
        }
        return result;
    };

    sasien.repeat = function (value, n) {
        var result = [];
        for (var i = 0; i < n; i++) {
            result.push((typeof value === 'function') ? value() : value);
        }
        return result;
    };

    sasien.getImgSrc = function (which, categoryName, id) {
        return '/img/{0}/{1}/{2}'.format(which, categoryName, sasien.zfill('{0}.jpg'.format(id), 12));
    };

    sasien.getImgId = function (fn) {
        return Number(fn.substr(-12,8));
    };

    sasien.clickImage = function (id) {
        var portfolio = window.portfolio,
            idx, len, i, l, category, image;

        for (idx=0, len=portfolio.length; idx < len; idx++) {
            category = portfolio[idx];
            for (i=0, l=category.images.length; i < l; i++) {
                image = category.images[i];
                if (image.id === id) {
                    window.location.hash = 'portfolio/{0}/{1}'.format(category.name, id);
                    return;
                }
            }
        }
    };


    window.sasien = sasien;
})();
