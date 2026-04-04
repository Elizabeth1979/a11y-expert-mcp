---
description: Main accessibility instruction file for generating WCAG-compliant code
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Accessibility Coding Guidelines

## CRITICAL INSTRUCTION

**When making accessibility improvements, modify ONLY the HTML markup and semantic structure. DO NOT change the visual appearance or design of the page.**

- ✅ Add/fix HTML attributes (alt, aria-label, role, etc.)
- ✅ Change HTML tags to more semantic elements (div → button, div → nav, etc.)
- ✅ Add or reorganize heading levels (h1, h2, h3, etc.)
- ✅ Add ARIA attributes and labels
- ❌ DO NOT modify CSS styles
- ❌ DO NOT change colors, fonts, sizes, or layout
- ❌ DO NOT alter the visual design or appearance
- ❌ DO NOT add or remove visual elements

**The goal is to make the page accessible WITHOUT changing how it looks to sighted users.**

## Core Principles

Follow these fundamental accessibility principles:

1. **Perceivable** - Information must be presentable to users in ways they can perceive
2. **Operable** - User interface components must be operable by all users
3. **Understandable** - Information and UI operation must be understandable
4. **Robust** - Content must be robust enough to work with assistive technologies

## Specific Accessibility Skills

This main file references specialized instruction files for specific accessibility concerns. All widget patterns follow [WAI-ARIA Authoring Practices Guide (APG)](https://www.w3.org/WAI/ARIA/apg/patterns/).

### Document Structure
- [headings.instructions.md](headings.instructions.md) - Proper heading hierarchy and semantic structure
- [landmarks.instructions.md](landmarks.instructions.md) - Page landmarks and regions (banner, navigation, main, complementary, contentinfo, search, form, region)
- [breadcrumbs.instructions.md](breadcrumbs.instructions.md) - Breadcrumb navigation patterns

### Images and Media
- [Image_labeling.instructions.md](Image_labeling.instructions.md) - Proper alt text and image labeling

### Buttons and Interactive Elements
- [buttons.instructions.md](buttons.instructions.md) - Button accessibility and clickable elements
- [link.instructions.md](link.instructions.md) - Link accessibility and navigation elements

### Form Controls and Inputs
- [checkbox.instructions.md](checkbox.instructions.md) - Checkbox accessibility (dual-state and tri-state)
- [radio.instructions.md](radio.instructions.md) - Radio button groups (mutually exclusive selection)
- [switch.instructions.md](switch.instructions.md) - Switch/toggle controls (on/off states)
- [slider.instructions.md](slider.instructions.md) - Single-thumb slider controls
- [slider-multithumb.instructions.md](slider-multithumb.instructions.md) - Multi-thumb range sliders
- [spinbutton.instructions.md](spinbutton.instructions.md) - Number input with increment/decrement

### Selection and Dropdown Patterns
- [combobox.instructions.md](combobox.instructions.md) - Combobox/autocomplete patterns
- [listbox.instructions.md](listbox.instructions.md) - Selectable option lists

### Menus and Navigation
- [menu.instructions.md](menu.instructions.md) - Menu and menubar patterns
- [menu-button.instructions.md](menu-button.instructions.md) - Button that opens a menu

### Disclosure and Expansion Patterns
- [accordion.instructions.md](accordion.instructions.md) - Vertically stacked collapsible sections
- [disclosure.instructions.md](disclosure.instructions.md) - Show/hide toggles (expand/collapse)
- [tabs.instructions.md](tabs.instructions.md) - Layered tabbed content panels

### Dialog and Modal Patterns
- [dialog-modal.instructions.md](dialog-modal.instructions.md) - Modal dialog accessibility
- [alertdialog.instructions.md](alertdialog.instructions.md) - Alert dialog for critical messages
- [tooltip.instructions.md](tooltip.instructions.md) - Tooltip and popup information

### Alerts and Status Messages
- [alert.instructions.md](alert.instructions.md) - Non-interrupting alert messages
- [meter.instructions.md](meter.instructions.md) - Meter/gauge displays

### Tables and Data Display
- [tables.instructions.md](tables.instructions.md) - Proper table structure and semantics
- [grid.instructions.md](grid.instructions.md) - Interactive data grids with keyboard navigation
- [treegrid.instructions.md](treegrid.instructions.md) - Hierarchical grids with expandable rows

### Hierarchical and Feed Patterns
- [treeview.instructions.md](treeview.instructions.md) - Tree view for hierarchical data
- [feed.instructions.md](feed.instructions.md) - Auto-loading scrollable content feeds

### Layout and Presentation
- [carousel.instructions.md](carousel.instructions.md) - Carousel/slideshow patterns
- [toolbar.instructions.md](toolbar.instructions.md) - Toolbar grouping of controls
- [windowsplitter.instructions.md](windowsplitter.instructions.md) - Resizable pane splitters

## General Rules

1. **No visual changes** - Make accessibility improvements through HTML/semantic changes only, NOT through visual design changes
2. **Use semantic HTML** - Use appropriate HTML elements (`<button>`, `<nav>`, `<main>`, etc.) rather than generic divs
3. **Keyboard accessibility** - Ensure all interactive elements are keyboard accessible
4. **Focus indicators** - Never remove focus outlines without providing alternatives
5. **Color contrast** - Text must meet WCAG contrast ratios (4.5:1 for normal text, 3:1 for large text)
6. **Error identification** - Clearly identify and describe errors to users
7. **Labels and instructions** - Provide clear labels for all form inputs

## Testing Recommendations

When generating code, consider these testing approaches:
- Test with keyboard only (no mouse)
- Verify with screen reader (NVDA, JAWS, VoiceOver)
- Check color contrast ratios
- Validate HTML semantics
- Run automated accessibility audits (axe, Lighthouse)

## Resources

- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [MDN Accessibility](https://developer.mozilla.org/en-US/docs/Web/Accessibility)
