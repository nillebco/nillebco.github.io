# README

## publish a new post

- export the post (Markdown/CSV)
- generate a slug from the file name
- add a record in the posts.json file
- run generate_rss.py
- publish the site (using ./cli push)
- create a new BlueSky post, get the post ID
- update posts.json with the bskyId
- publish again
