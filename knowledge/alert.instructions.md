---
description: Instructions for proper alert accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Alert Accessibility

## CRITICAL RULES

**Alerts communicate brief, important messages without interrupting the user's workflow. Use for non-critical notifications that don't require user action.**

### 1. Use role="alert" for Dynamic Alerts

**Alerts MUST use `role="alert"` to be automatically announced by screen readers.**

```html
✅ Good - Dynamic alert:
<div role="alert">
  Your changes have been saved
</div>

✅ Good - Error alert:
<div role="alert">
  Error: Unable to connect to server
</div>

❌ Bad - Missing role="alert":
<div class="notification">
  Your changes have been saved  <!-- Not announced! -->
</div>
```

**CRITICAL**: Only alerts added to the DOM *after* page load are announced automatically. Pre-existing alerts are silent.

### 2. Alerts Must NOT Move Focus

**Alerts MUST preserve keyboard focus and NOT interrupt the user's workflow.**

```javascript
✅ Good - Alert doesn't move focus:
function showAlert(message) {
  const alert = document.createElement('div');
  alert.setAttribute('role', 'alert');
  alert.textContent = message;
  document.body.appendChild(alert);
  // Focus stays on current element
}

❌ Bad - Alert steals focus:
function showAlert(message) {
  const alert = document.createElement('div');
  alert.setAttribute('role', 'alert');
  alert.textContent = message;
  document.body.appendChild(alert);
  alert.focus();  // WRONG! Don't move focus
}
```

### 3. Do NOT Auto-Dismiss Alerts

**Alerts MUST remain visible long enough for users to read them. Avoid auto-dismissing alerts.**

```javascript
✅ Good - Alert stays visible:
<div role="alert">
  File uploaded successfully
  <button onclick="this.parentElement.remove()">Dismiss</button>
</div>

⚠️ Acceptable with caution - Long timeout (minimum 5+ seconds):
setTimeout(() => {
  alert.remove();
}, 10000); // 10 seconds - still risky

❌ Bad - Auto-dismisses too quickly:
setTimeout(() => {
  alert.remove();
}, 2000); // FAILS WCAG 2.2.3 - Not enough time
```

**WCAG 2.2.3**: Content must not disappear automatically unless user can extend the time limit.

### 4. Limit Alert Frequency

**Minimize interruptions - frequent alerts inhibit usability for people with cognitive disabilities.**

```javascript
✅ Good - Batch multiple alerts:
function showBatchedAlerts(messages) {
  const alert = document.createElement('div');
  alert.setAttribute('role', 'alert');
  alert.innerHTML = `
    <ul>
      ${messages.map(msg => `<li>${msg}</li>`).join('')}
    </ul>
  `;
  document.body.appendChild(alert);
}

❌ Bad - Multiple rapid alerts:
errors.forEach(error => {
  showAlert(error); // Creates too many interruptions!
});
```

### 5. Use Alert Dialog for Workflow Interruption

**If user action is required or workflow interruption is necessary, use `role="alertdialog"` instead.**

```html
✅ Use role="alert" for:
- Form submission success/error (no action needed)
- Auto-save confirmations
- System notifications
- Background process completions

✅ Use role="alertdialog" for:
- Confirmation required ("Are you sure?")
- Critical errors requiring acknowledgment
- Data loss warnings
```

## Complete Alert Structure

```html
<!-- Simple alert -->
<div role="alert" class="alert-success">
  Your profile has been updated
</div>

<!-- Alert with dismissible button -->
<div role="alert" class="alert-info">
  <span>New messages available</span>
  <button
    type="button"
    aria-label="Dismiss notification"
    onclick="this.parentElement.remove()">
    ×
  </button>
</div>

<!-- Error alert -->
<div role="alert" class="alert-error">
  <strong>Error:</strong> Unable to save changes. Please try again.
</div>

<!-- Alert container (for positioning) -->
<div aria-live="polite" aria-atomic="true" class="alert-container">
  <!-- Alerts will be dynamically added here -->
</div>

<script>
// Alert manager
const alertContainer = document.querySelector('.alert-container');
let alertCount = 0;

function showAlert(message, type = 'info') {
  alertCount++;
  const alertId = `alert-${alertCount}`;

  const alert = document.createElement('div');
  alert.id = alertId;
  alert.setAttribute('role', 'alert');
  alert.className = `alert-${type}`;

  alert.innerHTML = `
    <span>${message}</span>
    <button
      type="button"
      aria-label="Dismiss notification"
      onclick="dismissAlert('${alertId}')">
      ×
    </button>
  `;

  alertContainer.appendChild(alert);
}

function dismissAlert(alertId) {
  const alert = document.getElementById(alertId);
  if (alert) {
    alert.remove();
  }
}

// Example usage
document.getElementById('save-btn').addEventListener('click', () => {
  // Perform save operation
  showAlert('Your changes have been saved', 'success');
});
</script>
```

## Examples

### ✅ Good: Form Validation Alert

```html
<form id="contact-form">
  <label for="email">Email</label>
  <input type="email" id="email" required>

  <button type="submit">Submit</button>
</form>

<div id="form-alerts"></div>

<script>
document.getElementById('contact-form').addEventListener('submit', (e) => {
  e.preventDefault();
  const email = document.getElementById('email').value;

  const alertContainer = document.getElementById('form-alerts');
  const alert = document.createElement('div');
  alert.setAttribute('role', 'alert');

  if (!email.includes('@')) {
    alert.textContent = 'Please enter a valid email address';
    alert.className = 'alert-error';
  } else {
    alert.textContent = 'Form submitted successfully!';
    alert.className = 'alert-success';
  }

  alertContainer.innerHTML = '';
  alertContainer.appendChild(alert);
});
</script>
```

### ✅ Good: React Alert Component

```jsx
function Alert({ message, type = 'info', onDismiss }) {
  return (
    <div role="alert" className={`alert alert-${type}`}>
      <span>{message}</span>
      {onDismiss && (
        <button
          type="button"
          aria-label="Dismiss notification"
          onClick={onDismiss}>
          ×
        </button>
      )}
    </div>
  );
}

// Usage
function App() {
  const [alerts, setAlerts] = useState([]);

  const addAlert = (message, type) => {
    const id = Date.now();
    setAlerts([...alerts, { id, message, type }]);
  };

  const dismissAlert = (id) => {
    setAlerts(alerts.filter(alert => alert.id !== id));
  };

  return (
    <div>
      <button onClick={() => addAlert('Success!', 'success')}>
        Trigger Alert
      </button>

      <div className="alert-container">
        {alerts.map(alert => (
          <Alert
            key={alert.id}
            message={alert.message}
            type={alert.type}
            onDismiss={() => dismissAlert(alert.id)}
          />
        ))}
      </div>
    </div>
  );
}
```

### ✅ Good: Vue Alert Component

```vue
<template>
  <div role="alert" :class="`alert alert-${type}`">
    <span>{{ message }}</span>
    <button
      v-if="dismissible"
      type="button"
      aria-label="Dismiss notification"
      @click="$emit('dismiss')">
      ×
    </button>
  </div>
</template>

<script>
export default {
  props: {
    message: {
      type: String,
      required: true
    },
    type: {
      type: String,
      default: 'info'
    },
    dismissible: {
      type: Boolean,
      default: true
    }
  }
}
</script>
```

### ❌ Bad Examples

```html
<!-- Missing role="alert" -->
<div class="notification">
  Changes saved  <!-- Not announced to screen readers! -->
</div>

<!-- Auto-dismisses too quickly -->
<div role="alert" id="quick-alert">
  Error occurred
</div>
<script>
setTimeout(() => {
  document.getElementById('quick-alert').remove();
}, 1000); // FAILS WCAG 2.2.3
</script>

<!-- Moves focus (wrong!) -->
<div role="alert" tabindex="-1" id="focus-alert">
  Alert message
</div>
<script>
document.getElementById('focus-alert').focus(); // DON'T DO THIS
</script>

<!-- Too many rapid alerts -->
<script>
for (let i = 0; i < 10; i++) {
  const alert = document.createElement('div');
  alert.setAttribute('role', 'alert');
  alert.textContent = `Alert ${i}`;
  document.body.appendChild(alert); // Overwhelming!
}
</script>
```

## Alert vs Alert Dialog vs Live Region

```html
<!-- Use role="alert" for brief, non-interactive messages -->
<div role="alert">
  Message sent successfully
</div>

<!-- Use role="alertdialog" when user action required -->
<div role="alertdialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Confirm Delete</h2>
  <p>Are you sure you want to delete this item?</p>
  <button>Cancel</button>
  <button>Delete</button>
</div>

<!-- Use aria-live for status updates -->
<div aria-live="polite" aria-atomic="true">
  Loading: 50% complete
</div>
```

## WCAG References

- **WCAG 2.1 Success Criterion 2.2.3**: No Timing (Level AAA) - Don't auto-dismiss alerts
- **WCAG 2.1 Success Criterion 2.2.4**: Interruptions (Level AAA) - Minimize alert frequency
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)
- **WCAG 2.1 Success Criterion 4.1.3**: Status Messages (Level AA)

## Implementation Checklist

- [ ] **Does alert have `role="alert"`?** (CRITICAL)
- [ ] **Is alert added dynamically after page load?** (CRITICAL - pre-load alerts aren't announced)
- [ ] **Does alert preserve keyboard focus?** (CRITICAL - no focus movement)
- [ ] Does alert stay visible long enough to read?
- [ ] Is auto-dismiss avoided or has very long timeout (10+ seconds)?
- [ ] Are alerts batched to avoid too many interruptions?
- [ ] Is alertdialog used instead when user action required?
- [ ] Does dismissible alert have accessible close button?
- [ ] Is alert visually distinctive (color alone is not enough)?

## Quick Reference

```
✅ DO:
- Use role="alert" for dynamic messages
- Add alerts after page load (for announcement)
- Keep alerts visible (no auto-dismiss or 10+ seconds minimum)
- Preserve keyboard focus
- Batch multiple alerts together
- Provide dismiss button if alert is persistent
- Use clear, concise messaging
- Distinguish visually (not just by color)

❌ DON'T:
- Move focus to alert
- Auto-dismiss alerts quickly (< 10 seconds)
- Create too many rapid alerts
- Use for messages requiring user action (use alertdialog)
- Rely on color alone for meaning
- Forget role="alert" attribute
- Put alerts in the initial page HTML (they won't be announced)

## When to Use What:

alert role:
  - Brief, important message
  - No user action required
  - Non-critical notifications
  - Auto-save confirmations
  - Form submission results

alertdialog role:
  - User action required
  - Critical warnings
  - Confirmation prompts
  - Data loss prevention
  - Error acknowledgment needed

aria-live region:
  - Ongoing status updates
  - Progress indicators
  - Live search results
  - Chat messages
  - Real-time data updates
```
