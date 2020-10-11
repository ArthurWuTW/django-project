// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var chart = new Chart(ctx, {
    type:'line',
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            label: 'My First dataset',
            backgroundColor: 'rgb(255, 99, 132)',
            borderColor: 'rgb(255, 99, 132)',
            data: [0, 10, 5, 2, 20, 30, 45]
        }]
    },
    options:{
      maintainAspectRatio:false,
      legend:{
        display:false
      },
      title:{},
      scales:{
        xAxes:[
          {
            gridLines:{
              color:'rgb(234, 236, 244)',
              zeroLineColor:'rgb(234, 236, 244)',
              drawBorder:false,
              drawTicks:false,
              borderDash:[2],
              zeroLineBorderDash:[2],
              drawOnChartArea:false},
              ticks:{
                fontColor:'#858796',
                padding:20
              }
            }
          ],
          yAxes:[
            {
              gridLines:{
                color:'rgb(234, 236, 244)',
                zeroLineColor:'rgb(234, 236, 244)',
                drawBorder:false,
                drawTicks:false,
                borderDash:[2],
                zeroLineBorderDash:[2]
              },
              ticks:{
                fontColor:'#858796',
                padding:20
              }
            }
          ]
        }
      }
});
