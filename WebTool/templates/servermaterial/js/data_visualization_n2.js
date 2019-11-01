$(document).ready(function () {

    // alert(sp);
    $.ajax({
        url: '/web/query_xy/',
        type: 'POST',
        data: {'sp': $("#sp").val(), 'grade__': $("#grade__").val()},
        // dataType: 'JSON',
        // contentType: 'application/json;charset=utf-8',
        success: function (result) {
            draw_yuwen(result[0]);
            draw_shuxue(result[0]);
            draw_yingyu(result[0]);
            draw_ywfb(result[1]);

        }

    });

    $("#sp").change(function () {
        $.ajax({
            url: '/web/query_xy/',
            type: 'POST',
            data: {'sp': $("#sp").val(), 'grade__': $("#grade__").val()},
            // dataType: 'JSON',
            // contentType: 'application/json;charset=utf-8',
            success: function (result) {
                draw_yuwen(result[0]);
                draw_shuxue(result[0]);
                draw_yingyu(result[0]);
                draw_ywfb(result[1]);

            }

        });
    });

    $("#grade__").change(function () {
        $.ajax({
            url: '/web/query_xy/',
            type: 'POST',
            data: {'sp': $("#sp").val(), 'grade__': $("#grade__").val()},
            // dataType: 'JSON',
            // contentType: 'application/json;charset=utf-8',
            success: function (result) {
                draw_yuwen(result[0]);
                draw_shuxue(result[0]);
                draw_yingyu(result[0]);
                draw_ywfb(result[1]);

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
                data: data['grade'][1],
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
                data: data['grade'][2],
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


//语文成绩分布
function draw_ywfb(dat) {
    var myChart = echarts.init(document.getElementById('chart-grade-ywfb'));
    var girth = dat['dataPs'][0];

    // See https://github.com/ecomfe/echarts-stat
    var bins = ecStat.histogram(girth);

    var interval;
    var min = Infinity;
    var max = -Infinity;

    data = echarts.util.map(bins.data, function (item, index) {
        var x0 = bins.bins[index].x0;
        var x1 = bins.bins[index].x1;
        interval = x1 - x0;
        min = Math.min(min, x0);
        max = Math.max(max, x1);
        return [x0, x1, item[1]];
    });

    function renderItem(params, api) {
        var yValue = api.value(2);
        var start = api.coord([api.value(0), yValue]);
        var size = api.size([api.value(1) - api.value(0), yValue]);
        var style = api.style();

        return {
            type: 'rect',
            shape: {
                x: start[0] + 1,
                y: start[1],
                width: size[0] - 2,
                height: size[1]
            },
            style: style
        };
    }

    option = {
        title: {
            text: 'Girths of Black Cherry Trees',
            sublink: 'https://github.com/ecomfe/echarts-stat',
            left: 'center',
            top: 10
        },
        color: ['rgb(25, 183, 207)'],
        grid: {
            top: 80,
            containLabel: true
        },
        xAxis: [{
            type: 'value',
            min: min,
            max: max,
            interval: interval
        }],
        yAxis: [{
            type: 'value',
        }],
        series: [{
            name: 'height',
            type: 'custom',
            renderItem: renderItem,
            label: {
                normal: {
                    show: true,
                    position: 'insideTop'
                }
            },
            encode: {
                x: [0, 1],
                y: 2,
                tooltip: 2,
                label: 2
            },
            data: data
        }]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}