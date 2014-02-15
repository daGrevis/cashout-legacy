$chart = $("#frequency_chart")
data = $chart.data "chart_data"

if not data.length
    return

$.each data, (i, el) ->
    el.color = window.main.colors[i]

$.plot $chart, data,
    series:
        bars:
            show: true
            barWidth: .9
            align: "center"
            lineWidth: 0
            fill: 1
    grid:
        borderWidth: 0
        labelMargin: 20
    xaxis:
        mode: "categories"
        tickLength: 0
    yaxis:
        tickFormatter: (n) -> "#{n}×"
