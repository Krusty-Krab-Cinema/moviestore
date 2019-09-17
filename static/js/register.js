$(document).ready(function () {
    // 验证昵称是否被占用
    $('#nickname').bind('blur', function () {
        // 验证长度
        if($(this).val().length < 4 || $(this).val().length > 16){
            $('#nickerror1').show();
            return;
        }
        
        $.post('/register/', {'nickname':$(this).val()}, function (data, status) {
            if(data.data == '1'){
                $('#nickerror2').show();
            }
        })
    })
    
    $('#nickname').bind('focus', function () {
        $('#nickerror1').hide();
        $('#nickerror2').hide();
        $('#emailerror1').hide();
        $('#emailerror2').hide();
        $(this).val('')
    })

    // 验证邮箱是否可用
    $('#email').bind('blur', function () {
        // 验证长度
        if($(this).val().indexOf('@') == -1){
            $('#emailerror1').show();
            return;
        }

        $.post('/register/', {'email':$(this).val()}, function (data, status) {
            if(data.data == '2'){
                $('#emailerror2').show();
            }
        })

    })
    $('#email').bind('focus', function () {
        $('#emailerror1').hide();
        $('#emailerror2').hide();
        $(this).val('');
    })

    $('#password').bind('blur', function () {
        // 验证长度
        if($(this).val().length < 6 || $(this).val().length > 16){
            $('#passworderror1').show();
            return;
        }
    })

    $('#password').bind('focus', function () {
        $('#passworderror1').hide();
        $('#passworderror2').hide();
        $('#password').val('');
    })

    $('#repassword').bind('blur', function () {
        var password = document.getElementById('password').value;
        var repassword = document.getElementById('repassword').value;
        console.log(password)
        console.log(repassword)

        if(password != repassword){
            $('#passworderror2').show();
            return;
        }
    })

    $('#repassword').bind('focus', function () {
        $('#passworderror2').hide();
        $('#repassword').val('');
    })





})