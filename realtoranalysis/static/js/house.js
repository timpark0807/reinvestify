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
                    min: 0,
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

};
