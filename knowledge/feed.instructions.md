---
description: Instructions for proper feed accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Feed Accessibility

## CRITICAL RULES

**Feeds present auto-loading scrollable lists of articles, like social media feeds or news streams.**

### 1. Use role="feed" with Accessible Label

**Feed containers MUST have `role="feed"` and an accessible label.**

```html
✅ Good - Feed with accessible label:
<div role="feed" aria-label="Recent articles">
  <article>...</article>
  <article>...</article>
</div>

✅ Good - Using aria-labelledby:
<h2 id="feed-title">Latest News</h2>
<div role="feed" aria-labelledby="feed-title">
  <article>...</article>
</div>

❌ Bad - Missing accessible label:
<div role="feed">  <!-- No label! -->
  <article>...</article>
</div>
```

### 2. Use role="article" with Position Information

**Feed items MUST use `role="article"` with `aria-posinset` and `aria-setsize`.**

```html
✅ Good - Articles with position info:
<div role="feed" aria-label="Posts" aria-busy="false">
  <article aria-posinset="1" aria-setsize="100">
    <h3>Post Title 1</h3>
    <p>Content...</p>
  </article>

  <article aria-posinset="2" aria-setsize="100">
    <h3>Post Title 2</h3>
    <p>Content...</p>
  </article>
</div>

❌ Bad - Missing position attributes:
<div role="feed" aria-label="Posts">
  <article>  <!-- Missing aria-posinset and aria-setsize! -->
    <h3>Post Title</h3>
  </article>
</div>
```

### 3. Each Article Needs Accessible Label and Description

**Articles MUST have `aria-labelledby` (title) and `aria-describedby` (summary).**

```html
✅ Good - Article with label and description:
<article
  aria-labelledby="article-1-title"
  aria-describedby="article-1-desc"
  aria-posinset="1"
  aria-setsize="50">
  <h3 id="article-1-title">Breaking News</h3>
  <p id="article-1-desc">Latest updates on the story...</p>
</article>

❌ Bad - Missing aria-labelledby/aria-describedby:
<article aria-posinset="1" aria-setsize="50">
  <h3>Breaking News</h3>  <!-- Not connected with aria-labelledby! -->
  <p>Latest updates...</p>
</article>
```

### 4. Implement Page Down/Page Up Navigation

**Required keyboard interactions:**
- **Page Down**: Load more articles and move focus to next article
- **Page Up**: Move focus to previous article
- **Ctrl+End**: Move focus out of feed (to next element after feed)
- **Ctrl+Home**: Move focus out of feed (to previous element before feed)

```javascript
feed.addEventListener('keydown', (e) => {
  const articles = Array.from(feed.querySelectorAll('article'));
  const currentArticle = document.activeElement.closest('article');
  const currentIndex = articles.indexOf(currentArticle);

  switch(true) {
    case e.key === 'PageDown':
      e.preventDefault();
      if (currentIndex < articles.length - 1) {
        focusArticle(articles[currentIndex + 1]);
      } else {
        // Load more articles
        loadMoreArticles().then(() => {
          const newArticles = feed.querySelectorAll('article');
          focusArticle(newArticles[currentIndex + 1]);
        });
      }
      break;

    case e.key === 'PageUp':
      e.preventDefault();
      if (currentIndex > 0) {
        focusArticle(articles[currentIndex - 1]);
      }
      break;

    case e.ctrlKey && e.key === 'End':
      e.preventDefault();
      const nextElement = feed.nextElementSibling;
      if (nextElement && nextElement.tabIndex >= 0) {
        nextElement.focus();
      }
      break;

    case e.ctrlKey && e.key === 'Home':
      e.preventDefault();
      const prevElement = feed.previousElementSibling;
      if (prevElement && prevElement.tabIndex >= 0) {
        prevElement.focus();
      }
      break;
  }
});

function focusArticle(article) {
  const focusableElement = article.querySelector('a, button, [tabindex="0"]');
  if (focusableElement) {
    focusableElement.focus();
  } else {
    article.tabIndex = -1;
    article.focus();
  }
}
```

### 5. Use aria-busy During Content Loading

**Set `aria-busy="true"` on feed while loading new articles.**

```html
✅ Good - Indicating busy state:
<!-- While loading -->
<div role="feed" aria-label="Posts" aria-busy="true">
  <article>...</article>
  <!-- Loading indicator -->
</div>

<!-- After loading -->
<div role="feed" aria-label="Posts" aria-busy="false">
  <article>...</article>
  <article>...</article>  <!-- New articles added -->
</div>
```

## Complete Feed Structure

```html
<h2 id="news-feed-label">News Feed</h2>

<div
  role="feed"
  aria-labelledby="news-feed-label"
  aria-busy="false"
  id="news-feed">

  <article
    aria-labelledby="article-1-title"
    aria-describedby="article-1-summary"
    aria-posinset="1"
    aria-setsize="50">
    <h3 id="article-1-title">
      <a href="/article/1">First Article Title</a>
    </h3>
    <p id="article-1-summary">
      This is a brief summary of the first article content...
    </p>
    <button>Like</button>
    <button>Share</button>
  </article>

  <article
    aria-labelledby="article-2-title"
    aria-describedby="article-2-summary"
    aria-posinset="2"
    aria-setsize="50">
    <h3 id="article-2-title">
      <a href="/article/2">Second Article Title</a>
    </h3>
    <p id="article-2-summary">
      This is a brief summary of the second article content...
    </p>
    <button>Like</button>
    <button>Share</button>
  </article>

  <article
    aria-labelledby="article-3-title"
    aria-describedby="article-3-summary"
    aria-posinset="3"
    aria-setsize="50">
    <h3 id="article-3-title">
      <a href="/article/3">Third Article Title</a>
    </h3>
    <p id="article-3-summary">
      This is a brief summary of the third article content...
    </p>
    <button>Like</button>
    <button>Share</button>
  </article>
</div>

<script>
const feed = document.getElementById('news-feed');
let currentArticleCount = 3;
const totalArticles = 50;

feed.addEventListener('keydown', (e) => {
  const articles = Array.from(feed.querySelectorAll('article'));
  const currentArticle = document.activeElement.closest('article');

  if (!currentArticle) return;

  const currentIndex = articles.indexOf(currentArticle);

  switch(true) {
    case e.key === 'PageDown':
      e.preventDefault();
      if (currentIndex < articles.length - 1) {
        // Move to next article
        focusArticle(articles[currentIndex + 1]);
      } else if (currentArticleCount < totalArticles) {
        // Load more articles
        loadMoreArticles();
      }
      break;

    case e.key === 'PageUp':
      e.preventDefault();
      if (currentIndex > 0) {
        focusArticle(articles[currentIndex - 1]);
      }
      break;

    case e.ctrlKey && e.key === 'End':
      e.preventDefault();
      exitFeedForward();
      break;

    case e.ctrlKey && e.key === 'Home':
      e.preventDefault();
      exitFeedBackward();
      break;
  }
});

function focusArticle(article) {
  const link = article.querySelector('h3 a');
  if (link) {
    link.focus();
  }
}

function loadMoreArticles() {
  feed.setAttribute('aria-busy', 'true');

  // Simulate async loading
  setTimeout(() => {
    const articlesToLoad = Math.min(3, totalArticles - currentArticleCount);

    for (let i = 0; i < articlesToLoad; i++) {
      currentArticleCount++;
      const article = createArticle(currentArticleCount, totalArticles);
      feed.appendChild(article);
    }

    feed.setAttribute('aria-busy', 'false');

    // Focus newly loaded article
    const newArticles = feed.querySelectorAll('article');
    focusArticle(newArticles[newArticles.length - articlesToLoad]);
  }, 500);
}

function createArticle(position, setSize) {
  const article = document.createElement('article');
  article.setAttribute('aria-posinset', position);
  article.setAttribute('aria-setsize', setSize);
  article.setAttribute('aria-labelledby', `article-${position}-title`);
  article.setAttribute('aria-describedby', `article-${position}-summary`);

  article.innerHTML = `
    <h3 id="article-${position}-title">
      <a href="/article/${position}">Article ${position} Title</a>
    </h3>
    <p id="article-${position}-summary">
      Summary of article ${position}...
    </p>
    <button>Like</button>
    <button>Share</button>
  `;

  return article;
}

function exitFeedForward() {
  const nextElement = feed.nextElementSibling;
  if (nextElement) {
    const focusable = nextElement.querySelector('a, button, [tabindex="0"]');
    if (focusable) {
      focusable.focus();
    } else if (nextElement.tabIndex >= 0) {
      nextElement.focus();
    }
  }
}

function exitFeedBackward() {
  const prevElement = feed.previousElementSibling;
  if (prevElement) {
    const focusable = prevElement.querySelector('a, button, [tabindex="0"]');
    if (focusable) {
      focusable.focus();
    } else if (prevElement.tabIndex >= 0) {
      prevElement.focus();
    }
  }
}
</script>
```

## Examples

### ✅ Good: Social Media Feed

```html
<h2 id="timeline-label">Your Timeline</h2>

<div role="feed" aria-labelledby="timeline-label" aria-busy="false">
  <article
    aria-labelledby="post-1-author"
    aria-describedby="post-1-content"
    aria-posinset="1"
    aria-setsize="200">
    <h3 id="post-1-author">
      <a href="/user/jane">Jane Smith</a>
    </h3>
    <p id="post-1-content">Just finished my morning run! 🏃‍♀️</p>
    <time datetime="2025-01-04T08:30:00">8:30 AM</time>
    <button>Like</button>
    <button>Comment</button>
  </article>

  <article
    aria-labelledby="post-2-author"
    aria-describedby="post-2-content"
    aria-posinset="2"
    aria-setsize="200">
    <h3 id="post-2-author">
      <a href="/user/john">John Doe</a>
    </h3>
    <p id="post-2-content">Check out my new blog post about accessibility!</p>
    <time datetime="2025-01-04T07:15:00">7:15 AM</time>
    <button>Like</button>
    <button>Comment</button>
  </article>
</div>
```

### ✅ Good: News Feed with Images

```html
<div role="feed" aria-label="Latest news" aria-busy="false">
  <article
    aria-labelledby="news-1-headline"
    aria-describedby="news-1-summary"
    aria-posinset="1"
    aria-setsize="100">
    <img src="news1.jpg" alt="Breaking news scene">
    <h3 id="news-1-headline">
      <a href="/news/1">Breaking: Major Development</a>
    </h3>
    <p id="news-1-summary">
      Officials announced today that...
    </p>
    <time datetime="2025-01-04T10:00:00">10:00 AM</time>
  </article>
</div>
```

### ✅ Good: React Feed Component

```jsx
function Feed({ articles, totalCount, onLoadMore }) {
  const feedRef = useRef(null);
  const [loading, setLoading] = useState(false);

  const handleKeyDown = (e) => {
    const articles = feedRef.current.querySelectorAll('article');
    const currentArticle = document.activeElement.closest('article');

    if (!currentArticle) return;

    const currentIndex = Array.from(articles).indexOf(currentArticle);

    switch(true) {
      case e.key === 'PageDown':
        e.preventDefault();
        if (currentIndex < articles.length - 1) {
          focusArticle(articles[currentIndex + 1]);
        } else {
          loadMore();
        }
        break;

      case e.key === 'PageUp':
        e.preventDefault();
        if (currentIndex > 0) {
          focusArticle(articles[currentIndex - 1]);
        }
        break;

      case e.ctrlKey && e.key === 'End':
        e.preventDefault();
        exitFeedForward();
        break;

      case e.ctrlKey && e.key === 'Home':
        e.preventDefault();
        exitFeedBackward();
        break;
    }
  };

  const focusArticle = (article) => {
    const link = article.querySelector('a');
    if (link) link.focus();
  };

  const loadMore = async () => {
    setLoading(true);
    await onLoadMore();
    setLoading(false);
  };

  return (
    <div
      role="feed"
      aria-label="News feed"
      aria-busy={loading}
      ref={feedRef}
      onKeyDown={handleKeyDown}>
      {articles.map((article, index) => (
        <article
          key={article.id}
          aria-labelledby={`article-${article.id}-title`}
          aria-describedby={`article-${article.id}-desc`}
          aria-posinset={index + 1}
          aria-setsize={totalCount}>
          <h3 id={`article-${article.id}-title`}>
            <a href={`/articles/${article.id}`}>{article.title}</a>
          </h3>
          <p id={`article-${article.id}-desc`}>{article.summary}</p>
          <button>Like</button>
          <button>Share</button>
        </article>
      ))}
      {loading && <div role="status">Loading more articles...</div>}
    </div>
  );
}
```

### ❌ Bad Examples

```html
<!-- Missing role="feed" -->
<div aria-label="Posts">
  <article>...</article>
</div>

<!-- Missing aria-posinset and aria-setsize -->
<div role="feed" aria-label="Posts">
  <article>
    <h3>Post Title</h3>
  </article>
</div>

<!-- Missing aria-labelledby and aria-describedby on articles -->
<div role="feed" aria-label="Posts">
  <article aria-posinset="1" aria-setsize="50">
    <h3>Post Title</h3>
    <p>Content...</p>
  </article>
</div>

<!-- Missing accessible label on feed -->
<div role="feed">
  <article aria-posinset="1" aria-setsize="50">...</article>
</div>

<!-- Not updating aria-busy during loading -->
<div role="feed" aria-label="Posts" aria-busy="false">
  <!-- Still showing aria-busy="false" while loading! -->
  <div>Loading...</div>
</div>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)
- **WCAG 2.1 Success Criterion 4.1.3**: Status Messages (Level AA)

## Implementation Checklist

- [ ] **Does container have `role="feed"`?** (CRITICAL)
- [ ] **Does feed have accessible label?** (CRITICAL)
- [ ] **Do all articles have `role="article"`?** (CRITICAL - may be implicit)
- [ ] **Do articles have `aria-posinset` and `aria-setsize`?** (CRITICAL)
- [ ] **Do articles have `aria-labelledby`?** (CRITICAL)
- [ ] **Do articles have `aria-describedby`?** (CRITICAL)
- [ ] **Does Page Down move to next article or load more?** (CRITICAL)
- [ ] **Does Page Up move to previous article?** (CRITICAL)
- [ ] Does Ctrl+End exit feed forward?
- [ ] Does Ctrl+Home exit feed backward?
- [ ] Is `aria-busy="true"` set during loading?
- [ ] Are new articles announced to screen readers?
- [ ] Is focus managed when loading new content?

## Quick Reference

```
✅ DO:
- Use role="feed" on container
- Provide accessible label (aria-label or aria-labelledby)
- Use role="article" for feed items (or semantic <article>)
- Set aria-posinset and aria-setsize on articles
- Connect article title with aria-labelledby
- Connect article summary with aria-describedby
- Support Page Down/Up for navigation
- Support Ctrl+End/Home to exit feed
- Set aria-busy="true" while loading
- Update aria-setsize as total changes
- Focus newly loaded articles appropriately

❌ DON'T:
- Forget role="feed" on container
- Omit accessible label
- Skip aria-posinset/aria-setsize
- Forget aria-labelledby/aria-describedby on articles
- Ignore Page Down/Up keyboard support
- Leave aria-busy unchanged during loading
- Break focus management when loading content
- Use for static content (use regular article list instead)
```
