---
description: Instructions for proper radio group accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Radio Group Accessibility

## CRITICAL RULES

**Radio groups allow users to select exactly one option from a set of mutually exclusive choices.**

### 1. Use Native Radio Inputs OR role="radiogroup" with role="radio"

**Prefer native HTML `<input type="radio">` when possible. For custom radio buttons, use ARIA roles.**

```html
✅ Good - Native radio buttons (PREFERRED):
<fieldset>
  <legend>Choose size</legend>
  <label>
    <input type="radio" name="size" value="small">
    Small
  </label>
  <label>
    <input type="radio" name="size" value="medium" checked>
    Medium
  </label>
  <label>
    <input type="radio" name="size" value="large">
    Large
  </label>
</fieldset>

✅ Good - Custom radio with ARIA (when native isn't possible):
<div role="radiogroup" aria-labelledby="size-label">
  <span id="size-label">Choose size</span>
  <div role="radio" aria-checked="false" tabindex="-1">Small</div>
  <div role="radio" aria-checked="true" tabindex="0">Medium</div>
  <div role="radio" aria-checked="false" tabindex="-1">Large</div>
</div>

❌ Bad - Missing roles:
<div class="radio-group">
  <div class="radio">Small</div>  <!-- Missing role="radio"! -->
  <div class="radio">Medium</div>
</div>
```

### 2. Group Radios with role="radiogroup" (or fieldset)

**Radio buttons MUST be contained in a `role="radiogroup"` (or `<fieldset>` for native inputs).**

```html
✅ Good - Using fieldset (native):
<fieldset>
  <legend>Shipping method</legend>
  <label>
    <input type="radio" name="shipping" value="standard">
    Standard (3-5 days)
  </label>
  <label>
    <input type="radio" name="shipping" value="express">
    Express (1-2 days)
  </label>
</fieldset>

✅ Good - Using role="radiogroup" (custom):
<div role="radiogroup" aria-label="Shipping method">
  <div role="radio" aria-checked="false" tabindex="0">
    Standard (3-5 days)
  </div>
  <div role="radio" aria-checked="false" tabindex="-1">
    Express (1-2 days)
  </div>
</div>

❌ Bad - No grouping:
<div>  <!-- Missing role="radiogroup"! -->
  <div role="radio" aria-checked="false">Option 1</div>
  <div role="radio" aria-checked="false">Option 2</div>
</div>
```

### 3. Mark Checked State with aria-checked (Custom Radios)

**For custom radio buttons, use `aria-checked="true"` for selected, `aria-checked="false"` for unselected.**

Only ONE radio in a group can have `aria-checked="true"`.

```html
✅ Good - Proper aria-checked usage:
<div role="radiogroup" aria-label="Color">
  <div role="radio" aria-checked="false" tabindex="-1">Red</div>
  <div role="radio" aria-checked="true" tabindex="0">Blue</div>
  <div role="radio" aria-checked="false" tabindex="-1">Green</div>
</div>

❌ Bad - Multiple checked:
<div role="radiogroup" aria-label="Color">
  <div role="radio" aria-checked="true">Red</div>
  <div role="radio" aria-checked="true">Blue</div>
  <!-- Only ONE can be checked! -->
</div>

❌ Bad - Missing aria-checked:
<div role="radiogroup" aria-label="Color">
  <div role="radio" tabindex="0">Red</div>  <!-- Missing aria-checked! -->
  <div role="radio" tabindex="-1">Blue</div>
</div>
```

### 4. Implement Arrow Key Navigation

**Radio groups MUST support arrow key navigation that automatically selects the focused radio.**

**Required keyboard interactions:**
- **Tab**: Enter/exit group; focus lands on checked radio (or first if none checked)
- **Arrow Down/Right**: Move to next radio, check it, uncheck previous
- **Arrow Up/Left**: Move to previous radio, check it, uncheck previous
- **Space**: Check focused radio if unchecked (optional, arrows usually handle selection)

**Key behavior:** Arrow keys wrap (last → first, first → last)

```javascript
// ✅ Good - Arrow key navigation
radiogroup.addEventListener('keydown', (e) => {
  const radios = Array.from(radiogroup.querySelectorAll('[role="radio"]'));
  const currentIndex = radios.indexOf(document.activeElement);

  let newIndex;

  switch(e.key) {
    case 'ArrowDown':
    case 'ArrowRight':
      e.preventDefault();
      newIndex = (currentIndex + 1) % radios.length;  // Wrap to first
      checkRadio(radios[newIndex]);
      break;

    case 'ArrowUp':
    case 'ArrowLeft':
      e.preventDefault();
      newIndex = currentIndex === 0 ? radios.length - 1 : currentIndex - 1;
      checkRadio(radios[newIndex]);
      break;

    case ' ':
      e.preventDefault();
      checkRadio(radios[currentIndex]);
      break;
  }
});

function checkRadio(radio) {
  // Uncheck all radios
  radios.forEach(r => {
    r.setAttribute('aria-checked', 'false');
    r.setAttribute('tabindex', '-1');
  });

  // Check and focus new radio
  radio.setAttribute('aria-checked', 'true');
  radio.setAttribute('tabindex', '0');
  radio.focus();
}
```

### 5. Manage Focus with Roving tabindex

**Only the checked radio (or first radio if none checked) should be in tab sequence (`tabindex="0"`).**

All other radios: `tabindex="-1"`

```html
✅ Good - Roving tabindex:
<div role="radiogroup" aria-label="Plan">
  <div role="radio" aria-checked="false" tabindex="-1">Basic</div>
  <div role="radio" aria-checked="true" tabindex="0">Pro</div>
  <div role="radio" aria-checked="false" tabindex="-1">Enterprise</div>
</div>

❌ Bad - All radios have tabindex="0":
<div role="radiogroup" aria-label="Plan">
  <div role="radio" aria-checked="false" tabindex="0">Basic</div>
  <div role="radio" aria-checked="true" tabindex="0">Pro</div>
  <div role="radio" aria-checked="false" tabindex="0">Enterprise</div>
  <!-- Only checked radio should have tabindex="0"! -->
</div>
```

## Complete Radio Group Structure

### Native HTML (Preferred)

```html
<fieldset>
  <legend>Preferred contact method</legend>

  <label>
    <input type="radio" name="contact" value="email" checked>
    Email
  </label>

  <label>
    <input type="radio" name="contact" value="phone">
    Phone
  </label>

  <label>
    <input type="radio" name="contact" value="sms">
    Text message
  </label>
</fieldset>
```

### Custom Radio Group with ARIA

```html
<div role="radiogroup" aria-labelledby="payment-label" id="payment-group">
  <span id="payment-label">Payment method</span>

  <div
    role="radio"
    aria-checked="true"
    tabindex="0"
    id="radio-credit">
    <span class="radio-icon"></span>
    Credit Card
  </div>

  <div
    role="radio"
    aria-checked="false"
    tabindex="-1"
    id="radio-paypal">
    <span class="radio-icon"></span>
    PayPal
  </div>

  <div
    role="radio"
    aria-checked="false"
    tabindex="-1"
    id="radio-bank">
    <span class="radio-icon"></span>
    Bank Transfer
  </div>
</div>

<script>
const radiogroup = document.getElementById('payment-group');
const radios = radiogroup.querySelectorAll('[role="radio"]');

// Arrow key navigation
radiogroup.addEventListener('keydown', (e) => {
  const radiosArray = Array.from(radios);
  const currentIndex = radiosArray.indexOf(document.activeElement);

  let newIndex;

  switch(e.key) {
    case 'ArrowDown':
    case 'ArrowRight':
      e.preventDefault();
      newIndex = (currentIndex + 1) % radiosArray.length;
      selectRadio(radiosArray[newIndex]);
      break;

    case 'ArrowUp':
    case 'ArrowLeft':
      e.preventDefault();
      newIndex = currentIndex === 0 ? radiosArray.length - 1 : currentIndex - 1;
      selectRadio(radiosArray[newIndex]);
      break;

    case ' ':
      e.preventDefault();
      selectRadio(radiosArray[currentIndex]);
      break;
  }
});

// Click selection
radios.forEach(radio => {
  radio.addEventListener('click', () => selectRadio(radio));
});

function selectRadio(radio) {
  // Uncheck all radios
  radios.forEach(r => {
    r.setAttribute('aria-checked', 'false');
    r.setAttribute('tabindex', '-1');
  });

  // Check selected radio
  radio.setAttribute('aria-checked', 'true');
  radio.setAttribute('tabindex', '0');
  radio.focus();
}
</script>
```

## Examples

### ✅ Good: Native Radio Group

```html
<fieldset>
  <legend>Subscribe to newsletter?</legend>
  <label>
    <input type="radio" name="subscribe" value="yes">
    Yes, send me updates
  </label>
  <label>
    <input type="radio" name="subscribe" value="no" checked>
    No, thanks
  </label>
</fieldset>
```

### ✅ Good: Custom Radio with Visual Indicators

```html
<div role="radiogroup" aria-label="Difficulty level">
  <div role="radio" aria-checked="false" tabindex="0" class="radio-option">
    <span class="radio-icon"></span>
    <span class="radio-label">Easy</span>
  </div>
  <div role="radio" aria-checked="true" tabindex="-1" class="radio-option">
    <span class="radio-icon"></span>
    <span class="radio-label">Medium</span>
  </div>
  <div role="radio" aria-checked="false" tabindex="-1" class="radio-option">
    <span class="radio-icon"></span>
    <span class="radio-label">Hard</span>
  </div>
</div>
```

### ✅ Good: React Radio Group Component

```jsx
function RadioGroup({ label, options, value, onChange, name }) {
  const handleKeyDown = (e, index) => {
    let newIndex;

    switch(e.key) {
      case 'ArrowDown':
      case 'ArrowRight':
        e.preventDefault();
        newIndex = (index + 1) % options.length;
        onChange(options[newIndex].value);
        break;

      case 'ArrowUp':
      case 'ArrowLeft':
        e.preventDefault();
        newIndex = index === 0 ? options.length - 1 : index - 1;
        onChange(options[newIndex].value);
        break;

      case ' ':
        e.preventDefault();
        onChange(options[index].value);
        break;
    }
  };

  return (
    <fieldset>
      <legend>{label}</legend>
      {options.map((option, index) => (
        <label key={option.value}>
          <input
            type="radio"
            name={name}
            value={option.value}
            checked={value === option.value}
            onChange={() => onChange(option.value)}
            onKeyDown={(e) => handleKeyDown(e, index)}
          />
          {option.label}
        </label>
      ))}
    </fieldset>
  );
}

// Usage
<RadioGroup
  label="Choose size"
  name="size"
  options={[
    { value: 'small', label: 'Small' },
    { value: 'medium', label: 'Medium' },
    { value: 'large', label: 'Large' }
  ]}
  value={selectedSize}
  onChange={setSelectedSize}
/>
```

### ✅ Good: Vue Radio Group Component

```vue
<template>
  <fieldset>
    <legend>{{ label }}</legend>
    <label v-for="option in options" :key="option.value">
      <input
        type="radio"
        :name="name"
        :value="option.value"
        :checked="modelValue === option.value"
        @change="$emit('update:modelValue', option.value)">
      {{ option.label }}
    </label>
  </fieldset>
</template>

<script>
export default {
  props: {
    label: String,
    name: String,
    options: Array,
    modelValue: String
  },
  emits: ['update:modelValue']
};
</script>
```

### ❌ Bad Examples

```html
<!-- Missing role="radiogroup" -->
<div>
  <div role="radio" aria-checked="false">Option 1</div>
  <div role="radio" aria-checked="false">Option 2</div>
</div>

<!-- Multiple radios checked -->
<div role="radiogroup" aria-label="Color">
  <div role="radio" aria-checked="true">Red</div>
  <div role="radio" aria-checked="true">Blue</div>
</div>

<!-- All radios have tabindex="0" -->
<div role="radiogroup" aria-label="Size">
  <div role="radio" aria-checked="false" tabindex="0">Small</div>
  <div role="radio" aria-checked="true" tabindex="0">Medium</div>
</div>

<!-- Missing aria-checked -->
<div role="radiogroup" aria-label="Color">
  <div role="radio" tabindex="0">Red</div>
</div>

<!-- Missing accessible label -->
<div role="radiogroup">
  <div role="radio" aria-checked="false">Option 1</div>
</div>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Are native `<input type="radio">` used when possible?** (PREFERRED)
- [ ] **Is group wrapped in `<fieldset>` (native) or has `role="radiogroup"` (custom)?** (CRITICAL)
- [ ] **Does each custom radio have `role="radio"`?** (CRITICAL for custom)
- [ ] **Does each custom radio have `aria-checked="true|false"`?** (CRITICAL for custom)
- [ ] **Is only ONE radio checked at a time?** (CRITICAL)
- [ ] **Does group have accessible label (`<legend>`, `aria-label`, or `aria-labelledby`)?** (CRITICAL)
- [ ] **Do arrow keys navigate and select radios?** (CRITICAL)
- [ ] **Is focus managed with roving tabindex?** (CRITICAL - checked: tabindex="0", others: tabindex="-1")
- [ ] **Does Tab key enter/exit group (not navigate within)?** (CRITICAL)
- [ ] Do arrow keys wrap (last → first, first → last)?
- [ ] Does focus land on checked radio when entering group?
- [ ] If no radio checked, does focus land on first radio?

## Quick Reference

```
✅ DO:
- Use native <input type="radio"> when possible
- Group radios in <fieldset> (native) or role="radiogroup" (custom)
- Use <legend> (native) or aria-label/aria-labelledby (custom) for group label
- For custom: use role="radio" on each radio
- For custom: use aria-checked="true|false"
- Ensure only ONE radio is checked
- Support arrow key navigation
- Arrow keys automatically select focused radio
- Use roving tabindex (checked: "0", others: "-1")
- Wrap arrow navigation (last to first, first to last)
- Tab enters/exits group (doesn't navigate within)

❌ DON'T:
- Skip role="radiogroup" for custom radios
- Allow multiple radios to be checked
- Forget aria-checked on custom radios
- Give all radios tabindex="0"
- Use Tab to navigate within group (use arrows)
- Forget accessible label on group
- Make arrow navigation not wrap

## Native vs Custom:

Native (PREFERRED):
  - <input type="radio"> inside <fieldset>
  - Browser handles all accessibility automatically
  - Use <legend> for group label
  - Use <label> for each radio

Custom (when necessary):
  - role="radiogroup" on container
  - role="radio" on each option
  - aria-checked="true|false" on each
  - aria-label or aria-labelledby on group
  - Implement arrow key navigation
  - Manage roving tabindex
```
