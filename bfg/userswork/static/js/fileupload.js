window.URL = window.URL || window.webkitURL;
function handleMainFile(files){
    var numFiles = files.length;
    if (files[0].type != 'image/jpg'){
        var img = document.createElement("img");
        document.getElementById('main_file_select').insertBefore(img, document.getElementById('before_img'));
        //img.insertBefore(document.getElementById('before_img'));
        var reader = new FileReader();
    //download file
        reader.onload = (function(aImg) { return function(e) { aImg.src = e.target.result; }; })(img);
    //read file in string base64
        reader.readAsDataURL(files[0]);
    }

}

$('#main_file_select').on("click", function (e) {
     $('#main_file_img').click();
     e.preventDefault(); // prevent navigation to "#"
});
