$(document).ready(function () {

    $('input').on('click', function () {
        $(this).parent().parent().next().show()
    });

    $('input').blur(function(){
        $(this).parent().parent().next().hide()
    });
})
