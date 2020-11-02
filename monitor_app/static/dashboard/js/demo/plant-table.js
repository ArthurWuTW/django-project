let mountains = table_data['plants'];
let path = table_data['path'];

function generateTableHead(table, data) {
  let thead = table.createTHead();
  let row = thead.insertRow();
  for (let key of data) {
    let th = document.createElement("th");
    let text = document.createTextNode(key);
    th.appendChild(text);
    row.appendChild(th);
  }
}

function generateTable(table, data) {
  for (let element of data) {
    // console.log(element)
    let row = table.insertRow();
    for (key in element) {
      if(key=="Image"){
        let cell = row.insertCell();

        var img = document.createElement('img');
        img.src = path+element[key];
        img.style.width = "30%";
        img.style.height = "30%"
        cell.appendChild(img);

        // <img src={% static "2020jav_10_29_1.jpg" %} width="70%" height="70%">
      }
      else{
        let cell = row.insertCell();
        let text = document.createTextNode(element[key]);
        cell.appendChild(text);
      }
    }
  }
}

let table = document.querySelector("#dataTable"); // querySelector("#id")
let data = Object.keys(mountains[0]);
generateTable(table, mountains);
generateTableHead(table, data);
