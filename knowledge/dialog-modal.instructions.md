---
description: Instructions for proper modal dialog accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Modal Dialog Accessibility

## CRITICAL RULES

**Modal dialogs interrupt the user's workflow and require interaction before returning to the main content.**

### 1. Use role="dialog" with aria-modal="true"

**Every modal dialog MUST have `role="dialog"` and `aria-modal="true"`.**

```html
✅ Good - Proper dialog roles:
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Confirm Delete</h2>
  <p>Are you sure you want to delete this item?</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>

❌ Bad - Missing aria-modal:
<div role="dialog" aria-labelledby="dialog-title">
  <!-- Missing aria-modal="true"! -->
  <h2 id="dialog-title">Confirm</h2>
</div>

❌ Bad - Missing role="dialog":
<div aria-modal="true">  <!-- Missing role="dialog"! -->
  <h2>Dialog Title</h2>
</div>
```

**When to use `aria-modal="true"`:**
- Visual styling obscures content outside the dialog (overlay/backdrop)
- Application prevents interaction with elements outside the dialog
- Both conditions must be true

### 2. Provide Accessible Name with aria-labelledby or aria-label

**Every dialog MUST have an accessible name using `aria-labelledby` (preferred) or `aria-label`.**

```html
✅ Good - Using aria-labelledby (preferred):
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Save Changes</h2>
  <p>Do you want to save your changes before closing?</p>
</div>

✅ Good - Using aria-label:
<div role="dialog" aria-modal="true" aria-label="Confirmation dialog">
  <p>Are you sure you want to proceed?</p>
</div>

❌ Bad - No accessible name:
<div role="dialog" aria-modal="true">  <!-- Missing aria-labelledby or aria-label! -->
  <h2>Dialog Title</h2>
</div>
```

**Optional: aria-describedby**
- Use ONLY for simple, static descriptions
- Do NOT use if dialog content has complex semantics (lists, tables, multiple paragraphs)

```html
✅ Good - Simple description:
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc">
  <h2 id="dialog-title">Delete File</h2>
  <p id="dialog-desc">This action cannot be undone.</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>

❌ Bad - Complex content with aria-describedby:
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="title"
  aria-describedby="content">  <!-- Don't use for complex content! -->
  <h2 id="title">Settings</h2>
  <div id="content">
    <ul>
      <li>Option 1</li>
      <li>Option 2</li>
    </ul>
    <table>...</table>  <!-- Complex semantics! -->
  </div>
</div>
```

### 3. Trap Focus Within the Dialog

**Focus MUST be trapped inside the dialog. Users cannot tab to elements outside the dialog.**

Required keyboard behavior:
- **Tab**: Move to next focusable element; wrap to first when at last
- **Shift+Tab**: Move to previous focusable element; wrap to last when at first
- **Escape**: Close the dialog

```javascript
// ✅ Good - Focus trap implementation
function trapFocus(dialog) {
  const focusableElements = dialog.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstFocusable = focusableElements[0];
  const lastFocusable = focusableElements[focusableElements.length - 1];

  dialog.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey) {
        // Shift+Tab: wrap to last element
        if (document.activeElement === firstFocusable) {
          e.preventDefault();
          lastFocusable.focus();
        }
      } else {
        // Tab: wrap to first element
        if (document.activeElement === lastFocusable) {
          e.preventDefault();
          firstFocusable.focus();
        }
      }
    } else if (e.key === 'Escape') {
      closeDialog();
    }
  });
}
```

### 4. Manage Initial Focus and Focus Return

**When dialog opens, move focus to an appropriate element inside the dialog.**

**When dialog closes, return focus to the element that opened it.**

```javascript
// ✅ Good - Focus management
let previouslyFocusedElement;

function openDialog(dialog) {
  // Save reference to element that opened dialog
  previouslyFocusedElement = document.activeElement;

  // Show dialog
  dialog.removeAttribute('hidden');

  // Move focus into dialog
  const firstButton = dialog.querySelector('button');
  if (firstButton) {
    firstButton.focus();
  }

  // Trap focus
  trapFocus(dialog);
}

function closeDialog(dialog) {
  // Hide dialog
  dialog.setAttribute('hidden', '');

  // Return focus to triggering element
  if (previouslyFocusedElement) {
    previouslyFocusedElement.focus();
  }
}
```

**Initial focus guidelines:**
- **Simple dialogs**: Focus first focusable element (usually first button)
- **Destructive actions**: Consider focusing least destructive button (e.g., "Cancel")
- **Long/complex content**: Focus static element with `tabindex="-1"` at content start
- **Forms**: Focus first form field

### 5. Ensure All Interactive Elements Are Inside Dialog

**All elements required to operate the dialog MUST be descendants of the dialog element.**

```html
✅ Good - All controls inside dialog:
<div role="dialog" aria-modal="true" aria-labelledby="title">
  <h2 id="title">Confirm Action</h2>
  <p>Are you sure?</p>
  <button>Cancel</button>
  <button>Confirm</button>
  <button aria-label="Close dialog">×</button>
</div>

❌ Bad - Close button outside dialog:
<div role="dialog" aria-modal="true" aria-labelledby="title">
  <h2 id="title">Dialog</h2>
  <p>Content...</p>
</div>
<button onclick="closeDialog()">Close</button>  <!-- Outside dialog! -->

❌ Bad - Dialog nested in aria-hidden:
<div aria-hidden="true">
  <div role="dialog" aria-modal="true">  <!-- Can't nest inside aria-hidden! -->
    <h2>Dialog</h2>
  </div>
</div>
```

## Complete Modal Dialog Structure

```html
<!-- Trigger button -->
<button id="open-dialog-btn" onclick="openDialog()">
  Open Dialog
</button>

<!-- Modal dialog -->
<div
  id="confirmation-dialog"
  role="dialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  hidden>

  <h2 id="dialog-title">Confirm Delete</h2>

  <p>
    Are you sure you want to delete this item? This action cannot be undone.
  </p>

  <div class="dialog-buttons">
    <button onclick="closeDialog()">Cancel</button>
    <button onclick="confirmDelete()">Delete</button>
  </div>

  <button
    aria-label="Close dialog"
    class="close-button"
    onclick="closeDialog()">
    ×
  </button>
</div>

<!-- Backdrop overlay -->
<div id="dialog-backdrop" class="backdrop" hidden onclick="closeDialog()"></div>

<script>
let previouslyFocusedElement;

function openDialog() {
  const dialog = document.getElementById('confirmation-dialog');
  const backdrop = document.getElementById('dialog-backdrop');

  // Save focus
  previouslyFocusedElement = document.activeElement;

  // Show dialog and backdrop
  dialog.removeAttribute('hidden');
  backdrop.removeAttribute('hidden');

  // Move focus to first button
  const cancelButton = dialog.querySelector('button');
  cancelButton.focus();

  // Trap focus
  trapFocusInDialog(dialog);
}

function closeDialog() {
  const dialog = document.getElementById('confirmation-dialog');
  const backdrop = document.getElementById('dialog-backdrop');

  // Hide dialog and backdrop
  dialog.setAttribute('hidden', '');
  backdrop.setAttribute('hidden', '');

  // Return focus
  if (previouslyFocusedElement) {
    previouslyFocusedElement.focus();
  }
}

function trapFocusInDialog(dialog) {
  const focusableElements = dialog.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  dialog.addEventListener('keydown', handleKeyDown);

  function handleKeyDown(e) {
    if (e.key === 'Escape') {
      closeDialog();
    } else if (e.key === 'Tab') {
      if (e.shiftKey) {
        if (document.activeElement === firstElement) {
          e.preventDefault();
          lastElement.focus();
        }
      } else {
        if (document.activeElement === lastElement) {
          e.preventDefault();
          firstElement.focus();
        }
      }
    }
  }
}
</script>
```

## Examples

### ✅ Good: Confirmation Dialog

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="confirm-title"
  hidden>
  <h2 id="confirm-title">Unsaved Changes</h2>
  <p>You have unsaved changes. Do you want to save before closing?</p>
  <button onclick="saveAndClose()">Save</button>
  <button onclick="closeWithoutSaving()">Don't Save</button>
  <button onclick="cancelClose()">Cancel</button>
</div>
```

### ✅ Good: Form Dialog

```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="form-title">
  <h2 id="form-title">Add New User</h2>

  <form>
    <label for="username">Username</label>
    <input type="text" id="username" required>

    <label for="email">Email</label>
    <input type="email" id="email" required>

    <button type="submit">Add User</button>
    <button type="button" onclick="closeDialog()">Cancel</button>
  </form>
</div>
```

### ✅ Good: Alert Dialog (Critical Message)

```html
<div
  role="alertdialog"
  aria-modal="true"
  aria-labelledby="alert-title"
  aria-describedby="alert-desc">
  <h2 id="alert-title">Error</h2>
  <p id="alert-desc">Your session has expired. Please log in again.</p>
  <button onclick="redirectToLogin()">Log In</button>
</div>
```

**Note**: Use `role="alertdialog"` instead of `role="dialog"` for urgent messages requiring immediate attention.

### ✅ Good: React Modal Dialog Component

```jsx
function Modal({ isOpen, onClose, title, children }) {
  const [previousFocus, setPreviousFocus] = React.useState(null);
  const dialogRef = React.useRef(null);

  React.useEffect(() => {
    if (isOpen) {
      // Save previous focus
      setPreviousFocus(document.activeElement);

      // Focus first button in dialog
      const firstButton = dialogRef.current?.querySelector('button');
      firstButton?.focus();

      // Add escape key listener
      const handleEscape = (e) => {
        if (e.key === 'Escape') {
          onClose();
        }
      };
      document.addEventListener('keydown', handleEscape);

      return () => {
        document.removeEventListener('keydown', handleEscape);
        // Return focus when closing
        previousFocus?.focus();
      };
    }
  }, [isOpen, onClose, previousFocus]);

  if (!isOpen) return null;

  return (
    <>
      <div className="backdrop" onClick={onClose} />
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="dialog-title">
        <h2 id="dialog-title">{title}</h2>
        {children}
      </div>
    </>
  );
}

// Usage
<Modal
  isOpen={showDialog}
  onClose={() => setShowDialog(false)}
  title="Confirm Action">
  <p>Are you sure you want to continue?</p>
  <button onClick={handleConfirm}>Confirm</button>
  <button onClick={() => setShowDialog(false)}>Cancel</button>
</Modal>
```

### ✅ Good: Vue Modal Dialog Component

```vue
<template>
  <div v-if="isOpen">
    <div class="backdrop" @click="$emit('close')"></div>
    <div
      ref="dialog"
      role="dialog"
      aria-modal="true"
      :aria-labelledby="titleId">
      <h2 :id="titleId">{{ title }}</h2>
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    isOpen: Boolean,
    title: String
  },
  data() {
    return {
      previousFocus: null,
      titleId: `dialog-title-${Math.random().toString(36).substr(2, 9)}`
    };
  },
  watch: {
    isOpen(newValue) {
      if (newValue) {
        this.previousFocus = document.activeElement;
        this.$nextTick(() => {
          const firstButton = this.$refs.dialog?.querySelector('button');
          firstButton?.focus();
        });
      } else {
        this.previousFocus?.focus();
      }
    }
  },
  mounted() {
    document.addEventListener('keydown', this.handleKeyDown);
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleKeyDown);
  },
  methods: {
    handleKeyDown(e) {
      if (e.key === 'Escape' && this.isOpen) {
        this.$emit('close');
      }
    }
  }
};
</script>
```

### ❌ Bad: Missing Required Attributes

```html
<!-- Missing aria-modal -->
<div role="dialog" aria-labelledby="title">
  <h2 id="title">Dialog</h2>
</div>

<!-- Missing aria-labelledby or aria-label -->
<div role="dialog" aria-modal="true">
  <h2>Dialog Title</h2>
</div>

<!-- Missing role="dialog" -->
<div aria-modal="true" aria-label="Dialog">
  <p>Content...</p>
</div>
```

### ❌ Bad: No Focus Trap

```javascript
// ❌ Bad - No focus management
function openDialog() {
  dialog.style.display = 'block';
  // Missing: focus trap, initial focus, Escape key handler
}
```

### ❌ Bad: Not Returning Focus

```javascript
// ❌ Bad - Doesn't return focus
function closeDialog() {
  dialog.style.display = 'none';
  // Missing: return focus to triggering element
}
```

### ❌ Bad: Using aria-describedby for Complex Content

```html
<!-- Don't use aria-describedby for lists, tables, etc. -->
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="title"
  aria-describedby="content">
  <h2 id="title">Settings</h2>
  <div id="content">
    <ul>  <!-- Complex semantics! -->
      <li>Setting 1</li>
      <li>Setting 2</li>
    </ul>
  </div>
</div>
```

## WCAG References

- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 2.1.2**: No Keyboard Trap (Level A)
- **WCAG 2.1 Success Criterion 2.4.3**: Focus Order (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

When creating modal dialogs:
- [ ] **Does the dialog have `role="dialog"`?** (CRITICAL)
- [ ] **Does the dialog have `aria-modal="true"`?** (CRITICAL)
- [ ] **Does the dialog have `aria-labelledby` or `aria-label`?** (CRITICAL)
- [ ] **Is focus trapped inside the dialog?** (CRITICAL - Tab/Shift+Tab wrap within dialog)
- [ ] **Does Escape key close the dialog?** (CRITICAL)
- [ ] **Does opening the dialog move focus inside?** (CRITICAL)
- [ ] **Does closing the dialog return focus to the triggering element?** (CRITICAL)
- [ ] **Are all interactive elements inside the dialog element?** (CRITICAL)
- [ ] Is `aria-describedby` used only for simple descriptions?
- [ ] Does the dialog have a visible close button?
- [ ] Is the backdrop/overlay properly implemented?
- [ ] Are destructive actions appropriately de-emphasized in focus order?
- [ ] Is the dialog hidden when not open (using `hidden` attribute)?

## Quick Reference

```
✅ DO:
- Use role="dialog" and aria-modal="true"
- Provide aria-labelledby (preferred) or aria-label
- Trap focus inside the dialog (Tab wraps to first, Shift+Tab to last)
- Close dialog on Escape key
- Move focus into dialog when opening
- Return focus to triggering element when closing
- Include all interactive elements inside dialog
- Use aria-describedby only for simple, static descriptions
- Include a visible close button
- Hide dialog with hidden attribute when closed

❌ DON'T:
- Omit role="dialog" or aria-modal="true"
- Forget to provide accessible name (aria-labelledby/aria-label)
- Allow focus to escape the dialog
- Ignore Escape key
- Leave focus on triggering element when dialog opens
- Lose focus when dialog closes
- Put interactive elements outside dialog container
- Use aria-describedby for complex content (lists, tables)
- Nest dialog inside aria-hidden="true" elements
- Use visibility: hidden to hide dialogs (use hidden attribute)

## Dialog Types:

role="dialog":
  - Standard modal dialogs
  - Form dialogs
  - Confirmation dialogs

role="alertdialog":
  - Error messages requiring immediate attention
  - Critical warnings
  - Urgent confirmations

## Focus Placement:

Simple dialogs → First focusable element (usually button)
Destructive actions → Least destructive button ("Cancel")
Long content → Static element with tabindex="-1"
Form dialogs → First form field
```
