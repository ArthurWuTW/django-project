let path = table_data['path']+"data_image/";
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
  for(let element of data){
    // insert First element space
    let row = table.insertRow();
    let cell = row.insertCell();
    let text = document.createTextNode(element[0]);
    cell.appendChild(text);

    // insert image from index 1
    for(var i=1;i<element.length;++i){
      let cell = row.insertCell();
            let a = document.createElement("a");
            a.setAttribute("href", "#");

            var img = document.createElement('img');
            img.src = path+element[i];
            img.style.width = "15%";
            img.style.height = "15%";
            img.setAttribute("onclick","function()");
            img.setAttribute("id", "plant-img");
            a.appendChild(img)
            cell.appendChild(a);
    }
  }
}

let table = document.querySelector("#dataTable"); // querySelector("#id")
generateTable(table, table_data['data']);
generateTableHead(table, table_data['title']);
