---
description: Instructions for proper button and clickable element accessibility
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Button and Clickable Element Accessibility

## CRITICAL RULES

**Any element that responds to clicks MUST be properly identified for assistive technologies.**

### 1. Use Proper Button Elements or Add role="button"

When creating clickable elements:
- **Preferred**: Use native `<button>` element
- **If using div/span**: MUST add `role="button"` and `tabindex="0"`

```html
✅ Good - Native button:
<button onclick="handleClick()">Click Me</button>

✅ Good - Div with role="button":
<div role="button" tabindex="0" onclick="handleClick()">Click Me</div>

❌ Bad - Clickable div without role:
<div onclick="handleClick()">Click Me</div>  <!-- Missing role="button"! -->
```

**Why this matters:**
- Screen readers need to know an element is clickable
- `role="button"` tells assistive technology this element can be activated
- `tabindex="0"` makes the element keyboard accessible

### 2. Buttons with Images Must Have aria-label

**When a button contains only an image (or icon), the button MUST have an `aria-label` describing its function.**

The `aria-label` should describe:
- **What the button DOES** (the action)
- NOT what the image looks like

```html
✅ Good - Button with image and aria-label:
<button aria-label="Close dialog">
  <img src="close-icon.png" alt="">
</button>

<div role="button" tabindex="0" aria-label="Delete item" onclick="deleteItem()">
  <img src="trash-icon.png" alt="">
</div>

<button aria-label="Submit form">
  <svg aria-hidden="true">
    <path d="..."/>
  </svg>
</button>

❌ Bad - Button with image but no aria-label:
<button>
  <img src="close-icon.png" alt="Close icon">  <!-- Button needs aria-label! -->
</button>

<div role="button" onclick="delete()">
  <img src="trash.png" alt="Trash">  <!-- Missing aria-label on button! -->
</div>
```

**Important notes:**
- When a button has `aria-label`, images inside should have `alt=""` or `aria-hidden="true"`
- The button's `aria-label` provides the accessible name, not the image
- Always describe the ACTION, not the appearance

### 3. Keyboard Accessibility for Custom Buttons

**Custom clickable elements (div/span with role="button") MUST be keyboard accessible:**

Required attributes:
- `role="button"` - Identifies as a button
- `tabindex="0"` - Makes it keyboard focusable
- Handle both click AND keyboard events (Enter/Space)

```html
✅ Good - Fully accessible custom button:
<div
  role="button"
  tabindex="0"
  aria-label="Open menu"
  onclick="openMenu()"
  onkeydown="handleKeyPress(event)">
  <img src="menu-icon.png" alt="">
</div>

<script>
function handleKeyPress(event) {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    openMenu();
  }
}
</script>

❌ Bad - Not keyboard accessible:
<div role="button" aria-label="Open menu" onclick="openMenu()">
  <!-- Missing tabindex="0"! -->
  <img src="menu-icon.png" alt="">
</div>
```

### 4. Text Buttons vs. Icon Buttons

**Text buttons** - Use text content for the label:
```html
✅ Good:
<button>Submit Form</button>
<button>Cancel</button>
<div role="button" tabindex="0">Learn More</div>
```

**Icon-only buttons** - MUST have `aria-label`:
```html
✅ Good:
<button aria-label="Search">
  <img src="search-icon.png" alt="">
</button>

<button aria-label="Settings">
  <svg aria-hidden="true">...</svg>
</button>
```

**Buttons with both text and icon** - Text provides the label:
```html
✅ Good:
<button>
  <img src="save-icon.png" alt="">
  Save
</button>

<button>
  <svg aria-hidden="true">...</svg>
  Delete Item
</button>
```

## Examples

### ✅ Good: Native Button with Image

```html
<button aria-label="Close notification">
  <img src="close.png" alt="">
</button>

<button aria-label="Add to cart">
  <svg aria-hidden="true" width="20" height="20">
    <path d="..."/>
  </svg>
</button>
```

### ✅ Good: Custom Clickable Div with Image

```html
<div
  role="button"
  tabindex="0"
  aria-label="Play video"
  onclick="playVideo()"
  onkeydown="handleKeyPress(event)">
  <img src="play-button.png" alt="">
</div>
```

### ✅ Good: Button with Text and Icon

```html
<!-- Text provides the label, image is decorative -->
<button onclick="save()">
  <img src="save-icon.png" alt="">
  Save Changes
</button>

<!-- Or with icon after text -->
<button onclick="download()">
  Download PDF
  <svg aria-hidden="true">
    <path d="..."/>
  </svg>
</button>
```

### ✅ Good: React/JSX Components

```jsx
// Icon-only button
<button aria-label="Delete item" onClick={handleDelete}>
  <img src={trashIcon} alt="" />
</button>

// Custom clickable div
<div
  role="button"
  tabIndex={0}
  aria-label="Toggle menu"
  onClick={toggleMenu}
  onKeyDown={handleKeyDown}>
  <img src={menuIcon} alt="" />
</div>

// Button with text and icon
<button onClick={handleSubmit}>
  <svg aria-hidden="true">...</svg>
  Submit Form
</button>
```

### ❌ Bad: Clickable Div Without role="button"

```html
<!-- NEVER do this -->
<div onclick="handleClick()">
  Click Me  <!-- Missing role="button" and tabindex! -->
</div>

<span onclick="delete()">
  <img src="trash.png" alt="Delete">  <!-- Missing role="button"! -->
</span>
```

### ❌ Bad: Button with Image but No aria-label

```html
<!-- Missing aria-label on button -->
<button>
  <img src="settings.png" alt="Settings icon">  <!-- Button needs aria-label! -->
</button>

<!-- Wrong: image alt is not enough for icon buttons -->
<div role="button" tabindex="0" onclick="close()">
  <img src="x.png" alt="X icon">  <!-- Div needs aria-label! -->
</div>

<!-- Correct versions: -->
<button aria-label="Open settings">
  <img src="settings.png" alt="">
</button>

<div role="button" tabindex="0" aria-label="Close" onclick="close()">
  <img src="x.png" alt="">
</div>
```

### ❌ Bad: Custom Button Missing Keyboard Support

```html
<!-- Missing tabindex -->
<div role="button" aria-label="Open menu" onclick="openMenu()">
  <img src="menu.png" alt="">
</div>

<!-- Correct: -->
<div
  role="button"
  tabindex="0"
  aria-label="Open menu"
  onclick="openMenu()"
  onkeydown="handleKeyPress(event)">
  <img src="menu.png" alt="">
</div>
```

## Framework-Specific Examples

### React

```jsx
// Icon button with proper accessibility
function IconButton({ onClick, ariaLabel, icon }) {
  return (
    <button aria-label={ariaLabel} onClick={onClick}>
      <img src={icon} alt="" />
    </button>
  );
}

// Custom clickable div
function CustomButton({ onClick, ariaLabel, children }) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      onClick();
    }
  };

  return (
    <div
      role="button"
      tabIndex={0}
      aria-label={ariaLabel}
      onClick={onClick}
      onKeyDown={handleKeyDown}>
      {children}
    </div>
  );
}

// Usage
<IconButton
  ariaLabel="Delete item"
  icon={trashIcon}
  onClick={handleDelete}
/>
```

### Vue

```vue
<template>
  <!-- Icon button -->
  <button :aria-label="buttonLabel" @click="handleClick">
    <img :src="iconSrc" alt="">
  </button>

  <!-- Custom clickable div -->
  <div
    role="button"
    tabindex="0"
    :aria-label="actionLabel"
    @click="handleAction"
    @keydown="handleKeyDown">
    <img :src="iconImage" alt="">
  </div>
</template>

<script>
export default {
  methods: {
    handleKeyDown(event) {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        this.handleAction();
      }
    }
  }
}
</script>
```

## Common Use Cases

### Close/Dismiss Buttons

```html
<!-- Modal close button -->
<button aria-label="Close dialog">
  <img src="close-icon.png" alt="">
</button>

<!-- Notification dismiss -->
<button aria-label="Dismiss notification">
  <svg aria-hidden="true">
    <path d="..."/>
  </svg>
</button>
```

### Navigation Buttons

```html
<!-- Menu toggle -->
<button aria-label="Toggle navigation menu">
  <img src="hamburger-icon.png" alt="">
</button>

<!-- Back button -->
<button aria-label="Go back">
  <svg aria-hidden="true">
    <path d="..."/>
  </svg>
</button>
```

### Action Buttons

```html
<!-- Edit button -->
<button aria-label="Edit profile">
  <img src="edit-icon.png" alt="">
</button>

<!-- Delete button -->
<button aria-label="Delete item">
  <img src="trash-icon.png" alt="">
</button>

<!-- Share button -->
<button aria-label="Share this page">
  <img src="share-icon.png" alt="">
</button>
```

### Social Media Buttons

```html
<button aria-label="Share on Facebook">
  <img src="facebook-icon.png" alt="">
</button>

<button aria-label="Share on Twitter">
  <img src="twitter-icon.png" alt="">
</button>
```

## WCAG References

- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 2.4.4**: Link Purpose (Level A)

## Implementation Checklist

When creating clickable elements:
- [ ] **Is a native `<button>` used when possible?** (PREFERRED)
- [ ] **Do clickable divs/spans have `role="button"`?** (CRITICAL)
- [ ] **Do custom buttons have `tabindex="0"`?** (CRITICAL for keyboard access)
- [ ] **Do icon-only buttons have `aria-label`?** (CRITICAL)
- [ ] **Do images inside labeled buttons have `alt=""`?** (CRITICAL)
- [ ] **Do custom buttons handle keyboard events (Enter/Space)?**
- [ ] **Does the aria-label describe the ACTION, not appearance?**
- [ ] **Are SVG icons marked with `aria-hidden="true"`?**

## Quick Reference

```
✅ ALWAYS:
- Use native <button> elements when possible
- Add role="button" to clickable divs/spans
- Add tabindex="0" to custom clickable elements
- Add aria-label to icon-only buttons (describing the ACTION)
- Handle keyboard events (Enter and Space) for custom buttons
- Use alt="" for images inside labeled buttons
- Mark decorative SVGs with aria-hidden="true"

❌ NEVER:
- Create clickable divs/spans without role="button"
- Forget tabindex="0" on custom clickable elements
- Omit aria-label from icon-only buttons
- Use image alt text as the only label for icon buttons
- Describe appearance instead of function in aria-label
- Make elements clickable without keyboard support

## Button Labeling Rules:

Icon-only button:
  <button aria-label="Close">
    <img src="x.png" alt="">
  </button>

Button with text:
  <button>
    Submit Form
  </button>

Button with text + icon:
  <button>
    <img src="icon.png" alt="">
    Save Changes
  </button>

Custom clickable div:
  <div role="button" tabindex="0" aria-label="Action">
    <img src="icon.png" alt="">
  </div>
```
