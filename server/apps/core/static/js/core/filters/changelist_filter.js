if (!$) { $ = django.jQuery; }

$(document).ready(function(){
    var LIST_FILTER = 'is_list_filter';
    var PARAMETER = 'parameter'

    initSelect2();
    initUI();
    initHandlers();

    function initSelect2() {
        var elements = $('select.filter-autocomplete').not('.is-rendered');

        for (var i = 0; i < elements.length; i++) {
          var $element = $(elements[i]);
          $element.djangoAdminSelect2();
          $element.addClass('is-rendered');
        }
    }

    function initUI() {
        $('select[' + LIST_FILTER + ']').next('span.select2.select2-container').css('width', '100%');
    }

    function initHandlers() {
        $('select[' + LIST_FILTER + ']').on('change', function (e) {
            $target = $(e.target);

            var value = $target.val();
            var parameter = $target.data(PARAMETER);

            setFilter(parameter, value);
        });
    }

    function setFilter(parameter, value) {
        window.location.search = updateSearch(window.location.search, parameter, value);
    }

    function updateSearch(search, parameter, value) {
        var searchParams = new URLSearchParams(search);
        searchParams.delete(parameter);

        if (!value) {
            return searchParams.toString();
        }

        if (!Array.isArray(value)) {
            value = [value];
        }

        for (var i in value) {
            searchParams.append(parameter, value[i])
        }

        return searchParams.toString();
    }
});
