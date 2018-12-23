$(function(){
    layui.use('form',function(){
        var form = layui.form
        form.on('checkbox(phoneon)', function(data){
            phonenum = $('#phone_span').html()
            if (phonenum == '空')
            {
                layui.use('layer', function(){
                    var layer = layui.layer;
                    layer.tips('请先填写手机号！', '#phone_span');
                });
                return;
            }
            phoneon = data.elem.checked
            $.ajax({
                url:'../change_phoneon/',
                type:'POST',
                data:{'csrfmiddlewaretoken':$('[name="csrfmiddlewaretoken"]').val(),'phoneon':String(phoneon)},
                success:function(ret){
                    if (ret=='True')
                    {
                        layui.use('layer', function(){
                            var layer = layui.layer;
                            layer.msg('已开通短信提醒');
                        }); 
                    }
                    else
                    {
                        layui.use('layer', function(){
                            var layer = layui.layer;
                            layer.msg('已关闭短信提醒');
                        }); 
                    }
                },
            })
        });
        form.on('checkbox(emailon)', function(data){
            emailaddress = $('#email_span').html()
            if (emailaddress == '空')
            {
                layui.use('layer', function(){
                    var layer = layui.layer;
                    layer.tips('请先填写邮箱地址！', '#email_span');
                });
                return;
            }
            emailon = data.elem.checked
            $.ajax({
                url:'../change_emailon/',
                type:'POST',
                data:{'csrfmiddlewaretoken':$('[name="csrfmiddlewaretoken"]').val(),'emailon':String(emailon)},
                success:function(ret){
                    if (ret=='True')
                    {
                        layui.use('layer', function(){
                            var layer = layui.layer;
                            layer.msg('已开通邮件提醒');
                        }); 
                    }
                    else
                    {
                        layui.use('layer', function(){
                            var layer = layui.layer;
                            layer.msg('已关闭邮件提醒');
                        }); 
                    }
                },
            })
        });
    })
})
