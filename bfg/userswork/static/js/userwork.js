$(document).ready(function () {
    $('.delete').click(function (e) {
        $('#myModalDelete').modal('show');
        e.preventDefault();
    });

    $('#cancelDeleted').click(function () {
        $('#myModalDelete').modal('hide');
    });

    $('#deletedSentence').click(function () {
        $('#myModalDelete').modal('hide');
    });
});
