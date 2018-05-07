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

$(document).on('click', '[data-id-subs]', function(event) {
    event.preventDefault();
    var id_sub = $(this).attr('data-id-subs');
    $('#hellopreloader_preload_sub').css({'display':'block', 'opacity': '0.5'});
    $.get(
        "/user/privateoffice/deactivesub/"+$(this).attr('data-id-subs')+"/",
        onAjaxSuccess
    );
    function onAjaxSuccess(data){
        if (data.status == true){
            $('[data-is-active-info="'+id_sub+'"]').text('Активна');
            $('[data-is-active-action="'+id_sub+'"]').text('Деактивировать');
            $('#hellopreloader_preload_sub').css({'display':'none'});
        }
        else {
            $('[data-is-active-info="'+id_sub+'"]').text('Не активна');
            $('[data-is-active-action="'+id_sub+'"]').text('Активировать');
            $('#hellopreloader_preload_sub').css({'display':'none'});
        }
    }
});