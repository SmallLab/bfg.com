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
