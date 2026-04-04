---
description: Instructions for proper menu button accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Menu Button Accessibility

## CRITICAL RULES

**A menu button is a button that opens a menu. Common examples: dropdown menus, action menus, context menus.**

### 1. Use Button Element with aria-haspopup

**The trigger MUST be a `<button>` element with `aria-haspopup="true"` or `aria-haspopup="menu"`.**

```html
✅ Good - Button with aria-haspopup:
<button
  id="menu-btn"
  aria-haspopup="true"
  aria-expanded="false"
  aria-controls="dropdown-menu">
  Actions
</button>

<ul id="dropdown-menu" role="menu" hidden>
  <li role="menuitem">Edit</li>
  <li role="menuitem">Delete</li>
</ul>

❌ Bad - Missing aria-haspopup:
<button id="menu-btn" aria-expanded="false">
  Actions  <!-- Missing aria-haspopup! -->
</button>

❌ Bad - Using div instead of button:
<div onclick="openMenu()">  <!-- Should be <button>! -->
  Actions
</div>
```

### 2. Use aria-expanded to Indicate Menu State

**The button MUST have `aria-expanded="true"` when menu is open, `aria-expanded="false"` when closed.**

```html
✅ Good - Proper aria-expanded usage:
<!-- Closed state -->
<button
  aria-haspopup="true"
  aria-expanded="false"
  aria-controls="menu-1">
  File
</button>

<!-- Open state -->
<button
  aria-haspopup="true"
  aria-expanded="true"
  aria-controls="menu-1">
  File
</button>

❌ Bad - Missing aria-expanded:
<button aria-haspopup="true">
  File  <!-- Missing aria-expanded! -->
</button>
```

### 3. Menu Must Use role="menu" and role="menuitem"

**The menu MUST follow the Menu pattern with proper roles.**

See [menu.instructions.md](menu.instructions.md) for complete menu requirements.

```html
✅ Good - Proper menu structure:
<button
  id="actions-btn"
  aria-haspopup="true"
  aria-expanded="false"
  aria-controls="actions-menu">
  Actions
</button>

<ul id="actions-menu" role="menu" aria-labelledby="actions-btn" hidden>
  <li role="menuitem" tabindex="0">Edit</li>
  <li role="menuitem" tabindex="-1">Delete</li>
  <li role="menuitem" tabindex="-1">Share</li>
</ul>

❌ Bad - Missing menu roles:
<button aria-haspopup="true" aria-expanded="false">
  Actions
</button>
<ul id="menu">  <!-- Missing role="menu"! -->
  <li>Edit</li>  <!-- Missing role="menuitem"! -->
</ul>
```

### 4. Implement Required Keyboard Interactions

**The menu button MUST support Enter and Space to open the menu.**

**Required keyboard support:**
- **Enter**: Open menu and move focus to first menu item
- **Space**: Open menu and move focus to first menu item

**Optional (recommended) keyboard support:**
- **Down Arrow**: Open menu and move focus to first menu item
- **Up Arrow**: Open menu and move focus to last menu item

```javascript
// ✅ Good - Keyboard event handling
menuButton.addEventListener('keydown', (e) => {
  switch(e.key) {
    case 'Enter':
    case ' ':
      e.preventDefault();
      openMenu();
      focusFirstMenuItem();
      break;

    case 'ArrowDown':
      e.preventDefault();
      openMenu();
      focusFirstMenuItem();
      break;

    case 'ArrowUp':
      e.preventDefault();
      openMenu();
      focusLastMenuItem();
      break;
  }
});
```

### 5. Move Focus to Menu When Opening

**When the menu opens, focus MUST move to the first menu item (or last if opened with Up Arrow).**

When menu closes, focus MUST return to the button.

```javascript
// ✅ Good - Focus management
function openMenu() {
  const menu = document.getElementById('actions-menu');
  const menuItems = menu.querySelectorAll('[role="menuitem"]');

  // Show menu
  menu.removeAttribute('hidden');
  menuButton.setAttribute('aria-expanded', 'true');

  // Move focus to first menu item
  menuItems[0].focus();
}

function closeMenu() {
  const menu = document.getElementById('actions-menu');

  // Hide menu
  menu.setAttribute('hidden', '');
  menuButton.setAttribute('aria-expanded', 'false');

  // Return focus to button
  menuButton.focus();
}
```

## Complete Menu Button Structure

```html
<button
  id="actions-button"
  aria-haspopup="true"
  aria-expanded="false"
  aria-controls="actions-menu">
  Actions ▾
</button>

<ul id="actions-menu" role="menu" aria-labelledby="actions-button" hidden>
  <li role="menuitem" tabindex="0">Edit</li>
  <li role="menuitem" tabindex="-1">Duplicate</li>
  <li role="menuitem" tabindex="-1">Delete</li>
  <li role="separator"></li>
  <li role="menuitem" tabindex="-1">Share</li>
</ul>

<script>
const menuButton = document.getElementById('actions-button');
const menu = document.getElementById('actions-menu');
const menuItems = menu.querySelectorAll('[role="menuitem"]:not([aria-disabled="true"])');

// Button click
menuButton.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  if (isOpen) {
    closeMenu();
  } else {
    openMenu();
  }
});

// Button keyboard
menuButton.addEventListener('keydown', (e) => {
  switch(e.key) {
    case 'Enter':
    case ' ':
      e.preventDefault();
      openMenu();
      break;

    case 'ArrowDown':
      e.preventDefault();
      openMenu();
      focusMenuItem(0);
      break;

    case 'ArrowUp':
      e.preventDefault();
      openMenu();
      focusMenuItem(menuItems.length - 1);
      break;
  }
});

// Menu keyboard navigation
menu.addEventListener('keydown', (e) => {
  const itemsArray = Array.from(menuItems);
  const currentIndex = itemsArray.indexOf(document.activeElement);

  switch(e.key) {
    case 'ArrowDown':
      e.preventDefault();
      const nextIndex = (currentIndex + 1) % itemsArray.length;
      focusMenuItem(nextIndex);
      break;

    case 'ArrowUp':
      e.preventDefault();
      const prevIndex = currentIndex === 0 ? itemsArray.length - 1 : currentIndex - 1;
      focusMenuItem(prevIndex);
      break;

    case 'Enter':
    case ' ':
      e.preventDefault();
      activateMenuItem(e.target);
      closeMenu();
      break;

    case 'Escape':
      closeMenu();
      break;

    case 'Tab':
      closeMenu();
      break;
  }
});

function openMenu() {
  menu.removeAttribute('hidden');
  menuButton.setAttribute('aria-expanded', 'true');
  focusMenuItem(0);
}

function closeMenu() {
  menu.setAttribute('hidden', '');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.focus();
}

function focusMenuItem(index) {
  if (index >= 0 && index < menuItems.length) {
    menuItems[index].focus();
  }
}

function activateMenuItem(item) {
  console.log('Activated:', item.textContent);
  // Perform action here
}

// Close menu when clicking outside
document.addEventListener('click', (e) => {
  if (!menu.contains(e.target) && e.target !== menuButton) {
    closeMenu();
  }
});
</script>
```

## Examples

### ✅ Good: Actions Menu Button

```html
<button
  id="card-actions"
  aria-haspopup="true"
  aria-expanded="false"
  aria-controls="card-menu">
  ⋮
</button>

<ul id="card-menu" role="menu" aria-labelledby="card-actions" hidden>
  <li role="menuitem" tabindex="0">Edit</li>
  <li role="menuitem" tabindex="-1">Duplicate</li>
  <li role="menuitem" tabindex="-1">Archive</li>
  <li role="separator"></li>
  <li role="menuitem" tabindex="-1">Delete</li>
</ul>
```

### ✅ Good: User Profile Menu

```html
<button
  id="user-menu-btn"
  aria-haspopup="true"
  aria-expanded="false"
  aria-controls="user-menu"
  aria-label="User menu">
  <img src="avatar.jpg" alt="">
  John Doe
</button>

<ul id="user-menu" role="menu" aria-labelledby="user-menu-btn" hidden>
  <li role="menuitem" tabindex="0">Profile</li>
  <li role="menuitem" tabindex="-1">Settings</li>
  <li role="separator"></li>
  <li role="menuitem" tabindex="-1">Sign Out</li>
</ul>
```

### ✅ Good: React Menu Button Component

```jsx
function MenuButton({ label, items }) {
  const [isOpen, setIsOpen] = React.useState(false);
  const buttonRef = React.useRef(null);
  const menuRef = React.useRef(null);
  const [focusedIndex, setFocusedIndex] = React.useState(0);

  const openMenu = () => {
    setIsOpen(true);
    setFocusedIndex(0);
  };

  const closeMenu = () => {
    setIsOpen(false);
    buttonRef.current?.focus();
  };

  const handleButtonKeyDown = (e) => {
    switch(e.key) {
      case 'Enter':
      case ' ':
        e.preventDefault();
        openMenu();
        break;

      case 'ArrowDown':
        e.preventDefault();
        openMenu();
        setFocusedIndex(0);
        break;

      case 'ArrowUp':
        e.preventDefault();
        openMenu();
        setFocusedIndex(items.length - 1);
        break;
    }
  };

  const handleMenuKeyDown = (e, index) => {
    switch(e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setFocusedIndex((index + 1) % items.length);
        break;

      case 'ArrowUp':
        e.preventDefault();
        setFocusedIndex(index === 0 ? items.length - 1 : index - 1);
        break;

      case 'Enter':
      case ' ':
        e.preventDefault();
        items[index].action();
        closeMenu();
        break;

      case 'Escape':
      case 'Tab':
        closeMenu();
        break;
    }
  };

  React.useEffect(() => {
    if (isOpen && menuRef.current) {
      const focusableItems = menuRef.current.querySelectorAll('[role="menuitem"]');
      focusableItems[focusedIndex]?.focus();
    }
  }, [isOpen, focusedIndex]);

  return (
    <div>
      <button
        ref={buttonRef}
        aria-haspopup="true"
        aria-expanded={isOpen}
        onClick={() => setIsOpen(!isOpen)}
        onKeyDown={handleButtonKeyDown}>
        {label}
      </button>

      {isOpen && (
        <ul ref={menuRef} role="menu">
          {items.map((item, index) => (
            <li
              key={index}
              role="menuitem"
              tabIndex={index === focusedIndex ? 0 : -1}
              onClick={() => {
                item.action();
                closeMenu();
              }}
              onKeyDown={(e) => handleMenuKeyDown(e, index)}>
              {item.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

// Usage
<MenuButton
  label="Actions"
  items={[
    { label: 'Edit', action: () => console.log('Edit') },
    { label: 'Delete', action: () => console.log('Delete') },
    { label: 'Share', action: () => console.log('Share') }
  ]}
/>
```

### ❌ Bad Examples

```html
<!-- Missing aria-haspopup -->
<button id="menu-btn" aria-expanded="false">
  Actions
</button>

<!-- Missing aria-expanded -->
<button aria-haspopup="true">
  Actions
</button>

<!-- Not a button -->
<div class="menu-button" onclick="openMenu()">
  Actions
</div>

<!-- Menu missing roles -->
<button aria-haspopup="true" aria-expanded="false">
  Actions
</button>
<ul id="menu">
  <li>Edit</li>
  <li>Delete</li>
</ul>
```

## WCAG References

- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Is the trigger a `<button>` element?** (CRITICAL)
- [ ] **Does button have `aria-haspopup="true"` or `aria-haspopup="menu"`?** (CRITICAL)
- [ ] **Does button have `aria-expanded` attribute?** (CRITICAL)
- [ ] **Does menu have `role="menu"`?** (CRITICAL)
- [ ] **Do menu items have `role="menuitem"`?** (CRITICAL)
- [ ] **Does Enter/Space open menu and move focus to first item?** (CRITICAL)
- [ ] **Does menu close and return focus to button?** (CRITICAL)
- [ ] Do Down Arrow and Up Arrow open menu with directional focus?
- [ ] Does button have `aria-controls` referencing menu ID?
- [ ] Does menu have accessible label (aria-labelledby)?
- [ ] Is menu hidden when closed (using `hidden` attribute)?
- [ ] Does clicking outside close the menu?

## Quick Reference

```
✅ DO:
- Use <button> element for trigger
- Include aria-haspopup="true" or aria-haspopup="menu"
- Include aria-expanded="true|false"
- Use role="menu" and role="menuitem" for menu
- Open menu with Enter or Space
- Move focus to first menu item when opening
- Return focus to button when closing
- Optionally support Down/Up arrows to open menu
- Follow Menu pattern for menu keyboard navigation

❌ DON'T:
- Use div or span instead of button
- Forget aria-haspopup or aria-expanded
- Leave focus on button when menu opens
- Forget to return focus when menu closes
- Skip menu roles (role="menu", role="menuitem")
- Ignore keyboard navigation requirements

## Related Patterns:

See [menu.instructions.md](menu.instructions.md) for complete menu keyboard navigation and structure requirements.

See [buttons.instructions.md](buttons.instructions.md) for general button accessibility.
```
