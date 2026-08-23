import * as d3 from "d3";
import { useEffect, useRef } from "react";

const StrikeZone = () => {
  const ref = useRef(null);

  useEffect(() => {
    // set the dimensions and margins of the graph
    const width = 400,
      height = 400,
      zone_width = 300,
      zone_height = 350,
      x_coord = 50,
      y_coord = 20;

    // append the svg object to the body of the page
    const svg = d3
      .select(ref.current)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")

    svg.append("rect")
        .attr("x", x_coord)          // Horizontal position of the top-left corner
        .attr("y", y_coord)          // Vertical position of the top-left corner
        .attr("width", zone_width)     // Width of the box
        .attr("height", zone_height)    // Height of the box
        .attr("fill", "#16171d") // Background color of the box
        .attr("stroke", "white") // Border color
        .attr("stroke-width", 2);// Border thickness

    for (let j = 0; j < 3; j++){
      for (let i = 0; i < 3; i++){
        svg.append("rect")
          .attr("x", x_coord + (i * (zone_width / 3)))          // Horizontal position of the top-left corner
          .attr("y", y_coord + (j * (zone_height / 3)))          // Vertical position of the top-left corner
          .attr("width", zone_width / 3)     // Width of the box
          .attr("height", zone_height / 3)    // Height of the box
          .attr("fill", "#16171d") // Background color of the box
          .attr("stroke", "white") // Border color
          .attr("stroke-width", 2)// Border thickness
          .attr("opacity", 0.5); // border opacity
      }
    }



  }, []);

  return <svg width={400} height={400} id="strikezone" ref={ref} />;
};

export default StrikeZone