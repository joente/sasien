/* global $ */

'use strict';

String.prototype.format = function () {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
        return typeof args[number] != 'undefined' ? args[number] : match;
    });
};

$(document).ready(function () {
    // Close menu on click while in mobile view
    $('.navbar-collapse a').not('.dropdown-toggle').click(function () {
        if ($('.navbar-collapse').is(':visible') && $('.navbar-toggle').is(':visible')) {
            $('.navbar-collapse').collapse('toggle');
        }
    });

    // Enable bootstrap tooltips
    $('.footer [data-toggle="tooltip"]').tooltip().click(function () {
        $(this).tooltip('hide');
    });

});
