---
description: Instructions for proper combobox accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Combobox Accessibility

## CRITICAL RULES

**A combobox is an input widget with an associated popup that can be a listbox, grid, tree, or dialog.**

### 1. Use role="combobox" on the Input Element

**The text input MUST have `role="combobox"` with required ARIA attributes.**

```html
✅ Good - Combobox with required attributes:
<input
  type="text"
  role="combobox"
  aria-expanded="false"
  aria-controls="listbox-1"
  aria-autocomplete="list"
  id="combobox-input">

<ul id="listbox-1" role="listbox" hidden>
  <li role="option">Option 1</li>
  <li role="option">Option 2</li>
</ul>

❌ Bad - Missing role="combobox":
<input
  type="text"
  aria-expanded="false"
  aria-controls="listbox-1">

❌ Bad - Missing aria-expanded:
<input
  type="text"
  role="combobox"
  aria-controls="listbox-1">
```

**Required ARIA attributes:**
- `role="combobox"` - Identifies the input
- `aria-expanded="true|false"` - Indicates popup state
- `aria-controls="{popup-id}"` - References popup element
- `aria-autocomplete="none|list|both"` - Indicates autocomplete behavior

**Optional attributes:**
- `aria-haspopup="listbox|grid|tree|dialog"` - Popup type (defaults to listbox)
- `aria-activedescendant="{option-id}"` - References focused option

### 2. Implement aria-activedescendant for Focus Management

**Use `aria-activedescendant` to indicate the focused option in the popup.**

DOM focus stays on the combobox input; assistive technology focus moves via `aria-activedescendant`.

```html
✅ Good - Using aria-activedescendant:
<input
  type="text"
  role="combobox"
  aria-expanded="true"
  aria-controls="listbox-1"
  aria-activedescendant="option-2">

<ul id="listbox-1" role="listbox">
  <li id="option-1" role="option">Apple</li>
  <li id="option-2" role="option" aria-selected="true">Banana</li>
  <li id="option-3" role="option">Cherry</li>
</ul>
```

**Key points:**
- DOM focus remains on the combobox input
- `aria-activedescendant` references the highlighted option ID
- Update `aria-activedescendant` as user navigates with arrow keys
- Use `aria-selected="true"` on the currently highlighted option

### 3. Provide Required Keyboard Navigation

**Comboboxes MUST support specific keyboard interactions.**

**When focus is on combobox:**
- **Down Arrow**: Open popup if closed; move to next option if open
- **Up Arrow**: Open popup if closed; move to previous option if open
- **Enter**: Accept current option and close popup
- **Escape**: Close popup; optionally clear input
- **Alt+Down Arrow**: Open popup without moving focus
- **Typing characters**: Filter options or navigate (if editable)
- **Home/End**: Move to first/last option (when popup open)

```javascript
// ✅ Good - Keyboard event handling
input.addEventListener('keydown', (e) => {
  const isOpen = input.getAttribute('aria-expanded') === 'true';

  switch(e.key) {
    case 'ArrowDown':
      e.preventDefault();
      if (!isOpen) {
        openPopup();
      }
      moveToNextOption();
      break;

    case 'ArrowUp':
      e.preventDefault();
      if (!isOpen) {
        openPopup();
      }
      moveToPreviousOption();
      break;

    case 'Enter':
      if (isOpen) {
        e.preventDefault();
        selectCurrentOption();
        closePopup();
      }
      break;

    case 'Escape':
      if (isOpen) {
        closePopup();
      }
      break;

    case 'Home':
      if (isOpen) {
        e.preventDefault();
        moveToFirstOption();
      }
      break;

    case 'End':
      if (isOpen) {
        e.preventDefault();
        moveToLastOption();
      }
      break;
  }
});
```

### 4. Mark Options with role="option"

**Popup options MUST use proper roles and selection states.**

```html
✅ Good - Listbox popup with options:
<ul id="listbox" role="listbox">
  <li id="option-1" role="option">Alabama</li>
  <li id="option-2" role="option" aria-selected="true">Alaska</li>
  <li id="option-3" role="option">Arizona</li>
</ul>

✅ Good - Grid popup with options:
<div id="grid" role="grid">
  <div role="row">
    <div id="cell-1" role="gridcell" tabindex="-1">Item 1</div>
  </div>
</div>

❌ Bad - Missing role="option":
<ul id="listbox" role="listbox">
  <li id="option-1">Alabama</li>  <!-- Missing role="option"! -->
  <li id="option-2">Alaska</li>
</ul>
```

**Popup types:**
- `role="listbox"` - Most common, for simple lists
- `role="grid"` - For tabular data navigation
- `role="tree"` - For hierarchical navigation
- `role="dialog"` - For complex selection interfaces

### 5. Provide Accessible Label

**Every combobox MUST have an accessible label.**

```html
✅ Good - Using <label>:
<label for="state-select">State</label>
<input
  id="state-select"
  type="text"
  role="combobox"
  aria-expanded="false"
  aria-controls="states-listbox">

✅ Good - Using aria-labelledby:
<span id="state-label">State</span>
<input
  type="text"
  role="combobox"
  aria-labelledby="state-label"
  aria-expanded="false"
  aria-controls="states-listbox">

✅ Good - Using aria-label:
<input
  type="text"
  role="combobox"
  aria-label="Select state"
  aria-expanded="false"
  aria-controls="states-listbox">
```

## Complete Combobox Structure

```html
<label for="fruit-combobox">Fruit</label>
<div class="combobox-wrapper">
  <input
    id="fruit-combobox"
    type="text"
    role="combobox"
    aria-expanded="false"
    aria-controls="fruit-listbox"
    aria-autocomplete="list"
    aria-activedescendant="">

  <ul id="fruit-listbox" role="listbox" hidden>
    <li id="option-apple" role="option">Apple</li>
    <li id="option-banana" role="option">Banana</li>
    <li id="option-cherry" role="option">Cherry</li>
    <li id="option-date" role="option">Date</li>
    <li id="option-elderberry" role="option">Elderberry</li>
  </ul>
</div>

<script>
const combobox = document.getElementById('fruit-combobox');
const listbox = document.getElementById('fruit-listbox');
const options = listbox.querySelectorAll('[role="option"]');
let currentIndex = -1;

combobox.addEventListener('input', (e) => {
  const filter = e.target.value.toLowerCase();
  filterOptions(filter);
  openListbox();
});

combobox.addEventListener('keydown', (e) => {
  const isOpen = combobox.getAttribute('aria-expanded') === 'true';

  switch(e.key) {
    case 'ArrowDown':
      e.preventDefault();
      if (!isOpen) openListbox();
      moveToNextOption();
      break;

    case 'ArrowUp':
      e.preventDefault();
      if (!isOpen) openListbox();
      moveToPreviousOption();
      break;

    case 'Enter':
      if (isOpen && currentIndex >= 0) {
        e.preventDefault();
        selectOption(currentIndex);
      }
      break;

    case 'Escape':
      closeListbox();
      break;

    case 'Home':
      if (isOpen) {
        e.preventDefault();
        setActiveOption(0);
      }
      break;

    case 'End':
      if (isOpen) {
        e.preventDefault();
        setActiveOption(options.length - 1);
      }
      break;
  }
});

function openListbox() {
  listbox.removeAttribute('hidden');
  combobox.setAttribute('aria-expanded', 'true');
}

function closeListbox() {
  listbox.setAttribute('hidden', '');
  combobox.setAttribute('aria-expanded', 'false');
  combobox.removeAttribute('aria-activedescendant');
  currentIndex = -1;
}

function setActiveOption(index) {
  // Remove previous selection
  options.forEach(opt => opt.removeAttribute('aria-selected'));

  // Set new selection
  if (index >= 0 && index < options.length) {
    currentIndex = index;
    const option = options[index];
    option.setAttribute('aria-selected', 'true');
    combobox.setAttribute('aria-activedescendant', option.id);

    // Scroll into view
    option.scrollIntoView({ block: 'nearest' });
  }
}

function moveToNextOption() {
  setActiveOption(Math.min(currentIndex + 1, options.length - 1));
}

function moveToPreviousOption() {
  setActiveOption(Math.max(currentIndex - 1, 0));
}

function selectOption(index) {
  if (index >= 0 && index < options.length) {
    combobox.value = options[index].textContent;
    closeListbox();
  }
}

function filterOptions(filter) {
  let visibleCount = 0;
  options.forEach(option => {
    const text = option.textContent.toLowerCase();
    const matches = text.includes(filter);
    option.hidden = !matches;
    if (matches) visibleCount++;
  });

  // Auto-select first visible option
  if (visibleCount > 0) {
    const firstVisible = Array.from(options).findIndex(opt => !opt.hidden);
    setActiveOption(firstVisible);
  }
}
</script>
```

## Examples

### ✅ Good: Autocomplete Combobox

```html
<label for="country">Country</label>
<input
  id="country"
  type="text"
  role="combobox"
  aria-expanded="false"
  aria-controls="country-list"
  aria-autocomplete="list"
  placeholder="Type to search">

<ul id="country-list" role="listbox" hidden>
  <li id="country-us" role="option">United States</li>
  <li id="country-uk" role="option">United Kingdom</li>
  <li id="country-ca" role="option">Canada</li>
</ul>
```

### ✅ Good: Select-Only Combobox

```html
<label for="month">Month</label>
<input
  id="month"
  type="text"
  role="combobox"
  aria-expanded="false"
  aria-controls="month-list"
  aria-autocomplete="none"
  readonly>
<button aria-label="Show months" onclick="openMonthList()">▼</button>

<ul id="month-list" role="listbox" hidden>
  <li id="month-jan" role="option">January</li>
  <li id="month-feb" role="option">February</li>
  <!-- ... -->
</ul>
```

### ✅ Good: React Combobox Component

```jsx
function Combobox({ label, options, value, onChange }) {
  const [isOpen, setIsOpen] = React.useState(false);
  const [activeIndex, setActiveIndex] = React.useState(-1);
  const [filterText, setFilterText] = React.useState(value || '');

  const filteredOptions = options.filter(opt =>
    opt.toLowerCase().includes(filterText.toLowerCase())
  );

  const handleKeyDown = (e) => {
    switch(e.key) {
      case 'ArrowDown':
        e.preventDefault();
        if (!isOpen) setIsOpen(true);
        setActiveIndex(Math.min(activeIndex + 1, filteredOptions.length - 1));
        break;

      case 'ArrowUp':
        e.preventDefault();
        if (!isOpen) setIsOpen(true);
        setActiveIndex(Math.max(activeIndex - 1, 0));
        break;

      case 'Enter':
        if (isOpen && activeIndex >= 0) {
          e.preventDefault();
          onChange(filteredOptions[activeIndex]);
          setIsOpen(false);
        }
        break;

      case 'Escape':
        setIsOpen(false);
        break;
    }
  };

  return (
    <div>
      <label htmlFor="combobox-input">{label}</label>
      <input
        id="combobox-input"
        type="text"
        role="combobox"
        aria-expanded={isOpen}
        aria-controls="combobox-listbox"
        aria-autocomplete="list"
        aria-activedescendant={
          activeIndex >= 0 ? `option-${activeIndex}` : ''
        }
        value={filterText}
        onChange={(e) => {
          setFilterText(e.target.value);
          setIsOpen(true);
        }}
        onKeyDown={handleKeyDown}
      />

      {isOpen && (
        <ul id="combobox-listbox" role="listbox">
          {filteredOptions.map((option, index) => (
            <li
              key={index}
              id={`option-${index}`}
              role="option"
              aria-selected={index === activeIndex}
              onClick={() => {
                onChange(option);
                setIsOpen(false);
              }}>
              {option}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

### ❌ Bad Examples

```html
<!-- Missing role="combobox" -->
<input type="text" aria-expanded="false">

<!-- Missing aria-expanded -->
<input type="text" role="combobox" aria-controls="list">

<!-- Missing role="option" on items -->
<ul id="list" role="listbox">
  <li>Option 1</li>  <!-- Needs role="option"! -->
</ul>

<!-- No accessible label -->
<input
  type="text"
  role="combobox"
  aria-expanded="false">
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does input have `role="combobox"`?** (CRITICAL)
- [ ] **Does combobox have `aria-expanded`?** (CRITICAL)
- [ ] **Does combobox have `aria-controls`?** (CRITICAL)
- [ ] **Does combobox have accessible label?** (CRITICAL)
- [ ] **Do popup items have proper roles (option/gridcell)?** (CRITICAL)
- [ ] **Is `aria-activedescendant` updated on navigation?** (CRITICAL)
- [ ] Does combobox support arrow key navigation?
- [ ] Does Enter key select option?
- [ ] Does Escape key close popup?
- [ ] Is `aria-autocomplete` set appropriately?
- [ ] Are options properly filtered on input?

## Quick Reference

```
✅ DO:
- Use role="combobox" on input element
- Include aria-expanded="true|false"
- Include aria-controls="{popup-id}"
- Provide accessible label
- Use aria-activedescendant for focus management
- Mark options with role="option"
- Support arrow keys, Enter, Escape
- Keep DOM focus on combobox input
- Update aria-selected on highlighted option

❌ DON'T:
- Omit role="combobox"
- Forget aria-expanded or aria-controls
- Miss accessible label
- Forget role="option" on items
- Move DOM focus to popup options
- Ignore keyboard navigation
- Use without aria-activedescendant
```
