window.onload = function() {

new Chart(document.getElementById("line-chart"), {
  type: 'line',
  data: {
    labels:     line_labels = year,
    datasets: [{
            data: equity,
        label: "Equity",
        borderColor: "#1f497d",
        fill: false
      }, {
        data: appreciation,
        label: "Home Value",
        borderColor: "#c6d9f1",
        fill: false
      }, {
        data: loan,
        label: "Loan Balance",
        borderColor: "#fdeada",
        fill: false
      },
    ]
  },
  options: {

  legend: {position: 'bottom'},
    title: {
      display: false,
      fontSize: 24,
      text: '3 Year Trend'
    },
    scales: {
        yAxes: [
            {
                ticks: {
                    callback: function(label, index, labels) {
                        return label/1000 +'k';
                    }
                }
            }
        ]
    }
  }
  })



new Chart(document.getElementById("bar-chart"), {
  type: 'bar',
  data: {
    labels:     line_labels = bar_year,
    datasets: [{
            data: bar_rent,
        label: "Cash Flow",
        backgroundColor: "#1f497d",
        fill: true
      }
    ]
  },
  options: {

  legend: {position: 'bottom'},
    title: {
      display: false,
      fontSize: 24
          },
    scales: {
        yAxes: [
            {
                ticks: {
                beginAtZero:true,
                    stepSize: 1000,
                    callback: function(label, index, labels) {
                        return label/1000 +'k';
                    }
                }
            }
        ]
    }
  }
  })

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
                                isNumberShown: true,

                                legend: {
                                responsive:true,
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

        if (chart.config.options.isNumberShown) {

                var text = '$' + pie_cf,
                    textX = Math.round((width - ctx.measureText(text).width) / 2),
                    textY = (height / 2)-12;

                ctx.fillText(text, textX, textY);
                }
                ctx.save();

              }

            })





};
