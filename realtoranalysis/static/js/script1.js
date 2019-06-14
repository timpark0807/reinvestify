$(document).ready(function(){

// This loads a doughnut chart when you open the page
         chartx = new Chart(document.getElementById("bar-chart"), {
                      type: 'doughnut',
                         data: {
                               labels: ["Mortgage", "Taxes", "Insurance"],
                               datasets: [
                               {
                                backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
                                data: [429, 90, 80]
                               }
                               ]
                               },
                         options: {
                                legend: { display: true,
                                          position: 'bottom',
                                          }

                                          ,
                                 title: {
                                  display: false
                                        }
                                },

                        });

         Chart.pluginService.register({
              beforeDraw: function(chart) {
                var width = chart.chart.width,
                    height = chart.chart.height,
                    ctx = chart.chart.ctx;

                ctx.restore();
                var fontSize = (height / 114).toFixed(2);
                ctx.font = fontSize + "em sans-serif";
                ctx.textBaseline = "middle";

                var text = '$599',
                    textX = Math.round((width - ctx.measureText(text).width) / 2),
                    textY = (height / 2)-12;

                ctx.fillText(text, textX, textY);
                ctx.save();
              }

            })


// This refreshes donut chart on submit via ajax calls

    $('form').on('submit', function(event) {

        $.ajax({
            data : {
                price : $('#price_id').val(),
                down_payment : $('#down_payment_id').val(),
                term : $('#term_id').val(),
                interest_rate : $('#interest_rate_id').val()
            },
            type : 'POST',
            url : '/process'
        })
        .done(function(data) {

         chartx = new Chart(document.getElementById("bar-chart"), {
              type: 'doughnut',
                 data: {
                       labels: data.labels,
                       datasets: [
                       {
                        label: "Population (millions)",
                        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
                        data: data.number
                       }
                       ]
                       },
                 options: {
                        legend: { display: true,
                                  position: 'bottom',
                                  }

                                  ,
                         title: {
                          display: false
                                }
                        },

                });

         Chart.pluginService.register({
              beforeDraw: function(chart) {
                var width = chart.chart.width,
                    height = chart.chart.height,
                    ctx = chart.chart.ctx;

                ctx.restore();
                var fontSize = (height / 114).toFixed(2);
                ctx.font = fontSize + "em sans-serif";
                ctx.textBaseline = "middle";

                var text = '$' + data.total,
                    textX = Math.round((width - ctx.measureText(text).width) / 2),
                    textY = (height / 2)-12;

                ctx.fillText(text, textX, textY);
                ctx.save();
              }

            })


        });

   });

});


//    values = [12, 19, 3]
//    labels = ['Red', 'Blue', 'Yellow']
//    colors = ['#ff0000','#0000ff','#008000']
//
//    var ctx = $('#mycanvas').get(0).getContext("2d");
//
//    var data = [
//        {
//            value:270,
//            color: "cornflowblue",
//            highlight: "lightblue",
//            label: "javascript"
//        },
//
//        {
//            value: 25,
//            color: "lightgreen",
//            highlight: "yellowgreen",
//            label: "html"
//        },
//
//        {
//            value: 50,
//            color: "orange",
//            highlight: "darkorange",
//            label: "python"
//        }
//
//    ];
//
//    var chart = new Chart(ctx).Doughnut(data);
//
//
//
//  });

//BELOW IS GOOD
//           var _data;
//           var _labels;
//          $.ajax({
//           url: "/get_data",
//           type: "get",
//           data: {vals: ''},
//           success: function(response) {
//             full_data = JSON.parse(response.payload);
//             _data = full_data['data'];
//             _labels = full_data['labels'];
//           },
//
//         });
//         new Chart(document.getElementById("bar-chart"), {
//          type: 'bar',
//         data: {
//           labels: _labels,
//           datasets: [
//           {
//            label: "Population (millions)",
//            backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
//           data: _data
//           }
//           ]
//           },
//            options: {
//            legend: { display: false },
//             title: {
//              display: true,
//             text: 'Predicted world population (millions) in 2050'
//           }
//          }
//         });
//
//        });
//
//         Chart.pluginService.register({
//              beforeDraw: function(chart) {
//                var width = chart.chart.width,
//                    height = chart.chart.height,
//                    ctx = chart.chart.ctx;
//
//                ctx.restore();
//                var fontSize = (height / 114).toFixed(2);
//                ctx.font = fontSize + "em sans-serif";
//                ctx.textBaseline = "middle";
//
//                var text = (data.mortgage_payment),
//                    textX = Math.round((width - ctx.measureText(text).width) / 2),
//                    textY = (height / 2)-12;
//
//                ctx.fillText(text, textX, textY);
//                ctx.save();
//              }
//            })