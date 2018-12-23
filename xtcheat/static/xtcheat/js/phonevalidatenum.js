validatenum = ""

/*
 *author:lixin
 *date:20181211
 *desc:修改手机页面表单提交
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
    phonenum = $('#phone').val();
    if (phonenum=="")
    {
        layui.use('layer', function(){
            var layer = layui.layer;
            layer.tips('请输入手机号！', '#phone');
        });
        $('#phone').focus();
        return false;
    }
    if (!(/^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$/.test(phonenum)))
    {
        layui.use('layer', function(){
            var layer = layui.layer;
            layer.tips('请输入有效的手机号码！', '#phone');
        });
        $('#phone').val('');
        $('#phone').focus();
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
            phonenum = $('#phone').val();
            if (phonenum=="")
            {
                layui.use('layer', function(){
                    var layer = layui.layer;
                    layer.tips('请输入手机号！', '#phone');
                });
                $('#phone').focus();
                return;
            }
            if (!(/^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\d{8}$/.test(phonenum)))
            {
                layui.use('layer', function(){
                    var layer = layui.layer;
                    layer.tips('请输入有效的手机号码！', '#phone');
                });
                $('#phone').val('');
                $('#phone').focus();
                return;
            }
            $.ajax({
                url:'../send_phone_validatenum/',
                type:'POST',
                data:{'csrfmiddlewaretoken':$('[name="csrfmiddlewaretoken"]').val(),'phone':phonenum},
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
