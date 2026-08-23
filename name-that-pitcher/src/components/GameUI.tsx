import "../styles/Buttons.css";
import "../styles/GameUI.css";
import React, { createContext, useState} from 'react';
import HighScore from './game-components/HighScore.tsx'
import StrikeCounter from './game-components/StrikeCounter.tsx'
import StrikeZone from './game-components/StrikeZone.tsx'
import HintBlock from './game-components/HintBlock.tsx'
import InputForm from './game-components/InputForm.tsx'

const hintTranslations = {
        jersey: "Jersey #",
        team: "Team",
        division: "Division",
        age: "Age",
        birthplace: "Birthplace",
        position: "SP/RP"
    }

interface GameContextType {
    strikes: number;
    addStrike: React.Dispatch<React.SetStateAction<number>>;
}
export const GameContext = createContext<GameContextType>({} as GameContextType);

const Game = () => {
    const [strikes, addStrike] = useState(0);
    const gameState = {
        strikes, addStrike
    }

    let player = {
        jersey: "45",
        team: "Phillies",
        division: "NL East",
        age: "37",
        birthplace: "United States",
        position: "SP"
    }

    let hintElements = []
    for (const[key, value] of Object.entries(player)){
        hintElements.push(<HintBlock hint={hintTranslations[key as keyof typeof hintTranslations]} answer={value}></HintBlock>)
    };
  return (
      <div>
        <GameContext.Provider value={gameState}>
          <div className={"gameStats"}>
            <HighScore></HighScore>
            <StrikeCounter></StrikeCounter>
            <button className="giveUp">Give Up</button>
          </div>
          <div className={"game"}>
            <StrikeZone></StrikeZone>
            <div id={"hints"}>
                {hintElements}
            </div>
          </div>
          <InputForm></InputForm>
        </GameContext.Provider>
      </div>

  )
}

export default Game