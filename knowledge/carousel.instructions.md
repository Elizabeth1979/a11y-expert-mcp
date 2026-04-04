---
description: Instructions for proper carousel accessibility following WAI-ARIA APG patterns
applyTo: '**/*.{html,jsx,tsx,vue,svelte}'
---

# Carousel (Slideshow) Accessibility

## CRITICAL RULES

**Carousels display a rotating sequence of content slides. They must be keyboard accessible, provide rotation controls, and announce slide changes.**

### 1. Use role="group" or role="region" with aria-roledescription="carousel"

**Carousel containers MUST use `role="group"` or `role="region"` with `aria-roledescription="carousel"`.**

```html
✅ Good - Carousel with proper roles:
<div
  role="region"
  aria-roledescription="carousel"
  aria-label="Featured products">
  <div role="group" aria-roledescription="slide" aria-label="1 of 5">
    <!-- Slide content -->
  </div>
</div>

❌ Bad - Missing aria-roledescription:
<div role="region" aria-label="Products">
  <!-- Missing aria-roledescription="carousel"! -->
  <div>Slide content</div>
</div>
```

### 2. Slides Must Have role="group" with aria-roledescription="slide"

**Each slide MUST use `role="group"` with `aria-roledescription="slide"` and accessible name.**

```html
✅ Good - Proper slide structure:
<div
  role="group"
  aria-roledescription="slide"
  aria-label="1 of 5">
  <img src="product1.jpg" alt="Product 1">
  <h3>Product 1</h3>
  <p>Description...</p>
</div>

<div
  role="group"
  aria-roledescription="slide"
  aria-label="2 of 5">
  <img src="product2.jpg" alt="Product 2">
  <h3>Product 2</h3>
</div>

❌ Bad - Slides without proper roles:
<div class="slide">
  <!-- Missing role="group" and aria-roledescription! -->
  <img src="product1.jpg" alt="Product 1">
</div>
```

### 3. Provide Previous/Next Navigation Buttons

**Carousels MUST have accessible previous and next buttons.**

```html
✅ Good - Navigation buttons:
<button aria-label="Previous slide">
  <svg aria-hidden="true"><!-- left arrow icon --></svg>
</button>

<button aria-label="Next slide">
  <svg aria-hidden="true"><!-- right arrow icon --></svg>
</button>

❌ Bad - Buttons without accessible names:
<button>
  <svg><!-- left arrow --></svg>  <!-- No aria-label! -->
</button>
```

### 4. Auto-Rotation MUST Pause on Hover, Focus, and User Action

**If carousel auto-rotates, it MUST pause on hover, keyboard focus, and provide stop/start control.**

```html
✅ Good - Rotation control button:
<button aria-label="Stop automatic slide rotation" id="rotation-btn">
  <svg aria-hidden="true"><!-- pause icon --></svg>
</button>

<script>
let isRotating = true;
const rotationBtn = document.getElementById('rotation-btn');

rotationBtn.addEventListener('click', () => {
  isRotating = !isRotating;

  if (isRotating) {
    rotationBtn.setAttribute('aria-label', 'Stop automatic slide rotation');
    startRotation();
  } else {
    rotationBtn.setAttribute('aria-label', 'Start automatic slide rotation');
    stopRotation();
  }
});

carousel.addEventListener('mouseenter', stopRotation);
carousel.addEventListener('mouseleave', () => {
  if (isRotating) startRotation();
});

carousel.addEventListener('focusin', stopRotation);
carousel.addEventListener('focusout', () => {
  if (isRotating) startRotation();
});
</script>

❌ Bad - Auto-rotation without pause:
<script>
setInterval(nextSlide, 3000); // Can't be stopped!
</script>
```

**WCAG 2.2.2**: Auto-rotating content must be pausable.

### 5. Rotation Control Must Be First Focusable Element

**If carousel has auto-rotation, the stop/start button SHOULD be the first focusable element.**

```html
✅ Good - Rotation control first:
<div role="region" aria-roledescription="carousel" aria-label="Products">
  <!-- Rotation control is first -->
  <button aria-label="Stop automatic slide rotation">Pause</button>

  <div role="group" aria-roledescription="slide" aria-label="1 of 3">
    <img src="slide1.jpg" alt="...">
  </div>

  <button aria-label="Previous slide">Previous</button>
  <button aria-label="Next slide">Next</button>
</div>
```

## Complete Carousel Structure

```html
<div
  id="carousel"
  role="region"
  aria-roledescription="carousel"
  aria-label="Featured products"
  class="carousel">

  <!-- Rotation control (first focusable element) -->
  <button
    id="rotation-control"
    aria-label="Stop automatic slide rotation">
    <span id="rotation-icon" aria-hidden="true">⏸</span>
  </button>

  <!-- Slides container -->
  <div class="slides-container">
    <div
      class="slide active"
      role="group"
      aria-roledescription="slide"
      aria-label="1 of 3"
      id="slide-1">
      <img src="product1.jpg" alt="Product 1">
      <h3>Product 1</h3>
      <p>Amazing features...</p>
      <a href="/product/1">Learn More</a>
    </div>

    <div
      class="slide"
      role="group"
      aria-roledescription="slide"
      aria-label="2 of 3"
      id="slide-2"
      hidden>
      <img src="product2.jpg" alt="Product 2">
      <h3>Product 2</h3>
      <p>Excellent quality...</p>
      <a href="/product/2">Learn More</a>
    </div>

    <div
      class="slide"
      role="group"
      aria-roledescription="slide"
      aria-label="3 of 3"
      id="slide-3"
      hidden>
      <img src="product3.jpg" alt="Product 3">
      <h3>Product 3</h3>
      <p>Best value...</p>
      <a href="/product/3">Learn More</a>
    </div>
  </div>

  <!-- Navigation buttons -->
  <button id="prev-btn" aria-label="Previous slide">
    <span aria-hidden="true">‹</span>
  </button>

  <button id="next-btn" aria-label="Next slide">
    <span aria-hidden="true">›</span>
  </button>

  <!-- Slide indicators (optional) -->
  <div class="slide-indicators" role="group" aria-label="Slide controls">
    <button aria-label="Go to slide 1" aria-current="true">1</button>
    <button aria-label="Go to slide 2">2</button>
    <button aria-label="Go to slide 3">3</button>
  </div>

  <!-- Live region for announcements (optional) -->
  <div aria-live="polite" aria-atomic="false" class="sr-only"></div>
</div>

<script>
const carousel = document.getElementById('carousel');
const slides = carousel.querySelectorAll('.slide');
const prevBtn = document.getElementById('prev-btn');
const nextBtn = document.getElementById('next-btn');
const rotationControl = document.getElementById('rotation-control');
const rotationIcon = document.getElementById('rotation-icon');
const indicators = carousel.querySelectorAll('.slide-indicators button');

let currentSlide = 0;
let isRotating = true;
let rotationInterval = null;

// Initialize
showSlide(currentSlide);
if (isRotating) startRotation();

// Event listeners
prevBtn.addEventListener('click', () => {
  showSlide(currentSlide - 1);
});

nextBtn.addEventListener('click', () => {
  showSlide(currentSlide + 1);
});

rotationControl.addEventListener('click', toggleRotation);

indicators.forEach((indicator, index) => {
  indicator.addEventListener('click', () => showSlide(index));
});

// Pause on hover
carousel.addEventListener('mouseenter', () => {
  if (isRotating) stopRotation();
});

carousel.addEventListener('mouseleave', () => {
  if (isRotating) startRotation();
});

// Pause on focus
carousel.addEventListener('focusin', () => {
  if (isRotating) stopRotation();
});

carousel.addEventListener('focusout', (e) => {
  if (isRotating && !carousel.contains(e.relatedTarget)) {
    startRotation();
  }
});

function showSlide(index) {
  // Wrap around
  if (index >= slides.length) index = 0;
  if (index < 0) index = slides.length - 1;

  // Hide all slides
  slides.forEach(slide => {
    slide.hidden = true;
    slide.classList.remove('active');
  });

  // Show current slide
  slides[index].hidden = false;
  slides[index].classList.add('active');
  currentSlide = index;

  // Update indicators
  indicators.forEach((indicator, i) => {
    if (i === index) {
      indicator.setAttribute('aria-current', 'true');
    } else {
      indicator.removeAttribute('aria-current');
    }
  });
}

function startRotation() {
  rotationInterval = setInterval(() => {
    showSlide(currentSlide + 1);
  }, 5000); // 5 seconds
}

function stopRotation() {
  clearInterval(rotationInterval);
}

function toggleRotation() {
  isRotating = !isRotating;

  if (isRotating) {
    rotationControl.setAttribute('aria-label', 'Stop automatic slide rotation');
    rotationIcon.textContent = '⏸';
    startRotation();
  } else {
    rotationControl.setAttribute('aria-label', 'Start automatic slide rotation');
    rotationIcon.textContent = '▶';
    stopRotation();
  }
}
</script>
```

## Examples

### ✅ Good: Simple Image Carousel

```html
<div
  role="region"
  aria-roledescription="carousel"
  aria-label="Image gallery">

  <button aria-label="Stop automatic slide rotation">Pause</button>

  <div
    role="group"
    aria-roledescription="slide"
    aria-label="1 of 4">
    <img src="image1.jpg" alt="Mountain landscape">
  </div>

  <button aria-label="Previous slide">Previous</button>
  <button aria-label="Next slide">Next</button>
</div>
```

### ✅ Good: React Carousel Component

```jsx
function Carousel({ slides, autoRotate = true, interval = 5000 }) {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(autoRotate);
  const carouselRef = useRef(null);
  const intervalRef = useRef(null);

  useEffect(() => {
    if (isPlaying) {
      intervalRef.current = setInterval(() => {
        setCurrentIndex((prev) => (prev + 1) % slides.length);
      }, interval);
    }

    return () => clearInterval(intervalRef.current);
  }, [isPlaying, slides.length, interval]);

  const handlePause = () => {
    setIsPlaying(false);
    clearInterval(intervalRef.current);
  };

  const handlePlay = () => {
    setIsPlaying(true);
  };

  const goToSlide = (index) => {
    setCurrentIndex(index);
  };

  const nextSlide = () => {
    setCurrentIndex((prev) => (prev + 1) % slides.length);
  };

  const prevSlide = () => {
    setCurrentIndex((prev) => (prev - 1 + slides.length) % slides.length);
  };

  return (
    <div
      ref={carouselRef}
      role="region"
      aria-roledescription="carousel"
      aria-label="Featured content"
      onMouseEnter={handlePause}
      onMouseLeave={isPlaying ? handlePlay : undefined}
      onFocus={handlePause}
      onBlur={isPlaying ? handlePlay : undefined}>

      {autoRotate && (
        <button
          onClick={() => isPlaying ? handlePause() : handlePlay()}
          aria-label={
            isPlaying
              ? 'Stop automatic slide rotation'
              : 'Start automatic slide rotation'
          }>
          {isPlaying ? '⏸' : '▶'}
        </button>
      )}

      {slides.map((slide, index) => (
        <div
          key={index}
          role="group"
          aria-roledescription="slide"
          aria-label={`${index + 1} of ${slides.length}`}
          hidden={index !== currentIndex}>
          {slide.content}
        </div>
      ))}

      <button onClick={prevSlide} aria-label="Previous slide">
        ‹
      </button>

      <button onClick={nextSlide} aria-label="Next slide">
        ›
      </button>

      <div role="group" aria-label="Slide controls">
        {slides.map((_, index) => (
          <button
            key={index}
            onClick={() => goToSlide(index)}
            aria-label={`Go to slide ${index + 1}`}
            aria-current={index === currentIndex ? 'true' : undefined}>
            {index + 1}
          </button>
        ))}
      </div>
    </div>
  );
}

// Usage
<Carousel
  slides={[
    { content: <img src="slide1.jpg" alt="Slide 1" /> },
    { content: <img src="slide2.jpg" alt="Slide 2" /> },
    { content: <img src="slide3.jpg" alt="Slide 3" /> }
  ]}
  autoRotate={true}
  interval={5000}
/>
```

### ❌ Bad Examples

```html
<!-- Missing carousel roles -->
<div class="carousel">
  <!-- Missing role and aria-roledescription! -->
  <div class="slide">
    <img src="slide1.jpg" alt="Slide 1">
  </div>
</div>

<!-- Auto-rotation without pause controls -->
<div role="region" aria-roledescription="carousel" aria-label="Products">
  <div role="group" aria-roledescription="slide" aria-label="1 of 3">
    <img src="product1.jpg" alt="Product 1">
  </div>
  <!-- Auto-rotates but no pause button! FAILS WCAG 2.2.2 -->
</div>

<!-- Buttons without accessible names -->
<button>
  <img src="prev.png">  <!-- No alt text or aria-label! -->
</button>

<!-- Doesn't pause on hover/focus -->
<div role="region" aria-roledescription="carousel">
  <!-- Auto-rotates but doesn't pause on hover/focus! -->
</div>
```

## WCAG References

- **WCAG 2.1 Success Criterion 1.3.1**: Info and Relationships (Level A)
- **WCAG 2.1 Success Criterion 2.1.1**: Keyboard (Level A)
- **WCAG 2.1 Success Criterion 2.2.2**: Pause, Stop, Hide (Level A) - Auto-rotation must be pausable
- **WCAG 2.1 Success Criterion 4.1.2**: Name, Role, Value (Level A)

## Implementation Checklist

- [ ] **Does container have `role="region"` or `role="group"`?** (CRITICAL)
- [ ] **Does container have `aria-roledescription="carousel"`?** (CRITICAL)
- [ ] **Does container have accessible label?** (CRITICAL)
- [ ] **Do slides have `role="group"`?** (CRITICAL)
- [ ] **Do slides have `aria-roledescription="slide"`?** (CRITICAL)
- [ ] **Do slides have accessible names (e.g., "1 of 5")?** (CRITICAL)
- [ ] **Are previous/next buttons accessible?** (CRITICAL)
- [ ] If auto-rotating, is there a pause/play button? (CRITICAL)
- [ ] If auto-rotating, does rotation pause on hover? (CRITICAL)
- [ ] If auto-rotating, does rotation pause on focus? (CRITICAL)
- [ ] Is rotation control the first focusable element?
- [ ] Do navigation buttons have proper labels?
- [ ] Are slide indicators accessible (if present)?
- [ ] Does Tab key move through interactive elements properly?

## Quick Reference

```
✅ DO:
- Use role="region" with aria-roledescription="carousel"
- Use role="group" with aria-roledescription="slide" for slides
- Provide accessible labels for carousel and slides
- Include previous/next navigation buttons
- Provide pause/play button if auto-rotating
- Pause rotation on hover and keyboard focus
- Make rotation control first focusable element
- Use aria-label for navigation buttons
- Update slide labels with position (e.g., "2 of 5")
- Hide inactive slides with hidden attribute

❌ DON'T:
- Auto-rotate without pause control (FAILS WCAG 2.2.2)
- Forget to pause on hover/focus
- Use images for buttons without alt text or aria-label
- Forget aria-roledescription attributes
- Make carousel inaccessible to keyboard users
- Rotate too fast (minimum 5 seconds recommended)
- Omit slide position information
- Use complex gestures as only interaction method

## Auto-Rotation Requirements (WCAG 2.2.2):

If carousel auto-rotates, you MUST:
  ✓ Provide pause/play button
  ✓ Pause on mouse hover
  ✓ Pause on keyboard focus
  ✓ Make pause button first focusable element
  ✓ Update button label when toggling (Stop/Start)
  ✓ Allow at least 5 seconds per slide
```
