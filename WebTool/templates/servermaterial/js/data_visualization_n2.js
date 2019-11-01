$(document).ready(function () {

    // alert(sp);
    $.ajax({
        url: '/web/query_xy/',
        type: 'POST',
        data: {'sp': $("#sp").val()},
        // dataType: 'JSON',
        // contentType: 'application/json;charset=utf-8',
        success: function (result) {
            draw_avg_height(result[0]);
            draw_std_height(result[0]);
            draw_avg_weight(result[0]);
            draw_std_weight(result[0]);
            draw_bmi(result[0]);
            draw_vision_level(result[2]);
            draw_tooth_level(result[3]);
        }

    });

    $("#sp").change(function () {
        $.ajax({
            url: '/web/query_xy/',
            type: 'POST',
            data: {'sp': $("#sp").val()},
            // dataType: 'JSON',
            // contentType: 'application/json;charset=utf-8',
            success: function (result) {
                draw_avg_height(result[0]);
                draw_std_height(result[0]);
                draw_avg_weight(result[0]);
                draw_std_weight(result[0]);
                draw_bmi(result[0])
            }

        });
    });
});


function draw_avg_height(data) {
    var myChart = echarts.init(document.getElementById('chart-grade-yuwen'));
    // alert('here');
    option = {
        title: {
            text: '各年级学生语文区考情况图',
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
            data: ['优秀率', '及格率'],
            y: 'bottom'
        },
        xAxis: [
            {
                type: 'category',
                data: data['grade'],
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
                name: '优秀率',
                type: 'line',
                data: data['dataP'][1],
                itemStyle: {
                    normal: {
                        color: '#4f9D9D'
                    }
                }
            },
            {
                name: '及格率',
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

