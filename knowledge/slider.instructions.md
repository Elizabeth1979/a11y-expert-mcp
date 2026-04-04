---
description: Instructions for proper slider accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Slider Accessibility

## CRITICAL RULES

**Sliders allow users to select a value from a continuous or discrete range.**

### 1. Use role="slider" with Required ARIA Attributes

**Sliders MUST have `role="slider"`, `aria-valuenow`, `aria-valuemin`, and `aria-valuemax`.**

```html
✅ Good - Proper slider attributes:
<div
  role="slider"
  aria-valuenow="50"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-label="Volume"
  tabindex="0">
</div>

❌ Bad - Missing required attributes:
<div role="slider" tabindex="0">  <!-- Missing value attributes! -->
</div>
```

### 2. Use aria-valuetext for Non-Numeric Values

**When numeric values aren't user-friendly, provide `aria-valuetext`.**

```html
✅ Good - Using aria-valuetext:
<div
  role="slider"
  aria-valuenow="2"
  aria-valuemin="1"
  aria-valuemax="7"
  aria-valuetext="Tuesday"
  aria-label="Select day"
  tabindex="0">
</div>
```

### 3. Implement Arrow Key Navigation

**Required keyboard interactions:**
- **Right/Up Arrow**: Increase value by one step
- **Left/Down Arrow**: Decrease value by one step
- **Home**: Set to minimum value
- **End**: Set to maximum value
- **Page Up**: Larger increase (optional)
- **Page Down**: Larger decrease (optional)

```javascript
slider.addEventListener('keydown', (e) => {
  let newValue = parseInt(slider.getAttribute('aria-valuenow'));
  const min = parseInt(slider.getAttribute('aria-valuemin'));
  const max = parseInt(slider.getAttribute('aria-valuemax'));

  switch(e.key) {
    case 'ArrowRight':
    case 'ArrowUp':
      e.preventDefault();
      newValue = Math.min(newValue + 1, max);
      break;
    case 'ArrowLeft':
    case 'ArrowDown':
      e.preventDefault();
      newValue = Math.max(newValue - 1, min);
      break;
    case 'Home':
      e.preventDefault();
      newValue = min;
      break;
    case 'End':
      e.preventDefault();
      newValue = max;
      break;
  }

  slider.setAttribute('aria-valuenow', newValue);
  updateSliderVisual(newValue);
});
```

### 4. Provide Accessible Label

**Every slider MUST have an accessible label.**

```html
✅ Good - Using aria-label:
<div
  role="slider"
  aria-label="Volume level"
  aria-valuenow="75"
  aria-valuemin="0"
  aria-valuemax="100"
  tabindex="0">
</div>

✅ Good - Using aria-labelledby:
<label id="vol-label">Volume</label>
<div
  role="slider"
  aria-labelledby="vol-label"
  aria-valuenow="75"
  aria-valuemin="0"
  aria-valuemax="100"
  tabindex="0">
</div>
```

### 5. Set aria-orientation for Vertical Sliders

**Vertical sliders MUST have `aria-orientation="vertical"`.**

```html
✅ Good - Vertical slider:
<div
  role="slider"
  aria-orientation="vertical"
  aria-label="Temperature"
  aria-valuenow="72"
  aria-valuemin="60"
  aria-valuemax="80"
  tabindex="0">
</div>
```

## Complete Slider Structure

```html
<label id="volume-label">Volume</label>
<div class="slider-container">
  <div
    role="slider"
    id="volume-slider"
    aria-labelledby="volume-label"
    aria-valuenow="50"
    aria-valuemin="0"
    aria-valuemax="100"
    tabindex="0">
    <div class="slider-track">
      <div class="slider-thumb" style="left: 50%;"></div>
    </div>
  </div>
  <output id="volume-output">50</output>
</div>

<script>
const slider = document.getElementById('volume-slider');
const output = document.getElementById('volume-output');
const thumb = slider.querySelector('.slider-thumb');

slider.addEventListener('keydown', (e) => {
  let value = parseInt(slider.getAttribute('aria-valuenow'));
  const min = parseInt(slider.getAttribute('aria-valuemin'));
  const max = parseInt(slider.getAttribute('aria-valuemax'));

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
    case 'PageUp':
      e.preventDefault();
      value = Math.min(value + 10, max);
      break;
    case 'PageDown':
      e.preventDefault();
      value = Math.max(value - 10, min);
      break;
  }

  updateSlider(value);
});

function updateSlider(value) {
  slider.setAttribute('aria-valuenow', value);
  output.textContent = value;

  const percent = ((value - 0) / (100 - 0)) * 100;
  thumb.style.left = `${percent}%`;
}
</script>
```

## Examples

### ✅ Good: Native Range Input

```html
<label for="brightness">Brightness</label>
<input
  type="range"
  id="brightness"
  min="0"
  max="100"
  value="75">
<output id="brightness-value">75</output>
```

### ✅ Good: React Slider

```jsx
function Slider({ label, min, max, value, onChange }) {
  const handleKeyDown = (e) => {
    let newValue = value;

    switch(e.key) {
      case 'ArrowRight':
      case 'ArrowUp':
        e.preventDefault();
        newValue = Math.min(value + 1, max);
        break;
      case 'ArrowLeft':
      case 'ArrowDown':
        e.preventDefault();
        newValue = Math.max(value - 1, min);
        break;
      case 'Home':
        e.preventDefault();
        newValue = min;
        break;
      case 'End':
        e.preventDefault();
        newValue = max;
        break;
    }

    if (newValue !== value) {
      onChange(newValue);
    }
  };

  const percent = ((value - min) / (max - min)) * 100;

  return (
    <div>
      <label>{label}</label>
      <div
        role="slider"
        aria-label={label}
        aria-valuenow={value}
        aria-valuemin={min}
        aria-valuemax={max}
        tabIndex={0}
        onKeyDown={handleKeyDown}>
        <div className="slider-track">
          <div className="slider-thumb" style={{ left: `${percent}%` }} />
        </div>
      </div>
      <output>{value}</output>
    </div>
  );
}
```

## WCAG References

- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does slider have `role="slider"`?** (CRITICAL)
- [ ] **Does slider have `aria-valuenow`?** (CRITICAL)
- [ ] **Does slider have `aria-valuemin`?** (CRITICAL)
- [ ] **Does slider have `aria-valuemax`?** (CRITICAL)
- [ ] **Does slider have accessible label?** (CRITICAL)
- [ ] **Is slider focusable (tabindex="0")?** (CRITICAL)
- [ ] **Do arrow keys adjust value?** (CRITICAL)
- [ ] **Do Home/End keys work?** (CRITICAL)
- [ ] Is `aria-valuetext` used for non-numeric values?
- [ ] Is `aria-orientation="vertical"` set for vertical sliders?
- [ ] Are Page Up/Down supported for larger steps?

## Quick Reference

```
✅ DO:
- Use role="slider"
- Include aria-valuenow, aria-valuemin, aria-valuemax
- Provide accessible label
- Make focusable with tabindex="0"
- Support arrow keys (Right/Up increase, Left/Down decrease)
- Support Home (min) and End (max) keys
- Use aria-valuetext for non-numeric values
- Set aria-orientation="vertical" for vertical sliders
- Consider native <input type="range"> when possible

❌ DON'T:
- Omit required ARIA attributes
- Forget accessible label
- Skip keyboard support
- Forget tabindex="0"
```
