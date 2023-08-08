var maxWidth = window.innerWidth;
var padding = 100;
var width = window.innerWidth - padding;
var height = 700;

var svg = d3.select("#chart-container").append("svg")
    .attr("width", width)
    .attr("height", height);

var g = svg.append("g");

var legendG = svg.append("g")
    .attr("transform", "translate(10, 10)");

legendG.append("circle")
    .attr("cx", 20)
    .attr("cy", 30)
    .attr("r", 6)
    .style("fill", "green");

legendG.append("text")
    .attr("x", 30)
    .attr("y", 30)
    .text("ASSET MANAGERS")
    .style("font-size", "15px")
    .attr("alignment-baseline", "middle");

legendG.append("circle")
    .attr("cx", 20)
    .attr("cy", 60)
    .attr("r", 6)
    .style("fill", "pink")

legendG.append("text")
    .attr("x", 30)
    .attr("y", 60)
    .text("INVESTMENTS")
    .style("font-size", "15px")
    .attr("alignment-baseline", "middle");

var zoom = d3.zoom()
    .scaleExtent([-5, 10])
    .on("zoom", zoomed);

svg.call(zoom);

function zoomed({ transform }) {
    g.attr("transform", transform);
    legendG.attr("transform", `translate(${10 / transform.k}, ${10 / transform.k})`);
}

d3.json("jsonnetworks/graph.json").then(function (graph) {
    var simulation = d3.forceSimulation(graph.nodes)
        .force("link", d3.forceLink(graph.links).id(function (d) { return d.id; }).distance(80))
        .force("charge", d3.forceManyBody().strength(-300))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("x", d3.forceX(width / 2).strength(0.1))
        .force("y", d3.forceY(height / 2).strength(0.1));

    var link = g.selectAll("line")
        .data(graph.links)
        .enter().append("line")
        .attr("stroke", "#999")
        .attr("stroke-opacity", 0.6);

    let investmentMap = new Map();
    let investmentCount = new Map();
    let investorMap = new Map();

    graph.links.forEach(link => {
        if (investmentMap.has(link.source.id)) {
            investmentMap.get(link.source.id).push(link.target.id);
        } else {
            investmentMap.set(link.source.id, [link.target.id]);
        }

        investmentCount.set(link.target.id, (investmentCount.get(link.target.id) || 0) + 1);

        if (investorMap.has(link.target.id)) {
            investorMap.get(link.target.id).push(link.source.id);
        } else {
            investorMap.set(link.target.id, [link.source.id]);
        }
    });

    var node = g.selectAll("circle")
        .data(graph.nodes)
        .enter().append("circle")
        .on("mouseover", function (d) {
            d3.select(this).style("cursor", "pointer");
        })
        .on("mouseout", function (d) {
            d3.select(this).style("cursor", "default");
        })
        .attr("r", function (d) {
            let baseRadius = 5;
            let additionalRadius = (investmentCount.get(d.id) || 0) * 7.5;
            if (d.color === "green") {
                return 15;
            } else {
                return baseRadius + additionalRadius;
            }
        })
        .attr("fill", function (d) {
            if (d.color === "green") {
                return "green";
            } else {
                return "pink";
            }
        })
        .attr("stroke", function (d) {
            if (d.color === "pink") {
                return "black";
            } else {
                return "transparent";
            }
        })
        .attr("stroke-width", 5);


    var tooltip = d3.select("body").append("div")
        .attr("class", "tooltip")
        .style("opacity", 0)

    var clickedNode = null;

    node.on("click", function (event, d) {
        event.stopPropagation();

        if (clickedNode) {
            d3.select(clickedNode).attr("stroke", "transparent");
        }

        d3.select(this).attr("stroke", "black");

        clickedNode = this;

        var [x, y] = d3.pointer(event, this);
        tooltip.transition()
            .duration(200)
            .style("opacity", .9);

        let tooltipText = `<strong>Name of Company:</strong> ${d.id}`;

        if (d.color === "green" && investmentMap.has(d.id)) {
            let investedCompanies = investmentMap.get(d.id).join(", ");
            tooltipText += `<br/><strong>Companies that ${d.id} is invested in:</strong> ${investedCompanies}`;
        }

        if (d.color !== "green" && investorMap.has(d.id)) {
            let investingCompanies = investorMap.get(d.id).join(", ");
            tooltipText += `<br/><strong>Companies that invest in ${d.id}:</strong> ${investingCompanies}`;
        }

        tooltip.html(tooltipText)
            .style("left", x + "px")
            .style("top", (y - 28) + "px");
    });

    document.addEventListener("click", function () {
        if (clickedNode) {
            d3.select(clickedNode).attr("stroke", "transparent");
            clickedNode = null;
        }
    });

    svg.on("click", function () {
        tooltip.transition()
            .duration(500)
            .style("opacity", 0);
    });

    simulation.on("tick", function () {
        link
            .attr("x1", function (d) { return d.source.x; })
            .attr("y1", function (d) { return d.source.y; })
            .attr("x2", function (d) { return d.target.x; })
            .attr("y2", function (d) { return d.target.y; });

        node
            .attr("cx", function (d) { return d.x; })
            .attr("cy", function (d) { return d.y; });
    });
});
