# System Design - Scalable CSS Architecture

## CSS Naming Conventions

### BEM (Block Element Modifier)
```css
/* Block - standalone component */
.card { }

/* Element - part of block */
.card__header { }
.card__body { }
.card__footer { }

/* Modifier - variation of block or element */
.card--featured { }
.card--large { }
.card__header--dark { }

/* Example usage */
.button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.button__icon {
    margin-right: 0.5rem;
}

.button--primary {
    background: #007bff;
    color: white;
}

.button--secondary {
    background: #6c757d;
    color: white;
}

.button--large {
    padding: 1rem 2rem;
    font-size: 1.2rem;
}
```

### ITCSS (Inverted Triangle CSS)
```css
/* 1. Settings - global variables, config */
:root {
    --color-primary: #007bff;
    --spacing-unit: 1rem;
    --font-size-base: 16px;
}

/* 2. Tools - mixins, functions (in Sass/Less) */
/* @mixin button-style($bg-color) { ... } */

/* 3. Generic - normalize, reset, box-sizing */
*, *::before, *::after {
    box-sizing: border-box;
}

html {
    font-size: var(--font-size-base);
}

/* 4. Elements - bare HTML elements */
body {
    font-family: system-ui, sans-serif;
    line-height: 1.6;
    color: #333;
}

h1, h2, h3, h4, h5, h6 {
    margin-top: 0;
    margin-bottom: var(--spacing-unit);
}

/* 5. Objects - layout patterns, no cosmetics */
.o-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-unit);
}

.o-grid {
    display: grid;
    gap: var(--spacing-unit);
}

.o-stack > * + * {
    margin-top: var(--spacing-unit);
}

/* 6. Components - designed components */
.c-button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    background: var(--color-primary);
    color: white;
    cursor: pointer;
}

.c-card {
    background: white;
    border-radius: 8px;
    padding: var(--spacing-unit);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

/* 7. Utilities - single-purpose classes */
.u-text-center { text-align: center !important; }
.u-hidden { display: none !important; }
.u-visually-hidden { /* screen reader only styles */ }
```

### Utility-First (Tailwind Style)
```css
/* Spacing utilities */
.p-1 { padding: 0.25rem; }
.p-2 { padding: 0.5rem; }
.p-4 { padding: 1rem; }
.px-4 { padding-left: 1rem; padding-right: 1rem; }
.py-2 { padding-top: 0.5rem; padding-bottom: 0.5rem; }

.m-1 { margin: 0.25rem; }
.m-2 { margin: 0.5rem; }
.m-4 { margin: 1rem; }
.mx-auto { margin-left: auto; margin-right: auto; }
.mt-4 { margin-top: 1rem; }

/* Layout utilities */
.flex { display: flex; }
.grid { display: grid; }
.block { display: block; }
.inline { display: inline; }
.hidden { display: none; }

.justify-center { justify-content: center; }
.items-center { align-items: center; }
.flex-col { flex-direction: column; }

/* Typography utilities */
.text-sm { font-size: 0.875rem; }
.text-base { font-size: 1rem; }
.text-lg { font-size: 1.125rem; }
.text-xl { font-size: 1.25rem; }

.font-normal { font-weight: 400; }
.font-bold { font-weight: 700; }

.text-center { text-align: center; }
.text-left { text-align: left; }

/* Color utilities */
.text-gray-500 { color: #6b7280; }
.text-blue-600 { color: #2563eb; }
.bg-white { background-color: #ffffff; }
.bg-gray-100 { background-color: #f3f4f6; }
```

## Design Tokens

### CSS Custom Properties Implementation
```css
:root {
    /* Colors */
    --color-primary-50: #eff6ff;
    --color-primary-100: #dbeafe;
    --color-primary-500: #3b82f6;
    --color-primary-600: #2563eb;
    --color-primary-900: #1e3a8a;
    
    --color-gray-50: #f9fafb;
    --color-gray-100: #f3f4f6;
    --color-gray-500: #6b7280;
    --color-gray-900: #111827;
    
    --color-success: #10b981;
    --color-warning: #f59e0b;
    --color-error: #ef4444;
    
    /* Typography */
    --font-family-sans: system-ui, -apple-system, sans-serif;
    --font-family-mono: 'SF Mono', Monaco, monospace;
    
    --font-size-xs: 0.75rem;
    --font-size-sm: 0.875rem;
    --font-size-base: 1rem;
    --font-size-lg: 1.125rem;
    --font-size-xl: 1.25rem;
    --font-size-2xl: 1.5rem;
    --font-size-3xl: 1.875rem;
    
    --font-weight-normal: 400;
    --font-weight-medium: 500;
    --font-weight-semibold: 600;
    --font-weight-bold: 700;
    
    --line-height-tight: 1.25;
    --line-height-normal: 1.5;
    --line-height-relaxed: 1.75;
    
    /* Spacing */
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-6: 1.5rem;
    --space-8: 2rem;
    --space-12: 3rem;
    --space-16: 4rem;
    
    /* Shadows */
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
    
    /* Border radius */
    --radius-sm: 0.125rem;
    --radius-md: 0.375rem;
    --radius-lg: 0.5rem;
    --radius-xl: 0.75rem;
    --radius-full: 9999px;
    
    /* Breakpoints (for container queries) */
    --breakpoint-sm: 640px;
    --breakpoint-md: 768px;
    --breakpoint-lg: 1024px;
    --breakpoint-xl: 1280px;
}

/* Dark theme overrides */
[data-theme="dark"] {
    --color-primary-50: #1e3a8a;
    --color-primary-100: #1e40af;
    
    --color-gray-50: #111827;
    --color-gray-100: #1f2937;
    --color-gray-500: #9ca3af;
    --color-gray-900: #f9fafb;
}
```

### Component Using Design Tokens
```css
.button {
    /* Base styles */
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: var(--space-2) var(--space-4);
    font-family: var(--font-family-sans);
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-medium);
    line-height: var(--line-height-tight);
    border: 1px solid transparent;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: all 150ms ease;
    
    /* Primary variant */
    &.button--primary {
        background-color: var(--color-primary-500);
        color: white;
        
        &:hover {
            background-color: var(--color-primary-600);
        }
        
        &:focus {
            outline: 2px solid var(--color-primary-500);
            outline-offset: 2px;
        }
    }
    
    /* Size variants */
    &.button--sm {
        padding: var(--space-1) var(--space-3);
        font-size: var(--font-size-xs);
    }
    
    &.button--lg {
        padding: var(--space-3) var(--space-6);
        font-size: var(--font-size-base);
    }
}
```

## Theme System Implementation

### CSS-only Theme Switching
```css
/* Define themes */
:root {
    --bg-primary: #ffffff;
    --bg-secondary: #f8f9fa;
    --text-primary: #212529;
    --text-secondary: #6c757d;
    --border-color: #dee2e6;
}

[data-theme="dark"] {
    --bg-primary: #212529;
    --bg-secondary: #343a40;
    --text-primary: #f8f9fa;
    --text-secondary: #adb5bd;
    --border-color: #495057;
}

[data-theme="high-contrast"] {
    --bg-primary: #000000;
    --bg-secondary: #000000;
    --text-primary: #ffffff;
    --text-secondary: #ffffff;
    --border-color: #ffffff;
}

/* Use in components */
body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    transition: background-color 0.3s ease, color 0.3s ease;
}

.card {
    background-color: var(--bg-secondary);
    border: 1px solid var(--border-color);
    color: var(--text-primary);
}
```

### JavaScript Theme Toggle
```javascript
class ThemeManager {
    constructor() {
        this.currentTheme = localStorage.getItem('theme') || 'light';
        this.init();
    }
    
    init() {
        this.applyTheme(this.currentTheme);
        this.setupToggle();
        this.listenForSystemChanges();
    }
    
    applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('theme', theme);
        this.currentTheme = theme;
    }
    
    toggleTheme() {
        const newTheme = this.currentTheme === 'light' ? 'dark' : 'light';
        this.applyTheme(newTheme);
    }
    
    setupToggle() {
        const toggleBtn = document.querySelector('[data-theme-toggle]');
        if (toggleBtn) {
            toggleBtn.addEventListener('click', () => this.toggleTheme());
        }
    }
    
    listenForSystemChanges() {
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        mediaQuery.addEventListener('change', (e) => {
            if (!localStorage.getItem('theme')) {
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
}

// Initialize theme manager
new ThemeManager();
```

## CSS Architecture Strategies

### CSS Modules Approach
```css
/* Button.module.css */
.button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.primary {
    background: #007bff;
    color: white;
}

.secondary {
    background: #6c757d;
    color: white;
}
```

```javascript
// Button.js
import styles from './Button.module.css';

function Button({ variant = 'primary', children, ...props }) {
    return (
        <button 
            className={`${styles.button} ${styles[variant]}`}
            {...props}
        >
            {children}
        </button>
    );
}
```

### CSS-in-JS Pattern
```javascript
// Styled-components example
import styled, { css } from 'styled-components';

const Button = styled.button`
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 1rem;
    transition: all 0.2s ease;
    
    ${props => props.variant === 'primary' && css`
        background: #007bff;
        color: white;
        
        &:hover {
            background: #0056b3;
        }
    `}
    
    ${props => props.variant === 'secondary' && css`
        background: #6c757d;
        color: white;
        
        &:hover {
            background: #545b62;
        }
    `}
    
    ${props => props.size === 'large' && css`
        padding: 1rem 2rem;
        font-size: 1.2rem;
    `}
`;

// Usage
<Button variant="primary" size="large">
    Click me
</Button>
```

### Component-Based Architecture
```css
/* components/Button/Button.css */
.button {
    /* Base button styles */
}

.button--primary {
    /* Primary variant */
}

.button--secondary {
    /* Secondary variant */
}

/* components/Card/Card.css */
.card {
    /* Base card styles */
}

.card__header {
    /* Card header */
}

.card__body {
    /* Card body */
}

/* layouts/Grid/Grid.css */
.grid {
    /* Grid layout */
}

.grid__item {
    /* Grid item */
}
```

## Performance and Maintenance

### CSS Optimization Strategies
```css
/* 1. Avoid deep nesting */
/* Bad */
.nav .menu .item .link .icon { }

/* Good */
.nav-link-icon { }

/* 2. Use efficient selectors */
/* Bad - slow */
* { }
[type="text"] { }
.class-name * { }

/* Good - fast */
.class-name { }
#id-name { }

/* 3. Minimize specificity conflicts */
/* Use consistent specificity levels */
.button { } /* 0-0-1-0 */
.button--primary { } /* 0-0-1-0 */
.button--large { } /* 0-0-1-0 */

/* 4. Group related properties */
.element {
    /* Positioning */
    position: relative;
    top: 0;
    left: 0;
    
    /* Box model */
    display: block;
    width: 100%;
    height: auto;
    padding: 1rem;
    margin: 0;
    
    /* Typography */
    font-family: sans-serif;
    font-size: 1rem;
    line-height: 1.5;
    
    /* Visual */
    background: white;
    border: 1px solid #ddd;
    border-radius: 4px;
    
    /* Misc */
    cursor: pointer;
    transition: all 0.3s ease;
}
```

### CSS Linting Configuration
```json
// .stylelintrc.json
{
    "extends": ["stylelint-config-standard"],
    "rules": {
        "max-nesting-depth": 3,
        "selector-max-compound-selectors": 4,
        "selector-max-specificity": "0,4,0",
        "declaration-block-no-duplicate-properties": true,
        "color-no-invalid-hex": true,
        "font-family-no-duplicate-names": true,
        "function-calc-no-invalid": true,
        "property-no-unknown": true,
        "selector-pseudo-class-no-unknown": true,
        "selector-pseudo-element-no-unknown": true,
        "unit-no-unknown": true
    }
}
```

## Common Interview Questions

### 1. How would you design a theme system (light/dark mode)?
- Use CSS custom properties for theme variables
- Implement data attributes for theme switching
- Consider system preferences with `prefers-color-scheme`
- Provide smooth transitions between themes
- Store user preference in localStorage

### 2. How to structure CSS for a large multi-team project?
- Use consistent naming convention (BEM or similar)
- Implement design token system
- Create component library with clear documentation
- Use CSS layers for predictable cascade
- Establish linting rules and code standards
- Consider CSS-in-JS for component isolation

### 3. Difference between CSS-in-JS and traditional CSS?
- **CSS-in-JS**: Component-scoped, dynamic styling, JavaScript integration, runtime overhead
- **Traditional CSS**: Global scope, static styling, build-time optimization, potential naming conflicts
- **Hybrid**: CSS Modules provide scoping with traditional CSS performance

### 4. How to prevent CSS specificity wars?
- Use consistent specificity levels
- Avoid deep nesting
- Use CSS layers for organization
- Implement utility-first approach
- Use CSS custom properties for theming
- Establish naming conventions

### 5. How would you implement a scalable color system?
```css
:root {
    /* Base colors */
    --blue-50: #eff6ff;
    --blue-500: #3b82f6;
    --blue-900: #1e3a8a;
    
    /* Semantic colors */
    --color-primary: var(--blue-500);
    --color-text: var(--gray-900);
    --color-background: var(--gray-50);
    
    /* Component-specific */
    --button-bg: var(--color-primary);
    --button-text: white;
}
```
