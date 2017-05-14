$(document).ready( function(){
  if ($('#authfail').text() != 0) {
      $('#myModal').modal()
  }

  $('.btn-vk').click(function () {
      $('#hellopreloader_preload').css({'display':'block', 'opacity': '0.5'});
      return true;
  })

});