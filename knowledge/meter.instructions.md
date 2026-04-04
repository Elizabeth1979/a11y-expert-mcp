---
description: Instructions for proper meter accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Meter Accessibility

## CRITICAL RULES

**Meters display a scalar measurement within a known range (e.g., disk usage, temperature). Use for gauges and indicators, NOT for progress bars.**

### 1. Use role="meter" with Required ARIA Attributes

**Meters MUST have `role="meter"`, `aria-valuenow`, `aria-valuemin`, and `aria-valuemax`.**

```html
✅ Good - Proper meter:
<div
  role="meter"
  aria-label="Disk usage"
  aria-valuenow="75"
  aria-valuemin="0"
  aria-valuemax="100">
  75%
</div>

❌ Bad - Missing value attributes:
<div role="meter" aria-label="Usage">
  75%  <!-- Missing aria-valuenow, aria-valuemin, aria-valuemax! -->
</div>
```

### 2. Use Meter for Measurements, NOT Progress

**Use `role="meter"` for scalar measurements within a range. Use `role="progressbar"` for task completion.**

```html
✅ Good - Meter for measurement:
<div
  role="meter"
  aria-label="Battery level"
  aria-valuenow="50"
  aria-valuemin="0"
  aria-valuemax="100">
  50%
</div>

✅ Good - Progressbar for task completion:
<div
  role="progressbar"
  aria-label="Upload progress"
  aria-valuenow="50"
  aria-valuemin="0"
  aria-valuemax="100">
  50% uploaded
</div>

❌ Bad - Using meter for progress:
<div
  role="meter"
  aria-label="Loading"
  aria-valuenow="50"
  aria-valuemin="0"
  aria-valuemax="100">
  <!-- Should be progressbar! -->
  50% complete
</div>
```

**Key distinction**:
- **Meter**: Current state of a measurement (battery, disk space, temperature, ratings)
- **Progressbar**: Task completion percentage (file upload, page loading, operation progress)

### 3. Use aria-valuetext for User-Friendly Values

**When percentage alone isn't meaningful, provide `aria-valuetext` with contextual information.**

```html
✅ Good - Meter with aria-valuetext:
<div
  role="meter"
  aria-label="Battery"
  aria-valuenow="50"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-valuetext="50% (6 hours remaining)">
  50%
</div>

✅ Good - Temperature meter:
<div
  role="meter"
  aria-label="CPU temperature"
  aria-valuenow="72"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-valuetext="72 degrees Celsius">
  72°C
</div>

✅ Good - Star rating:
<div
  role="meter"
  aria-label="Product rating"
  aria-valuenow="4.5"
  aria-valuemin="0"
  aria-valuemax="5"
  aria-valuetext="4.5 out of 5 stars">
  ★★★★½
</div>
```

### 4. Provide Accessible Label

**Every meter MUST have an accessible label.**

```html
✅ Good - Using aria-label:
<div
  role="meter"
  aria-label="Storage used"
  aria-valuenow="85"
  aria-valuemin="0"
  aria-valuemax="100">
  85GB of 100GB
</div>

✅ Good - Using aria-labelledby:
<span id="disk-label">Disk Usage</span>
<div
  role="meter"
  aria-labelledby="disk-label"
  aria-valuenow="75"
  aria-valuemin="0"
  aria-valuemax="100">
  75%
</div>

❌ Bad - No accessible label:
<div
  role="meter"
  aria-valuenow="75"
  aria-valuemin="0"
  aria-valuemax="100">
  75%  <!-- What is being measured? -->
</div>
```

### 5. Do NOT Use for Unbounded Values

**Meters require defined min/max ranges. Don't use for values without meaningful limits.**

```html
❌ Bad - Unbounded value:
<div
  role="meter"
  aria-label="World population"
  aria-valuenow="8000000000"
  aria-valuemin="0"
  aria-valuemax="??">
  <!-- No meaningful maximum! Don't use meter -->
  8 billion
</div>

✅ Good - Use plain text instead:
<div>
  World population: <strong>8 billion</strong>
</div>
```

## Complete Meter Structure

```html
<!-- Battery level meter -->
<div class="meter-container">
  <label id="battery-label">Battery Level</label>
  <div
    role="meter"
    aria-labelledby="battery-label"
    aria-valuenow="65"
    aria-valuemin="0"
    aria-valuemax="100"
    aria-valuetext="65% charged">
    <div class="meter-bar" style="width: 65%;">
      <span class="meter-value">65%</span>
    </div>
  </div>
</div>

<!-- Disk usage meter -->
<div class="meter-container">
  <span id="disk-label">Disk Usage</span>
  <div
    role="meter"
    aria-labelledby="disk-label"
    aria-valuenow="250"
    aria-valuemin="0"
    aria-valuemax="500"
    aria-valuetext="250GB of 500GB used">
    <div class="meter-bar" style="width: 50%;">
      <span class="meter-value">250GB / 500GB</span>
    </div>
  </div>
</div>

<!-- Temperature meter with color zones -->
<div class="meter-container">
  <div
    role="meter"
    aria-label="CPU Temperature"
    aria-valuenow="82"
    aria-valuemin="0"
    aria-valuemax="100"
    aria-valuetext="82 degrees Celsius - High"
    class="meter-high">
    <div class="meter-bar" style="width: 82%;">
      <span class="meter-value">82°C</span>
    </div>
  </div>
</div>

<style>
.meter-container {
  margin: 1rem 0;
}

[role="meter"] {
  position: relative;
  width: 200px;
  height: 24px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.meter-bar {
  height: 100%;
  background: #4caf50;
  transition: width 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.meter-value {
  color: white;
  font-weight: bold;
  font-size: 12px;
}

/* Different colors for different levels */
.meter-low .meter-bar {
  background: #ff9800; /* Orange for low battery */
}

.meter-high .meter-bar {
  background: #f44336; /* Red for high temperature */
}
</style>
```

## Examples

### ✅ Good: Storage Meter

```html
<div
  role="meter"
  aria-label="Cloud storage"
  aria-valuenow="15"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-valuetext="15GB of 100GB used">
  <div style="width: 15%; background: blue; height: 20px;"></div>
  <span>15GB / 100GB</span>
</div>
```

### ✅ Good: Star Rating Meter

```html
<div
  role="meter"
  aria-label="Average customer rating"
  aria-valuenow="4.3"
  aria-valuemin="0"
  aria-valuemax="5"
  aria-valuetext="4.3 out of 5 stars">
  ★★★★☆ 4.3
</div>
```

### ✅ Good: React Meter Component

```jsx
function Meter({ label, value, min = 0, max = 100, valueText }) {
  const percentage = ((value - min) / (max - min)) * 100;

  // Determine color based on percentage
  const getColor = () => {
    if (percentage < 25) return '#ff9800'; // Orange
    if (percentage < 50) return '#ffc107'; // Yellow
    if (percentage < 75) return '#4caf50'; // Green
    return '#f44336'; // Red
  };

  return (
    <div className="meter-container">
      <label>{label}</label>
      <div
        role="meter"
        aria-label={label}
        aria-valuenow={value}
        aria-valuemin={min}
        aria-valuemax={max}
        aria-valuetext={valueText || `${value} of ${max}`}
        className="meter">
        <div
          className="meter-bar"
          style={{
            width: `${percentage}%`,
            background: getColor()
          }}>
          <span className="meter-value">
            {valueText || `${value}/${max}`}
          </span>
        </div>
      </div>
    </div>
  );
}

// Usage
function App() {
  return (
    <>
      <Meter
        label="Battery Level"
        value={65}
        max={100}
        valueText="65% (3 hours remaining)"
      />

      <Meter
        label="Disk Usage"
        value={250}
        max={500}
        valueText="250GB of 500GB used"
      />

      <Meter
        label="CPU Temperature"
        value={72}
        max={100}
        valueText="72°C - Normal"
      />
    </>
  );
}
```

### ✅ Good: Vue Meter Component

```vue
<template>
  <div class="meter-container">
    <label>{{ label }}</label>
    <div
      role="meter"
      :aria-label="label"
      :aria-valuenow="value"
      :aria-valuemin="min"
      :aria-valuemax="max"
      :aria-valuetext="computedValueText"
      class="meter">
      <div
        class="meter-bar"
        :style="{ width: percentage + '%', background: color }">
        <span class="meter-value">{{ displayValue }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    label: String,
    value: Number,
    min: {
      type: Number,
      default: 0
    },
    max: {
      type: Number,
      default: 100
    },
    valueText: String,
    unit: String
  },
  computed: {
    percentage() {
      return ((this.value - this.min) / (this.max - this.min)) * 100;
    },
    color() {
      if (this.percentage < 25) return '#ff9800';
      if (this.percentage < 50) return '#ffc107';
      if (this.percentage < 75) return '#4caf50';
      return '#f44336';
    },
    computedValueText() {
      return this.valueText || `${this.value} of ${this.max}${this.unit || ''}`;
    },
    displayValue() {
      return `${this.value}${this.unit || ''}/${this.max}${this.unit || ''}`;
    }
  }
}
</script>
```

### ❌ Bad Examples

```html
<!-- Missing aria-valuenow/min/max -->
<div role="meter" aria-label="Level">
  50%  <!-- No value attributes! -->
</div>

<!-- Using meter for progress -->
<div
  role="meter"
  aria-label="File upload"
  aria-valuenow="50"
  aria-valuemin="0"
  aria-valuemax="100">
  <!-- Should be progressbar! -->
  50% uploaded
</div>

<!-- No accessible label -->
<div
  role="meter"
  aria-valuenow="75"
  aria-valuemin="0"
  aria-valuemax="100">
  75%  <!-- What is this measuring? -->
</div>

<!-- Unbounded value -->
<div
  role="meter"
  aria-label="Page views"
  aria-valuenow="9999999"
  aria-valuemin="0"
  aria-valuemax="???">
  <!-- No meaningful maximum! -->
</div>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 1.4.1**: Use of Color (Level A) - Don't rely solely on color
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does element have `role="meter"`?** (CRITICAL)
- [ ] **Does meter have `aria-valuenow`?** (CRITICAL)
- [ ] **Does meter have `aria-valuemin`?** (CRITICAL)
- [ ] **Does meter have `aria-valuemax`?** (CRITICAL)
- [ ] **Does meter have accessible label?** (CRITICAL)
- [ ] Is `aria-valuetext` used when percentage isn't user-friendly?
- [ ] Is meter used for measurements (not progress)?
- [ ] Does meter have defined min/max range?
- [ ] Is visual representation not relying on color alone?
- [ ] Does meter update aria-valuenow when value changes?

## Quick Reference

```
✅ DO:
- Use role="meter" for scalar measurements
- Include aria-valuenow, aria-valuemin, aria-valuemax
- Provide accessible label (aria-label or aria-labelledby)
- Use aria-valuetext for context (battery hours, temperature units)
- Ensure defined min/max range
- Update aria-valuenow when value changes
- Use for: battery level, disk usage, ratings, temperature, volume

❌ DON'T:
- Use meter for progress/loading (use progressbar)
- Omit required ARIA attributes
- Forget accessible label
- Use for unbounded values
- Rely on color alone to convey information
- Use meter when simple text would suffice

## Meter vs Progressbar:

meter role:
  - Current state measurement
  - Battery level
  - Disk usage
  - Temperature gauge
  - Star ratings
  - Signal strength
  - Value within known range
  - Relatively static values

progressbar role:
  - Task completion
  - File upload/download
  - Page loading
  - Operation progress
  - Percentage complete
  - Time-based progress
  - Dynamic increasing values
```
