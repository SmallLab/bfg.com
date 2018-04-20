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
			$('#scrollup').fadeOut("slow");;
		}
	};
	$('[data-toggle="tooltip"]').tooltip();

	$('#exitEnter').click(function () {
        $('#myModalSubLogin').modal('hide');
    });

    $('#cancelSub').click(function () {
        $('#myModalSub').modal('hide');
    });
	isSubscrabers();
};

/*
* Subscription design
* */
$(document).on('click', '[data-id-sent]', function(event) {
               sub = new SubServise(event, $(this));
               sub.init();
            });
//Add subscrabers for user
function SubServise(e, obj) {
    this.e = e;
    this.obj = obj;
    this.id_sub = this.obj.attr('data-id-sent');
    this.popup_is_auth = $('#myModalSub');
    this.popup_is_login = $('#myModalSubLogin');
    this.is_auth_status = data_sub.is_auth;
    this.init = function () {
        this.e.preventDefault();
        this.is_auth_status == 0 ? this.loginSub() : this.addSub();
    };
    this.loginSub = function () {
        $('#enterSystem').attr('href', $('#enterSystem').attr('href')+'&id_sent='+this.id_sub);
        this.popup_is_login.modal('show');
    };

    this.addSub = function () {
        this.popup_is_auth.modal('show');
    };
}
//Show modal window if user is auth and wath redirect
function isSubscrabers() {
    if (data_sub.sub_id != 0) {
       $('[data-id-sent='+data_sub.sub_id+']').click();
    }
}