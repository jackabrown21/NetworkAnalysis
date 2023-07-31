var width = 800;
var height = 600;

var svg = d3.select("body").append("svg")
    .attr("width", width)
    .attr("height", height);

d3.json("jsonnetworks/graph.json").then(function(graph) {
    var simulation = d3.forceSimulation(graph.nodes)
        .force("link", d3.forceLink(graph.links).id(function(d) { return d.id; }))
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

    var link = svg.selectAll("line")
        .data(graph.links)
        .enter().append("line")
            .attr("stroke", "#999")
            .attr("stroke-opacity", 0.6);

    var node = svg.selectAll("circle")
        .data(graph.nodes)
        .enter().append("circle")
            .attr("r", 5)
            .attr("fill", "#69b3a2");

    simulation.on("tick", function() {
        link
            .attr("x1", function(d) { return d.source.x; })
            .attr("y1", function(d) { return d.source.y; })
            .attr("x2", function(d) { return d.target.x; })
            .attr("y2", function(d) { return d.target.y; });

        node
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
    });
});
