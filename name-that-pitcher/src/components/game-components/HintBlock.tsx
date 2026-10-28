import ReactFlipCard from "reactjs-flip-card";
import '../../styles/GameUI.css'
import {type MouseEventHandler, useContext, useEffect, useState} from "react";
import {GameContext} from "../GameUI.tsx";

function HintBlock(props: { hintId: number; hint: string; answer: string; }) {
    const {hints, revealHint, newGame} = useContext(GameContext);
    const [flip, setFlip] = useState(false);
    const styles = {
        size: {width: '60px', height: '60px'},
        front: {background: '#3b5c51', color: 'white', border: '2px solid white', borderRadius: 10, display: 'flex', alignItems: 'center', fontSize: 14, justifyContent: 'center'},
        back: {background: '#3b5c51', color: 'white', border: '2px solid white', borderRadius: 10, display: 'flex', alignItems: 'center', fontSize: 14, justifyContent: 'center'},
    }

    // Reset on New Game
    useEffect(() => {
        setFlip(false);
         revealHint((prev) => {
            prev[props["hintId"]] = 0;
            return prev
        });
    }, [newGame]);

    const flipHint: MouseEventHandler<HTMLInputElement> | undefined = () => {
      revealHint((prev) => {
          prev[props["hintId"]] = 1;
          return prev
      });
      if (hints[props["hintId"]] == 1) {
          setFlip(true);
      }
    }

    return (
        <ReactFlipCard
            containerStyle={styles.size}
            frontStyle={styles.front}
            backStyle={styles.back}
            frontComponent={<div className={"hintFront"}>{props.hint}</div>}
            backComponent={<div className={"hintBack"}>{props.answer}</div>}
            onClick={flipHint}
            flipTrigger={"disabled"}
            flipByProp={flip}
        />
    );
}

export default HintBlock