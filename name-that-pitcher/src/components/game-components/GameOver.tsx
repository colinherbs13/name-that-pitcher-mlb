import "../../styles/Buttons.css";
import "../../styles/GameUI.css";
import "../../styles/GameOver.css";
import React, {useContext} from 'react';
import {GameContext} from "../GameUI.tsx";

const GameOver = () => {
    const {pitcher, strikes, score,  setNewGame} = useContext(GameContext);

    const resetGame = () => {
        setNewGame(true);
        return;
    }

    return (
      <div id={"backdrop"} hidden={strikes < 3}>
          <div id={"window"}>
              <h3>Game Over!</h3>
              <span>Score: {score}</span>
              <span>The Correct Answer was: {pitcher.name}</span>
              <button onClick={resetGame}>Play Again</button>
          </div>
      </div>
    )
}

export default GameOver