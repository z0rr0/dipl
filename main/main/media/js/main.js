/*
 for djago Cross Site Request Forgery protection (CSRF)
 https://docs.djangoproject.com/en/1.4/ref/contrib/csrf/
*/
jQuery(document).ajaxSend(function(event, xhr, settings) {
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
    // $('#product_list').html('<p>Пожалуйста подождите, идет поиск...</p>');
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
// quickly edit product
function smalledit (product, p) {
    // $('#product_' + product).html('<p>Пожалуйста подождите, идет поиск...</p>');
    $.ajax({
        url: '/product/smalledit/' + product,
        type: 'GET',
        data: {
            page: p
        },
        dataType: 'html',
        context: document.body,
        success: function (data) {
            $('#product_' + product).html(data);
        },
        error: function () {
            message = "<p>Ошибка обработки данных.</p>";
            $('#product_' + product).html(message);
        },
    });
}
// cancal edit product, return to view product
function smalledit_cancel (product, p) {
    $.ajax({
        url: '/product/smallview/' + product,
        type: 'GET',
        data: {
            page: p
        },
        dataType: 'html',
        context: document.body,
        success: function (data) {
            $('#product_' + product).html(data);
        },
        error: function () {
            message = "<p>Ошибка обработки данных.</p>";
            $('#product_' + product).html(message);
        },
    });
}
// validate data
function val_validate(val_id, force) {
    str = $(val_id).val();
    str = jQuery.trim(str.replace(/,/gi, "."));
    $(val_id).val(str);
    if (force) val = parseFloat(str);
    else val = str;
    if (isNaN(val)) return false;
    else return val;
}
function unint_validate(val_id, forse) {
    str = $(val_id).val();
    val = parseInt(str);
    if (forse) val = Math.abs(val);
    if (isNaN(val) || (val == 0)) return false;
    else return val;
}
function torusdec (val_id) {
    str = $(val_id).val();
    str = jQuery.trim(str.replace(/,/gi, "."));
    $(val_id).val(str);
    return str;
}
function smalledit_save (product, p) {
    prefix = '#id_' + product + '_';
    name_id = prefix + 'name';
    price_id = prefix + 'price';
    rest_id = prefix + 'rest';
    price = torusdec(price_id);
    rest = torusdec(rest_id);
    to_data_send = {
        name: $(name_id).val(),
        price: price,
        rest: rest,
        comment: $(prefix + 'comment').val()
    }
    if ($(prefix + 'service').is(':checked')) to_data_send['service'] = 1;
    // else service = 0; 
    $.ajax({
        url: '/product/smalledit/' + product + '/?page=' + p,
        type: 'POST',
        data: to_data_send,
        dataType: 'html',
        context: document.body,
        success: function (data) {
            if (data != '1') {
                // alert('Пожалуйста проверьте указанные значения (название не может дублироваться)');
                $('#product_' + product).html(data);
            }
            else {
                smalledit_cancel(product, p);
            }
        },
        error: function () {
            error_msg = "Ошибка обработки данных. Возможно у Вас не хватает прав или нет соединения с сервером.";
            alert(error_msg);
        },
    });
}
function reqlist_search() {
    $.ajax({
        url: '/reqlist/search/',
        type: 'POST',
        data: {
            client: $('#id_client').val()
        },
        dataType: 'html',
        context: document.body,
        success: function (data) {
            $('#clientreq').html(data);
        },
        error: function () {
            error_msg = "<p>Ошибка обработки данных. Возможно у Вас не хватает прав или нет соединения с сервером.</p>";
            $('#clientreq').html(error_msg);
        },
    });
}
// delete product record
function delete_req(id) {
    $.get('/reqlist/ajdel/' + id, function(data) {
            reqlist_search();
        }).error(function() { 
            error_msg = "Ошибка обработки данных. Возможно у Вас не хватает прав или нет соединения с сервером.";
            alert(error_msg);
        });
}
function delete_reqlist(id) {
    $.get('/reqlist/ajdel/' + id, function(data) {
            get_product();
            get_reqlist();
        }).error(function() { 
            error_msg = "Ошибка обработки данных. Возможно у Вас не хватает прав или нет соединения с сервером.";
            alert(error_msg);
        });
}
// get all product for client
function get_product() {
    $.ajax({
        url: '/reqlist/product/',
        type: 'POST',
        data: {
            client: $('#id_client').val(),
            name: $('#id_search').val()
        },
        dataType: 'html',
        context: document.body,
        success: function (data) {
            $('#div_product').html(data);
        },
        error: function () {
            error_msg = "<p>Ошибка обработки данных. Возможно у Вас не хватает прав или нет соединения с сервером.</p>";
            $('#div_product').html(error_msg);
        },
    });
}
// get all reqlist for client
function get_reqlist() {
    $.ajax({
        url: '/reqlist/client/' + $('#id_client').val(),
        type: 'GET',
        dataType: 'html',
        context: document.body,
        success: function (data) {
            $('#div_reqlist').html(data);
        },
        error: function () {
            error_msg = "<p>Ошибка обработки данных. Возможно у Вас не хватает прав или нет соединения с сервером.</p>";
            $('#div_reqlist').html(error_msg);
        },
    });
}
// sent update reqlist
function update_reqlist() {
    datas = {'len': $("#countreq").val()};
    validate = true;
    for (var i = 1; i <= $("#countreq").val(); i++) {
        datas['id' + i] = $('#id_id_' + i).val();
        datas['number' + i] = unint_validate('#id_number_' + i, true);
        if (datas['number' + i]) $('#id_number_' + i).val(datas['number' + i]);
        else validate = false;
    };
    if (validate) {
        $.ajax({
            url: '/reqlist/client/' + $('#id_client').val(),
            type: 'POST',
            data: datas,
            dataType: 'html',
            context: document.body,
            success: function (data) {
                $('#div_reqlist').html(data);
            },
            error: function () {
                error_msg = "<p>Ошибка обработки данных. Возможно у Вас не хватает прав или нет соединения с сервером.</p>";
                $('#div_reqlist').html(error_msg);
            },
        }); 
    }
    else {
        alert('Пожалуйста, проверьте значения для количества товара.');
    }
}
// add product in reqlist
function addreq_product(id) {
    $.ajax({
        url: '/reqlist/plus/' + $('#id_client').val() + '/' + id,
        type: 'GET',
        dataType: 'html',
        context: document.body,
        success: function (data) {
            get_product();
            get_reqlist();
        },
        error: function () {
           error_msg = "Ошибка обработки данных. Возможно у Вас не хватает прав или нет соединения с сервером.";
            alert(error_msg);
        },
    });
}
// get date report
function get_date_report () {
    $.ajax({
        url: '/reports/viewdiv/',
        type: 'GET',
        data: {
            reptype: $('#id_reptype').val(),
            date1: $('#id_date1').val(),
            date2: $('#id_date2').val()
        },
        dataType: 'html',
        context: document.body,
        success: function (data) {
            $('#report_list').html(data);
        },
        error: function () {
            error_msg = "<p>Ошибка обработки данных. Возможно у Вас не хватает прав или нет соединения с сервером.</p>";
            $('#report_list').html(error_msg);
        },
    });
}
