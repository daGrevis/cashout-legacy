PERCENTAGE_OF_CRITICAL_BALANCE = 20

$chart = $("#burndown_chart")
data = $chart.data "chart_data"

critical_balance = (data.start_balance / 100) * PERCENTAGE_OF_CRITICAL_BALANCE

data = [
    {
        data: data.ideal,
        color: window.main.color_names_to_colors["silver"]
    }
    {
        data: data.actual,
        color: window.main.color_names_to_colors["blue"]
    }
]

$.plot $chart, data,
    shadowSize: 0
    grid:
        borderWidth: 0
        labelMargin: 20
        markings: [
            color: "#FFC0B5" # Red, lightened by 50%.
            yaxis: { from: critical_balance, to: critical_balance }
        ]
    xaxis:
        mode: "time"
        timeformat: "%m/%d"
    yaxis:
        tickFormatter: (n) -> "#{n} €"  # TODO: Hardcoded euro-sign.
