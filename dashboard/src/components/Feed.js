import moment from "moment";
import React from "react";

import './Feed.css'

class Feed extends React.Component {

  state = {
    postsData: [],
  }

  fetchData = () => {
    const { feedData } = this.props;
    fetch(`http://localhost:8080/api/feeds/${feedData.id}/posts?limit=15`)
      .then(res => res.json())
      .then(data => this.setState({ postsData: data }))
      .catch(console.log);
  }

  calculateLastUpdate = () => {
    const { postsData } = this.state;
    const lastPostAt = new Date(
      Math.max(...postsData.map(post => new Date(post.published_at)))
    );
    return moment(lastPostAt).fromNow();
  }

  componentDidMount() {
    this.fetchData();
  }

  render() {
    const { feedData } = this.props;
    const { postsData }  = this.state;
    const lastPostAt = this.calculateLastUpdate();
    return (
      <div className="feed">
        <FeedHeader feedData={feedData} lastPostAt={lastPostAt} />
        <FeedBody postsData={postsData} />
      </div>
    )
  }

}

const FeedHeader = (props) => {
  const { feedData } = props;
  const { lastPostAt } = props;

  const feedUrl = (new URL(feedData.url)).origin;
  const iconUrl = new URL("/favicon.ico", feedUrl);

  return (
    <div className="feed-header">
      <img src={iconUrl} alt={feedData.name} />
      <a href={feedUrl} target="_blank" rel="noopener noreferrer nofollow">
        {feedData.name}
      </a>
      <br/>
      <small>
        Last post {lastPostAt}
      </small>
    </div>
  )
}

const FeedBody = (props) => {
  const { postsData } = props;
  const rows = postsData.map((post, index) => {
    return <FeedPost key={index} postData={post} />
  });
  return (
    <div className="feed-body">
      {rows}
    </div>
  )
}

const FeedPost = (props) => {
  const { postData } = props;
  return (
    <div className="post">
      <a href={postData.url} target="_blank" rel="noopener noreferrer nofollow">
        {postData.title}
      </a>
    </div>
  )
}

export default Feed