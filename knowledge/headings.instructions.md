---
description: Instructions for proper heading hierarchy and semantic structure
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Heading Hierarchy and Accessibility

## CRITICAL RULE

**Headings (`<h1>` through `<h6>`) are used to define the LOGICAL HIERARCHICAL STRUCTURE of content, NOT for text formatting.**

- ✅ Heading levels represent the structure and organization of your content (like an outline)
- ❌ Heading levels are NOT for making text bigger, bolder, or achieving visual appearance
- ✅ Every page MUST have at least one `<h1>` element
- ✅ Use CSS for styling text appearance

Proper heading usage is critical for accessibility, SEO, and content navigation.

## Core Principles

### 1. Headings Define Structure, Not Style

**NEVER** use heading tags (`<h1>`, `<h2>`, `<h3>`, etc.) to achieve a visual appearance. If you need larger or bolder text for styling purposes, use CSS instead.

- ✅ Use headings to organize content hierarchically
- ❌ Use headings because you want bigger/bolder text
- ✅ Style text appearance with CSS classes
- ❌ Pick heading levels based on font size

### 2. Maintain Logical Hierarchy

Headings must follow a logical, sequential order that represents the hierarchical structure of the page:

- **Every page MUST have at least one `<h1>`** (the main page title)
- **Heading levels represent the logical hierarchical structure** of the content, not visual styling
- Subheadings should increment by one level at a time
- Don't skip levels (e.g., `<h2>` to `<h5>`)
- You can jump back up multiple levels (e.g., `<h4>` to `<h2>`)

### 3. Screen Reader Navigation

Users with screen readers rely on headings to:
- Understand page structure at a glance
- Navigate quickly between sections
- Skip to relevant content

Improper heading structure makes this impossible.

## Rules for Heading Usage

### Rule 1: Every Page Must Have At Least One H1

**Every page MUST have at least one `<h1>` element** representing the main topic or title. Most pages should have exactly one `<h1>`, but the critical requirement is that there is at least one.

```html
✅ Good:
<h1>Product Documentation</h1>
<h2>Getting Started</h2>
<h2>API Reference</h2>

❌ Bad:
<h1>Product Documentation</h1>
<h1>Getting Started</h1>  <!-- Don't use multiple h1s -->
```

### Rule 2: Heading Levels Represent Logical Hierarchy

**Heading levels directly represent the logical hierarchical structure of your content.** Think of your page as an outline or table of contents:

- `<h1>` = Main topic/title
- `<h2>` = Major sections under the main topic
- `<h3>` = Subsections under h2 sections
- `<h4>` = Sub-subsections under h3 sections
- And so on...

**Don't skip heading levels** - always increment by one when going deeper into the hierarchy.

```html
✅ Good:
<h1>Main Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>
<h4>Sub-subsection</h4>

❌ Bad:
<h1>Main Title</h1>
<h3>Section</h3>  <!-- Skipped h2 -->
<h5>Subsection</h5>  <!-- Skipped h4 -->
```

### Rule 3: Headings Can Jump Back Up

When moving to a new section at a higher level, you can jump back up multiple levels.

```html
✅ Good:
<h2>Chapter 1</h2>
<h3>Section 1.1</h3>
<h4>Subsection 1.1.1</h4>
<h2>Chapter 2</h2>  <!-- Jump back to h2 is fine -->
<h3>Section 2.1</h3>
```

### Rule 4: One Complete Heading Per Element

**Never split a single heading across multiple heading tags.** Each heading should be contained in one complete element.

```html
✅ Good:
<h1>This is the complete heading</h1>

❌ Bad:
<h1>This is</h1><h1> incorrect</h1>  <!-- Don't split headings -->
<h2>Welcome to</h2><h2> our site</h2>  <!-- Don't split headings -->
```

**Why this matters:**
- Screen readers will announce each heading separately, confusing users
- The document structure will appear to have multiple headings when there should be one
- It breaks the logical hierarchy of the page

### Rule 5: Headings Should Be Concise

**Headings should be brief and descriptive, not long blocks of text.** If you have a large amount of text, use a heading followed by paragraphs.

```html
✅ Good:
<h2>Getting Started</h2>
<p>
  This section will guide you through the initial setup process,
  including installation, configuration, and your first steps
  with the application.
</p>

❌ Bad:
<h2>
  This section will guide you through the initial setup process,
  including installation, configuration, and your first steps
  with the application.
</h2>
```

**Guidelines for heading length:**
- Keep headings under 60 characters when possible
- Use 1-8 words for most headings
- Put detailed content in paragraphs, not headings
- Headings should identify sections, not contain full sentences of content

### Rule 6: Use CSS for Visual Styling

If you need text to look like a heading but it's not a structural heading, use CSS classes instead.

```html
✅ Good:
<p class="text-large font-bold">Important Notice</p>
<div class="card-title">Card Heading</div>

❌ Bad:
<h3>Important Notice</h3>  <!-- Not actually a section heading -->
<h2 class="small-text">Card Heading</h2>  <!-- Misusing heading for style -->
```

```css
/* Use CSS to style non-heading text */
.text-large {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #333;
}
```

## Examples

### ✅ Good: Proper Heading Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Blog Post</title>
</head>
<body>
  <header>
    <h1>Understanding Web Accessibility</h1>
    <p class="subtitle">A beginner's guide</p>  <!-- Not a heading, styled with CSS -->
  </header>

  <main>
    <h2>Introduction</h2>
    <p>Content about accessibility...</p>

    <h2>Key Principles</h2>
    <h3>Perceivable</h3>
    <p>Information must be presentable...</p>

    <h3>Operable</h3>
    <p>User interfaces must be operable...</p>

    <h2>Conclusion</h2>
    <p>Summary of key points...</p>
  </main>
</body>
</html>
```

### ✅ Good: React/JSX Component Structure

```jsx
function ProductPage() {
  return (
    <div>
      <h1>Wireless Headphones</h1>

      <section>
        <h2>Features</h2>
        <h3>Sound Quality</h3>
        <p>40mm drivers with deep bass...</p>

        <h3>Battery Life</h3>
        <p>Up to 30 hours of playback...</p>
      </section>

      <section>
        <h2>Technical Specifications</h2>
        <h3>Connectivity</h3>
        <p>Bluetooth 5.0...</p>

        <h3>Dimensions</h3>
        <p>180mm x 150mm x 80mm...</p>
      </section>

      <section>
        <h2>Customer Reviews</h2>
        <div className="review-card">
          <p className="review-title">Great sound!</p>  {/* Not a heading */}
          <p>These headphones are amazing...</p>
        </div>
      </section>
    </div>
  );
}
```

### ✅ Good: Using ARIA for Visually Hidden Headings

Sometimes you need a heading for screen readers even if it's not visible:

```html
<section>
  <h2 class="sr-only">Navigation Menu</h2>
  <nav>
    <ul>
      <li><a href="/home">Home</a></li>
      <li><a href="/about">About</a></li>
    </ul>
  </nav>
</section>

<style>
  /* Screen reader only class */
  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
  }
</style>
```

### ❌ Bad: Using Headings for Styling

```html
<!-- DON'T DO THIS -->
<div class="card">
  <h2>Product Name</h2>  <!-- Wrong if this is just for making text big -->
  <p class="price">$99.99</p>
</div>

<!-- Do this instead -->
<div class="card">
  <p class="card-title">Product Name</p>  <!-- Style with CSS -->
  <p class="price">$99.99</p>
</div>
```

### ❌ Bad: Skipping Heading Levels

```html
<!-- DON'T DO THIS -->
<h1>My Website</h1>
<h3>About Us</h3>  <!-- Skipped h2 -->
<h5>Our Team</h5>  <!-- Skipped h4 -->
<p>Meet our team members...</p>

<!-- Do this instead -->
<h1>My Website</h1>
<h2>About Us</h2>
<h3>Our Team</h3>
<p>Meet our team members...</p>
```

### ❌ Bad: Multiple H1s

```html
<!-- DON'T DO THIS -->
<h1>Welcome to Our Site</h1>
<main>
  <h1>Featured Products</h1>  <!-- Should be h2 -->
  <section>
    <h1>Special Offers</h1>  <!-- Should be h2 -->
  </section>
</main>

<!-- Do this instead -->
<h1>Welcome to Our Site</h1>
<main>
  <h2>Featured Products</h2>
  <section>
    <h2>Special Offers</h2>
  </section>
</main>
```

### ❌ Bad: Styling Headings to Look Different

```html
<!-- DON'T DO THIS -->
<h1 style="font-size: 14px;">Small Heading</h1>  <!-- h1 styled small -->
<h5 style="font-size: 32px;">Big Heading</h5>    <!-- h5 styled big -->

<!-- Do this instead -->
<h1>Proper Main Heading</h1>
<p class="text-large">Text styled to be large</p>
```

### ❌ Bad: Split Headings

```html
<!-- DON'T DO THIS -->
<h1>Welcome to</h1><h1> Our Website</h1>  <!-- Split heading - wrong! -->

<h2>Chapter 1:</h2><h2> Introduction</h2>  <!-- Split heading - wrong! -->

<div>
  <h3>User</h3>
  <h3>Profile</h3>  <!-- Two separate headings when it should be one -->
</div>

<!-- Do this instead -->
<h1>Welcome to Our Website</h1>  <!-- Complete heading in one element -->

<h2>Chapter 1: Introduction</h2>  <!-- Complete heading -->

<div>
  <h3>User Profile</h3>  <!-- Single, complete heading -->
</div>
```

### ❌ Bad: Long Block of Text as Heading

```html
<!-- DON'T DO THIS -->
<h2>
  In this comprehensive guide, we will walk you through every step
  of the process, from initial setup and configuration to advanced
  features and best practices. You'll learn how to optimize your
  workflow, troubleshoot common issues, and make the most of all
  the available features.
</h2>

<!-- Do this instead -->
<h2>Comprehensive Setup Guide</h2>
<p>
  In this comprehensive guide, we will walk you through every step
  of the process, from initial setup and configuration to advanced
  features and best practices. You'll learn how to optimize your
  workflow, troubleshoot common issues, and make the most of all
  the available features.
</p>

<!-- Or use a summary approach -->
<h2>Getting Started</h2>
<p class="summary">
  Learn everything from initial setup to advanced features.
</p>
<p>
  In this comprehensive guide, we will walk you through...
</p>
```

## Common Use Cases

### Blog Post Structure

```html
<article>
  <h1>10 Tips for Better Code</h1>  <!-- Article title -->

  <h2>Introduction</h2>
  <p>Content...</p>

  <h2>Tip 1: Write Clean Code</h2>
  <h3>What is Clean Code?</h3>
  <p>Explanation...</p>

  <h3>How to Achieve It</h3>
  <p>Steps...</p>

  <h2>Tip 2: Use Version Control</h2>
  <p>Content...</p>

  <h2>Conclusion</h2>
  <p>Summary...</p>
</article>
```

### Dashboard Layout

```html
<div class="dashboard">
  <h1>Dashboard</h1>  <!-- Main page title -->

  <section class="metrics">
    <h2>Key Metrics</h2>  <!-- Section heading -->

    <div class="metric-card">
      <p class="metric-label">Total Users</p>  <!-- Not a heading, just a label -->
      <p class="metric-value">1,234</p>
    </div>

    <div class="metric-card">
      <p class="metric-label">Revenue</p>
      <p class="metric-value">$45,678</p>
    </div>
  </section>

  <section class="recent-activity">
    <h2>Recent Activity</h2>
    <ul>
      <li>User signed up</li>
      <li>Payment received</li>
    </ul>
  </section>
</div>
```

### Card Components

```html
<!-- Cards often misuse headings - here's the right way -->
<div class="product-grid">
  <!-- If cards are part of a list, they don't need heading tags -->
  <div class="product-card">
    <img src="product.jpg" alt="Blue sneakers">
    <p class="product-name">Classic Sneakers</p>  <!-- Styled with CSS -->
    <p class="product-price">$79.99</p>
  </div>

  <!-- Unless the card represents an actual section -->
  <article class="blog-card">
    <h3>How to Choose Running Shoes</h3>  <!-- This is a real section heading -->
    <p>A comprehensive guide...</p>
    <a href="/article">Read more</a>
  </article>
</div>
```

## Framework-Specific Considerations

### React/Next.js

```jsx
// ✅ Good: Proper heading structure in components
function BlogPost({ post }) {
  return (
    <article>
      <h1>{post.title}</h1>
      {post.sections.map((section, index) => (
        <section key={index}>
          <h2>{section.title}</h2>
          <p>{section.content}</p>
        </section>
      ))}
    </article>
  );
}

// ✅ Good: Styled text, not headings
function Card({ title, description }) {
  return (
    <div className="card">
      <p className="card-title">{title}</p>
      <p className="card-description">{description}</p>
    </div>
  );
}
```

### Vue

```vue
<template>
  <!-- ✅ Good -->
  <div>
    <h1>{{ pageTitle }}</h1>
    <section v-for="section in sections" :key="section.id">
      <h2>{{ section.title }}</h2>
      <p>{{ section.content }}</p>
    </section>
  </div>
</template>
```

## Testing Heading Structure

### Browser DevTools

1. Open browser DevTools
2. Use the Accessibility Tree inspector
3. Verify heading hierarchy is logical

### Automated Tools

```bash
# Using axe-core in tests
expect(violations).toHaveLength(0);

# Common heading violations:
# - Multiple h1 elements
# - Skipped heading levels
# - Empty headings
```

### Manual Testing

Use browser extensions or screen readers to test:
- **HeadingsMap** (Chrome/Firefox extension)
- **WAVE** (Web accessibility evaluation tool)
- **NVDA/JAWS** (Screen readers) - Use heading navigation shortcuts

### Screen Reader Testing

Test with a screen reader:
- NVDA (Windows): Press `H` to navigate by headings
- VoiceOver (Mac): Use VO+CMD+H to open headings menu
- Check that heading hierarchy makes sense when announced

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.4.6**: Headings and Labels (Level AA)
- **WCAG 2.1 Success Criterion 2.4.10**: Section Headings (Level AAA)

## Implementation Checklist

When generating code with headings:
- [ ] **Does the page have at least one `<h1>`?** (REQUIRED)
- [ ] **Do heading levels represent the logical hierarchical structure of the content?**
- [ ] **Is each heading complete in a single element?** (not split across multiple tags)
- [ ] **Are headings concise?** (not large blocks of text)
- [ ] Are headings used for structure, not styling?
- [ ] Do headings follow a logical hierarchy (h1 → h2 → h3, etc.)?
- [ ] Are there no skipped heading levels?
- [ ] Is CSS used for text styling instead of heading tags?
- [ ] Do headings accurately describe the content they introduce?
- [ ] Can the page be navigated logically using headings alone?
- [ ] Are headings not empty or only whitespace?

## Quick Reference

```
✅ DO:
- ALWAYS include at least one h1 per page (REQUIRED)
- Use heading levels to represent the logical hierarchical structure
- Keep each heading complete in a single element
- Keep headings concise (1-8 words, under 60 characters)
- Increment heading levels sequentially (h2, h3, h4)
- Jump back up any number of levels (h4 → h2 is fine)
- Use CSS for styling text appearance
- Make headings descriptive and meaningful
- Think of headings as an outline of your page content
- Put detailed content in paragraphs, not headings

❌ DON'T:
- Forget to include an h1 on the page
- Split a single heading across multiple heading tags
- Use large blocks of text as headings
- Use headings for text styling or visual appearance
- Skip heading levels (h2 → h5)
- Choose heading levels based on desired font size
- Leave headings empty
- Use headings for anything other than representing content hierarchy
```
