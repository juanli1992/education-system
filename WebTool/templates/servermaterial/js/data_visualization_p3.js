$(document).ready(function () {

    // alert(sp);
    $.ajax({
        url: '/web/query_course/',
        type: 'POST',
        data: {'sp': $("#sp").val()},
        // dataType: 'JSON',
        // contentType: 'application/json;charset=utf-8',
        success: function (result) {
            draw_course_p1(result[0]);

            draw_comp_p1(result[1]);
            draw_comp_p2(result[2]);
            draw_comp_p3(result[3]);
            draw_comp_p4(result[4]);
        }

    });

    $("#sp").change(function () {
        $.ajax({
            url: '/web/query_hw/',
            type: 'POST',
            data: {'sp': $("#sp").val()},
            // dataType: 'JSON',
            // contentType: 'application/json;charset=utf-8',
            success: function (result) {

            }

        });
    });
});


function draw_course_p1(data) {
    var myChart = echarts.init(document.getElementById('chart-grade-30'));
    option = {
        title: {
            text: '兴趣课程开设数量图',
            x: 'center'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data: ["走班制", "整班制"]
        },
        toolbox: {
            show: true,
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {
                    show: true,
                    type: ['pie', 'funnel'],
                    option: {
                        funnel: {
                            x: '25%',
                            width: '50%',
                            funnelAlign: 'left',
                            max: 1548
                        }
                    }
                },
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        calculable: true,
        series: [
            {
                name: '兴趣课程开设数量图',
                type: 'pie',
                radius: '55%',
                center: ['50%', '60%'],
                data: [
                    {value: data['ratio'][0], name: "走班制"},
                    {value: data['ratio'][1], name: "整班制"},
                ]
            }
        ]
    };
    myChart.setOption(option);

    myChart = echarts.init(document.getElementById('chart-grade-31'));
    option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        legend: {
            data: ['走班制', '整班制']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value'
        },
        yAxis: {
            type: 'category',
            data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        },
        series: [
            {
                name: '走班制',
                type: 'bar',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'insideRight'
                    }
                },
                data: [320, 302, 301, 334, 390, 330, 320]
            },
            {
                name: '整班制',
                type: 'bar',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'insideRight'
                    }
                },
                data: [120, 132, 101, 134, 90, 230, 210]
            },
        ]
    };
    myChart.setOption(option);
}

function draw_comp_p1(data) {
    var myChart = echarts.init(document.getElementById('chart-grade-37'));
    option = {
        title: {
            text: '所有学生各类竞赛参与数量图',
            x: 'center'
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value'
        },
        yAxis: {
            type: 'category',
            data: data['all'][0]
        },
        series: [
            {
                name: '走班制',
                type: 'bar',
                stack: '总量',
                itemStyle: {
                    normal: {
                        color: '#ca8622'
                    }
                },
                label: {
                    normal: {
                        show: true,
                        position: 'insideRight'
                    }
                },
                data: data['all'][1]
            },
        ]
    };
    myChart.setOption(option);


    var tmp_dict = data['sp_dict']["1"];
    var primaryNode = $("<tr><td>小学</td><td>" + tmp_dict["技术类"] + "</td><td>" + tmp_dict["科学类"] + "</td><td>" + tmp_dict["社会类"] +
        "</td><td>" + tmp_dict["数学类"] + "</td><td>" + tmp_dict["体育类"] + "</td><td>" + tmp_dict["艺术类"] + "</td><td>" + tmp_dict["语言类"] +
        "</td><td>" + tmp_dict["综合实践类"] + "</td><td>" + data["all_sp_dict"]["1"] + "</td>></tr>");

    tmp_dict = data['sp_dict']["2"];
    var juniorNode = $("<tr><td>初中</td><td>" + tmp_dict["技术类"] + "</td><td>" + tmp_dict["科学类"] + "</td><td>" + tmp_dict["社会类"] +
        "</td><td>" + tmp_dict["数学类"] + "</td><td>" + tmp_dict["体育类"] + "</td><td>" + tmp_dict["艺术类"] + "</td><td>" + tmp_dict["语言类"] +
        "</td><td>" + tmp_dict["综合实践类"] + "</td><td>" + data["all_sp_dict"]["2"] + "</td>></tr>");
    var es_table = $("tbody[class='9999']");
    es_table.append(primaryNode);
    es_table.append(juniorNode);
}


function draw_comp_p2(data) {

    var myChart = echarts.init(document.getElementById('chart-grade-38'));

    option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        title: {
            text: '各类竞赛获奖情况图',
            x: 'center'
        },
        legend: {
            orient: 'vertical',
            x: 'left',
            data: ['个人获奖', '集体获奖']
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value'
        },
        yAxis: {
            type: 'category',
            data: data["all"][0]
        },
        series: [
            {
                name: '个人获奖',
                type: 'bar',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'insideRight'
                    }
                },
                data: data["all"][1]
            },
            {
                name: '集体获奖',
                type: 'bar',
                stack: '总量',
                label: {
                    normal: {
                        show: true,
                        position: 'insideRight'
                    }
                },
                data: data["all"][3]
            },
        ]
    };
    myChart.setOption(option);

    var tmp_dict = data['sp_type_dict']["1"];
    var primaryNode = $("<tr><td class=\"text-center\" rowspan=\"2\" style=\"vertical-align: middle;\">小学</td><td>个人获奖</td><td>"
        + tmp_dict[1]["技术类"] + "</td><td>" + tmp_dict[1]["科学类"] + "</td><td>" + tmp_dict[1]["社会类"] + "</td><td>"
        + tmp_dict[1]["数学类"] + "</td><td>" + tmp_dict[1]["体育类"] + "</td><td>" + tmp_dict[1]["艺术类"] + "</td><td>"
        + tmp_dict[1]["语言类"] + "</td><td>" + tmp_dict[1]["综合实践类"] + "</td><td>" + data["all_st_dict"]["1"][1] +
        "</td></tr><tr><td>集体获奖</td><td>" + tmp_dict[2]["技术类"] + "</td><td>" + tmp_dict[2]["科学类"] + "</td><td>"
        + tmp_dict[2]["社会类"] + "</td><td>" + tmp_dict[2]["数学类"] + "</td><td>" + tmp_dict[2]["体育类"] + "</td><td>"
        + tmp_dict[2]["艺术类"] + "</td><td>" + tmp_dict[2]["语言类"] + "</td><td>" + tmp_dict[2]["综合实践类"] + "</td><td>"
        + data["all_st_dict"]["1"][2] + "</td>></tr>");

    tmp_dict = data['sp_type_dict']["2"];
    var juniorNode = $("<tr><td class=\"text-center\" rowspan=\"2\" style=\"vertical-align: middle;\">初中</td><td>个人获奖</td><td>"
        + tmp_dict[1]["技术类"] + "</td><td>" + tmp_dict[1]["科学类"] + "</td><td>" + tmp_dict[1]["社会类"] + "</td><td>"
        + tmp_dict[1]["数学类"] + "</td><td>" + tmp_dict[1]["体育类"] + "</td><td>" + tmp_dict[1]["艺术类"] + "</td><td>"
        + tmp_dict[1]["语言类"] + "</td><td>" + tmp_dict[1]["综合实践类"] + "</td><td>" + data["all_st_dict"]["1"][1] +
        "</td></tr><tr><td>集体获奖</td><td>" + tmp_dict[2]["技术类"] + "</td><td>" + tmp_dict[2]["科学类"] + "</td><td>"
        + tmp_dict[2]["社会类"] + "</td><td>" + tmp_dict[2]["数学类"] + "</td><td>" + tmp_dict[2]["体育类"] + "</td><td>"
        + tmp_dict[2]["艺术类"] + "</td><td>" + tmp_dict[2]["语言类"] + "</td><td>" + tmp_dict[2]["综合实践类"] + "</td><td>"
        + data["all_st_dict"]["1"][2] + "</td>></tr>");
    var es_table = $("tbody[class='8888']");
    es_table.append(primaryNode);
    es_table.append(juniorNode);
}

function draw_comp_p3(data) {
    var myChart = echarts.init(document.getElementById('chart-grade-39'));
    option = {
        title: {
            text: '各级别竞赛参与情况图',
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
        xAxis: [
            {
                type: 'category',
                data: ["区级", "市级", "国家级"],
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
                name: '总数',
                interval: 10,
            }
        ],
        series: [
            {
                name: '男生',
                type: 'bar',
                data: [data['all'][1], data['all'][2], data['all'][3]],
                itemStyle: {
                    normal: {
                        color: '#4f9D9D',
                    }
                }
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);

    var tableNode = "<tr><td>小学</td><td>2018</td><td>" + data["sp_dict"]["1"][1] + "</td><td>" + data["sp_dict"]["1"][2] + "</td><td>"
        + data["sp_dict"]["1"][3] + "</td></tr><tr><td>初中</td><td>2018</td><td>" + data["sp_dict"]["2"][1] + "</td><td>"
        + data["sp_dict"]["2"][2] + "</td><td>" + data["sp_dict"]["2"][3] + "</td></tr>";
    var es_table = $("tbody[class='7777']");
    es_table.append(tableNode);
}

function draw_comp_p4(data) {
    var myChart = echarts.init(document.getElementById('chart-grade-40'));
    option = {
        title: {
            text: '各级别竞赛参与情况图',
            x: 'center'
        },
        legend: {
            y: 'bottom',
            data: ['个人获奖', '集体获奖']
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
        xAxis: [
            {
                type: 'category',
                data: ["区级", "市级", "国家级"],
                axisPointer: {
                    type: 'shadow'
                },
            }
        ],
        yAxis: [
            {
                type: 'value',
                name: '总数',
                interval: 10,
            }
        ],
        series: [
            {
                name: '个人获奖',
                type: 'bar',
                data: [data['all'][1][1], data['all'][1][2], data['all'][1][3]],
                itemStyle: {
                    normal: {
                        color: '#4f9D9D',
                    }
                }
            },
            {
                name: '集体获奖',
                type: 'bar',
                data: [data['all'][2][1], data['all'][2][2], data['all'][2][3]],
                itemStyle: {
                    normal: {
                        color: '#EA7500',
                    }
                }
            }
        ]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);

    var tableNode = "<tr><td class=\"text-center\" rowspan=\"2\" style=\"vertical-align: middle;\">小学</td><td>个人获奖</td><td>"
        + data["sp_dict"]["1"][1][1] + "</td><td>" + data["sp_dict"]["1"][1][2] + "</td><td>" + data["sp_dict"]["1"][1][3] + "</td></tr>"
        + "<tr><td>集体获奖</td><td>" + data["sp_dict"]["1"][2][1] + "</td><td>" + data["sp_dict"]["1"][2][2] + "</td><td>" + data["sp_dict"]["1"][2][3]
        + "</td></tr><tr><td class=\"text-center\" rowspan=\"2\" style=\"vertical-align: middle;\">初中</td><td>个人获奖</td><td>" +
        +data["sp_dict"]["2"][1][1] + "</td><td>" + data["sp_dict"]["2"][1][2] + "</td><td>" + data["sp_dict"]["2"][1][3] + "</td></tr>"
        + "<tr><td>集体获奖</td><td>" + data["sp_dict"]["2"][2][1] + "</td><td>" + data["sp_dict"]["2"][2][2] + "</td><td>" + data["sp_dict"]["2"][2][3]
        + "</td></tr>";

    var es_table = $("tbody[class='6666']");
    es_table.append(tableNode);
}