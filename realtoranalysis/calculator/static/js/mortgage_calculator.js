$(document).ready(function(){


// This loads a doughnut chart when you open the page
         var chartx = new Chart(document.getElementById("bar-chart"), {
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
                                legend: {
                                        responsive:true,
                                        maintainAspectRatio: false,
                                        display: true,

                                      position: 'bottom',
                                      align: 'middle',
                                      padding:20,
                                      labels:{fontSize: 15}
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

                var text = '$619',
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
                price : $('#price').val(),
                down_payment : $('#down_payment').val(),
                term : $('#term').val(),
                interest_rate : $('#interest_rate').val(),
                property_tax : $('#property_tax').val(),
                insurance : $('#insurance').val()
            },
            type : 'POST',
            url : '/mortgage_calculator/process'
        })
        .done(function(data) {

        $("canvas#bar-chart").remove();
        $("div.holder").append('<canvas id="bar-chart" ></canvas>');

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
                            legend: { responsive:true,
                                    maintainAspectRatio: false,
                                    display: true,
                                      position: 'bottom',
                                      align: 'middle',
                                      padding:20,
                                      labels:{fontSize: 15}
                                      }
                                      ,

                             title: {
                              display: false,
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

                ctx.clearRect(0, 0, chart.width, chart.height);

                ctx.fillText(text, textX, textY);
                ctx.save();

              }

            })

        });

        event.preventDefault();

   });

});
