---
description: Instructions for proper treegrid (hierarchical grid) accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Treegrid (Hierarchical Grid) Accessibility

## CRITICAL RULES

**Treegrids combine grid and tree patterns - hierarchical data with expandable/collapsible rows and arrow key navigation.**

### 1. Use role="treegrid" with Proper Row/Cell Roles

**Treegrids MUST use `role="treegrid"` with rows and cells.**

```html
✅ Good - Treegrid structure:
<div role="treegrid" aria-label="File system">
  <div role="row" aria-expanded="true" aria-level="1">
    <div role="gridcell">📁 Documents</div>
    <div role="gridcell">10 items</div>
  </div>
  <div role="row" aria-expanded="false" aria-level="2">
    <div role="gridcell">📁 Work</div>
    <div role="gridcell">5 items</div>
  </div>
  <div role="row" aria-level="3">
    <div role="gridcell">📄 report.pdf</div>
    <div role="gridcell">2MB</div>
  </div>
</div>
```

### 2. Mark Expandable Rows with aria-expanded

**Parent rows MUST have `aria-expanded="true|false"`.**

```html
✅ Good - Using aria-expanded:
<!-- Expanded parent row -->
<div role="row" aria-expanded="true" aria-level="1">
  <div role="gridcell">Folder</div>
</div>

<!-- Collapsed parent row -->
<div role="row" aria-expanded="false" aria-level="1">
  <div role="gridcell">Folder</div>
</div>

<!-- Leaf node (no children) -->
<div role="row" aria-level="2">
  <div role="gridcell">File</div>
</div>
```

### 3. Implement Full Keyboard Navigation

**Required keyboard interactions:**

**Navigation:**
- **Arrow keys**: Navigate between rows and cells
- **Enter**: Expand/collapse parent row or activate cell
- **Home/End**: First/last row or cell in row
- **Ctrl+Home/End**: Grid corners

**Expansion:**
- **Right Arrow**: Expand collapsed row; move to first child if expanded
- **Left Arrow**: Collapse expanded row; move to parent if collapsed

```javascript
treegrid.addEventListener('keydown', (e) => {
  const currentRow = document.activeElement.closest('[role="row"]');

  if (e.key === 'Enter') {
    const isExpanded = currentRow.getAttribute('aria-expanded');
    if (isExpanded !== null) {
      toggleRow(currentRow);
    }
  } else if (e.key === 'ArrowRight') {
    const isExpanded = currentRow.getAttribute('aria-expanded');
    if (isExpanded === 'false') {
      expandRow(currentRow);
    } else if (isExpanded === 'true') {
      focusFirstChild(currentRow);
    }
  } else if (e.key === 'ArrowLeft') {
    const isExpanded = currentRow.getAttribute('aria-expanded');
    if (isExpanded === 'true') {
      collapseRow(currentRow);
    } else {
      focusParentRow(currentRow);
    }
  }
});
```

### 4. Provide Accessible Label

**Every treegrid MUST have an accessible label.**

```html
✅ Good - Using aria-label:
<div role="treegrid" aria-label="File browser">
  <!-- rows -->
</div>

✅ Good - Using aria-labelledby:
<h2 id="files-title">Files</h2>
<div role="treegrid" aria-labelledby="files-title">
  <!-- rows -->
</div>
```

### 5. Make Rows and Cells Focusable

**All rows and cells MUST be focusable.**

```html
✅ Good - Focusable cells:
<div role="row" aria-level="1">
  <div role="gridcell" tabindex="0">Name</div>
  <div role="gridcell" tabindex="-1">Size</div>
</div>
```

## Complete Treegrid Structure

```html
<h2 id="files-title">File System</h2>

<div
  role="treegrid"
  aria-labelledby="files-title"
  id="file-treegrid">

  <!-- Level 1: Root folder (expanded) -->
  <div role="row" aria-expanded="true" aria-level="1" data-row-id="1">
    <div role="gridcell" tabindex="0">📁 Documents</div>
    <div role="gridcell" tabindex="-1">15 items</div>
    <div role="gridcell" tabindex="-1">Modified: 2024-01-15</div>
  </div>

  <!-- Level 2: Subfolder (collapsed) -->
  <div role="row" aria-expanded="false" aria-level="2" data-row-id="2" data-parent-id="1">
    <div role="gridcell" tabindex="-1">📁 Work</div>
    <div role="gridcell" tabindex="-1">8 items</div>
    <div role="gridcell" tabindex="-1">Modified: 2024-01-10</div>
  </div>

  <!-- Level 3: File (hidden, child of row 2) -->
  <div role="row" aria-level="3" data-row-id="3" data-parent-id="2" hidden>
    <div role="gridcell" tabindex="-1">📄 report.pdf</div>
    <div role="gridcell" tabindex="-1">2.5 MB</div>
    <div role="gridcell" tabindex="-1">Modified: 2024-01-09</div>
  </div>

  <!-- Level 2: File -->
  <div role="row" aria-level="2" data-row-id="4" data-parent-id="1">
    <div role="gridcell" tabindex="-1">📄 notes.txt</div>
    <div role="gridcell" tabindex="-1">5 KB</div>
    <div role="gridcell" tabindex="-1">Modified: 2024-01-12</div>
  </div>
</div>

<script>
const treegrid = document.getElementById('file-treegrid');

treegrid.addEventListener('keydown', (e) => {
  const currentCell = document.activeElement;
  const currentRow = currentCell.closest('[role="row"]');

  switch(e.key) {
    case 'Enter':
      e.preventDefault();
      toggleRow(currentRow);
      break;

    case 'ArrowRight':
      e.preventDefault();
      const isCollapsed = currentRow.getAttribute('aria-expanded') === 'false';
      if (isCollapsed) {
        expandRow(currentRow);
      }
      break;

    case 'ArrowLeft':
      e.preventDefault();
      const isExpanded = currentRow.getAttribute('aria-expanded') === 'true';
      if (isExpanded) {
        collapseRow(currentRow);
      }
      break;

    // Add arrow navigation between cells/rows
  }
});

function toggleRow(row) {
  const isExpanded = row.getAttribute('aria-expanded');
  if (isExpanded === 'true') {
    collapseRow(row);
  } else if (isExpanded === 'false') {
    expandRow(row);
  }
}

function expandRow(row) {
  row.setAttribute('aria-expanded', 'true');

  const rowId = row.getAttribute('data-row-id');
  const children = treegrid.querySelectorAll(`[data-parent-id="${rowId}"]`);

  children.forEach(child => {
    child.removeAttribute('hidden');
  });
}

function collapseRow(row) {
  row.setAttribute('aria-expanded', 'false');

  const rowId = row.getAttribute('data-row-id');
  const children = treegrid.querySelectorAll(`[data-parent-id="${rowId}"]`);

  children.forEach(child => {
    child.setAttribute('hidden', '');

    // Recursively collapse nested children
    if (child.getAttribute('aria-expanded') === 'true') {
      collapseRow(child);
    }
  });
}
</script>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does container have `role="treegrid"`?** (CRITICAL)
- [ ] **Do rows have `role="row"`?** (CRITICAL)
- [ ] **Do parent rows have `aria-expanded`?** (CRITICAL)
- [ ] **Do cells have `role="gridcell"`?** (CRITICAL)
- [ ] **Does treegrid have accessible label?** (CRITICAL)
- [ ] **Are rows/cells focusable?** (CRITICAL)
- [ ] **Does Enter toggle expansion?** (CRITICAL)
- [ ] Do arrow keys navigate properly?
- [ ] Does Right Arrow expand collapsed rows?
- [ ] Does Left Arrow collapse expanded rows?

## Quick Reference

```
✅ DO:
- Use role="treegrid"
- Use aria-expanded="true|false" on parent rows
- Make all rows and cells focusable
- Support Enter to expand/collapse
- Support arrow key navigation
- Provide accessible label
- Use aria-level to indicate hierarchy

❌ DON'T:
- Forget aria-expanded on parent rows
- Skip keyboard navigation
- Make rows/cells non-focusable
- Confuse with regular grid (use treegrid for hierarchical data)
```
