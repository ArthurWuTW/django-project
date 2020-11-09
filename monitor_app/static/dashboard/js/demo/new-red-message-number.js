let msgCenterNav = document.querySelector("#alertsDropdown");

if(messagelog_data['red_message_number']>3){
  let span = document.createElement("span");
  span.setAttribute("class", "badge badge-danger badge-counter");
  span.setAttribute("id", "unread-red-message-count");
  let text = document.createTextNode("3+");
  span.appendChild(text);
  msgCenterNav.appendChild(span);
}
else if(messagelog_data['red_message_number']>0)
{
  let span = document.createElement("span");
  span.setAttribute("class", "badge badge-danger badge-counter");
  span.setAttribute("id", "unread-red-message-count");
  let text = document.createTextNode(messagelog_data['red_message_number']);
  span.appendChild(text);
  msgCenterNav.appendChild(span);
}
