import './App.css'
import Header from './components/Header.tsx'
import Game from './components/GameUI.tsx'

function App() {

  return (
    <>
      <Header highscore={1}></Header>
      <Game></Game>
    </>
  )
}

export default App
