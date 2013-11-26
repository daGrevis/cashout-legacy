burndown_graph = new Rickshaw.Graph
    element: $("#burndown_graph").get(0)
    renderer: "line"
    series: [
        data: [
            { x: 0, y: 40 }
            { x: 1, y: 49 }
        ]
        color: "steelblue"
    ]

burndown_graph.render()
