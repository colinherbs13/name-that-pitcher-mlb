import '../../styles/GameUI.css'

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

function PitchInfo(props: { isOpen: boolean, pitch: Pitch, color: string }) {
    let pitch = props.pitch;
    return (
        <div id="pitchDetails"
             style={{border: `1px solid ${props.color}`}}
             hidden={!props.isOpen}>
            <ul>Type: {pitch.type}</ul>
            <ul>Avg. Velocity: {Math.round(pitch.velocity * 100) / 100}</ul>
            <ul>Avg. Spin: {Math.round(pitch.spin)}</ul>
        </div>
    );
}

export default PitchInfo