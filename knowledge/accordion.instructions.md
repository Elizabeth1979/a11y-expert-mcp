---
description: Instructions for proper accordion accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Accordion Accessibility

## CRITICAL RULES

**Accordions are vertically stacked collapsible sections that allow users to show/hide content panels.**

### 1. Use Button Elements with aria-expanded

**Every accordion header MUST be a `<button>` element with `aria-expanded` state.**

- `aria-expanded="true"` when panel is visible
- `aria-expanded="false"` when panel is hidden
- `aria-controls="{panel-id}"` referencing the panel element

```html
✅ Good - Button with aria-expanded:
<button
  id="accordion-btn-1"
  aria-expanded="false"
  aria-controls="accordion-panel-1">
  Section Title
</button>

❌ Bad - Missing aria-expanded:
<button id="accordion-btn-1">
  Section Title
</button>

❌ Bad - Using div instead of button:
<div onclick="toggle()">  <!-- Should be <button>! -->
  Section Title
</div>
```

### 2. Wrap Buttons in Heading Elements

**Accordion buttons MUST be wrapped in heading elements (`<h2>`, `<h3>`, etc.) to establish proper document structure.**

The heading level should reflect the page's heading hierarchy.

```html
✅ Good - Button wrapped in heading:
<h3>
  <button
    aria-expanded="false"
    aria-controls="panel-1">
    Section 1
  </button>
</h3>

❌ Bad - Button not in heading:
<button aria-expanded="false" aria-controls="panel-1">
  Section 1
</button>

❌ Bad - Heading inside button:
<button>
  <h3>Section 1</h3>  <!-- Wrong structure! -->
</button>
```

**Why this matters:**
- Screen readers use heading navigation to understand page structure
- Users can jump between accordion sections using heading shortcuts
- Maintains proper semantic hierarchy

### 3. Use role="region" for Panel Containers

**Panel containers SHOULD use `role="region"` with `aria-labelledby` referencing the button.**

This is especially important when panels contain headings or nested accordions.

```html
✅ Good - Panel with role="region":
<div
  id="panel-1"
  role="region"
  aria-labelledby="btn-1"
  hidden>
  <p>Panel content...</p>
</div>

✅ Good - Without role="region" (simpler content):
<div id="panel-1" hidden>
  <p>Simple content without headings</p>
</div>

❌ Bad - Missing aria-labelledby on region:
<div id="panel-1" role="region" hidden>  <!-- Missing aria-labelledby! -->
  <p>Content...</p>
</div>
```

**Guidelines:**
- Use `role="region"` when panel has headings or complex structure
- Limit to ~6 or fewer simultaneous region roles on a page
- For simple text content, `role="region"` is optional

### 4. Implement Keyboard Navigation

**Accordion buttons MUST be keyboard accessible with proper interactions.**

Required keyboard support:
- **Enter or Space**: Toggle panel expanded/collapsed
- **Tab**: Move focus to next focusable element
- **Shift+Tab**: Move focus to previous focusable element

Optional (recommended) keyboard support:
- **Down Arrow**: Move focus to next accordion header
- **Up Arrow**: Move focus to previous accordion header
- **Home**: Move focus to first accordion header
- **End**: Move focus to last accordion header

```javascript
// ✅ Good - Keyboard event handling
function handleKeyDown(event) {
  const key = event.key;

  if (key === 'Enter' || key === ' ') {
    event.preventDefault();
    togglePanel(event.target);
  } else if (key === 'ArrowDown') {
    focusNextHeader();
  } else if (key === 'ArrowUp') {
    focusPreviousHeader();
  } else if (key === 'Home') {
    focusFirstHeader();
  } else if (key === 'End') {
    focusLastHeader();
  }
}
```

### 5. Hide Collapsed Panels Properly

**Collapsed panels MUST be hidden from screen readers and keyboard navigation.**

Use the `hidden` attribute (preferred) or CSS `display: none`.

```html
✅ Good - Using hidden attribute:
<div id="panel-1" role="region" aria-labelledby="btn-1" hidden>
  <p>Hidden content</p>
</div>

✅ Good - Using CSS display:
<div id="panel-1" role="region" aria-labelledby="btn-1" style="display: none;">
  <p>Hidden content</p>
</div>

❌ Bad - Using visibility: hidden or opacity:
<div id="panel-1" role="region" aria-labelledby="btn-1" style="visibility: hidden;">
  <!-- Still in keyboard tab sequence! -->
</div>

❌ Bad - Using aria-hidden without hiding visually:
<div id="panel-1" role="region" aria-labelledby="btn-1" aria-hidden="true">
  <!-- Content still visible! -->
</div>
```

## Complete Accordion Structure

```html
<div class="accordion">
  <h3>
    <button
      id="accordion-button-1"
      aria-expanded="false"
      aria-controls="accordion-panel-1">
      Section 1: Getting Started
    </button>
  </h3>
  <div
    id="accordion-panel-1"
    role="region"
    aria-labelledby="accordion-button-1"
    hidden>
    <p>Content for section 1...</p>
  </div>

  <h3>
    <button
      id="accordion-button-2"
      aria-expanded="true"
      aria-controls="accordion-panel-2">
      Section 2: Configuration
    </button>
  </h3>
  <div
    id="accordion-panel-2"
    role="region"
    aria-labelledby="accordion-button-2">
    <p>Content for section 2...</p>
  </div>

  <h3>
    <button
      id="accordion-button-3"
      aria-expanded="false"
      aria-controls="accordion-panel-3">
      Section 3: Advanced Topics
    </button>
  </h3>
  <div
    id="accordion-panel-3"
    role="region"
    aria-labelledby="accordion-button-3"
    hidden>
    <p>Content for section 3...</p>
  </div>
</div>
```

## Examples

### ✅ Good: Basic Accordion

```html
<div class="accordion">
  <h2>
    <button
      id="btn-faq-1"
      aria-expanded="false"
      aria-controls="panel-faq-1">
      What is your return policy?
    </button>
  </h2>
  <div
    id="panel-faq-1"
    role="region"
    aria-labelledby="btn-faq-1"
    hidden>
    <p>You can return items within 30 days of purchase...</p>
  </div>

  <h2>
    <button
      id="btn-faq-2"
      aria-expanded="false"
      aria-controls="panel-faq-2">
      How do I track my order?
    </button>
  </h2>
  <div
    id="panel-faq-2"
    role="region"
    aria-labelledby="btn-faq-2"
    hidden>
    <p>You can track your order using the tracking number...</p>
  </div>
</div>
```

### ✅ Good: Accordion with Icon Indicators

```html
<h3>
  <button
    id="accordion-btn-1"
    aria-expanded="false"
    aria-controls="accordion-panel-1">
    <svg aria-hidden="true" class="icon">
      <use href="#icon-chevron"></use>
    </svg>
    Features
  </button>
</h3>
<div
  id="accordion-panel-1"
  role="region"
  aria-labelledby="accordion-btn-1"
  hidden>
  <ul>
    <li>Feature 1</li>
    <li>Feature 2</li>
  </ul>
</div>
```

**Note**: Icons should be marked with `aria-hidden="true"` since the button text provides the label.

### ✅ Good: Accordion Allowing Multiple Panels Open

```html
<!-- Multiple panels can be expanded simultaneously -->
<div class="accordion" data-allow-multiple="true">
  <h3>
    <button aria-expanded="true" aria-controls="panel-1">
      Section 1
    </button>
  </h3>
  <div id="panel-1" role="region" aria-labelledby="btn-1">
    <p>First section content (expanded)</p>
  </div>

  <h3>
    <button aria-expanded="true" aria-controls="panel-2">
      Section 2
    </button>
  </h3>
  <div id="panel-2" role="region" aria-labelledby="btn-2">
    <p>Second section content (also expanded)</p>
  </div>
</div>
```

### ✅ Good: React/JSX Accordion Component

```jsx
function Accordion({ items }) {
  const [openIndex, setOpenIndex] = React.useState(null);

  const togglePanel = (index) => {
    setOpenIndex(openIndex === index ? null : index);
  };

  return (
    <div className="accordion">
      {items.map((item, index) => {
        const isOpen = openIndex === index;
        const buttonId = `accordion-btn-${index}`;
        const panelId = `accordion-panel-${index}`;

        return (
          <div key={index}>
            <h3>
              <button
                id={buttonId}
                aria-expanded={isOpen}
                aria-controls={panelId}
                onClick={() => togglePanel(index)}>
                {item.title}
              </button>
            </h3>
            <div
              id={panelId}
              role="region"
              aria-labelledby={buttonId}
              hidden={!isOpen}>
              <p>{item.content}</p>
            </div>
          </div>
        );
      })}
    </div>
  );
}

// Usage
<Accordion
  items={[
    { title: 'Section 1', content: 'Content for section 1...' },
    { title: 'Section 2', content: 'Content for section 2...' },
    { title: 'Section 3', content: 'Content for section 3...' }
  ]}
/>
```

### ✅ Good: Vue Accordion Component

```vue
<template>
  <div class="accordion">
    <div v-for="(item, index) in items" :key="index">
      <h3>
        <button
          :id="`accordion-btn-${index}`"
          :aria-expanded="openIndex === index"
          :aria-controls="`accordion-panel-${index}`"
          @click="togglePanel(index)">
          {{ item.title }}
        </button>
      </h3>
      <div
        :id="`accordion-panel-${index}`"
        role="region"
        :aria-labelledby="`accordion-btn-${index}`"
        :hidden="openIndex !== index">
        <p>{{ item.content }}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    items: Array
  },
  data() {
    return {
      openIndex: null
    };
  },
  methods: {
    togglePanel(index) {
      this.openIndex = this.openIndex === index ? null : index;
    }
  }
};
</script>
```

### ❌ Bad: Missing Required ARIA Attributes

```html
<!-- Missing aria-expanded and aria-controls -->
<h3>
  <button id="btn-1">
    Section 1
  </button>
</h3>
<div id="panel-1" hidden>
  <p>Content...</p>
</div>
```

### ❌ Bad: Wrong HTML Structure

```html
<!-- Button not wrapped in heading -->
<button aria-expanded="false" aria-controls="panel-1">
  Section 1
</button>
<div id="panel-1" role="region" hidden>
  <p>Content...</p>
</div>

<!-- Heading inside button (wrong!) -->
<button aria-expanded="false">
  <h3>Section 1</h3>
</button>
```

### ❌ Bad: Using div Instead of Button

```html
<!-- Clickable div without role="button" -->
<h3>
  <div onclick="toggle()" aria-expanded="false">
    Section 1
  </div>
</h3>
```

### ❌ Bad: Improper Panel Hiding

```html
<!-- Using visibility: hidden leaves content in keyboard sequence -->
<div
  id="panel-1"
  role="region"
  aria-labelledby="btn-1"
  style="visibility: hidden;">
  <p>Still keyboard accessible!</p>
</div>

<!-- Using aria-hidden without visual hiding -->
<div
  id="panel-1"
  role="region"
  aria-hidden="true">
  <p>Still visible on screen!</p>
</div>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)
- **WCAG 2.1 Success Criterion 2.4.6**: Headings and Labels (Level AA)

## Implementation Checklist

When creating accordions:
- [ ] **Is each accordion header a `<button>` element?** (CRITICAL)
- [ ] **Does each button have `aria-expanded` attribute?** (CRITICAL)
- [ ] **Does each button have `aria-controls` referencing its panel?** (CRITICAL)
- [ ] **Is each button wrapped in a heading element (`<h2>`, `<h3>`, etc.)?** (CRITICAL)
- [ ] **Does each panel have `role="region"` when containing complex content?** (CRITICAL)
- [ ] **Does each region have `aria-labelledby` referencing its button?** (CRITICAL when using region)
- [ ] **Are collapsed panels hidden using `hidden` attribute or `display: none`?** (CRITICAL)
- [ ] Do buttons respond to Enter and Space keys?
- [ ] Are arrow keys implemented for optional enhanced keyboard navigation?
- [ ] Do panel IDs and button IDs match aria-controls and aria-labelledby references?
- [ ] Is the heading level appropriate for the page hierarchy?
- [ ] Are icons marked with `aria-hidden="true"`?

## Quick Reference

```
✅ DO:
- Use <button> elements for accordion headers
- Include aria-expanded="true|false" on buttons
- Include aria-controls="{panel-id}" on buttons
- Wrap buttons in heading elements (h2, h3, etc.)
- Use role="region" for panels with complex content
- Include aria-labelledby="{button-id}" on regions
- Hide collapsed panels with hidden attribute or display: none
- Implement keyboard navigation (Enter, Space, arrows)
- Use appropriate heading levels for page hierarchy
- Allow Enter and Space to toggle panels

❌ DON'T:
- Use div or span instead of button for headers
- Omit aria-expanded or aria-controls attributes
- Put heading inside button (wrong structure)
- Forget to wrap button in heading element
- Use visibility: hidden or opacity to hide panels
- Use aria-hidden without visually hiding content
- Skip keyboard event handling
- Use too many role="region" on one page (limit ~6)
- Forget to update aria-expanded when toggling
- Leave panel content visible when aria-expanded="false"

## Accordion Behavior Options:

Single-panel mode (only one open at a time):
  - Expanding panel automatically collapses others
  - Common for FAQs, settings

Multi-panel mode (multiple can be open):
  - Expanding panel doesn't affect others
  - Common for filters, forms

Collapsible all (all panels can close):
  - User can close all panels
  - Most common pattern

At least one open:
  - At least one panel always visible
  - Use aria-disabled="true" on active panel button
```
