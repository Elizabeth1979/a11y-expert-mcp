---
description: Instructions for proper table accessibility and semantic table usage
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Table Accessibility

## CRITICAL RULES

**Tables should ONLY be used for tabular data, NOT for layout purposes.**

### 1. Tables Are for Tabular Data ONLY

**The `<table>` element is for displaying data in rows and columns, NOT for page layout.**

```html
✅ Good - Tabular data (products in a cart):
<table>
  <thead>
    <tr>
      <th>Product</th>
      <th>Price</th>
      <th>Quantity</th>
      <th>Total</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Wireless Mouse</td>
      <td>$25.00</td>
      <td>2</td>
      <td>$50.00</td>
    </tr>
  </tbody>
</table>

❌ Bad - Using table for layout:
<table>
  <tr>
    <td>
      <nav>Navigation menu...</nav>
    </td>
    <td>
      <main>Main content...</main>
    </td>
    <td>
      <aside>Sidebar...</aside>
    </td>
  </tr>
</table>
```

**Use tables for:**
- Data tables (products, prices, statistics)
- Comparison charts
- Schedules and calendars
- Financial data
- Any data with row/column relationships

**Do NOT use tables for:**
- Page layout
- Navigation menus
- Form layouts
- Positioning elements
- Creating columns

**Use CSS Grid or Flexbox for layouts instead.**

### 2. Use `<th>` for Column Headers

**Column headers MUST use `<th>` (table header) elements, NOT `<td>` (table data) elements.**

The `<th>` element:
- Identifies header cells
- Helps screen readers understand table structure
- Associates headers with data cells
- Should include `scope` attribute

```html
✅ Good - Using <th> for headers:
<table>
  <thead>
    <tr>
      <th scope="col">Product Name</th>
      <th scope="col">Price</th>
      <th scope="col">Stock</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Laptop</td>
      <td>$999</td>
      <td>15</td>
    </tr>
  </tbody>
</table>

❌ Bad - Using <td> for headers:
<table>
  <tr>
    <td><strong>Product Name</strong></td>  <!-- Should be <th>! -->
    <td><strong>Price</strong></td>
    <td><strong>Stock</strong></td>
  </tr>
  <tr>
    <td>Laptop</td>
    <td>$999</td>
    <td>15</td>
  </tr>
</table>
```

**Key points:**
- Use `<th scope="col">` for column headers
- Use `<th scope="row">` for row headers
- Group headers in `<thead>` when possible
- `<th>` elements are automatically bold and centered (can be styled with CSS)

### 3. Include Table Description When Relevant

**Provide context for tables using `<caption>` or `aria-label` whenever possible.**

The `<caption>` element:
- Must be the first child of `<table>`
- Provides a title/description for the table
- Helps users understand the table's purpose
- Is visible to all users (can be hidden with CSS if needed)

```html
✅ Good - Table with caption:
<table>
  <caption>Shopping Cart Items - 3 products</caption>
  <thead>
    <tr>
      <th scope="col">Product</th>
      <th scope="col">Price</th>
      <th scope="col">Quantity</th>
    </tr>
  </thead>
  <tbody>
    <!-- table data -->
  </tbody>
</table>

✅ Good - Table with aria-label:
<table aria-label="Monthly sales report for Q4 2024">
  <thead>
    <tr>
      <th scope="col">Month</th>
      <th scope="col">Sales</th>
      <th scope="col">Growth</th>
    </tr>
  </thead>
  <tbody>
    <!-- table data -->
  </tbody>
</table>

❌ Bad - No description:
<table>
  <thead>
    <tr>
      <th scope="col">Product</th>
      <th scope="col">Price</th>
    </tr>
  </thead>
  <tbody>
    <!-- What is this table showing? -->
  </tbody>
</table>
```

**When to use:**
- `<caption>` - When you want a visible table title
- `aria-label` - When you want a hidden description for screen readers
- `aria-describedby` - When you have a longer description elsewhere on the page

### 4. Avoid Split Cells (Colspan/Rowspan) When Possible

**Complex tables with merged cells are harder for screen readers to navigate. Avoid splitting cells across columns when possible.**

```html
✅ Good - Simple table without merged cells:
<table>
  <caption>Product Comparison</caption>
  <thead>
    <tr>
      <th scope="col">Feature</th>
      <th scope="col">Basic Plan</th>
      <th scope="col">Pro Plan</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Storage</th>
      <td>10 GB</td>
      <td>100 GB</td>
    </tr>
    <tr>
      <th scope="row">Users</th>
      <td>1</td>
      <td>Unlimited</td>
    </tr>
  </tbody>
</table>

⚠️ Use sparingly - Merged cells (complex):
<table>
  <caption>Weekly Schedule</caption>
  <thead>
    <tr>
      <th scope="col">Time</th>
      <th scope="col" colspan="2">Monday</th>  <!-- Merged cells -->
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">9:00 AM</th>
      <td>Meeting</td>
      <td>Room A</td>
    </tr>
  </tbody>
</table>

❌ Avoid - Overly complex merged cells:
<table>
  <tr>
    <th rowspan="2" colspan="2">Complex</th>  <!-- Too complex! -->
    <td>Data</td>
  </tr>
  <!-- Screen readers will struggle with this -->
</table>
```

**If you must use colspan/rowspan:**
- Keep it simple (avoid rowspan when possible)
- Ensure each cell has proper headers
- Test with a screen reader
- Consider if there's a simpler way to present the data

## Complete Table Structure

**A well-structured accessible table includes:**

```html
<table>
  <caption>Table description goes here</caption>

  <thead>
    <tr>
      <th scope="col">Header 1</th>
      <th scope="col">Header 2</th>
      <th scope="col">Header 3</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Data 1</td>
      <td>Data 2</td>
      <td>Data 3</td>
    </tr>
    <tr>
      <td>Data 4</td>
      <td>Data 5</td>
      <td>Data 6</td>
    </tr>
  </tbody>

  <tfoot> <!-- Optional -->
    <tr>
      <th scope="row">Total</th>
      <td>Sum 1</td>
      <td>Sum 2</td>
    </tr>
  </tfoot>
</table>
```

## Examples

### ✅ Good: Shopping Cart Table

```html
<table>
  <caption>Shopping Cart - 3 items</caption>
  <thead>
    <tr>
      <th scope="col">Product</th>
      <th scope="col">Price</th>
      <th scope="col">Quantity</th>
      <th scope="col">Subtotal</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Wireless Mouse</td>
      <td>$25.00</td>
      <td>2</td>
      <td>$50.00</td>
    </tr>
    <tr>
      <td>USB Cable</td>
      <td>$10.00</td>
      <td>1</td>
      <td>$10.00</td>
    </tr>
    <tr>
      <td>Keyboard</td>
      <td>$75.00</td>
      <td>1</td>
      <td>$75.00</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <th scope="row" colspan="3">Total</th>
      <td>$135.00</td>
    </tr>
  </tfoot>
</table>
```

### ✅ Good: Data Table with Row Headers

```html
<table aria-label="Monthly website statistics">
  <thead>
    <tr>
      <th scope="col">Month</th>
      <th scope="col">Visitors</th>
      <th scope="col">Page Views</th>
      <th scope="col">Bounce Rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">January</th>
      <td>12,450</td>
      <td>45,230</td>
      <td>42%</td>
    </tr>
    <tr>
      <th scope="row">February</th>
      <td>15,890</td>
      <td>52,100</td>
      <td>38%</td>
    </tr>
    <tr>
      <th scope="row">March</th>
      <td>18,200</td>
      <td>61,450</td>
      <td>35%</td>
    </tr>
  </tbody>
</table>
```

### ✅ Good: Comparison Table

```html
<table>
  <caption>Pricing Plans Comparison</caption>
  <thead>
    <tr>
      <th scope="col">Feature</th>
      <th scope="col">Basic</th>
      <th scope="col">Pro</th>
      <th scope="col">Enterprise</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th scope="row">Storage</th>
      <td>10 GB</td>
      <td>100 GB</td>
      <td>Unlimited</td>
    </tr>
    <tr>
      <th scope="row">Users</th>
      <td>1</td>
      <td>10</td>
      <td>Unlimited</td>
    </tr>
    <tr>
      <th scope="row">Support</th>
      <td>Email</td>
      <td>Email + Chat</td>
      <td>24/7 Phone</td>
    </tr>
  </tbody>
</table>
```

### ✅ Good: React/JSX Table Component

```jsx
function ProductTable({ products }) {
  return (
    <table>
      <caption>Available Products - {products.length} items</caption>
      <thead>
        <tr>
          <th scope="col">Name</th>
          <th scope="col">Price</th>
          <th scope="col">Stock</th>
        </tr>
      </thead>
      <tbody>
        {products.map((product) => (
          <tr key={product.id}>
            <td>{product.name}</td>
            <td>${product.price}</td>
            <td>{product.stock}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
```

### ❌ Bad: Using Table for Layout

```html
<!-- NEVER DO THIS - Use CSS Grid/Flexbox instead -->
<table>
  <tr>
    <td width="200">
      <nav>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
        </ul>
      </nav>
    </td>
    <td>
      <main>
        <h1>Page Content</h1>
        <p>Main content here...</p>
      </main>
    </td>
    <td width="300">
      <aside>
        <h2>Sidebar</h2>
        <p>Sidebar content...</p>
      </aside>
    </td>
  </tr>
</table>

<!-- Do this instead with CSS Grid: -->
<div class="layout">
  <nav class="sidebar">...</nav>
  <main class="content">...</main>
  <aside class="sidebar-right">...</aside>
</div>

<style>
.layout {
  display: grid;
  grid-template-columns: 200px 1fr 300px;
}
</style>
```

### ❌ Bad: Missing `<th>` Elements

```html
<!-- Headers should be <th>, not <td> with bold styling -->
<table>
  <tr>
    <td><strong>Product</strong></td>  <!-- Should be <th scope="col">! -->
    <td><strong>Price</strong></td>
    <td><strong>Stock</strong></td>
  </tr>
  <tr>
    <td>Laptop</td>
    <td>$999</td>
    <td>15</td>
  </tr>
</table>

<!-- Correct version: -->
<table>
  <thead>
    <tr>
      <th scope="col">Product</th>
      <th scope="col">Price</th>
      <th scope="col">Stock</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Laptop</td>
      <td>$999</td>
      <td>15</td>
    </tr>
  </tbody>
</table>
```

### ❌ Bad: No Table Description

```html
<!-- Missing caption or aria-label -->
<table>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
      <th scope="col">Role</th>
    </tr>
  </thead>
  <tbody>
    <!-- User data -->
  </tbody>
</table>

<!-- Better with caption: -->
<table>
  <caption>Team Members - 15 users</caption>
  <thead>
    <tr>
      <th scope="col">Name</th>
      <th scope="col">Email</th>
      <th scope="col">Role</th>
    </tr>
  </thead>
  <tbody>
    <!-- User data -->
  </tbody>
</table>
```

## Framework Examples

### React/JSX

```jsx
// Simple data table component
function DataTable({ data, columns, caption }) {
  return (
    <table>
      {caption && <caption>{caption}</caption>}
      <thead>
        <tr>
          {columns.map((col) => (
            <th key={col.key} scope="col">
              {col.label}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((row, index) => (
          <tr key={index}>
            {columns.map((col) => (
              <td key={col.key}>{row[col.key]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

// Usage
<DataTable
  caption="Sales Report - Q4 2024"
  columns={[
    { key: 'month', label: 'Month' },
    { key: 'sales', label: 'Sales' },
    { key: 'growth', label: 'Growth' }
  ]}
  data={salesData}
/>
```

### Vue

```vue
<template>
  <table>
    <caption>{{ caption }}</caption>
    <thead>
      <tr>
        <th v-for="header in headers" :key="header" scope="col">
          {{ header }}
        </th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(row, index) in rows" :key="index">
        <td v-for="(cell, cellIndex) in row" :key="cellIndex">
          {{ cell }}
        </td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  props: {
    caption: String,
    headers: Array,
    rows: Array
  }
}
</script>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 1.3.2**: Meaningful Sequence (Level A)

## Implementation Checklist

When creating tables:
- [ ] **Is the table used for tabular data, NOT layout?** (CRITICAL)
- [ ] **Do column headers use `<th>` elements?** (CRITICAL)
- [ ] **Do `<th>` elements have `scope` attributes?** (col or row)
- [ ] **Does the table have a `<caption>` or `aria-label`?** (when relevant)
- [ ] **Is the table structure simple?** (avoid complex colspan/rowspan)
- [ ] **Are headers grouped in `<thead>`?**
- [ ] **Is data grouped in `<tbody>`?**
- [ ] **Are row headers using `<th scope="row">`?** (when applicable)
- [ ] **Is the table keyboard accessible?**
- [ ] **Does the table work well on mobile?** (consider responsive design)

## Quick Reference

```
✅ DO:
- Use tables ONLY for tabular data (products, schedules, data)
- Use <th scope="col"> for column headers
- Use <th scope="row"> for row headers
- Include <caption> or aria-label for context
- Group headers in <thead>
- Group data in <tbody>
- Keep table structure simple
- Use CSS Grid/Flexbox for layouts

❌ DON'T:
- Use tables for page layout or positioning
- Use <td> for headers (use <th> instead)
- Omit scope attribute on <th> elements
- Create tables without descriptions
- Use complex nested tables
- Overuse colspan/rowspan (avoid when possible)
- Style tables to look like layouts
- Use tables for navigation menus

## When to Use Tables:

✅ Use tables for:
- Shopping carts
- Product comparisons
- Price lists
- Data reports
- Schedules/calendars
- Financial data
- Any row/column data relationships

❌ Use CSS layout for:
- Page structure
- Navigation menus
- Form layouts
- Card grids
- Multi-column text
- Sidebars
```
