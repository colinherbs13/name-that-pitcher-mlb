import {useContext} from "react";
import {GameContext} from '../GameUI.tsx'

function StrikeCounter() {
    const {strikes, addStrike} = useContext(GameContext);
    return(<button onClick={() => addStrike((prev: number) => prev + 1)}>Strikes: {strikes}</button>)
}

export default StrikeCounter