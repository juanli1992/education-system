$(document).ready(function () {

    // alert(sp);
    $.ajax({
        url: '/web/query_xy/',
        type: 'POST',
        data: {'sp': $("#sp").val()},
        // dataType: 'JSON',
        // contentType: 'application/json;charset=utf-8',
        success: function (result) {
            draw_yuwen(result[0]);
            draw_shuxue(result[0]);
            draw_yingyu(result[0]);

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
                draw_yuwen(result[0]);
                draw_shuxue(result[0]);
                draw_yingyu(result[0]);

            }

        });
    });
});


//语文
function draw_yuwen(data) {
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

//数学
function draw_shuxue(data) {
    var myChart = echarts.init(document.getElementById('chart-grade-shuxue'));
    // alert('here');
    option = {
        title: {
            text: '各年级学生数学区考情况图',
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
                data: data['dataP'][3],
                itemStyle: {
                    normal: {
                        color: '#4f9D9D'
                    }
                }
            },
            {
                name: '及格率',
                type: 'line',
                data: data['dataP'][2],
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

//英语
function draw_yingyu(data) {
    var myChart = echarts.init(document.getElementById('chart-grade-yingyu'));
    // alert('here');
    option = {
        title: {
            text: '各年级学生数学区考情况图',
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
                data: data['dataP'][5],
                itemStyle: {
                    normal: {
                        color: '#4f9D9D'
                    }
                }
            },
            {
                name: '及格率',
                type: 'line',
                data: data['dataP'][4],
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
