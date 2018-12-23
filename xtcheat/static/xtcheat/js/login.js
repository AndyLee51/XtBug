$(function(){
    if ($('#id_username').val()=="")
    {
        $.ajax({
            url:'../get_info_via_cookies/',
            type:'POST',
            data:{'csrfmiddlewaretoken':$('[name="csrfmiddlewaretoken"]').val()},
            success:function(ret){
                if (ret!="{}")
                {
                    info =JSON.parse(ret)
                    $('#id_username').val(info['account'])
                    $('#id_password').val(info['password'])
                    $('#IsRemember').prop("checked", true)
                }
            }
        })
    }
})