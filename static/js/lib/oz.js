/*
Create by Jeroen van der Heijden
Version 0.0.1
*/

'use strict';

(function () {
    var oz = {},
        EMAIL = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

    oz.isEmail = function (s) {
        return EMAIL.test(s);
    };

    window.oz = oz;

})();