$(document).ready(function () {

    // alert(sp);
    $.ajax({
        url: '/web/query_zz/',
        type: 'POST',
        data: {'sp': $("#sp").val()},
        // dataType: 'JSON',
        // contentType: 'application/json;charset=utf-8',
        success: function (result) {
            draw_dushujie(result[0]);


        }

    });


    $("#sp").change(function () {
        $.ajax({
            url: '/web/query_zz/',
            type: 'POST',
            data: {'sp': $("#sp").val()},
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
                data: data['dataP'][0],
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
            // {
            //     name: '覆盖率',
            //     type: 'line',
            //     data: data['dataP'][0],
            //     itemStyle: {
            //         normal: {
            //             color: '#EA7500'
            //         }
            //     }
            // }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}


