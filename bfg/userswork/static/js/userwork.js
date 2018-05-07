$(document).ready(function () {
    $('.delete').click(function (e) {
        $('#myModalDelete').modal('show');
        $('#deletedSentence').attr('href', $(this).attr('href'));
        e.preventDefault();
    });

    $('#cancelDeleted').click(function () {
        $('#myModalDelete').modal('hide');
        $('#deletedSentence').attr('href', '');
    });

});

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
};
