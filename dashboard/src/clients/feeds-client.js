import {client} from "./api-client";

function listFeeds() {
  return client("feeds");
}

export {listFeeds}