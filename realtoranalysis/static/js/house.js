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
                        return label/1000+'k';
                    }
                }
            }
        ]
    }
  }
  })
};
