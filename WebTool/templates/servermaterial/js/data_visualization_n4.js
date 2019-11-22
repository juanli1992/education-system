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
            draw_kejijie(result[0]);
            draw_tiyujie(result[0]);
            draw_yishujie(result[0]);
            draw_xiaoyunhui(result[0]);
            draw_qita(result[0]);


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
                draw_kejijie(result[0]);
                draw_tiyujie(result[0]);
                draw_yishujie(result[0]);
                draw_xiaoyunhui(result[0]);
                draw_qita(result[0]);


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
            {
                name: '覆盖率',
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

//科技节开展情况
function draw_kejijie(data) {
    var myChart = echarts.init(document.getElementById('chart-exp-kejijie'));
    // alert('here');
    option = {
        title: {
            text: '各年级学生科技节开展情况情况图',
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
                data: data['dataP'][3],
                itemStyle: {
                    normal: {
                        color: '#4f9D9D'
                    }
                }
            },
            {
                name: '覆盖率',
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

//体育节开展情况
function draw_tiyujie(data) {
    var myChart = echarts.init(document.getElementById('chart-exp-tiyujie'));
    // alert('here');
    option = {
        title: {
            text: '各年级学生体育节开展情况情况图',
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
                data: data['dataP'][5],
                itemStyle: {
                    normal: {
                        color: '#4f9D9D'
                    }
                }
            },
            {
                name: '覆盖率',
                type: 'line',
                data: data['dataP'][6],
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

//艺术节开展情况
function draw_yishujie(data) {
    var myChart = echarts.init(document.getElementById('chart-exp-yishujie'));
    // alert('here');
    option = {
        title: {
            text: '各年级学生艺术节开展情况情况图',
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
                data: data['dataP'][7],
                itemStyle: {
                    normal: {
                        color: '#4f9D9D'
                    }
                }
            },
            {
                name: '覆盖率',
                type: 'line',
                data: data['dataP'][8],
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

//校运会项目开设情况
function draw_xiaoyunhui(dat) {
    var myChart = echarts.init(document.getElementById('chart-exp-xiaoyunhui'));

    option = {
        title: {
            text: '校运会项目开设情况',
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
            data: ['短跑', '中长跑', '跨栏', '投掷', '跳跃', '接力']
        },
        yAxis: {
            type: 'value',
            name: '比率'
        },
        series: [{
            data: dat['dataH'],
            type: 'bar'
        }]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

//其他主题活动开展情况图
function draw_qita(dat) {
    var myChart = echarts.init(document.getElementById('chart-exp-qita'));

    option = {
        title: {
            text: '其他主题活动开展情况图'
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
                type: 'shadow'
            }
        },
        legend: {
            data: ['参与率', '覆盖率']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            boundaryGap: [0, 0.01]
        },
        yAxis: {
            type: 'category',
            data: ['特色活动','节庆及仪式活动','其他活动']
        },
        series: [
            {
                name: '参与率',
                type: 'bar',
                data: dat['dataoOther'][0]
            },
            {
                name: '覆盖率',
                type: 'bar',
                data: dat['dataoOther'][1]
            }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

