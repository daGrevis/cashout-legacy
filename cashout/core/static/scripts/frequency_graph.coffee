$graph = $("#frequency_graph")
data = $graph.data "graph_data"
series = []
$.each data, (i, el) ->
    series.push
        color: ($.map window.main.colors, (value, key) -> value)[i]
        name: "“#{el[0]}“ (#{el[1]})"
        data: [x: 0, y: el[1]]
graph = new Rickshaw.Graph
    element: $graph.get(0)
    unstack: true
    height: 400
    renderer: "bar"
    series: series
new Rickshaw.Graph.Legend
    graph: graph
    element: $("#frequency_legend").get(0)
    naturalOrder: true
graph.render()
