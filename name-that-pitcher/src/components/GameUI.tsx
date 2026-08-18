function StrikeZone() {
    return (
        <div>
            BOX
        </div>
    )
}

function InputForm() {
    return (
        <div>
            <input type={"text"}></input>
            <button>Guess</button>
        </div>
    )
}


const Game = () => {
  return (
    <>
      <StrikeZone></StrikeZone>
      <InputForm></InputForm>
    </>
  )
}

export default Game