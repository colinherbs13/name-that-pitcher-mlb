import ReactFlipCard from "reactjs-flip-card";
import '../../styles/GameUI.css'

function HintBlock(props: { hint: string; answer: string; }) {
    const styles = {
        size: {width: '60px', height: '60px'},
        front: {background: 'blue', color: 'white', borderRadius: 10, display: 'flex', alignItems: 'center', fontSize: 14, justifyContent: 'center'},
        back: {background: 'blue', color: 'white', borderRadius: 10, display: 'flex', alignItems: 'center', fontSize: 14, justifyContent: 'center'},
    }

    return (
        <ReactFlipCard
            containerStyle={styles.size}
            frontStyle={styles.front}
            backStyle={styles.back}
            frontComponent={<div className={"hintFront"}>{props.hint}</div>}
            backComponent={<div className={"hintBack"}>{props.answer}</div>}
            flipTrigger={"onClick"}
        />
    );
}

export default HintBlock