'use strict';

// For production we include this file in app.min.js

(function (routie, $, sasien) {

    var interval;

    $.getJSON('/portfolio.json', function (portfolio) {
        window.portfolio = portfolio;

        routie({
            '': renderHome,
            'home': renderHome,
            'portfolio/:category': renderPortfolio,
            'portfolio/:category/:imageId': renderImage,
            'about/:language': renderAbout,
            '*': function () { render('#page-not-found-view'); }
        });

    }).fail(function (e) {
        window.console.error('error in json data', e.responseText);
    });


    function render (view, target) {
        if (interval) { interval.stop(); }
        var $view = $(view);
        if ($view.length) {
            $('#view').html($view.html());
        }
        target = target || view;
        $('.navbar-nav li').removeClass('active');
        $('.navbar-nav li[data-target="' + target + '"]').addClass('active');
    }

    function renderHome () {
        render('#home-view');

        var settings = {
            mobile: {
                nWalls: 6,
                nSwitch: 2,
            },
            desktop: {
                nWalls: 9,
                nSwitch: 2,
            }
        };

        var current = ($(window).width() < 768) ? settings.mobile : settings.desktop,
            wall = $('#wall');

        interval = sasien.wall(wall, sasien.getWallImages(window.portfolio), current);

        $(window).off('resize').resize(function () {
            var n = ($(window).width() < 768) ? settings.mobile : settings.desktop;
            if (n !== current) {
                current = n;
                if (interval) { interval.stop(); }
                interval = sasien.wall(wall, sasien.getWallImages(window.portfolio), current);
            }
        });
    }

    function renderPortfolio (category, callback) {
        var gallery = $('#portfolio .gallery:first').first();

        if (gallery.data('category') === category) {
            return;
        }

        render('#portfolio-view', category);

        var settings = {
            mobile: {
                nColumns: 2,
            },
            desktop: {
                nColumns: 3,
            }
        };

        var current = ($(window).width() < 768) ? settings.mobile : settings.desktop;

        gallery = $('#portfolio .gallery').first();

        gallery.data('category', category);

        sasien.gallery(gallery, category, current, function () {

            $(window).off('resize').resize(function () {
                var n = ($(window).width() < 768) ? settings.mobile : settings.desktop;
                if (n !== current) {
                    current = n;
                    sasien.gallery(gallery, category, current);
                }
            });

            if (callback) { callback(); }

        });


    }

    function renderImage (category, imageId) {
        var gallery = $('#portfolio .gallery:first').first(),
            overlay = $('#portfolio .overlay').first(),
            single = $('#portfolio .single').first(),
            closeButton = single.children('.close-button').first(),
            prevButton = single.children('.prev-button').first(),
            nextButton = single.children('.next-button').first();

        if (gallery.data('category') !== category) {
            renderPortfolio(category, function () {
                renderImage(category, imageId);
            });
            return;
        }

        var orderedIds = [],
            positions = [],
            pos, l, $im, top;

        gallery.find('img').each(function (_, im) {
            $im = $(im);
            top = $im.offset().top;
            for (pos=0, l=positions.length; pos < l; pos++) {
                if (top < positions[pos]) {
                    break;
                }
            }
            positions.splice(pos, 0, top);
            orderedIds.splice(pos, 0, $im.data('id'));
        });

        var myPos = orderedIds.indexOf(parseInt(imageId)),
            last = orderedIds.length - 1,
            prevId = (myPos === 0) ? orderedIds[last] : orderedIds[myPos - 1],
            nextId = (myPos === last) ?  orderedIds[0] : orderedIds[myPos + 1];

        var switchImg = function () {
            var $this =  $(this);
            window.location.hash = 'portfolio/{0}/{1}'.format(category, $this.data('id'));
            $('#portfolio .single img').animate({opacity: 0}, 100, function () {
                $(this).remove();
            });
        };

        prevButton.data('id', prevId).off('click').click(switchImg);

        nextButton.data('id', nextId).off('click').click(switchImg);


        closeButton.data('id', imageId).off('click').click(function () {
            scrollToImg($(this).data('id'));
            single.hide();
            overlay.animate({opacity: 0}, 400, function () {
                overlay.hide();
                window.location.hash = 'portfolio/{0}'.format(category);
            });
            $('#portfolio .single img').remove();
        });


        closeButton.data('id', imageId).off('click').click(function () {
            $(document).off('keyup');
            scrollToImg($(this).data('id'));
            single.hide();
            overlay.animate({opacity: 0}, 400, function () {
                overlay.hide();
                window.location.hash = 'portfolio/{0}'.format(category);
            });
            $('#portfolio .single img').remove();
        });

        var scrollToImg = function (imageId) {
            $('html, body').animate({scrollTop: $('#' + imageId).offset().top - 8}, 400);
        };

        overlay.show().animate({opacity: 0.95}, 400);
        single.show();

        $(document).off('keyup').keyup(function (event) {
            if (event.keyCode == 27) {
               closeButton.click();
            }
            if (event.keyCode == 37) {
               prevButton.click();
            }
            if (event.keyCode == 39 || event.keyCode == 32) {
               nextButton.click();
            }
        });



        var s = sasien.getImgSrc('large', category, imageId);


        var onImgLoad = function () {
            var $this = $(this);

            $this.on('swipeleft', function () {
                nextButton.click();
            });

            $this.on('swiperight', function () {
                prevButton.click();
            });


            single.append($this);

            var iSizeWidth = $this.width(),
                iSizeHeight = $this.height(),
                iRatio = iSizeWidth / iSizeHeight;

            var draw = function (e, noAnimation) {
                var w = $(window),
                    wWidth = w.width(),
                    wHeight = w.height(),
                    viewWidth = wWidth - 100,
                    viewHeight = wHeight - 60,
                    wRatio = viewWidth / viewHeight,
                    iWidth, iHeight;

                if (wRatio < iRatio) {
                    iWidth = Math.min(Math.max(viewWidth, 50), iSizeWidth);
                    iHeight = Math.round(iWidth / iSizeWidth * iSizeHeight);
                } else {
                    iHeight = Math.min(Math.max(viewHeight, 50), iSizeHeight);
                    iWidth = Math.round(iHeight / iSizeHeight * iSizeWidth);
                }
                if (noAnimation) {
                    $this.css({
                        top: Math.max((wHeight / 2) - (iHeight / 2), 40),
                        left: (wWidth / 2) - (iWidth / 2),
                        width: iWidth,
                        height: iHeight
                    });
                } else {
                    $this.animate({
                        top: Math.max((wHeight / 2) - (iHeight / 2), 40),
                        left: (wWidth / 2) - (iWidth / 2),
                        width: iWidth,
                        height: iHeight
                    }, 100);
                }
            };

            $(window).off('resize').resize(draw);
            draw(true, true);
            $this.animate({opacity: 1}, 500);

        };

        $('<img>').attr({src: s}).load(onImgLoad);
    }

    function renderAbout (language) {
        render('#about-{0}-view'.format(language));
    }

})(window.routie, window.jQuery, window.sasien);
