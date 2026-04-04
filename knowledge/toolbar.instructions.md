---
description: Instructions for proper toolbar accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Toolbar Accessibility

## CRITICAL RULES

**Toolbars group related controls (buttons, toggles, menus) into a single tab stop with arrow key navigation. Use only when grouping 3+ controls.**

### 1. Use role="toolbar" Only for 3+ Controls

**Toolbars SHOULD only be used when grouping 3 or more controls.**

```html
✅ Good - Toolbar with multiple controls:
<div role="toolbar" aria-label="Text formatting">
  <button>Bold</button>
  <button>Italic</button>
  <button>Underline</button>
  <button>Strikethrough</button>
</div>

❌ Bad - Toolbar with only 2 controls:
<div role="toolbar" aria-label="Actions">
  <button>Save</button>
  <button>Cancel</button>
  <!-- Only 2 controls - don't use toolbar! -->
</div>
```

**Why**: Toolbars add navigation complexity. For 1-2 controls, regular buttons are simpler.

### 2. Provide Accessible Label

**Toolbars MUST have an accessible label using `aria-label` or `aria-labelledby`.**

```html
✅ Good - Using aria-label:
<div role="toolbar" aria-label="Text formatting">
  <button>Bold</button>
  <button>Italic</button>
</div>

✅ Good - Using aria-labelledby:
<h3 id="formatting-label">Formatting Tools</h3>
<div role="toolbar" aria-labelledby="formatting-label">
  <button>Bold</button>
  <button>Italic</button>
</div>

❌ Bad - No accessible label:
<div role="toolbar">
  <button>Bold</button>  <!-- What toolbar is this? -->
</div>
```

### 3. Implement Roving tabindex Navigation

**Tab enters/exits toolbar. Arrow keys navigate between controls. Only one control has `tabindex="0"`.**

```html
✅ Good - Roving tabindex:
<div role="toolbar" aria-label="Text formatting">
  <button tabindex="0">Bold</button>  <!-- First or last-focused -->
  <button tabindex="-1">Italic</button>
  <button tabindex="-1">Underline</button>
</div>

<script>
toolbar.addEventListener('keydown', (e) => {
  const buttons = toolbar.querySelectorAll('button');
  const currentIndex = Array.from(buttons).indexOf(document.activeElement);

  let nextIndex = currentIndex;

  if (e.key === 'ArrowRight') {
    e.preventDefault();
    nextIndex = currentIndex + 1;
    if (nextIndex >= buttons.length) nextIndex = 0; // Wrap
  } else if (e.key === 'ArrowLeft') {
    e.preventDefault();
    nextIndex = currentIndex - 1;
    if (nextIndex < 0) nextIndex = buttons.length - 1; // Wrap
  }

  if (nextIndex !== currentIndex) {
    buttons[currentIndex].tabIndex = -1;
    buttons[nextIndex].tabIndex = 0;
    buttons[nextIndex].focus();
  }
});
</script>

❌ Bad - All controls in tab sequence:
<div role="toolbar" aria-label="Formatting">
  <button tabindex="0">Bold</button>
  <button tabindex="0">Italic</button>  <!-- Wrong! Should be -1 -->
  <button tabindex="0">Underline</button>  <!-- Wrong! Should be -1 -->
</div>
```

### 4. Use Arrow Keys for Navigation

**For horizontal toolbars: Right/Left arrows. For vertical: Down/Up arrows.**

**Horizontal toolbar** (default):
- **Right Arrow**: Next control (with optional wrap)
- **Left Arrow**: Previous control (with optional wrap)
- **Home**: First control (optional)
- **End**: Last control (optional)

**Vertical toolbar**:
- **Down Arrow**: Next control
- **Up Arrow**: Previous control
- **Home**: First control (optional)
- **End**: Last control (optional)

```html
✅ Good - Vertical toolbar:
<div
  role="toolbar"
  aria-orientation="vertical"
  aria-label="Alignment">
  <button tabindex="0">Align Left</button>
  <button tabindex="-1">Align Center</button>
  <button tabindex="-1">Align Right</button>
</div>

<script>
toolbar.addEventListener('keydown', (e) => {
  const buttons = toolbar.querySelectorAll('button');
  const currentIndex = Array.from(buttons).indexOf(document.activeElement);

  let nextIndex = currentIndex;

  // Vertical toolbar uses Up/Down arrows
  if (e.key === 'ArrowDown') {
    e.preventDefault();
    nextIndex = currentIndex + 1;
    if (nextIndex >= buttons.length) nextIndex = 0;
  } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    nextIndex = currentIndex - 1;
    if (nextIndex < 0) nextIndex = buttons.length - 1;
  }

  if (nextIndex !== currentIndex) {
    buttons[currentIndex].tabIndex = -1;
    buttons[nextIndex].tabIndex = 0;
    buttons[nextIndex].focus();
  }
});
</script>
```

### 5. Avoid Controls That Need Arrow Keys

**Don't include controls that require arrow keys (like spinbuttons) in toolbars. If unavoidable, place them last.**

```html
✅ Good - Simple button controls only:
<div role="toolbar" aria-label="Formatting">
  <button>Bold</button>
  <button>Italic</button>
  <button>Underline</button>
</div>

⚠️ Acceptable with caution - Spinbutton at end:
<div role="toolbar" aria-label="Formatting">
  <button tabindex="0">Bold</button>
  <button tabindex="-1">Italic</button>
  <!-- Spinbutton last, so users can still navigate toolbar -->
  <input
    type="number"
    role="spinbutton"
    aria-label="Font size"
    tabindex="-1">
</div>

❌ Bad - Complex control in middle:
<div role="toolbar" aria-label="Tools">
  <button>Bold</button>
  <input type="number" role="spinbutton">  <!-- Conflicts with toolbar arrows! -->
  <button>Italic</button>
</div>
```

## Complete Toolbar Structure

```html
<div
  id="text-toolbar"
  role="toolbar"
  aria-label="Text formatting"
  aria-controls="editor">

  <button
    type="button"
    aria-label="Bold"
    aria-pressed="false"
    tabindex="0">
    <strong>B</strong>
  </button>

  <button
    type="button"
    aria-label="Italic"
    aria-pressed="false"
    tabindex="-1">
    <em>I</em>
  </button>

  <button
    type="button"
    aria-label="Underline"
    aria-pressed="false"
    tabindex="-1">
    <u>U</u>
  </button>

  <div role="separator"></div>

  <button
    type="button"
    aria-label="Align left"
    tabindex="-1">
    ≣
  </button>

  <button
    type="button"
    aria-label="Align center"
    tabindex="-1">
    ≡
  </button>

  <button
    type="button"
    aria-label="Align right"
    tabindex="-1">
    ≢
  </button>
</div>

<textarea id="editor" aria-label="Text editor"></textarea>

<script>
const toolbar = document.getElementById('text-toolbar');
const controls = Array.from(toolbar.querySelectorAll('button'));

toolbar.addEventListener('keydown', (e) => {
  const currentIndex = controls.indexOf(document.activeElement);

  if (currentIndex === -1) return;

  let nextIndex = currentIndex;

  switch(e.key) {
    case 'ArrowRight':
      e.preventDefault();
      nextIndex = (currentIndex + 1) % controls.length;
      break;

    case 'ArrowLeft':
      e.preventDefault();
      nextIndex = (currentIndex - 1 + controls.length) % controls.length;
      break;

    case 'Home':
      e.preventDefault();
      nextIndex = 0;
      break;

    case 'End':
      e.preventDefault();
      nextIndex = controls.length - 1;
      break;

    default:
      return;
  }

  if (nextIndex !== currentIndex) {
    controls[currentIndex].tabIndex = -1;
    controls[nextIndex].tabIndex = 0;
    controls[nextIndex].focus();
  }
});

// Handle button activation
controls.forEach(button => {
  button.addEventListener('click', (e) => {
    const pressed = button.getAttribute('aria-pressed');

    if (pressed !== null) {
      // Toggle button
      button.setAttribute('aria-pressed', pressed === 'true' ? 'false' : 'true');
    }

    // Perform action
    console.log(`${button.getAttribute('aria-label')} activated`);
  });
});
</script>
```

## Examples

### ✅ Good: Simple Formatting Toolbar

```html
<div role="toolbar" aria-label="Text formatting">
  <button aria-label="Bold" aria-pressed="false" tabindex="0">
    <strong>B</strong>
  </button>
  <button aria-label="Italic" aria-pressed="false" tabindex="-1">
    <em>I</em>
  </button>
  <button aria-label="Underline" aria-pressed="false" tabindex="-1">
    <u>U</u>
  </button>
</div>
```

### ✅ Good: Vertical Toolbar

```html
<div
  role="toolbar"
  aria-orientation="vertical"
  aria-label="Drawing tools">
  <button aria-label="Select tool" tabindex="0">
    <svg aria-hidden="true"><!-- pointer icon --></svg>
  </button>
  <button aria-label="Pen tool" tabindex="-1">
    <svg aria-hidden="true"><!-- pen icon --></svg>
  </button>
  <button aria-label="Eraser tool" tabindex="-1">
    <svg aria-hidden="true"><!-- eraser icon --></svg>
  </button>
</div>
```

### ✅ Good: React Toolbar Component

```jsx
function Toolbar({ label, orientation = 'horizontal', children }) {
  const toolbarRef = useRef(null);
  const [focusedIndex, setFocusedIndex] = useState(0);

  const handleKeyDown = (e) => {
    const buttons = toolbarRef.current.querySelectorAll('button');
    const currentIndex = Array.from(buttons).indexOf(document.activeElement);

    if (currentIndex === -1) return;

    let nextIndex = currentIndex;

    const isVertical = orientation === 'vertical';
    const nextKey = isVertical ? 'ArrowDown' : 'ArrowRight';
    const prevKey = isVertical ? 'ArrowUp' : 'ArrowLeft';

    switch(e.key) {
      case nextKey:
        e.preventDefault();
        nextIndex = (currentIndex + 1) % buttons.length;
        break;

      case prevKey:
        e.preventDefault();
        nextIndex = (currentIndex - 1 + buttons.length) % buttons.length;
        break;

      case 'Home':
        e.preventDefault();
        nextIndex = 0;
        break;

      case 'End':
        e.preventDefault();
        nextIndex = buttons.length - 1;
        break;

      default:
        return;
    }

    if (nextIndex !== currentIndex) {
      buttons[currentIndex].tabIndex = -1;
      buttons[nextIndex].tabIndex = 0;
      buttons[nextIndex].focus();
      setFocusedIndex(nextIndex);
    }
  };

  return (
    <div
      ref={toolbarRef}
      role="toolbar"
      aria-label={label}
      aria-orientation={orientation}
      onKeyDown={handleKeyDown}>
      {React.Children.map(children, (child, index) => {
        if (React.isValidElement(child)) {
          return React.cloneElement(child, {
            tabIndex: index === focusedIndex ? 0 : -1
          });
        }
        return child;
      })}
    </div>
  );
}

// Usage
<Toolbar label="Text formatting">
  <button aria-label="Bold" aria-pressed={false}>
    <strong>B</strong>
  </button>
  <button aria-label="Italic" aria-pressed={false}>
    <em>I</em>
  </button>
  <button aria-label="Underline" aria-pressed={false}>
    <u>U</u>
  </button>
</Toolbar>
```

### ❌ Bad Examples

```html
<!-- Missing aria-label -->
<div role="toolbar">
  <button>Bold</button>  <!-- What toolbar is this? -->
</div>

<!-- All buttons in tab sequence -->
<div role="toolbar" aria-label="Formatting">
  <button tabindex="0">Bold</button>
  <button tabindex="0">Italic</button>  <!-- Should be -1! -->
</div>

<!-- Only 2 controls -->
<div role="toolbar" aria-label="Actions">
  <button>Save</button>
  <button>Cancel</button>
  <!-- Use regular buttons instead -->
</div>

<!-- No keyboard navigation -->
<div role="toolbar" aria-label="Tools">
  <button>Cut</button>
  <button>Copy</button>
  <button>Paste</button>
  <!-- Missing arrow key handlers! -->
</div>
```

## WCAG References

- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 2.4.3**: Focus Order (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does toolbar have `role="toolbar"`?** (CRITICAL)
- [ ] **Does toolbar have accessible label?** (CRITICAL)
- [ ] **Does toolbar contain 3+ controls?** (CRITICAL - otherwise don't use toolbar)
- [ ] **Is roving tabindex implemented?** (CRITICAL)
- [ ] **Do arrow keys navigate between controls?** (CRITICAL)
- [ ] Is only one control in tab sequence (tabindex="0")?
- [ ] Is `aria-orientation="vertical"` set for vertical toolbars?
- [ ] Do Home/End keys work (optional)?
- [ ] Are toggle buttons using `aria-pressed`?
- [ ] Do controls have accessible labels?
- [ ] Are complex controls (spinbuttons) avoided or placed last?

## Quick Reference

```
✅ DO:
- Use role="toolbar" for groups of 3+ controls
- Provide accessible label (aria-label or aria-labelledby)
- Implement roving tabindex (one control with tabindex="0")
- Support arrow key navigation
- Use aria-orientation="vertical" for vertical toolbars
- Use simple controls (buttons, toggles)
- Place complex controls at end if needed
- Update aria-pressed for toggle buttons
- Support Home/End keys (optional)
- Allow wrapping with arrow keys

❌ DON'T:
- Use toolbar for 1-2 controls
- Forget accessible label
- Put all controls in tab sequence
- Skip arrow key navigation
- Include controls that need arrow keys (spinbuttons, sliders)
- Forget to update tabindex when focus moves
- Use for unrelated controls

## Toolbar Best Practices:

Use toolbar when:
  ✓ Grouping 3+ related controls
  ✓ Controls are simple (buttons, toggles)
  ✓ Users need quick sequential access
  ✓ Controls perform related actions

Don't use toolbar when:
  ✗ Only 1-2 controls (use regular buttons)
  ✗ Controls are unrelated
  ✗ Controls need arrow keys themselves
  ✗ Layout is only visual grouping

## Keyboard Pattern:

Tab/Shift+Tab:
  - Enter/exit toolbar
  - First focus: First control or last-focused control

Arrow Right/Left (horizontal):
  - Navigate to next/previous control
  - Optional: Wrap at ends

Arrow Down/Up (vertical):
  - Navigate to next/previous control
  - Optional: Wrap at ends

Home/End (optional):
  - Jump to first/last control
```
