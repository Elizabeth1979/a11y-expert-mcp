---
description: Instructions for proper link accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Link Accessibility

## CRITICAL RULES

**Links navigate users to different locations or resources. ALWAYS use native `<a>` elements with `href` attribute.**

### 1. Use Native <a> Elements with href

**ALWAYS prefer native `<a href="...">` over custom elements with `role="link"`.**

```html
✅ Good - Native link (STRONGLY PREFERRED):
<a href="/about">About Us</a>

✅ Good - External link:
<a href="https://example.com">Visit Example</a>

❌ Bad - Using role="link" on non-link:
<span role="link" onclick="navigate()">About</span>
<!-- Use <a> instead! -->

❌ Bad - Link without href:
<a>About Us</a>  <!-- Missing href! -->
```

**Why native links are essential:**
- Browser provides navigation automatically
- Right-click context menu works
- "Open in new tab" works
- Browser back/forward history works
- Search engine indexing works
- role="link" alone doesn't provide these behaviors

### 2. Only Use role="link" When Absolutely Necessary

**Use `role="link"` ONLY when you cannot use native `<a>` elements.**

If using `role="link"`, you MUST manually implement all link behaviors.

```html
✅ Acceptable - Custom link (when native isn't possible):
<span
  role="link"
  tabindex="0"
  onclick="navigateTo('/page')"
  onkeydown="handleKeyPress(event)">
  Go to Page
</span>

<script>
function handleKeyPress(e) {
  if (e.key === 'Enter') {
    navigateTo('/page');
  }
}

function navigateTo(url) {
  window.location.href = url;
}
</script>

❌ Bad - Missing keyboard support:
<span role="link" onclick="navigate()">
  Link  <!-- Missing Enter key handler! -->
</span>
```

### 3. Provide Descriptive Link Text

**Link text MUST clearly describe the link's destination or purpose.**

```html
✅ Good - Descriptive link text:
<a href="/pricing">View pricing plans</a>

<a href="/report.pdf">Download annual report (PDF, 2MB)</a>

<a href="https://github.com/user/repo">View project on GitHub</a>

❌ Bad - Generic link text:
<a href="/pricing">Click here</a>

<a href="/report.pdf">Download</a>

<a href="/more">Read more</a>

<a href="/info">Learn more</a>
```

**Why this matters:**
- Screen reader users often navigate by links
- Generic text like "click here" provides no context
- Link purpose should be clear out of context

### 4. Indicate External Links and File Downloads

**External links and downloads SHOULD be indicated to users.**

```html
✅ Good - External link with indicator:
<a href="https://example.com" target="_blank" rel="noopener noreferrer">
  Example website
  <span class="sr-only">(opens in new window)</span>
</a>

✅ Good - File download with type and size:
<a href="/report.pdf">
  Annual report
  <span class="sr-only">(PDF, 2.5MB)</span>
</a>

✅ Good - Using aria-label:
<a
  href="https://example.com"
  target="_blank"
  rel="noopener noreferrer"
  aria-label="Example website (opens in new window)">
  Example website
</a>
```

### 5. Enter Key Must Activate Links

**Links MUST activate on Enter key (native links do this automatically).**

```javascript
// ✅ Good - Custom link with Enter key support
customLink.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    window.location.href = customLink.getAttribute('data-href');
  }
});
```

**Note:** Native `<a>` elements handle Enter automatically - another reason to prefer them.

## Complete Link Structure

### Native Links (Preferred)

```html
<!-- Internal navigation -->
<a href="/products">Products</a>

<!-- External link (new window) -->
<a
  href="https://example.com"
  target="_blank"
  rel="noopener noreferrer">
  External site
  <span class="sr-only">(opens in new window)</span>
</a>

<!-- File download -->
<a href="/manual.pdf" download>
  User manual
  <span class="sr-only">(PDF, 1.2MB)</span>
</a>

<!-- Email link -->
<a href="mailto:contact@example.com">
  contact@example.com
</a>

<!-- Phone link -->
<a href="tel:+15551234567">
  (555) 123-4567
</a>

<!-- Skip link -->
<a href="#main-content" class="skip-link">
  Skip to main content
</a>
```

### Custom Link (When Native Isn't Possible)

```html
<span
  role="link"
  tabindex="0"
  data-href="/products"
  id="custom-link">
  Products
</span>

<script>
const customLink = document.getElementById('custom-link');

// Click navigation
customLink.addEventListener('click', () => {
  navigateTo(customLink.getAttribute('data-href'));
});

// Enter key navigation
customLink.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    navigateTo(customLink.getAttribute('data-href'));
  }
});

// Shift+F10 for context menu (optional)
customLink.addEventListener('keydown', (e) => {
  if (e.shiftKey && e.key === 'F10') {
    // Show context menu
  }
});

function navigateTo(url) {
  window.location.href = url;
}
</script>
```

## Examples

### ✅ Good: Navigation Links

```html
<nav aria-label="Main navigation">
  <a href="/">Home</a>
  <a href="/about">About</a>
  <a href="/services">Services</a>
  <a href="/contact">Contact</a>
</nav>
```

### ✅ Good: Link with Icon

```html
<a href="/settings">
  <svg aria-hidden="true"><!-- gear icon --></svg>
  Settings
</a>

<!-- Or icon-only with aria-label -->
<a href="/settings" aria-label="Settings">
  <svg aria-hidden="true"><!-- gear icon --></svg>
</a>
```

### ✅ Good: Card with Link

```html
<article class="card">
  <h2>
    <a href="/article">Article Title</a>
  </h2>
  <p>Article description...</p>
  <a href="/article">Read full article</a>
</article>
```

### ✅ Good: React Link Component

```jsx
function Link({ href, children, external }) {
  const props = external
    ? {
        target: '_blank',
        rel: 'noopener noreferrer'
      }
    : {};

  return (
    <a href={href} {...props}>
      {children}
      {external && (
        <span className="sr-only">(opens in new window)</span>
      )}
    </a>
  );
}

// Usage
<Link href="/about">About Us</Link>
<Link href="https://example.com" external>
  External Site
</Link>
```

### ❌ Bad Examples

```html
<!-- Generic link text -->
<a href="/more">Click here</a>
<a href="/info">Read more</a>

<!-- Missing href -->
<a onclick="navigate()">Go to page</a>

<!-- Using div as link -->
<div role="link" onclick="navigate()">Link</div>

<!-- Empty link -->
<a href="/page"></a>

<!-- Link with only icon, no label -->
<a href="/settings">
  <svg><!-- icon --></svg>
</a>
```

## WCAG References

- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 2.4.4**: Link Purpose (In Context) (Level A)
- **WCAG 2.1 Success Criterion 2.4.9**: Link Purpose (Link Only) (Level AAA)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Are native `<a>` elements with `href` used?** (CRITICAL - strongly preferred)
- [ ] **Is link text descriptive and meaningful?** (CRITICAL)
- [ ] **Does link activate on Enter key?** (CRITICAL - automatic with native)
- [ ] Do external links indicate they open in new window?
- [ ] Do file downloads indicate file type and size?
- [ ] Are icon-only links properly labeled?
- [ ] Are generic link texts avoided ("click here", "read more")?
- [ ] If using role="link", is keyboard support implemented?
- [ ] If using role="link", is click navigation implemented?
- [ ] Are skip links provided for main content?

## Quick Reference

```
✅ DO:
- Use native <a href="..."> elements
- Provide descriptive link text
- Indicate external links (opens in new window)
- Indicate file downloads (type and size)
- Use aria-label for icon-only links
- Make link purpose clear from text alone
- Include href attribute
- Support Enter key (automatic with native)

❌ DON'T:
- Use role="link" when <a> would work
- Use generic text ("click here", "read more")
- Create links without href
- Make links that don't look like links
- Use div/span with onclick instead of <a>
- Omit accessible name for icon-only links
- Forget target="_blank" warning for new windows

## Native <a> vs role="link":

Native <a> (USE THIS):
  - Browser handles navigation automatically
  - Context menu works (right-click)
  - "Open in new tab" works
  - Browser history works
  - Enter key works automatically
  - No JavaScript required

role="link" (AVOID):
  - Must manually implement navigation
  - Must add Enter key handler
  - Must add tabindex="0"
  - Context menu doesn't work
  - "Open in new tab" doesn't work
  - Only use when <a> truly isn't possible
```
