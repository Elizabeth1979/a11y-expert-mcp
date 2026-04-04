---
description: Instructions for proper tooltip accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Tooltip Accessibility

## CRITICAL RULES

**Tooltips display brief contextual information on hover or focus. They are non-focusable and automatically dismiss.**

### 1. Use role="tooltip" on Tooltip Container

**The tooltip element MUST have `role="tooltip"`.**

```html
✅ Good - Proper tooltip role:
<button aria-describedby="tooltip-1">
  Save
</button>

<div id="tooltip-1" role="tooltip" hidden>
  Save your changes
</div>

❌ Bad - Missing role="tooltip":
<button aria-describedby="tooltip-1">Save</button>
<div id="tooltip-1" hidden>  <!-- Missing role="tooltip"! -->
  Save your changes
</div>
```

### 2. Connect Trigger and Tooltip with aria-describedby

**The trigger element MUST reference the tooltip using `aria-describedby`.**

```html
✅ Good - Using aria-describedby:
<button aria-describedby="save-tooltip">
  <svg aria-hidden="true"><!-- save icon --></svg>
  Save
</button>

<div id="save-tooltip" role="tooltip" hidden>
  Save your changes (Ctrl+S)
</div>

❌ Bad - Missing aria-describedby:
<button id="save-btn">  <!-- Missing aria-describedby! -->
  Save
</button>
<div id="tooltip" role="tooltip" hidden>
  Save your changes
</div>
```

### 3. Tooltips Must Be Non-Focusable

**Tooltips MUST NOT receive keyboard focus. They appear on hover/focus of trigger element.**

```html
✅ Good - Tooltip has no tabindex:
<div id="tooltip" role="tooltip" hidden>
  Helpful information
</div>

❌ Bad - Tooltip is focusable:
<div id="tooltip" role="tooltip" tabindex="0" hidden>
  <!-- Tooltips should NOT be focusable! -->
</div>

❌ Bad - Tooltip contains focusable elements:
<div id="tooltip" role="tooltip">
  Click <a href="/help">here</a> for more.
  <!-- Don't put links in tooltips! Use dialog instead -->
</div>
```

**Important:** If the tooltip needs focusable content (links, buttons), use a **non-modal dialog** instead, not a tooltip.

### 4. Show Tooltip on Hover AND Focus

**Tooltips MUST appear on both mouse hover AND keyboard focus of the trigger.**

```javascript
// ✅ Good - Show on hover and focus
const trigger = document.getElementById('button');
const tooltip = document.getElementById('tooltip');

trigger.addEventListener('mouseenter', showTooltip);
trigger.addEventListener('focus', showTooltip);

trigger.addEventListener('mouseleave', hideTooltip);
trigger.addEventListener('blur', hideTooltip);

function showTooltip() {
  tooltip.removeAttribute('hidden');
}

function hideTooltip() {
  tooltip.setAttribute('hidden', '');
}
```

### 5. Dismiss Tooltip on Escape Key

**Tooltips MUST be dismissible with the Escape key.**

```javascript
// ✅ Good - Dismiss on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    const visibleTooltips = document.querySelectorAll('[role="tooltip"]:not([hidden])');
    visibleTooltips.forEach(tooltip => {
      tooltip.setAttribute('hidden', '');
    });
  }
});
```

## Complete Tooltip Structure

```html
<button
  id="delete-btn"
  aria-describedby="delete-tooltip"
  aria-label="Delete item">
  <svg aria-hidden="true" width="20" height="20">
    <!-- trash icon -->
  </svg>
</button>

<div id="delete-tooltip" role="tooltip" hidden>
  Permanently delete this item
</div>

<style>
#delete-tooltip {
  position: absolute;
  background: #333;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  white-space: nowrap;
  pointer-events: none; /* Prevents tooltip from blocking hover */
}
</style>

<script>
const button = document.getElementById('delete-btn');
const tooltip = document.getElementById('delete-tooltip');

// Show tooltip on hover and focus
button.addEventListener('mouseenter', showTooltip);
button.addEventListener('focus', showTooltip);

// Hide tooltip on mouse leave and blur
button.addEventListener('mouseleave', hideTooltip);
button.addEventListener('blur', hideTooltip);

// Dismiss on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    hideTooltip();
  }
});

function showTooltip() {
  tooltip.removeAttribute('hidden');
  positionTooltip();
}

function hideTooltip() {
  tooltip.setAttribute('hidden', '');
}

function positionTooltip() {
  const buttonRect = button.getBoundingClientRect();
  tooltip.style.top = `${buttonRect.bottom + 8}px`;
  tooltip.style.left = `${buttonRect.left}px`;
}
</script>
```

## Examples

### ✅ Good: Icon Button Tooltip

```html
<button aria-describedby="settings-tooltip" aria-label="Settings">
  <svg aria-hidden="true"><!-- gear icon --></svg>
</button>

<div id="settings-tooltip" role="tooltip" hidden>
  Open settings
</div>
```

### ✅ Good: Input Field Tooltip

```html
<label for="username">Username</label>
<input
  type="text"
  id="username"
  aria-describedby="username-tooltip">

<div id="username-tooltip" role="tooltip" hidden>
  Must be 3-20 characters, letters and numbers only
</div>
```

### ✅ Good: Abbreviation Tooltip

```html
<abbr aria-describedby="html-tooltip">HTML</abbr>

<div id="html-tooltip" role="tooltip" hidden>
  HyperText Markup Language
</div>
```

### ✅ Good: React Tooltip Component

```jsx
function Tooltip({ children, text }) {
  const [isVisible, setIsVisible] = React.useState(false);
  const tooltipId = React.useId();
  const triggerRef = React.useRef(null);

  React.useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        setIsVisible(false);
      }
    };

    document.addEventListener('keydown', handleEscape);
    return () => document.removeEventListener('keydown', handleEscape);
  }, []);

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <div
        ref={triggerRef}
        aria-describedby={tooltipId}
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        onFocus={() => setIsVisible(true)}
        onBlur={() => setIsVisible(false)}>
        {children}
      </div>

      {isVisible && (
        <div
          id={tooltipId}
          role="tooltip"
          style={{
            position: 'absolute',
            top: '100%',
            left: 0,
            marginTop: '8px',
            background: '#333',
            color: 'white',
            padding: '4px 8px',
            borderRadius: '4px',
            fontSize: '14px',
            whiteSpace: 'nowrap',
            pointerEvents: 'none',
            zIndex: 1000
          }}>
          {text}
        </div>
      )}
    </div>
  );
}

// Usage
<Tooltip text="Save your changes (Ctrl+S)">
  <button>Save</button>
</Tooltip>
```

### ✅ Good: Vue Tooltip Component

```vue
<template>
  <div class="tooltip-wrapper">
    <div
      :aria-describedby="tooltipId"
      @mouseenter="show"
      @mouseleave="hide"
      @focus="show"
      @blur="hide">
      <slot></slot>
    </div>

    <div
      v-if="isVisible"
      :id="tooltipId"
      role="tooltip"
      class="tooltip">
      {{ text }}
    </div>
  </div>
</template>

<script>
export default {
  props: {
    text: String
  },
  data() {
    return {
      isVisible: false,
      tooltipId: `tooltip-${Math.random().toString(36).substr(2, 9)}`
    };
  },
  mounted() {
    document.addEventListener('keydown', this.handleEscape);
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleEscape);
  },
  methods: {
    show() {
      this.isVisible = true;
    },
    hide() {
      this.isVisible = false;
    },
    handleEscape(e) {
      if (e.key === 'Escape') {
        this.isVisible = false;
      }
    }
  }
};
</script>

<style scoped>
.tooltip-wrapper {
  position: relative;
  display: inline-block;
}

.tooltip {
  position: absolute;
  top: 100%;
  left: 0;
  margin-top: 8px;
  background: #333;
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
  white-space: nowrap;
  pointer-events: none;
  z-index: 1000;
}
</style>
```

### ❌ Bad Examples

```html
<!-- Missing role="tooltip" -->
<button aria-describedby="tooltip-1">Save</button>
<div id="tooltip-1" hidden>Save changes</div>

<!-- Missing aria-describedby -->
<button id="save-btn">Save</button>
<div role="tooltip" hidden>Save changes</div>

<!-- Tooltip is focusable (wrong!) -->
<div id="tooltip" role="tooltip" tabindex="0">
  Tooltip content
</div>

<!-- Tooltip contains focusable elements (wrong!) -->
<div role="tooltip">
  Click <a href="/help">here</a> for help.
  <!-- Use dialog instead! -->
</div>

<!-- Only shows on hover, not on focus -->
<button onmouseenter="show()" onmouseleave="hide()">
  Help
  <!-- Missing focus event handlers! -->
</button>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 1.4.13**: Content on Hover or Focus (Level AA)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)

## Implementation Checklist

- [ ] **Does tooltip have `role="tooltip"`?** (CRITICAL)
- [ ] **Does trigger have `aria-describedby` referencing tooltip?** (CRITICAL)
- [ ] **Is tooltip non-focusable (no tabindex)?** (CRITICAL)
- [ ] **Does tooltip appear on both hover AND focus?** (CRITICAL)
- [ ] **Does tooltip dismiss on blur/mouseleave?** (CRITICAL)
- [ ] **Can tooltip be dismissed with Escape key?** (CRITICAL)
- [ ] Is tooltip hidden when not visible (using `hidden` attribute)?
- [ ] Does tooltip contain only plain text (no interactive elements)?
- [ ] Is tooltip positioned accessibly (doesn't obstruct content)?
- [ ] Does tooltip have appropriate delay before appearing?

## Quick Reference

```
✅ DO:
- Use role="tooltip"
- Connect with aria-describedby on trigger
- Keep tooltip non-focusable (no tabindex)
- Show on both hover AND focus
- Hide on blur and mouseleave
- Dismiss with Escape key
- Use plain text only (no links/buttons)
- Position tooltip near trigger
- Add small delay before showing (~500ms)
- Use hidden attribute when not visible

❌ DON'T:
- Make tooltip focusable
- Put interactive elements in tooltip
- Show only on hover (must work on focus too)
- Forget aria-describedby connection
- Omit role="tooltip"
- Forget Escape key dismissal
- Block content with tooltip
- Use tooltip for critical information
- Use tooltip for long text (use dialog instead)

## Tooltip vs Dialog:

Tooltip:
  - Brief contextual information
  - Non-focusable
  - Plain text only
  - Appears on hover/focus
  - Auto-dismisses

Dialog:
  - Complex content
  - Can contain interactive elements (links, buttons)
  - User must explicitly close
  - Use when tooltip needs focusable content

## Common Use Cases:

✅ Good uses:
- Icon button labels
- Form field hints
- Abbreviation expansions
- Brief help text
- Keyboard shortcuts

❌ Don't use for:
- Critical information
- Long explanations
- Interactive content
- Forms or inputs
- Required reading
```
