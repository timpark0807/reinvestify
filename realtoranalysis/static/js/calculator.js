$(document).ready(function() {


    $('form').on('submit', function(event) {

        $.ajax({
            data : {
                price : $('#price_id').val(),
                down_payment : $('#down_payment_id').val(),
                term : $('#term_id').val(),
                interest_rate : $('#interest_rate_id').val(),
                property_tax : $('#property_tax_id').val(),
                insurance : $('#insurance_id').val()
            },
            type : 'POST',
            url : '/process'
        })

        .done(function(data) {

          $('#mortgage_payment_output').text(data.mortgage_payment).show;
          $('#down_payment_output').text(data.down_payment).show;


        });

        event.preventDefault();


    });


});
