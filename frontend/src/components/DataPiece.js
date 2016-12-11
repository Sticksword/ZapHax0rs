import React from 'react';

class DataPiece extends React.Component {



  render() {
    const item = this.props.item;
    return (
      <div>
        <strong>Text:</strong> {item.text}
        <br />
        <strong>Score:</strong> {item.documentSentiment.score}
        <br />
        <strong>Magnitude:</strong> {item.documentSentiment.magnitude}</div>
    );
  }
}

export default DataPiece;
