$chart = $("#expenses_chart")
data = $chart.data "chart_data"

if not data.length
    return

$.each data, (i, el) ->
    el.color = window.main.colors[i]

$.plot $chart, data,
    series:
        pie:
            show: true
            innerRadius: .25
            combine:
                color: window.main.color_names_to_colors["gray"]
                threshold: .025
            label:
                show: true
                formatter: (label, series) ->
                    """
                    <div class="chart_label">
                        #{label}<br>
                        #{Math.round series.percent}%
                    </div>
                    """
                background:
                    color: "black"
                    opacity: .75
    legend:
        show: false
