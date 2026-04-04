---
description: Instructions for proper checkbox accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Checkbox Accessibility

## CRITICAL RULES

**Checkboxes allow users to select zero, one, or multiple options from a set. They can be dual-state (checked/unchecked) or tri-state (checked/unchecked/mixed).**

### 1. Use Native Checkboxes OR role="checkbox"

**Prefer native HTML `<input type="checkbox">` when possible. For custom checkboxes, use `role="checkbox"`.**

```html
✅ Good - Native checkbox (PREFERRED):
<label>
  <input type="checkbox" name="newsletter">
  Subscribe to newsletter
</label>

✅ Good - Custom checkbox with ARIA:
<div role="checkbox" aria-checked="false" tabindex="0">
  Subscribe to newsletter
</div>

❌ Bad - Missing role:
<div class="checkbox" onclick="toggle()">
  <!-- Missing role="checkbox"! -->
  Subscribe
</div>
```

### 2. Mark Checked State with aria-checked

**For custom checkboxes, use `aria-checked="true|false|mixed"`.**

- `aria-checked="true"` - Checkbox is checked
- `aria-checked="false"` - Checkbox is unchecked
- `aria-checked="mixed"` - Checkbox is partially checked (tri-state only)

```html
✅ Good - Proper aria-checked usage:
<div role="checkbox" aria-checked="false" tabindex="0">
  Accept terms
</div>

✅ Good - Tri-state checkbox:
<div role="checkbox" aria-checked="mixed" tabindex="0">
  Select all (2 of 5 selected)
</div>

❌ Bad - Missing aria-checked:
<div role="checkbox" tabindex="0">  <!-- Missing aria-checked! -->
  Accept terms
</div>
```

**Note:** Native `<input type="checkbox">` uses the `checked` attribute, not `aria-checked`.

### 3. Provide Accessible Label

**Every checkbox MUST have an accessible label.**

```html
✅ Good - Using <label> with native checkbox:
<label>
  <input type="checkbox" name="agree">
  I agree to the terms
</label>

✅ Good - Using aria-labelledby with custom checkbox:
<span id="terms-label">I agree to the terms</span>
<div role="checkbox" aria-checked="false" aria-labelledby="terms-label" tabindex="0"></div>

✅ Good - Using aria-label:
<div role="checkbox" aria-checked="false" aria-label="I agree to the terms" tabindex="0"></div>

✅ Good - Visible text content:
<div role="checkbox" aria-checked="false" tabindex="0">
  I agree to the terms
</div>

❌ Bad - No accessible label:
<div role="checkbox" aria-checked="false" tabindex="0"></div>
```

### 4. Implement Space Key Toggle

**Custom checkboxes MUST toggle on Space key.**

```javascript
// ✅ Good - Space key toggle
checkbox.addEventListener('keydown', (e) => {
  if (e.key === ' ') {
    e.preventDefault();
    toggleCheckbox();
  }
});

function toggleCheckbox() {
  const isChecked = checkbox.getAttribute('aria-checked') === 'true';
  checkbox.setAttribute('aria-checked', !isChecked);
}
```

**Note:** Native `<input type="checkbox">` handles Space key automatically.

### 5. Make Custom Checkboxes Focusable

**Custom checkboxes MUST have `tabindex="0"` to be keyboard accessible.**

```html
✅ Good - Focusable custom checkbox:
<div role="checkbox" aria-checked="false" tabindex="0">
  Enable notifications
</div>

❌ Bad - Not focusable:
<div role="checkbox" aria-checked="false">
  <!-- Missing tabindex="0"! -->
  Enable notifications
</div>
```

## Complete Checkbox Structure

### Native Checkbox (Preferred)

```html
<fieldset>
  <legend>Notification preferences</legend>

  <label>
    <input type="checkbox" name="email" checked>
    Email notifications
  </label>

  <label>
    <input type="checkbox" name="sms">
    SMS notifications
  </label>

  <label>
    <input type="checkbox" name="push">
    Push notifications
  </label>
</fieldset>
```

### Custom Checkbox with ARIA

```html
<div role="group" aria-labelledby="prefs-label">
  <span id="prefs-label">Notification preferences</span>

  <div
    role="checkbox"
    aria-checked="true"
    tabindex="0"
    id="checkbox-email">
    <span class="checkbox-icon"></span>
    Email notifications
  </div>

  <div
    role="checkbox"
    aria-checked="false"
    tabindex="0"
    id="checkbox-sms">
    <span class="checkbox-icon"></span>
    SMS notifications
  </div>

  <div
    role="checkbox"
    aria-checked="false"
    tabindex="0"
    id="checkbox-push">
    <span class="checkbox-icon"></span>
    Push notifications
  </div>
</div>

<script>
const checkboxes = document.querySelectorAll('[role="checkbox"]');

checkboxes.forEach(checkbox => {
  // Click toggle
  checkbox.addEventListener('click', () => {
    toggleCheckbox(checkbox);
  });

  // Space key toggle
  checkbox.addEventListener('keydown', (e) => {
    if (e.key === ' ') {
      e.preventDefault();
      toggleCheckbox(checkbox);
    }
  });
});

function toggleCheckbox(checkbox) {
  const isChecked = checkbox.getAttribute('aria-checked') === 'true';
  checkbox.setAttribute('aria-checked', !isChecked);
}
</script>
```

### Tri-State Checkbox (Select All)

```html
<div role="checkbox" aria-checked="false" tabindex="0" id="select-all">
  Select all
</div>

<fieldset role="group" aria-labelledby="items-label">
  <span id="items-label">Items</span>

  <label>
    <input type="checkbox" name="item1" class="item-checkbox">
    Item 1
  </label>

  <label>
    <input type="checkbox" name="item2" class="item-checkbox">
    Item 2
  </label>

  <label>
    <input type="checkbox" name="item3" class="item-checkbox">
    Item 3
  </label>
</fieldset>

<script>
const selectAll = document.getElementById('select-all');
const itemCheckboxes = document.querySelectorAll('.item-checkbox');

// Select all toggle
selectAll.addEventListener('click', () => {
  const currentState = selectAll.getAttribute('aria-checked');

  if (currentState === 'true' || currentState === 'mixed') {
    // Uncheck all
    selectAll.setAttribute('aria-checked', 'false');
    itemCheckboxes.forEach(cb => cb.checked = false);
  } else {
    // Check all
    selectAll.setAttribute('aria-checked', 'true');
    itemCheckboxes.forEach(cb => cb.checked = true);
  }
});

// Update select all state when individual items change
itemCheckboxes.forEach(checkbox => {
  checkbox.addEventListener('change', updateSelectAllState);
});

function updateSelectAllState() {
  const checkedCount = Array.from(itemCheckboxes).filter(cb => cb.checked).length;
  const totalCount = itemCheckboxes.length;

  if (checkedCount === 0) {
    selectAll.setAttribute('aria-checked', 'false');
  } else if (checkedCount === totalCount) {
    selectAll.setAttribute('aria-checked', 'true');
  } else {
    selectAll.setAttribute('aria-checked', 'mixed');
  }
}
</script>
```

## Examples

### ✅ Good: Native Checkbox Group

```html
<fieldset>
  <legend>Select your interests</legend>

  <label>
    <input type="checkbox" name="interests" value="sports">
    Sports
  </label>

  <label>
    <input type="checkbox" name="interests" value="music" checked>
    Music
  </label>

  <label>
    <input type="checkbox" name="interests" value="art">
    Art
  </label>
</fieldset>
```

### ✅ Good: Single Checkbox with Description

```html
<label>
  <input
    type="checkbox"
    name="terms"
    aria-describedby="terms-desc">
  I agree to the terms and conditions
</label>
<p id="terms-desc">
  By checking this box, you agree to our privacy policy and user agreement.
</p>
```

### ✅ Good: React Checkbox Component

```jsx
function Checkbox({ label, checked, onChange, describedBy }) {
  return (
    <label>
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        aria-describedby={describedBy}
      />
      {label}
    </label>
  );
}

// Usage
<Checkbox
  label="Enable dark mode"
  checked={isDarkMode}
  onChange={setIsDarkMode}
/>
```

### ✅ Good: Vue Checkbox Component

```vue
<template>
  <label>
    <input
      type="checkbox"
      :checked="modelValue"
      @change="$emit('update:modelValue', $event.target.checked)">
    {{ label }}
  </label>
</template>

<script>
export default {
  props: {
    label: String,
    modelValue: Boolean
  },
  emits: ['update:modelValue']
};
</script>
```

### ❌ Bad Examples

```html
<!-- Missing role="checkbox" on custom -->
<div class="checkbox" onclick="toggle()">
  Accept terms
</div>

<!-- Missing aria-checked -->
<div role="checkbox" tabindex="0">
  Accept terms
</div>

<!-- Missing tabindex -->
<div role="checkbox" aria-checked="false">
  Accept terms
</div>

<!-- Missing label -->
<input type="checkbox" name="agree">

<!-- Using aria-checked on native input -->
<input type="checkbox" aria-checked="false">
<!-- Use checked attribute instead! -->
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Are native `<input type="checkbox">` used when possible?** (PREFERRED)
- [ ] **Do custom checkboxes have `role="checkbox"`?** (CRITICAL for custom)
- [ ] **Do custom checkboxes have `aria-checked="true|false|mixed"`?** (CRITICAL for custom)
- [ ] **Do custom checkboxes have `tabindex="0"`?** (CRITICAL for custom)
- [ ] **Does every checkbox have an accessible label?** (CRITICAL)
- [ ] **Does Space key toggle custom checkboxes?** (CRITICAL for custom)
- [ ] Are related checkboxes grouped in `<fieldset>` or `role="group"`?
- [ ] Does group have accessible label (`<legend>` or `aria-labelledby`)?
- [ ] For tri-state: Is `aria-checked="mixed"` used appropriately?
- [ ] Are descriptions provided with `aria-describedby` when needed?

## Quick Reference

```
✅ DO:
- Use native <input type="checkbox"> when possible
- Use <label> to associate label with native checkbox
- For custom: use role="checkbox"
- For custom: use aria-checked="true|false|mixed"
- For custom: use tabindex="0"
- For custom: toggle on Space key
- Group related checkboxes in <fieldset> or role="group"
- Provide group label with <legend> or aria-labelledby
- Use aria-checked="mixed" for tri-state (select all)
- Use aria-describedby for additional context

❌ DON'T:
- Skip role="checkbox" on custom checkboxes
- Forget aria-checked on custom checkboxes
- Make custom checkbox non-focusable
- Omit accessible label
- Use aria-checked on native <input type="checkbox">
- Forget to handle Space key for custom checkboxes
- Leave checkboxes ungrouped when related

## Native vs Custom:

Native (PREFERRED):
  - <input type="checkbox">
  - Use checked attribute (not aria-checked)
  - Browser handles keyboard automatically
  - Use <label> for association
  - Use <fieldset> and <legend> for groups

Custom (when necessary):
  - role="checkbox"
  - aria-checked="true|false|mixed"
  - tabindex="0"
  - Implement Space key toggle
  - Use aria-label or aria-labelledby
  - Use role="group" with aria-labelledby for groups

## Tri-State (Mixed):

Use aria-checked="mixed" when:
  - Select all checkbox controls multiple items
  - Some (but not all) sub-items are checked
  - Indicates partial selection state
```
