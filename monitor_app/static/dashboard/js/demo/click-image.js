$("img").click(function(){
  var src = $(this).attr('src')
  // alert(src);
  $("#modal-img").attr('src',src);
  $("#joes").modal('show');

  // return false to prevent the page goes to top
  return false;
})
