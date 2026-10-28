// @ts-ignore
import '../styles/Buttons.css'
import {Settings, CircleQuestionMark} from 'lucide-react'
import { FaGithub } from 'react-icons/fa';
import {useContext} from "react";
import {AppContext} from "../App.tsx";


function Header() {
    const {setInfo, setSettings} = useContext(AppContext)

  return (
      <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-100 dark:bg-gray-900/80 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">

            <div className="flex-shrink-0 flex items-center gap-2">
              <svg className="h-8 w-8 text-red-600 dark:text-red-400" xmlns="http://w3.org" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 21a9.004 9.004 0 008.716-6.747M12 21a9.004 9.004 0 01-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 2 12 2m0 19c-2.485 0-4.5-4.03-4.5-9s2.015-9 4.5-9yM12 2a8.997 8.997 0 017.843 4.582M12 2a8.997 8.997 0 00-7.843 4.582m15.686 0A11.953 11.953 0 0112 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0121 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0112 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 013 12c0-.778.099-1.533.284-2.253" />
              </svg>
              <span className="text-xl font-bold text-gray-900 dark:text-white tracking-tight">Name That Pitcher Game</span>
            </div>

            <div className="flex">
                <button className={"headerButton"} onClick={() => setInfo(true)}>
                    <CircleQuestionMark size={25}/>
                </button>
                <a className={"headerButton"} href={"https://colinherbs13.github.io"} target="_blank" rel="noopener noreferrer">
                    <FaGithub size={25}/>
                </a>
                <button className={"headerButton"} onClick={() => setSettings(true)}>
                    <Settings size={25}/>
                </button>
            </div>
          </div>
        </div>
      </header>
  )
};

export default Header;