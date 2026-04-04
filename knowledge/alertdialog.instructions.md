---
description: Instructions for proper alert dialog accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Alert Dialog Accessibility

## CRITICAL RULES

**Alert dialogs are modal dialogs that interrupt workflow to communicate critical messages requiring user response. Use when immediate action or acknowledgment is necessary.**

### 1. Use role="alertdialog" with aria-modal="true"

**Alert dialogs MUST use `role="alertdialog"` and `aria-modal="true"`.**

```html
✅ Good - Proper alert dialog:
<div
  role="alertdialog"
  aria-modal="true"
  aria-labelledby="dialog-title"
  aria-describedby="dialog-desc">
  <h2 id="dialog-title">Confirm Delete</h2>
  <p id="dialog-desc">
    Are you sure you want to delete this item? This cannot be undone.
  </p>
  <button>Cancel</button>
  <button>Delete</button>
</div>

❌ Bad - Using role="dialog" instead:
<div role="dialog" aria-modal="true">
  <!-- Should use role="alertdialog" for critical messages! -->
  <h2>Confirm Delete</h2>
</div>
```

### 2. Provide Both aria-labelledby and aria-describedby

**Alert dialogs MUST have both a title (aria-labelledby) and description (aria-describedby).**

```html
✅ Good - Both label and description:
<div
  role="alertdialog"
  aria-modal="true"
  aria-labelledby="alert-title"
  aria-describedby="alert-desc">
  <h2 id="alert-title">Unsaved Changes</h2>
  <p id="alert-desc">
    You have unsaved changes. Do you want to save before closing?
  </p>
  <button>Don't Save</button>
  <button>Cancel</button>
  <button>Save</button>
</div>

❌ Bad - Missing aria-describedby:
<div
  role="alertdialog"
  aria-modal="true"
  aria-labelledby="alert-title">
  <h2 id="alert-title">Error</h2>
  <p>Connection failed</p>  <!-- Not referenced! -->
</div>
```

### 3. Move Focus to Alert Dialog

**Unlike regular alerts (role="alert"), alert dialogs SHOULD receive focus when opened.**

```javascript
✅ Good - Focus moves to alert dialog:
function showAlertDialog() {
  const dialog = document.getElementById('alert-dialog');
  dialog.removeAttribute('hidden');

  // Move focus to first focusable element (usually first button)
  const firstButton = dialog.querySelector('button');
  firstButton.focus();
}

❌ Bad - Focus not moved:
function showAlertDialog() {
  const dialog = document.getElementById('alert-dialog');
  dialog.removeAttribute('hidden');
  // Focus stays on trigger button - wrong for alertdialog!
}
```

### 4. Trap Focus Within Alert Dialog

**Alert dialogs MUST trap keyboard focus - Tab should cycle only through dialog elements.**

```javascript
✅ Good - Focus trap implementation:
function trapFocus(dialog) {
  const focusableElements = dialog.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  dialog.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    }
  });
}
```

### 5. Close on Escape Key and Return Focus

**Alert dialogs MUST close on Escape and return focus to the trigger element.**

```javascript
✅ Good - Escape key and focus return:
let triggerElement = null;

function openAlertDialog() {
  triggerElement = document.activeElement;
  const dialog = document.getElementById('alert-dialog');
  dialog.removeAttribute('hidden');
  dialog.querySelector('button').focus();
}

function closeAlertDialog() {
  const dialog = document.getElementById('alert-dialog');
  dialog.setAttribute('hidden', '');

  if (triggerElement) {
    triggerElement.focus();
    triggerElement = null;
  }
}

dialog.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    e.preventDefault();
    closeAlertDialog();
  }
});
```

## Complete Alert Dialog Structure

```html
<button id="delete-btn">Delete Item</button>

<div
  id="confirm-delete"
  role="alertdialog"
  aria-modal="true"
  aria-labelledby="delete-title"
  aria-describedby="delete-desc"
  hidden>
  <div class="dialog-overlay"></div>

  <div class="dialog-content">
    <h2 id="delete-title">Confirm Delete</h2>

    <p id="delete-desc">
      Are you sure you want to delete this item?
      This action cannot be undone.
    </p>

    <div class="dialog-actions">
      <button id="cancel-btn">Cancel</button>
      <button id="confirm-btn" class="danger">Delete</button>
    </div>
  </div>
</div>

<script>
const deleteBtn = document.getElementById('delete-btn');
const dialog = document.getElementById('confirm-delete');
const cancelBtn = document.getElementById('cancel-btn');
const confirmBtn = document.getElementById('confirm-btn');
let triggerElement = null;

deleteBtn.addEventListener('click', openDialog);
cancelBtn.addEventListener('click', closeDialog);
confirmBtn.addEventListener('click', () => {
  // Perform delete action
  performDelete();
  closeDialog();
});

function openDialog() {
  triggerElement = document.activeElement;
  dialog.removeAttribute('hidden');

  // Move focus to first button
  cancelBtn.focus();

  // Trap focus
  trapFocus(dialog);

  // Handle Escape key
  dialog.addEventListener('keydown', handleEscape);
}

function closeDialog() {
  dialog.setAttribute('hidden', '');

  // Return focus
  if (triggerElement) {
    triggerElement.focus();
    triggerElement = null;
  }

  dialog.removeEventListener('keydown', handleEscape);
}

function handleEscape(e) {
  if (e.key === 'Escape') {
    e.preventDefault();
    closeDialog();
  }
}

function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  element.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
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
  });
}

function performDelete() {
  console.log('Item deleted');
}
</script>
```

## Examples

### ✅ Good: Error Alert Dialog

```html
<div
  role="alertdialog"
  aria-modal="true"
  aria-labelledby="error-title"
  aria-describedby="error-desc">
  <h2 id="error-title">Connection Error</h2>
  <p id="error-desc">
    Unable to connect to the server.
    Please check your internet connection and try again.
  </p>
  <button autofocus>OK</button>
</div>
```

### ✅ Good: Unsaved Changes Alert Dialog

```html
<div
  role="alertdialog"
  aria-modal="true"
  aria-labelledby="unsaved-title"
  aria-describedby="unsaved-desc">
  <h2 id="unsaved-title">Unsaved Changes</h2>
  <p id="unsaved-desc">
    You have unsaved changes. What would you like to do?
  </p>
  <button>Discard</button>
  <button>Cancel</button>
  <button autofocus>Save Changes</button>
</div>
```

### ✅ Good: React Alert Dialog Component

```jsx
function AlertDialog({ isOpen, title, message, onCancel, onConfirm }) {
  const dialogRef = useRef(null);
  const cancelBtnRef = useRef(null);
  const [triggerElement, setTriggerElement] = useState(null);

  useEffect(() => {
    if (isOpen) {
      setTriggerElement(document.activeElement);
      cancelBtnRef.current?.focus();
    } else if (triggerElement) {
      triggerElement.focus();
      setTriggerElement(null);
    }
  }, [isOpen]);

  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        onCancel();
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
      return () => document.removeEventListener('keydown', handleEscape);
    }
  }, [isOpen, onCancel]);

  if (!isOpen) return null;

  return (
    <div
      ref={dialogRef}
      role="alertdialog"
      aria-modal="true"
      aria-labelledby="alert-title"
      aria-describedby="alert-desc">
      <div className="dialog-overlay" onClick={onCancel}></div>

      <div className="dialog-content">
        <h2 id="alert-title">{title}</h2>
        <p id="alert-desc">{message}</p>

        <div className="dialog-actions">
          <button ref={cancelBtnRef} onClick={onCancel}>
            Cancel
          </button>
          <button onClick={onConfirm} className="danger">
            Confirm
          </button>
        </div>
      </div>
    </div>
  );
}

// Usage
function App() {
  const [showDialog, setShowDialog] = useState(false);

  const handleDelete = () => {
    setShowDialog(false);
    // Perform delete
  };

  return (
    <>
      <button onClick={() => setShowDialog(true)}>
        Delete Item
      </button>

      <AlertDialog
        isOpen={showDialog}
        title="Confirm Delete"
        message="Are you sure you want to delete this item? This cannot be undone."
        onCancel={() => setShowDialog(false)}
        onConfirm={handleDelete}
      />
    </>
  );
}
```

### ❌ Bad Examples

```html
<!-- Using role="dialog" instead of "alertdialog" -->
<div role="dialog" aria-modal="true">
  <h2>Critical Error</h2>  <!-- Should be alertdialog! -->
</div>

<!-- Missing aria-describedby -->
<div
  role="alertdialog"
  aria-modal="true"
  aria-labelledby="title">
  <h2 id="title">Delete?</h2>
  <p>This will delete everything</p>  <!-- Not connected! -->
</div>

<!-- Not moving focus -->
<div role="alertdialog" aria-modal="true" hidden>
  <h2>Confirm</h2>
  <button>OK</button>
</div>
<script>
dialog.removeAttribute('hidden');
// Focus not moved - wrong!
</script>

<!-- No focus trap -->
<div role="alertdialog" aria-modal="true">
  <h2>Alert</h2>
  <button>OK</button>
  <!-- Tab can escape dialog - wrong! -->
</div>
```

## Alert Dialog vs Regular Dialog

```html
<!-- Use alertdialog for critical interruptions -->
<div role="alertdialog" aria-modal="true">
  <h2>Delete Account?</h2>
  <p>This will permanently delete your account</p>
  <button>Cancel</button>
  <button>Delete Account</button>
</div>

<!-- Use regular dialog for non-critical interactions -->
<div role="dialog" aria-modal="true">
  <h2>Settings</h2>
  <form>
    <!-- Settings form -->
  </form>
  <button>Cancel</button>
  <button>Save</button>
</div>
```

## WCAG References

- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 2.1.2**: No Keyboard Trap (Level A)
- **WCAG 2.1 Success Criterion 2.4.3**: Focus Order (Level A)
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does dialog have `role="alertdialog"`?** (CRITICAL)
- [ ] **Does dialog have `aria-modal="true"`?** (CRITICAL)
- [ ] **Does dialog have `aria-labelledby`?** (CRITICAL)
- [ ] **Does dialog have `aria-describedby`?** (CRITICAL)
- [ ] **Does focus move to dialog when opened?** (CRITICAL)
- [ ] **Is focus trapped within dialog?** (CRITICAL)
- [ ] **Does Escape key close dialog?** (CRITICAL)
- [ ] **Does focus return to trigger element on close?** (CRITICAL)
- [ ] Are all elements inside dialog contained within alertdialog element?
- [ ] Is dialog visually distinct from page content?
- [ ] Does dialog have at least one action button?
- [ ] Is background content inert when dialog is open?

## Quick Reference

```
✅ DO:
- Use role="alertdialog" for critical messages
- Include aria-modal="true"
- Provide aria-labelledby (title)
- Provide aria-describedby (message)
- Move focus to dialog when opened
- Trap focus within dialog
- Close on Escape key
- Return focus to trigger element
- Use for confirmations, critical errors, data loss warnings
- Provide clear action buttons

❌ DON'T:
- Use role="dialog" for critical messages
- Forget aria-describedby
- Leave focus outside dialog
- Allow Tab to escape dialog
- Ignore Escape key
- Forget to return focus
- Use for non-critical messages (use role="alert" instead)
- Auto-dismiss without user action

## When to Use What:

alertdialog role:
  - Confirmation required ("Are you sure?")
  - Critical errors needing acknowledgment
  - Data loss warnings
  - Account deletion confirmations
  - Permanent action warnings
  - Security alerts requiring user response

dialog role:
  - Settings panels
  - Forms
  - Content viewers
  - Non-critical notifications with interactions
  - General modal windows

alert role:
  - Brief notifications
  - No user action required
  - Non-interrupting messages
  - Success/error messages
  - Auto-save confirmations
```
