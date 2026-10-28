import './App.css'
import Header from './components/Header.tsx'
import Game from './components/GameUI.tsx'
import InfoPopup from './components/InfoPopup.tsx'
import SettingsWindow from "./components/game-components/SettingsWindow.tsx";
import React, {createContext, useState} from 'react';

interface AppContextType {
    info: boolean,
    setInfo: React.Dispatch<React.SetStateAction<boolean>>;
    settings: boolean,
    setSettings: React.Dispatch<React.SetStateAction<boolean>>;
}
export const AppContext = createContext<AppContextType>({} as AppContextType);

function App() {
    const [info, setInfo] = useState(false);
    const [settings, setSettings] = useState(false);
    const appState = {
      info, setInfo, settings, setSettings
    }
    return (
        <AppContext.Provider value={appState}>
        <Header></Header>
        <Game></Game>
        <InfoPopup></InfoPopup>
        <SettingsWindow></SettingsWindow>
        </AppContext.Provider>
    )
}

export default App
