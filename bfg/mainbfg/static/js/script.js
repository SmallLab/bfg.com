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
	$('[data-toggle="tooltip"]').tooltip()
};

/*
* Subscription design
* */
$(document).on('click', '[data-id-sent]', function(event) {
               sub = new SubServise(event, $(this));
               sub.init();
            });

function SubServise(e, obj) {
    this.e = e;
    this.obj = obj;
    this.popup_is_auth = $('#myModalSub');
    this.popup_is_login = $('#myModalSubLogin');
    this.is_auth_status = data_sub.is_auth;
    this.init = function () {
        this.e.preventDefault();
        //alert(this.obj.attr('data-id-sent'));
        //alert(data_sub.current_url);
        this.is_auth_status == 0 ? this.loginSub() : this.addSub();

    };
    this.loginSub = function () {
        var current_url = window.location;
        //$('#enterSystem').attr('href', '/login/?next='+current_url+'');
        this.popup_is_login.modal('show');
    };

    this.addSub = function () {
        this.popup_is_auth.modal('show');
    }
}