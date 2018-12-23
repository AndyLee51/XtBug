validatenum = ""

/*
 *author:lixin
 *date:20181211
 *desc:修改邮箱页面表单提交
 *input:none
 *return:boolean
*/
function compare()
{
    inputvalinum = $('#validate').val()
    if (inputvalinum!=validatenum)
    {
        layui.use('layer', function(){
            var layer = layui.layer;
            layer.tips('验证码输入错误，请重新输入！', '#validate');
        });
        $('#validate').val('')
        $('#validate').focus()
        return false
    }
    emailaddress = $('#email').val();
    if (emailaddress=="")
    {
        layui.use('layer', function(){
            var layer = layui.layer;
            layer.tips('请输入邮箱地址！', '#email');
        });
        $('#email').focus();
        return false;
    }
    if (!(/^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/.test(emailaddress)))
    {
        layui.use('layer', function(){
            var layer = layui.layer;
            layer.tips('请输入有效的邮箱地址！', '#email');
        });
        $('#email').val('');
        $('#email').focus();
        return false;
    }
    return true
}

$(function() {
 
    var btn = ($('#getValinum'));
	$(function() {
		btn.click(settime);
	})
	var countdown = 30;//倒计时总时间，为了演示效果，设为5秒，一般都是60s
	function settime() {
        if (countdown==30)
        {
            emailaddress = $('#email').val();
            if (emailaddress=="")
            {
                layui.use('layer', function(){
                    var layer = layui.layer;
                    layer.tips('请输入邮箱地址！', '#email');
                });
                $('#email').focus();
                return;
            }
            if (!(/^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$/.test(emailaddress)))
            {
                layui.use('layer', function(){
                    var layer = layui.layer;
                    layer.tips('请输入有效的手机号码！', '#email');
                });
                $('#email').val('');
                $('#email').focus();
                return;
            }
            $.ajax({
                url:'../send_email_validatenum/',
                type:'POST',
                data:{'csrfmiddlewaretoken':$('[name="csrfmiddlewaretoken"]').val(),'email':emailaddress},
                success:function(ret){
                    validatenum = ret
                }
            });
        }
		if (countdown == 0) {
			btn.attr("disabled", false);
			btn.html("获取验证码");
			btn.removeClass("disabled");
			countdown = 30;
			return;
		} else {
			btn.addClass("disabled");
			btn.attr("disabled", true);
			btn.html("重新发送(" + countdown + ")");
			countdown--;
		}
		setTimeout(settime, 1000);
	}
 
})
