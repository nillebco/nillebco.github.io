# add comments to your blog with BlueSky and ATProto [HTMX component]

Tags: ATProto, BlueSky, HTMX, comments
Publish Date: January 6, 2025

I have recently switched my personal website to [HTMX](https://htmx.org/).

And I am a loving BlueSky user. A few weeks ago I have added to the reading list a blog post from Emily Liu, and I've decided to translate this to (my) reality, today.

The result is a small htmx component, that you can integrate in any site (vanilla, server side rendering, …)

Easy to integrate (kind of static):

```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>

/* [...] */

<div
  id="bluesky-comments"
  data-bsky-uri="at://FIXME_BLUESKY_DID/app.bsky.feed.post/FIXME_BLUESKY_POSTID"
  hx-get="https://nilleb.com/components/bluesky-comments.html"
  hx-trigger="load"
></div>
```

Or slightly more dynamically (assuming that you fetch the post data somewhere)

```html
<div id="bluesky-comments"></div>

<script>
window.BLUESKY_DID = 'did:plc:FIXME'
document.addEventListener('DOMContentLoaded', () => {
    // load post
    const commentsDiv = document.getElementById('bluesky-comments');
    commentsDiv.setAttribute('data-bsky-uri', `at://${window.BLUESKY_DID}/app.bsky.feed.post/${post.bskyId}`);
    commentsDiv.setAttribute('hx-get', '../../components/bluesky-comments.html');
    commentsDiv.setAttribute('hx-trigger', 'load');
    htmx.process(commentsDiv);
});
</script>
```

You still have to

- retrieve your DID (you could visit your bluesky profile or any of your tweets with your network tools open and filter on "profile”; the string after %3A is your DID), or just execute this code in your Console

```jsx
 JSON.parse(localStorage.BSKY_STORAGE).session.currentAccount.did
```

- create a post (tweet) in bluesky and retrieve its ID; this time it's easier to retrieve since it's the last part of the URL

![image.png](add%20comments%20to%20your%20blog%20through%20BlueSky%20and%20ATPr%20173023b4857680afa362d2fda9cca8b5/image.png)

## Reference

For convenience, all the sources I used to implement the component and my blog

- [HTMX](https://htmx.org/)
- [Emily Liu Blog Post](https://emilyliu.me/blog/comments)
- [Emily Liu's gist](https://gist.github.com/emilyliu7321/19ac4e111588bdc0cb4e411c88d9c79a)
- [The component](https://nilleb.com/components/bluesky-comments.html) source code

##