import * as d3 from "d3";
import {useEffect, useRef, useState} from "react";
import PitchInfo from "./PitchInfo.tsx";

const StrikeZone = () => {
  const [showPitchDetails, setShowPitchDetails] = useState([false, {}, ""]);
  const ref = useRef(null);

  interface Pitch {
    type: string,
    location: {
      x: number,
      y: number
    },
    spin: number,
    velocity: number,
    zone: {
      top: number,
      bottom: number
    }
  }

  function spinPitch(id: string, x: number, y: number){
    d3.select(`#${id}`)
      .transition()
      .duration(2000)
      .ease(d3.easeLinear)
      .attrTween("transform", function() {
        return d3.interpolateString(`rotate(0, ${x}, ${y})`, `rotate(360, ${x}, ${y})`);
      })
      .on("end", () => spinPitch(id, x, y));
  }

  function createPitches(svg: any, pitches: Pitch[], handedness: string) {
    if (pitches.length == 0) return;

    const colors: Record<string, string> = {
      "4-Seam Fastball": "#D22D49",
      "Sinker": "#FE9800",
      "Curveball": "#00D1ED",
      "Knuckle Curve": "#6236CD",
      "Sweeper": "#DDB33A",
      "Slider": "#C3BD0E",
      "Slurve": "#8a8c04",
      "Changeup": "#1DBE3A",
      "Knuckleball": "#3C44CD",
      "Split Finger": "#3BACAC",
      "Cutter": "#933F2C",
      "Forkball": "#55CCAB",
      "Eephus": "#cf34eb",
      "Gyroball": "#f257cb",
      "Screwball": "#2ab89e"
    }

    let pitch = pitches[0];

    const zone_width_ratio = 150 / 0.71,
          zone_center_x = 250;

    let id = `pitch-${pitch.type.replaceAll(" ", "")}`
    let x_start = 0, y_start = 15;
    if (handedness == "right") {
      x_start = 130;
    } else {
      x_start = 370;
    }

    let x_end = (pitch.location.x * (zone_width_ratio)) + zone_center_x,
        y_end = (75 + ((pitch.zone.top - pitch.location.y)/(pitch.zone.top - pitch.zone.bottom)) * 350)
    svg.append("circle")
      .attr("id", id)
      .attr("cx", x_start)
      .attr("cy", y_start)
      .attr("r", 8)
      .attr("fill", "url(#image-pattern)")
      .attr("stroke", colors[pitch.type])
      .attr("stroke-width", 4)
      .on("click", () => {setShowPitchDetails([true, pitch, colors[pitch.type]])})
      .transition()
        .duration(60000 / (pitch.velocity * 1.467)) // Velocity in seconds
        .attr("cx", x_end)
        .attr("cy", y_end)
        .attr("r", 25)
        .on("end", () => {spinPitch(id, x_end, y_end); createPitches(svg, pitches.slice(1), handedness)})

  }

  useEffect(() => {
    // @ts-ignore
    if (ref.current.querySelector('svg')){
      return
    }

    // set the dimensions and margins of the graph
    const width = 500,
      height = 500,
      zone_width = 300,
      zone_height = 350,
      x_coord = 100,
      y_coord = 75;

    // append the svg object to the body of the page
    const svg = d3
      .select(ref.current)
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")

    svg.append("rect")
        .attr("id", "strikezone")
        .attr("x", x_coord)          // Horizontal position of the top-left corner
        .attr("y", y_coord)          // Vertical position of the top-left corner
        .attr("width", zone_width)     // Width of the box
        .attr("height", zone_height)    // Height of the box
        .attr("fill", "#16171d") // Background color of the box
        .attr("stroke", "white") // Border color
        .attr("stroke-width", 2);// Border thickness

    // partitions of the strikezone
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

    // Add a defs element and the pattern
    const defs = svg.append("defs");

    defs.append("pattern")
      .attr("id", "image-pattern")
      .attr("width", 1)
      .attr("height", 1)
      .attr("patternUnits", "objectBoundingBox")
      .attr("patternContentUnits", "objectBoundingBox")
    .append("image")
      .attr("href", "/static/baseball-18872.png")
      .attr("width", 1)
      .attr("height", 1)
      .attr("preserveAspectRatio", "xMidYMid slice")
      .attr("x", 0)
      .attr("y", 0);

    let pitches: Pitch[] = [
      {
        "type": "4-Seam Fastball",
        "location": {
          "x": 0,
          "y": 1.8
        },
        "spin": 1974.2525773195875,
        "velocity": 95.89782330345722,
        "zone": {
          "top": 3.3980855067927687,
          "bottom": 1.6057147738210702
        }
      },
      {
        "type": "Curveball",
        "location": {
          "x": 0.5,
          "y": 2.6
        },
        "spin": 3000.2525773195875,
        "velocity": 75.89782330345722,
        "zone": {
          "top": 3.3980855067927687,
          "bottom": 1.6057147738210702
        }
      }
    ]
    createPitches(svg, pitches, "left");

    // Standard layout of a pitch displayed on chart (change onclick event to when previous pitch is triggered)


    // for (const pitch in pitches) {
    //   svg.node().appendChild(pitch.node())
    // }

  }, []);

  return (<>
    <svg width={500} height={500} id="s" ref={ref}/>
    <PitchInfo isOpen={showPitchDetails[0]} pitch={showPitchDetails[1]} color={showPitchDetails[2]} onClose={() => setShowPitchDetails([false, {}, ""])}/></>);
};

export default StrikeZone