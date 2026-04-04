---
description: Instructions for proper switch (toggle) accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Switch (Toggle) Accessibility

## CRITICAL RULES

**A switch is an on/off toggle control representing a binary state. Switches are typically used for settings that take effect immediately.**

### 1. Use role="switch" with aria-checked

**Switch elements MUST have `role="switch"` and `aria-checked="true|false"`.**

```html
✅ Good - Switch with role and state:
<button role="switch" aria-checked="false">
  Dark mode
</button>

✅ Good - Checkbox-based switch:
<input type="checkbox" role="switch" aria-checked="false" id="toggle">
<label for="toggle">Dark mode</label>

❌ Bad - Missing role="switch":
<button aria-checked="false">  <!-- Missing role="switch"! -->
  Dark mode
</button>

❌ Bad - Missing aria-checked:
<button role="switch">  <!-- Missing aria-checked! -->
  Dark mode
</button>
```

### 2. CRITICAL: Switch Label Must Never Change

**The label text MUST remain constant regardless of switch state. Only the state (aria-checked) changes.**

```html
✅ Good - Label stays constant:
<!-- OFF state -->
<button role="switch" aria-checked="false">
  Dark mode
</button>

<!-- ON state -->
<button role="switch" aria-checked="true">
  Dark mode  <!-- Same label! -->
</button>

❌ Bad - Label changes with state:
<!-- OFF state -->
<button role="switch" aria-checked="false">
  Enable dark mode
</button>

<!-- ON state -->
<button role="switch" aria-checked="true">
  Disable dark mode  <!-- Label changed! Wrong! -->
</button>
```

**Why this matters:**
- Screen readers announce both the label and the state
- Changing the label is redundant and confusing
- The label describes the feature, not the action

### 3. Implement Space Key Toggle

**Switches MUST toggle on Space key (and optionally Enter key).**

```javascript
// ✅ Good - Space key toggle
switchBtn.addEventListener('keydown', (e) => {
  if (e.key === ' ' || e.key === 'Enter') {
    e.preventDefault();
    toggleSwitch();
  }
});

function toggleSwitch() {
  const isOn = switchBtn.getAttribute('aria-checked') === 'true';
  switchBtn.setAttribute('aria-checked', !isOn);
}
```

**Note:** Native `<button>` elements handle Space and Enter automatically.

### 4. Make Switch Focusable

**Switches MUST be keyboard focusable.**

```html
✅ Good - Using button (focusable by default):
<button role="switch" aria-checked="false">
  Airplane mode
</button>

✅ Good - Custom element with tabindex:
<div role="switch" aria-checked="false" tabindex="0">
  Airplane mode
</div>

❌ Bad - Not focusable:
<div role="switch" aria-checked="false">
  <!-- Missing tabindex="0"! -->
  Airplane mode
</div>
```

### 5. Group Related Switches

**Related switches SHOULD be grouped with `role="group"` or `<fieldset>`.**

```html
✅ Good - Grouped switches:
<fieldset>
  <legend>Notification settings</legend>

  <button role="switch" aria-checked="true">
    Email notifications
  </button>

  <button role="switch" aria-checked="false">
    SMS notifications
  </button>

  <button role="switch" aria-checked="true">
    Push notifications
  </button>
</fieldset>

✅ Good - Using role="group":
<div role="group" aria-labelledby="notif-label">
  <span id="notif-label">Notification settings</span>

  <button role="switch" aria-checked="true">
    Email notifications
  </button>

  <button role="switch" aria-checked="false">
    SMS notifications
  </button>
</div>
```

## Complete Switch Structure

### Button-based Switch (Recommended)

```html
<button
  role="switch"
  aria-checked="false"
  id="dark-mode-switch">
  Dark mode
</button>

<style>
/* Visual indicator for state */
button[role="switch"][aria-checked="true"]::before {
  content: 'ON';
}

button[role="switch"][aria-checked="false"]::before {
  content: 'OFF';
}
</style>

<script>
const switchBtn = document.getElementById('dark-mode-switch');

switchBtn.addEventListener('click', toggleSwitch);

switchBtn.addEventListener('keydown', (e) => {
  if (e.key === ' ' || e.key === 'Enter') {
    e.preventDefault();
    toggleSwitch();
  }
});

function toggleSwitch() {
  const isOn = switchBtn.getAttribute('aria-checked') === 'true';
  const newState = !isOn;

  switchBtn.setAttribute('aria-checked', newState);

  // Apply setting
  if (newState) {
    enableDarkMode();
  } else {
    disableDarkMode();
  }
}

function enableDarkMode() {
  document.body.classList.add('dark-mode');
}

function disableDarkMode() {
  document.body.classList.remove('dark-mode');
}
</script>
```

### Checkbox-based Switch

```html
<label class="switch">
  <input
    type="checkbox"
    role="switch"
    id="notifications-switch">
  <span>Enable notifications</span>
</label>

<script>
const checkbox = document.getElementById('notifications-switch');

checkbox.addEventListener('change', () => {
  if (checkbox.checked) {
    enableNotifications();
  } else {
    disableNotifications();
  }
});
</script>
```

## Examples

### ✅ Good: Settings Toggle

```html
<div class="settings">
  <button role="switch" aria-checked="false">
    Auto-save
  </button>

  <button role="switch" aria-checked="true">
    Spell check
  </button>

  <button role="switch" aria-checked="false">
    Word wrap
  </button>
</div>
```

### ✅ Good: Switch with Description

```html
<button
  role="switch"
  aria-checked="false"
  aria-describedby="location-desc">
  Location services
</button>

<p id="location-desc">
  Allow apps to access your location for personalized content.
</p>
```

### ✅ Good: React Switch Component

```jsx
function Switch({ label, checked, onChange, describedBy }) {
  const handleToggle = () => {
    onChange(!checked);
  };

  return (
    <button
      role="switch"
      aria-checked={checked}
      aria-describedby={describedBy}
      onClick={handleToggle}>
      {label}
    </button>
  );
}

// Usage
<Switch
  label="Dark mode"
  checked={isDarkMode}
  onChange={setIsDarkMode}
/>
```

### ✅ Good: Vue Switch Component

```vue
<template>
  <button
    role="switch"
    :aria-checked="modelValue"
    @click="toggle">
    {{ label }}
  </button>
</template>

<script>
export default {
  props: {
    label: String,
    modelValue: Boolean
  },
  emits: ['update:modelValue'],
  methods: {
    toggle() {
      this.$emit('update:modelValue', !this.modelValue);
    }
  }
};
</script>
```

### ❌ Bad Examples

```html
<!-- Label changes with state -->
<button role="switch" aria-checked="false">
  Turn on notifications
</button>
<!-- When ON: -->
<button role="switch" aria-checked="true">
  Turn off notifications  <!-- Label changed! Wrong! -->
</button>

<!-- Missing role="switch" -->
<button aria-checked="false">
  Dark mode
</button>

<!-- Missing aria-checked -->
<button role="switch">
  Dark mode
</button>

<!-- Not focusable -->
<div role="switch" aria-checked="false">
  Dark mode
</div>

<!-- Using aria-checked on native checkbox without role="switch" -->
<input type="checkbox" aria-checked="false">
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does switch have `role="switch"`?** (CRITICAL)
- [ ] **Does switch have `aria-checked="true|false"`?** (CRITICAL)
- [ ] **Does switch label stay constant (never changes)?** (CRITICAL)
- [ ] **Is switch focusable (button or tabindex="0")?** (CRITICAL)
- [ ] **Does Space key toggle the switch?** (CRITICAL)
- [ ] Does Enter key toggle the switch (optional but recommended)?
- [ ] Are related switches grouped in fieldset or role="group"?
- [ ] Does group have accessible label (legend or aria-labelledby)?
- [ ] Is aria-describedby used for additional context?
- [ ] Does switch have clear visual indication of ON/OFF state?

## Quick Reference

```
✅ DO:
- Use role="switch"
- Use aria-checked="true|false"
- Keep label text constant (don't change on toggle)
- Use <button> element (preferred)
- Make switch focusable
- Toggle on Space key
- Optionally toggle on Enter key
- Group related switches with fieldset or role="group"
- Provide clear visual ON/OFF indicators
- Use aria-describedby for additional context

❌ DON'T:
- Change label text when state changes
- Omit role="switch"
- Forget aria-checked
- Make switch non-focusable
- Skip keyboard toggle support
- Use checkbox without role="switch" for switches
- Confuse with checkbox (use checkbox for selection, switch for settings)

## Switch vs Checkbox:

Switch:
  - Immediate effect (changes apply instantly)
  - Binary on/off state
  - Settings and preferences
  - Example: "Dark mode", "Notifications"
  - Label describes feature (constant)

Checkbox:
  - Delayed effect (often requires submit/save)
  - Selection/deselection
  - Forms and data collection
  - Example: "I agree to terms", "Select all"
  - Label describes option (constant)

## Label Rules:

✅ Good labels (stay constant):
  - "Dark mode" (not "Enable/Disable dark mode")
  - "Notifications" (not "Turn on/off notifications")
  - "Auto-save" (not "Enable/Disable auto-save")
  - "Bluetooth" (not "Connect/Disconnect Bluetooth")

❌ Bad labels (change with state):
  - "Turn on WiFi" → "Turn off WiFi"
  - "Enable feature" → "Disable feature"
  - "Start" → "Stop"
```
