/*
* To Top
*/

window.onload = function() {
	$('#scrollup').click(function() {
         $('body,html').animate({scrollTop:0},800);
    });
	window.onscroll = function () {
		if ( window.pageYOffset > 0 ) {
			$('#scrollup').fadeIn("slow");
		} else {
			$('#scrollup').fadeOut("slow");
		}
	};
	$('[data-toggle="tooltip"]').tooltip();

	$('#exitEnter').click(function () {
        $('#myModalSubLogin').modal('hide');
    });

    $('#cancelSub').click(function () {
        $('#myModalSub').modal('hide');
    });

    $('#myModalSubOk').click(function () {
        $('#myModalSubOk').modal('hide');
    });
	isSubscrabers();
};

/*
* Subscription design
* */
$(document).on('click', '[data-id-sent]', function(event) {
               if ($.inArray(+$(this).attr('data-id-sent'), data_sub.sub_list)== -1) {
                   sub = new SubServise(event, $(this));
                   sub.init();
               }
               else {
                   alert('Вы уже подписаны на данного автора!!!');
                   return false;
               }
           });

//Add subscrabers for user
function SubServise(e, obj) {
    this.e = e;
    this.obj = obj;
    this.id_sub = this.obj.attr('data-id-sent');
    this.autor = this.obj.attr('data-autor-sent');
    this.popup_is_auth = $('#myModalSub');
    this.popup_is_login = $('#myModalSubLogin');
    this.popup_sub_ok = $('#myModalSubOk');
    this.is_auth_status = data_sub.is_auth;
    this.init = function () {
        this.e.preventDefault();
        this.is_auth_status == 0 ? this.loginSub() : this.addDataSub();
        $('[name="email_sms"]').on('click', enterData);
        $('#addSub').on('click', this.sendDataSub);
    };

    this.sendDataSub = function () {
        $('#hellopreloader_preload_sub').css({'display':'block', 'opacity': '0.5'});
        if ($("#sms_data").is(":checked")){
                               if (checkPhone($('#dataSub').val())){
                                   $('#sub_data_error').text('');
                                   this.sendIdSub(0, $('#dataSub').val());
                                   data_sub.sub_list.push(parseInt(this.id_sub));
                                   this.popup_is_auth.modal('hide');
                                   $('#autor_sent_ok').text(this.autor);
                                   this.popup_sub_ok.modal('show');
                                   this.destroy();
                                   console.log(data_sub.sub_list);
                               }
                               else {
                                    $('#hellopreloader_preload_sub').css({'display':'none'});
                                    $('#sub_data_error').text('Введите корректный номер телефона');

                               }
                           }
        else if ($("#email_data").is(":checked")){
                                if (checkEmail($('#dataSub').val())){
                                    $('#sub_data_error').text('');
                                    this.sendIdSub(1, $('#dataSub').val());
                                    data_sub.sub_list.push(parseInt(this.id_sub));
                                    this.popup_is_auth.modal('hide');
                                    $('#autor_sent_ok').text(this.autor);
                                    this.popup_sub_ok.modal('show');
                                    this.destroy();
                                    console.log(data_sub.sub_list);
                                }
                                else {
                                    $('#hellopreloader_preload_sub').css({'display':'none'});
                                    $('#sub_data_error').text('Введите корректный адрес почты');

                                }
        }
        else {
            $('#hellopreloader_preload_sub').css({'display':'none'});
            $('#sub_data_error').text('Введите корректные данные');
        }
    }.bind(this);

    this.sendIdSub = function (type_sub, data_type) {
            $.get(
              "/sentence/addsub/",
              {
                  id_sub: this.id_sub,
                  type_sub:type_sub,
                  data_type:data_type
              },
              onAjaxSuccess
            );
            function onAjaxSuccess(data)
            {
                if (data.status){
                    $('#hellopreloader_preload_sub').css({'display':'none'});
                    return true;
                }
                else {
                    alert('Ошибка!!!Попробуйте позже!!!');
                    return false;
                }
            }
            return onAjaxSuccess;
    };
//Show window popup for login
    this.loginSub = function () {
        $('#enterSystem').attr('href', $('#enterSystem').attr('href')+'&id_sent='+this.id_sub);
        this.popup_is_login.modal('show');
    };
//Show form for enter data sub
    this.addDataSub = function () {
        $('#autor_sent').text(this.autor);
        this.popup_is_auth.modal('show');
    };
//Enter data for sub
    function enterData() {
            if ($(this).attr('id') == 'sms_data'){
                if(data_sub.phone){
                    $('#dataSub').val(data_sub.phone);
                }
                else {
                    $('#dataSub').val('');
                    $('#dataSub').attr('placeholder', 'Введите телефон (999)123-45-67');
                }
            }
            else{
                if (data_sub.email) {
                    $('#dataSub').val(data_sub.email);
                }
                else {
                    $('#dataSub').val('');
                    $('#dataSub').attr('placeholder', 'Введите EMAIL');
                }
            }
        }

    function checkEmail(email) {
        var regex = /^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
        return regex.test(email);
    }
    
    function checkPhone(phone) {
        var regex = /^\([\d]{2,3}\)[\d]{2,3}-[\d]{2}-[\d]{2}$/;
        return regex.test(phone);
    }

    this.destroy = function(){
        this.init = null;
        this.id_sub = null;
        this.sendDataSub = undefined;
        this.sendIdSub = function () {
            return undefined;
        };
        //$('#autor_sent_ok').text('');
        $('#autor_sent').text('');
        console.log(this);
    }
}
//Show modal window for enter data sub when user is auth and wath redirect for prew page
function isSubscrabers() {
    if (data_sub.sub_id != 0 && $.inArray(+data_sub.sub_id, data_sub.sub_list) == -1) {
       $('[data-id-sent='+data_sub.sub_id+']')[0].click();
    }
    else if (data_sub.sub_id == 0){
        return false;
    }
    else {
        alert('Вы уже подписаны на данного автора!!!');
        return false;
    }
}