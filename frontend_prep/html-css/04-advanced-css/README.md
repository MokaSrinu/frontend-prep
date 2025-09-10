# Advanced CSS

## CSS Variables (Custom Properties)

### Defining and Using Variables
```css
/* Global variables in :root */
:root {
    --primary-color: #3498db;
    --secondary-color: #2ecc71;
    --font-size-base: 16px;
    --spacing-unit: 1rem;
    --border-radius: 4px;
    --shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* Using variables */
.button {
    background-color: var(--primary-color);
    font-size: var(--font-size-base);
    padding: var(--spacing-unit);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow);
}

/* Fallback values */
.element {
    color: var(--text-color, #333); /* Use #333 if --text-color not defined */
}

/* Local scope variables */
.theme-dark {
    --primary-color: #1e3a8a;
    --text-color: #ffffff;
}
```

### Dynamic Variables with JavaScript
```css
/* CSS */
.dynamic-element {
    transform: translateX(var(--x, 0px));
    opacity: var(--opacity, 1);
}
```

```javascript
// JavaScript
const element = document.querySelector('.dynamic-element');
element.style.setProperty('--x', '100px');
element.style.setProperty('--opacity', '0.5');
```

## CSS Layers

### Layer Declaration and Usage
```css
/* Declare layers in order */
@layer reset, base, components, utilities;

/* Reset layer */
@layer reset {
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
}

/* Base layer */
@layer base {
    body {
        font-family: system-ui, sans-serif;
        line-height: 1.6;
    }
    
    h1, h2, h3 {
        margin-bottom: 1rem;
    }
}

/* Components layer */
@layer components {
    .button {
        padding: 0.5rem 1rem;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    
    .card {
        background: white;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
}

/* Utilities layer (highest priority) */
@layer utilities {
    .text-center { text-align: center !important; }
    .hidden { display: none !important; }
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
    }
}
```

## Animations and Transitions

### CSS Transitions
```css
.element {
    /* Basic transition */
    transition: all 0.3s ease;
    
    /* Specific properties */
    transition: opacity 0.3s ease, transform 0.3s ease-out;
    
    /* Different timing functions */
    transition-timing-function: ease | ease-in | ease-out | ease-in-out | linear;
    transition-timing-function: cubic-bezier(0.25, 0.1, 0.25, 1);
    
    /* Delay */
    transition-delay: 0.1s;
}

/* Hover effects */
.button {
    background-color: #3498db;
    transform: translateY(0);
    transition: all 0.2s ease;
}

.button:hover {
    background-color: #2980b9;
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(52, 152, 219, 0.3);
}
```

### CSS Keyframe Animations
```css
/* Define keyframes */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes pulse {
    0%, 100% {
        transform: scale(1);
    }
    50% {
        transform: scale(1.05);
    }
}

@keyframes slideIn {
    0% {
        transform: translateX(-100%);
    }
    50% {
        transform: translateX(10px);
    }
    100% {
        transform: translateX(0);
    }
}

/* Apply animations */
.fade-in {
    animation: fadeIn 0.6s ease-out;
}

.loading-button {
    animation: pulse 2s infinite;
}

.slide-in {
    animation: slideIn 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Animation properties */
.complex-animation {
    animation-name: fadeIn;
    animation-duration: 1s;
    animation-timing-function: ease-out;
    animation-delay: 0.2s;
    animation-iteration-count: infinite;
    animation-direction: alternate;
    animation-fill-mode: forwards;
    animation-play-state: running;
    
    /* Shorthand */
    animation: fadeIn 1s ease-out 0.2s infinite alternate forwards;
}
```

### Performance Optimization
```css
/* Optimize for animations */
.animated-element {
    will-change: transform, opacity;
    /* Remove will-change after animation completes */
}

/* Use transform and opacity for best performance */
.performant-animation {
    transform: translateX(100px) scale(1.2);
    opacity: 0.8;
    transition: transform 0.3s ease, opacity 0.3s ease;
}

/* Avoid animating these properties */
.avoid-animating {
    /* Don't animate these - they trigger layout/paint */
    /* width, height, top, left, margin, padding */
}
```

## Advanced Pseudo-elements

### Creative Uses
```css
/* Tooltips */
.tooltip {
    position: relative;
}

.tooltip::before {
    content: attr(data-tooltip);
    position: absolute;
    bottom: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: #333;
    color: white;
    padding: 0.5rem;
    border-radius: 4px;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s;
}

.tooltip:hover::before {
    opacity: 1;
}

/* Custom checkbox */
.custom-checkbox {
    position: relative;
    display: inline-block;
}

.custom-checkbox input {
    opacity: 0;
    position: absolute;
}

.custom-checkbox::before {
    content: '';
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 2px solid #ddd;
    border-radius: 3px;
    margin-right: 8px;
    vertical-align: middle;
    transition: all 0.3s;
}

.custom-checkbox input:checked + ::before {
    background: #3498db;
    border-color: #3498db;
}

.custom-checkbox input:checked + ::after {
    content: '✓';
    position: absolute;
    left: 6px;
    top: 2px;
    color: white;
    font-size: 14px;
}

/* Loading spinner */
.spinner::before {
    content: '';
    display: inline-block;
    width: 20px;
    height: 20px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
```

## Accessibility in CSS

### Accessible Focus States
```css
/* Enhanced focus indicators */
.button:focus-visible {
    outline: 2px solid #3498db;
    outline-offset: 2px;
}

/* Skip to main content link */
.skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    background: #000;
    color: white;
    padding: 8px;
    text-decoration: none;
    z-index: 1000;
    transition: top 0.3s;
}

.skip-link:focus {
    top: 6px;
}

/* Screen reader only content */
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
}
```

### Responsive to User Preferences
```css
/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
    *,
    *::before,
    *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    :root {
        --bg-color: #1a1a1a;
        --text-color: #ffffff;
        --border-color: #333;
    }
}

/* High contrast mode */
@media (prefers-contrast: high) {
    .button {
        border: 2px solid;
    }
}

/* Reduced transparency */
@media (prefers-reduced-transparency: reduce) {
    .translucent {
        opacity: 1;
        background: solid-color;
    }
}
```

## Performance Optimization

### Content Visibility
```css
/* Improve rendering performance */
.long-content {
    content-visibility: auto;
    contain-intrinsic-size: 1000px; /* Estimated height */
}

/* Skip rendering off-screen content */
.off-screen {
    content-visibility: hidden;
}
```

### Critical CSS Strategy
```css
/* Inline critical CSS in <head> */
/* Above-the-fold styles */
body {
    font-family: system-ui, sans-serif;
    margin: 0;
}

.header {
    background: #fff;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Load non-critical CSS asynchronously */
```

### Font Loading Strategies
```css
/* Font display strategies */
@font-face {
    font-family: 'CustomFont';
    src: url('font.woff2') format('woff2');
    font-display: swap; /* Show fallback immediately, swap when loaded */
}

/* Preload important fonts */
/* <link rel="preload" href="font.woff2" as="font" type="font/woff2" crossorigin> */

/* Font loading classes */
.font-loading {
    font-family: system-ui, sans-serif;
}

.font-loaded {
    font-family: 'CustomFont', system-ui, sans-serif;
}
```

## Common Interview Questions

### 1. Difference between `display: none` vs `visibility: hidden`?
- **`display: none`**: Removes element from document flow, no space taken, affects layout
- **`visibility: hidden`**: Hides element but preserves space, doesn't affect layout

### 2. What triggers a new stacking context?
- Elements with `position: fixed` or `position: sticky`
- Elements with `position: absolute/relative` and `z-index` other than `auto`
- Elements with `opacity` less than 1
- Elements with `transform`, `filter`, `perspective` properties
- Flex/grid items with `z-index`
- Elements with `will-change` property

### 3. How does `content-visibility: auto` improve performance?
- Allows browser to skip rendering work for off-screen content
- Reduces layout, paint, and composite operations
- Improves initial page load and scroll performance
- Browser can skip style recalculation for hidden content

### 4. When to use CSS animations vs JavaScript animations?
- **CSS**: Simple animations, hover effects, loading spinners, better performance for transform/opacity
- **JavaScript**: Complex logic, dynamic values, precise timing control, animation sequences

### 5. How to implement a performant dark mode?
```css
:root {
    --bg: #ffffff;
    --text: #000000;
}

[data-theme="dark"] {
    --bg: #1a1a1a;
    --text: #ffffff;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg: #1a1a1a;
        --text: #ffffff;
    }
}

body {
    background: var(--bg);
    color: var(--text);
    transition: background-color 0.3s ease, color 0.3s ease;
}
```
