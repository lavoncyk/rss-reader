import _ from "lodash";
import React from "react";

import {listFeeds} from "../clients/feeds-client";
import Category from "./Category";
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
    const groupedFeedsData = _(feedsData)
      .groupBy('category.slug')
      .map(g => ({...g[0].category, feeds: g}))
      .value();

    const categories = groupedFeedsData.map((categoryData, index) => {
      return <Category key={index} categoryData={categoryData} />
    });

    return (
      <div className="board">
        {categories}
      </div>
    );
  }

}

export default Board