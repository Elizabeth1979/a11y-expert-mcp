---
description: Instructions for proper tree view accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Tree View Accessibility

## CRITICAL RULES

**Tree views present hierarchical lists with expandable/collapsible nodes. Common uses: file browsers, navigation menus, org charts.**

### 1. Use role="tree" with role="treeitem"

**Trees MUST have `role="tree"` and items MUST have `role="treeitem"`.**

```html
✅ Good - Proper tree structure:
<ul role="tree" aria-label="File Navigator">
  <li role="treeitem" aria-expanded="true">
    Documents
    <ul role="group">
      <li role="treeitem">report.pdf</li>
      <li role="treeitem">notes.txt</li>
    </ul>
  </li>
</ul>

❌ Bad - Missing roles:
<ul>  <!-- Missing role="tree"! -->
  <li>Documents</li>  <!-- Missing role="treeitem"! -->
</ul>
```

### 2. Mark Expandable Nodes with aria-expanded

**Parent nodes MUST have `aria-expanded="true|false"`. Leaf nodes MUST NOT have `aria-expanded`.**

```html
✅ Good - Using aria-expanded:
<!-- Parent node (expanded) -->
<li role="treeitem" aria-expanded="true">
  Folder
  <ul role="group">
    <li role="treeitem">File</li>
  </ul>
</li>

<!-- Parent node (collapsed) -->
<li role="treeitem" aria-expanded="false">
  Folder
  <ul role="group" hidden>
    <li role="treeitem">File</li>
  </ul>
</li>

<!-- Leaf node (no aria-expanded) -->
<li role="treeitem">File</li>

❌ Bad - aria-expanded on leaf node:
<li role="treeitem" aria-expanded="false">
  File  <!-- No children, should not have aria-expanded! -->
</li>
```

### 3. Implement Arrow Key Navigation

**Required keyboard interactions:**

**Navigation:**
- **Down Arrow**: Next tree item
- **Up Arrow**: Previous tree item
- **Right Arrow**: Expand collapsed node; move to first child if expanded
- **Left Arrow**: Collapse expanded node; move to parent if collapsed
- **Home**: First tree item
- **End**: Last visible tree item
- **Enter**: Activate/select item

**Expansion:**
- **Asterisk (*)**: Expand all siblings at current level

**Type-ahead:**
- **Character keys**: Move to next item starting with typed character

```javascript
tree.addEventListener('keydown', (e) => {
  const currentItem = document.activeElement;

  switch(e.key) {
    case 'ArrowDown':
      e.preventDefault();
      focusNextItem(currentItem);
      break;

    case 'ArrowUp':
      e.preventDefault();
      focusPreviousItem(currentItem);
      break;

    case 'ArrowRight':
      e.preventDefault();
      const isExpanded = currentItem.getAttribute('aria-expanded');
      if (isExpanded === 'false') {
        expandNode(currentItem);
      } else if (isExpanded === 'true') {
        focusFirstChild(currentItem);
      }
      break;

    case 'ArrowLeft':
      e.preventDefault();
      const expanded = currentItem.getAttribute('aria-expanded');
      if (expanded === 'true') {
        collapseNode(currentItem);
      } else {
        focusParent(currentItem);
      }
      break;

    case 'Home':
      e.preventDefault();
      focusFirstItem();
      break;

    case 'End':
      e.preventDefault();
      focusLastVisibleItem();
      break;

    case 'Enter':
      e.preventDefault();
      selectItem(currentItem);
      break;

    case '*':
      e.preventDefault();
      expandAllSiblings(currentItem);
      break;
  }
});
```

### 4. Use role="group" for Child Containers

**Child nodes MUST be contained in elements with `role="group"`.**

```html
✅ Good - Using role="group":
<ul role="tree">
  <li role="treeitem" aria-expanded="true">
    Parent
    <ul role="group">  <!-- role="group" for children -->
      <li role="treeitem">Child 1</li>
      <li role="treeitem">Child 2</li>
    </ul>
  </li>
</ul>

❌ Bad - Missing role="group":
<ul role="tree">
  <li role="treeitem" aria-expanded="true">
    Parent
    <ul>  <!-- Missing role="group"! -->
      <li role="treeitem">Child</li>
    </ul>
  </li>
</ul>
```

### 5. Manage Focus with Roving tabindex

**Only the focused/selected item should have `tabindex="0"`, all others `tabindex="-1"`.**

```html
✅ Good - Roving tabindex:
<ul role="tree" aria-label="Folders">
  <li role="treeitem" tabindex="0" aria-selected="true">Selected</li>
  <li role="treeitem" tabindex="-1">Item 2</li>
  <li role="treeitem" tabindex="-1">Item 3</li>
</ul>

❌ Bad - All items have tabindex="0":
<ul role="tree">
  <li role="treeitem" tabindex="0">Item 1</li>
  <li role="treeitem" tabindex="0">Item 2</li>  <!-- Wrong! -->
</ul>
```

## Complete Tree View Structure

```html
<h2 id="nav-label">Navigation</h2>

<ul
  role="tree"
  aria-labelledby="nav-label"
  id="main-tree">

  <li role="treeitem" aria-expanded="true" tabindex="0">
    Products
    <ul role="group">
      <li role="treeitem" tabindex="-1">Laptops</li>
      <li role="treeitem" aria-expanded="false" tabindex="-1">
        Accessories
        <ul role="group" hidden>
          <li role="treeitem" tabindex="-1">Mouse</li>
          <li role="treeitem" tabindex="-1">Keyboard</li>
        </ul>
      </li>
    </ul>
  </li>

  <li role="treeitem" tabindex="-1">
    About
  </li>

  <li role="treeitem" tabindex="-1">
    Contact
  </li>
</ul>

<script>
const tree = document.getElementById('main-tree');
const items = tree.querySelectorAll('[role="treeitem"]');

tree.addEventListener('keydown', (e) => {
  const current = document.activeElement;

  switch(e.key) {
    case 'ArrowDown':
      e.preventDefault();
      focusNext(current);
      break;

    case 'ArrowUp':
      e.preventDefault();
      focusPrevious(current);
      break;

    case 'ArrowRight':
      e.preventDefault();
      if (current.getAttribute('aria-expanded') === 'false') {
        expand(current);
      } else if (current.getAttribute('aria-expanded') === 'true') {
        const firstChild = current.querySelector('[role="group"] > [role="treeitem"]');
        if (firstChild) focus(firstChild);
      }
      break;

    case 'ArrowLeft':
      e.preventDefault();
      if (current.getAttribute('aria-expanded') === 'true') {
        collapse(current);
      } else {
        const parent = current.closest('[role="group"]').closest('[role="treeitem"]');
        if (parent) focus(parent);
      }
      break;

    case 'Home':
      e.preventDefault();
      focus(items[0]);
      break;

    case 'End':
      e.preventDefault();
      const visible = getVisibleItems();
      focus(visible[visible.length - 1]);
      break;

    case 'Enter':
      e.preventDefault();
      selectItem(current);
      break;
  }
});

function expand(item) {
  item.setAttribute('aria-expanded', 'true');
  const group = item.querySelector('[role="group"]');
  if (group) group.removeAttribute('hidden');
}

function collapse(item) {
  item.setAttribute('aria-expanded', 'false');
  const group = item.querySelector('[role="group"]');
  if (group) group.setAttribute('hidden', '');
}

function focus(item) {
  items.forEach(i => i.setAttribute('tabindex', '-1'));
  item.setAttribute('tabindex', '0');
  item.focus();
}

function getVisibleItems() {
  return Array.from(items).filter(item => {
    return !item.closest('[hidden]');
  });
}

function focusNext(current) {
  const visible = getVisibleItems();
  const index = visible.indexOf(current);
  if (index < visible.length - 1) {
    focus(visible[index + 1]);
  }
}

function focusPrevious(current) {
  const visible = getVisibleItems();
  const index = visible.indexOf(current);
  if (index > 0) {
    focus(visible[index - 1]);
  }
}

function selectItem(item) {
  items.forEach(i => i.removeAttribute('aria-selected'));
  item.setAttribute('aria-selected', 'true');
}
</script>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does container have `role="tree"`?** (CRITICAL)
- [ ] **Do all items have `role="treeitem"`?** (CRITICAL)
- [ ] **Do parent nodes have `aria-expanded`?** (CRITICAL)
- [ ] **Do leaf nodes NOT have `aria-expanded`?** (CRITICAL)
- [ ] **Do child containers have `role="group"`?** (CRITICAL)
- [ ] **Does tree have accessible label?** (CRITICAL)
- [ ] **Is focus managed with roving tabindex?** (CRITICAL)
- [ ] **Do arrow keys navigate properly?** (CRITICAL)
- [ ] Do Right/Left arrows expand/collapse?
- [ ] Do Home/End keys work?
- [ ] Is Enter key supported?

## Quick Reference

```
✅ DO:
- Use role="tree"
- Use role="treeitem" for all items
- Use role="group" for child containers
- Use aria-expanded="true|false" on parent nodes only
- Omit aria-expanded from leaf nodes
- Provide accessible label
- Use roving tabindex
- Support full arrow key navigation
- Support Home/End keys
- Support Enter to select

❌ DON'T:
- Add aria-expanded to leaf nodes
- Forget role="group" for children
- Give all items tabindex="0"
- Skip arrow key navigation
- Forget accessible label
```
