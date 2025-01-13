# README

## publish a new post

- synchronize notion posts (./cli sync)
  - export the post (Markdown/CSV)
  - generate a slug from the file name
  - add a record in the posts.json file
- run generate_rss.py (./cli rss)
- create a new BlueSky post, get the post ID (./cli tweet slug)
- update posts.json with the bskyId
- publish the site (./cli push)
