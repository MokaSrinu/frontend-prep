# Interview Patterns - Common Coding Challenges

## 1. Center a Div (All Possible Ways)

### Flexbox Centering
```css
/* Method 1: Flexbox - Most Modern */
.flex-center {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* or desired height */
}

.flex-center .child {
    /* Child automatically centered */
}
```

### Grid Centering
```css
/* Method 2: CSS Grid */
.grid-center {
    display: grid;
    place-items: center;
    height: 100vh;
}

/* Alternative Grid syntax */
.grid-center-alt {
    display: grid;
    justify-content: center;
    align-content: center;
    height: 100vh;
}
```

### Absolute Positioning
```css
/* Method 3: Absolute + Transform */
.absolute-center {
    position: relative;
    height: 100vh;
}

.absolute-center .child {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

/* Method 4: Absolute + Margin (requires known dimensions) */
.absolute-margin {
    position: relative;
    height: 100vh;
}

.absolute-margin .child {
    position: absolute;
    top: 50%;
    left: 50%;
    width: 200px;
    height: 100px;
    margin-left: -100px; /* -width/2 */
    margin-top: -50px;   /* -height/2 */
}
```

### Text Alignment (for inline elements)
```css
/* Method 5: Text align + Line height */
.text-center {
    text-align: center;
    line-height: 100vh; /* Same as container height */
}

.text-center .child {
    display: inline-block;
    vertical-align: middle;
    line-height: normal;
}
```

### Margin Auto (horizontal only)
```css
/* Method 6: Margin auto for horizontal centering */
.margin-center {
    width: 300px;
    margin: 0 auto;
    /* For vertical: margin: 50vh auto 0; margin-top: -50px; */
}
```

## 2. Sticky Header + Scrollable Content

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .layout {
            height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background: #333;
            color: white;
            padding: 1rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .main-content {
            flex: 1;
            overflow-y: auto;
            padding: 1rem;
        }
        
        /* Alternative with CSS Grid */
        .grid-layout {
            display: grid;
            grid-template-rows: auto 1fr;
            height: 100vh;
        }
        
        .grid-header {
            background: #333;
            color: white;
            padding: 1rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }
        
        .grid-content {
            overflow-y: auto;
            padding: 1rem;
        }
    </style>
</head>
<body>
    <div class="layout">
        <header class="header">
            <h1>Sticky Header</h1>
            <nav>Navigation items...</nav>
        </header>
        <main class="main-content">
            <!-- Long scrollable content -->
            <p>Content that scrolls...</p>
        </main>
    </div>
</body>
</html>
```

## 3. Responsive Navbar with Hamburger Menu

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem;
            background: #333;
            color: white;
        }
        
        .nav-menu {
            display: flex;
            list-style: none;
            margin: 0;
            padding: 0;
            gap: 2rem;
        }
        
        .nav-link {
            color: white;
            text-decoration: none;
            padding: 0.5rem;
        }
        
        .hamburger {
            display: none;
            flex-direction: column;
            cursor: pointer;
            padding: 0.5rem;
        }
        
        .hamburger span {
            width: 25px;
            height: 3px;
            background: white;
            margin: 2px 0;
            transition: 0.3s;
            transform-origin: center;
        }
        
        /* Mobile styles */
        @media (max-width: 768px) {
            .nav-menu {
                position: fixed;
                top: 70px;
                left: -100%;
                width: 100%;
                height: calc(100vh - 70px);
                background: #333;
                flex-direction: column;
                align-items: center;
                justify-content: flex-start;
                gap: 0;
                transition: left 0.3s ease;
                padding-top: 2rem;
            }
            
            .nav-menu.active {
                left: 0;
            }
            
            .nav-item {
                width: 100%;
                text-align: center;
            }
            
            .nav-link {
                display: block;
                padding: 1rem;
                border-bottom: 1px solid #444;
            }
            
            .hamburger {
                display: flex;
            }
            
            /* Hamburger animation */
            .hamburger.active span:nth-child(1) {
                transform: rotate(45deg) translate(5px, 5px);
            }
            
            .hamburger.active span:nth-child(2) {
                opacity: 0;
            }
            
            .hamburger.active span:nth-child(3) {
                transform: rotate(-45deg) translate(7px, -6px);
            }
        }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="nav-brand">
            <h2>Logo</h2>
        </div>
        
        <ul class="nav-menu">
            <li class="nav-item">
                <a href="#" class="nav-link">Home</a>
            </li>
            <li class="nav-item">
                <a href="#" class="nav-link">About</a>
            </li>
            <li class="nav-item">
                <a href="#" class="nav-link">Services</a>
            </li>
            <li class="nav-item">
                <a href="#" class="nav-link">Contact</a>
            </li>
        </ul>
        
        <div class="hamburger">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </nav>

    <script>
        const hamburger = document.querySelector('.hamburger');
        const navMenu = document.querySelector('.nav-menu');

        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close menu when clicking on links
        document.querySelectorAll('.nav-link').forEach(n => n.addEventListener('click', () => {
            hamburger.classList.remove('active');
            navMenu.classList.remove('active');
        }));
    </script>
</body>
</html>
```

## 4. Modal with Backdrop (Focus Trap)

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.5);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        
        .modal-overlay.active {
            display: flex;
        }
        
        .modal {
            background: white;
            padding: 2rem;
            border-radius: 8px;
            max-width: 500px;
            width: 90%;
            max-height: 90vh;
            overflow-y: auto;
            position: relative;
            animation: modalSlideIn 0.3s ease;
        }
        
        @keyframes modalSlideIn {
            from {
                transform: scale(0.8);
                opacity: 0;
            }
            to {
                transform: scale(1);
                opacity: 1;
            }
        }
        
        .modal-close {
            position: absolute;
            top: 1rem;
            right: 1rem;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 4px;
        }
        
        .modal-close:hover {
            background: #f0f0f0;
        }
        
        .modal-close:focus {
            outline: 2px solid #007bff;
        }
        
        /* Prevent body scroll when modal is open */
        body.modal-open {
            overflow: hidden;
        }
        
        .open-modal-btn {
            padding: 1rem 2rem;
            background: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            margin: 2rem;
        }
    </style>
</head>
<body>
    <button class="open-modal-btn">Open Modal</button>
    
    <div class="modal-overlay" id="modal">
        <div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
            <button class="modal-close" aria-label="Close modal">&times;</button>
            <h2 id="modal-title">Modal Title</h2>
            <p>This is modal content. The focus should be trapped within this modal.</p>
            <form>
                <input type="text" placeholder="First input">
                <input type="text" placeholder="Second input">
                <button type="submit">Submit</button>
                <button type="button" class="cancel-btn">Cancel</button>
            </form>
        </div>
    </div>

    <script>
        class Modal {
            constructor(modalElement) {
                this.modal = modalElement;
                this.modalDialog = modalElement.querySelector('.modal');
                this.closeBtn = modalElement.querySelector('.modal-close');
                this.openBtn = document.querySelector('.open-modal-btn');
                this.focusableElements = null;
                this.firstFocusableElement = null;
                this.lastFocusableElement = null;
                
                this.init();
            }
            
            init() {
                this.openBtn.addEventListener('click', () => this.open());
                this.closeBtn.addEventListener('click', () => this.close());
                this.modal.addEventListener('click', (e) => {
                    if (e.target === this.modal) this.close();
                });
                
                document.addEventListener('keydown', (e) => {
                    if (e.key === 'Escape' && this.modal.classList.contains('active')) {
                        this.close();
                    }
                    
                    if (e.key === 'Tab' && this.modal.classList.contains('active')) {
                        this.trapFocus(e);
                    }
                });
            }
            
            open() {
                this.modal.classList.add('active');
                document.body.classList.add('modal-open');
                
                // Get focusable elements
                this.focusableElements = this.modalDialog.querySelectorAll(
                    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
                );
                this.firstFocusableElement = this.focusableElements[0];
                this.lastFocusableElement = this.focusableElements[this.focusableElements.length - 1];
                
                // Focus first element
                this.firstFocusableElement.focus();
            }
            
            close() {
                this.modal.classList.remove('active');
                document.body.classList.remove('modal-open');
                this.openBtn.focus(); // Return focus to trigger
            }
            
            trapFocus(e) {
                if (e.shiftKey) {
                    if (document.activeElement === this.firstFocusableElement) {
                        this.lastFocusableElement.focus();
                        e.preventDefault();
                    }
                } else {
                    if (document.activeElement === this.lastFocusableElement) {
                        this.firstFocusableElement.focus();
                        e.preventDefault();
                    }
                }
            }
        }
        
        // Initialize modal
        new Modal(document.getElementById('modal'));
    </script>
</body>
</html>
```

## 5. Accordion & Tabs (with Accessibility)

### Accessible Accordion
```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .accordion {
            border: 1px solid #ddd;
            border-radius: 4px;
            margin: 1rem 0;
        }
        
        .accordion-item {
            border-bottom: 1px solid #ddd;
        }
        
        .accordion-item:last-child {
            border-bottom: none;
        }
        
        .accordion-header {
            width: 100%;
            padding: 1rem;
            background: #f8f9fa;
            border: none;
            text-align: left;
            cursor: pointer;
            font-size: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .accordion-header:hover {
            background: #e9ecef;
        }
        
        .accordion-header:focus {
            outline: 2px solid #007bff;
            outline-offset: -2px;
        }
        
        .accordion-header[aria-expanded="true"] {
            background: #007bff;
            color: white;
        }
        
        .accordion-icon {
            transition: transform 0.3s ease;
        }
        
        .accordion-header[aria-expanded="true"] .accordion-icon {
            transform: rotate(180deg);
        }
        
        .accordion-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }
        
        .accordion-content.active {
            max-height: 200px; /* Adjust based on content */
        }
        
        .accordion-body {
            padding: 1rem;
        }
    </style>
</head>
<body>
    <div class="accordion">
        <div class="accordion-item">
            <button class="accordion-header" aria-expanded="false" aria-controls="content-1">
                <span>Section 1</span>
                <span class="accordion-icon">▼</span>
            </button>
            <div class="accordion-content" id="content-1">
                <div class="accordion-body">
                    Content for section 1. This content is collapsible.
                </div>
            </div>
        </div>
        
        <div class="accordion-item">
            <button class="accordion-header" aria-expanded="false" aria-controls="content-2">
                <span>Section 2</span>
                <span class="accordion-icon">▼</span>
            </button>
            <div class="accordion-content" id="content-2">
                <div class="accordion-body">
                    Content for section 2. This content is also collapsible.
                </div>
            </div>
        </div>
    </div>

    <script>
        class Accordion {
            constructor(accordion) {
                this.accordion = accordion;
                this.headers = accordion.querySelectorAll('.accordion-header');
                this.init();
            }
            
            init() {
                this.headers.forEach(header => {
                    header.addEventListener('click', () => this.toggle(header));
                    header.addEventListener('keydown', (e) => this.handleKeydown(e, header));
                });
            }
            
            toggle(header) {
                const content = document.getElementById(header.getAttribute('aria-controls'));
                const isExpanded = header.getAttribute('aria-expanded') === 'true';
                
                // Close all others (optional - for single-open accordion)
                // this.closeAll();
                
                if (isExpanded) {
                    this.close(header, content);
                } else {
                    this.open(header, content);
                }
            }
            
            open(header, content) {
                header.setAttribute('aria-expanded', 'true');
                content.classList.add('active');
                content.style.maxHeight = content.scrollHeight + 'px';
            }
            
            close(header, content) {
                header.setAttribute('aria-expanded', 'false');
                content.classList.remove('active');
                content.style.maxHeight = '0';
            }
            
            handleKeydown(e, header) {
                const key = e.key;
                const headers = Array.from(this.headers);
                const currentIndex = headers.indexOf(header);
                
                switch (key) {
                    case 'ArrowDown':
                        e.preventDefault();
                        const nextIndex = (currentIndex + 1) % headers.length;
                        headers[nextIndex].focus();
                        break;
                    case 'ArrowUp':
                        e.preventDefault();
                        const prevIndex = currentIndex === 0 ? headers.length - 1 : currentIndex - 1;
                        headers[prevIndex].focus();
                        break;
                    case 'Home':
                        e.preventDefault();
                        headers[0].focus();
                        break;
                    case 'End':
                        e.preventDefault();
                        headers[headers.length - 1].focus();
                        break;
                }
            }
        }
        
        // Initialize accordion
        document.querySelectorAll('.accordion').forEach(accordion => {
            new Accordion(accordion);
        });
    </script>
</body>
</html>
```

## 6. Skeleton Loader

```css
.skeleton {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: loading 1.5s infinite;
}

@keyframes loading {
    0% {
        background-position: 200% 0;
    }
    100% {
        background-position: -200% 0;
    }
}

.skeleton-text {
    height: 1rem;
    border-radius: 4px;
    margin-bottom: 0.5rem;
}

.skeleton-text:last-child {
    width: 80%;
}

.skeleton-avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
}

.skeleton-image {
    width: 100%;
    height: 200px;
    border-radius: 8px;
}

/* Card with skeleton */
.skeleton-card {
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 8px;
}

.skeleton-header {
    display: flex;
    gap: 1rem;
    margin-bottom: 1rem;
}
```

## 7. Multi-line Text Truncation

```css
/* Single line truncation */
.truncate-single {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Multi-line truncation (modern) */
.truncate-multiline {
    display: -webkit-box;
    -webkit-line-clamp: 3; /* Number of lines */
    -webkit-box-orient: vertical;
    overflow: hidden;
    line-height: 1.5;
}

/* Fallback for older browsers */
.truncate-multiline-fallback {
    position: relative;
    max-height: 4.5rem; /* line-height * number of lines */
    overflow: hidden;
    line-height: 1.5;
}

.truncate-multiline-fallback::after {
    content: '...';
    position: absolute;
    bottom: 0;
    right: 0;
    background: white;
    padding-left: 1rem;
}
```

## Key Interview Tips

### 1. Always Consider Accessibility
- Add proper ARIA attributes
- Ensure keyboard navigation works
- Test with screen readers
- Include focus indicators

### 2. Performance Considerations
- Use `transform` and `opacity` for animations
- Minimize layout thrashing
- Consider `will-change` property
- Test on mobile devices

### 3. Progressive Enhancement
- Start with basic functionality
- Add enhancements with CSS
- Ensure graceful degradation

### 4. Modern CSS Features
- Use CSS Grid and Flexbox appropriately
- Leverage CSS custom properties
- Consider container queries
- Use logical properties for internationalization
