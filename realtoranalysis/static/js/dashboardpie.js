$(document).ready(function(){


// This loads a doughnut chart when you open the page
         chartx = new Chart(document.getElementById("bar-chart"), {
                      type: 'doughnut',
                         data: {
                               labels: ["Cashflow", "Mortgage", "Expenses"],
                               datasets: [
                               {
                                backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
                                data: [  pie_cashflow, pie_expenses, pie_mortgage]
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


});

