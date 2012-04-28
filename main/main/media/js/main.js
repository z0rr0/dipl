/*
 for djago Cross Site Request Forgery protection (CSRF)
*/
$(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});
function product_search(page) {
    page = typeof page !== 'undefined' ? page : 1;
    $('#product_list').html('<p>Пожалуйста подождите, идет поиск...</p>');
    var_provider = $('#id_provider').val();
    var_search = $('#id_search').val();
    if ($('#id_onlyservice').is(':checked')) var_onlyserv = 1;
    else var_onlyserv = 0;
    $.ajax({
        url: '/product/search/?page=' + page,
        type: 'POST',
        data: {
            provider: var_provider,
            search : var_search,
            onlyservice: var_onlyserv,
        },
        dataType: 'html',
        context: document.body,
        success: function (data) {
            $('#product_list').html(data);
        },
        error: function () {
            message = "<p>Ошибка обработки данных.</p>";
            $('#product_list').html(message);
        },
    });
}
// delete product record
function delete_product(id) {
    if (confirm("Уверены, что хотите удалить данные?"))
        $.get('/product/ajdel/' + id, function(data) {
                product_search();
            }).error(function() { 
                error_msg = "Ошибка обработки данных. Возможно у Вас не хватает прав или нет соединения с сервером.";
                alert(error_msg);
            });
}
