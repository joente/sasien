'use strict';

(function ($, sasien) {

    sasien.getWallImages = function (portfolio) {
        var  wallImages = [];
        $.each(portfolio, function (idx, category) {
            $.each(category.images, function (idx, image) {
                if (image.wall) {
                    wallImages.push(sasien.getImgSrc('wall', category.name, image.id));
                }
            });
        });
        return wallImages;
    };

    sasien.wall = function (container, images, settings) {
        var defaults = {
            nWalls: 9,
            nSwitch: 2,
            interval: 5000,
            startAfter: 1500,
            speed: 600
        };

        var config = $.extend({}, defaults, settings);

        var switchList = sasien.shuffle(sasien.range(config.nWalls)),
            whichList = sasien.repeat(true, config.nWalls),
            initialPhotos,
            i;

        var content = [];

        for (i=0; i < config.nWalls; i++) {
            content.push([
                '<div id="wall-{0}" class="col-xs-6 col-sm-4">'.format(i),
                    '<span class="wall-img-0"></span>',
                    '<span class="wall-img-1"></span>',
                '</div>'
            ].join(''));
        }

        container.addClass('row').html(content.join(''));

        images = sasien.shuffle(images);

        var clickWall = function () {
            var $this = $(this);
            var id = $this.data('id');
            $this.parent().css({cursor: 'pointer'}).click(function () {
                sasien.clickImage(id);
            });
        };

        initialPhotos = sasien.take(images, config.nWalls);

        for (i = 0; i < config.nWalls; i++) {
            $('#wall-{0} .wall-img-{1}'.format(i, Number(whichList[i])))
                .html('<img src="' + initialPhotos[i] + '" />')
                .data('id', sasien.getImgId(initialPhotos[i]))
                .hide(0, clickWall)
                .fadeIn(config.speed);
        }
        var intervalFunc = function () {
            var switchWalls = sasien.take(switchList, config.nSwitch),
                switchPhotos = sasien.take(images, config.nSwitch);
            for (var i = 0; i < config.nSwitch; i++) {
                var wall = switchWalls[i];
                $('#wall-{0}'.format(wall))
                    .css({cursor: 'default'})
                    .off('click');
                $('#wall-{0} .wall-img-{1}'.format(wall, Number(!whichList[wall])))
                    .css({opacity: 0})
                    .html('<img src="' + switchPhotos[i] + '" />')
                    .data('id', sasien.getImgId(switchPhotos[i]))
                    .animate({opacity: 1}, config.speed, 'linear', clickWall);
                $('#wall-{0} .wall-img-{1}'.format(wall, Number(whichList[wall])))
                    .animate({opacity: 0}, config.speed, 'linear');
                whichList[wall] = !whichList[wall];
            }
        };
        var interval = {
            init: function () {
                var self = this;
                this.timeout = setTimeout(function () {
                    intervalFunc();
                    self.start();
                }, config.startAfter);
            },
            start: function () {
                this.interval = setInterval(intervalFunc, config.interval);
            },
            stop: function () {
                clearInterval(this.interval);
                clearTimeout(this.timeout);
            }
        };
        interval.init();
        return interval;
    };
})(window.jQuery, window.sasien);