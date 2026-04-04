---
description: Instructions for proper spinbutton accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Spinbutton (Number Input) Accessibility

## CRITICAL RULES

**Spinbuttons allow users to select from a range of discrete values, typically numbers, using increment/decrement buttons or arrow keys.**

### 1. Use role="spinbutton" with Required Attributes

**Spinbuttons MUST have `role="spinbutton"` and `aria-valuenow`.**

```html
✅ Good - Proper spinbutton:
<input
  type="text"
  role="spinbutton"
  aria-valuenow="5"
  aria-valuemin="0"
  aria-valuemax="10"
  aria-label="Quantity"
  value="5">

❌ Bad - Missing role:
<input type="number" aria-valuenow="5">
<!-- Should have role="spinbutton"! -->
```

### 2. Implement Arrow Key Increment/Decrement

**Required keyboard interactions:**
- **Up Arrow**: Increase value
- **Down Arrow**: Decrease value
- **Home**: Set to minimum (if defined)
- **End**: Set to maximum (if defined)
- **Page Up**: Larger increase (optional)
- **Page Down**: Larger decrease (optional)

```javascript
spinbutton.addEventListener('keydown', (e) => {
  let value = parseInt(spinbutton.getAttribute('aria-valuenow'));
  const min = parseInt(spinbutton.getAttribute('aria-valuemin'));
  const max = parseInt(spinbutton.getAttribute('aria-valuemax'));

  switch(e.key) {
    case 'ArrowUp':
      e.preventDefault();
      value = Math.min(value + 1, max);
      break;
    case 'ArrowDown':
      e.preventDefault();
      value = Math.max(value - 1, min);
      break;
    case 'Home':
      if (min !== undefined) {
        e.preventDefault();
        value = min;
      }
      break;
    case 'End':
      if (max !== undefined) {
        e.preventDefault();
        value = max;
      }
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

  updateValue(value);
});

function updateValue(value) {
  spinbutton.setAttribute('aria-valuenow', value);
  spinbutton.value = value;
}
```

### 3. Allow Direct Text Input

**Spinbuttons typically allow direct keyboard input of values.**

```javascript
// ✅ Good - Support direct input
spinbutton.addEventListener('input', (e) => {
  let value = parseInt(e.target.value);

  if (!isNaN(value)) {
    const min = parseInt(spinbutton.getAttribute('aria-valuemin'));
    const max = parseInt(spinbutton.getAttribute('aria-valuemax'));

    // Clamp to valid range
    value = Math.max(min, Math.min(value, max));

    spinbutton.setAttribute('aria-valuenow', value);
  }
});
```

### 4. Use aria-invalid for Out-of-Range Values

**Set `aria-invalid="true"` when value is outside allowed range.**

```html
✅ Good - Marking invalid value:
<input
  type="text"
  role="spinbutton"
  aria-valuenow="150"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-invalid="true"
  aria-label="Quantity"
  value="150">
```

### 5. Provide Accessible Label

**Every spinbutton MUST have an accessible label.**

```html
✅ Good - Using <label>:
<label for="qty">Quantity</label>
<input
  type="text"
  id="qty"
  role="spinbutton"
  aria-valuenow="1"
  aria-valuemin="1"
  aria-valuemax="99"
  value="1">

✅ Good - Using aria-label:
<input
  type="text"
  role="spinbutton"
  aria-label="Quantity"
  aria-valuenow="1"
  aria-valuemin="1"
  aria-valuemax="99"
  value="1">
```

## Complete Spinbutton Structure

```html
<label for="quantity">Quantity</label>

<div class="spinbutton-container">
  <button
    type="button"
    aria-label="Decrease quantity"
    onclick="decrement()">
    −
  </button>

  <input
    type="text"
    id="quantity"
    role="spinbutton"
    aria-valuenow="1"
    aria-valuemin="0"
    aria-valuemax="99"
    value="1">

  <button
    type="button"
    aria-label="Increase quantity"
    onclick="increment()">
    +
  </button>
</div>

<script>
const spinbutton = document.getElementById('quantity');

spinbutton.addEventListener('keydown', (e) => {
  let value = parseInt(spinbutton.getAttribute('aria-valuenow'));
  const min = parseInt(spinbutton.getAttribute('aria-valuemin'));
  const max = parseInt(spinbutton.getAttribute('aria-valuemax'));

  switch(e.key) {
    case 'ArrowUp':
      e.preventDefault();
      increment();
      break;
    case 'ArrowDown':
      e.preventDefault();
      decrement();
      break;
    case 'Home':
      e.preventDefault();
      setValue(min);
      break;
    case 'End':
      e.preventDefault();
      setValue(max);
      break;
  }
});

spinbutton.addEventListener('input', (e) => {
  let value = parseInt(e.target.value);

  if (!isNaN(value)) {
    const min = parseInt(spinbutton.getAttribute('aria-valuemin'));
    const max = parseInt(spinbutton.getAttribute('aria-valuemax'));

    if (value >= min && value <= max) {
      spinbutton.setAttribute('aria-valuenow', value);
      spinbutton.setAttribute('aria-invalid', 'false');
    } else {
      spinbutton.setAttribute('aria-invalid', 'true');
    }
  }
});

function increment() {
  let value = parseInt(spinbutton.getAttribute('aria-valuenow'));
  const max = parseInt(spinbutton.getAttribute('aria-valuemax'));

  if (value < max) {
    setValue(value + 1);
  }
}

function decrement() {
  let value = parseInt(spinbutton.getAttribute('aria-valuenow'));
  const min = parseInt(spinbutton.getAttribute('aria-valuemin'));

  if (value > min) {
    setValue(value - 1);
  }
}

function setValue(value) {
  spinbutton.setAttribute('aria-valuenow', value);
  spinbutton.setAttribute('aria-invalid', 'false');
  spinbutton.value = value;
}
</script>
```

## Examples

### ✅ Good: Simple Number Spinner

```html
<label for="age">Age</label>
<input
  type="text"
  id="age"
  role="spinbutton"
  aria-valuenow="25"
  aria-valuemin="0"
  aria-valuemax="120"
  value="25">
```

### ✅ Good: React Spinbutton

```jsx
function Spinbutton({ label, min, max, value, onChange }) {
  const handleKeyDown = (e) => {
    let newValue = value;

    switch(e.key) {
      case 'ArrowUp':
        e.preventDefault();
        newValue = Math.min(value + 1, max);
        break;
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

  const handleInput = (e) => {
    const newValue = parseInt(e.target.value);

    if (!isNaN(newValue) && newValue >= min && newValue <= max) {
      onChange(newValue);
    }
  };

  return (
    <div>
      <label>{label}</label>
      <input
        type="text"
        role="spinbutton"
        aria-valuenow={value}
        aria-valuemin={min}
        aria-valuemax={max}
        aria-invalid={value < min || value > max}
        value={value}
        onKeyDown={handleKeyDown}
        onChange={handleInput}
      />
    </div>
  );
}
```

## WCAG References

- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does input have `role="spinbutton"`?** (CRITICAL)
- [ ] **Does spinbutton have `aria-valuenow`?** (CRITICAL)
- [ ] **Does spinbutton have accessible label?** (CRITICAL)
- [ ] **Do arrow keys increment/decrement?** (CRITICAL)
- [ ] Are min/max values set with `aria-valuemin/aria-valuemax`?
- [ ] Do Home/End keys work?
- [ ] Can users type values directly?
- [ ] Is `aria-invalid="true"` used for out-of-range values?
- [ ] Are increment/decrement buttons labeled?
- [ ] Is focus kept on input during operations?

## Quick Reference

```
✅ DO:
- Use role="spinbutton"
- Include aria-valuenow
- Support arrow key increment/decrement
- Allow direct text input
- Support Home/End for min/max
- Use aria-invalid for out-of-range
- Provide accessible label
- Keep focus on input field

❌ DON'T:
- Use <input type="number"> without role="spinbutton"
- Forget arrow key support
- Prevent direct typing
- Move focus during increment/decrement
- Omit accessible label
```
