import {useContext} from 'react';
import {AppContext} from "../../App.tsx";

const SettingsWindow = () => {
    const {settings, setSettings} = useContext(AppContext);
    return (
      <div id={"backdrop"} hidden={!settings}>
          <div id={"window"}>
              <button onClick={() => setSettings(false)}>X</button>
              <span></span>
          </div>
      </div>
    )
}

export default SettingsWindow