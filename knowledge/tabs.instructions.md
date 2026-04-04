---
description: Instructions for proper tabs accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Tabs Accessibility

## CRITICAL RULES

**Tabs organize content into layered sections, with only one panel visible at a time.**

### 1. Use role="tablist", role="tab", and role="tabpanel"

**Tabs require three roles: `tablist` (container), `tab` (tab buttons), and `tabpanel` (content areas).**

```html
✅ Good - Proper tab roles:
<div role="tablist" aria-label="Sample Tabs">
  <button role="tab" aria-selected="true" aria-controls="panel-1" id="tab-1">
    Tab 1
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" id="tab-2" tabindex="-1">
    Tab 2
  </button>
</div>

<div role="tabpanel" id="panel-1" aria-labelledby="tab-1">
  <p>Panel 1 content</p>
</div>
<div role="tabpanel" id="panel-2" aria-labelledby="tab-2" hidden>
  <p>Panel 2 content</p>
</div>

❌ Bad - Missing roles:
<div class="tabs">
  <button>Tab 1</button>  <!-- Missing role="tab"! -->
  <button>Tab 2</button>
</div>
<div class="panel">Content</div>  <!-- Missing role="tabpanel"! -->
```

### 2. Mark Active Tab with aria-selected="true"

**The active tab MUST have `aria-selected="true"`, inactive tabs `aria-selected="false"`.**

```html
✅ Good - Proper aria-selected usage:
<div role="tablist">
  <button role="tab" aria-selected="true" id="tab-1">Active</button>
  <button role="tab" aria-selected="false" id="tab-2">Inactive</button>
  <button role="tab" aria-selected="false" id="tab-3">Inactive</button>
</div>

❌ Bad - Missing aria-selected:
<div role="tablist">
  <button role="tab" id="tab-1">Active</button>  <!-- Missing aria-selected! -->
  <button role="tab" id="tab-2">Inactive</button>
</div>
```

### 3. Connect Tabs and Panels with aria-controls and aria-labelledby

**Each tab MUST reference its panel with `aria-controls`, and each panel MUST reference its tab with `aria-labelledby`.**

```html
✅ Good - Proper tab/panel connections:
<button
  role="tab"
  id="tab-profile"
  aria-controls="panel-profile"
  aria-selected="true">
  Profile
</button>

<div
  role="tabpanel"
  id="panel-profile"
  aria-labelledby="tab-profile">
  <h2>Profile Settings</h2>
  <p>Content...</p>
</div>

❌ Bad - Missing connections:
<button role="tab" id="tab-1" aria-selected="true">
  Tab 1
</button>
<div role="tabpanel" id="panel-1">  <!-- Missing aria-labelledby! -->
  Content
</div>
```

### 4. Implement Arrow Key Navigation

**Users MUST be able to navigate between tabs using arrow keys.**

**Required keyboard interactions:**
- **Tab**: Enters tab list, moves to active tab; exits to next focusable element
- **Arrow Left/Up**: Move to previous tab (wraps to last)
- **Arrow Right/Down**: Move to next tab (wraps to first)
- **Home**: Move to first tab (optional)
- **End**: Move to last tab (optional)
- **Space/Enter**: Activate focused tab (if not auto-activated)

```javascript
// ✅ Good - Arrow key navigation
tablist.addEventListener('keydown', (e) => {
  const tabs = Array.from(tablist.querySelectorAll('[role="tab"]'));
  const currentIndex = tabs.indexOf(document.activeElement);

  let newIndex;

  switch(e.key) {
    case 'ArrowLeft':
    case 'ArrowUp':
      e.preventDefault();
      newIndex = currentIndex - 1;
      if (newIndex < 0) newIndex = tabs.length - 1;  // Wrap to last
      tabs[newIndex].focus();
      activateTab(tabs[newIndex]);
      break;

    case 'ArrowRight':
    case 'ArrowDown':
      e.preventDefault();
      newIndex = currentIndex + 1;
      if (newIndex >= tabs.length) newIndex = 0;  // Wrap to first
      tabs[newIndex].focus();
      activateTab(tabs[newIndex]);
      break;

    case 'Home':
      e.preventDefault();
      tabs[0].focus();
      activateTab(tabs[0]);
      break;

    case 'End':
      e.preventDefault();
      tabs[tabs.length - 1].focus();
      activateTab(tabs[tabs.length - 1]);
      break;
  }
});
```

### 5. Manage Tab Focus with tabindex

**Only the active tab should be in the tab sequence (`tabindex="0"`). Inactive tabs should have `tabindex="-1"`.**

```html
✅ Good - Proper tabindex management:
<div role="tablist">
  <button role="tab" aria-selected="true" tabindex="0">Active Tab</button>
  <button role="tab" aria-selected="false" tabindex="-1">Inactive 1</button>
  <button role="tab" aria-selected="false" tabindex="-1">Inactive 2</button>
</div>

❌ Bad - All tabs in tab sequence:
<div role="tablist">
  <button role="tab" aria-selected="true" tabindex="0">Tab 1</button>
  <button role="tab" aria-selected="false" tabindex="0">Tab 2</button>
  <button role="tab" aria-selected="false" tabindex="0">Tab 3</button>
</div>
```

**Why this matters:**
- Prevents excessive Tab key presses to navigate through tabs
- Conforms to ARIA Authoring Practices roving tabindex pattern
- Arrow keys navigate between tabs, not Tab key

## Complete Tabs Structure

```html
<div role="tablist" aria-label="Account Settings">
  <button
    role="tab"
    id="tab-profile"
    aria-selected="true"
    aria-controls="panel-profile"
    tabindex="0">
    Profile
  </button>
  <button
    role="tab"
    id="tab-security"
    aria-selected="false"
    aria-controls="panel-security"
    tabindex="-1">
    Security
  </button>
  <button
    role="tab"
    id="tab-notifications"
    aria-selected="false"
    aria-controls="panel-notifications"
    tabindex="-1">
    Notifications
  </button>
</div>

<div role="tabpanel" id="panel-profile" aria-labelledby="tab-profile">
  <h2>Profile Settings</h2>
  <p>Update your profile information...</p>
</div>

<div role="tabpanel" id="panel-security" aria-labelledby="tab-security" hidden>
  <h2>Security Settings</h2>
  <p>Manage your security preferences...</p>
</div>

<div role="tabpanel" id="panel-notifications" aria-labelledby="tab-notifications" hidden>
  <h2>Notification Settings</h2>
  <p>Configure your notifications...</p>
</div>

<script>
const tablist = document.querySelector('[role="tablist"]');
const tabs = tablist.querySelectorAll('[role="tab"]');
const panels = document.querySelectorAll('[role="tabpanel"]');

// Arrow key navigation
tablist.addEventListener('keydown', (e) => {
  const tabArray = Array.from(tabs);
  const currentIndex = tabArray.indexOf(document.activeElement);

  let newIndex;

  switch(e.key) {
    case 'ArrowLeft':
    case 'ArrowUp':
      e.preventDefault();
      newIndex = currentIndex - 1;
      if (newIndex < 0) newIndex = tabArray.length - 1;
      activateTab(tabArray[newIndex]);
      break;

    case 'ArrowRight':
    case 'ArrowDown':
      e.preventDefault();
      newIndex = currentIndex + 1;
      if (newIndex >= tabArray.length) newIndex = 0;
      activateTab(tabArray[newIndex]);
      break;

    case 'Home':
      e.preventDefault();
      activateTab(tabArray[0]);
      break;

    case 'End':
      e.preventDefault();
      activateTab(tabArray[tabArray.length - 1]);
      break;
  }
});

// Click activation
tabs.forEach(tab => {
  tab.addEventListener('click', () => activateTab(tab));
});

function activateTab(newTab) {
  // Deactivate all tabs
  tabs.forEach(tab => {
    tab.setAttribute('aria-selected', 'false');
    tab.setAttribute('tabindex', '-1');
  });

  // Hide all panels
  panels.forEach(panel => {
    panel.setAttribute('hidden', '');
  });

  // Activate selected tab
  newTab.setAttribute('aria-selected', 'true');
  newTab.setAttribute('tabindex', '0');
  newTab.focus();

  // Show selected panel
  const panelId = newTab.getAttribute('aria-controls');
  const panel = document.getElementById(panelId);
  panel.removeAttribute('hidden');
}
</script>
```

## Examples

### ✅ Good: Basic Tabs

```html
<div role="tablist" aria-label="Product Information">
  <button role="tab" aria-selected="true" aria-controls="desc-panel" id="desc-tab" tabindex="0">
    Description
  </button>
  <button role="tab" aria-selected="false" aria-controls="specs-panel" id="specs-tab" tabindex="-1">
    Specifications
  </button>
  <button role="tab" aria-selected="false" aria-controls="reviews-panel" id="reviews-tab" tabindex="-1">
    Reviews
  </button>
</div>

<div role="tabpanel" id="desc-panel" aria-labelledby="desc-tab">
  <h2>Product Description</h2>
  <p>This product is...</p>
</div>

<div role="tabpanel" id="specs-panel" aria-labelledby="specs-tab" hidden>
  <h2>Technical Specifications</h2>
  <ul>
    <li>Weight: 2 lbs</li>
    <li>Dimensions: 10x8x2 inches</li>
  </ul>
</div>

<div role="tabpanel" id="reviews-panel" aria-labelledby="reviews-tab" hidden>
  <h2>Customer Reviews</h2>
  <p>4.5 out of 5 stars...</p>
</div>
```

### ✅ Good: Vertical Tabs

```html
<div role="tablist" aria-label="Settings" aria-orientation="vertical">
  <button role="tab" aria-selected="true" aria-controls="panel-1" tabindex="0">
    General
  </button>
  <button role="tab" aria-selected="false" aria-controls="panel-2" tabindex="-1">
    Privacy
  </button>
</div>

<!-- Panels... -->
```

**Note**: Use `aria-orientation="vertical"` for vertical tab layouts.

### ✅ Good: React Tabs Component

```jsx
function Tabs({ tabs }) {
  const [activeIndex, setActiveIndex] = React.useState(0);

  const handleKeyDown = (e, index) => {
    let newIndex = index;

    switch(e.key) {
      case 'ArrowLeft':
      case 'ArrowUp':
        e.preventDefault();
        newIndex = index === 0 ? tabs.length - 1 : index - 1;
        break;

      case 'ArrowRight':
      case 'ArrowDown':
        e.preventDefault();
        newIndex = index === tabs.length - 1 ? 0 : index + 1;
        break;

      case 'Home':
        e.preventDefault();
        newIndex = 0;
        break;

      case 'End':
        e.preventDefault();
        newIndex = tabs.length - 1;
        break;

      default:
        return;
    }

    setActiveIndex(newIndex);
  };

  return (
    <div>
      <div role="tablist" aria-label="Content Tabs">
        {tabs.map((tab, index) => (
          <button
            key={index}
            role="tab"
            id={`tab-${index}`}
            aria-selected={index === activeIndex}
            aria-controls={`panel-${index}`}
            tabIndex={index === activeIndex ? 0 : -1}
            onClick={() => setActiveIndex(index)}
            onKeyDown={(e) => handleKeyDown(e, index)}>
            {tab.label}
          </button>
        ))}
      </div>

      {tabs.map((tab, index) => (
        <div
          key={index}
          role="tabpanel"
          id={`panel-${index}`}
          aria-labelledby={`tab-${index}`}
          hidden={index !== activeIndex}>
          {tab.content}
        </div>
      ))}
    </div>
  );
}
```

### ❌ Bad Examples

```html
<!-- Missing roles -->
<div class="tabs">
  <button>Tab 1</button>
  <button>Tab 2</button>
</div>

<!-- Missing aria-selected -->
<div role="tablist">
  <button role="tab">Tab 1</button>
</div>

<!-- All tabs have tabindex="0" -->
<div role="tablist">
  <button role="tab" aria-selected="true" tabindex="0">Tab 1</button>
  <button role="tab" aria-selected="false" tabindex="0">Tab 2</button>
</div>

<!-- Missing connections -->
<button role="tab" id="tab-1">Tab 1</button>
<div role="tabpanel">Content</div>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does container have `role="tablist"`?** (CRITICAL)
- [ ] **Do all tabs have `role="tab"`?** (CRITICAL)
- [ ] **Do all panels have `role="tabpanel"`?** (CRITICAL)
- [ ] **Does active tab have `aria-selected="true"`?** (CRITICAL)
- [ ] **Do inactive tabs have `aria-selected="false"`?** (CRITICAL)
- [ ] **Does each tab have `aria-controls` referencing its panel?** (CRITICAL)
- [ ] **Does each panel have `aria-labelledby` referencing its tab?** (CRITICAL)
- [ ] **Does active tab have `tabindex="0"`, inactive tabs `tabindex="-1"`?** (CRITICAL)
- [ ] **Do arrow keys navigate between tabs?** (CRITICAL)
- [ ] Does tablist have `aria-label` or `aria-labelledby`?
- [ ] Do inactive panels have `hidden` attribute?
- [ ] Are Home/End keys supported?
- [ ] Is `aria-orientation="vertical"` set for vertical tabs?

## Quick Reference

```
✅ DO:
- Use role="tablist" on container
- Use role="tab" on tab buttons
- Use role="tabpanel" on content areas
- Set aria-selected="true" on active tab
- Set aria-selected="false" on inactive tabs
- Connect tabs and panels with aria-controls/aria-labelledby
- Use tabindex="0" for active tab, tabindex="-1" for inactive tabs
- Implement arrow key navigation
- Hide inactive panels with hidden attribute
- Wrap to first/last tab when navigating

❌ DON'T:
- Forget role="tablist", role="tab", or role="tabpanel"
- Omit aria-selected attribute
- Give all tabs tabindex="0"
- Forget aria-controls or aria-labelledby
- Use Tab key to navigate between tabs (use arrows)
- Leave multiple panels visible simultaneously
- Ignore keyboard navigation
```
