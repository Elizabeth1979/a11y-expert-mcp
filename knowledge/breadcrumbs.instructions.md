---
description: Instructions for proper breadcrumb navigation accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Breadcrumb Navigation Accessibility

## CRITICAL RULES

**When implementing breadcrumb navigation, follow the WAI-ARIA Authoring Practices Guide (APG) patterns.**

Reference: [WAI-ARIA APG Breadcrumb Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/)

### 1. Use Proper Semantic Structure

**Breadcrumbs MUST be structured as an ordered list (`<ol>`) or unordered list (`<ul>`) with list items (`<li>`).**

```html
✅ Good - Proper list structure:
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/products/laptops">Laptops</a></li>
    <li aria-current="page">Gaming Laptop</li>
  </ol>
</nav>

❌ Bad - Not using list structure:
<nav aria-label="Breadcrumb">
  <a href="/">Home</a> >
  <a href="/products">Products</a> >
  <span>Gaming Laptop</span>
</nav>
```

**Key points:**
- Use `<ol>` (ordered list) or `<ul>` (unordered list)
- Each breadcrumb item must be in an `<li>` element
- This provides proper semantic structure for assistive technologies

### 2. Wrap in a `<nav>` Element

**Breadcrumbs MUST be contained within a `<nav>` element to identify it as a navigation landmark.**

```html
✅ Good - Wrapped in nav:
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Laptops</li>
  </ol>
</nav>

❌ Bad - Missing nav wrapper:
<div class="breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
  </ol>
</div>
```

**Why this matters:**
- `<nav>` creates a navigation landmark
- Screen reader users can quickly find and jump to navigation areas
- Identifies the breadcrumb as a navigation aid

### 3. Include `aria-label` on the `<nav>` Element

**The `<nav>` element MUST have an `aria-label` (or `aria-labelledby`) to identify it as breadcrumb navigation.**

```html
✅ Good - With aria-label:
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li aria-current="page">Current Page</li>
  </ol>
</nav>

✅ Good - With aria-labelledby:
<h2 id="breadcrumb-label">You are here</h2>
<nav aria-labelledby="breadcrumb-label">
  <ol>
    <li><a href="/">Home</a></li>
    <li aria-current="page">Current Page</li>
  </ol>
</nav>

❌ Bad - Missing aria-label:
<nav>
  <ol>
    <li><a href="/">Home</a></li>
  </ol>
</nav>
```

**Recommended labels:**
- `aria-label="Breadcrumb"`
- `aria-label="You are here"`
- `aria-label="Page navigation"`

### 4. Mark Current Page with `aria-current="page"`

**The last item (current page) MUST include `aria-current="page"` to indicate the user's current location.**

```html
✅ Good - Current page marked:
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li><a href="/products/laptops">Laptops</a></li>
    <li aria-current="page">Gaming Laptop XZ-1000</li>
  </ol>
</nav>

✅ Good - Current page as link (if clickable):
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li>
      <a href="/products/laptops" aria-current="page">Laptops</a>
    </li>
  </ol>
</nav>

❌ Bad - Current page not marked:
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li>Laptops</li>  <!-- Missing aria-current="page"! -->
  </ol>
</nav>
```

**Key points:**
- Use `aria-current="page"` on the current page item
- Can be on the `<li>` or the `<a>` element
- Most commonly, the current page is NOT a link (just text)

### 5. Each Item Should Be a Link (Except Current Page)

**All breadcrumb items except the current page should be clickable links.**

```html
✅ Good - All items are links except current:
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/category">Category</a></li>
    <li><a href="/category/subcategory">Subcategory</a></li>
    <li aria-current="page">Current Page</li>
  </ol>
</nav>

❌ Bad - Items are not links:
<nav aria-label="Breadcrumb">
  <ol>
    <li>Home</li>
    <li>Category</li>
    <li>Current Page</li>
  </ol>
</nav>
```

**Why links matter:**
- Users can click to navigate to parent pages
- Breadcrumbs provide quick navigation back up the hierarchy
- Links should go to actual pages users can visit

## Complete Breadcrumb Pattern

**Standard breadcrumb implementation following APG guidelines:**

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li>
      <a href="/">Home</a>
    </li>
    <li>
      <a href="/products">Products</a>
    </li>
    <li>
      <a href="/products/electronics">Electronics</a>
    </li>
    <li>
      <a href="/products/electronics/laptops">Laptops</a>
    </li>
    <li aria-current="page">
      Gaming Laptop XZ-1000
    </li>
  </ol>
</nav>
```

## Visual Separators

**When adding visual separators (>, /, →), use CSS or `aria-hidden` to hide them from screen readers:**

```html
✅ Good - Separators with aria-hidden:
<nav aria-label="Breadcrumb">
  <ol>
    <li>
      <a href="/">Home</a>
      <span aria-hidden="true"> / </span>
    </li>
    <li>
      <a href="/products">Products</a>
      <span aria-hidden="true"> / </span>
    </li>
    <li aria-current="page">Laptops</li>
  </ol>
</nav>

✅ Good - Separators with CSS ::after:
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Laptops</li>
  </ol>
</nav>

<style>
  ol li:not(:last-child)::after {
    content: " / ";
    padding: 0 0.5rem;
    color: #666;
  }
</style>

❌ Bad - Separators in link text:
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home ></a></li>  <!-- Screen reader reads "Home greater than" -->
    <li><a href="/products">Products ></a></li>
  </ol>
</nav>
```

## Examples

### ✅ Good: Basic Breadcrumb

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/blog">Blog</a></li>
    <li><a href="/blog/tutorials">Tutorials</a></li>
    <li aria-current="page">How to Build Accessible Breadcrumbs</li>
  </ol>
</nav>
```

### ✅ Good: E-commerce Breadcrumb

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Store Home</a></li>
    <li><a href="/categories">Categories</a></li>
    <li><a href="/categories/clothing">Clothing</a></li>
    <li><a href="/categories/clothing/mens">Men's Clothing</a></li>
    <li><a href="/categories/clothing/mens/shirts">Shirts</a></li>
    <li aria-current="page">Blue Oxford Shirt - Size M</li>
  </ol>
</nav>
```

### ✅ Good: Breadcrumb with Visual Styling

```html
<nav aria-label="Breadcrumb" class="breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/docs">Documentation</a></li>
    <li><a href="/docs/api">API Reference</a></li>
    <li aria-current="page">Authentication</li>
  </ol>
</nav>

<style>
  .breadcrumb ol {
    list-style: none;
    display: flex;
    gap: 0.5rem;
    padding: 0;
    margin: 1rem 0;
  }

  .breadcrumb li:not(:last-child)::after {
    content: "›";
    margin-left: 0.5rem;
    color: #999;
  }

  .breadcrumb a {
    color: #0066cc;
    text-decoration: none;
  }

  .breadcrumb a:hover {
    text-decoration: underline;
  }

  .breadcrumb li[aria-current="page"] {
    color: #333;
    font-weight: 500;
  }
</style>
```

### ✅ Good: React/JSX Breadcrumb Component

```jsx
function Breadcrumb({ items }) {
  return (
    <nav aria-label="Breadcrumb">
      <ol>
        {items.map((item, index) => {
          const isLast = index === items.length - 1;

          return (
            <li key={item.path} aria-current={isLast ? "page" : undefined}>
              {!isLast ? (
                <a href={item.path}>{item.label}</a>
              ) : (
                item.label
              )}
            </li>
          );
        })}
      </ol>
    </nav>
  );
}

// Usage
<Breadcrumb
  items={[
    { path: '/', label: 'Home' },
    { path: '/products', label: 'Products' },
    { path: '/products/laptops', label: 'Laptops' },
    { path: '/products/laptops/gaming', label: 'Gaming Laptop XZ-1000' }
  ]}
/>
```

### ✅ Good: Vue Breadcrumb Component

```vue
<template>
  <nav aria-label="Breadcrumb">
    <ol>
      <li
        v-for="(item, index) in items"
        :key="item.path"
        :aria-current="index === items.length - 1 ? 'page' : undefined">
        <a v-if="index < items.length - 1" :href="item.path">
          {{ item.label }}
        </a>
        <span v-else>{{ item.label }}</span>
      </li>
    </ol>
  </nav>
</template>

<script>
export default {
  props: {
    items: Array
  }
}
</script>
```

### ❌ Bad: Missing Navigation Wrapper

```html
<!-- Missing <nav> element -->
<div class="breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li>Current Page</li>
  </ol>
</div>

<!-- Correct: -->
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Current Page</li>
  </ol>
</nav>
```

### ❌ Bad: Not Using List Structure

```html
<!-- Using divs instead of list -->
<nav aria-label="Breadcrumb">
  <div class="breadcrumb-item">
    <a href="/">Home</a>
  </div>
  <div class="breadcrumb-item">
    <a href="/products">Products</a>
  </div>
  <div class="breadcrumb-item">Current Page</div>
</nav>

<!-- Correct: -->
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Current Page</li>
  </ol>
</nav>
```

### ❌ Bad: Missing aria-current

```html
<!-- Current page not marked -->
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li class="active">Current Page</li>  <!-- Missing aria-current! -->
  </ol>
</nav>

<!-- Correct: -->
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Current Page</li>
  </ol>
</nav>
```

### ❌ Bad: Missing aria-label on nav

```html
<!-- No aria-label to identify the navigation -->
<nav>
  <ol>
    <li><a href="/">Home</a></li>
    <li aria-current="page">Current Page</li>
  </ol>
</nav>

<!-- Correct: -->
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li aria-current="page">Current Page</li>
  </ol>
</nav>
```

## Common Patterns

### Pattern 1: Simple Path

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/category">Category</a></li>
    <li aria-current="page">Article Title</li>
  </ol>
</nav>
```

### Pattern 2: Deep Hierarchy

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/level1">Level 1</a></li>
    <li><a href="/level1/level2">Level 2</a></li>
    <li><a href="/level1/level2/level3">Level 3</a></li>
    <li><a href="/level1/level2/level3/level4">Level 4</a></li>
    <li aria-current="page">Current Page</li>
  </ol>
</nav>
```

### Pattern 3: With Icons

```html
<nav aria-label="Breadcrumb">
  <ol>
    <li>
      <a href="/">
        <svg aria-hidden="true" width="16" height="16">
          <path d="..."/>
        </svg>
        <span>Home</span>
      </a>
    </li>
    <li><a href="/products">Products</a></li>
    <li aria-current="page">Laptops</li>
  </ol>
</nav>
```

## Responsive Breadcrumbs

**For mobile, consider truncating or collapsing breadcrumbs:**

```html
<nav aria-label="Breadcrumb">
  <ol>
    <!-- Mobile: show first and last only -->
    <li class="show-mobile"><a href="/">Home</a></li>
    <li class="hide-mobile"><a href="/level1">Level 1</a></li>
    <li class="hide-mobile"><a href="/level2">Level 2</a></li>
    <li class="ellipsis hide-mobile" aria-hidden="true">...</li>
    <li aria-current="page">Current Page</li>
  </ol>
</nav>

<style>
  @media (max-width: 768px) {
    .hide-mobile {
      display: none;
    }
  }
</style>
```

## WCAG References

- **WCAG 2.1 Success Criterion 2.4.8**: Location (Level AAA)
- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

When creating breadcrumb navigation:
- [ ] **Is the breadcrumb wrapped in a `<nav>` element?** (REQUIRED)
- [ ] **Does the `<nav>` have `aria-label="Breadcrumb"`?** (REQUIRED)
- [ ] **Are breadcrumb items in an `<ol>` or `<ul>` list?** (REQUIRED)
- [ ] **Is each item in an `<li>` element?** (REQUIRED)
- [ ] **Does the current page have `aria-current="page"`?** (REQUIRED)
- [ ] **Are all items except current page clickable links?**
- [ ] **Do links point to valid parent pages?**
- [ ] **Are visual separators hidden from screen readers?** (use `aria-hidden` or CSS)
- [ ] **Is the breadcrumb positioned before main content?**
- [ ] **Does it work responsively on mobile?**

## Quick Reference

```
✅ REQUIRED Structure:

<nav aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="/parent">Parent</a></li>
    <li aria-current="page">Current Page</li>
  </ol>
</nav>

✅ DO:
- Wrap breadcrumbs in <nav> element
- Add aria-label="Breadcrumb" to <nav>
- Use <ol> or <ul> for the list
- Put each item in <li>
- Mark current page with aria-current="page"
- Make all items except current page into links
- Hide visual separators from screen readers
- Follow WAI-ARIA APG breadcrumb pattern

❌ DON'T:
- Use divs instead of list structure
- Omit the <nav> wrapper
- Forget aria-label on <nav>
- Skip aria-current="page" on current item
- Make the current page a clickable link (usually)
- Include separators in link text
- Use breadcrumbs without providing working links

Reference: https://www.w3.org/WAI/ARIA/apg/patterns/breadcrumb/
```
