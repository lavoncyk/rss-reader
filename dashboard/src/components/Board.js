import React from "react";

import Feed from "./Feed";
import './Board.css'

class Board extends React.Component {

  state = {
    feedsData: [],
  }

  fetchData = () => {
    fetch(`http://localhost:8080/api/feeds`)
      .then(res => res.json())
      .then(data => this.setState({ feedsData: data }))
      .catch(console.log);
  }

  componentDidMount() {
    this.fetchData();
  }

  render() {
    const { feedsData } = this.state;
    const feeds = feedsData.map((feed, index) => {
      return <Feed key={index} feedData={feed} />
    });
    return (
      <div className="board board-3">
        {feeds}
      </div>
    );
  }

}

export default Board