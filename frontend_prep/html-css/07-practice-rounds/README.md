# Practice Rounds - Mock Interview Scenarios

## Round 1: Theory Questions (Rapid Fire)

### HTML Semantics & Accessibility
1. **Q**: What's the difference between `<section>` and `<article>`?
   **A**: `<section>` groups thematic content, `<article>` is standalone, reusable content

2. **Q**: How do you make a custom checkbox accessible?
   **A**: Use `role="checkbox"`, `aria-checked`, `tabindex="0"`, keyboard event handlers

3. **Q**: What's the purpose of the `alt` attribute?
   **A**: Provides alternative text for screen readers and when images fail to load

4. **Q**: When should you use `<button>` vs `<a>`?
   **A**: `<button>` for actions, `<a>` for navigation

5. **Q**: What does `aria-live` do?
   **A**: Announces dynamic content changes to screen readers

### CSS Fundamentals
6. **Q**: How does CSS specificity work?
   **A**: Inline(1000) > ID(100) > Class/Attribute/Pseudo(10) > Element(1)

7. **Q**: Difference between `em` and `rem`?
   **A**: `em` relative to parent font-size, `rem` relative to root font-size

8. **Q**: What triggers a new stacking context?
   **A**: `position: fixed/sticky`, `position: absolute/relative + z-index`, `opacity < 1`, `transform`, `filter`

9. **Q**: Difference between `display: none` and `visibility: hidden`?
   **A**: `display: none` removes from layout, `visibility: hidden` keeps space

10. **Q**: How does flexbox `justify-content` differ from `align-items`?
    **A**: `justify-content` aligns along main axis, `align-items` along cross axis

### Modern CSS
11. **Q**: When to use CSS Grid vs Flexbox?
    **A**: Grid for 2D layouts, Flexbox for 1D layouts

12. **Q**: What's `auto-fit` vs `auto-fill` in Grid?
    **A**: `auto-fit` expands tracks to fill space, `auto-fill` creates empty tracks

13. **Q**: How does `clamp()` work?
    **A**: `clamp(min, preferred, max)` - responsive value between min and max

14. **Q**: What's the cascade in CSS?
    **A**: Order of importance: !important > inline > ID > class > element > source order

15. **Q**: How do CSS custom properties cascade?
    **A**: They inherit like normal properties and can be overridden in child elements

## Round 2: Live Coding Challenges

### Challenge 1: Responsive Card Grid
**Task**: Create a responsive card grid that adjusts columns based on screen size

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            padding: 2rem;
        }
        
        .card {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
        }
        
        .card-image {
            width: 100%;
            height: 200px;
            background: #f0f0f0;
            border-radius: 4px;
            margin-bottom: 1rem;
            background-size: cover;
            background-position: center;
        }
        
        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: #333;
        }
        
        .card-description {
            color: #666;
            line-height: 1.6;
            margin-bottom: 1rem;
        }
        
        .card-button {
            display: inline-block;
            padding: 0.5rem 1rem;
            background: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            transition: background 0.2s ease;
        }
        
        .card-button:hover {
            background: #0056b3;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .card-grid {
                grid-template-columns: 1fr;
                padding: 1rem;
                gap: 1rem;
            }
        }
        
        @media (min-width: 1200px) {
            .card-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
    </style>
</head>
<body>
    <div class="card-grid">
        <div class="card">
            <div class="card-image" style="background-image: url('https://via.placeholder.com/300x200')"></div>
            <h3 class="card-title">Card Title 1</h3>
            <p class="card-description">This is a sample card description that explains the content.</p>
            <a href="#" class="card-button">Read More</a>
        </div>
        
        <div class="card">
            <div class="card-image" style="background-image: url('https://via.placeholder.com/300x200')"></div>
            <h3 class="card-title">Card Title 2</h3>
            <p class="card-description">Another card with different content but same structure.</p>
            <a href="#" class="card-button">Read More</a>
        </div>
        
        <div class="card">
            <div class="card-image" style="background-image: url('https://via.placeholder.com/300x200')"></div>
            <h3 class="card-title">Card Title 3</h3>
            <p class="card-description">Third card to demonstrate the grid layout system.</p>
            <a href="#" class="card-button">Read More</a>
        </div>
    </div>
</body>
</html>
```

### Challenge 2: Accessible Modal with Keyboard Navigation
**Task**: Implement a modal with proper focus management and keyboard navigation

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
            background: rgba(0, 0, 0, 0.6);
            display: none;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            opacity: 0;
            transition: opacity 0.3s ease;
        }
        
        .modal-overlay.active {
            display: flex;
            opacity: 1;
        }
        
        .modal {
            background: white;
            border-radius: 8px;
            padding: 0;
            max-width: 500px;
            width: 90%;
            max-height: 90vh;
            overflow: hidden;
            transform: scale(0.8);
            transition: transform 0.3s ease;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        
        .modal-overlay.active .modal {
            transform: scale(1);
        }
        
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1.5rem;
            border-bottom: 1px solid #e9ecef;
        }
        
        .modal-title {
            margin: 0;
            font-size: 1.25rem;
            font-weight: 600;
        }
        
        .modal-close {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            padding: 0.5rem;
            border-radius: 4px;
            line-height: 1;
            color: #6c757d;
        }
        
        .modal-close:hover {
            background: #f8f9fa;
            color: #495057;
        }
        
        .modal-close:focus {
            outline: 2px solid #007bff;
            outline-offset: 2px;
        }
        
        .modal-body {
            padding: 1.5rem;
        }
        
        .modal-footer {
            display: flex;
            justify-content: flex-end;
            gap: 1rem;
            padding: 1.5rem;
            border-top: 1px solid #e9ecef;
            background: #f8f9fa;
        }
        
        .btn {
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 0.9rem;
            transition: background 0.2s ease;
        }
        
        .btn-primary {
            background: #007bff;
            color: white;
        }
        
        .btn-primary:hover {
            background: #0056b3;
        }
        
        .btn-secondary {
            background: #6c757d;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #545b62;
        }
        
        .btn:focus {
            outline: 2px solid #007bff;
            outline-offset: 2px;
        }
        
        .form-group {
            margin-bottom: 1rem;
        }
        
        .form-label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
        }
        
        .form-input {
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #ced4da;
            border-radius: 4px;
            font-size: 1rem;
        }
        
        .form-input:focus {
            outline: none;
            border-color: #007bff;
            box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
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
            font-size: 1rem;
        }
    </style>
</head>
<body>
    <h1>Modal Demo</h1>
    <button class="open-modal-btn" id="openModal">Open Modal</button>
    
    <div class="modal-overlay" id="modalOverlay" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
        <div class="modal">
            <header class="modal-header">
                <h2 class="modal-title" id="modalTitle">Contact Form</h2>
                <button class="modal-close" id="closeModal" aria-label="Close modal">&times;</button>
            </header>
            
            <div class="modal-body">
                <form id="contactForm">
                    <div class="form-group">
                        <label for="name" class="form-label">Name *</label>
                        <input type="text" id="name" class="form-input" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="email" class="form-label">Email *</label>
                        <input type="email" id="email" class="form-input" required>
                    </div>
                    
                    <div class="form-group">
                        <label for="message" class="form-label">Message</label>
                        <textarea id="message" class="form-input" rows="4"></textarea>
                    </div>
                </form>
            </div>
            
            <footer class="modal-footer">
                <button type="button" class="btn btn-secondary" id="cancelBtn">Cancel</button>
                <button type="submit" class="btn btn-primary" form="contactForm">Send Message</button>
            </footer>
        </div>
    </div>

    <script>
        class AccessibleModal {
            constructor(modalId) {
                this.modal = document.getElementById(modalId);
                this.modalDialog = this.modal.querySelector('.modal');
                this.openBtn = document.getElementById('openModal');
                this.closeBtns = this.modal.querySelectorAll('#closeModal, #cancelBtn');
                this.focusableElements = null;
                this.firstFocusableElement = null;
                this.lastFocusableElement = null;
                this.previouslyFocusedElement = null;
                
                this.init();
            }
            
            init() {
                // Open modal
                this.openBtn.addEventListener('click', () => this.open());
                
                // Close modal
                this.closeBtns.forEach(btn => {
                    btn.addEventListener('click', () => this.close());
                });
                
                // Close on overlay click
                this.modal.addEventListener('click', (e) => {
                    if (e.target === this.modal) this.close();
                });
                
                // Handle keyboard events
                document.addEventListener('keydown', (e) => this.handleKeydown(e));
            }
            
            open() {
                this.previouslyFocusedElement = document.activeElement;
                this.modal.classList.add('active');
                document.body.classList.add('modal-open');
                
                // Get focusable elements
                this.updateFocusableElements();
                
                // Focus first element
                if (this.firstFocusableElement) {
                    this.firstFocusableElement.focus();
                }
            }
            
            close() {
                this.modal.classList.remove('active');
                document.body.classList.remove('modal-open');
                
                // Return focus to previously focused element
                if (this.previouslyFocusedElement) {
                    this.previouslyFocusedElement.focus();
                }
            }
            
            updateFocusableElements() {
                const focusableSelectors = [
                    'button:not([disabled])',
                    '[href]',
                    'input:not([disabled])',
                    'select:not([disabled])',
                    'textarea:not([disabled])',
                    '[tabindex]:not([tabindex="-1"]):not([disabled])'
                ].join(', ');
                
                this.focusableElements = this.modalDialog.querySelectorAll(focusableSelectors);
                this.firstFocusableElement = this.focusableElements[0];
                this.lastFocusableElement = this.focusableElements[this.focusableElements.length - 1];
            }
            
            handleKeydown(e) {
                if (!this.modal.classList.contains('active')) return;
                
                switch (e.key) {
                    case 'Escape':
                        e.preventDefault();
                        this.close();
                        break;
                        
                    case 'Tab':
                        this.trapFocus(e);
                        break;
                }
            }
            
            trapFocus(e) {
                if (e.shiftKey) {
                    // Shift + Tab
                    if (document.activeElement === this.firstFocusableElement) {
                        e.preventDefault();
                        this.lastFocusableElement.focus();
                    }
                } else {
                    // Tab
                    if (document.activeElement === this.lastFocusableElement) {
                        e.preventDefault();
                        this.firstFocusableElement.focus();
                    }
                }
            }
        }
        
        // Initialize modal
        new AccessibleModal('modalOverlay');
    </script>
</body>
</html>
```

## Round 3: Debugging Scenarios

### Scenario 1: Layout Shift Issues
**Problem**: Images cause layout shift when loading

**Solution**:
```css
/* Reserve space for images */
.image-container {
    position: relative;
    width: 100%;
    height: 0;
    padding-bottom: 56.25%; /* 16:9 aspect ratio */
}

.image-container img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
}

/* Or use aspect-ratio property (modern) */
.modern-image {
    width: 100%;
    aspect-ratio: 16 / 9;
    object-fit: cover;
}
```

### Scenario 2: Flex Item Overflow
**Problem**: Flex item content overflows container

**Solution**:
```css
.flex-container {
    display: flex;
}

.flex-item {
    flex: 1;
    min-width: 0; /* Allow shrinking below content size */
    overflow: hidden; /* Prevent overflow */
}

.flex-item-content {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* For multiline text */
.multiline-text {
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
```

### Scenario 3: Z-index Not Working
**Problem**: Element with higher z-index appears behind another

**Solution**:
```css
/* Create stacking context */
.parent {
    position: relative;
    z-index: 1; /* Creates new stacking context */
}

.child {
    position: absolute;
    z-index: 999; /* Only works within parent's context */
}

/* Fix: Move z-index to correct level */
.correct-parent {
    position: relative;
    z-index: 999; /* Move z-index here */
}

.correct-child {
    position: absolute;
    /* z-index not needed or use lower value */
}
```

## Round 4: System Design Discussion

### Question: Design CSS Architecture for SaaS Application

**Requirements**:
- Multi-tenant (different themes per tenant)
- Component library
- Dark/light mode support
- Scalable for large team
- Performance optimized

**Solution Architecture**:

```css
/* 1. Design Token System */
:root {
    /* Core tokens */
    --color-primary-100: #dbeafe;
    --color-primary-500: #3b82f6;
    --color-primary-900: #1e3a8a;
    
    /* Semantic tokens */
    --color-surface: var(--color-white);
    --color-text: var(--color-gray-900);
    --color-border: var(--color-gray-200);
}

/* 2. Theme System */
[data-theme="dark"] {
    --color-surface: var(--color-gray-900);
    --color-text: var(--color-gray-100);
    --color-border: var(--color-gray-700);
}

[data-tenant="company-a"] {
    --color-primary-500: #10b981; /* Company A brand */
}

[data-tenant="company-b"] {
    --color-primary-500: #f59e0b; /* Company B brand */
}

/* 3. Component System */
.c-button {
    padding: var(--space-2) var(--space-4);
    background: var(--color-primary-500);
    color: var(--color-button-text);
    border: none;
    border-radius: var(--radius-md);
    cursor: pointer;
    transition: background 0.2s ease;
}

/* 4. Utility System */
.u-text-center { text-align: center !important; }
.u-mb-4 { margin-bottom: var(--space-4) !important; }

/* 5. Layout System */
.l-container {
    max-width: var(--container-max-width);
    margin: 0 auto;
    padding: 0 var(--space-4);
}

.l-grid {
    display: grid;
    gap: var(--space-4);
}
```

**Implementation Strategy**:
1. **CSS Layers** for predictable cascade
2. **CSS Custom Properties** for theming
3. **Component Library** with Storybook
4. **Design Tokens** in JSON format
5. **Build Process** for optimization
6. **Documentation** with examples
7. **Linting Rules** for consistency

## Interview Performance Checklist

### Technical Skills Demonstrated
- [ ] HTML semantics and accessibility
- [ ] CSS layout systems (Flexbox, Grid)
- [ ] Responsive design principles
- [ ] Cross-browser compatibility
- [ ] Performance optimization
- [ ] Modern CSS features
- [ ] Architecture patterns

### Soft Skills Demonstrated
- [ ] Problem-solving approach
- [ ] Code organization
- [ ] Communication of technical concepts
- [ ] Attention to detail
- [ ] User experience consideration
- [ ] Scalability thinking
- [ ] Team collaboration mindset

### Common Mistakes to Avoid
- [ ] Not considering accessibility
- [ ] Overusing !important
- [ ] Ignoring performance implications
- [ ] Poor naming conventions
- [ ] Not planning for maintenance
- [ ] Forgetting responsive design
- [ ] Not testing in multiple browsers
