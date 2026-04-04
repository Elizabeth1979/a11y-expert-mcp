---
description: Instructions for proper grid (data table) accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Grid (Interactive Data Table) Accessibility

## CRITICAL RULES

**Grids are interactive tables that allow keyboard navigation between cells using arrow keys. Use for data that requires cell-by-cell navigation, NOT for static data tables.**

### 1. Use role="grid" with role="row" and role="gridcell"

**Grids MUST use proper ARIA roles for structure.**

```html
✅ Good - Proper grid structure:
<div role="grid" aria-label="Products">
  <div role="row">
    <div role="columnheader">Name</div>
    <div role="columnheader">Price</div>
    <div role="columnheader">Stock</div>
  </div>
  <div role="row">
    <div role="gridcell">Laptop</div>
    <div role="gridcell">$999</div>
    <div role="gridcell">15</div>
  </div>
</div>

❌ Bad - Missing roles:
<div class="grid">
  <div class="row">
    <div>Name</div>  <!-- Missing role! -->
  </div>
</div>
```

**Role hierarchy:**
- `role="grid"` - Container
- `role="row"` - Row container
- `role="columnheader"` - Column header cells
- `role="rowheader"` - Row header cells
- `role="gridcell"` - Data cells

### 2. Provide Accessible Label

**Every grid MUST have an accessible label.**

```html
✅ Good - Using aria-label:
<div role="grid" aria-label="Employee directory">
  <!-- rows and cells -->
</div>

✅ Good - Using aria-labelledby:
<h2 id="products-title">Products</h2>
<div role="grid" aria-labelledby="products-title">
  <!-- rows and cells -->
</div>
```

### 3. Implement Arrow Key Navigation

**Grids MUST support arrow key navigation between cells.**

**Required keyboard interactions:**
- **Right Arrow**: Move to next cell in row
- **Left Arrow**: Move to previous cell in row
- **Down Arrow**: Move to cell below
- **Up Arrow**: Move to cell above
- **Home**: Move to first cell in row
- **End**: Move to last cell in row
- **Ctrl+Home**: Move to first cell in grid
- **Ctrl+End**: Move to last cell in grid
- **Page Down**: Move down by author-determined rows
- **Page Up**: Move up by author-determined rows

```javascript
grid.addEventListener('keydown', (e) => {
  const currentCell = document.activeElement;
  const cells = Array.from(grid.querySelectorAll('[role="gridcell"]'));
  const currentIndex = cells.indexOf(currentCell);

  // Calculate grid dimensions
  const colCount = grid.querySelector('[role="row"]')
    .querySelectorAll('[role="gridcell"], [role="columnheader"]').length;

  switch(e.key) {
    case 'ArrowRight':
      e.preventDefault();
      if (currentIndex < cells.length - 1) {
        cells[currentIndex + 1].focus();
      }
      break;

    case 'ArrowLeft':
      e.preventDefault();
      if (currentIndex > 0) {
        cells[currentIndex - 1].focus();
      }
      break;

    case 'ArrowDown':
      e.preventDefault();
      const nextRowIndex = currentIndex + colCount;
      if (nextRowIndex < cells.length) {
        cells[nextRowIndex].focus();
      }
      break;

    case 'ArrowUp':
      e.preventDefault();
      const prevRowIndex = currentIndex - colCount;
      if (prevRowIndex >= 0) {
        cells[prevRowIndex].focus();
      }
      break;

    case 'Home':
      e.preventDefault();
      if (e.ctrlKey) {
        cells[0].focus();
      } else {
        const rowStart = currentIndex - (currentIndex % colCount);
        cells[rowStart].focus();
      }
      break;

    case 'End':
      e.preventDefault();
      if (e.ctrlKey) {
        cells[cells.length - 1].focus();
      } else {
        const rowStart = currentIndex - (currentIndex % colCount);
        const rowEnd = Math.min(rowStart + colCount - 1, cells.length - 1);
        cells[rowEnd].focus();
      }
      break;
  }
});
```

### 4. Make Cells Focusable

**All data cells MUST be focusable with `tabindex`.**

```html
✅ Good - Cells are focusable:
<div role="grid" aria-label="Data">
  <div role="row">
    <div role="gridcell" tabindex="0">Cell 1</div>
    <div role="gridcell" tabindex="-1">Cell 2</div>
    <div role="gridcell" tabindex="-1">Cell 3</div>
  </div>
</div>

❌ Bad - Cells not focusable:
<div role="grid">
  <div role="row">
    <div role="gridcell">Cell 1</div>  <!-- Missing tabindex! -->
  </div>
</div>
```

**Focus management:**
- First cell (or selected cell) has `tabindex="0"`
- All other cells have `tabindex="-1"`
- Only one cell in tab sequence at a time

### 5. Grid vs Table: When to Use Grid

**Use `role="grid"` ONLY when you need:**
- Arrow key navigation between cells
- Editable cells
- Interactive cell content (buttons, inputs)
- Cell selection

**Use `<table>` (or role="table") when:**
- Data is static and read-only
- Users don't need cell-by-cell navigation
- See [tables.instructions.md](tables.instructions.md)

```html
✅ Good - Static data, use table:
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>John</td>
      <td>john@example.com</td>
    </tr>
  </tbody>
</table>

✅ Good - Interactive data, use grid:
<div role="grid" aria-label="Editable contacts">
  <div role="row">
    <div role="columnheader">Name</div>
    <div role="columnheader">Email</div>
    <div role="columnheader">Actions</div>
  </div>
  <div role="row">
    <div role="gridcell" tabindex="0">
      <input type="text" value="John">
    </div>
    <div role="gridcell" tabindex="-1">
      <input type="email" value="john@example.com">
    </div>
    <div role="gridcell" tabindex="-1">
      <button>Edit</button>
      <button>Delete</button>
    </div>
  </div>
</div>
```

## Complete Grid Structure

```html
<h2 id="employees-title">Employees</h2>

<div
  role="grid"
  aria-labelledby="employees-title"
  id="employees-grid">

  <!-- Header row -->
  <div role="row">
    <div role="columnheader">Name</div>
    <div role="columnheader">Department</div>
    <div role="columnheader">Email</div>
  </div>

  <!-- Data rows -->
  <div role="row">
    <div role="gridcell" tabindex="0">Alice Smith</div>
    <div role="gridcell" tabindex="-1">Engineering</div>
    <div role="gridcell" tabindex="-1">alice@example.com</div>
  </div>

  <div role="row">
    <div role="gridcell" tabindex="-1">Bob Johnson</div>
    <div role="gridcell" tabindex="-1">Marketing</div>
    <div role="gridcell" tabindex="-1">bob@example.com</div>
  </div>

  <div role="row">
    <div role="gridcell" tabindex="-1">Carol Williams</div>
    <div role="gridcell" tabindex="-1">Sales</div>
    <div role="gridcell" tabindex="-1">carol@example.com</div>
  </div>
</div>

<script>
const grid = document.getElementById('employees-grid');
const cells = grid.querySelectorAll('[role="gridcell"]');

// Arrow key navigation
grid.addEventListener('keydown', handleGridNavigation);

function handleGridNavigation(e) {
  if (!['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(e.key)) {
    return;
  }

  e.preventDefault();

  const currentCell = document.activeElement;
  const cellsArray = Array.from(cells);
  const currentIndex = cellsArray.indexOf(currentCell);

  const rows = grid.querySelectorAll('[role="row"]');
  const colCount = rows[0].querySelectorAll('[role="gridcell"], [role="columnheader"]').length;

  let newIndex = currentIndex;

  switch(e.key) {
    case 'ArrowRight':
      newIndex = Math.min(currentIndex + 1, cellsArray.length - 1);
      break;
    case 'ArrowLeft':
      newIndex = Math.max(currentIndex - 1, 0);
      break;
    case 'ArrowDown':
      newIndex = Math.min(currentIndex + colCount, cellsArray.length - 1);
      break;
    case 'ArrowUp':
      newIndex = Math.max(currentIndex - colCount, 0);
      break;
    case 'Home':
      if (e.ctrlKey) {
        newIndex = 0;
      } else {
        newIndex = currentIndex - (currentIndex % colCount);
      }
      break;
    case 'End':
      if (e.ctrlKey) {
        newIndex = cellsArray.length - 1;
      } else {
        const rowStart = currentIndex - (currentIndex % colCount);
        newIndex = Math.min(rowStart + colCount - 1, cellsArray.length - 1);
      }
      break;
  }

  if (newIndex !== currentIndex) {
    moveFocus(currentIndex, newIndex);
  }
}

function moveFocus(oldIndex, newIndex) {
  cells[oldIndex].setAttribute('tabindex', '-1');
  cells[newIndex].setAttribute('tabindex', '0');
  cells[newIndex].focus();
}
</script>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does container have `role="grid"`?** (CRITICAL)
- [ ] **Do rows have `role="row"`?** (CRITICAL)
- [ ] **Do cells have appropriate roles (gridcell/columnheader/rowheader)?** (CRITICAL)
- [ ] **Does grid have accessible label?** (CRITICAL)
- [ ] **Are all cells focusable (tabindex)?** (CRITICAL)
- [ ] **Do arrow keys navigate between cells?** (CRITICAL)
- [ ] Do Home/End keys work?
- [ ] Do Ctrl+Home/Ctrl+End work?
- [ ] Is grid used appropriately (not for static data)?
- [ ] Is only one cell in tab sequence (roving tabindex)?

## Quick Reference

```
✅ DO:
- Use role="grid" for interactive tables
- Use role="row" for rows
- Use role="gridcell" for data cells
- Use role="columnheader" for column headers
- Provide accessible label
- Make all cells focusable with tabindex
- Support arrow key navigation
- Use roving tabindex (one cell: tabindex="0", others: tabindex="-1")
- Support Home/End and Ctrl+Home/Ctrl+End

❌ DON'T:
- Use grid for static, read-only tables (use <table> instead)
- Forget to make cells focusable
- Skip arrow key navigation
- Give all cells tabindex="0"
- Use grid when table would suffice

## Grid vs Table:

Grid (role="grid"):
  - Interactive, editable data
  - Arrow key cell navigation needed
  - Contains interactive widgets
  - User selects individual cells
  - Example: Spreadsheet, data editor

Table (<table> or role="table"):
  - Static, read-only data
  - Screen reader table navigation sufficient
  - No interactive cell content
  - User reads data linearly
  - Example: Reports, lists, static data
  - See tables.instructions.md
```
