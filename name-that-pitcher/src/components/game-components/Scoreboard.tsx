import "../../styles/Scoreboard.css";
import {useContext, useEffect} from "react";
import {GameContext} from '../GameUI.tsx';

function HighScore() {
    const {highScore} = useContext(GameContext)
    return (
        <>
            <div className={"scoreRow"}>
                <span className={"label"}>HIGH SCORE: </span>
                <span className={"label"}>{highScore}</span>
            </div>
        </>
    )
}

function Score() {
    const {score} = useContext(GameContext);
    return (
        <div className={"scoreRow"}>
            <span className={"label"}>SCORE: </span>
            <span className={"label"}>{score}</span>
        </div>
    )
}

function StrikeCounter() {
    const {strikes} = useContext(GameContext);

    useEffect(() => {
        // Update Strikes
        const strikeLights = document.querySelectorAll('#strikes-lights .light');
        strikeLights.forEach((light, index) => {
            if (index < strikes) {
                light.classList.add('active');
            } else {
                light.classList.remove('active');
            }
        });
    }, [strikes]);

    return(<div className={"scoreRow"}>
            <span className={"label"}>STRIKES</span>
            <div className={"lights"} id="strikes-lights">
                <div className={"light strike"}></div>
                <div className={"light strike"}></div>
            </div>
        </div>)
}

function Scoreboard() {
    return(<div className={"scoreboard"}><HighScore></HighScore>
    <StrikeCounter></StrikeCounter>
        <Score></Score></div>);
}

export default Scoreboard