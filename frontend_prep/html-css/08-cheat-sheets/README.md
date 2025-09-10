# Cheat Sheets - Quick Reference Guides

## CSS Specificity Ladder

### Specificity Calculation
```
!important     = Override everything (use sparingly)
Inline Style   = 1000 points
ID             = 100 points  
Class          = 10 points
Attribute      = 10 points
Pseudo-class   = 10 points
Element        = 1 point
Pseudo-element = 1 point
Universal (*)  = 0 points
```

### Examples
```css
/* 0001 */ p
/* 0010 */ .class
/* 0100 */ #id
/* 1000 */ style="color: red"
/* 0011 */ p.class
/* 0101 */ #id p
/* 0111 */ #id p.class
/* 0021 */ p.class:hover
```

## Flexbox Cheatsheet

### Container Properties
```css
.flex-container {
    display: flex | inline-flex;
    
    /* Main axis direction */
    flex-direction: row | row-reverse | column | column-reverse;
    
    /* Wrap items */
    flex-wrap: nowrap | wrap | wrap-reverse;
    
    /* Shorthand: direction + wrap */
    flex-flow: row wrap;
    
    /* Main axis alignment */
    justify-content: 
        flex-start | flex-end | center | 
        space-between | space-around | space-evenly;
    
    /* Cross axis alignment */
    align-items: 
        stretch | flex-start | flex-end | center | baseline;
    
    /* Wrapped lines alignment */
    align-content: 
        stretch | flex-start | flex-end | center |
        space-between | space-around | space-evenly;
    
    /* Gap between items */
    gap: 1rem;
    row-gap: 1rem;
    column-gap: 1rem;
}
```

### Item Properties
```css
.flex-item {
    /* Growth factor (how much to grow) */
    flex-grow: 0; /* default */
    
    /* Shrink factor (how much to shrink) */
    flex-shrink: 1; /* default */
    
    /* Base size before growing/shrinking */
    flex-basis: auto; /* default */
    
    /* Shorthand: grow shrink basis */
    flex: none; /* 0 0 auto */
    flex: auto; /* 1 1 auto */
    flex: 1;    /* 1 1 0% */
    flex: 2;    /* 2 1 0% */
    
    /* Override container's align-items */
    align-self: auto | flex-start | flex-end | center | baseline | stretch;
    
    /* Visual order */
    order: 0; /* default */
}
```

### Common Patterns
```css
/* Center content */
.center { display: flex; justify-content: center; align-items: center; }

/* Equal columns */
.equal-cols > * { flex: 1; }

/* Sidebar layout */
.sidebar { flex: 0 0 250px; }
.main { flex: 1; }

/* Push to edges */
.space-between { justify-content: space-between; }
.push-right { margin-left: auto; }
```

## CSS Grid Cheatsheet

### Container Properties
```css
.grid-container {
    display: grid | inline-grid;
    
    /* Define columns */
    grid-template-columns: 
        200px 1fr 200px |
        repeat(3, 1fr) |
        repeat(auto-fit, minmax(250px, 1fr));
    
    /* Define rows */
    grid-template-rows: 
        auto 1fr auto |
        repeat(3, 100px);
    
    /* Named areas */
    grid-template-areas: 
        "header header"
        "sidebar main"
        "footer footer";
    
    /* Gaps */
    gap: 1rem;
    row-gap: 1rem;
    column-gap: 1rem;
    
    /* Align items in cells */
    justify-items: start | end | center | stretch;
    align-items: start | end | center | stretch;
    place-items: center; /* shorthand */
    
    /* Align grid in container */
    justify-content: start | end | center | stretch | space-around | space-between | space-evenly;
    align-content: start | end | center | stretch | space-around | space-between | space-evenly;
    place-content: center; /* shorthand */
}
```

### Item Properties
```css
.grid-item {
    /* Position by line numbers */
    grid-column-start: 1;
    grid-column-end: 3;
    grid-row-start: 1;
    grid-row-end: 2;
    
    /* Shorthand */
    grid-column: 1 / 3; /* start / end */
    grid-row: 1 / 2;
    grid-area: 1 / 1 / 2 / 3; /* row-start / col-start / row-end / col-end */
    
    /* Span syntax */
    grid-column: span 2;
    grid-row: span 3;
    
    /* Named areas */
    grid-area: header;
    
    /* Align within cell */
    justify-self: start | end | center | stretch;
    align-self: start | end | center | stretch;
    place-self: center; /* shorthand */
}
```

### Grid Functions
```css
/* repeat() */
grid-template-columns: repeat(12, 1fr);
grid-template-columns: repeat(auto-fit, 200px);
grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));

/* minmax() */
grid-template-columns: minmax(200px, 1fr) 300px;

/* fit-content() */
grid-template-columns: fit-content(300px) 1fr;

/* fr unit (fractional) */
grid-template-columns: 1fr 2fr 1fr; /* 1:2:1 ratio */
```

## Media Query Breakpoints

### Standard Breakpoints
```css
/* Mobile First Approach */
/* Extra small devices (phones, 600px and down) */
@media only screen and (max-width: 600px) { }

/* Small devices (portrait tablets and large phones, 600px and up) */
@media only screen and (min-width: 600px) { }

/* Medium devices (landscape tablets, 768px and up) */
@media only screen and (min-width: 768px) { }

/* Large devices (laptops/desktops, 992px and up) */
@media only screen and (min-width: 992px) { }

/* Extra large devices (large laptops and desktops, 1200px and up) */
@media only screen and (min-width: 1200px) { }

/* Common Framework Breakpoints */
/* Bootstrap */
@media (min-width: 576px) { } /* sm */
@media (min-width: 768px) { } /* md */
@media (min-width: 992px) { } /* lg */
@media (min-width: 1200px) { } /* xl */
@media (min-width: 1400px) { } /* xxl */

/* Tailwind CSS */
@media (min-width: 640px) { } /* sm */
@media (min-width: 768px) { } /* md */
@media (min-width: 1024px) { } /* lg */
@media (min-width: 1280px) { } /* xl */
@media (min-width: 1536px) { } /* 2xl */
```

### Media Query Types
```css
/* Orientation */
@media (orientation: landscape) { }
@media (orientation: portrait) { }

/* Resolution */
@media (min-resolution: 2dppx) { } /* High DPI */
@media (-webkit-min-device-pixel-ratio: 2) { } /* WebKit */

/* Accessibility */
@media (prefers-reduced-motion: reduce) { }
@media (prefers-color-scheme: dark) { }
@media (prefers-contrast: high) { }

/* Print */
@media print { }

/* Hover capability */
@media (hover: hover) { } /* Can hover */
@media (hover: none) { } /* Touch device */
```

## CSS Units Reference

### Absolute Units
```css
px    /* Pixels (1px = 1/96th of 1in) */
pt    /* Points (1pt = 1/72th of 1in) */
pc    /* Picas (1pc = 12pt) */
in    /* Inches */
cm    /* Centimeters */
mm    /* Millimeters */
```

### Relative Units
```css
%     /* Percentage of parent */
em    /* Relative to parent font-size */
rem   /* Relative to root font-size */
ex    /* Height of lowercase 'x' */
ch    /* Width of '0' character */

/* Viewport units */
vw    /* 1% of viewport width */
vh    /* 1% of viewport height */
vmin  /* 1% of viewport's smaller dimension */
vmax  /* 1% of viewport's larger dimension */

/* Logical units (CSS Logical Properties) */
vi    /* 1% of viewport inline size */
vb    /* 1% of viewport block size */

/* Container query units */
cqw   /* 1% of container width */
cqh   /* 1% of container height */
cqi   /* 1% of container inline size */
cqb   /* 1% of container block size */
```

## Position Property Values

### Position Types
```css
static    /* Default - normal flow */
relative  /* Relative to normal position */
absolute  /* Relative to nearest positioned ancestor */
fixed     /* Relative to viewport */
sticky    /* Switches between relative and fixed */
```

### Position Examples
```css
/* Relative - offset from normal position */
.relative {
    position: relative;
    top: 10px;    /* 10px down from normal */
    left: 20px;   /* 20px right from normal */
}

/* Absolute - relative to positioned parent */
.absolute {
    position: absolute;
    top: 0;       /* Top of positioned parent */
    right: 0;     /* Right of positioned parent */
}

/* Fixed - relative to viewport */
.fixed {
    position: fixed;
    bottom: 20px; /* 20px from bottom of screen */
    right: 20px;  /* 20px from right of screen */
}

/* Sticky - relative until threshold, then fixed */
.sticky {
    position: sticky;
    top: 0;       /* Stick at top when scrolling */
}
```

## Accessibility Checklist

### ARIA Attributes
```html
<!-- Roles -->
role="button | link | navigation | main | banner | contentinfo"
role="dialog | alertdialog | tooltip | tab | tabpanel"
role="grid | row | cell | listbox | option"

<!-- Properties -->
aria-label="Descriptive label"
aria-labelledby="element-id"
aria-describedby="element-id"
aria-expanded="true | false"
aria-hidden="true | false"
aria-current="page | step | location | date | time"
aria-live="polite | assertive | off"
aria-atomic="true | false"

<!-- States -->
aria-checked="true | false | mixed"
aria-disabled="true | false"
aria-invalid="true | false"
aria-pressed="true | false | mixed"
aria-selected="true | false"
```

### Focus Management
```css
/* Remove default outline only if providing alternative */
:focus {
    outline: none; /* Only if you provide custom focus styles */
}

/* Visible focus indicators */
:focus-visible {
    outline: 2px solid #007bff;
    outline-offset: 2px;
}

/* Skip link for keyboard users */
.skip-link {
    position: absolute;
    top: -40px;
    left: 6px;
    background: #000;
    color: white;
    padding: 8px;
    text-decoration: none;
    z-index: 1000;
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

## Performance Tips

### CSS Performance
```css
/* Use efficient selectors */
.class-name { }           /* Fast */
#id-name { }              /* Fast */
element { }               /* Moderate */
.class element { }        /* Moderate */
element element { }       /* Slow */
* { }                     /* Slowest */

/* Optimize animations */
.animate {
    /* Use these for best performance */
    transform: translateX(100px);
    opacity: 0.5;
    
    /* Avoid animating these */
    /* width, height, top, left, margin, padding */
}

/* Use will-change for heavy animations */
.heavy-animation {
    will-change: transform, opacity;
    /* Remove after animation completes */
}

/* Optimize images */
.responsive-image {
    max-width: 100%;
    height: auto;
    /* Use loading="lazy" in HTML */
}

/* Use contain for performance */
.contained-element {
    contain: layout style;
}
```

### Critical CSS Strategy
```html
<!-- Inline critical CSS in head -->
<style>
    /* Above-the-fold styles only */
    body { font-family: sans-serif; margin: 0; }
    .header { background: #fff; }
</style>

<!-- Load non-critical CSS asynchronously -->
<link rel="preload" href="styles.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
<noscript><link rel="stylesheet" href="styles.css"></noscript>
```

## Common CSS Functions

### Math Functions
```css
/* calc() - calculations */
width: calc(100% - 2rem);
font-size: calc(1rem + 2vw);

/* min() - smaller value */
width: min(500px, 100%);

/* max() - larger value */
height: max(200px, 50vh);

/* clamp() - responsive between min and max */
font-size: clamp(1rem, 4vw, 2rem);
padding: clamp(1rem, 5%, 3rem);
```

### Color Functions
```css
/* rgb() and rgba() */
color: rgb(255, 0, 0);
background: rgba(255, 0, 0, 0.5);

/* hsl() and hsla() */
color: hsl(0, 100%, 50%);
background: hsla(0, 100%, 50%, 0.5);

/* Modern color functions */
color: hwb(0 0% 0%);
color: lab(50% 20 -20);
color: lch(50% 20 0);
```

### Transform Functions
```css
/* 2D transforms */
transform: translateX(100px);
transform: translateY(50px);
transform: translate(100px, 50px);
transform: scale(1.5);
transform: scaleX(2);
transform: scaleY(0.5);
transform: rotate(45deg);
transform: skew(30deg, 20deg);

/* 3D transforms */
transform: translateZ(100px);
transform: translate3d(100px, 50px, 20px);
transform: rotateX(45deg);
transform: rotateY(45deg);
transform: rotateZ(45deg);
transform: scale3d(2, 1, 0.5);

/* Combine transforms */
transform: translate(100px, 50px) rotate(45deg) scale(1.2);
```
