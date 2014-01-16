$graph = $("#burndown_graph")
data = $graph.data "graph_data"
graph = new Rickshaw.Graph
    element: $graph.get(0)
    renderer: "line"
    height: 400
    interpolation: "basis"
    padding:
        left: 0.05
        right: 0.05
        top: 0.05
        bottom: .05
    min: "auto"
    series: [
        {
            data: data["ideal"]
            color: window.main.colors["silver"]
        }
        {
            data: data["actual"]
            color: window.main.colors["blue"]
        }
    ]
new Rickshaw.Graph.Axis.Time graph: graph
new Rickshaw.Graph.Axis.Y
    graph: graph
graph.render()
