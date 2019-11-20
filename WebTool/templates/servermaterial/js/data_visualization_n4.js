$(document).ready(function () {

    // alert(sp);
    $.ajax({
        url: '/web/query_zz/',
        type: 'POST',
        data: {'grade__': $("#grade__").val()},
        // dataType: 'JSON',
        // contentType: 'application/json;charset=utf-8',
        success: function (result) {
            draw_dushujie(result[0]);


        }

    });


    $("#grade__").change(function () {
        $.ajax({
            url: '/web/query_zz/',
            type: 'POST',
            data: {'grade__': $("#grade__").val()},
            // dataType: 'JSON',
            // contentType: 'application/json;charset=utf-8',
            success: function (result) {
                draw_dushujie(result[0]);


            }

        });
    });



});




//图书节开展情况
function draw_dushujie(data) {
    var myChart = echarts.init(document.getElementById('chart-exp-dushujie'));
    // alert('here');
    option = {
        title: {
            text: '各年级学生读书节开展情况情况图',
            x: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                    color: '#999'
                }
            }
        },
        toolbox: {
            feature: {
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        legend: {
            data: ['参与率', '覆盖率'],
            y: 'bottom'
        },
        xAxis: [
            {
                type: 'category',
                data: data['grade'][0],
                axisPointer: {
                    type: 'shadow'
                },
                axisLabel: {
                    interval: 0,
                    rotate: 40
                }
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '比率'
                // interval: ,
            }
        ],
        series: [
            {
                name: '参与率',
                type: 'line',
                data: data['dataP'][1],
                itemStyle: {
                    normal: {
                        color: '#4f9D9D'
                    }
                }
            },
            {
                name: '覆盖率',
                type: 'line',
                data: data['dataP'][0],
                itemStyle: {
                    normal: {
                        color: '#EA7500'
                    }
                }
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


//数学成绩分布
function draw_sxfb(dat) {
    var myChart = echarts.init(document.getElementById('chart-grade-sxfb'));

    option = {
        title: {
            text: '数学期末考试成绩分布图',
            x: 'center'
        },
        toolbox: {
            feature: {
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['bar','line']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                    color: '#999'
                }
            }
        },
        xAxis: {
            type: 'category',
            data: ['<60', '60-65', '65-70', '70-75', '75-80', '80-85', '85-90', '90-95','95-100']
        },
        yAxis: {
            type: 'value',
            name: '人数'
        },
        series: [{
            data: dat['dataPs'][1],
            type: 'bar'
        }]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


//英语成绩分布
function draw_yyfb(dat) {
    var myChart = echarts.init(document.getElementById('chart-grade-yyfb'));

    option = {
        title: {
            text: '英语期末考试成绩分布图',
            x: 'center'
        },
        toolbox: {
            feature: {
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['bar','line']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                    color: '#999'
                }
            }
        },
        xAxis: {
            type: 'category',
            data: ['<60', '60-65', '65-70', '70-75', '75-80', '80-85', '85-90', '90-95','95-100']
        },
        yAxis: {
            type: 'value',
            name: '人数'
        },
        series: [{
            data: dat['dataPs'][2],
            type: 'bar'
        }]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}