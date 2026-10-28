import "../../styles/GameUI.css"
import {useState, type MouseEventHandler, useContext, useEffect} from 'react';
import {GameContext} from "../GameUI.tsx";

export default function InputForm(props: {player: any, namesList: string[]}) {
    const [inputVal, setInputVal] = useState('');
    const [suggestions, setSuggestions] = useState([]);
    const {score, addScore, strikes, addStrike, hints, newGame} = useContext(GameContext);
    const [canSubmit, enableSubmit] = useState(false);

    // Reset on new game
    useEffect(() => {
        if (!newGame) return;
        setInputVal("");
    }, [newGame]);

    const setEnableSubmit = (name: string)=> {
        if (props.namesList.includes(name)) {
            enableSubmit(true);
        }
        else {
            enableSubmit(false);
        }
    }

    const handleChange = (e: any) => {
        const value = e.target.value;
        setInputVal(value);

        if (value.trim() === '') {
          setSuggestions([]);
          return;
        }

        const filtered = props.namesList.filter(name =>
          name.toLowerCase().split(" ")[0].substring(0, value.length) == value.toLowerCase(0).trim()
            || name.toLowerCase().split(" ")[1].substring(0, value.length) == value.toLowerCase(0).trim()
            || name.toLowerCase().split(" ").at(-1).substring(0, value.length) == value.toLowerCase(0).trim()
            || name.toLowerCase().substring(0, value.length) == value.toLowerCase(0).trim()
        );
        setSuggestions([...filtered].sort((a, b) => a.split(" ").at(-1).localeCompare(b.split(" ").at(-1))));

        setEnableSubmit(value);
    };

    const handleSelect = (name: string) => {
        setInputVal(name);
        setEnableSubmit(name);
        setSuggestions([])
    };

    const calculateHintScore = () => {
        let hintsUsed = 0;
        for (let i = 0; i < hints.length; i++){
            if (hints[i] == 1) {
                hintsUsed++;
            }
        }
        return 6 - hintsUsed;
    }

    const makeGuess = (e: any) => {
        e.preventDefault();
        if (!canSubmit) return;
        if (inputVal == props.player.name) {
            addScore((prev: number) => prev + calculateHintScore());
            alert("Correct! Score: " + score);
            addStrike(0);
        }
        else {
            addStrike((prev: number) => {
                if (strikes <= 3) {
                   return prev + 1;
                } else return prev;
            })
        }
    }

    return (
        <form id={"inputForm"} onSubmit={makeGuess}>
          <input
            name={"playerGuess"}
            type="text"
            value={inputVal}
            onBlur={() => {
                    setSuggestions([]);
            }}
            onChange={handleChange}
            autoComplete={"off"}
            placeholder="Guess"
          />
          {suggestions.length > 0 && inputVal && (
            <ul>
              {suggestions.map((name, index) => (
                <li
                  key={index}
                  onMouseDown={() => handleSelect(name)}
                  style={{ padding: '8px', cursor: 'pointer'}}
                >
                  {name}
                </li>
              ))}
            </ul>
          )}
          <input type="submit" hidden />
        </form>
    );
}