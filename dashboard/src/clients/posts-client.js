import {client} from "./api-client";

function listLatestPostsByFeed(feed_id) {
  return client(`feeds/${feed_id}/posts?order_by=published_at.desc&limit=15`);
}

export {listLatestPostsByFeed}