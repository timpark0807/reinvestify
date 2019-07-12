$(document).ready(function(){

    chartx = new Chart(document.getElementById("pie-chart"), {
                      type: 'doughnut',
                         data: {
                               labels: [ "Expenses", "Loan Amortization", "Net Profit"],
                               datasets: [
                               {
                                backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
                                data: [ pie_oe, pie_ma, pie_cf]
                               }
                               ]
                               },
                         options: {
                                legend: { responsive:true,
                                    maintainAspectRatio: false,
                                    display: true,
                                          position: 'bottom'
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

                var text = '$' + pie_cf,
                    textX = Math.round((width - ctx.measureText(text).width) / 2),
                    textY = (height / 2)-12;

                ctx.clearRect(0, 0, chart.width, chart.height);

                ctx.fillText(text, textX, textY);
                ctx.save();

              }
              })




};