import '../styles/InfoPopup.css'
import {useContext} from 'react';
import {AppContext} from "../App.tsx";

const InfoPopup = () => {
    const {info, setInfo} = useContext(AppContext);
    return (
      <div id={"backdrop"} hidden={!info}>
          <div id={"infoWindow"}>
              <button id={"closeButton"} onClick={() => setInfo(false)}>X</button>
              <span></span>
              <span>Name That Pitcher</span>
          </div>
      </div>
    )
}

export default InfoPopup