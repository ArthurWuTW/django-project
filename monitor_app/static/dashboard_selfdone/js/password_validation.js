function Validate()
{
  const pwd = document.querySelector("#password");
  const repeat_pwd = document.querySelector("#repeat_password");
  const error_text = document.querySelector("#error-text");
  if(pwd.value==null || repeat_pwd.value==null){
    return false;
  }

  if(pwd.value!=repeat_pwd.value){
    error_text.removeAttribute("hidden");
    return false;
  }
  else{
    return true;
  }
}
