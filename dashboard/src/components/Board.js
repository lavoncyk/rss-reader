import React from "react";

import {listFeeds} from "../clients/feeds-client";
import Feed from "./Feed";
import './Board.css';

class Board extends React.Component {

  state = {
    feedsData: [],
  }

  fetchData = () => {
    listFeeds()
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