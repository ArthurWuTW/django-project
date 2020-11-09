function clickCount(){

  click_msgbell_count++;
  console.log(click_msgbell_count);

  // remove red unread hint
  let msgCenterNav = document.querySelector("#alertsDropdown");
  let unreadCountSpan = document.querySelector("#unread-red-message-count")
  if(unreadCountSpan != null){
    msgCenterNav.removeChild(unreadCountSpan);
  }

  if(click_msgbell_count == 1){
    // show unread message board
    let h6 = document.createElement("h6");
    h6.setAttribute("class", "dropdown-header");
    let text = document.createTextNode("Alerts Center");
    h6.appendChild(text);

    var msgCenter = document.querySelector("#messageCenter");
    while(msgCenter.firstChild){
      msgCenter.removeChild(msgCenter.firstChild);
    }
    msgCenter.appendChild(h6);

    for(let data of messagelog_data['messagelog_array']){
      let a = document.createElement("a");
      a.setAttribute("class", "dropdown-item d-flex align-items-center");
      a.setAttribute("href", "#");

      let div1 = document.createElement("div");
      div1.setAttribute("class", "mr-3");

      let div2 = document.createElement("div");
      div2.setAttribute("class", "icon-circle bg-primary");

      let i = document.createElement("i");
      i.setAttribute("class", "fas fa-file-alt text-white");
      div2.appendChild(i);
      div1.appendChild(div2);
      a.appendChild(div1);

      let div3 = document.createElement("div");
      let div4 = document.createElement("div");
      div4.setAttribute("class", "small text-gray-500");
      let text1 = document.createTextNode(data['delta_time']);
      div4.appendChild(text1);
      div3.appendChild(div4);

      if(data['read']){
        let text2 = document.createTextNode(data['log']);
        div3.appendChild(text2);
      }
      else{
        let span = document.createElement("span");
        span.setAttribute("class", "font-weight-bold");
        let text2 = document.createTextNode(data['log']);
        span.appendChild(text2);
        div3.appendChild(span);
      }

      a.appendChild(div3);
      msgCenter.appendChild(a);
    }

    // // ajax pass read value back to django
    // for(let data of messagelog_data['messagelog_array']){
    //   data['read'] = true;
    // }
  }
  else if(click_msgbell_count >1){
    $.ajax({
      type: "GET",
      url: messagelog_data['update_message_path'],
      data: {'data': []},
    }).done(function(respose){
      $("#messageCenter").html(respose);
    })
  }
}
