import "../styles/Buttons.css";
import "../styles/GameUI.css";
import React, {createContext, useEffect, useState} from 'react';
import Scoreboard from './game-components/Scoreboard.tsx';
import StrikeZone from './game-components/StrikeZone.tsx';
import HintBlock from './game-components/HintBlock.tsx';
import InputForm from './game-components/InputForm.tsx';
import GameOver from './game-components/GameOver.tsx';
import {getAllPitchers, type Pitcher} from "./api/api.tsx";

const hintTranslations = {
        jersey: "Jersey #",
        team: "Team",
        division: "Division",
        age: "Age",
        birthplace: "Birthplace",
        position: "SP/RP"
    }

interface GameContextType {
    pitcher: Pitcher;
    setPitcher: React.Dispatch<React.SetStateAction<Pitcher>>;
    strikes: number;
    addStrike: React.Dispatch<React.SetStateAction<number>>;
    score: number;
    addScore: React.Dispatch<React.SetStateAction<number>>;
    highScore: number;
    setHighScore: React.Dispatch<React.SetStateAction<number>>;
    hints: number[];
    revealHint: React.Dispatch<React.SetStateAction<number[]>>;
    newGame: boolean;
    setNewGame: React.Dispatch<React.SetStateAction<boolean>>;
}
export const GameContext = createContext<GameContextType>({} as GameContextType);

const Game = () => {
    const [pitcherNames, setPitcherNames] = useState<string[]>([]);
    const [pitcher, setPitcher] = useState<Pitcher>({
        age: "",
        birthplace: "",
        division: "",
        handedness: "",
        id: 0,
        jersey_number: "",
        name: "",
        position: "",
        team: ""
    });
    const [strikes, addStrike] = useState(0);
    const [score, addScore] = useState(0);
    const [highScore, setHighScore] = useState(0);
    const [hints, revealHint] = useState([0, 0, 0, 0, 0, 0])
    const [newGame, setNewGame] = useState(true);

    const gameState = {
        pitcher, setPitcher,
        strikes, addStrike,
        score, addScore,
        highScore, setHighScore,
        hints, revealHint,
        newGame, setNewGame
    }

    let hintElements = []
    let hintCount = 0;
    for (const[key, value] of Object.entries(hintTranslations)){
        hintElements.push(<HintBlock hintId={hintCount - 1} hint={hintTranslations[key as keyof typeof hintTranslations]} answer={value}></HintBlock>)
        hintCount++;
    };

    useEffect(() => {
        const getPitchers = async () => {
          try {
            const data = await getAllPitchers();
            console.log(data)
            setPitcherNames(data['pitchers'].map(p => p.name))
            setPitcher(data['pitchers'][Math.floor(Math.random() * data['pitchers'].length)])
            return data;
          } catch (err) {
              console.error(err);
          }
        };
        getPitchers().then(() => console.log("ANSWER: " + pitcher.name));

        if (!newGame) return;
        if (score > highScore) {
            setHighScore(score);
        }
        addScore(0);
        addStrike(0);
        setNewGame(false);
    }, [newGame]);

  return (
      <div id={"game"}>
        <GameContext.Provider value={gameState}>
            <Scoreboard></Scoreboard>
            <InputForm player={pitcher} namesList={pitcherNames}></InputForm>
            <div className={"game"}>
                <StrikeZone></StrikeZone>
                <div id={"hints"}>
                    {hintElements}
                </div>
            </div>
            <GameOver></GameOver>
        </GameContext.Provider>
      </div>

  )
}

export default Game