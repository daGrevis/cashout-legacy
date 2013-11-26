$graph = $("#burndown_graph")
data = $graph.data "graph_data"
graph = new Rickshaw.Graph
    element: $graph.get(0)
    renderer: "line"
    series: [
        {
            data: data["spent"]
            color: "steelblue"
        }
        {
            data: data["available"]
            color: "lightblue"
        }
    ]
Rickshaw.Graph.Axis.Time graph: graph
graph.render()
