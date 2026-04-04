---
description: Instructions for proper menu and menubar accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Menu and Menubar Accessibility

## CRITICAL RULES

**Menus offer a list of actions or functions. Menubars are visually persistent horizontal menus, typically at the top of an application.**

### 1. Use role="menu" or role="menubar" with role="menuitem"

**Menu containers MUST use `role="menu"` (or `role="menubar"`) and items MUST use `role="menuitem"`.**

```html
✅ Good - Proper menu roles:
<ul role="menu" aria-label="File">
  <li role="menuitem">New</li>
  <li role="menuitem">Open</li>
  <li role="menuitem">Save</li>
</ul>

✅ Good - Menubar:
<ul role="menubar" aria-label="Main Navigation">
  <li role="menuitem" aria-haspopup="true">File</li>
  <li role="menuitem" aria-haspopup="true">Edit</li>
  <li role="menuitem" aria-haspopup="true">View</li>
</ul>

❌ Bad - Missing roles:
<ul class="menu">
  <li>New</li>  <!-- Missing role="menuitem"! -->
  <li>Open</li>
</ul>
```

**Menu item types:**
- `role="menuitem"` - Standard action item
- `role="menuitemcheckbox"` - Checkable item (toggled on/off)
- `role="menuitemradio"` - Radio button item (one selected in group)

```html
✅ Good - Checkbox menu items:
<ul role="menu">
  <li role="menuitemcheckbox" aria-checked="true">Show Toolbar</li>
  <li role="menuitemcheckbox" aria-checked="false">Show Sidebar</li>
</ul>

✅ Good - Radio menu items:
<ul role="menu">
  <li role="menuitemradio" aria-checked="true">Small</li>
  <li role="menuitemradio" aria-checked="false">Medium</li>
  <li role="menuitemradio" aria-checked="false">Large</li>
</ul>
```

### 2. Mark Submenus with aria-haspopup and aria-expanded

**Parent menu items with submenus MUST have `aria-haspopup="true"` (or `"menu"`) and `aria-expanded`.**

```html
✅ Good - Submenu indication:
<ul role="menu">
  <li
    role="menuitem"
    aria-haspopup="true"
    aria-expanded="false"
    id="file-menu">
    File
    <ul role="menu" hidden>
      <li role="menuitem">New</li>
      <li role="menuitem">Open</li>
    </ul>
  </li>
</ul>

❌ Bad - Missing aria-haspopup:
<li role="menuitem" id="file-menu">  <!-- Missing aria-haspopup! -->
  File
  <ul role="menu">
    <li role="menuitem">New</li>
  </ul>
</li>
```

**Important:** Submenu MUST be a sibling element immediately following its parent menuitem.

### 3. Implement Arrow Key Navigation

**Menus MUST support arrow key navigation, NOT Tab key navigation.**

**Horizontal menubar:**
- **Right Arrow**: Next menuitem; open submenu if present
- **Left Arrow**: Previous menuitem; close submenu and return to parent
- **Down Arrow**: Open submenu (or move to first submenu item)
- **Up Arrow**: Move to last submenu item (optional)

**Vertical menu:**
- **Down Arrow**: Next menuitem
- **Up Arrow**: Previous menuitem
- **Right Arrow**: Open submenu; move to first submenu item
- **Left Arrow**: Close submenu; return to parent menuitem

**All menus:**
- **Enter**: Activate menuitem; open submenu if present
- **Space**: Optional - activate menuitem or toggle checkbox/radio
- **Escape**: Close menu; return focus to trigger element
- **Home**: Move to first menuitem (optional)
- **End**: Move to last menuitem (optional)
- **Character keys**: Move to next item starting with typed character (optional)

```javascript
// ✅ Good - Menu keyboard navigation
menu.addEventListener('keydown', (e) => {
  const items = Array.from(menu.querySelectorAll('[role="menuitem"]'));
  const currentIndex = items.indexOf(document.activeElement);

  switch(e.key) {
    case 'ArrowDown':
      e.preventDefault();
      const nextIndex = (currentIndex + 1) % items.length;
      items[nextIndex].focus();
      break;

    case 'ArrowUp':
      e.preventDefault();
      const prevIndex = currentIndex === 0 ? items.length - 1 : currentIndex - 1;
      items[prevIndex].focus();
      break;

    case 'ArrowRight':
      // Open submenu if present
      const submenu = e.target.querySelector('[role="menu"]');
      if (submenu) {
        openSubmenu(submenu);
      }
      break;

    case 'ArrowLeft':
      // Close submenu and return to parent
      closeSubmenu();
      break;

    case 'Enter':
    case ' ':
      e.preventDefault();
      activateMenuItem(e.target);
      break;

    case 'Escape':
      closeMenu();
      returnFocusToTrigger();
      break;

    case 'Home':
      e.preventDefault();
      items[0].focus();
      break;

    case 'End':
      e.preventDefault();
      items[items.length - 1].focus();
      break;
  }
});
```

### 4. Manage Focus with tabindex and aria-activedescendant

**Only the currently focused menuitem should be in tab sequence.**

**Two approaches:**

**Approach 1: Roving tabindex** (recommended)
- Active menuitem: `tabindex="0"`
- All other menuitems: `tabindex="-1"`

```html
✅ Good - Roving tabindex:
<ul role="menu">
  <li role="menuitem" tabindex="0">New</li>
  <li role="menuitem" tabindex="-1">Open</li>
  <li role="menuitem" tabindex="-1">Save</li>
</ul>
```

**Approach 2: aria-activedescendant**
- Menu container manages `aria-activedescendant`
- All menuitems have `tabindex="-1"`

```html
✅ Good - aria-activedescendant:
<ul role="menu" tabindex="0" aria-activedescendant="menuitem-1">
  <li role="menuitem" id="menuitem-1">New</li>
  <li role="menuitem" id="menuitem-2">Open</li>
  <li role="menuitem" id="menuitem-3">Save</li>
</ul>
```

### 5. Tab Key Behavior - Enter and Exit Only

**Tab and Shift+Tab MUST NOT navigate within the menu. They move focus out of the menu.**

```javascript
// ✅ Good - Tab exits menu
menu.addEventListener('keydown', (e) => {
  if (e.key === 'Tab') {
    // Allow default behavior - Tab exits menu
    closeMenu();
    // Focus naturally moves to next/previous focusable element
  }
});

// ❌ Bad - Tab navigates within menu
menu.addEventListener('keydown', (e) => {
  if (e.key === 'Tab') {
    e.preventDefault();  // Don't do this!
    moveToNextMenuItem();
  }
});
```

**Key principle:** Arrow keys navigate within menus, Tab key navigates between major UI components.

## Complete Menu Structure

```html
<!-- Menu button trigger -->
<button
  id="menu-button"
  aria-haspopup="true"
  aria-expanded="false"
  aria-controls="file-menu"
  onclick="toggleMenu()">
  File
</button>

<!-- Menu -->
<ul id="file-menu" role="menu" aria-labelledby="menu-button" hidden>
  <li role="menuitem" tabindex="0">
    New File
  </li>
  <li role="menuitem" tabindex="-1">
    Open File...
  </li>
  <li role="menuitem" tabindex="-1">
    Save
  </li>
  <li role="separator"></li>
  <li
    role="menuitem"
    tabindex="-1"
    aria-haspopup="true"
    aria-expanded="false">
    Recent Files
    <ul role="menu" hidden>
      <li role="menuitem" tabindex="-1">Document1.txt</li>
      <li role="menuitem" tabindex="-1">Document2.txt</li>
    </ul>
  </li>
  <li role="separator"></li>
  <li role="menuitem" tabindex="-1" aria-disabled="true">
    Print
  </li>
  <li role="menuitem" tabindex="-1">
    Exit
  </li>
</ul>

<script>
const menuButton = document.getElementById('menu-button');
const menu = document.getElementById('file-menu');
const menuItems = menu.querySelectorAll('[role="menuitem"]:not([aria-disabled="true"])');

function toggleMenu() {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';

  if (isOpen) {
    closeMenu();
  } else {
    openMenu();
  }
}

function openMenu() {
  menu.removeAttribute('hidden');
  menuButton.setAttribute('aria-expanded', 'true');

  // Focus first item
  menuItems[0].focus();
}

function closeMenu() {
  menu.setAttribute('hidden', '');
  menuButton.setAttribute('aria-expanded', 'false');

  // Return focus to button
  menuButton.focus();
}

menu.addEventListener('keydown', (e) => {
  const itemsArray = Array.from(menuItems);
  const currentIndex = itemsArray.indexOf(document.activeElement);

  switch(e.key) {
    case 'ArrowDown':
      e.preventDefault();
      const nextIndex = (currentIndex + 1) % itemsArray.length;
      itemsArray[nextIndex].focus();
      break;

    case 'ArrowUp':
      e.preventDefault();
      const prevIndex = currentIndex === 0 ? itemsArray.length - 1 : currentIndex - 1;
      itemsArray[prevIndex].focus();
      break;

    case 'Home':
      e.preventDefault();
      itemsArray[0].focus();
      break;

    case 'End':
      e.preventDefault();
      itemsArray[itemsArray.length - 1].focus();
      break;

    case 'Escape':
      closeMenu();
      break;

    case 'Enter':
    case ' ':
      e.preventDefault();
      // Activate menu item
      const item = e.target;
      if (!item.hasAttribute('aria-haspopup')) {
        // Perform action
        console.log('Activated:', item.textContent);
        closeMenu();
      }
      break;

    case 'Tab':
      // Allow default - closes menu and moves focus
      closeMenu();
      break;
  }
});

// Close menu when clicking outside
document.addEventListener('click', (e) => {
  if (!menu.contains(e.target) && e.target !== menuButton) {
    closeMenu();
  }
});
</script>
```

## Examples

### ✅ Good: Simple Menu

```html
<button id="actions-btn" aria-haspopup="true" aria-expanded="false">
  Actions
</button>

<ul role="menu" aria-labelledby="actions-btn" hidden>
  <li role="menuitem" tabindex="0">Edit</li>
  <li role="menuitem" tabindex="-1">Delete</li>
  <li role="menuitem" tabindex="-1">Share</li>
</ul>
```

### ✅ Good: Menu with Checkboxes

```html
<ul role="menu" aria-label="View Options">
  <li role="menuitemcheckbox" aria-checked="true" tabindex="0">
    Show Line Numbers
  </li>
  <li role="menuitemcheckbox" aria-checked="false" tabindex="-1">
    Word Wrap
  </li>
  <li role="menuitemcheckbox" aria-checked="true" tabindex="-1">
    Minimap
  </li>
</ul>
```

### ✅ Good: Menubar with Submenus

```html
<ul role="menubar" aria-label="Main Menu">
  <li role="menuitem" aria-haspopup="true" aria-expanded="false" tabindex="0">
    File
    <ul role="menu" hidden>
      <li role="menuitem" tabindex="-1">New</li>
      <li role="menuitem" tabindex="-1">Open</li>
    </ul>
  </li>
  <li role="menuitem" aria-haspopup="true" aria-expanded="false" tabindex="-1">
    Edit
    <ul role="menu" hidden>
      <li role="menuitem" tabindex="-1">Cut</li>
      <li role="menuitem" tabindex="-1">Copy</li>
      <li role="menuitem" tabindex="-1">Paste</li>
    </ul>
  </li>
</ul>
```

### ✅ Good: React Menu Component

```jsx
function Menu({ items, label }) {
  const [focusedIndex, setFocusedIndex] = React.useState(0);
  const itemRefs = React.useRef([]);

  const handleKeyDown = (e, index) => {
    switch(e.key) {
      case 'ArrowDown':
        e.preventDefault();
        const nextIndex = (index + 1) % items.length;
        setFocusedIndex(nextIndex);
        itemRefs.current[nextIndex]?.focus();
        break;

      case 'ArrowUp':
        e.preventDefault();
        const prevIndex = index === 0 ? items.length - 1 : index - 1;
        setFocusedIndex(prevIndex);
        itemRefs.current[prevIndex]?.focus();
        break;

      case 'Enter':
      case ' ':
        e.preventDefault();
        items[index].action();
        break;
    }
  };

  return (
    <ul role="menu" aria-label={label}>
      {items.map((item, index) => (
        <li
          key={index}
          role="menuitem"
          tabIndex={index === focusedIndex ? 0 : -1}
          ref={(el) => (itemRefs.current[index] = el)}
          onKeyDown={(e) => handleKeyDown(e, index)}
          onClick={item.action}>
          {item.label}
        </li>
      ))}
    </ul>
  );
}
```

### ❌ Bad Examples

```html
<!-- Missing roles -->
<ul class="menu">
  <li>Item 1</li>
</ul>

<!-- Using Tab navigation instead of arrows -->
<ul role="menu">
  <li role="menuitem" tabindex="0">Item 1</li>
  <li role="menuitem" tabindex="0">Item 2</li>  <!-- All have tabindex="0"! -->
</ul>

<!-- Missing aria-haspopup on submenu parent -->
<li role="menuitem">
  File
  <ul role="menu">...</ul>
</li>
```

## WCAG References

- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does container have `role="menu"` or `role="menubar"`?** (CRITICAL)
- [ ] **Do all items have appropriate menuitem roles?** (CRITICAL)
- [ ] **Do arrow keys navigate between items?** (CRITICAL - NOT Tab key)
- [ ] **Does Tab key exit the menu?** (CRITICAL)
- [ ] **Do parent items have `aria-haspopup="true"`?** (CRITICAL for submenus)
- [ ] **Is focus managed with roving tabindex or aria-activedescendant?** (CRITICAL)
- [ ] **Does Escape close the menu?** (CRITICAL)
- [ ] **Does Enter activate menu items?** (CRITICAL)
- [ ] Do checkbox items have `aria-checked`?
- [ ] Do radio items have `aria-checked`?
- [ ] Are disabled items marked with `aria-disabled="true"`?
- [ ] Does menu have accessible label?
- [ ] Are separators marked with `role="separator"`?

## Quick Reference

```
✅ DO:
- Use role="menu" or role="menubar"
- Use role="menuitem", role="menuitemcheckbox", or role="menuitemradio"
- Navigate with arrow keys (NOT Tab)
- Exit menu with Tab or Escape
- Use roving tabindex (active: tabindex="0", others: tabindex="-1")
- Mark submenus with aria-haspopup and aria-expanded
- Place submenus as siblings after parent menuitem
- Close menu on Escape
- Activate items with Enter
- Mark disabled items with aria-disabled="true"

❌ DON'T:
- Forget role="menu" and role="menuitem"
- Use Tab to navigate within menu
- Give all menuitems tabindex="0"
- Forget aria-haspopup on submenu parents
- Nest submenus incorrectly
- Prevent Tab from exiting menu
- Forget to return focus when closing
```
