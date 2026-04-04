---
description: Instructions for proper multi-thumb slider accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Multi-Thumb Slider Accessibility

## CRITICAL RULES

**Multi-thumb sliders have multiple thumbs on a single track, commonly used for selecting a range (min/max values).**

### 1. Each Thumb Must Have role="slider"

**Each thumb MUST have `role="slider"` with all required attributes.**

```html
✅ Good - Two thumbs for range:
<!-- Min thumb -->
<div
  role="slider"
  aria-label="Minimum price"
  aria-valuenow="20"
  aria-valuemin="0"
  aria-valuemax="100"
  tabindex="0">
</div>

<!-- Max thumb -->
<div
  role="slider"
  aria-label="Maximum price"
  aria-valuenow="80"
  aria-valuemin="0"
  aria-valuemax="100"
  tabindex="0">
</div>
```

### 2. Update Dependent Thumb Constraints

**When one thumb's value affects another thumb's range, update `aria-valuemin` or `aria-valuemax` dynamically.**

```javascript
// ✅ Good - Update max thumb's minimum when min thumb changes
function updateMinThumb(value) {
  minThumb.setAttribute('aria-valuenow', value);

  // Update max thumb's minimum to prevent overlap
  const maxValue = parseInt(maxThumb.getAttribute('aria-valuenow'));
  maxThumb.setAttribute('aria-valuemin', value);

  // Adjust max value if it's now invalid
  if (maxValue < value) {
    maxThumb.setAttribute('aria-valuenow', value);
  }
}
```

### 3. Maintain Consistent Tab Order

**Tab order MUST remain constant regardless of thumb positions.**

```html
✅ Good - Consistent tab order:
<div class="range-slider">
  <!-- Min thumb always first in tab order -->
  <div role="slider" aria-label="Minimum" tabindex="0"></div>

  <!-- Max thumb always second in tab order -->
  <div role="slider" aria-label="Maximum" tabindex="0"></div>
</div>
```

**Key principle:** Even if thumbs visually reorder (min passes max), keyboard tab order stays the same.

### 4. Provide Clear Labels for Each Thumb

**Each thumb MUST have a distinct label indicating its purpose.**

```html
✅ Good - Clear distinct labels:
<div role="slider" aria-label="Minimum price" ...></div>
<div role="slider" aria-label="Maximum price" ...></div>

✅ Good - Using aria-labelledby:
<span id="min-label">Min</span>
<div role="slider" aria-labelledby="min-label" ...></div>

<span id="max-label">Max</span>
<div role="slider" aria-labelledby="max-label" ...></div>

❌ Bad - Generic labels:
<div role="slider" aria-label="Price" ...></div>
<div role="slider" aria-label="Price" ...></div>
<!-- Not distinct! -->
```

## Complete Multi-Thumb Slider Structure

```html
<div class="range-slider-container">
  <label id="price-label">Price range</label>

  <div class="range-slider" role="group" aria-labelledby="price-label">
    <!-- Min thumb -->
    <div
      role="slider"
      id="min-thumb"
      aria-label="Minimum price"
      aria-valuenow="25"
      aria-valuemin="0"
      aria-valuemax="100"
      tabindex="0"
      class="slider-thumb">
    </div>

    <!-- Max thumb -->
    <div
      role="slider"
      id="max-thumb"
      aria-label="Maximum price"
      aria-valuenow="75"
      aria-valuemin="0"
      aria-valuemax="100"
      tabindex="0"
      class="slider-thumb">
    </div>
  </div>

  <output id="range-output">$25 - $75</output>
</div>

<script>
const minThumb = document.getElementById('min-thumb');
const maxThumb = document.getElementById('max-thumb');
const output = document.getElementById('range-output');

function handleKeyDown(thumb, e) {
  let value = parseInt(thumb.getAttribute('aria-valuenow'));
  let min = parseInt(thumb.getAttribute('aria-valuemin'));
  let max = parseInt(thumb.getAttribute('aria-valuemax'));

  switch(e.key) {
    case 'ArrowRight':
    case 'ArrowUp':
      e.preventDefault();
      value = Math.min(value + 1, max);
      break;
    case 'ArrowLeft':
    case 'ArrowDown':
      e.preventDefault();
      value = Math.max(value - 1, min);
      break;
    case 'Home':
      e.preventDefault();
      value = min;
      break;
    case 'End':
      e.preventDefault();
      value = max;
      break;
  }

  updateThumb(thumb, value);
}

function updateThumb(thumb, value) {
  thumb.setAttribute('aria-valuenow', value);

  const minValue = parseInt(minThumb.getAttribute('aria-valuenow'));
  const maxValue = parseInt(maxThumb.getAttribute('aria-valuenow'));

  // Update constraints
  if (thumb === minThumb) {
    // Min thumb changed - update max thumb's minimum
    maxThumb.setAttribute('aria-valuemin', minValue);

    // Ensure max >= min
    if (maxValue < minValue) {
      maxThumb.setAttribute('aria-valuenow', minValue);
    }
  } else {
    // Max thumb changed - update min thumb's maximum
    minThumb.setAttribute('aria-valuemax', maxValue);

    // Ensure min <= max
    if (minValue > maxValue) {
      minThumb.setAttribute('aria-valuenow', maxValue);
    }
  }

  updateOutput();
  updateVisual();
}

function updateOutput() {
  const minValue = minThumb.getAttribute('aria-valuenow');
  const maxValue = maxThumb.getAttribute('aria-valuenow');
  output.textContent = `$${minValue} - $${maxValue}`;
}

minThumb.addEventListener('keydown', (e) => handleKeyDown(minThumb, e));
maxThumb.addEventListener('keydown', (e) => handleKeyDown(maxThumb, e));
</script>
```

## Examples

### ✅ Good: Price Range Slider

```html
<div role="group" aria-label="Price range filter">
  <div
    role="slider"
    aria-label="Minimum price"
    aria-valuenow="50"
    aria-valuemin="0"
    aria-valuemax="1000"
    aria-valuetext="$50"
    tabindex="0">
  </div>

  <div
    role="slider"
    aria-label="Maximum price"
    aria-valuenow="500"
    aria-valuemin="0"
    aria-valuemax="1000"
    aria-valuetext="$500"
    tabindex="0">
  </div>
</div>

<output>$50 - $500</output>
```

### ✅ Good: React Range Slider

```jsx
function RangeSlider({ min, max, minValue, maxValue, onChange }) {
  const handleMinKeyDown = (e) => {
    let newValue = minValue;

    switch(e.key) {
      case 'ArrowRight':
      case 'ArrowUp':
        e.preventDefault();
        newValue = Math.min(minValue + 1, maxValue);
        break;
      case 'ArrowLeft':
      case 'ArrowDown':
        e.preventDefault();
        newValue = Math.max(minValue - 1, min);
        break;
      case 'Home':
        e.preventDefault();
        newValue = min;
        break;
      case 'End':
        e.preventDefault();
        newValue = maxValue;
        break;
    }

    onChange({ min: newValue, max: maxValue });
  };

  const handleMaxKeyDown = (e) => {
    let newValue = maxValue;

    switch(e.key) {
      case 'ArrowRight':
      case 'ArrowUp':
        e.preventDefault();
        newValue = Math.min(maxValue + 1, max);
        break;
      case 'ArrowLeft':
      case 'ArrowDown':
        e.preventDefault();
        newValue = Math.max(maxValue - 1, minValue);
        break;
      case 'Home':
        e.preventDefault();
        newValue = minValue;
        break;
      case 'End':
        e.preventDefault();
        newValue = max;
        break;
    }

    onChange({ min: minValue, max: newValue });
  };

  return (
    <div role="group" aria-label="Price range">
      <div
        role="slider"
        aria-label="Minimum price"
        aria-valuenow={minValue}
        aria-valuemin={min}
        aria-valuemax={max}
        tabIndex={0}
        onKeyDown={handleMinKeyDown}
      />

      <div
        role="slider"
        aria-label="Maximum price"
        aria-valuenow={maxValue}
        aria-valuemin={min}
        aria-valuemax={max}
        tabIndex={0}
        onKeyDown={handleMaxKeyDown}
      />

      <output>${minValue} - ${maxValue}</output>
    </div>
  );
}
```

## WCAG References

- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does each thumb have `role="slider"`?** (CRITICAL)
- [ ] **Does each thumb have all required ARIA attributes?** (CRITICAL)
- [ ] **Does each thumb have a distinct label?** (CRITICAL)
- [ ] **Are dependent constraints updated dynamically?** (CRITICAL)
- [ ] **Is tab order consistent regardless of thumb positions?** (CRITICAL)
- [ ] Does each thumb support arrow key navigation?
- [ ] Do Home/End keys work for each thumb?
- [ ] Are thumbs grouped with role="group"?
- [ ] Is output updated to show current range?

## Quick Reference

```
✅ DO:
- Give each thumb role="slider"
- Provide distinct labels for each thumb
- Update aria-valuemin/aria-valuemax dynamically
- Maintain consistent tab order
- Support full keyboard navigation per thumb
- Group thumbs with role="group"
- Show current range in output

❌ DON'T:
- Use same label for all thumbs
- Allow invalid ranges (min > max)
- Change tab order based on visual position
- Forget to update constraints dynamically
```
