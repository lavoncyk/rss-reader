import React from "react";

import Feed from "./Feed";
import './Category.css';

const CategoryHeader = (props) => {
  const { categoryData } = props;
  return (
    <div className="category-header">
      {categoryData.name}
    </div>
  )
}

class Category extends React.Component {

  render() {
    const { categoryData } = this.props;
    const feeds = categoryData.feeds.map((feedData, index) => {
      return <Feed key={index} feedData={feedData} />
    });
    return (
      <div className="category">
        <CategoryHeader categoryData={categoryData} />
        <div className="category-body category-body-3">
          {feeds}
        </div>
      </div>
    );
  }

}

export default Category