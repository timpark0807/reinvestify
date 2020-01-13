$(document).ready(function(){

    $("#next-1").click(function() {

        $("#step1").hide();
        $("#stepicon1").removeClass('active');
        $("#stepicon1").addClass('disabled');


        $("#step2").show();
        $("#stepicon2").removeClass('disabled');
        $("#stepicon2").addClass('active');

    });

    $("#next-2").click(function() {
        $("#step2").hide();
        $("#stepicon2").removeClass('active');
        $("#stepicon2").addClass('disabled');


        $("#step3").show();
        $("#stepicon3").removeClass('disabled');
        $("#stepicon3").addClass('active');

    });

    $("#prev-2").click(function() {
        $("#step2").hide();
        $("#stepicon2").removeClass('active');
        $("#stepicon2").addClass('disabled');


        $("#step1").show();
        $("#stepicon1").removeClass('disabled');
        $("#stepicon1").addClass('active');

    });


    $("#next-3").click(function() {
        $("#step3").hide();
        $("#stepicon3").removeClass('active');
        $("#stepicon3").addClass('disabled');


        $("#step4").show();
        $("#stepicon4").removeClass('disabled');
        $("#stepicon4").addClass('active');

    });

    $("#prev-3").click(function() {
        $("#step3").hide();
        $("#stepicon3").removeClass('active');
        $("#stepicon3").addClass('disabled');


        $("#step2").show();
        $("#stepicon2").removeClass('disabled');
        $("#stepicon2").addClass('active');

    });

    $("#next-4").click(function() {
        $("#step4").hide();
        $("#stepicon4").removeClass('active');
        $("#stepicon4").addClass('disabled');


        $("#step5").show();
        $("#stepicon5").removeClass('disabled');
        $("#stepicon5").addClass('active');

    });

    $("#prev-4").click(function() {
        $("#step4").hide();
        $("#stepicon4").removeClass('active');
        $("#stepicon4").addClass('disabled');


        $("#step3").show();
        $("#stepicon3").removeClass('disabled');
        $("#stepicon3").addClass('active');

    });


});

