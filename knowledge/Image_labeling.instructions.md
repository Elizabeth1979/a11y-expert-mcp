---
description: Instructions for proper image accessibility and alt text implementation
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Image Labeling and Accessibility

## CRITICAL RULES

**EVERY image MUST have either an `alt` attribute OR an `aria-label` attribute. NEVER omit both.**

### 1. SVG Images: Use `aria-label`

For SVG images, use **`aria-label`** (NOT `alt`):
- The `alt` attribute is not valid on SVG elements
- Use `aria-label` to provide the accessible name
- Add `role="img"` to the SVG element

```html
✅ Good:
<svg aria-label="Download icon" role="img" width="24" height="24">
  <path d="M12 2L12 14M12 14L8 10M12 14L16 10M4 18L20 18"/>
</svg>

❌ Bad:
<svg alt="Download icon">  <!-- alt doesn't work on SVG -->
  <path d="..."/>
</svg>

❌ Bad:
<svg>  <!-- Missing aria-label -->
  <path d="..."/>
</svg>
```

### 2. Decorative Images: Use `alt=""`

Images that serve **only a decorative purpose** (not conveying information) MUST have an **empty alt attribute**:
- Use `alt=""` exactly (empty string)
- This tells screen readers to skip the image
- **NEVER omit the `alt` attribute entirely** - always include `alt=""`

```html
✅ Good:
<img src="decorative-flourish.png" alt="">

❌ Bad:
<img src="decorative-flourish.png">  <!-- Missing alt attribute -->
```

### 3. Content Images: Use Descriptive `alt` Text

Every `<img>` element that conveys information MUST have a descriptive `alt` attribute:
- **Human-readable and descriptive**
- **Convey the purpose or content** of the image
- **Concise** (typically under 125 characters)
- **Contextually appropriate** to the surrounding content

```html
✅ Good:
<img src="mountain-sunset.jpg" alt="Sunset over snow-capped mountains with orange and pink sky">

❌ Bad:
<img src="mountain-sunset.jpg" alt="image">  <!-- Not descriptive -->
<img src="mountain-sunset.jpg">  <!-- Missing alt attribute -->
```

### 4. Images of Text: Include the Text in Alt Attribute

**When an image contains text, the `alt` attribute MUST include that text.**

This applies to:
- Screenshots with text
- Graphics with text overlays
- Infographics with labels
- Logos with text
- Buttons or banners with text
- Any image where text is part of the content

**How to handle images of text:**

1. **If you know what text is in the image** → Include it in the `alt` attribute
2. **If you don't know the text content:**
   - **Option A (Preferred)**: Ask the user who generated the code what text is in the image
   - **Option B**: Try to perform OCR (Optical Character Recognition) on the image to extract the text
   - **Option C (Last Resort)**: Use `alt="Image of text, insert text here"` as a placeholder and add a comment asking for the actual text

```html
✅ Good - Image of text with text included:
<img src="welcome-banner.png" alt="Welcome to Our Website">
<img src="sale-graphic.png" alt="50% Off Sale - Limited Time Only">
<img src="quote.png" alt="The only way to do great work is to love what you do. - Steve Jobs">

❌ Bad - Missing the text content:
<img src="welcome-banner.png" alt="Banner image">  <!-- What does the banner say? -->
<img src="sale-graphic.png" alt="Sale graphic">  <!-- What's the sale text? -->

⚠️ Acceptable placeholder when text is unknown:
<img src="unknown-graphic.png" alt="Image of text, insert text here">
<!-- TODO: Replace with actual text from the image -->
```

**Important notes:**
- Users who can't see images need to know what text the image displays
- Screen readers will read the alt text aloud, so include the exact text from the image
- If the image has both text and other meaningful content, describe both

### 5. Images Inside Buttons or Clickable Elements

**CRITICAL: When an image is inside a button or clickable element (div/span with click handler), the image should have `alt=""` because labeling is handled by the containing button.**

The button/clickable element should have an `aria-label` describing the action, NOT the image inside.

```html
✅ Good - Button has aria-label, image has empty alt:
<button aria-label="Close dialog">
  <img src="close-icon.png" alt="">
</button>

<div role="button" tabindex="0" aria-label="Delete item" onclick="deleteItem()">
  <img src="trash-icon.png" alt="">
</div>

<button aria-label="Play video">
  <svg aria-hidden="true">
    <path d="..."/>
  </svg>
</button>

❌ Bad - Image has alt inside labeled button (redundant):
<button aria-label="Close dialog">
  <img src="close-icon.png" alt="Close icon">  <!-- Don't label the image! -->
</button>

❌ Bad - No aria-label on button with image:
<button>
  <img src="close-icon.png" alt="Close">  <!-- Button needs aria-label! -->
</button>
```

**Key rules:**
- If a button/clickable element has `aria-label` → images inside use `alt=""`
- If a button/clickable element has text content → images inside use `alt=""`
- The button's label (aria-label or text) describes the ACTION
- SVG icons inside buttons should use `aria-hidden="true"`

**See [buttons.instructions.md](buttons.instructions.md) for complete button accessibility guidelines.**

### 6. Background Images (CSS)

Background images added via CSS cannot have alt text:
- If the background image is decorative, no action needed
- If the background image conveys information, add an `aria-label` to the container element
- Alternatively, use an `<img>` tag instead when the image is content, not decoration

## Examples

### ✅ Good: Content Image with Descriptive Alt Text

```html
<!-- HTML -->
<img src="mountain-sunset.jpg" alt="Sunset over snow-capped mountains with orange and pink sky">
```

```jsx
<!-- React/JSX -->
<img src={profilePic} alt="Sarah Johnson, Senior Developer" />
```

### ✅ Good: Decorative Image with Empty Alt

```html
<!-- Decorative border image -->
<img src="decorative-flourish.png" alt="">
```

```jsx
<!-- React decorative icon next to text -->
<div>
  <img src="star-icon.svg" alt="" />
  <span>Featured Item</span>
</div>
```

### ✅ Good: SVG with aria-label

```html
<!-- Inline SVG -->
<svg aria-label="Download icon" role="img" width="24" height="24">
  <path d="M12 2L12 14M12 14L8 10M12 14L16 10M4 18L20 18"/>
</svg>
```

```jsx
<!-- React SVG component -->
<svg aria-label="User profile menu" role="img" viewBox="0 0 24 24">
  <circle cx="12" cy="8" r="4"/>
  <path d="M4 20c0-4 4-6 8-6s8 2 8 6"/>
</svg>
```

### ✅ Good: Images of Text

```html
<!-- Screenshot with text -->
<img src="error-message.png" alt="Error: Invalid username or password">

<!-- Logo with text -->
<img src="company-logo.png" alt="Acme Corporation">

<!-- Promotional banner -->
<img src="summer-sale.png" alt="Summer Sale - Up to 70% Off - Shop Now">

<!-- Quote graphic -->
<img src="motivational-quote.png" alt="Dream big, work hard, stay focused">

<!-- Button image with text -->
<img src="download-button.png" alt="Download Free Trial">

<!-- Infographic with text and content -->
<img src="tips-infographic.png" alt="5 Tips for Success: 1. Set clear goals, 2. Stay organized, 3. Manage your time, 4. Keep learning, 5. Stay motivated">
```

```jsx
<!-- React - Image of text in a component -->
<img
  src={bannerImage}
  alt="New Feature: Dark Mode Now Available"
/>
```

### ✅ Good: SVG with title and desc

```html
<!-- Complex SVG with detailed description -->
<svg role="img" viewBox="0 0 200 200">
  <title>Company Sales Chart</title>
  <desc>Bar chart showing monthly sales from January to December, with highest sales in July at $50,000</desc>
  <!-- chart elements -->
</svg>
```

### ✅ Good: Images Inside Buttons

```html
<!-- Icon-only button with aria-label -->
<button aria-label="Close notification">
  <img src="close-icon.png" alt="">
</button>

<!-- Button with text - image is decorative -->
<button onclick="save()">
  <img src="save-icon.png" alt="">
  Save Changes
</button>

<!-- Clickable div with role="button" -->
<div role="button" tabindex="0" aria-label="Delete item" onclick="deleteItem()">
  <img src="trash-icon.png" alt="">
</div>

<!-- Button with SVG icon -->
<button aria-label="Settings">
  <svg aria-hidden="true" width="20" height="20">
    <path d="..."/>
  </svg>
</button>
```

```jsx
<!-- React - Icon button -->
<button aria-label="Open menu" onClick={openMenu}>
  <img src={menuIcon} alt="" />
</button>

<!-- React - Button with text and icon -->
<button onClick={handleSubmit}>
  <svg aria-hidden="true">...</svg>
  Submit Form
</button>
```

### ✅ Good: Background Image with Accessible Alternative

```html
<!-- CSS background image with aria-label on container -->
<div
  class="hero-banner"
  style="background-image: url('team-photo.jpg')"
  role="img"
  aria-label="Our development team collaborating in the office">
  <h1>Meet Our Team</h1>
</div>
```

### ❌ Bad: Missing Alt Attribute - CRITICAL ERROR

```html
<!-- NEVER EVER do this - this is a CRITICAL accessibility violation -->
<img src="important-chart.png">  <!-- Missing alt attribute! -->
<img src="logo.png">  <!-- Missing alt attribute! -->
<img src="photo.jpg">  <!-- Missing alt attribute! -->

<!-- ALWAYS include alt, even if empty for decorative images -->
<img src="decorative.png" alt="">  <!-- Correct for decorative -->
<img src="photo.jpg" alt="Team celebrating in office">  <!-- Correct for content -->
```

### ❌ Bad: SVG Without aria-label - CRITICAL ERROR

```html
<!-- NEVER do this - SVG must have aria-label -->
<svg width="24" height="24">  <!-- Missing aria-label! -->
  <path d="..."/>
</svg>

<!-- Wrong: alt doesn't work on SVG -->
<svg alt="Download icon">  <!-- alt is invalid on SVG! -->
  <path d="..."/>
</svg>

<!-- Correct: use aria-label -->
<svg aria-label="Download icon" role="img" width="24" height="24">
  <path d="..."/>
</svg>
```

### ❌ Bad: Non-Descriptive Alt Text

```html
<!-- Too vague - be descriptive -->
<img src="chart.png" alt="chart">  <!-- Not descriptive enough -->
<img src="photo.jpg" alt="image">  <!-- Not descriptive enough -->
<img src="diagram.png" alt="picture">  <!-- Not descriptive enough -->

<!-- Better: -->
<img src="chart.png" alt="Monthly sales revenue chart for 2024">
<img src="photo.jpg" alt="Sarah Johnson presenting at conference">
<img src="diagram.png" alt="System architecture diagram showing database connections">
```

### ❌ Bad: Decorative Image with Descriptive Alt

```html
<!-- Decorative flourish doesn't need description -->
<img src="decorative-line.png" alt="decorative horizontal line with curves">

<!-- Correct: use empty alt for decorative images -->
<img src="decorative-line.png" alt="">
```

### ❌ Bad: Image of Text Without the Text

```html
<!-- Missing the actual text from the image -->
<img src="welcome-banner.png" alt="Banner">  <!-- What does it say? -->
<img src="error-screenshot.png" alt="Error message">  <!-- What's the error? -->
<img src="company-logo.png" alt="Logo">  <!-- What company? -->
<img src="sale-graphic.png" alt="Promotional image">  <!-- What's the promotion? -->

<!-- Correct versions with actual text: -->
<img src="welcome-banner.png" alt="Welcome to Our Platform">
<img src="error-screenshot.png" alt="Error 404: Page not found">
<img src="company-logo.png" alt="TechCorp Solutions">
<img src="sale-graphic.png" alt="50% Off Everything - Sale Ends Sunday">
```

### ❌ Bad: Unknown Text Content - Needs Placeholder

```html
<!-- When you genuinely don't know what text is in the image -->
<img src="user-generated-screenshot.png" alt="Screenshot">  <!-- Wrong - too vague -->

<!-- Better - use placeholder and ask for help: -->
<img src="user-generated-screenshot.png" alt="Image of text, insert text here">
<!-- TODO: Ask user what text appears in this screenshot -->

<!-- Or ask the user directly in code review/PR -->
<img src="banner.png" alt="Image of text, insert text here">
<!-- @user What text appears in this banner image? -->
```

## Special Cases

### Images in Links or Buttons

**For links:** When an image is the only content in a link, the alt text should describe the **destination/action**:

```html
<!-- ✅ Good - Link with image -->
<a href="/home">
  <img src="logo.png" alt="Go to homepage">
</a>

<!-- ❌ Bad - Describes image, not destination -->
<a href="/home">
  <img src="logo.png" alt="Company logo">
</a>
```

**For buttons:** Use `aria-label` on the button, NOT alt on the image:

```html
<!-- ✅ Good - Button has aria-label, image has empty alt -->
<button aria-label="Close dialog">
  <img src="close-icon.svg" alt="">
</button>

<!-- ❌ Bad - Using image alt instead of button aria-label -->
<button>
  <img src="close-icon.svg" alt="Close dialog">
</button>

<!-- ✅ Good - Custom clickable div -->
<div role="button" tabindex="0" aria-label="Delete item" onclick="deleteItem()">
  <img src="trash-icon.png" alt="">
</div>
```

**See [buttons.instructions.md](buttons.instructions.md) for complete button accessibility guidelines.**

### Images with Adjacent Text

If text adjacent to the image conveys the same information, consider if the image is decorative:

```html
<!-- The text already says "Download", so icon is decorative -->
<a href="/download">
  <img src="download-icon.svg" alt="">
  Download Report
</a>
```

### Complex Images (Charts, Diagrams, Infographics)

For complex images, provide:
1. Short alt text summarizing the purpose
2. Long description either in the page content or linked separately

```html
<img 
  src="sales-chart.png" 
  alt="Annual sales data 2023-2024"
  aria-describedby="chart-description">
<div id="chart-description">
  Detailed description: Sales increased from $2M in Q1 2023 to $5M in Q4 2024...
</div>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.1.1**: Non-text Content (Level A)
- **WCAG 2.1 Success Criterion 1.4.5**: Images of Text (Level AA)

## Implementation Checklist

When generating code with images:
- [ ] **Does EVERY `<img>` have an `alt` attribute?** (CRITICAL - NEVER omit)
- [ ] **Does EVERY `<svg>` have an `aria-label` attribute?** (CRITICAL - NEVER omit)
- [ ] **If the image contains text, does the `alt` include that text?** (CRITICAL)
- [ ] **If image is inside a button/clickable element, does it use `alt=""`?** (CRITICAL)
- [ ] Are decorative images using `alt=""` (empty string)?
- [ ] Is the alt text descriptive and meaningful for content images?
- [ ] Are SVGs using `aria-label` with `role="img"`?
- [ ] Do image links describe the action, not just the image?
- [ ] For buttons with images, does the button have `aria-label`?
- [ ] Are background images either decorative or have accessible alternatives?
- [ ] Is the alt text concise (under 125 characters when possible)?

## Quick Reference

```
✅ ALWAYS:
- Include alt attribute on EVERY <img> element
- Include aria-label on EVERY <svg> element
- Include the actual text in alt when image contains text
- Use alt="" for decorative images (empty string, not omitted)
- Use alt="" for images inside buttons/clickable elements
- Use aria-label for SVG images (not alt)
- Be descriptive for content images
- Put aria-label on buttons with images, not on the images themselves

❌ NEVER:
- Omit alt attribute from <img> elements
- Omit aria-label from <svg> elements
- Use alt on SVG elements (use aria-label instead)
- Use vague descriptions like "image" or "photo"
- Describe an image of text without including the actual text
- Put alt text on images inside labeled buttons (use alt="" instead)

## Images of Text - Special Handling

When encountering an image that contains text:

1. ✅ **Know the text?** → Include it in the alt attribute
   ```html
   <img src="welcome.png" alt="Welcome to Our Site">
   ```

2. ❓ **Don't know the text?** → Follow this priority:
   - **First choice**: Ask the user what text is in the image
   - **Second choice**: Try OCR to extract the text
   - **Last resort**: Use placeholder and add TODO comment
   ```html
   <img src="banner.png" alt="Image of text, insert text here">
   <!-- TODO: Replace with actual text from the image -->
   ```
```
