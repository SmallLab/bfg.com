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
    this.init = function () {
        e.preventDefault();
        alert(obj.attr('data-id-sent'));
    };
}