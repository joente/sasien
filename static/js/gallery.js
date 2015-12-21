'use strict';

(function ($, sasien) {

    sasien.getGalleryIds = function (portfolio, categoryName) {
        var galleryIds = [];
        $.each(portfolio, function (idx, category) {
            if (category.name === categoryName) {
                $.each(category.images, function (idx, image) {
                    galleryIds.push(image.id);
                });
            }
        });
        return galleryIds;
    };

    var getColumn = function () {
        return {
            elem: $('<ul>'),
            size: 0
        };
    };

    var addToColumn = function (columns, item) {
        var column = 0,
            size = columns[column].size;

        for (var i=1, l=columns.length; i < l; i++) {
            if (columns[i].size < size) {
                column = i;
            }
        }
        columns[column].elem.append($('<li>').append(item));
        columns[column].size += item.height();
    };

    sasien.gallery = function (container, categoryName, settings, callback) {
        var defaults = {
            nColumns: 3
        };

        container.html('');

        var imageIds = sasien.getGalleryIds(window.portfolio, categoryName);

        var config = $.extend({}, defaults, settings);
        var i, s, id, count=0, nImages=imageIds.length;
        var columns = sasien.repeat(getColumn, config.nColumns);
        var galleryIds = sasien.shuffle(imageIds);

        for (i=0; i < config.nColumns; i++) {
            container.append($('<div class="col-xs-6 col-sm-4">').append(columns[i].elem));
        }

        var onImgLoad = function () {
            addToColumn(columns, $(this));
            count += 1;
            if (callback && count === nImages ) {
                callback();
            }
        };

        var onImgClick = function () {
            sasien.clickImage($(this).data('id'));
        };

        for (i=0; i < nImages; i++) {
            id = galleryIds[i];
            s = sasien.getImgSrc('gallery', categoryName, id);
            $('<img>').attr({id: id, src: s}).data('id', id).click(onImgClick).load(onImgLoad);
        }
    };
})(window.jQuery, window.sasien);