
                    
                    document.addEventListener("DOMContentLoaded", function() {
                    

                    var salesMonth = JSON.parse('{{ sales_month|safe}}');
                    console.log(salesMonth);
                    var month_labels = [];
                    var month_data = [];
                    for (var i = 0; i < salesMonth.length; i++) {
                        var date = new Date(salesMonth[i].year, salesMonth[i].month - 1);  
                        var monthYear = date.toLocaleString('en-US', { month: 'long',}); 
                        month_labels.push(monthYear);
                        month_data.push(salesMonth[i].total_revenue);
                        // labels.push(salesData[i].year + '-' + salesData[i].month);
                        // data.push(salesData[i].total_revenue);
                    }
                    console.log(month_labels);
                    console.log(month_data);
                    var canvas = document.getElementById('monthly_sale');
                    console.log(canvas);
                    var ctx=canvas.getContext('2d');
                    console.log(ctx);
                    var chart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: month_labels,
                            datasets: [{
                                label: 'month Sales',
                                data: month_data,
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                borderColor: 'rgba(55, 142, 182, 1)',
                                borderWidth: 1
                            }]
                        },
                        options: {
                            scales: {
                                yAxes:[{

                                        ticks:{
                                                beginAtZero: true
                                            }

                                        }]
                            }
                        }
                    });
                    var salesYear = JSON.parse('{{ sales_year|safe}}');
                    console.log(salesYear);
                    var year_labels = [];
                    var year_data = [];
                    for (var i = 0; i < salesYear.length; i++) {
                        var year = salesYear[i].year; 
                        var totalRevenue = salesYear[i].total_revenue; 
                        year_labels.push(year); 
                        year_data.push(totalRevenue); 
                    }

                    var ctx = document.getElementById('sales_year').getContext('2d');
                    var chart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: year_labels,
                            datasets: [{
                                label: 'Yearly Sales',
                                data: year_data,
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                borderColor: 'rgba(55, 142, 182, 1)',
                                borderWidth: 1
                            }]
                        },
                        options: {
                            scales: {
                                yAxes:[{
                                    ticks:{
                                        beginAtZero: true
                                    }
                                }]
                            }
                        }
                    });
               

                    var salesWeak = JSON.parse('{{ sales_weak|safe}}');
                    // console.log(salesData);
                    var weak_labels = [];
                    var weak_data = [];
                    for (var i = 0; i < salesWeak.length; i++) {
                        var date = new Date(salesWeak[i].date);
                            var day = date.toLocaleString('en-US', { weekday: 'long' });  
                            console.log(day);
                            var month = date.toLocaleString('en-US', { month: 'long' });  
                            var year = date.getFullYear();  
                            var formattedDate = day + ' ' + month + ' ' + year;
                            weak_labels.push(formattedDate);  
                            weak_data.push(salesWeak[i].total_revenue);
                    }
                    // console.log(labels);
                    // console.log(data);

                    var ctx = document.getElementById('sales_weak').getContext('2d');
                    var chart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: weak_labels,
                            datasets: [{
                                label: 'current weak Sales',
                                data: weak_data,
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                borderColor: 'rgba(55, 142, 182, 1)',
                                borderWidth: 1
                            }]
                        },
                        options: {
                            scales: {
                                yAxes:[{

                                    ticks:{
                                            beginAtZero: true
                                    }

                                }]
                            }
                        }
                    });
                    
                    
                    var salesToday = JSON.parse('{{ sales_today|safe}}');
                    // console.log(salesData);
                    var today_labels = [];
                    var today_data = [];
                    for (var i = 0; i < salesToday.length; i++) {
                        var date = new Date(salesToday[i].date);
                            var day = date.toLocaleString('en-US', { weekday: 'long' });  
                            var month = date.toLocaleString('en-US', { month: 'long' });  
                            var year = date.getFullYear();  
                            var formattedDate = day + ' ' + month + ' ' + year;
                            today_labels.push(formattedDate);  
                            today_data.push(salesToday[i].total_revenue);
                    }
                    // console.log(labels);
                    // console.log(data);

                    var ctx = document.getElementById('sales_today').getContext('2d');
                    var chart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: today_labels,
                            datasets: [{
                                label: 'Today Sales',
                                data: today_data,
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                borderColor: 'rgba(55, 142, 182, 1)',
                                borderWidth: 1
                            }]
                        },
                        options: {
                            scales: {
                                yAxes:[{

                                    ticks:{
                                                beginAtZero: true
                                        }

                                    }]
                            }
                        }
                    });


                    var salesCmonth = JSON.parse('{{ sales_cmonth|safe}}');
                    var clabels = [];
                    var cdata = [];
                    for (var i = 0; i < salesCmonth.length; i++) {
                        var dateParts = salesCmonth[i].date.split(' '); 
                        var day = parseInt(dateParts[1]); 
                        console.log(day)

                        var date = new Date(salesCmonth[i].date);
                        // var day = date.toLocaleString('en-US', { weekday: 'long' });
                        // console.log(day);  
                        // var month = date.toLocaleString('en-US', { month: 'long' });  
                        // var year = date.getFullYear();  
                        // var formattedDate = day + ' ' + month + ' ' + year;
                        var formattedDate=day
                        clabels.push(formattedDate);  
                        cdata.push(salesCmonth[i].total_revenue);
                        // console.log(clabels);
                        // console.log(formattedDate);  
                    }
                    var ctx = document.getElementById('sales_day').getContext('2d');
                    var chart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: clabels,
                            datasets: [{
                                label: 'Daily Sales',
                                data: cdata,
                                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                                borderColor: 'rgba(55, 142, 182, 1)',
                                borderWidth: 1
                            }]
                        },
                        options: {
                            scales: {
                                yAxes:[{

                                        ticks:{
                                                beginAtZero: true
                                            }

                                    }],

                                xAxes:[{

                                    ticks:{
                                            beginAtZero: true
                                             }

                                }]
                            }
                        }
                    });

                }); 