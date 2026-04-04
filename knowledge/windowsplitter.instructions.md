---
description: Instructions for proper window splitter accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Window Splitter Accessibility

## CRITICAL RULES

**Window splitters (resize handles) allow users to adjust the size of adjacent panes. They must be keyboard accessible with clear feedback.**

### 1. Use role="separator" with aria-valuenow/min/max

**Splitters MUST use `role="separator"` with `aria-valuenow`, `aria-valuemin`, and `aria-valuemax`.**

```html
✅ Good - Proper splitter:
<div
  role="separator"
  aria-label="Resize navigation panel"
  aria-valuenow="25"
  aria-valuemin="10"
  aria-valuemax="90"
  aria-controls="nav-panel"
  tabindex="0">
</div>

❌ Bad - Missing ARIA attributes:
<div
  role="separator"
  aria-label="Resize"
  tabindex="0">
  <!-- Missing aria-valuenow, aria-valuemin, aria-valuemax! -->
</div>
```

**Value represents position**: `0` = primary pane smallest, `100` = primary pane largest.

### 2. Splitters Must Be Keyboard Focusable

**Splitters MUST have `tabindex="0"` to be keyboard accessible.**

```html
✅ Good - Focusable splitter:
<div
  role="separator"
  aria-label="Resize sidebar"
  aria-valuenow="30"
  aria-valuemin="0"
  aria-valuemax="100"
  tabindex="0">
</div>

❌ Bad - Not focusable:
<div
  role="separator"
  aria-label="Resize sidebar">
  <!-- Missing tabindex! Can't use keyboard -->
</div>
```

### 3. Implement Arrow Key Resizing

**Required keyboard interactions:**

**For vertical splitters** (left/right resize):
- **Right Arrow**: Increase primary pane size (increase value)
- **Left Arrow**: Decrease primary pane size (decrease value)

**For horizontal splitters** (top/bottom resize):
- **Down Arrow**: Increase primary pane size (increase value)
- **Up Arrow**: Decrease primary pane size (decrease value)

**Common keys**:
- **Enter**: Toggle collapse/restore primary pane
- **Home**: Minimize primary pane (optional)
- **End**: Maximize primary pane (optional)
- **F6**: Cycle through panes (optional)

```javascript
splitter.addEventListener('keydown', (e) => {
  let value = parseInt(splitter.getAttribute('aria-valuenow'));
  const min = parseInt(splitter.getAttribute('aria-valuemin'));
  const max = parseInt(splitter.getAttribute('aria-valuemax'));

  const step = 5; // Percentage points

  switch(e.key) {
    case 'ArrowRight': // For vertical splitter
      e.preventDefault();
      value = Math.min(value + step, max);
      break;

    case 'ArrowLeft': // For vertical splitter
      e.preventDefault();
      value = Math.max(value - step, min);
      break;

    case 'Home':
      e.preventDefault();
      value = min;
      break;

    case 'End':
      e.preventDefault();
      value = max;
      break;

    case 'Enter':
      e.preventDefault();
      toggleCollapse();
      return;
  }

  updateSplitter(value);
});
```

### 4. Label Splitter After Primary Pane

**Splitter label SHOULD describe what is being resized (the primary pane).**

```html
✅ Good - Clear labels:
<!-- Vertical splitter -->
<div
  role="separator"
  aria-label="Resize navigation panel"
  aria-controls="nav-panel"
  ...>
</div>

<!-- Horizontal splitter -->
<div
  role="separator"
  aria-label="Resize code editor"
  aria-controls="editor-panel"
  ...>
</div>

❌ Bad - Generic label:
<div
  role="separator"
  aria-label="Splitter">
  <!-- What is being resized? -->
</div>
```

### 5. Use aria-controls to Reference Primary Pane

**Splitter SHOULD use `aria-controls` to reference the primary pane element.**

```html
✅ Good - Using aria-controls:
<div id="sidebar" style="width: 25%;">
  Sidebar content
</div>

<div
  role="separator"
  aria-label="Resize sidebar"
  aria-controls="sidebar"
  aria-valuenow="25"
  aria-valuemin="10"
  aria-valuemax="50"
  tabindex="0">
</div>

<div style="flex: 1;">
  Main content
</div>
```

## Fixed vs Variable Splitters

**Variable splitters**: Continuously adjustable within range
**Fixed splitters**: Toggle between two positions

### Variable Splitter (Continuous)

Supports full range of values, arrow keys adjust incrementally.

```html
<div
  role="separator"
  aria-label="Resize sidebar"
  aria-valuenow="30"
  aria-valuemin="10"
  aria-valuemax="90"
  tabindex="0">
</div>
```

### Fixed Splitter (Toggle)

Only two positions: collapsed (minimum) or expanded (restored).

```html
<div
  role="separator"
  aria-label="Toggle sidebar"
  aria-valuenow="30"
  aria-valuemin="0"
  aria-valuemax="30"
  tabindex="0">
</div>

<script>
// Fixed splitter only supports Enter key (no arrows)
splitter.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    e.preventDefault();
    const current = parseInt(splitter.getAttribute('aria-valuenow'));
    const min = parseInt(splitter.getAttribute('aria-valuemin'));
    const max = parseInt(splitter.getAttribute('aria-valuemax'));

    // Toggle between min and max
    const newValue = current === min ? max : min;
    updateSplitter(newValue);
  }
});
</script>
```

## Complete Splitter Structure

```html
<div class="split-view">
  <!-- Primary pane (sidebar) -->
  <div id="sidebar" class="pane" style="width: 25%;">
    <h2>Navigation</h2>
    <nav>
      <a href="#section1">Section 1</a>
      <a href="#section2">Section 2</a>
    </nav>
  </div>

  <!-- Vertical splitter -->
  <div
    id="splitter"
    role="separator"
    aria-label="Resize navigation panel"
    aria-controls="sidebar"
    aria-valuenow="25"
    aria-valuemin="10"
    aria-valuemax="50"
    tabindex="0"
    class="splitter vertical">
    <div class="splitter-handle"></div>
  </div>

  <!-- Secondary pane (main content) -->
  <div class="pane main" style="flex: 1;">
    <h1>Main Content</h1>
    <p>Content area...</p>
  </div>
</div>

<style>
.split-view {
  display: flex;
  height: 100vh;
}

.pane {
  overflow: auto;
  padding: 1rem;
}

.splitter {
  width: 8px;
  background: #ddd;
  cursor: col-resize;
  position: relative;
  flex-shrink: 0;
}

.splitter:focus {
  outline: 2px solid #0066cc;
  outline-offset: -2px;
}

.splitter-handle {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 4px;
  height: 40px;
  background: #666;
  border-radius: 2px;
}

.splitter.horizontal {
  width: auto;
  height: 8px;
  cursor: row-resize;
}
</style>

<script>
const splitter = document.getElementById('splitter');
const sidebar = document.getElementById('sidebar');
const container = document.querySelector('.split-view');

let isDragging = false;
let savedValue = null; // For collapse/restore

// Keyboard navigation
splitter.addEventListener('keydown', (e) => {
  let value = parseInt(splitter.getAttribute('aria-valuenow'));
  const min = parseInt(splitter.getAttribute('aria-valuemin'));
  const max = parseInt(splitter.getAttribute('aria-valuemax'));

  const step = 5; // 5% increments

  switch(e.key) {
    case 'ArrowRight':
      e.preventDefault();
      value = Math.min(value + step, max);
      updateSize(value);
      break;

    case 'ArrowLeft':
      e.preventDefault();
      value = Math.max(value - step, min);
      updateSize(value);
      break;

    case 'Home':
      e.preventDefault();
      updateSize(min);
      break;

    case 'End':
      e.preventDefault();
      updateSize(max);
      break;

    case 'Enter':
      e.preventDefault();
      toggleCollapse();
      break;
  }
});

// Mouse dragging
splitter.addEventListener('mousedown', (e) => {
  isDragging = true;
  e.preventDefault();
});

document.addEventListener('mousemove', (e) => {
  if (!isDragging) return;

  const containerRect = container.getBoundingClientRect();
  const offsetX = e.clientX - containerRect.left;
  const percentage = (offsetX / containerRect.width) * 100;

  const min = parseInt(splitter.getAttribute('aria-valuemin'));
  const max = parseInt(splitter.getAttribute('aria-valuemax'));
  const clampedValue = Math.max(min, Math.min(percentage, max));

  updateSize(clampedValue);
});

document.addEventListener('mouseup', () => {
  isDragging = false;
});

function updateSize(percentage) {
  splitter.setAttribute('aria-valuenow', Math.round(percentage));
  sidebar.style.width = `${percentage}%`;
}

function toggleCollapse() {
  const current = parseInt(splitter.getAttribute('aria-valuenow'));
  const min = parseInt(splitter.getAttribute('aria-valuemin'));

  if (current === min) {
    // Restore
    const restored = savedValue || 25;
    updateSize(restored);
  } else {
    // Collapse
    savedValue = current;
    updateSize(min);
  }
}
</script>
```

## Examples

### ✅ Good: Horizontal Splitter

```html
<div class="vertical-layout">
  <div id="editor" style="height: 60%;">
    <textarea aria-label="Code editor"></textarea>
  </div>

  <div
    role="separator"
    aria-label="Resize code editor"
    aria-controls="editor"
    aria-valuenow="60"
    aria-valuemin="20"
    aria-valuemax="80"
    tabindex="0"
    class="splitter horizontal">
  </div>

  <div style="flex: 1;">
    <div>Console output</div>
  </div>
</div>

<script>
splitter.addEventListener('keydown', (e) => {
  let value = parseInt(splitter.getAttribute('aria-valuenow'));
  const min = parseInt(splitter.getAttribute('aria-valuemin'));
  const max = parseInt(splitter.getAttribute('aria-valuemax'));

  switch(e.key) {
    case 'ArrowDown':
      e.preventDefault();
      value = Math.min(value + 5, max);
      editor.style.height = value + '%';
      splitter.setAttribute('aria-valuenow', value);
      break;

    case 'ArrowUp':
      e.preventDefault();
      value = Math.max(value - 5, min);
      editor.style.height = value + '%';
      splitter.setAttribute('aria-valuenow', value);
      break;
  }
});
</script>
```

### ✅ Good: React Splitter Component

```jsx
function Splitter({
  orientation = 'vertical',
  initialPosition = 50,
  min = 10,
  max = 90,
  primaryPaneId,
  label
}) {
  const [position, setPosition] = useState(initialPosition);
  const [isDragging, setIsDragging] = useState(false);
  const [savedPosition, setSavedPosition] = useState(null);
  const splitterRef = useRef(null);

  const step = 5;

  const handleKeyDown = (e) => {
    let newPosition = position;

    const isVertical = orientation === 'vertical';

    switch(e.key) {
      case isVertical ? 'ArrowRight' : 'ArrowDown':
        e.preventDefault();
        newPosition = Math.min(position + step, max);
        break;

      case isVertical ? 'ArrowLeft' : 'ArrowUp':
        e.preventDefault();
        newPosition = Math.max(position - step, min);
        break;

      case 'Home':
        e.preventDefault();
        newPosition = min;
        break;

      case 'End':
        e.preventDefault();
        newPosition = max;
        break;

      case 'Enter':
        e.preventDefault();
        toggleCollapse();
        return;
    }

    setPosition(newPosition);
  };

  const toggleCollapse = () => {
    if (position === min) {
      setPosition(savedPosition || initialPosition);
    } else {
      setSavedPosition(position);
      setPosition(min);
    }
  };

  return (
    <div
      ref={splitterRef}
      role="separator"
      aria-label={label}
      aria-controls={primaryPaneId}
      aria-valuenow={position}
      aria-valuemin={min}
      aria-valuemax={max}
      aria-orientation={orientation}
      tabIndex={0}
      onKeyDown={handleKeyDown}
      className={`splitter ${orientation}`}
      style={{
        cursor: orientation === 'vertical' ? 'col-resize' : 'row-resize'
      }}>
      <div className="splitter-handle" />
    </div>
  );
}

// Usage
<div className="split-view">
  <div id="sidebar" style={{ width: `${position}%` }}>
    Sidebar
  </div>

  <Splitter
    orientation="vertical"
    primaryPaneId="sidebar"
    label="Resize sidebar"
    initialPosition={25}
    min={10}
    max={50}
  />

  <div style={{ flex: 1 }}>
    Main content
  </div>
</div>
```

### ❌ Bad Examples

```html
<!-- Missing aria-valuenow/min/max -->
<div
  role="separator"
  aria-label="Resize"
  tabindex="0">
  <!-- Missing value attributes! -->
</div>

<!-- Not focusable -->
<div
  role="separator"
  aria-label="Resize sidebar"
  aria-valuenow="30"
  aria-valuemin="0"
  aria-valuemax="100">
  <!-- Missing tabindex! Can't use keyboard -->
</div>

<!-- No keyboard support -->
<div
  role="separator"
  aria-label="Resize"
  aria-valuenow="50"
  aria-valuemin="0"
  aria-valuemax="100"
  tabindex="0">
  <!-- No keydown handler! Arrow keys don't work -->
</div>

<!-- Generic label -->
<div
  role="separator"
  aria-label="Splitter"
  ...>
  <!-- What is being resized? -->
</div>
```

## WCAG References

- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 2.4.6**: Headings and Labels (Level AA)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does splitter have `role="separator"`?** (CRITICAL)
- [ ] **Does splitter have `aria-valuenow`?** (CRITICAL)
- [ ] **Does splitter have `aria-valuemin`?** (CRITICAL)
- [ ] **Does splitter have `aria-valuemax`?** (CRITICAL)
- [ ] **Is splitter focusable (`tabindex="0")?** (CRITICAL)
- [ ] **Do arrow keys resize panes?** (CRITICAL)
- [ ] Does splitter have descriptive label?
- [ ] Does splitter use `aria-controls`?
- [ ] Is `aria-orientation` set for horizontal splitters?
- [ ] Does Enter key toggle collapse/restore?
- [ ] Do Home/End keys work (optional)?
- [ ] Is splitter visually distinguishable?
- [ ] Does splitter show focus indicator?
- [ ] Does mouse dragging update aria-valuenow?

## Quick Reference

```
✅ DO:
- Use role="separator"
- Include aria-valuenow, aria-valuemin, aria-valuemax
- Make focusable with tabindex="0"
- Support arrow key resizing
- Provide descriptive label
- Use aria-controls to reference primary pane
- Set aria-orientation for horizontal splitters
- Update aria-valuenow when resizing
- Show clear focus indicator
- Support Enter to collapse/restore
- Clamp values to min/max range

❌ DON'T:
- Forget required ARIA attributes
- Skip keyboard support
- Forget tabindex (can't focus)
- Use generic label ("Splitter")
- Forget to update aria-valuenow during drag
- Make splitter too narrow to grab
- Rely on mouse-only interaction

## Keyboard Pattern:

Vertical splitter (left/right):
  - Right Arrow: Increase primary pane width
  - Left Arrow: Decrease primary pane width
  - Home: Minimum width (optional)
  - End: Maximum width (optional)
  - Enter: Toggle collapse/restore

Horizontal splitter (top/bottom):
  - Down Arrow: Increase primary pane height
  - Up Arrow: Decrease primary pane height
  - Home: Minimum height (optional)
  - End: Maximum height (optional)
  - Enter: Toggle collapse/restore

F6 (optional):
  - Cycle focus through panes

## Value Representation:

aria-valuenow:
  - Represents primary pane size as percentage
  - 0 = Primary pane at minimum
  - 100 = Primary pane at maximum
  - Update on every resize (keyboard or mouse)

Primary pane:
  - The pane being resized
  - Referenced by aria-controls
  - Named in splitter's aria-label
```
