import React from "react";

import Feed from "./Feed";
import './Board.css'

class Board extends React.Component {

  render() {
    const feedData = this.props.feedData
    const postsData = this.props.postsData

    return (
      <div className="board board-3">
        <Feed postsData={postsData} feedData={feedData} />
        <Feed postsData={postsData} feedData={feedData} />
        <Feed postsData={postsData} feedData={feedData} />
      </div>
    );
  }
}

export default Board