---
description: Instructions for proper listbox accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Listbox Accessibility

## CRITICAL RULES

**A listbox presents a list of options from which a user can select one or more items. Listboxes are static, non-editable widgets (unlike combobox).**

### 1. Use role="listbox" and role="option"

**The container MUST have `role="listbox"` and each item MUST have `role="option"`.**

```html
✅ Good - Proper listbox roles:
<ul role="listbox" aria-label="Available colors">
  <li role="option" aria-selected="false">Red</li>
  <li role="option" aria-selected="true">Blue</li>
  <li role="option" aria-selected="false">Green</li>
</ul>

❌ Bad - Missing roles:
<ul class="listbox">
  <li>Red</li>  <!-- Missing role="option"! -->
  <li>Blue</li>
</ul>

❌ Bad - Missing role="listbox":
<ul>  <!-- Missing role="listbox"! -->
  <li role="option">Red</li>
  <li role="option">Blue</li>
</ul>
```

### 2. Mark Selected Options with aria-selected

**All options MUST have `aria-selected="true"` (selected) or `aria-selected="false"` (not selected).**

```html
✅ Good - Using aria-selected:
<ul role="listbox" aria-label="Choose size">
  <li role="option" aria-selected="false">Small</li>
  <li role="option" aria-selected="true">Medium</li>
  <li role="option" aria-selected="false">Large</li>
</ul>

❌ Bad - Missing aria-selected:
<ul role="listbox">
  <li role="option">Small</li>  <!-- Missing aria-selected! -->
  <li role="option">Medium</li>
</ul>

❌ Bad - Using both aria-selected and aria-checked:
<ul role="listbox">
  <li role="option" aria-selected="true" aria-checked="true">Item</li>
  <!-- Don't use both! Choose one consistently -->
</ul>
```

**Note:** Use `aria-selected` OR `aria-checked`, not both in the same listbox.

### 3. Provide Accessible Label

**Every listbox MUST have an accessible label using `aria-label` or `aria-labelledby`.**

```html
✅ Good - Using aria-label:
<ul role="listbox" aria-label="Select your country">
  <li role="option" aria-selected="false">United States</li>
  <li role="option" aria-selected="false">Canada</li>
  <li role="option" aria-selected="false">Mexico</li>
</ul>

✅ Good - Using aria-labelledby:
<label id="country-label">Country</label>
<ul role="listbox" aria-labelledby="country-label">
  <li role="option" aria-selected="false">United States</li>
  <li role="option" aria-selected="false">Canada</li>
</ul>

❌ Bad - No accessible label:
<ul role="listbox">  <!-- Missing aria-label or aria-labelledby! -->
  <li role="option">Item 1</li>
</ul>
```

### 4. Implement Arrow Key Navigation

**Listboxes MUST support arrow key navigation.**

**Required keyboard interactions:**
- **Down Arrow**: Move focus to next option
- **Up Arrow**: Move focus to previous option
- **Home**: Move focus to first option (recommended for 5+ options)
- **End**: Move focus to last option (recommended for 5+ options)

**Single-select listbox:**
- Arrow keys may optionally select as they move focus
- **Space**: Toggle selection of focused option (optional)
- **Enter**: Activate selection and close (if part of a dialog/popup)

**Multi-select listbox:**
- **Space**: Toggle selection of focused option
- **Shift+Down/Up Arrow**: Extend selection (optional)
- **Control+A**: Select all (optional)

```javascript
// ✅ Good - Single-select keyboard navigation
listbox.addEventListener('keydown', (e) => {
  const options = Array.from(listbox.querySelectorAll('[role="option"]'));
  const currentIndex = options.indexOf(document.activeElement);

  switch(e.key) {
    case 'ArrowDown':
      e.preventDefault();
      const nextIndex = Math.min(currentIndex + 1, options.length - 1);
      options[nextIndex].focus();
      selectOption(options[nextIndex]);  // Optional: auto-select
      break;

    case 'ArrowUp':
      e.preventDefault();
      const prevIndex = Math.max(currentIndex - 1, 0);
      options[prevIndex].focus();
      selectOption(options[prevIndex]);  // Optional: auto-select
      break;

    case 'Home':
      e.preventDefault();
      options[0].focus();
      selectOption(options[0]);
      break;

    case 'End':
      e.preventDefault();
      options[options.length - 1].focus();
      selectOption(options[options.length - 1]);
      break;

    case ' ':
      e.preventDefault();
      selectOption(document.activeElement);
      break;
  }
});
```

### 5. Manage Focus with tabindex

**For roving tabindex approach: Only the focused/selected option should have `tabindex="0"`, all others `tabindex="-1"`.**

```html
✅ Good - Roving tabindex:
<ul role="listbox" aria-label="Colors">
  <li role="option" aria-selected="false" tabindex="-1">Red</li>
  <li role="option" aria-selected="true" tabindex="0">Blue</li>
  <li role="option" aria-selected="false" tabindex="-1">Green</li>
</ul>

✅ Good - Alternative: aria-activedescendant:
<ul role="listbox" aria-label="Colors" tabindex="0" aria-activedescendant="option-2">
  <li role="option" id="option-1" aria-selected="false">Red</li>
  <li role="option" id="option-2" aria-selected="true">Blue</li>
  <li role="option" id="option-3" aria-selected="false">Green</li>
</ul>

❌ Bad - All options have tabindex="0":
<ul role="listbox">
  <li role="option" tabindex="0">Red</li>
  <li role="option" tabindex="0">Blue</li>  <!-- Don't do this! -->
  <li role="option" tabindex="0">Green</li>
</ul>
```

## Complete Listbox Structure

### Single-Select Listbox

```html
<label id="size-label">Choose size</label>
<ul
  role="listbox"
  aria-labelledby="size-label"
  aria-activedescendant="size-m">
  <li id="size-s" role="option" aria-selected="false" tabindex="-1">
    Small
  </li>
  <li id="size-m" role="option" aria-selected="true" tabindex="0">
    Medium
  </li>
  <li id="size-l" role="option" aria-selected="false" tabindex="-1">
    Large
  </li>
  <li id="size-xl" role="option" aria-selected="false" tabindex="-1">
    Extra Large
  </li>
</ul>

<script>
const listbox = document.querySelector('[role="listbox"]');
const options = listbox.querySelectorAll('[role="option"]');

listbox.addEventListener('keydown', (e) => {
  const optionsArray = Array.from(options);
  const currentIndex = optionsArray.indexOf(document.activeElement);

  switch(e.key) {
    case 'ArrowDown':
      e.preventDefault();
      if (currentIndex < optionsArray.length - 1) {
        selectOption(optionsArray[currentIndex + 1]);
      }
      break;

    case 'ArrowUp':
      e.preventDefault();
      if (currentIndex > 0) {
        selectOption(optionsArray[currentIndex - 1]);
      }
      break;

    case 'Home':
      e.preventDefault();
      selectOption(optionsArray[0]);
      break;

    case 'End':
      e.preventDefault();
      selectOption(optionsArray[optionsArray.length - 1]);
      break;
  }
});

function selectOption(option) {
  // Deselect all options
  options.forEach(opt => {
    opt.setAttribute('aria-selected', 'false');
    opt.setAttribute('tabindex', '-1');
  });

  // Select and focus new option
  option.setAttribute('aria-selected', 'true');
  option.setAttribute('tabindex', '0');
  option.focus();

  // Update activedescendant
  listbox.setAttribute('aria-activedescendant', option.id);
}

// Click selection
options.forEach(option => {
  option.addEventListener('click', () => selectOption(option));
});
</script>
```

### Multi-Select Listbox

```html
<label id="toppings-label">Choose toppings</label>
<ul
  role="listbox"
  aria-labelledby="toppings-label"
  aria-multiselectable="true">
  <li role="option" aria-selected="false" tabindex="0">Pepperoni</li>
  <li role="option" aria-selected="true" tabindex="-1">Mushrooms</li>
  <li role="option" aria-selected="true" tabindex="-1">Onions</li>
  <li role="option" aria-selected="false" tabindex="-1">Peppers</li>
</ul>

<script>
const multiListbox = document.querySelector('[role="listbox"][aria-multiselectable="true"]');
const multiOptions = multiListbox.querySelectorAll('[role="option"]');

multiListbox.addEventListener('keydown', (e) => {
  const optionsArray = Array.from(multiOptions);
  const currentIndex = optionsArray.indexOf(document.activeElement);

  switch(e.key) {
    case 'ArrowDown':
      e.preventDefault();
      if (currentIndex < optionsArray.length - 1) {
        focusOption(optionsArray[currentIndex + 1]);
      }
      break;

    case 'ArrowUp':
      e.preventDefault();
      if (currentIndex > 0) {
        focusOption(optionsArray[currentIndex - 1]);
      }
      break;

    case ' ':
      e.preventDefault();
      toggleSelection(document.activeElement);
      break;

    case 'Home':
      e.preventDefault();
      focusOption(optionsArray[0]);
      break;

    case 'End':
      e.preventDefault();
      focusOption(optionsArray[optionsArray.length - 1]);
      break;
  }
});

function focusOption(option) {
  multiOptions.forEach(opt => opt.setAttribute('tabindex', '-1'));
  option.setAttribute('tabindex', '0');
  option.focus();
}

function toggleSelection(option) {
  const isSelected = option.getAttribute('aria-selected') === 'true';
  option.setAttribute('aria-selected', !isSelected);
}

// Click toggle
multiOptions.forEach(option => {
  option.addEventListener('click', () => {
    focusOption(option);
    toggleSelection(option);
  });
});
</script>
```

## Examples

### ✅ Good: Single-Select Listbox

```html
<span id="country-label">Country</span>
<ul role="listbox" aria-labelledby="country-label">
  <li role="option" aria-selected="false" tabindex="-1">United States</li>
  <li role="option" aria-selected="true" tabindex="0">Canada</li>
  <li role="option" aria-selected="false" tabindex="-1">Mexico</li>
</ul>
```

### ✅ Good: Multi-Select Listbox

```html
<label id="features-label">Select features</label>
<ul
  role="listbox"
  aria-labelledby="features-label"
  aria-multiselectable="true">
  <li role="option" aria-selected="true" tabindex="0">WiFi</li>
  <li role="option" aria-selected="false" tabindex="-1">Bluetooth</li>
  <li role="option" aria-selected="true" tabindex="-1">GPS</li>
  <li role="option" aria-selected="false" tabindex="-1">Camera</li>
</ul>
```

### ✅ Good: Grouped Listbox

```html
<ul role="listbox" aria-label="Choose location">
  <li role="group" aria-labelledby="group-us">
    <span id="group-us">United States</span>
    <ul role="presentation">
      <li role="option" aria-selected="false">New York</li>
      <li role="option" aria-selected="false">Los Angeles</li>
    </ul>
  </li>
  <li role="group" aria-labelledby="group-ca">
    <span id="group-ca">Canada</span>
    <ul role="presentation">
      <li role="option" aria-selected="false">Toronto</li>
      <li role="option" aria-selected="true">Vancouver</li>
    </ul>
  </li>
</ul>
```

### ✅ Good: React Listbox Component

```jsx
function Listbox({ label, options, selectedId, onChange, multiSelect = false }) {
  const [focusedIndex, setFocusedIndex] = React.useState(0);
  const [selected, setSelected] = React.useState(
    multiSelect ? [] : selectedId
  );

  const handleKeyDown = (e, index) => {
    const optionsLength = options.length;

    switch(e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setFocusedIndex(Math.min(index + 1, optionsLength - 1));
        break;

      case 'ArrowUp':
        e.preventDefault();
        setFocusedIndex(Math.max(index - 1, 0));
        break;

      case 'Home':
        e.preventDefault();
        setFocusedIndex(0);
        break;

      case 'End':
        e.preventDefault();
        setFocusedIndex(optionsLength - 1);
        break;

      case ' ':
        e.preventDefault();
        if (multiSelect) {
          toggleMultiSelect(options[index].id);
        } else {
          selectSingle(options[index].id);
        }
        break;
    }
  };

  const selectSingle = (id) => {
    setSelected(id);
    onChange?.(id);
  };

  const toggleMultiSelect = (id) => {
    const newSelected = selected.includes(id)
      ? selected.filter(s => s !== id)
      : [...selected, id];
    setSelected(newSelected);
    onChange?.(newSelected);
  };

  const isSelected = (id) => {
    return multiSelect ? selected.includes(id) : selected === id;
  };

  return (
    <div>
      <label id="listbox-label">{label}</label>
      <ul
        role="listbox"
        aria-labelledby="listbox-label"
        aria-multiselectable={multiSelect}>
        {options.map((option, index) => (
          <li
            key={option.id}
            role="option"
            aria-selected={isSelected(option.id)}
            tabIndex={index === focusedIndex ? 0 : -1}
            onKeyDown={(e) => handleKeyDown(e, index)}
            onClick={() => {
              setFocusedIndex(index);
              multiSelect ? toggleMultiSelect(option.id) : selectSingle(option.id);
            }}>
            {option.label}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

### ❌ Bad Examples

```html
<!-- Missing role="listbox" -->
<ul aria-label="Colors">
  <li role="option">Red</li>
</ul>

<!-- Missing role="option" -->
<ul role="listbox" aria-label="Colors">
  <li>Red</li>
  <li>Blue</li>
</ul>

<!-- Missing aria-selected -->
<ul role="listbox" aria-label="Colors">
  <li role="option">Red</li>
  <li role="option">Blue</li>
</ul>

<!-- Missing accessible label -->
<ul role="listbox">
  <li role="option" aria-selected="false">Red</li>
</ul>

<!-- Multi-select missing aria-multiselectable -->
<ul role="listbox" aria-label="Features">
  <li role="option" aria-selected="true">WiFi</li>
  <li role="option" aria-selected="true">GPS</li>
</ul>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does container have `role="listbox"`?** (CRITICAL)
- [ ] **Do all items have `role="option"`?** (CRITICAL)
- [ ] **Do all options have `aria-selected="true|false"`?** (CRITICAL)
- [ ] **Does listbox have accessible label (aria-label or aria-labelledby)?** (CRITICAL)
- [ ] **Do arrow keys navigate between options?** (CRITICAL)
- [ ] **Is focus managed with roving tabindex or aria-activedescendant?** (CRITICAL)
- [ ] For multi-select: Is `aria-multiselectable="true"` set?
- [ ] For multi-select: Does Space toggle selection?
- [ ] Are Home/End keys supported (for 5+ options)?
- [ ] Are grouped options properly structured with role="group"?
- [ ] Do groups have accessible labels?

## Quick Reference

```
✅ DO:
- Use role="listbox" on container
- Use role="option" on all items
- Include aria-selected="true|false" on all options
- Provide aria-label or aria-labelledby
- Support arrow key navigation
- Use roving tabindex (focused: tabindex="0", others: tabindex="-1")
- Set aria-multiselectable="true" for multi-select
- Support Space to toggle selection (multi-select)
- Support Home/End for long lists (5+ items)
- Use role="group" for grouped options with aria-label

❌ DON'T:
- Omit role="listbox" or role="option"
- Forget aria-selected on options
- Skip accessible label
- Give all options tabindex="0"
- Use both aria-selected and aria-checked
- Forget aria-multiselectable for multi-select
- Use listbox for interactive elements (use grid instead)
- Create very long option names (hard to understand)

## Single-Select vs Multi-Select:

Single-select:
  - Only one option selected at a time
  - Arrow keys may auto-select
  - Enter activates (if in dialog/popup)

Multi-select:
  - Multiple options can be selected
  - Requires aria-multiselectable="true"
  - Space toggles selection
  - Arrow keys move focus without changing selection
```
