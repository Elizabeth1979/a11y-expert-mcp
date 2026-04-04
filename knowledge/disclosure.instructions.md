---
description: Instructions for proper disclosure (show/hide) accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Disclosure (Show/Hide) Accessibility

## CRITICAL RULES

**A disclosure widget is a button that controls visibility of content. Common examples: "Show more", "Read more", "Expand details".**

### 1. Use Button Element with aria-expanded

**The toggle control MUST be a `<button>` with `aria-expanded="true|false"`.**

```html
✅ Good - Button with aria-expanded:
<button aria-expanded="false" aria-controls="details-1">
  Show Details
</button>
<div id="details-1" hidden>
  <p>Additional details...</p>
</div>

❌ Bad - Missing aria-expanded:
<button id="show-btn">
  Show Details  <!-- Missing aria-expanded! -->
</button>

❌ Bad - Using div instead of button:
<div onclick="toggleDetails()">  <!-- Should be <button>! -->
  Show Details
</div>
```

### 2. Update aria-expanded Based on Visibility

**`aria-expanded` MUST be `"false"` when content is hidden, `"true"` when visible.**

```html
✅ Good - Content hidden:
<button aria-expanded="false" aria-controls="content-1">
  Show More
</button>
<div id="content-1" hidden>
  <p>Hidden content</p>
</div>

✅ Good - Content visible:
<button aria-expanded="true" aria-controls="content-1">
  Show Less
</button>
<div id="content-1">
  <p>Visible content</p>
</div>

❌ Bad - aria-expanded doesn't match visibility:
<button aria-expanded="false">Show</button>
<div>  <!-- Content visible but aria-expanded="false"! -->
  <p>Content</p>
</div>
```

### 3. Connect Button and Content with aria-controls

**The button SHOULD have `aria-controls` referencing the content element ID.**

```html
✅ Good - Using aria-controls:
<button
  aria-expanded="false"
  aria-controls="faq-answer-1"
  id="faq-button-1">
  What is your return policy?
</button>
<div id="faq-answer-1" hidden>
  <p>You can return items within 30 days...</p>
</div>

✅ Acceptable - Without aria-controls (if adjacent):
<button aria-expanded="false">
  Show More
</button>
<div hidden>
  <p>Content immediately follows button</p>
</div>
```

### 4. Hide Content Properly

**Hidden content MUST use `hidden` attribute or CSS `display: none`.**

```html
✅ Good - Using hidden attribute:
<div id="content" hidden>
  <p>This content is hidden</p>
</div>

✅ Good - Using CSS display:
<div id="content" style="display: none;">
  <p>This content is hidden</p>
</div>

❌ Bad - Using visibility or opacity:
<div id="content" style="visibility: hidden;">
  <!-- Still in keyboard tab sequence! -->
</div>

<div id="content" style="opacity: 0;">
  <!-- Still in keyboard tab sequence! -->
</div>
```

### 5. Implement Keyboard Support

**The button MUST respond to Enter and Space keys.**

```javascript
// ✅ Good - Keyboard support (native button handles this automatically)
<button
  aria-expanded="false"
  aria-controls="content"
  onclick="toggleContent()">
  Show Details
</button>

// If using a custom element, handle keyboard:
customButton.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    toggleContent();
  }
});
```

**Note:** Native `<button>` elements handle Enter and Space automatically.

## Complete Disclosure Structure

```html
<button
  id="disclosure-btn"
  aria-expanded="false"
  aria-controls="disclosure-content">
  Show More Information
</button>

<div id="disclosure-content" hidden>
  <h3>Additional Information</h3>
  <p>
    This is the content that will be shown when the disclosure
    button is activated. It can contain any HTML content including
    headings, paragraphs, lists, links, etc.
  </p>
  <ul>
    <li>Item 1</li>
    <li>Item 2</li>
    <li>Item 3</li>
  </ul>
</div>

<script>
const button = document.getElementById('disclosure-btn');
const content = document.getElementById('disclosure-content');

button.addEventListener('click', () => {
  const isExpanded = button.getAttribute('aria-expanded') === 'true';

  if (isExpanded) {
    // Hide content
    button.setAttribute('aria-expanded', 'false');
    content.setAttribute('hidden', '');
    button.textContent = 'Show More Information';
  } else {
    // Show content
    button.setAttribute('aria-expanded', 'true');
    content.removeAttribute('hidden');
    button.textContent = 'Show Less Information';
  }
});
</script>
```

## Examples

### ✅ Good: Simple Show/Hide

```html
<button aria-expanded="false" aria-controls="bio">
  Read Full Biography
</button>

<div id="bio" hidden>
  <p>
    Born in 1950, Dr. Smith completed her PhD at MIT and went on
    to pioneer research in quantum computing...
  </p>
</div>
```

### ✅ Good: FAQ Disclosure

```html
<h2>Frequently Asked Questions</h2>

<h3>
  <button
    aria-expanded="false"
    aria-controls="answer-1"
    id="question-1">
    How do I reset my password?
  </button>
</h3>
<div id="answer-1" hidden>
  <p>
    Click "Forgot Password" on the login page and follow the
    instructions sent to your email.
  </p>
</div>

<h3>
  <button
    aria-expanded="false"
    aria-controls="answer-2"
    id="question-2">
    What payment methods do you accept?
  </button>
</h3>
<div id="answer-2" hidden>
  <p>We accept Visa, Mastercard, American Express, and PayPal.</p>
</div>
```

### ✅ Good: Disclosure with Icon

```html
<button aria-expanded="false" aria-controls="details">
  <svg aria-hidden="true" class="icon">
    <!-- Chevron right icon -->
  </svg>
  Show Technical Specifications
</button>

<div id="details" hidden>
  <dl>
    <dt>Processor</dt>
    <dd>Intel Core i7</dd>
    <dt>Memory</dt>
    <dd>16GB RAM</dd>
    <dt>Storage</dt>
    <dd>512GB SSD</dd>
  </dl>
</div>
```

**Note:** Icons should be decorative (aria-hidden="true") since button text provides the label.

### ✅ Good: React Disclosure Component

```jsx
function Disclosure({ buttonText, children }) {
  const [isExpanded, setIsExpanded] = React.useState(false);
  const contentId = React.useId();

  return (
    <div>
      <button
        aria-expanded={isExpanded}
        aria-controls={contentId}
        onClick={() => setIsExpanded(!isExpanded)}>
        {isExpanded ? 'Show Less' : buttonText}
      </button>

      <div id={contentId} hidden={!isExpanded}>
        {children}
      </div>
    </div>
  );
}

// Usage
<Disclosure buttonText="Show Details">
  <p>This is the hidden content that will be revealed.</p>
</Disclosure>
```

### ✅ Good: Vue Disclosure Component

```vue
<template>
  <div>
    <button
      :aria-expanded="isExpanded"
      :aria-controls="contentId"
      @click="isExpanded = !isExpanded">
      {{ isExpanded ? 'Show Less' : buttonText }}
    </button>

    <div :id="contentId" :hidden="!isExpanded">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    buttonText: String
  },
  data() {
    return {
      isExpanded: false,
      contentId: `disclosure-${Math.random().toString(36).substr(2, 9)}`
    };
  }
};
</script>
```

### ❌ Bad Examples

```html
<!-- Missing aria-expanded -->
<button id="show-btn">Show More</button>
<div id="content" hidden>Content</div>

<!-- Using div instead of button -->
<div class="disclosure-btn" onclick="toggle()">
  Show More
</div>

<!-- aria-expanded doesn't match visibility -->
<button aria-expanded="false">Show Details</button>
<div>Visible content</div>  <!-- Should be hidden! -->

<!-- Using visibility: hidden (wrong) -->
<button aria-expanded="false">Show</button>
<div style="visibility: hidden;">
  <!-- Still focusable! Should use hidden attribute -->
</div>

<!-- Missing button element -->
<a href="#" onclick="toggle()">Show More</a>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Is the toggle control a `<button>` element?** (CRITICAL)
- [ ] **Does button have `aria-expanded` attribute?** (CRITICAL)
- [ ] **Is `aria-expanded="false"` when content hidden?** (CRITICAL)
- [ ] **Is `aria-expanded="true"` when content visible?** (CRITICAL)
- [ ] **Is hidden content using `hidden` attribute or `display: none`?** (CRITICAL)
- [ ] Does button have `aria-controls` referencing content ID?
- [ ] Does button text change to reflect state (e.g., "Show"/"Hide")?
- [ ] Does button respond to Enter and Space keys?
- [ ] Is icon (if present) marked with `aria-hidden="true"`?

## Quick Reference

```
✅ DO:
- Use <button> element for toggle control
- Include aria-expanded="true|false"
- Update aria-expanded when toggling
- Hide content with hidden attribute or display: none
- Optionally include aria-controls="{content-id}"
- Change button text to reflect state ("Show"/"Hide")
- Mark decorative icons with aria-hidden="true"
- Support Enter and Space keys (automatic with <button>)

❌ DON'T:
- Use div, span, or anchor for toggle control
- Omit aria-expanded attribute
- Leave aria-expanded out of sync with visibility
- Use visibility: hidden or opacity: 0 to hide content
- Forget to update button text on toggle
- Use interactive elements without button wrapper

## Disclosure vs Accordion:

Disclosure:
  - Single independent show/hide control
  - Button controls one content section
  - Simpler pattern for standalone toggles

Accordion:
  - Multiple related disclosure widgets
  - Buttons wrapped in headings
  - Content panels use role="region"
  - See accordion.instructions.md

## Common Use Cases:

- "Read more" / "Show less" links
- "Show details" / "Hide details"
- FAQ expand/collapse
- Product description expansion
- Comment thread expansion
- Filter panel toggles
```
