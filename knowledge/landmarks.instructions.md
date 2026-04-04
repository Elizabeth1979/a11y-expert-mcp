---
description: Instructions for proper landmark accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Landmarks Accessibility

## CRITICAL RULES

**Landmarks identify major page sections, enabling screen reader users to quickly navigate and understand page structure. There are 8 landmark roles.**

### 1. Use Semantic HTML Elements (Preferred)

**ALWAYS prefer native HTML5 semantic elements over ARIA landmark roles.**

```html
✅ Good - Semantic HTML (STRONGLY PREFERRED):
<header>
  <nav>...</nav>
</header>
<main>...</main>
<aside>...</aside>
<footer>...</footer>

❌ Bad - Using ARIA roles instead of semantic HTML:
<div role="banner">  <!-- Use <header> instead! -->
  <div role="navigation">...</div>  <!-- Use <nav> instead! -->
</div>
<div role="main">...</div>  <!-- Use <main> instead! -->
```

**Native HTML elements automatically create landmarks**:
- `<header>` → banner landmark (when not inside article/section)
- `<nav>` → navigation landmark
- `<main>` → main landmark
- `<aside>` → complementary landmark
- `<footer>` → contentinfo landmark (when not inside article/section)
- `<form>` → form landmark (when has accessible name)
- `<section>` → region landmark (when has accessible name)

### 2. All Content Must Be Within Landmarks

**Every piece of content SHOULD be contained within an appropriate landmark region.**

```html
✅ Good - All content in landmarks:
<body>
  <header>
    <nav>...</nav>
  </header>

  <main>
    <h1>Page Title</h1>
    <p>All main content here...</p>
  </main>

  <aside>
    <h2>Related Links</h2>
    ...
  </aside>

  <footer>
    <p>Copyright info</p>
  </footer>
</body>

❌ Bad - Content outside landmarks:
<body>
  <div>Orphan content</div>  <!-- Not in any landmark! -->
  <main>...</main>
</body>
```

### 3. Limit to ~7 Landmarks Per Page

**Use approximately 7 or fewer landmark regions for optimal navigation value.**

```html
✅ Good - Reasonable number of landmarks:
<header>...</header>  <!-- 1: banner -->
<nav>...</nav>  <!-- 2: navigation -->
<main>  <!-- 3: main -->
  <article>...</article>
  <aside>...</aside>  <!-- 4: complementary -->
</main>
<footer>...</footer>  <!-- 5: contentinfo -->

❌ Bad - Too many landmarks:
<main>
  <section aria-label="Intro">...</section>
  <section aria-label="Step 1">...</section>
  <section aria-label="Step 2">...</section>
  <section aria-label="Step 3">...</section>
  <!-- ... 15 more section landmarks -->
  <!-- Too many! Loses navigation value -->
</main>
```

### 4. Label Multiple Instances of Same Landmark

**When multiple landmarks of the same type exist, each MUST have a unique label.**

```html
✅ Good - Multiple navs with unique labels:
<nav aria-label="Main navigation">
  <a href="/">Home</a>
  <a href="/about">About</a>
</nav>

<main>
  <nav aria-label="Table of contents">
    <a href="#intro">Introduction</a>
    <a href="#methods">Methods</a>
  </nav>
</main>

<nav aria-label="Footer navigation">
  <a href="/privacy">Privacy</a>
  <a href="/terms">Terms</a>
</nav>

❌ Bad - Multiple navs without labels:
<nav>  <!-- Which navigation is this? -->
  <a href="/">Home</a>
</nav>

<nav>  <!-- Can't distinguish from first! -->
  <a href="#intro">Intro</a>
</nav>
```

### 5. Use Each Landmark Type Appropriately

**Each of the 8 landmark roles has a specific purpose.**

```html
✅ Good - Proper landmark usage:
<!-- banner: Site header (logo, site nav) -->
<header>
  <img src="logo.png" alt="Company">
  <nav aria-label="Main">...</nav>
</header>

<!-- navigation: Navigation links -->
<nav aria-label="Products">...</nav>

<!-- main: Primary page content (ONE per page) -->
<main>
  <h1>Page Title</h1>
  <p>Main content...</p>
</main>

<!-- complementary: Related but separate content -->
<aside>
  <h2>Related Articles</h2>
  ...
</aside>

<!-- contentinfo: Site footer (copyright, legal) -->
<footer>
  <p>&copy; 2025 Company</p>
</footer>

<!-- search: Search functionality -->
<div role="search">
  <input type="search" aria-label="Search">
  <button>Search</button>
</div>

<!-- form: Form with accessible name -->
<form aria-label="Contact form">
  ...
</form>

<!-- region: Important content area (use sparingly) -->
<section aria-label="Latest news">
  ...
</section>
```

## The Eight Landmark Roles

### 1. banner (use `<header>`)

**Site-wide header containing logo, site navigation, search.**

```html
✅ Good:
<header>
  <img src="logo.png" alt="Site Name">
  <nav aria-label="Main navigation">...</nav>
</header>

<!-- Or with ARIA role: -->
<div role="banner">
  <img src="logo.png" alt="Site Name">
</div>
```

**Rules**:
- Only ONE banner per page
- Must be at top level (not inside `<article>` or `<section>`)
- `<header>` inside article/section is NOT a banner

### 2. navigation (use `<nav>`)

**Groups of navigation links.**

```html
✅ Good:
<nav aria-label="Main navigation">
  <a href="/">Home</a>
  <a href="/about">About</a>
</nav>

<nav aria-label="Breadcrumb" aria-label="Breadcrumb">
  <a href="/">Home</a> > <a href="/products">Products</a>
</nav>
```

**Rules**:
- Use for major navigation blocks
- Label multiple navs with `aria-label` or `aria-labelledby`
- Don't overuse (not for every list of links)

### 3. main (use `<main>`)

**Primary content of the page.**

```html
✅ Good:
<main>
  <h1>Page Title</h1>
  <p>Main content...</p>
</main>
```

**Rules**:
- **Only ONE main per page** (CRITICAL)
- Contains unique page content
- Skip all repeated content (header, nav, footer)

### 4. complementary (use `<aside>`)

**Supporting content related to main content.**

```html
✅ Good:
<aside>
  <h2>Related Articles</h2>
  <ul>...</ul>
</aside>

<aside aria-label="Advertisement">
  <img src="ad.jpg" alt="...">
</aside>
```

**Rules**:
- Related but separate from main content
- Should make sense on its own
- Examples: sidebars, related links, ads, author bio

### 5. contentinfo (use `<footer>`)

**Site footer with metadata, copyright, legal links.**

```html
✅ Good:
<footer>
  <p>&copy; 2025 Company Name</p>
  <nav aria-label="Legal">
    <a href="/privacy">Privacy</a>
    <a href="/terms">Terms</a>
  </nav>
</footer>
```

**Rules**:
- Only ONE contentinfo per page
- Must be at top level (not inside article/section)
- `<footer>` inside article/section is NOT contentinfo

### 6. search

**Search functionality (NO native HTML element).**

```html
✅ Good:
<div role="search">
  <label for="search-input">Search</label>
  <input type="search" id="search-input">
  <button>Search</button>
</div>

<!-- Or wrap search form: -->
<form role="search">
  <input type="search" aria-label="Search">
  <button>Search</button>
</form>
```

**Rules**:
- Must use `role="search"` (no native element)
- One search landmark per page typically

### 7. form (use `<form>` with label)

**Form with accessible name becomes form landmark.**

```html
✅ Good - Form landmark:
<form aria-label="Contact form">
  <label for="name">Name</label>
  <input type="text" id="name">
  <button>Submit</button>
</form>

✅ Good - Using aria-labelledby:
<h2 id="login-heading">Log In</h2>
<form aria-labelledby="login-heading">
  ...
</form>

❌ Bad - Form without label (NOT a landmark):
<form>
  <!-- No aria-label or aria-labelledby -->
  <!-- This is NOT a landmark -->
</form>
```

**Rules**:
- Form becomes landmark ONLY when it has `aria-label` or `aria-labelledby`
- Use for important forms (contact, login, search)
- Don't overuse - not every form needs to be a landmark

### 8. region (use `<section>` with label)

**Important content area with accessible name.**

```html
✅ Good - Region landmark:
<section aria-labelledby="news-heading">
  <h2 id="news-heading">Latest News</h2>
  ...
</section>

<section aria-label="Image gallery">
  ...
</section>

❌ Bad - Section without label (NOT a landmark):
<section>
  <!-- No aria-label or aria-labelledby -->
  <!-- This is NOT a landmark -->
</section>
```

**Rules**:
- Section becomes landmark ONLY when it has `aria-label` or `aria-labelledby`
- Use sparingly for important content areas
- Don't overuse - creates too many landmarks

## Complete Page Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Page Title</title>
</head>
<body>
  <!-- banner landmark -->
  <header>
    <img src="logo.png" alt="Company Name">

    <!-- navigation landmark -->
    <nav aria-label="Main navigation">
      <a href="/">Home</a>
      <a href="/about">About</a>
      <a href="/products">Products</a>
    </nav>

    <!-- search landmark -->
    <div role="search">
      <label for="site-search">Search</label>
      <input type="search" id="site-search">
      <button>Search</button>
    </div>
  </header>

  <!-- navigation landmark (breadcrumb) -->
  <nav aria-label="Breadcrumb">
    <a href="/">Home</a> &gt;
    <a href="/products">Products</a> &gt;
    <span aria-current="page">Widget</span>
  </nav>

  <!-- main landmark -->
  <main>
    <h1>Product: Super Widget</h1>

    <article>
      <h2>Description</h2>
      <p>Product description...</p>
    </article>

    <!-- region landmark (important section) -->
    <section aria-labelledby="reviews-heading">
      <h2 id="reviews-heading">Customer Reviews</h2>
      ...
    </section>
  </main>

  <!-- complementary landmark -->
  <aside>
    <h2>Related Products</h2>
    <ul>
      <li><a href="/product/1">Product 1</a></li>
      <li><a href="/product/2">Product 2</a></li>
    </ul>
  </aside>

  <!-- contentinfo landmark -->
  <footer>
    <p>&copy; 2025 Company Name. All rights reserved.</p>

    <!-- navigation landmark (footer nav) -->
    <nav aria-label="Footer navigation">
      <a href="/privacy">Privacy Policy</a>
      <a href="/terms">Terms of Service</a>
      <a href="/contact">Contact Us</a>
    </nav>
  </footer>
</body>
</html>
```

## Examples

### ✅ Good: Application Layout

```html
<body>
  <header>
    <h1>My App</h1>
    <nav aria-label="Main">
      <a href="/dashboard">Dashboard</a>
      <a href="/settings">Settings</a>
    </nav>
  </header>

  <main>
    <h2>Dashboard</h2>
    <p>Welcome back!</p>
  </main>

  <footer>
    <p>© 2025 My App</p>
  </footer>
</body>
```

### ✅ Good: React Page Component

```jsx
function PageLayout({ children }) {
  return (
    <>
      <header>
        <Logo />
        <nav aria-label="Main navigation">
          <Link to="/">Home</Link>
          <Link to="/about">About</Link>
          <Link to="/contact">Contact</Link>
        </nav>
      </header>

      <main>
        {children}
      </main>

      <aside>
        <h2>Newsletter</h2>
        <form aria-label="Newsletter signup">
          <label htmlFor="email">Email</label>
          <input type="email" id="email" />
          <button>Subscribe</button>
        </form>
      </aside>

      <footer>
        <p>&copy; 2025 Company</p>
        <nav aria-label="Legal">
          <Link to="/privacy">Privacy</Link>
          <Link to="/terms">Terms</Link>
        </nav>
      </footer>
    </>
  );
}
```

### ❌ Bad Examples

```html
<!-- Missing main landmark -->
<body>
  <header>...</header>
  <div class="content">  <!-- Should be <main>! -->
    <h1>Title</h1>
  </div>
  <footer>...</footer>
</body>

<!-- Multiple main landmarks -->
<main>Section 1</main>
<main>Section 2</main>  <!-- WRONG! Only one main allowed -->

<!-- Content outside landmarks -->
<body>
  <p>Orphan content</p>  <!-- Not in any landmark! -->
  <main>...</main>
</body>

<!-- Unlabeled duplicate landmarks -->
<nav>  <!-- Which nav is this? -->
  <a href="/">Home</a>
</nav>
<nav>  <!-- Can't distinguish! Need labels -->
  <a href="#intro">Intro</a>
</nav>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.4.1**: Bypass Blocks (Level A)
- **WCAG 2.1 Success Criterion 2.4.6**: Headings and Labels (Level AA)

## Implementation Checklist

- [ ] **Is there exactly ONE `<main>` landmark?** (CRITICAL)
- [ ] **Is all content within landmarks?** (CRITICAL)
- [ ] **Are semantic HTML elements used?** (CRITICAL - prefer over ARIA roles)
- [ ] Is there approximately 7 or fewer landmarks?
- [ ] Are multiple instances of same landmark type labeled?
- [ ] Is `<header>` used only at top level for banner?
- [ ] Is `<footer>` used only at top level for contentinfo?
- [ ] Do forms have labels to become landmarks (when appropriate)?
- [ ] Do sections have labels to become landmarks (when appropriate)?
- [ ] Is search functionality wrapped in `role="search"`?

## Quick Reference

```
✅ DO:
- Use semantic HTML (<header>, <nav>, <main>, <aside>, <footer>)
- Include exactly ONE <main> per page
- Put all content within landmarks
- Label duplicate landmarks uniquely
- Limit to ~7 landmarks per page
- Use <section> with label for important regions
- Use <form> with label for important forms
- Use role="search" for search functionality

❌ DON'T:
- Use ARIA roles when semantic HTML exists
- Create multiple <main> landmarks
- Leave content outside landmarks
- Overuse landmarks (creates too many)
- Forget to label duplicate landmark types
- Use <section> without label (not a landmark)
- Use <form> without label (not a landmark unless needed)
- Use <header>/<footer> inside article for banner/contentinfo

## The 8 Landmarks:

1. banner - <header> at top level (site header)
2. navigation - <nav> (navigation links)
3. main - <main> (primary content, ONE per page)
4. complementary - <aside> (related content)
5. contentinfo - <footer> at top level (site footer)
6. search - role="search" (search functionality)
7. form - <form aria-label="..."> (labeled forms)
8. region - <section aria-label="..."> (labeled sections)
```
