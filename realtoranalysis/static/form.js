$(document).ready(function() {

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

          $('#mortgage_payment_output').text(data.mortgage_payment).show;


        });

        event.preventDefault();

    });




//
//
//    new Chart(document.getElementById("mycanvas"), {
//                 type: 'doughnut',
//                  data: {
//                    labels: {{labels | tojson}},
//                    datasets: [{
//                      label: "Pie Chart",
//                      backgroundColor: {{colors | tojson}},
//                    data: {{values | tojson}}
//                    }]
//                  },
//                  options: {
//                    title: {
//                      display: true,
//                      text: 'Pie Chart Title'
//                    }
//                  }
//                });
//
//
//});
