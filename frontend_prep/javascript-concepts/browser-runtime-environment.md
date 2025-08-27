# 🌐 Browser & Runtime Environment - Detailed Guide

> **Master browser APIs, DOM manipulation, and web runtime concepts with comprehensive explanations and practical examples**

---

## 📋 Table of Contents

1. [DOM Manipulation](#1-dom-manipulation)
2. [Event System](#2-event-system)
3. [Storage Mechanisms](#3-storage-mechanisms)
4. [Web APIs](#4-web-apis)
5. [Security](#5-security)
6. [Performance Optimization](#6-performance-optimization)

---

## 1. DOM Manipulation

> **Interview Explanation:** The DOM (Document Object Model) is a programming interface for HTML documents. It represents the structure of a document as a tree of objects that can be modified with JavaScript. Understanding DOM manipulation is essential for creating dynamic web applications.

### 🎯 DOM Traversal

> **Interview Key Point:** DOM traversal allows you to navigate through the document tree structure. This is fundamental for selecting and manipulating elements.

#### **Parent-Child Relationships**

```javascript
// DOM Traversal Methods
const element = document.getElementById('myElement');

// Parent navigation
console.log(element.parentNode);        // Direct parent (including text nodes)
console.log(element.parentElement);     // Parent element (excludes text nodes)

// Child navigation
console.log(element.childNodes);        // All child nodes (including text)
console.log(element.children);          // Only element children
console.log(element.firstChild);        // First child node
console.log(element.firstElementChild); // First element child
console.log(element.lastChild);         // Last child node
console.log(element.lastElementChild);  // Last element child

// Sibling navigation
console.log(element.nextSibling);       // Next sibling node
console.log(element.nextElementSibling); // Next sibling element
console.log(element.previousSibling);   // Previous sibling node
console.log(element.previousElementSibling); // Previous sibling element
```

> **Interview Tip:** Know the difference between `Node` and `Element`. Nodes include text nodes and comments, while Elements are only HTML tags.

#### **Advanced Traversal Methods**

```javascript
// Modern traversal methods
const container = document.querySelector('.container');

// Closest ancestor matching selector
const closestForm = element.closest('form');

// Check if element matches selector
const isButton = element.matches('button');

// Get all matching descendants
const allButtons = container.querySelectorAll('button');

// Check if element contains another
const containsChild = container.contains(element);

// Practical example: Find all form inputs
function getAllFormInputs(formElement) {
    return formElement.querySelectorAll('input, select, textarea');
}
```

### 🎯 Element Selection

> **Interview Key Point:** Efficient element selection is crucial for performance. Know the trade-offs between different selection methods.

#### **Selection Methods Comparison**

```javascript
// Selection methods with performance implications

// 1. By ID (Fastest - O(1))
const elementById = document.getElementById('myId');

// 2. By Class Name (Fast - optimized)
const elementsByClass = document.getElementsByClassName('myClass');

// 3. By Tag Name (Fast - optimized)
const elementsByTag = document.getElementsByTagName('div');

// 4. Query Selector (Flexible but slower)
const elementByQuery = document.querySelector('.myClass');
const elementsByQueryAll = document.querySelectorAll('.myClass');

// 5. By Name (For form elements)
const elementsByName = document.getElementsByName('username');
```

> **Interview Tip:** `getElementById` returns a single element, while `getElementsByClassName` and `getElementsByTagName` return live HTMLCollections that update automatically when the DOM changes.

#### **Live vs Static Collections**

```javascript
// Live Collection (updates automatically)
const liveButtons = document.getElementsByTagName('button');
console.log(liveButtons.length); // Current count

// Add new button
document.body.appendChild(document.createElement('button'));
console.log(liveButtons.length); // Count increased automatically

// Static Collection (snapshot)
const staticButtons = document.querySelectorAll('button');
const initialCount = staticButtons.length;

// Add new button
document.body.appendChild(document.createElement('button'));
console.log(staticButtons.length); // Same as initialCount

// Performance consideration
function efficientSelection() {
    // Cache selections to avoid repeated DOM queries
    const buttons = document.querySelectorAll('.btn');
    
    buttons.forEach(button => {
        // Perform operations on cached collection
        button.addEventListener('click', handleClick);
    });
}
```

### 🎯 Event Handling

> **Interview Explanation:** Event handling is how JavaScript responds to user interactions and browser events. Understanding the event lifecycle and different ways to attach event handlers is crucial.

#### **Event Attachment Methods**

```javascript
// 1. Inline Event Handlers (Not recommended)
// <button onclick="handleClick()">Click me</button>

// 2. Property Assignment
const button = document.getElementById('myButton');
button.onclick = function(event) {
    console.log('Button clicked!');
};

// 3. addEventListener (Recommended)
button.addEventListener('click', function(event) {
    console.log('Button clicked via addEventListener!');
});

// 4. Multiple Event Listeners
button.addEventListener('click', handler1);
button.addEventListener('click', handler2);
button.addEventListener('click', handler3);

// 5. Event Options
button.addEventListener('click', handler, {
    once: true,      // Execute only once
    passive: true,   // Never calls preventDefault
    capture: true    // Execute during capture phase
});
```

> **Interview Key Point:** `addEventListener` is preferred because it allows multiple handlers for the same event and provides more control through options.

#### **Event Object Properties**

```javascript
function handleEvent(event) {
    // Event target vs currentTarget
    console.log('target:', event.target);           // Element that triggered event
    console.log('currentTarget:', event.currentTarget); // Element with event listener
    
    // Event type and timing
    console.log('type:', event.type);               // Event type (click, keydown, etc.)
    console.log('timeStamp:', event.timeStamp);     // When event occurred
    
    // Mouse events
    if (event instanceof MouseEvent) {
        console.log('clientX:', event.clientX);     // X coordinate relative to viewport
        console.log('clientY:', event.clientY);     // Y coordinate relative to viewport
        console.log('offsetX:', event.offsetX);     // X coordinate relative to target
        console.log('offsetY:', event.offsetY);     // Y coordinate relative to target
        console.log('button:', event.button);       // Which mouse button (0=left, 1=middle, 2=right)
    }
    
    // Keyboard events
    if (event instanceof KeyboardEvent) {
        console.log('key:', event.key);             // Key value
        console.log('code:', event.code);           // Physical key code
        console.log('altKey:', event.altKey);       // Alt key pressed
        console.log('ctrlKey:', event.ctrlKey);     // Ctrl key pressed
        console.log('shiftKey:', event.shiftKey);   // Shift key pressed
    }
    
    // Prevent default behavior
    event.preventDefault();
    
    // Stop event propagation
    event.stopPropagation();
    event.stopImmediatePropagation(); // Stops other listeners on same element
}
```

### 🎯 Dynamic Content Creation

> **Interview Key Point:** Creating elements dynamically is essential for modern web applications. Know the performance implications and best practices.

#### **Element Creation Methods**

```javascript
// 1. createElement (Traditional method)
function createElementTraditional() {
    const div = document.createElement('div');
    div.className = 'dynamic-element';
    div.id = 'element-1';
    div.textContent = 'Dynamically created element';
    
    // Set attributes
    div.setAttribute('data-id', '123');
    div.setAttribute('aria-label', 'Dynamic content');
    
    // Add styles
    div.style.backgroundColor = 'lightblue';
    div.style.padding = '10px';
    
    // Append to DOM
    document.body.appendChild(div);
    
    return div;
}

// 2. innerHTML (Faster for multiple elements but security risk)
function createWithInnerHTML() {
    const container = document.getElementById('container');
    container.innerHTML = `
        <div class="card">
            <h3>Card Title</h3>
            <p>Card content goes here</p>
            <button class="btn">Action</button>
        </div>
    `;
}

// 3. Template strings with insertAdjacentHTML (Best of both worlds)
function createWithTemplate(data) {
    const container = document.getElementById('container');
    const template = `
        <div class="user-card" data-user-id="${data.id}">
            <img src="${data.avatar}" alt="${data.name}">
            <h3>${data.name}</h3>
            <p>${data.email}</p>
            <button class="contact-btn">Contact</button>
        </div>
    `;
    
    container.insertAdjacentHTML('beforeend', template);
}

// 4. Document Fragment (Best performance for multiple elements)
function createMultipleElements(items) {
    const fragment = document.createDocumentFragment();
    
    items.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item.name;
        li.dataset.id = item.id;
        fragment.appendChild(li);
    });
    
    // Single DOM update
    document.getElementById('list').appendChild(fragment);
}
```

> **Interview Tip:** Use DocumentFragment when creating multiple elements to minimize DOM reflows and improve performance.

#### **Cloning and Templates**

```javascript
// 1. Cloning existing elements
function cloneElement() {
    const original = document.getElementById('template');
    const clone = original.cloneNode(true); // true for deep clone
    
    // Modify clone
    clone.id = 'cloned-element';
    clone.querySelector('.title').textContent = 'Cloned Title';
    
    document.body.appendChild(clone);
}

// 2. HTML Templates (Modern approach)
// HTML: <template id="card-template">...</template>
function useHTMLTemplate(data) {
    const template = document.getElementById('card-template');
    const clone = template.content.cloneNode(true);
    
    // Populate template
    clone.querySelector('.card-title').textContent = data.title;
    clone.querySelector('.card-description').textContent = data.description;
    clone.querySelector('.card-image').src = data.image;
    
    document.getElementById('cards-container').appendChild(clone);
}

// 3. Efficient list rendering
function renderList(items) {
    const listContainer = document.getElementById('list');
    
    // Clear existing content
    listContainer.innerHTML = '';
    
    // Use fragment for better performance
    const fragment = document.createDocumentFragment();
    
    items.forEach((item, index) => {
        const listItem = document.createElement('li');
        listItem.className = 'list-item';
        listItem.innerHTML = `
            <span class="item-name">${item.name}</span>
            <span class="item-count">${item.count}</span>
            <button class="delete-btn" data-index="${index}">Delete</button>
        `;
        
        fragment.appendChild(listItem);
    });
    
    listContainer.appendChild(fragment);
}
```

#### **Performance Considerations**

```javascript
// BAD: Multiple DOM manipulations
function inefficientUpdate() {
    const list = document.getElementById('list');
    
    for (let i = 0; i < 1000; i++) {
        const li = document.createElement('li');
        li.textContent = `Item ${i}`;
        list.appendChild(li); // Triggers reflow for each append
    }
}

// GOOD: Batch DOM manipulations
function efficientUpdate() {
    const list = document.getElementById('list');
    const fragment = document.createDocumentFragment();
    
    for (let i = 0; i < 1000; i++) {
        const li = document.createElement('li');
        li.textContent = `Item ${i}`;
        fragment.appendChild(li); // No DOM reflow
    }
    
    list.appendChild(fragment); // Single reflow
}

// BEST: Virtual DOM concept simulation
class SimpleVirtualDOM {
    constructor(container) {
        this.container = container;
        this.currentState = [];
    }
    
    render(newState) {
        if (JSON.stringify(newState) === JSON.stringify(this.currentState)) {
            return; // No changes needed
        }
        
        // Batch update
        const fragment = document.createDocumentFragment();
        newState.forEach(item => {
            const element = document.createElement('div');
            element.textContent = item.text;
            element.className = item.className;
            fragment.appendChild(element);
        });
        
        this.container.innerHTML = '';
        this.container.appendChild(fragment);
        this.currentState = [...newState];
    }
}
```

> **Interview Explanation:** DOM manipulation can be expensive. Always batch operations, use DocumentFragments for multiple elements, and avoid unnecessary DOM queries by caching element references.

---

## 2. Event System

> **Interview Explanation:** The Event System is how browsers handle user interactions and system events. Understanding event flow, delegation, and custom events is crucial for building interactive web applications.

### 🎯 Event Bubbling & Capturing

> **Interview Key Point:** Events in the DOM follow a three-phase lifecycle: Capture → Target → Bubble. Understanding this flow is essential for proper event handling.

#### **Event Flow Phases**

```javascript
// HTML Structure:
// <div id="outer">
//   <div id="middle">
//     <button id="inner">Click me</button>
//   </div>
// </div>

// Phase 1: Capture (from document to target)
document.getElementById('outer').addEventListener('click', (e) => {
    console.log('Outer - Capture Phase');
}, true); // true enables capture phase

document.getElementById('middle').addEventListener('click', (e) => {
    console.log('Middle - Capture Phase');
}, true);

// Phase 2: Target (at the clicked element)
document.getElementById('inner').addEventListener('click', (e) => {
    console.log('Target - Button clicked');
});

// Phase 3: Bubble (from target back to document)
document.getElementById('middle').addEventListener('click', (e) => {
    console.log('Middle - Bubble Phase');
});

document.getElementById('outer').addEventListener('click', (e) => {
    console.log('Outer - Bubble Phase');
});

// Click order: Outer Capture → Middle Capture → Target → Middle Bubble → Outer Bubble
```

> **Interview Tip:** Most events bubble (except focus, blur, mouseenter, mouseleave). Use `event.stopPropagation()` to stop the flow.

#### **Controlling Event Flow**

```javascript
function demonstrateEventFlow() {
    const outer = document.getElementById('outer');
    const middle = document.getElementById('middle');
    const inner = document.getElementById('inner');
    
    // Stop propagation
    middle.addEventListener('click', (e) => {
        console.log('Middle clicked - stopping propagation');
        e.stopPropagation(); // Prevents bubbling to outer
    });
    
    // Stop immediate propagation
    inner.addEventListener('click', (e) => {
        console.log('First handler');
        e.stopImmediatePropagation(); // Stops other handlers on same element
    });
    
    inner.addEventListener('click', (e) => {
        console.log('This will not execute');
    });
    
    // Prevent default behavior
    const link = document.querySelector('a');
    link.addEventListener('click', (e) => {
        e.preventDefault(); // Prevents navigation
        console.log('Link clicked but navigation prevented');
    });
}
```

### 🎯 Event Delegation

> **Interview Key Point:** Event delegation leverages event bubbling to handle events for multiple elements with a single event listener. This is more efficient and works for dynamically added elements.

#### **Basic Event Delegation**

```javascript
// Without delegation (inefficient)
function attachEventsDirectly() {
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', handleButtonClick);
    });
}

// With delegation (efficient)
function setupEventDelegation() {
    const container = document.getElementById('button-container');
    
    container.addEventListener('click', function(e) {
        // Check if clicked element is a button
        if (e.target.classList.contains('btn')) {
            handleButtonClick(e);
        }
        
        // Handle different types of elements
        if (e.target.matches('.delete-btn')) {
            handleDelete(e);
        } else if (e.target.matches('.edit-btn')) {
            handleEdit(e);
        } else if (e.target.closest('.card')) {
            handleCardClick(e);
        }
    });
}

function handleButtonClick(e) {
    const button = e.target;
    const action = button.dataset.action;
    const id = button.dataset.id;
    
    console.log(`Button clicked: ${action} for item ${id}`);
}
```

#### **Advanced Delegation Patterns**

```javascript
// Delegation with method mapping
class EventDelegator {
    constructor(container) {
        this.container = container;
        this.handlers = new Map();
        this.setupDelegation();
    }
    
    setupDelegation() {
        this.container.addEventListener('click', this.handleClick.bind(this));
        this.container.addEventListener('keydown', this.handleKeydown.bind(this));
        this.container.addEventListener('change', this.handleChange.bind(this));
    }
    
    handleClick(e) {
        const target = e.target;
        const action = target.dataset.action;
        
        if (action && this.handlers.has(action)) {
            this.handlers.get(action)(e, target);
        }
        
        // Handle by element type
        if (target.matches('button')) {
            this.handleButtonClick(e, target);
        }
    }
    
    handleKeydown(e) {
        if (e.key === 'Enter' && e.target.matches('[data-action]')) {
            e.target.click(); // Simulate click for accessibility
        }
    }
    
    handleChange(e) {
        if (e.target.matches('input[type="checkbox"]')) {
            this.handleCheckboxChange(e, e.target);
        }
    }
    
    // Register action handlers
    registerHandler(action, handler) {
        this.handlers.set(action, handler);
    }
    
    handleButtonClick(e, button) {
        const ripple = this.createRippleEffect(e, button);
        button.appendChild(ripple);
    }
    
    createRippleEffect(e, button) {
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            width: ${size}px;
            height: ${size}px;
            left: ${x}px;
            top: ${y}px;
            background: rgba(255,255,255,0.5);
            border-radius: 50%;
            transform: scale(0);
            animation: ripple 0.6s ease-out;
            pointer-events: none;
        `;
        
        setTimeout(() => ripple.remove(), 600);
        return ripple;
    }
}

// Usage
const delegator = new EventDelegator(document.getElementById('app'));
delegator.registerHandler('delete', (e, target) => {
    const id = target.dataset.id;
    if (confirm('Are you sure?')) {
        deleteItem(id);
    }
});
```

### 🎯 Custom Events

> **Interview Key Point:** Custom events allow you to create your own event types for component communication and decoupled architecture.

#### **Creating and Dispatching Custom Events**

```javascript
// Simple custom event
function createSimpleEvent() {
    const element = document.getElementById('myElement');
    
    // Create custom event
    const customEvent = new CustomEvent('myCustomEvent', {
        detail: {
            message: 'Hello from custom event!',
            timestamp: Date.now(),
            data: { user: 'john', action: 'login' }
        },
        bubbles: true,
        cancelable: true
    });
    
    // Dispatch the event
    element.dispatchEvent(customEvent);
}

// Listen for custom event
document.addEventListener('myCustomEvent', (e) => {
    console.log('Custom event received:', e.detail);
});

// Advanced custom event with validation
class CustomEventManager {
    constructor() {
        this.eventTypes = new Set();
        this.listeners = new Map();
    }
    
    // Register event type
    registerEventType(eventType, schema = {}) {
        this.eventTypes.add(eventType);
        this.listeners.set(eventType, new Set());
        
        // Create convenience method
        this[`emit${this.capitalize(eventType)}`] = (detail) => {
            this.emit(eventType, detail, schema);
        };
    }
    
    // Emit custom event with validation
    emit(eventType, detail = {}, schema = {}) {
        if (!this.eventTypes.has(eventType)) {
            throw new Error(`Event type '${eventType}' not registered`);
        }
        
        // Validate against schema
        if (schema.required && !this.validateSchema(detail, schema)) {
            throw new Error('Event detail validation failed');
        }
        
        const event = new CustomEvent(eventType, {
            detail: {
                ...detail,
                timestamp: Date.now(),
                eventId: this.generateId()
            },
            bubbles: true,
            cancelable: true
        });
        
        document.dispatchEvent(event);
        return event;
    }
    
    // Subscribe to custom event
    on(eventType, handler, options = {}) {
        const wrappedHandler = (e) => {
            if (options.once) {
                this.off(eventType, wrappedHandler);
            }
            handler(e.detail, e);
        };
        
        document.addEventListener(eventType, wrappedHandler);
        this.listeners.get(eventType)?.add(wrappedHandler);
        
        return () => this.off(eventType, wrappedHandler);
    }
    
    // Unsubscribe from custom event
    off(eventType, handler) {
        document.removeEventListener(eventType, handler);
        this.listeners.get(eventType)?.delete(handler);
    }
    
    validateSchema(detail, schema) {
        if (schema.required) {
            return schema.required.every(prop => prop in detail);
        }
        return true;
    }
    
    generateId() {
        return Math.random().toString(36).substr(2, 9);
    }
    
    capitalize(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
}

// Usage example
const eventManager = new CustomEventManager();

// Register event types
eventManager.registerEventType('userLogin', {
    required: ['userId', 'timestamp']
});
eventManager.registerEventType('dataUpdate', {
    required: ['entity', 'action']
});

// Emit events
eventManager.emitUserLogin({
    userId: '12345',
    username: 'john_doe',
    timestamp: Date.now()
});

// Listen for events
const unsubscribe = eventManager.on('userLogin', (detail) => {
    console.log('User logged in:', detail);
});
```

#### **Inter-Component Communication**

```javascript
// Component communication using custom events
class Component {
    constructor(element) {
        this.element = element;
        this.events = new EventTarget(); // For internal events
        this.setupListeners();
    }
    
    // Internal event system
    emit(eventType, data) {
        this.events.dispatchEvent(new CustomEvent(eventType, { detail: data }));
    }
    
    on(eventType, handler) {
        this.events.addEventListener(eventType, handler);
    }
    
    // Global event system (DOM events)
    broadcast(eventType, data) {
        const event = new CustomEvent(`component:${eventType}`, {
            detail: { source: this.constructor.name, data },
            bubbles: true
        });
        document.dispatchEvent(event);
    }
    
    listen(eventType, handler) {
        document.addEventListener(`component:${eventType}`, handler);
    }
}

// Shopping cart component
class ShoppingCart extends Component {
    constructor(element) {
        super(element);
        this.items = [];
    }
    
    addItem(item) {
        this.items.push(item);
        this.emit('itemAdded', item);
        this.broadcast('cartUpdated', { 
            items: this.items, 
            total: this.getTotal() 
        });
    }
    
    removeItem(itemId) {
        const index = this.items.findIndex(item => item.id === itemId);
        if (index > -1) {
            const removed = this.items.splice(index, 1)[0];
            this.emit('itemRemoved', removed);
            this.broadcast('cartUpdated', { 
                items: this.items, 
                total: this.getTotal() 
            });
        }
    }
    
    getTotal() {
        return this.items.reduce((sum, item) => sum + item.price, 0);
    }
}

// Navigation component that listens to cart updates
class Navigation extends Component {
    constructor(element) {
        super(element);
        this.cartBadge = element.querySelector('.cart-badge');
        this.setupCartListener();
    }
    
    setupCartListener() {
        this.listen('cartUpdated', (e) => {
            const { items } = e.detail.data;
            this.updateCartBadge(items.length);
        });
    }
    
    updateCartBadge(count) {
        this.cartBadge.textContent = count;
        this.cartBadge.style.display = count > 0 ? 'block' : 'none';
    }
}
```

### 🎯 Event Object Properties

> **Interview Key Point:** Understanding event object properties is crucial for handling different types of events effectively.

#### **Mouse Event Properties**

```javascript
function handleMouseEvent(e) {
    // Position properties
    console.log('clientX/Y:', e.clientX, e.clientY);     // Relative to viewport
    console.log('pageX/Y:', e.pageX, e.pageY);           // Relative to document
    console.log('screenX/Y:', e.screenX, e.screenY);     // Relative to screen
    console.log('offsetX/Y:', e.offsetX, e.offsetY);     // Relative to target element
    
    // Button properties
    console.log('button:', e.button);                     // 0=left, 1=middle, 2=right
    console.log('buttons:', e.buttons);                   // Bitmask of pressed buttons
    
    // Modifier keys
    console.log('altKey:', e.altKey);
    console.log('ctrlKey:', e.ctrlKey);
    console.log('shiftKey:', e.shiftKey);
    console.log('metaKey:', e.metaKey);                   // Cmd on Mac, Windows key on PC
    
    // Related targets (for mouseover/mouseout)
    console.log('relatedTarget:', e.relatedTarget);
    
    // Movement
    console.log('movementX/Y:', e.movementX, e.movementY); // Mouse movement delta
}

// Practical mouse event usage
class DragAndDrop {
    constructor(element) {
        this.element = element;
        this.isDragging = false;
        this.startPos = { x: 0, y: 0 };
        this.currentPos = { x: 0, y: 0 };
        
        this.setupDragEvents();
    }
    
    setupDragEvents() {
        this.element.addEventListener('mousedown', this.startDrag.bind(this));
        document.addEventListener('mousemove', this.drag.bind(this));
        document.addEventListener('mouseup', this.endDrag.bind(this));
    }
    
    startDrag(e) {
        this.isDragging = true;
        this.startPos = { x: e.clientX, y: e.clientY };
        this.element.style.cursor = 'grabbing';
        e.preventDefault();
    }
    
    drag(e) {
        if (!this.isDragging) return;
        
        const deltaX = e.clientX - this.startPos.x;
        const deltaY = e.clientY - this.startPos.y;
        
        this.element.style.transform = `translate(${deltaX}px, ${deltaY}px)`;
    }
    
    endDrag(e) {
        if (!this.isDragging) return;
        
        this.isDragging = false;
        this.element.style.cursor = 'grab';
        
        // Emit custom event with final position
        this.element.dispatchEvent(new CustomEvent('dragEnd', {
            detail: {
                startPos: this.startPos,
                endPos: { x: e.clientX, y: e.clientY },
                deltaX: e.clientX - this.startPos.x,
                deltaY: e.clientY - this.startPos.y
            }
        }));
    }
}
```

#### **Keyboard Event Properties**

```javascript
function handleKeyboardEvent(e) {
    // Key identification
    console.log('key:', e.key);                 // 'a', 'Enter', 'ArrowUp', etc.
    console.log('code:', e.code);               // 'KeyA', 'Enter', 'ArrowUp', etc.
    console.log('keyCode:', e.keyCode);         // Deprecated but still used
    
    // Event type
    console.log('type:', e.type);               // 'keydown', 'keyup', 'keypress'
    
    // Modifier keys
    console.log('altKey:', e.altKey);
    console.log('ctrlKey:', e.ctrlKey);
    console.log('shiftKey:', e.shiftKey);
    console.log('metaKey:', e.metaKey);
    
    // Repeat detection
    console.log('repeat:', e.repeat);           // True if key is being held down
}

// Advanced keyboard handling
class KeyboardHandler {
    constructor() {
        this.pressedKeys = new Set();
        this.shortcuts = new Map();
        this.setupKeyboardEvents();
    }
    
    setupKeyboardEvents() {
        document.addEventListener('keydown', this.handleKeyDown.bind(this));
        document.addEventListener('keyup', this.handleKeyUp.bind(this));
        
        // Prevent default for certain keys
        document.addEventListener('keydown', (e) => {
            // Prevent F5 refresh
            if (e.key === 'F5') {
                e.preventDefault();
            }
            
            // Prevent Ctrl+S save dialog
            if (e.ctrlKey && e.key === 's') {
                e.preventDefault();
            }
        });
    }
    
    handleKeyDown(e) {
        const keyCombo = this.getKeyCombo(e);
        this.pressedKeys.add(e.code);
        
        // Execute shortcut if registered
        if (this.shortcuts.has(keyCombo)) {
            e.preventDefault();
            this.shortcuts.get(keyCombo)(e);
        }
        
        // Handle special keys
        switch (e.key) {
            case 'Escape':
                this.handleEscape(e);
                break;
            case 'Tab':
                this.handleTab(e);
                break;
            case 'Enter':
                this.handleEnter(e);
                break;
        }
    }
    
    handleKeyUp(e) {
        this.pressedKeys.delete(e.code);
    }
    
    getKeyCombo(e) {
        const modifiers = [];
        if (e.ctrlKey) modifiers.push('Ctrl');
        if (e.altKey) modifiers.push('Alt');
        if (e.shiftKey) modifiers.push('Shift');
        if (e.metaKey) modifiers.push('Meta');
        
        return [...modifiers, e.key].join('+');
    }
    
    registerShortcut(keyCombo, handler) {
        this.shortcuts.set(keyCombo, handler);
    }
    
    isPressed(keyCode) {
        return this.pressedKeys.has(keyCode);
    }
    
    handleEscape(e) {
        // Close modals, clear selections, etc.
        document.querySelectorAll('.modal.open').forEach(modal => {
            modal.classList.remove('open');
        });
    }
    
    handleTab(e) {
        // Trap focus in modals
        const modal = document.querySelector('.modal.open');
        if (modal) {
            this.trapFocus(e, modal);
        }
    }
    
    trapFocus(e, container) {
        const focusableElements = container.querySelectorAll(
            'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );
        
        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];
        
        if (e.shiftKey && document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
        } else if (!e.shiftKey && document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
        }
    }
}

// Usage
const keyHandler = new KeyboardHandler();
keyHandler.registerShortcut('Ctrl+k', () => console.log('Command palette'));
keyHandler.registerShortcut('Ctrl+/', () => console.log('Show shortcuts'));
```

---

## 3. Storage Mechanisms

> **Interview Explanation:** Browser storage mechanisms allow web applications to persist data locally. Understanding the differences, limitations, and use cases of each storage type is crucial for building efficient web applications.

### 🎯 LocalStorage vs SessionStorage

> **Interview Key Point:** Both localStorage and sessionStorage use the same API but differ in persistence and scope. This is a fundamental distinction that interviewers often ask about.

#### **Key Differences**

```javascript
// LocalStorage - Persists until manually cleared
localStorage.setItem('user', JSON.stringify({
    id: 123,
    name: 'John Doe',
    preferences: { theme: 'dark' }
}));

// SessionStorage - Persists only for the session
sessionStorage.setItem('tempData', JSON.stringify({
    formData: { step: 2, values: {} },
    timestamp: Date.now()
}));

// Comparison
console.log('localStorage scope:', 'Origin (protocol + domain + port)');
console.log('sessionStorage scope:', 'Tab/Window specific');
console.log('localStorage persistence:', 'Until manually cleared');
console.log('sessionStorage persistence:', 'Until tab/window closed');

// Storage size (typically 5-10MB)
console.log('Typical storage limit:', '5-10MB per origin');
```

#### **Storage API Methods**

```javascript
class WebStorage {
    constructor(storageType = 'localStorage') {
        this.storage = window[storageType];
        this.prefix = 'app_';
    }
    
    // Set item with automatic JSON serialization
    setItem(key, value, expiration = null) {
        try {
            const item = {
                value: value,
                timestamp: Date.now(),
                expiration: expiration ? Date.now() + expiration : null
            };
            
            this.storage.setItem(this.prefix + key, JSON.stringify(item));
            return true;
        } catch (error) {
            this.handleStorageError(error);
            return false;
        }
    }
    
    // Get item with automatic JSON parsing and expiration check
    getItem(key) {
        try {
            const itemStr = this.storage.getItem(this.prefix + key);
            if (!itemStr) return null;
            
            const item = JSON.parse(itemStr);
            
            // Check expiration
            if (item.expiration && Date.now() > item.expiration) {
                this.removeItem(key);
                return null;
            }
            
            return item.value;
        } catch (error) {
            this.handleStorageError(error);
            return null;
        }
    }
    
    // Remove item
    removeItem(key) {
        try {
            this.storage.removeItem(this.prefix + key);
            return true;
        } catch (error) {
            this.handleStorageError(error);
            return false;
        }
    }
    
    // Clear all items with prefix
    clear() {
        try {
            const keys = Object.keys(this.storage);
            keys.forEach(key => {
                if (key.startsWith(this.prefix)) {
                    this.storage.removeItem(key);
                }
            });
            return true;
        } catch (error) {
            this.handleStorageError(error);
            return false;
        }
    }
    
    // Get all items with prefix
    getAllItems() {
        const items = {};
        try {
            for (let i = 0; i < this.storage.length; i++) {
                const key = this.storage.key(i);
                if (key && key.startsWith(this.prefix)) {
                    const cleanKey = key.replace(this.prefix, '');
                    items[cleanKey] = this.getItem(cleanKey);
                }
            }
            return items;
        } catch (error) {
            this.handleStorageError(error);
            return {};
        }
    }
    
    // Check available storage space
    getStorageSize() {
        let total = 0;
        try {
            for (let key in this.storage) {
                if (this.storage.hasOwnProperty(key)) {
                    total += this.storage[key].length + key.length;
                }
            }
            return total;
        } catch (error) {
            return 0;
        }
    }
    
    // Test storage availability and quota
    testStorageQuota() {
        const testKey = this.prefix + 'quota_test';
        const chunk = '0'.repeat(1024); // 1KB
        let size = 0;
        
        try {
            while (true) {
                this.storage.setItem(testKey, chunk.repeat(size));
                size++;
            }
        } catch (error) {
            this.storage.removeItem(testKey);
            return (size - 1) * 1024; // Return in bytes
        }
    }
    
    handleStorageError(error) {
        if (error.name === 'QuotaExceededError') {
            console.warn('Storage quota exceeded');
            this.cleanupExpiredItems();
        } else if (error.name === 'SecurityError') {
            console.warn('Storage access denied (private browsing?)');
        } else {
            console.error('Storage error:', error);
        }
    }
    
    cleanupExpiredItems() {
        const keys = Object.keys(this.storage);
        keys.forEach(key => {
            if (key.startsWith(this.prefix)) {
                try {
                    const item = JSON.parse(this.storage.getItem(key));
                    if (item.expiration && Date.now() > item.expiration) {
                        this.storage.removeItem(key);
                    }
                } catch (error) {
                    // Remove corrupted items
                    this.storage.removeItem(key);
                }
            }
        });
    }
}

// Usage examples
const localStorage = new WebStorage('localStorage');
const sessionStorage = new WebStorage('sessionStorage');

// Store user preferences (persistent)
localStorage.setItem('userPrefs', {
    theme: 'dark',
    language: 'en',
    notifications: true
});

// Store form data (session only)
sessionStorage.setItem('formDraft', {
    title: 'Draft title',
    content: 'Draft content...'
}, 30 * 60 * 1000); // 30 minutes expiration
```

### 🎯 Cookies

> **Interview Key Point:** Cookies are the oldest storage mechanism and are automatically sent with HTTP requests. Understanding cookie attributes and limitations is important for security and performance.

#### **Cookie Management**

```javascript
class CookieManager {
    // Set cookie with all options
    setCookie(name, value, options = {}) {
        let cookieString = `${encodeURIComponent(name)}=${encodeURIComponent(value)}`;
        
        // Expiration (Date object or days)
        if (options.expires) {
            if (typeof options.expires === 'number') {
                const date = new Date();
                date.setTime(date.getTime() + (options.expires * 24 * 60 * 60 * 1000));
                cookieString += `; expires=${date.toUTCString()}`;
            } else {
                cookieString += `; expires=${options.expires.toUTCString()}`;
            }
        }
        
        // Max-Age (seconds)
        if (options.maxAge) {
            cookieString += `; max-age=${options.maxAge}`;
        }
        
        // Domain
        if (options.domain) {
            cookieString += `; domain=${options.domain}`;
        }
        
        // Path
        if (options.path) {
            cookieString += `; path=${options.path}`;
        }
        
        // Security flags
        if (options.secure) {
            cookieString += `; secure`;
        }
        
        if (options.httpOnly) {
            cookieString += `; httponly`;
        }
        
        // SameSite attribute
        if (options.sameSite) {
            cookieString += `; samesite=${options.sameSite}`;
        }
        
        document.cookie = cookieString;
    }
    
    // Get cookie value
    getCookie(name) {
        const encodedName = encodeURIComponent(name);
        const cookies = document.cookie.split(';');
        
        for (let cookie of cookies) {
            let [cookieName, cookieValue] = cookie.trim().split('=');
            if (cookieName === encodedName) {
                return decodeURIComponent(cookieValue);
            }
        }
        
        return null;
    }
    
    // Get all cookies as object
    getAllCookies() {
        const cookies = {};
        document.cookie.split(';').forEach(cookie => {
            const [name, value] = cookie.trim().split('=');
            if (name && value) {
                cookies[decodeURIComponent(name)] = decodeURIComponent(value);
            }
        });
        return cookies;
    }
    
    // Delete cookie
    deleteCookie(name, options = {}) {
        this.setCookie(name, '', {
            ...options,
            expires: new Date(0)
        });
    }
    
    // Check if cookies are enabled
    areCookiesEnabled() {
        const testCookie = 'test_cookie';
        this.setCookie(testCookie, 'test');
        const enabled = this.getCookie(testCookie) === 'test';
        this.deleteCookie(testCookie);
        return enabled;
    }
    
    // Cookie consent management
    setConsentCookie(consentData) {
        this.setCookie('cookie_consent', JSON.stringify({
            ...consentData,
            timestamp: Date.now(),
            version: '1.0'
        }), {
            expires: 365, // 1 year
            secure: true,
            sameSite: 'Strict'
        });
    }
    
    getConsentStatus() {
        const consent = this.getCookie('cookie_consent');
        return consent ? JSON.parse(consent) : null;
    }
}

// Usage
const cookieManager = new CookieManager();

// Set authentication cookie
cookieManager.setCookie('auth_token', 'abc123', {
    expires: 7, // 7 days
    secure: true,
    httpOnly: false, // Can't set httpOnly from JavaScript
    sameSite: 'Strict',
    path: '/'
});

// Set preferences cookie
cookieManager.setCookie('user_prefs', JSON.stringify({
    theme: 'dark',
    language: 'en'
}), {
    expires: 30,
    secure: true,
    sameSite: 'Lax'
});
```

### 🎯 IndexedDB

> **Interview Key Point:** IndexedDB is a powerful, asynchronous database for storing large amounts of structured data. It's more complex but much more capable than other storage options.

#### **IndexedDB Wrapper Class**

```javascript
class IndexedDBManager {
    constructor(dbName, version = 1) {
        this.dbName = dbName;
        this.version = version;
        this.db = null;
        this.stores = new Map();
    }
    
    // Initialize database
    async init(storeConfigs = []) {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.version);
            
            request.onerror = () => {
                reject(new Error(`Failed to open database: ${request.error}`));
            };
            
            request.onsuccess = () => {
                this.db = request.result;
                resolve(this.db);
            };
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                
                // Create object stores
                storeConfigs.forEach(config => {
                    if (!db.objectStoreNames.contains(config.name)) {
                        const store = db.createObjectStore(config.name, {
                            keyPath: config.keyPath || 'id',
                            autoIncrement: config.autoIncrement || false
                        });
                        
                        // Create indexes
                        if (config.indexes) {
                            config.indexes.forEach(index => {
                                store.createIndex(index.name, index.keyPath, {
                                    unique: index.unique || false
                                });
                            });
                        }
                    }
                });
            };
        });
    }
    
    // Add or update record
    async put(storeName, data) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);
            const request = store.put(data);
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    // Get record by key
    async get(storeName, key) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const request = store.get(key);
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    // Get all records
    async getAll(storeName, query = null, count = null) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const request = store.getAll(query, count);
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    // Delete record
    async delete(storeName, key) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);
            const request = store.delete(key);
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    // Query by index
    async getByIndex(storeName, indexName, key) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const index = store.index(indexName);
            const request = index.get(key);
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    // Advanced cursor-based iteration
    async iterate(storeName, callback, direction = 'next') {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const request = store.openCursor(null, direction);
            
            request.onsuccess = (event) => {
                const cursor = event.target.result;
                if (cursor) {
                    const continueIteration = callback(cursor.value, cursor.key);
                    if (continueIteration !== false) {
                        cursor.continue();
                    }
                } else {
                    resolve();
                }
            };
            
            request.onerror = () => reject(request.error);
        });
    }
    
    // Bulk operations
    async bulkPut(storeName, records) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);
            let completed = 0;
            
            const results = [];
            
            transaction.oncomplete = () => resolve(results);
            transaction.onerror = () => reject(transaction.error);
            
            records.forEach((record, index) => {
                const request = store.put(record);
                request.onsuccess = () => {
                    results[index] = request.result;
                    completed++;
                };
            });
        });
    }
    
    // Count records
    async count(storeName, query = null) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const request = store.count(query);
            
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }
    
    // Clear store
    async clear(storeName) {
        return new Promise((resolve, reject) => {
            const transaction = this.db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);
            const request = store.clear();
            
            request.onsuccess = () => resolve();
            request.onerror = () => reject(request.error);
        });
    }
}

// Usage example
async function setupOfflineStorage() {
    const db = new IndexedDBManager('OfflineApp', 1);
    
    await db.init([
        {
            name: 'users',
            keyPath: 'id',
            autoIncrement: true,
            indexes: [
                { name: 'email', keyPath: 'email', unique: true },
                { name: 'name', keyPath: 'name' }
            ]
        },
        {
            name: 'posts',
            keyPath: 'id',
            autoIncrement: true,
            indexes: [
                { name: 'userId', keyPath: 'userId' },
                { name: 'createdAt', keyPath: 'createdAt' }
            ]
        }
    ]);
    
    // Add user
    await db.put('users', {
        name: 'John Doe',
        email: 'john@example.com',
        createdAt: new Date()
    });
    
    // Get user by email
    const user = await db.getByIndex('users', 'email', 'john@example.com');
    
    // Add posts
    await db.bulkPut('posts', [
        { userId: user.id, title: 'Post 1', content: 'Content 1', createdAt: new Date() },
        { userId: user.id, title: 'Post 2', content: 'Content 2', createdAt: new Date() }
    ]);
    
    return db;
}
```

### 🎯 Cache API

> **Interview Key Point:** The Cache API is part of the Service Worker specification and provides programmatic cache management for network requests and responses.

#### **Cache API Implementation**

```javascript
class CacheManager {
    constructor(cacheName = 'app-cache-v1') {
        this.cacheName = cacheName;
        this.cache = null;
    }
    
    // Initialize cache
    async init() {
        this.cache = await caches.open(this.cacheName);
        return this.cache;
    }
    
    // Add single request to cache
    async add(request) {
        return this.cache.add(request);
    }
    
    // Add multiple requests to cache
    async addAll(requests) {
        return this.cache.addAll(requests);
    }
    
    // Put request/response pair in cache
    async put(request, response) {
        return this.cache.put(request, response);
    }
    
    // Get response from cache
    async match(request, options = {}) {
        return this.cache.match(request, options);
    }
    
    // Get all cached requests
    async keys(request = null, options = {}) {
        return this.cache.keys(request, options);
    }
    
    // Delete cached request
    async delete(request, options = {}) {
        return this.cache.delete(request, options);
    }
    
    // Cache with fallback strategy
    async cacheWithFallback(request, fallbackResponse) {
        try {
            // Try to fetch from network first
            const networkResponse = await fetch(request);
            if (networkResponse.ok) {
                // Cache successful response
                await this.put(request, networkResponse.clone());
                return networkResponse;
            }
        } catch (error) {
            console.warn('Network request failed:', error);
        }
        
        // Try cache
        const cachedResponse = await this.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Return fallback
        return fallbackResponse;
    }
    
    // Cache first strategy
    async cacheFirst(request, maxAge = 86400000) { // 24 hours default
        const cachedResponse = await this.match(request);
        
        if (cachedResponse) {
            const cachedDate = new Date(cachedResponse.headers.get('date'));
            const now = new Date();
            
            if (now.getTime() - cachedDate.getTime() < maxAge) {
                return cachedResponse;
            }
        }
        
        // Cache miss or expired, fetch from network
        try {
            const networkResponse = await fetch(request);
            if (networkResponse.ok) {
                await this.put(request, networkResponse.clone());
            }
            return networkResponse;
        } catch (error) {
            // Return stale cache if network fails
            return cachedResponse || new Response('Network error', { status: 503 });
        }
    }
    
    // Network first strategy
    async networkFirst(request, timeout = 3000) {
        try {
            const networkPromise = fetch(request);
            const timeoutPromise = new Promise((_, reject) => {
                setTimeout(() => reject(new Error('Network timeout')), timeout);
            });
            
            const networkResponse = await Promise.race([networkPromise, timeoutPromise]);
            
            if (networkResponse.ok) {
                await this.put(request, networkResponse.clone());
            }
            
            return networkResponse;
        } catch (error) {
            console.warn('Network request failed, trying cache:', error);
            const cachedResponse = await this.match(request);
            return cachedResponse || new Response('Not found', { status: 404 });
        }
    }
    
    // Cleanup old cache entries
    async cleanup(maxEntries = 100, maxAge = 2592000000) { // 30 days
        const requests = await this.keys();
        
        // Sort by last modified (if available) or creation time
        const sortedRequests = requests.sort((a, b) => {
            // This is a simplified sort - in practice you'd need metadata
            return a.url.localeCompare(b.url);
        });
        
        // Remove old entries
        if (sortedRequests.length > maxEntries) {
            const toDelete = sortedRequests.slice(0, sortedRequests.length - maxEntries);
            await Promise.all(toDelete.map(request => this.delete(request)));
        }
        
        // Remove expired entries
        const now = new Date();
        for (const request of sortedRequests) {
            const response = await this.match(request);
            if (response) {
                const date = new Date(response.headers.get('date'));
                if (now.getTime() - date.getTime() > maxAge) {
                    await this.delete(request);
                }
            }
        }
    }
    
    // Get cache statistics
    async getStats() {
        const requests = await this.keys();
        let totalSize = 0;
        
        for (const request of requests) {
            const response = await this.match(request);
            if (response) {
                const blob = await response.blob();
                totalSize += blob.size;
            }
        }
        
        return {
            entries: requests.length,
            totalSize: totalSize,
            cacheName: this.cacheName
        };
    }
}

// Usage in Service Worker or main thread
async function setupCaching() {
    const cacheManager = new CacheManager('app-v1');
    await cacheManager.init();
    
    // Cache essential resources
    await cacheManager.addAll([
        '/',
        '/styles/main.css',
        '/scripts/app.js',
        '/offline.html'
    ]);
    
    // Handle fetch events with caching strategies
    self.addEventListener('fetch', async (event) => {
        const request = event.request;
        
        if (request.url.includes('/api/')) {
            // Network first for API calls
            event.respondWith(cacheManager.networkFirst(request, 2000));
        } else if (request.url.includes('/static/')) {
            // Cache first for static assets
            event.respondWith(cacheManager.cacheFirst(request));
        } else {
            // Cache with fallback for pages
            const fallback = await caches.match('/offline.html');
            event.respondWith(cacheManager.cacheWithFallback(request, fallback));
        }
    });
    
    return cacheManager;
}
```

> **Interview Tip:** Choose the right storage mechanism based on your needs:
> - **Cookies**: Small data that needs to be sent to server (≤4KB)
> - **localStorage**: Persistent client-side data (≤10MB)
> - **sessionStorage**: Temporary client-side data (≤10MB)
> - **IndexedDB**: Large, structured data with complex queries (≤250MB+)
> - **Cache API**: Network request/response caching for offline functionality

> **Interview Tip:** Choose the right storage mechanism based on your needs:
>
> - **Cookies**: Small data that needs to be sent to server (≤4KB)
> - **localStorage**: Persistent client-side data (≤10MB)
> - **sessionStorage**: Temporary client-side data (≤10MB)
> - **IndexedDB**: Large, structured data with complex queries (≤250MB+)
> - **Cache API**: Network request/response caching for offline functionality

---

## 4. Web APIs

> **Interview Explanation:** Web APIs provide powerful capabilities that extend beyond basic JavaScript. Understanding these APIs is crucial for building modern web applications with features like geolocation, background processing, and real-time updates.

### 🎯 Fetch API

> **Interview Key Point:** The Fetch API is the modern replacement for XMLHttpRequest. It uses Promises and provides a more flexible and powerful interface for network requests.

#### **Basic Fetch Operations**

```javascript
// Basic fetch with error handling
async function basicFetch() {
    try {
        const response = await fetch('/api/users');
        
        // Check if response is ok (status 200-299)
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

// Different response types
async function handleDifferentResponseTypes() {
    try {
        const response = await fetch('/api/data');
        
        // Check content type
        const contentType = response.headers.get('content-type');
        
        if (contentType?.includes('application/json')) {
            return await response.json();
        } else if (contentType?.includes('text/')) {
            return await response.text();
        } else if (contentType?.includes('image/')) {
            return await response.blob();
        } else {
            return await response.arrayBuffer();
        }
    } catch (error) {
        console.error('Response parsing error:', error);
        throw error;
    }
}
```

#### **Advanced Fetch Configuration**

```javascript
class FetchClient {
    constructor(baseURL = '', defaultOptions = {}) {
        this.baseURL = baseURL;
        this.defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
            ...defaultOptions
        };
        this.interceptors = {
            request: [],
            response: []
        };
    }
    
    // Add request interceptor
    addRequestInterceptor(interceptor) {
        this.interceptors.request.push(interceptor);
    }
    
    // Add response interceptor
    addResponseInterceptor(interceptor) {
        this.interceptors.response.push(interceptor);
    }
    
    // Apply request interceptors
    async applyRequestInterceptors(url, options) {
        let modifiedUrl = url;
        let modifiedOptions = options;
        
        for (const interceptor of this.interceptors.request) {
            const result = await interceptor(modifiedUrl, modifiedOptions);
            modifiedUrl = result.url || modifiedUrl;
            modifiedOptions = result.options || modifiedOptions;
        }
        
        return { url: modifiedUrl, options: modifiedOptions };
    }
    
    // Apply response interceptors
    async applyResponseInterceptors(response) {
        let modifiedResponse = response;
        
        for (const interceptor of this.interceptors.response) {
            modifiedResponse = await interceptor(modifiedResponse);
        }
        
        return modifiedResponse;
    }
    
    // Main fetch method
    async fetch(url, options = {}) {
        const fullURL = this.baseURL + url;
        const mergedOptions = {
            ...this.defaultOptions,
            ...options,
            headers: {
                ...this.defaultOptions.headers,
                ...options.headers
            }
        };
        
        // Apply request interceptors
        const { url: finalURL, options: finalOptions } = 
            await this.applyRequestInterceptors(fullURL, mergedOptions);
        
        try {
            const response = await fetch(finalURL, finalOptions);
            
            // Apply response interceptors
            const finalResponse = await this.applyResponseInterceptors(response);
            
            return finalResponse;
        } catch (error) {
            console.error('Fetch error:', error);
            throw error;
        }
    }
    
    // Convenience methods
    async get(url, options = {}) {
        return this.fetch(url, { ...options, method: 'GET' });
    }
    
    async post(url, data, options = {}) {
        return this.fetch(url, {
            ...options,
            method: 'POST',
            body: JSON.stringify(data)
        });
    }
    
    async put(url, data, options = {}) {
        return this.fetch(url, {
            ...options,
            method: 'PUT',
            body: JSON.stringify(data)
        });
    }
    
    async delete(url, options = {}) {
        return this.fetch(url, { ...options, method: 'DELETE' });
    }
    
    // File upload with progress
    async uploadFile(url, file, onProgress = null) {
        return new Promise((resolve, reject) => {
            const xhr = new XMLHttpRequest();
            const formData = new FormData();
            formData.append('file', file);
            
            if (onProgress) {
                xhr.upload.addEventListener('progress', (e) => {
                    if (e.lengthComputable) {
                        const progress = (e.loaded / e.total) * 100;
                        onProgress(progress);
                    }
                });
            }
            
            xhr.addEventListener('load', () => {
                if (xhr.status >= 200 && xhr.status < 300) {
                    try {
                        const response = JSON.parse(xhr.responseText);
                        resolve(response);
                    } catch (error) {
                        resolve(xhr.responseText);
                    }
                } else {
                    reject(new Error(`Upload failed: ${xhr.status}`));
                }
            });
            
            xhr.addEventListener('error', () => {
                reject(new Error('Upload failed'));
            });
            
            xhr.open('POST', this.baseURL + url);
            xhr.send(formData);
        });
    }
    
    // Request with timeout
    async fetchWithTimeout(url, options = {}, timeout = 5000) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeout);
        
        try {
            const response = await this.fetch(url, {
                ...options,
                signal: controller.signal
            });
            clearTimeout(timeoutId);
            return response;
        } catch (error) {
            clearTimeout(timeoutId);
            if (error.name === 'AbortError') {
                throw new Error(`Request timeout after ${timeout}ms`);
            }
            throw error;
        }
    }
    
    // Retry mechanism
    async fetchWithRetry(url, options = {}, maxRetries = 3, retryDelay = 1000) {
        let lastError;
        
        for (let attempt = 0; attempt <= maxRetries; attempt++) {
            try {
                return await this.fetch(url, options);
            } catch (error) {
                lastError = error;
                
                if (attempt < maxRetries) {
                    const delay = retryDelay * Math.pow(2, attempt); // Exponential backoff
                    console.warn(`Request failed, retrying in ${delay}ms... (attempt ${attempt + 1}/${maxRetries})`);
                    await new Promise(resolve => setTimeout(resolve, delay));
                }
            }
        }
        
        throw lastError;
    }
}

// Usage example
const api = new FetchClient('/api');

// Add authentication interceptor
api.addRequestInterceptor(async (url, options) => {
    const token = localStorage.getItem('authToken');
    if (token) {
        options.headers.Authorization = `Bearer ${token}`;
    }
    return { url, options };
});

// Add error handling interceptor
api.addResponseInterceptor(async (response) => {
    if (response.status === 401) {
        // Handle authentication error
        localStorage.removeItem('authToken');
        window.location.href = '/login';
    }
    return response;
});
```

### 🎯 Geolocation API

> **Interview Key Point:** The Geolocation API provides access to the user's location with their permission. Understanding accuracy, privacy, and error handling is important.

#### **Geolocation Implementation**

```javascript
class GeolocationManager {
    constructor() {
        this.isSupported = 'geolocation' in navigator;
        this.watchId = null;
        this.currentPosition = null;
    }
    
    // Check if geolocation is supported
    checkSupport() {
        if (!this.isSupported) {
            throw new Error('Geolocation is not supported by this browser');
        }
    }
    
    // Get current position (one-time)
    async getCurrentPosition(options = {}) {
        this.checkSupport();
        
        const defaultOptions = {
            enableHighAccuracy: true,
            timeout: 10000,
            maximumAge: 60000 // 1 minute
        };
        
        const finalOptions = { ...defaultOptions, ...options };
        
        return new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    this.currentPosition = position;
                    resolve(this.formatPosition(position));
                },
                (error) => {
                    reject(this.handleGeolocationError(error));
                },
                finalOptions
            );
        });
    }
    
    // Watch position changes
    watchPosition(callback, errorCallback = null, options = {}) {
        this.checkSupport();
        
        const defaultOptions = {
            enableHighAccuracy: true,
            timeout: 15000,
            maximumAge: 30000
        };
        
        const finalOptions = { ...defaultOptions, ...options };
        
        this.watchId = navigator.geolocation.watchPosition(
            (position) => {
                this.currentPosition = position;
                callback(this.formatPosition(position));
            },
            (error) => {
                const formattedError = this.handleGeolocationError(error);
                if (errorCallback) {
                    errorCallback(formattedError);
                } else {
                    console.error('Geolocation error:', formattedError);
                }
            },
            finalOptions
        );
        
        return this.watchId;
    }
    
    // Stop watching position
    stopWatching() {
        if (this.watchId !== null) {
            navigator.geolocation.clearWatch(this.watchId);
            this.watchId = null;
        }
    }
    
    // Format position data
    formatPosition(position) {
        return {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy,
            altitude: position.coords.altitude,
            altitudeAccuracy: position.coords.altitudeAccuracy,
            heading: position.coords.heading,
            speed: position.coords.speed,
            timestamp: position.timestamp
        };
    }
    
    // Handle geolocation errors
    handleGeolocationError(error) {
        switch (error.code) {
            case error.PERMISSION_DENIED:
                return {
                    code: 'PERMISSION_DENIED',
                    message: 'User denied the request for Geolocation.',
                    userMessage: 'Please allow location access to use this feature.'
                };
            case error.POSITION_UNAVAILABLE:
                return {
                    code: 'POSITION_UNAVAILABLE',
                    message: 'Location information is unavailable.',
                    userMessage: 'Unable to determine your location. Please try again.'
                };
            case error.TIMEOUT:
                return {
                    code: 'TIMEOUT',
                    message: 'The request to get user location timed out.',
                    userMessage: 'Location request timed out. Please try again.'
                };
            default:
                return {
                    code: 'UNKNOWN_ERROR',
                    message: 'An unknown error occurred.',
                    userMessage: 'An error occurred while getting your location.'
                };
        }
    }
    
    // Calculate distance between two points (Haversine formula)
    calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371; // Radius of the Earth in kilometers
        const dLat = this.toRadians(lat2 - lat1);
        const dLon = this.toRadians(lon2 - lon1);
        
        const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                  Math.cos(this.toRadians(lat1)) * Math.cos(this.toRadians(lat2)) *
                  Math.sin(dLon / 2) * Math.sin(dLon / 2);
        
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        const distance = R * c;
        
        return distance;
    }
    
    toRadians(degrees) {
        return degrees * (Math.PI / 180);
    }
    
    // Get address from coordinates (requires geocoding service)
    async getAddressFromCoordinates(lat, lon) {
        try {
            // Using a free geocoding service (replace with your preferred service)
            const response = await fetch(
                `https://api.bigdatacloud.net/data/reverse-geocode-client?latitude=${lat}&longitude=${lon}&localityLanguage=en`
            );
            
            if (!response.ok) {
                throw new Error('Geocoding failed');
            }
            
            const data = await response.json();
            return {
                address: data.locality || data.city || data.principalSubdivision,
                country: data.countryName,
                fullAddress: data.locality + ', ' + data.principalSubdivision + ', ' + data.countryName
            };
        } catch (error) {
            console.error('Geocoding error:', error);
            return null;
        }
    }
    
    // Check if user is within a certain area
    async isWithinArea(centerLat, centerLon, radiusKm) {
        try {
            const position = await this.getCurrentPosition();
            const distance = this.calculateDistance(
                position.latitude,
                position.longitude,
                centerLat,
                centerLon
            );
            
            return {
                isWithin: distance <= radiusKm,
                distance: distance,
                position: position
            };
        } catch (error) {
            throw error;
        }
    }
}

// Usage example
const geoManager = new GeolocationManager();

// Get current location
async function getCurrentLocation() {
    try {
        const position = await geoManager.getCurrentPosition({
            enableHighAccuracy: true,
            timeout: 5000
        });
        
        console.log('Current position:', position);
        
        // Get address
        const address = await geoManager.getAddressFromCoordinates(
            position.latitude,
            position.longitude
        );
        
        console.log('Address:', address);
        
        return { position, address };
    } catch (error) {
        console.error('Location error:', error);
        alert(error.userMessage || 'Failed to get location');
    }
}

// Watch position changes
function startLocationTracking() {
    return geoManager.watchPosition(
        (position) => {
            console.log('Position updated:', position);
            updateMapMarker(position);
        },
        (error) => {
            console.error('Location tracking error:', error);
        },
        { enableHighAccuracy: true, maximumAge: 5000 }
    );
}
```

### 🎯 Web Workers

> **Interview Key Point:** Web Workers allow you to run JavaScript in the background without blocking the main UI thread. This is crucial for CPU-intensive tasks.

#### **Web Worker Implementation**

```javascript
// Main thread - Worker Manager
class WorkerManager {
    constructor() {
        this.workers = new Map();
        this.taskQueue = [];
        this.results = new Map();
    }
    
    // Create a new worker
    createWorker(name, scriptPath) {
        if (this.workers.has(name)) {
            this.terminateWorker(name);
        }
        
        const worker = new Worker(scriptPath);
        
        // Handle messages from worker
        worker.onmessage = (event) => {
            this.handleWorkerMessage(name, event.data);
        };
        
        // Handle worker errors
        worker.onerror = (error) => {
            console.error(`Worker ${name} error:`, error);
        };
        
        this.workers.set(name, worker);
        return worker;
    }
    
    // Send task to worker
    async sendTask(workerName, taskType, data, timeout = 10000) {
        const worker = this.workers.get(workerName);
        if (!worker) {
            throw new Error(`Worker ${workerName} not found`);
        }
        
        const taskId = this.generateTaskId();
        
        return new Promise((resolve, reject) => {
            // Set up timeout
            const timeoutId = setTimeout(() => {
                this.results.delete(taskId);
                reject(new Error(`Task ${taskId} timed out`));
            }, timeout);
            
            // Store resolver
            this.results.set(taskId, {
                resolve: (result) => {
                    clearTimeout(timeoutId);
                    resolve(result);
                },
                reject: (error) => {
                    clearTimeout(timeoutId);
                    reject(error);
                }
            });
            
            // Send task to worker
            worker.postMessage({
                taskId,
                type: taskType,
                data
            });
        });
    }
    
    // Handle messages from workers
    handleWorkerMessage(workerName, message) {
        const { taskId, type, data, error } = message;
        
        if (type === 'result') {
            const task = this.results.get(taskId);
            if (task) {
                this.results.delete(taskId);
                task.resolve(data);
            }
        } else if (type === 'error') {
            const task = this.results.get(taskId);
            if (task) {
                this.results.delete(taskId);
                task.reject(new Error(error));
            }
        } else if (type === 'progress') {
            // Handle progress updates
            this.handleProgress(taskId, data);
        }
    }
    
    // Handle progress updates
    handleProgress(taskId, progress) {
        const event = new CustomEvent('workerProgress', {
            detail: { taskId, progress }
        });
        document.dispatchEvent(event);
    }
    
    // Terminate worker
    terminateWorker(name) {
        const worker = this.workers.get(name);
        if (worker) {
            worker.terminate();
            this.workers.delete(name);
        }
    }
    
    // Terminate all workers
    terminateAllWorkers() {
        this.workers.forEach((worker, name) => {
            this.terminateWorker(name);
        });
    }
    
    generateTaskId() {
        return Math.random().toString(36).substr(2, 9);
    }
}

// Usage in main thread
const workerManager = new WorkerManager();

// Create workers
workerManager.createWorker('dataProcessor', '/workers/data-processor.js');
workerManager.createWorker('imageProcessor', '/workers/image-processor.js');

// Process large dataset
async function processLargeDataset(data) {
    try {
        const result = await workerManager.sendTask('dataProcessor', 'processData', {
            dataset: data,
            options: { algorithm: 'advanced' }
        });
        
        console.log('Processing complete:', result);
        return result;
    } catch (error) {
        console.error('Processing failed:', error);
        throw error;
    }
}

// Listen for progress updates
document.addEventListener('workerProgress', (event) => {
    const { taskId, progress } = event.detail;
    console.log(`Task ${taskId} progress: ${progress}%`);
    updateProgressBar(progress);
});
```

```javascript
// Worker script (data-processor.js)
class DataProcessor {
    constructor() {
        this.setupMessageHandler();
    }
    
    setupMessageHandler() {
        self.onmessage = (event) => {
            const { taskId, type, data } = event.data;
            
            try {
                switch (type) {
                    case 'processData':
                        this.processData(taskId, data);
                        break;
                    case 'sortData':
                        this.sortData(taskId, data);
                        break;
                    case 'filterData':
                        this.filterData(taskId, data);
                        break;
                    default:
                        this.sendError(taskId, `Unknown task type: ${type}`);
                }
            } catch (error) {
                this.sendError(taskId, error.message);
            }
        };
    }
    
    processData(taskId, { dataset, options }) {
        const total = dataset.length;
        const results = [];
        
        for (let i = 0; i < total; i++) {
            // Simulate heavy processing
            const processed = this.heavyComputation(dataset[i], options);
            results.push(processed);
            
            // Send progress updates
            if (i % 100 === 0) {
                const progress = (i / total) * 100;
                this.sendProgress(taskId, progress);
            }
        }
        
        this.sendResult(taskId, {
            processed: results,
            statistics: this.calculateStatistics(results)
        });
    }
    
    heavyComputation(item, options) {
        // Simulate CPU-intensive work
        let result = item;
        
        if (options.algorithm === 'advanced') {
            // Complex calculations
            for (let i = 0; i < 1000; i++) {
                result = Math.sqrt(result * Math.PI + i);
            }
        }
        
        return {
            original: item,
            processed: result,
            timestamp: Date.now()
        };
    }
    
    sortData(taskId, { dataset, sortBy, order }) {
        const sorted = [...dataset].sort((a, b) => {
            const aVal = a[sortBy];
            const bVal = b[sortBy];
            
            if (order === 'desc') {
                return bVal - aVal;
            }
            return aVal - bVal;
        });
        
        this.sendResult(taskId, sorted);
    }
    
    filterData(taskId, { dataset, filters }) {
        const filtered = dataset.filter(item => {
            return filters.every(filter => {
                const value = item[filter.field];
                switch (filter.operator) {
                    case 'equals':
                        return value === filter.value;
                    case 'greater':
                        return value > filter.value;
                    case 'less':
                        return value < filter.value;
                    case 'contains':
                        return String(value).includes(filter.value);
                    default:
                        return true;
                }
            });
        });
        
        this.sendResult(taskId, filtered);
    }
    
    calculateStatistics(data) {
        const values = data.map(item => item.processed);
        return {
            count: values.length,
            sum: values.reduce((a, b) => a + b, 0),
            avg: values.reduce((a, b) => a + b, 0) / values.length,
            min: Math.min(...values),
            max: Math.max(...values)
        };
    }
    
    sendResult(taskId, data) {
        self.postMessage({
            taskId,
            type: 'result',
            data
        });
    }
    
    sendError(taskId, error) {
        self.postMessage({
            taskId,
            type: 'error',
            error
        });
    }
    
    sendProgress(taskId, progress) {
        self.postMessage({
            taskId,
            type: 'progress',
            data: progress
        });
    }
}

// Initialize processor
const processor = new DataProcessor();
```

### 🎯 Service Workers

> **Interview Key Point:** Service Workers act as a proxy between your web app and the network, enabling offline functionality, background sync, and push notifications. They run on a separate thread and have no DOM access.

#### **Service Worker Lifecycle and Implementation**

```javascript
// Main thread - Service Worker registration and management
class ServiceWorkerManager {
    constructor() {
        this.registration = null;
        this.isSupported = 'serviceWorker' in navigator;
        this.updateFound = false;
    }
    
    // Register service worker
    async register(swPath = '/sw.js', options = {}) {
        if (!this.isSupported) {
            throw new Error('Service Workers are not supported');
        }
        
        try {
            this.registration = await navigator.serviceWorker.register(swPath, {
                scope: '/',
                ...options
            });
            
            console.log('ServiceWorker registered:', this.registration);
            
            // Set up event listeners
            this.setupEventListeners();
            
            return this.registration;
        } catch (error) {
            console.error('ServiceWorker registration failed:', error);
            throw error;
        }
    }
    
    setupEventListeners() {
        // Listen for updates
        this.registration.addEventListener('updatefound', () => {
            console.log('New service worker found');
            this.updateFound = true;
            const newWorker = this.registration.installing;
            
            newWorker.addEventListener('statechange', () => {
                console.log('Service worker state:', newWorker.state);
                
                if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                    // New version available
                    this.notifyUpdate();
                }
            });
        });
        
        // Listen for controller changes
        navigator.serviceWorker.addEventListener('controllerchange', () => {
            console.log('New service worker activated');
            window.location.reload();
        });
        
        // Listen for messages from service worker
        navigator.serviceWorker.addEventListener('message', (event) => {
            this.handleMessage(event.data);
        });
    }
    
    // Handle messages from service worker
    handleMessage(message) {
        switch (message.type) {
            case 'CACHE_UPDATED':
                console.log('Cache updated:', message.payload);
                break;
            case 'BACKGROUND_SYNC':
                console.log('Background sync completed:', message.payload);
                break;
            case 'PUSH_RECEIVED':
                console.log('Push notification received:', message.payload);
                break;
            default:
                console.log('Unknown message from SW:', message);
        }
    }
    
    // Send message to service worker
    async sendMessage(message) {
        if (!this.registration || !this.registration.active) {
            throw new Error('No active service worker');
        }
        
        this.registration.active.postMessage(message);
    }
    
    // Notify user of update
    notifyUpdate() {
        const event = new CustomEvent('swUpdate', {
            detail: { registration: this.registration }
        });
        document.dispatchEvent(event);
    }
    
    // Skip waiting and activate new service worker
    async skipWaiting() {
        if (this.registration && this.registration.waiting) {
            await this.sendMessage({ type: 'SKIP_WAITING' });
        }
    }
    
    // Unregister service worker
    async unregister() {
        if (this.registration) {
            const result = await this.registration.unregister();
            console.log('ServiceWorker unregistered:', result);
            return result;
        }
        return false;
    }
    
    // Check for updates manually
    async checkForUpdates() {
        if (this.registration) {
            await this.registration.update();
        }
    }
    
    // Get service worker state
    getState() {
        if (!this.registration) return 'not-registered';
        
        if (this.registration.installing) return 'installing';
        if (this.registration.waiting) return 'waiting';
        if (this.registration.active) return 'active';
        
        return 'unknown';
    }
}

// Service Worker script (sw.js)
class ServiceWorkerCore {
    constructor() {
        this.CACHE_NAME = 'app-cache-v1';
        this.STATIC_CACHE = 'static-v1';
        this.DYNAMIC_CACHE = 'dynamic-v1';
        
        this.STATIC_ASSETS = [
            '/',
            '/index.html',
            '/styles/main.css',
            '/scripts/app.js',
            '/offline.html'
        ];
        
        this.setupEventListeners();
    }
    
    setupEventListeners() {
        // Install event
        self.addEventListener('install', (event) => {
            console.log('ServiceWorker installing');
            event.waitUntil(this.handleInstall());
        });
        
        // Activate event
        self.addEventListener('activate', (event) => {
            console.log('ServiceWorker activating');
            event.waitUntil(this.handleActivate());
        });
        
        // Fetch event
        self.addEventListener('fetch', (event) => {
            event.respondWith(this.handleFetch(event.request));
        });
        
        // Background sync
        self.addEventListener('sync', (event) => {
            console.log('Background sync:', event.tag);
            event.waitUntil(this.handleBackgroundSync(event.tag));
        });
        
        // Push notifications
        self.addEventListener('push', (event) => {
            console.log('Push received:', event.data?.text());
            event.waitUntil(this.handlePush(event));
        });
        
        // Notification click
        self.addEventListener('notificationclick', (event) => {
            event.waitUntil(this.handleNotificationClick(event));
        });
        
        // Message from main thread
        self.addEventListener('message', (event) => {
            this.handleMessage(event);
        });
    }
    
    async handleInstall() {
        // Cache static assets
        const cache = await caches.open(this.STATIC_CACHE);
        await cache.addAll(this.STATIC_ASSETS);
        
        // Skip waiting to activate immediately
        await self.skipWaiting();
    }
    
    async handleActivate() {
        // Clean up old caches
        const cacheNames = await caches.keys();
        const deletePromises = cacheNames
            .filter(name => name !== this.STATIC_CACHE && name !== this.DYNAMIC_CACHE)
            .map(name => caches.delete(name));
        
        await Promise.all(deletePromises);
        
        // Take control of all pages
        await self.clients.claim();
        
        // Notify clients
        this.notifyClients({ type: 'ACTIVATED' });
    }
    
    async handleFetch(request) {
        const url = new URL(request.url);
        
        // Different strategies for different types of requests
        if (this.STATIC_ASSETS.includes(url.pathname)) {
            return this.cacheFirst(request);
        } else if (url.pathname.startsWith('/api/')) {
            return this.networkFirst(request);
        } else if (request.destination === 'image') {
            return this.cacheWithFallback(request);
        } else {
            return this.staleWhileRevalidate(request);
        }
    }
    
    // Cache first strategy
    async cacheFirst(request) {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        try {
            const networkResponse = await fetch(request);
            if (networkResponse.ok) {
                const cache = await caches.open(this.DYNAMIC_CACHE);
                cache.put(request, networkResponse.clone());
            }
            return networkResponse;
        } catch (error) {
            // Return offline page for navigation requests
            if (request.mode === 'navigate') {
                return caches.match('/offline.html');
            }
            throw error;
        }
    }
    
    // Network first strategy
    async networkFirst(request) {
        try {
            const networkResponse = await fetch(request);
            if (networkResponse.ok) {
                const cache = await caches.open(this.DYNAMIC_CACHE);
                cache.put(request, networkResponse.clone());
            }
            return networkResponse;
        } catch (error) {
            const cachedResponse = await caches.match(request);
            if (cachedResponse) {
                return cachedResponse;
            }
            throw error;
        }
    }
    
    // Stale while revalidate strategy
    async staleWhileRevalidate(request) {
        const cachedResponse = await caches.match(request);
        
        const fetchPromise = fetch(request).then(networkResponse => {
            if (networkResponse.ok) {
                const cache = caches.open(this.DYNAMIC_CACHE);
                cache.then(c => c.put(request, networkResponse.clone()));
            }
            return networkResponse;
        }).catch(() => {
            // Ignore network errors in background
        });
        
        return cachedResponse || fetchPromise;
    }
    
    // Cache with fallback
    async cacheWithFallback(request) {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) {
            return cachedResponse;
        }
        
        try {
            const networkResponse = await fetch(request);
            if (networkResponse.ok) {
                const cache = await caches.open(this.DYNAMIC_CACHE);
                cache.put(request, networkResponse.clone());
            }
            return networkResponse;
        } catch (error) {
            // Return placeholder image
            return caches.match('/images/placeholder.png');
        }
    }
    
    async handleBackgroundSync(tag) {
        switch (tag) {
            case 'background-sync-posts':
                await this.syncPosts();
                break;
            case 'background-sync-analytics':
                await this.syncAnalytics();
                break;
            default:
                console.log('Unknown sync tag:', tag);
        }
    }
    
    async syncPosts() {
        // Get pending posts from IndexedDB
        const pendingPosts = await this.getPendingPosts();
        
        for (const post of pendingPosts) {
            try {
                const response = await fetch('/api/posts', {
                    method: 'POST',
                    body: JSON.stringify(post),
                    headers: { 'Content-Type': 'application/json' }
                });
                
                if (response.ok) {
                    await this.removePendingPost(post.id);
                }
            } catch (error) {
                console.error('Failed to sync post:', error);
            }
        }
        
        this.notifyClients({
            type: 'BACKGROUND_SYNC',
            payload: { tag: 'posts', synced: pendingPosts.length }
        });
    }
    
    async handlePush(event) {
        const data = event.data ? event.data.json() : {};
        
        const options = {
            body: data.body || 'New notification',
            icon: data.icon || '/icons/icon-192.png',
            badge: data.badge || '/icons/badge.png',
            tag: data.tag || 'default',
            requireInteraction: data.requireInteraction || false,
            actions: data.actions || [],
            data: data.data || {}
        };
        
        await self.registration.showNotification(data.title || 'Notification', options);
    }
    
    async handleNotificationClick(event) {
        event.notification.close();
        
        const data = event.notification.data;
        const action = event.action;
        
        if (action === 'open') {
            await this.openWindow(data.url || '/');
        } else if (action === 'dismiss') {
            // Just close the notification
        } else {
            // Default action - open app
            await this.openWindow('/');
        }
    }
    
    async openWindow(url) {
        const clients = await self.clients.matchAll({ type: 'window' });
        
        // Check if window is already open
        for (const client of clients) {
            if (client.url === url && 'focus' in client) {
                return client.focus();
            }
        }
        
        // Open new window
        if (self.clients.openWindow) {
            return self.clients.openWindow(url);
        }
    }
    
    handleMessage(event) {
        const { type, payload } = event.data;
        
        switch (type) {
            case 'SKIP_WAITING':
                self.skipWaiting();
                break;
            case 'GET_VERSION':
                event.ports[0].postMessage({ version: this.CACHE_NAME });
                break;
            case 'CACHE_URLS':
                this.cacheUrls(payload.urls);
                break;
            default:
                console.log('Unknown message:', event.data);
        }
    }
    
    async cacheUrls(urls) {
        const cache = await caches.open(this.DYNAMIC_CACHE);
        await cache.addAll(urls);
        
        this.notifyClients({
            type: 'CACHE_UPDATED',
            payload: { urls }
        });
    }
    
    async notifyClients(message) {
        const clients = await self.clients.matchAll();
        clients.forEach(client => {
            client.postMessage(message);
        });
    }
    
    // Helper methods for IndexedDB operations
    async getPendingPosts() {
        // Implementation would use IndexedDB
        return [];
    }
    
    async removePendingPost(id) {
        // Implementation would use IndexedDB
    }
}

// Initialize service worker
const swCore = new ServiceWorkerCore();

// Usage in main thread
const swManager = new ServiceWorkerManager();

// Register service worker
swManager.register('/sw.js').then(() => {
    console.log('Service Worker registered successfully');
}).catch(error => {
    console.error('Service Worker registration failed:', error);
});

// Listen for updates
document.addEventListener('swUpdate', (event) => {
    const shouldUpdate = confirm('New version available. Update now?');
    if (shouldUpdate) {
        swManager.skipWaiting();
    }
});
```

### 🎯 Intersection Observer

> **Interview Key Point:** Intersection Observer provides an efficient way to observe changes in the intersection of elements with a root element or viewport. It's essential for lazy loading, infinite scroll, and performance optimization.

#### **Intersection Observer Implementation**

```javascript
class IntersectionObserverManager {
    constructor() {
        this.observers = new Map();
        this.isSupported = 'IntersectionObserver' in window;
    }
    
    checkSupport() {
        if (!this.isSupported) {
            throw new Error('IntersectionObserver is not supported');
        }
    }
    
    // Create and configure observer
    createObserver(name, callback, options = {}) {
        this.checkSupport();
        
        const defaultOptions = {
            root: null, // viewport
            rootMargin: '0px',
            threshold: 0.1
        };
        
        const finalOptions = { ...defaultOptions, ...options };
        
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                callback(entry, observer);
            });
        }, finalOptions);
        
        this.observers.set(name, {
            observer,
            elements: new Set(),
            options: finalOptions
        });
        
        return observer;
    }
    
    // Observe element
    observe(observerName, element, data = {}) {
        const observerConfig = this.observers.get(observerName);
        if (!observerConfig) {
            throw new Error(`Observer ${observerName} not found`);
        }
        
        // Store additional data with element
        element._observerData = data;
        
        observerConfig.observer.observe(element);
        observerConfig.elements.add(element);
    }
    
    // Unobserve element
    unobserve(observerName, element) {
        const observerConfig = this.observers.get(observerName);
        if (observerConfig) {
            observerConfig.observer.unobserve(element);
            observerConfig.elements.delete(element);
            delete element._observerData;
        }
    }
    
    // Disconnect observer
    disconnect(observerName) {
        const observerConfig = this.observers.get(observerName);
        if (observerConfig) {
            observerConfig.observer.disconnect();
            observerConfig.elements.clear();
            this.observers.delete(observerName);
        }
    }
    
    // Get observer statistics
    getStats(observerName) {
        const observerConfig = this.observers.get(observerName);
        if (observerConfig) {
            return {
                name: observerName,
                elementCount: observerConfig.elements.size,
                options: observerConfig.options
            };
        }
        return null;
    }
}

// Lazy Loading Implementation
class LazyLoader {
    constructor() {
        this.observerManager = new IntersectionObserverManager();
        this.loadedImages = new Set();
        this.setupImageObserver();
        this.setupContentObserver();
    }
    
    setupImageObserver() {
        this.observerManager.createObserver('images', (entry) => {
            if (entry.isIntersecting) {
                this.loadImage(entry.target);
            }
        }, {
            rootMargin: '50px 0px', // Load 50px before entering viewport
            threshold: 0.01
        });
    }
    
    setupContentObserver() {
        this.observerManager.createObserver('content', (entry) => {
            if (entry.isIntersecting) {
                this.loadContent(entry.target);
            }
        }, {
            rootMargin: '100px 0px',
            threshold: 0.1
        });
    }
    
    // Load image lazily
    loadImage(img) {
        if (this.loadedImages.has(img)) return;
        
        const src = img.dataset.src;
        const srcset = img.dataset.srcset;
        
        if (src || srcset) {
            // Create new image to preload
            const imageLoader = new Image();
            
            imageLoader.onload = () => {
                // Update img element
                if (src) img.src = src;
                if (srcset) img.srcset = srcset;
                
                img.classList.add('loaded');
                img.classList.remove('loading');
                
                this.loadedImages.add(img);
                this.observerManager.unobserve('images', img);
                
                // Dispatch loaded event
                img.dispatchEvent(new CustomEvent('lazyLoaded', {
                    detail: { src, srcset }
                }));
            };
            
            imageLoader.onerror = () => {
                img.classList.add('error');
                img.classList.remove('loading');
                this.observerManager.unobserve('images', img);
            };
            
            // Start loading
            img.classList.add('loading');
            if (src) imageLoader.src = src;
        }
    }
    
    // Load content lazily
    async loadContent(element) {
        const url = element.dataset.src;
        const template = element.dataset.template;
        
        if (url) {
            try {
                element.classList.add('loading');
                
                const response = await fetch(url);
                const content = await response.text();
                
                if (template) {
                    // Use template engine or simple replacement
                    element.innerHTML = this.processTemplate(content, template);
                } else {
                    element.innerHTML = content;
                }
                
                element.classList.remove('loading');
                element.classList.add('loaded');
                
                this.observerManager.unobserve('content', element);
                
                // Dispatch event
                element.dispatchEvent(new CustomEvent('contentLoaded', {
                    detail: { url, content }
                }));
                
            } catch (error) {
                element.classList.remove('loading');
                element.classList.add('error');
                element.innerHTML = '<p>Failed to load content</p>';
                console.error('Content loading failed:', error);
            }
        }
    }
    
    processTemplate(content, template) {
        // Simple template processing
        return content;
    }
    
    // Register images for lazy loading
    registerImages(selector = 'img[data-src]') {
        const images = document.querySelectorAll(selector);
        images.forEach(img => {
            this.observerManager.observe('images', img);
        });
        return images.length;
    }
    
    // Register content for lazy loading
    registerContent(selector = '[data-src]:not(img)') {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            this.observerManager.observe('content', element);
        });
        return elements.length;
    }
}

// Infinite Scroll Implementation
class InfiniteScroll {
    constructor(options = {}) {
        this.observerManager = new IntersectionObserverManager();
        this.container = options.container || document.body;
        this.loadMore = options.loadMore || (() => {});
        this.threshold = options.threshold || 0.1;
        this.rootMargin = options.rootMargin || '100px';
        this.isLoading = false;
        this.hasMore = true;
        
        this.setupSentinel();
    }
    
    setupSentinel() {
        // Create sentinel element
        this.sentinel = document.createElement('div');
        this.sentinel.className = 'infinite-scroll-sentinel';
        this.sentinel.style.cssText = `
            height: 1px;
            visibility: hidden;
            pointer-events: none;
        `;
        
        // Create observer
        this.observerManager.createObserver('infinite', (entry) => {
            if (entry.isIntersecting && !this.isLoading && this.hasMore) {
                this.handleIntersection();
            }
        }, {
            rootMargin: this.rootMargin,
            threshold: this.threshold
        });
        
        // Add sentinel to container
        this.container.appendChild(this.sentinel);
        this.observerManager.observe('infinite', this.sentinel);
    }
    
    async handleIntersection() {
        this.isLoading = true;
        
        try {
            const result = await this.loadMore();
            
            if (result === false || result?.hasMore === false) {
                this.hasMore = false;
                this.destroy();
            }
            
            // Dispatch event
            document.dispatchEvent(new CustomEvent('infiniteScrollLoad', {
                detail: { result, hasMore: this.hasMore }
            }));
            
        } catch (error) {
            console.error('Infinite scroll load failed:', error);
            
            // Retry after delay
            setTimeout(() => {
                this.isLoading = false;
            }, 2000);
        } finally {
            if (this.hasMore) {
                this.isLoading = false;
            }
        }
    }
    
    // Reset infinite scroll
    reset() {
        this.isLoading = false;
        this.hasMore = true;
        
        if (!this.container.contains(this.sentinel)) {
            this.container.appendChild(this.sentinel);
            this.observerManager.observe('infinite', this.sentinel);
        }
    }
    
    // Destroy infinite scroll
    destroy() {
        this.observerManager.disconnect('infinite');
        if (this.sentinel.parentNode) {
            this.sentinel.parentNode.removeChild(this.sentinel);
        }
    }
}

// Visibility Tracking
class VisibilityTracker {
    constructor() {
        this.observerManager = new IntersectionObserverManager();
        this.visibleElements = new Map();
        this.setupVisibilityObserver();
    }
    
    setupVisibilityObserver() {
        this.observerManager.createObserver('visibility', (entry) => {
            const element = entry.target;
            const data = element._observerData || {};
            
            if (entry.isIntersecting) {
                this.handleElementVisible(element, entry, data);
            } else {
                this.handleElementHidden(element, entry, data);
            }
        }, {
            threshold: [0, 0.25, 0.5, 0.75, 1.0], // Multiple thresholds
            rootMargin: '0px'
        });
    }
    
    handleElementVisible(element, entry, data) {
        const visibilityData = {
            element,
            visibleSince: Date.now(),
            maxVisibility: entry.intersectionRatio,
            ...data
        };
        
        this.visibleElements.set(element, visibilityData);
        
        // Track analytics
        if (data.trackAnalytics) {
            this.trackVisibility(element, 'visible', entry.intersectionRatio);
        }
        
        // Dispatch event
        element.dispatchEvent(new CustomEvent('elementVisible', {
            detail: { entry, data }
        }));
    }
    
    handleElementHidden(element, entry, data) {
        const visibilityData = this.visibleElements.get(element);
        
        if (visibilityData) {
            const duration = Date.now() - visibilityData.visibleSince;
            
            // Track analytics
            if (data.trackAnalytics) {
                this.trackVisibility(element, 'hidden', {
                    duration,
                    maxVisibility: visibilityData.maxVisibility
                });
            }
            
            this.visibleElements.delete(element);
            
            // Dispatch event
            element.dispatchEvent(new CustomEvent('elementHidden', {
                detail: { entry, data, duration }
            }));
        }
    }
    
    trackVisibility(element, action, data) {
        // Send to analytics service
        console.log('Analytics:', {
            element: element.tagName,
            id: element.id,
            className: element.className,
            action,
            data
        });
    }
    
    // Track specific elements
    track(selector, options = {}) {
        const elements = document.querySelectorAll(selector);
        elements.forEach(element => {
            this.observerManager.observe('visibility', element, options);
        });
        return elements.length;
    }
    
    // Get currently visible elements
    getVisibleElements() {
        return Array.from(this.visibleElements.keys());
    }
    
    // Stop tracking element
    stopTracking(element) {
        this.observerManager.unobserve('visibility', element);
        this.visibleElements.delete(element);
    }
}

// Usage Examples
const lazyLoader = new LazyLoader();
const infiniteScroll = new InfiniteScroll({
    loadMore: async () => {
        const response = await fetch('/api/posts?page=' + currentPage++);
        const posts = await response.json();
        appendPosts(posts);
        return posts.length > 0;
    }
});

const visibilityTracker = new VisibilityTracker();

// Initialize lazy loading
lazyLoader.registerImages();
lazyLoader.registerContent();

// Track specific elements for analytics
visibilityTracker.track('.product-card', { trackAnalytics: true });
visibilityTracker.track('.advertisement', { trackAnalytics: true });
```

---

## 5. Security

> **Interview Explanation:** Web security is crucial for protecting users and applications from various attacks. Understanding common vulnerabilities and their prevention mechanisms is essential for any web developer.

### 🎯 Cross-Origin Resource Sharing (CORS)

> **Interview Key Point:** CORS is a mechanism that allows servers to specify which origins can access their resources. It's a relaxation of the same-origin policy that enables controlled cross-origin requests.

#### **Understanding CORS**

```javascript
// Client-side CORS handling
class CORSAwareClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }
    
    // Make CORS request with proper error handling
    async makeRequest(endpoint, options = {}) {
        const url = this.baseURL + endpoint;
        
        try {
            const response = await fetch(url, {
                method: options.method || 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                },
                credentials: options.includeCredentials ? 'include' : 'same-origin',
                mode: 'cors', // Explicitly set CORS mode
                ...options
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            return response;
        } catch (error) {
            if (error.name === 'TypeError' && error.message.includes('CORS')) {
                throw new Error('CORS error: The server does not allow cross-origin requests from this domain');
            }
            throw error;
        }
    }
    
    // Handle preflight requests
    async makeComplexRequest(endpoint, data, customHeaders = {}) {
        // This will trigger a preflight request due to custom headers
        return this.makeRequest(endpoint, {
            method: 'POST',
            headers: {
                'X-Custom-Header': 'value',
                'Authorization': 'Bearer token',
                ...customHeaders
            },
            body: JSON.stringify(data)
        });
    }
    
    // Check CORS support
    async checkCORSSupport(endpoint) {
        try {
            const response = await fetch(this.baseURL + endpoint, {
                method: 'HEAD',
                mode: 'cors'
            });
            return {
                supported: true,
                allowedMethods: response.headers.get('Access-Control-Allow-Methods'),
                allowedHeaders: response.headers.get('Access-Control-Allow-Headers'),
                maxAge: response.headers.get('Access-Control-Max-Age')
            };
        } catch (error) {
            return {
                supported: false,
                error: error.message
            };
        }
    }
}

// Server-side CORS configuration (Express.js example)
function setupCORS(app) {
    // Basic CORS middleware
    app.use((req, res, next) => {
        const origin = req.headers.origin;
        const allowedOrigins = [
            'https://myapp.com',
            'https://www.myapp.com',
            'http://localhost:3000',
            'http://localhost:8080'
        ];
        
        // Check if origin is allowed
        if (allowedOrigins.includes(origin)) {
            res.setHeader('Access-Control-Allow-Origin', origin);
        }
        
        // Set other CORS headers
        res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
        res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With');
        res.setHeader('Access-Control-Allow-Credentials', 'true');
        res.setHeader('Access-Control-Max-Age', '86400'); // 24 hours
        
        // Handle preflight requests
        if (req.method === 'OPTIONS') {
            res.status(200).end();
            return;
        }
        
        next();
    });
    
    // Advanced CORS configuration
    const corsConfig = {
        origin: (origin, callback) => {
            // Allow requests with no origin (mobile apps, etc.)
            if (!origin) return callback(null, true);
            
            const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(',') || [];
            
            if (allowedOrigins.includes(origin)) {
                callback(null, true);
            } else {
                callback(new Error('Not allowed by CORS'));
            }
        },
        credentials: true,
        optionsSuccessStatus: 200,
        methods: ['GET', 'POST', 'PUT', 'DELETE'],
        allowedHeaders: ['Content-Type', 'Authorization'],
        exposedHeaders: ['X-Total-Count', 'X-Page-Count']
    };
    
    return corsConfig;
}
```

### 🎯 Same-Origin Policy

> **Interview Key Point:** The same-origin policy is a critical security concept that restricts how documents or scripts from one origin can interact with resources from another origin.

#### **Same-Origin Policy Implementation**

```javascript
// URL origin comparison utility
class OriginValidator {
    constructor() {
        this.currentOrigin = window.location.origin;
    }
    
    // Check if two URLs have the same origin
    isSameOrigin(url1, url2) {
        const origin1 = this.getOrigin(url1);
        const origin2 = this.getOrigin(url2);
        return origin1 === origin2;
    }
    
    // Extract origin from URL
    getOrigin(url) {
        try {
            const urlObj = new URL(url, window.location.href);
            return urlObj.origin;
        } catch (error) {
            return null;
        }
    }
    
    // Check if URL is same origin as current page
    isCurrentOrigin(url) {
        return this.isSameOrigin(url, this.currentOrigin);
    }
    
    // Validate external links
    validateExternalLink(url) {
        if (!this.isCurrentOrigin(url)) {
            return {
                isExternal: true,
                origin: this.getOrigin(url),
                requiresNewTab: true,
                securityRisk: this.assessSecurityRisk(url)
            };
        }
        
        return {
            isExternal: false,
            origin: this.currentOrigin,
            requiresNewTab: false,
            securityRisk: 'none'
        };
    }
    
    assessSecurityRisk(url) {
        const origin = this.getOrigin(url);
        
        // Check against known malicious patterns
        const suspiciousPatterns = [
            /bit\.ly/,
            /tinyurl/,
            /t\.co/,
            /suspicious-domain/
        ];
        
        if (suspiciousPatterns.some(pattern => pattern.test(origin))) {
            return 'high';
        }
        
        // Check protocol
        if (origin?.startsWith('http:') && window.location.protocol === 'https:') {
            return 'medium';
        }
        
        return 'low';
    }
}

// Secure external link handler
class SecureLinkHandler {
    constructor() {
        this.originValidator = new OriginValidator();
        this.setupLinkHandlers();
    }
    
    setupLinkHandlers() {
        // Handle all link clicks
        document.addEventListener('click', (e) => {
            if (e.target.tagName === 'A' || e.target.closest('a')) {
                const link = e.target.tagName === 'A' ? e.target : e.target.closest('a');
                this.handleLinkClick(e, link);
            }
        });
    }
    
    handleLinkClick(event, link) {
        const href = link.href;
        if (!href) return;
        
        const validation = this.originValidator.validateExternalLink(href);
        
        if (validation.isExternal) {
            event.preventDefault();
            this.handleExternalLink(link, validation);
        }
    }
    
    handleExternalLink(link, validation) {
        // Add security attributes
        if (validation.requiresNewTab) {
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
        }
        
        // Show warning for high-risk links
        if (validation.securityRisk === 'high') {
            const proceed = confirm(
                `This link leads to an external site (${validation.origin}). ` +
                'This may be a security risk. Do you want to continue?'
            );
            
            if (!proceed) return;
        }
        
        // Log external link access
        this.logExternalAccess(link.href, validation);
        
        // Open link safely
        const newWindow = window.open(link.href, '_blank', 'noopener,noreferrer');
        
        // Additional security: clear the opener reference
        if (newWindow) {
            newWindow.opener = null;
        }
    }
    
    logExternalAccess(url, validation) {
        // Log for security monitoring
        console.log('External link accessed:', {
            url,
            origin: validation.origin,
            risk: validation.securityRisk,
            timestamp: new Date().toISOString()
        });
        
        // Send to analytics/security service
        if (typeof gtag !== 'undefined') {
            gtag('event', 'external_link_click', {
                url: url,
                risk_level: validation.securityRisk
            });
        }
    }
}

// PostMessage security
class SecurePostMessage {
    constructor(allowedOrigins = []) {
        this.allowedOrigins = new Set(allowedOrigins);
        this.setupMessageHandler();
    }
    
    setupMessageHandler() {
        window.addEventListener('message', (event) => {
            this.handleMessage(event);
        });
    }
    
    handleMessage(event) {
        // Validate origin
        if (!this.isOriginAllowed(event.origin)) {
            console.warn('Rejected message from unauthorized origin:', event.origin);
            return;
        }
        
        // Validate message structure
        if (!this.isValidMessage(event.data)) {
            console.warn('Rejected invalid message:', event.data);
            return;
        }
        
        // Process message
        this.processMessage(event.data, event.origin);
    }
    
    isOriginAllowed(origin) {
        return this.allowedOrigins.has(origin) || this.allowedOrigins.has('*');
    }
    
    isValidMessage(data) {
        // Check message structure
        return data && 
               typeof data === 'object' && 
               typeof data.type === 'string' &&
               data.type.length > 0;
    }
    
    processMessage(data, origin) {
        switch (data.type) {
            case 'AUTH_RESPONSE':
                this.handleAuthResponse(data.payload, origin);
                break;
            case 'RESIZE_REQUEST':
                this.handleResizeRequest(data.payload, origin);
                break;
            default:
                console.log('Unknown message type:', data.type);
        }
    }
    
    // Send secure message
    sendMessage(targetWindow, message, targetOrigin) {
        if (!this.isOriginAllowed(targetOrigin)) {
            throw new Error(`Origin ${targetOrigin} not allowed`);
        }
        
        const secureMessage = {
            ...message,
            timestamp: Date.now(),
            source: window.location.origin
        };
        
        targetWindow.postMessage(secureMessage, targetOrigin);
    }
    
    addAllowedOrigin(origin) {
        this.allowedOrigins.add(origin);
    }
    
    removeAllowedOrigin(origin) {
        this.allowedOrigins.delete(origin);
    }
}
```

### 🎯 Cross-Site Scripting (XSS) Prevention

> **Interview Key Point:** XSS attacks occur when malicious scripts are injected into web applications. Understanding different types of XSS and prevention techniques is crucial for web security.

#### **XSS Prevention Implementation**

```javascript
// Content sanitization utility
class ContentSanitizer {
    constructor() {
        // HTML entities for escaping
        this.htmlEntities = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#x27;',
            '/': '&#x2F;'
        };
        
        // Allowed HTML tags for rich content
        this.allowedTags = new Set([
            'p', 'br', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
            'ul', 'ol', 'li', 'blockquote', 'a'
        ]);
        
        // Allowed attributes
        this.allowedAttributes = {
            'a': ['href', 'title'],
            '*': ['class', 'id'] // Global attributes
        };
        
        // Dangerous protocols
        this.dangerousProtocols = /^(javascript|data|vbscript):/i;
    }
    
    // Escape HTML entities
    escapeHtml(str) {
        if (typeof str !== 'string') return str;
        
        return str.replace(/[&<>"'\/]/g, (char) => {
            return this.htmlEntities[char];
        });
    }
    
    // Unescape HTML entities
    unescapeHtml(str) {
        if (typeof str !== 'string') return str;
        
        const entityMap = Object.fromEntries(
            Object.entries(this.htmlEntities).map(([key, value]) => [value, key])
        );
        
        return str.replace(/&(amp|lt|gt|quot|#x27|#x2F);/g, (entity) => {
            return entityMap[entity] || entity;
        });
    }
    
    // Sanitize user input for display
    sanitizeText(input) {
        if (typeof input !== 'string') return '';
        
        return this.escapeHtml(input.trim());
    }
    
    // Sanitize HTML content
    sanitizeHtml(html) {
        if (typeof html !== 'string') return '';
        
        // Create a temporary DOM element
        const temp = document.createElement('div');
        temp.innerHTML = html;
        
        return this.sanitizeElement(temp).innerHTML;
    }
    
    // Recursively sanitize DOM elements
    sanitizeElement(element) {
        const clone = element.cloneNode(false);
        
        // Check if tag is allowed
        if (!this.allowedTags.has(element.tagName.toLowerCase())) {
            // Replace with safe span or remove
            const replacement = document.createElement('span');
            replacement.textContent = element.textContent;
            return replacement;
        }
        
        // Sanitize attributes
        this.sanitizeAttributes(element, clone);
        
        // Recursively sanitize children
        for (const child of element.childNodes) {
            if (child.nodeType === Node.TEXT_NODE) {
                clone.appendChild(document.createTextNode(child.textContent));
            } else if (child.nodeType === Node.ELEMENT_NODE) {
                const sanitizedChild = this.sanitizeElement(child);
                if (sanitizedChild) {
                    clone.appendChild(sanitizedChild);
                }
            }
        }
        
        return clone;
    }
    
    // Sanitize element attributes
    sanitizeAttributes(source, target) {
        const tagName = source.tagName.toLowerCase();
        const allowedForTag = this.allowedAttributes[tagName] || [];
        const globalAllowed = this.allowedAttributes['*'] || [];
        const allowed = [...allowedForTag, ...globalAllowed];
        
        for (const attr of source.attributes) {
            if (allowed.includes(attr.name)) {
                let value = attr.value;
                
                // Special handling for href attributes
                if (attr.name === 'href') {
                    value = this.sanitizeUrl(value);
                }
                
                // Special handling for style attributes
                if (attr.name === 'style') {
                    value = this.sanitizeStyle(value);
                }
                
                if (value !== null) {
                    target.setAttribute(attr.name, value);
                }
            }
        }
    }
    
    // Sanitize URLs
    sanitizeUrl(url) {
        if (!url) return null;
        
        // Remove dangerous protocols
        if (this.dangerousProtocols.test(url)) {
            return null;
        }
        
        // Allow relative URLs and safe protocols
        const safeProtocols = /^(https?|mailto|tel|ftp):/i;
        if (url.includes(':') && !safeProtocols.test(url)) {
            return null;
        }
        
        return url;
    }
    
    // Sanitize CSS styles
    sanitizeStyle(style) {
        if (!style) return null;
        
        // Remove dangerous CSS properties and values
        const dangerous = /(expression|javascript|import|@import)/i;
        if (dangerous.test(style)) {
            return null;
        }
        
        return style;
    }
    
    // Validate and sanitize JSON data
    sanitizeJson(jsonString) {
        try {
            const parsed = JSON.parse(jsonString);
            return this.sanitizeObject(parsed);
        } catch (error) {
            throw new Error('Invalid JSON input');
        }
    }
    
    // Recursively sanitize object properties
    sanitizeObject(obj) {
        if (typeof obj === 'string') {
            return this.sanitizeText(obj);
        } else if (Array.isArray(obj)) {
            return obj.map(item => this.sanitizeObject(item));
        } else if (obj && typeof obj === 'object') {
            const sanitized = {};
            for (const [key, value] of Object.entries(obj)) {
                const sanitizedKey = this.sanitizeText(key);
                sanitized[sanitizedKey] = this.sanitizeObject(value);
            }
            return sanitized;
        }
        
        return obj;
    }
}

// Content Security Policy (CSP) helper
class CSPHelper {
    constructor() {
        this.violations = [];
        this.setupViolationReporting();
    }
    
    setupViolationReporting() {
        // Listen for CSP violations
        document.addEventListener('securitypolicyviolation', (e) => {
            this.handleViolation(e);
        });
    }
    
    handleViolation(event) {
        const violation = {
            blockedURI: event.blockedURI,
            documentURI: event.documentURI,
            originalPolicy: event.originalPolicy,
            referrer: event.referrer,
            violatedDirective: event.violatedDirective,
            effectiveDirective: event.effectiveDirective,
            statusCode: event.statusCode,
            lineNumber: event.lineNumber,
            columnNumber: event.columnNumber,
            sourceFile: event.sourceFile,
            timestamp: new Date().toISOString()
        };
        
        this.violations.push(violation);
        console.warn('CSP Violation:', violation);
        
        // Report to security service
        this.reportViolation(violation);
    }
    
    reportViolation(violation) {
        // Send violation report to server
        fetch('/api/csp-violations', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(violation)
        }).catch(error => {
            console.error('Failed to report CSP violation:', error);
        });
    }
    
    // Generate CSP header
    generateCSP(config = {}) {
        const defaults = {
            'default-src': ["'self'"],
            'script-src': ["'self'", "'unsafe-inline'"],
            'style-src': ["'self'", "'unsafe-inline'"],
            'img-src': ["'self'", 'data:', 'https:'],
            'font-src': ["'self'"],
            'connect-src': ["'self'"],
            'frame-src': ["'none'"],
            'object-src': ["'none'"],
            'base-uri': ["'self'"],
            'form-action': ["'self'"]
        };
        
        const policy = { ...defaults, ...config };
        
        return Object.entries(policy)
            .map(([directive, sources]) => `${directive} ${sources.join(' ')}`)
            .join('; ');
    }
    
    // Validate nonce
    validateNonce(nonce, element) {
        const csp = document.querySelector('meta[http-equiv="Content-Security-Policy"]');
        if (!csp) return false;
        
        const content = csp.getAttribute('content');
        return content.includes(`'nonce-${nonce}'`);
    }
    
    getViolations() {
        return [...this.violations];
    }
    
    clearViolations() {
        this.violations = [];
    }
}

// XSS Detection and Prevention
class XSSProtection {
    constructor() {
        this.sanitizer = new ContentSanitizer();
        this.csp = new CSPHelper();
        this.suspiciousPatterns = [
            /<script[^>]*>.*?<\/script>/gi,
            /javascript:/gi,
            /on\w+\s*=/gi,
            /<iframe[^>]*>/gi,
            /<object[^>]*>/gi,
            /<embed[^>]*>/gi,
            /<link[^>]*>/gi,
            /<meta[^>]*>/gi
        ];
    }
    
    // Detect potential XSS in input
    detectXSS(input) {
        if (typeof input !== 'string') return false;
        
        return this.suspiciousPatterns.some(pattern => pattern.test(input));
    }
    
    // Safe innerHTML replacement
    safeInnerHTML(element, content) {
        if (this.detectXSS(content)) {
            console.warn('Potential XSS detected, sanitizing content');
            content = this.sanitizer.sanitizeHtml(content);
        }
        
        element.innerHTML = content;
    }
    
    // Safe text content setting
    safeTextContent(element, content) {
        element.textContent = this.sanitizer.sanitizeText(content);
    }
    
    // Safe attribute setting
    safeSetAttribute(element, name, value) {
        // Validate attribute name
        if (!/^[a-zA-Z-]+$/.test(name)) {
            throw new Error('Invalid attribute name');
        }
        
        // Sanitize value based on attribute type
        let sanitizedValue = value;
        
        if (name === 'href' || name === 'src') {
            sanitizedValue = this.sanitizer.sanitizeUrl(value);
        } else if (name === 'style') {
            sanitizedValue = this.sanitizer.sanitizeStyle(value);
        } else {
            sanitizedValue = this.sanitizer.sanitizeText(value);
        }
        
        if (sanitizedValue !== null) {
            element.setAttribute(name, sanitizedValue);
        }
    }
    
    // Create safe DOM element
    createSafeElement(tagName, attributes = {}, textContent = '') {
        // Validate tag name
        if (!/^[a-zA-Z][a-zA-Z0-9]*$/.test(tagName)) {
            throw new Error('Invalid tag name');
        }
        
        const element = document.createElement(tagName);
        
        // Set attributes safely
        for (const [name, value] of Object.entries(attributes)) {
            this.safeSetAttribute(element, name, value);
        }
        
        // Set text content safely
        if (textContent) {
            this.safeTextContent(element, textContent);
        }
        
        return element;
    }
}
```

### 🎯 Cross-Site Request Forgery (CSRF) Protection

> **Interview Key Point:** CSRF attacks trick users into performing unwanted actions on applications where they're authenticated. Understanding token-based protection is essential.

#### **CSRF Protection Implementation**

```javascript
// CSRF Token Manager
class CSRFProtection {
    constructor() {
        this.token = null;
        this.tokenExpiry = null;
        this.refreshThreshold = 5 * 60 * 1000; // 5 minutes
        this.setupCSRFProtection();
    }
    
    async setupCSRFProtection() {
        await this.refreshToken();
        this.setupFormProtection();
        this.setupAjaxProtection();
        this.setupTokenRefresh();
    }
    
    // Get CSRF token from server
    async refreshToken() {
        try {
            const response = await fetch('/api/csrf-token', {
                method: 'GET',
                credentials: 'same-origin'
            });
            
            if (!response.ok) {
                throw new Error('Failed to get CSRF token');
            }
            
            const data = await response.json();
            this.token = data.token;
            this.tokenExpiry = Date.now() + (data.expiresIn * 1000);
            
            // Update meta tag
            this.updateMetaTag();
            
            console.log('CSRF token refreshed');
        } catch (error) {
            console.error('CSRF token refresh failed:', error);
        }
    }
    
    // Update CSRF token in meta tag
    updateMetaTag() {
        let metaTag = document.querySelector('meta[name="csrf-token"]');
        if (!metaTag) {
            metaTag = document.createElement('meta');
            metaTag.name = 'csrf-token';
            document.head.appendChild(metaTag);
        }
        metaTag.content = this.token;
    }
    
    // Get current valid token
    async getToken() {
        if (!this.token || this.isTokenExpiringSoon()) {
            await this.refreshToken();
        }
        return this.token;
    }
    
    isTokenExpiringSoon() {
        return Date.now() + this.refreshThreshold > this.tokenExpiry;
    }
    
    // Setup automatic form protection
    setupFormProtection() {
        // Add CSRF token to all forms
        document.addEventListener('submit', async (e) => {
            const form = e.target;
            if (form.tagName === 'FORM' && this.shouldProtectForm(form)) {
                e.preventDefault();
                await this.protectForm(form);
                form.submit();
            }
        });
        
        // Protect existing forms
        this.protectAllForms();
    }
    
    shouldProtectForm(form) {
        // Only protect forms that modify data
        const method = form.method.toLowerCase();
        return ['post', 'put', 'patch', 'delete'].includes(method);
    }
    
    async protectForm(form) {
        // Remove existing CSRF token
        const existing = form.querySelector('input[name="csrf_token"]');
        if (existing) {
            existing.remove();
        }
        
        // Add new CSRF token
        const token = await this.getToken();
        const tokenInput = document.createElement('input');
        tokenInput.type = 'hidden';
        tokenInput.name = 'csrf_token';
        tokenInput.value = token;
        form.appendChild(tokenInput);
    }
    
    async protectAllForms() {
        const forms = document.querySelectorAll('form');
        for (const form of forms) {
            if (this.shouldProtectForm(form)) {
                await this.protectForm(form);
            }
        }
    }
    
    // Setup AJAX request protection
    setupAjaxProtection() {
        // Intercept fetch requests
        const originalFetch = window.fetch;
        window.fetch = async (url, options = {}) => {
            if (this.shouldProtectRequest(options)) {
                options = await this.protectRequest(options);
            }
            return originalFetch(url, options);
        };
        
        // Intercept XMLHttpRequest
        const originalOpen = XMLHttpRequest.prototype.open;
        const originalSend = XMLHttpRequest.prototype.send;
        
        XMLHttpRequest.prototype.open = function(method, url, async, user, password) {
            this._method = method;
            this._url = url;
            return originalOpen.call(this, method, url, async, user, password);
        };
        
        XMLHttpRequest.prototype.send = async function(data) {
            if (this._method && ['POST', 'PUT', 'PATCH', 'DELETE'].includes(this._method.toUpperCase())) {
                const token = await this.getToken();
                this.setRequestHeader('X-CSRF-Token', token);
            }
            return originalSend.call(this, data);
        }.bind(this);
    }
    
    shouldProtectRequest(options) {
        const method = options.method?.toUpperCase() || 'GET';
        return ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method);
    }
    
    async protectRequest(options) {
        const token = await this.getToken();
        
        return {
            ...options,
            headers: {
                ...options.headers,
                'X-CSRF-Token': token
            }
        };
    }
    
    // Setup automatic token refresh
    setupTokenRefresh() {
        setInterval(async () => {
            if (this.isTokenExpiringSoon()) {
                await this.refreshToken();
                await this.protectAllForms();
            }
        }, 60000); // Check every minute
    }
    
    // Validate token on client side (additional check)
    validateToken(token) {
        // Basic validation - server should do the real validation
        return token && 
               typeof token === 'string' && 
               token.length > 20 && 
               /^[a-zA-Z0-9+/=]+$/.test(token);
    }
    
    // Double submit cookie pattern
    setupDoubleSubmitCookie() {
        const cookieName = 'csrf_token_cookie';
        
        // Set CSRF token in cookie
        document.cookie = `${cookieName}=${this.token}; SameSite=Strict; Secure; Path=/`;
        
        // Verify token matches cookie on requests
        return {
            validateDoubleSubmit: (headerToken) => {
                const cookies = document.cookie.split(';').reduce((acc, cookie) => {
                    const [name, value] = cookie.trim().split('=');
                    acc[name] = value;
                    return acc;
                }, {});
                
                return cookies[cookieName] === headerToken;
            }
        };
    }
}

// Usage example
const csrfProtection = new CSRFProtection();

// Manual token usage
async function makeSecureRequest(url, data) {
    const token = await csrfProtection.getToken();
    
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRF-Token': token
        },
        body: JSON.stringify(data),
        credentials: 'same-origin'
    });
}
```

---

## 6. Performance Optimization

> **Interview Explanation:** Performance optimization is crucial for user experience and SEO. Understanding debouncing, throttling, lazy loading, and memory management helps create efficient web applications.

### 🎯 Debouncing vs Throttling

> **Interview Key Point:** Debouncing delays execution until after events stop firing, while throttling limits execution to once per interval. Both prevent excessive function calls but serve different use cases.

#### **Debouncing and Throttling Implementation**

```javascript
// Advanced Debouncing
class Debouncer {
    constructor() {
        this.timers = new Map();
    }
    
    // Basic debounce
    debounce(func, delay, key = 'default') {
        return (...args) => {
            // Clear existing timer
            if (this.timers.has(key)) {
                clearTimeout(this.timers.get(key));
            }
            
            // Set new timer
            const timer = setTimeout(() => {
                func.apply(this, args);
                this.timers.delete(key);
            }, delay);
            
            this.timers.set(key, timer);
        };
    }
    
    // Debounce with immediate execution option
    debounceImmediate(func, delay, immediate = false, key = 'default') {
        return (...args) => {
            const callNow = immediate && !this.timers.has(key);
            
            if (this.timers.has(key)) {
                clearTimeout(this.timers.get(key));
            }
            
            const timer = setTimeout(() => {
                this.timers.delete(key);
                if (!immediate) func.apply(this, args);
            }, delay);
            
            this.timers.set(key, timer);
            
            if (callNow) func.apply(this, args);
        };
    }
    
    // Debounce with promise support
    debouncePromise(func, delay, key = 'default') {
        let resolvePromise;
        let rejectPromise;
        
        return (...args) => {
            return new Promise((resolve, reject) => {
                // Reject previous promise if it exists
                if (rejectPromise) {
                    rejectPromise(new Error('Debounced'));
                }
                
                resolvePromise = resolve;
                rejectPromise = reject;
                
                if (this.timers.has(key)) {
                    clearTimeout(this.timers.get(key));
                }
                
                const timer = setTimeout(async () => {
                    try {
                        const result = await func.apply(this, args);
                        resolvePromise(result);
                    } catch (error) {
                        rejectPromise(error);
                    } finally {
                        this.timers.delete(key);
                    }
                }, delay);
                
                this.timers.set(key, timer);
            });
        };
    }
    
    // Cancel all debounced functions
    cancelAll() {
        this.timers.forEach(timer => clearTimeout(timer));
        this.timers.clear();
    }
    
    // Cancel specific debounced function
    cancel(key) {
        if (this.timers.has(key)) {
            clearTimeout(this.timers.get(key));
            this.timers.delete(key);
        }
    }
}

// Advanced Throttling
class Throttler {
    constructor() {
        this.lastExecution = new Map();
        this.timers = new Map();
    }
    
    // Basic throttle
    throttle(func, limit, key = 'default') {
        return (...args) => {
            const now = Date.now();
            const lastTime = this.lastExecution.get(key) || 0;
            
            if (now - lastTime >= limit) {
                this.lastExecution.set(key, now);
                return func.apply(this, args);
            }
        };
    }
    
    // Throttle with trailing execution
    throttleWithTrailing(func, limit, key = 'default') {
        return (...args) => {
            const now = Date.now();
            const lastTime = this.lastExecution.get(key) || 0;
            
            if (now - lastTime >= limit) {
                this.lastExecution.set(key, now);
                func.apply(this, args);
            } else {
                // Clear existing trailing timer
                if (this.timers.has(key)) {
                    clearTimeout(this.timers.get(key));
                }
                
                // Set trailing execution
                const timer = setTimeout(() => {
                    this.lastExecution.set(key, Date.now());
                    func.apply(this, args);
                    this.timers.delete(key);
                }, limit - (now - lastTime));
                
                this.timers.set(key, timer);
            }
        };
    }
    
    // Adaptive throttling based on performance
    adaptiveThrottle(func, baseLimit, key = 'default') {
        let currentLimit = baseLimit;
        
        return (...args) => {
            const start = performance.now();
            const now = Date.now();
            const lastTime = this.lastExecution.get(key) || 0;
            
            if (now - lastTime >= currentLimit) {
                this.lastExecution.set(key, now);
                
                const result = func.apply(this, args);
                
                // Adjust limit based on execution time
                const executionTime = performance.now() - start;
                if (executionTime > 16) { // 60fps threshold
                    currentLimit = Math.min(currentLimit * 1.5, baseLimit * 3);
                } else {
                    currentLimit = Math.max(currentLimit * 0.9, baseLimit);
                }
                
                return result;
            }
        };
    }
    
    // Reset throttle state
    reset(key = null) {
        if (key) {
            this.lastExecution.delete(key);
            if (this.timers.has(key)) {
                clearTimeout(this.timers.get(key));
                this.timers.delete(key);
            }
        } else {
            this.lastExecution.clear();
            this.timers.forEach(timer => clearTimeout(timer));
            this.timers.clear();
        }
    }
}

// Practical usage examples
class PerformanceOptimizer {
    constructor() {
        this.debouncer = new Debouncer();
        this.throttler = new Throttler();
        this.setupOptimizations();
    }
    
    setupOptimizations() {
        // Search input debouncing
        this.setupSearchDebouncing();
        
        // Scroll event throttling
        this.setupScrollThrottling();
        
        // Resize event optimization
        this.setupResizeOptimization();
        
        // Form validation debouncing
        this.setupFormValidation();
    }
    
    setupSearchDebouncing() {
        const searchInput = document.getElementById('search');
        if (!searchInput) return;
        
        const debouncedSearch = this.debouncer.debouncePromise(
            async (query) => {
                if (query.length < 2) return [];
                
                const response = await fetch(`/api/search?q=${encodeURIComponent(query)}`);
                return response.json();
            },
            300,
            'search'
        );
        
        searchInput.addEventListener('input', async (e) => {
            const query = e.target.value;
            
            try {
                const results = await debouncedSearch(query);
                this.displaySearchResults(results);
            } catch (error) {
                if (error.message !== 'Debounced') {
                    console.error('Search failed:', error);
                }
            }
        });
    }
    
    setupScrollThrottling() {
        const throttledScroll = this.throttler.throttleWithTrailing(
            () => {
                this.updateScrollPosition();
                this.handleLazyLoading();
                this.updateProgressBar();
            },
            16, // ~60fps
            'scroll'
        );
        
        window.addEventListener('scroll', throttledScroll, { passive: true });
    }
    
    setupResizeOptimization() {
        const debouncedResize = this.debouncer.debounce(
            () => {
                this.recalculateLayout();
                this.updateResponsiveElements();
            },
            250,
            'resize'
        );
        
        window.addEventListener('resize', debouncedResize);
    }
    
    setupFormValidation() {
        const forms = document.querySelectorAll('form[data-live-validation]');
        
        forms.forEach(form => {
            const inputs = form.querySelectorAll('input, textarea, select');
            
            inputs.forEach(input => {
                const debouncedValidation = this.debouncer.debounce(
                    () => this.validateField(input),
                    500,
                    `validation-${input.name}`
                );
                
                input.addEventListener('input', debouncedValidation);
            });
        });
    }
    
    // Utility methods
    displaySearchResults(results) {
        const container = document.getElementById('search-results');
        if (container) {
            container.innerHTML = results.map(result => 
                `<div class="search-result">${result.title}</div>`
            ).join('');
        }
    }
    
    updateScrollPosition() {
        const scrollPercent = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
        document.documentElement.style.setProperty('--scroll-percent', `${scrollPercent}%`);
    }
    
    handleLazyLoading() {
        // Trigger lazy loading check
        document.dispatchEvent(new CustomEvent('scrollCheck'));
    }
    
    updateProgressBar() {
        const progressBar = document.getElementById('reading-progress');
        if (progressBar) {
            const progress = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
            progressBar.style.width = `${Math.min(progress, 100)}%`;
        }
    }
    
    recalculateLayout() {
        // Recalculate responsive layouts
        document.dispatchEvent(new CustomEvent('layoutRecalculate'));
    }
    
    updateResponsiveElements() {
        // Update elements that depend on viewport size
        const viewportWidth = window.innerWidth;
        document.documentElement.style.setProperty('--viewport-width', `${viewportWidth}px`);
    }
    
    async validateField(input) {
        const value = input.value;
        const validationRules = input.dataset.validation;
        
        if (!validationRules) return;
        
        try {
            const response = await fetch('/api/validate', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    field: input.name,
                    value: value,
                    rules: validationRules
                })
            });
            
            const result = await response.json();
            this.displayValidationResult(input, result);
        } catch (error) {
            console.error('Validation failed:', error);
        }
    }
    
    displayValidationResult(input, result) {
        const feedback = input.parentNode.querySelector('.validation-feedback');
        if (feedback) {
            feedback.textContent = result.message;
            feedback.className = `validation-feedback ${result.valid ? 'valid' : 'invalid'}`;
        }
    }
}

// Initialize performance optimizer
const performanceOptimizer = new PerformanceOptimizer();

// Export for use in other modules
window.PerformanceUtils = {
    debouncer: performanceOptimizer.debouncer,
    throttler: performanceOptimizer.throttler,
    
    // Quick utility functions
    debounce: (func, delay) => performanceOptimizer.debouncer.debounce(func, delay),
    throttle: (func, limit) => performanceOptimizer.throttler.throttle(func, limit)
};
```

### 🎯 Memory Leak Prevention

> **Interview Key Point:** Memory leaks in JavaScript often occur due to unreferenced DOM elements, event listeners, closures, and timers. Understanding how to prevent and detect them is crucial for performance.

#### **Memory Management Implementation**

```javascript
// Memory Leak Detection and Prevention
class MemoryManager {
    constructor() {
        this.observers = new Set();
        this.timers = new Set();
        this.eventListeners = new Map();
        this.watchers = new Set();
        this.isMonitoring = false;
        
        this.setupMemoryMonitoring();
    }
    
    setupMemoryMonitoring() {
        // Monitor memory usage periodically
        this.startMemoryMonitoring();
        
        // Cleanup on page unload
        window.addEventListener('beforeunload', () => {
            this.cleanup();
        });
        
        // Setup performance observer for memory
        if ('PerformanceObserver' in window) {
            this.setupPerformanceObserver();
        }
    }
    
    setupPerformanceObserver() {
        const observer = new PerformanceObserver((list) => {
            for (const entry of list.getEntries()) {
                if (entry.entryType === 'measure' || entry.entryType === 'navigation') {
                    this.logPerformanceMetric(entry);
                }
            }
        });
        
        observer.observe({ entryTypes: ['measure', 'navigation'] });
        this.observers.add(observer);
    }
    
    startMemoryMonitoring() {
        if (this.isMonitoring) return;
        
        this.isMonitoring = true;
        
        const checkMemory = () => {
            if (performance.memory) {
                const memInfo = {
                    used: performance.memory.usedJSHeapSize,
                    total: performance.memory.totalJSHeapSize,
                    limit: performance.memory.jsHeapSizeLimit,
                    timestamp: Date.now()
                };
                
                this.handleMemoryInfo(memInfo);
            }
        };
        
        // Check memory every 30 seconds
        const timerId = setInterval(checkMemory, 30000);
        this.timers.add(timerId);
        
        // Initial check
        checkMemory();
    }
    
    handleMemoryInfo(memInfo) {
        const usagePercent = (memInfo.used / memInfo.limit) * 100;
        
        // Log memory usage
        console.log(`Memory usage: ${(memInfo.used / 1048576).toFixed(2)}MB (${usagePercent.toFixed(2)}%)`);
        
        // Warn if memory usage is high
        if (usagePercent > 80) {
            console.warn('High memory usage detected, consider cleanup');
            this.suggestCleanup();
        }
        
        // Dispatch memory event
        window.dispatchEvent(new CustomEvent('memoryUpdate', {
            detail: memInfo
        }));
    }
    
    suggestCleanup() {
        console.group('Memory Cleanup Suggestions:');
        console.log('- Check for unreferenced DOM elements');
        console.log('- Remove unused event listeners');
        console.log('- Clear unused timers and intervals');
        console.log('- Check for circular references');
        console.log('- Consider using WeakMap/WeakSet for temporary references');
        console.groupEnd();
    }
    
    // Safe event listener management
    addEventListener(element, event, handler, options, key) {
        const listenerKey = key || `${element.tagName}-${event}-${Date.now()}`;
        
        element.addEventListener(event, handler, options);
        
        // Store reference for cleanup
        if (!this.eventListeners.has(element)) {
            this.eventListeners.set(element, new Map());
        }
        
        this.eventListeners.get(element).set(listenerKey, {
            event,
            handler,
            options
        });
        
        return listenerKey;
    }
    
    removeEventListener(element, key) {
        const elementListeners = this.eventListeners.get(element);
        if (elementListeners && elementListeners.has(key)) {
            const { event, handler, options } = elementListeners.get(key);
            element.removeEventListener(event, handler, options);
            elementListeners.delete(key);
            
            if (elementListeners.size === 0) {
                this.eventListeners.delete(element);
            }
        }
    }
    
    // Safe timer management
    setTimeout(callback, delay) {
        const timerId = setTimeout(() => {
            callback();
            this.timers.delete(timerId);
        }, delay);
        
        this.timers.add(timerId);
        return timerId;
    }
    
    setInterval(callback, interval) {
        const timerId = setInterval(callback, interval);
        this.timers.add(timerId);
        return timerId;
    }
    
    clearTimer(timerId) {
        clearTimeout(timerId);
        clearInterval(timerId);
        this.timers.delete(timerId);
    }
    
    // Safe observer management
    addObserver(observer) {
        this.observers.add(observer);
        return observer;
    }
    
    removeObserver(observer) {
        if (observer && typeof observer.disconnect === 'function') {
            observer.disconnect();
        }
        this.observers.delete(observer);
    }
    
    // WeakMap-based cache for temporary data
    createWeakCache() {
        return new WeakMap();
    }
    
    // Detect potential memory leaks
    detectLeaks() {
        const leaks = [];
        
        // Check for detached DOM nodes
        const detachedNodes = this.findDetachedNodes();
        if (detachedNodes.length > 0) {
            leaks.push({
                type: 'detached-nodes',
                count: detachedNodes.length,
                description: 'DOM nodes that are no longer in the document but still referenced'
            });
        }
        
        // Check for excessive event listeners
        let totalListeners = 0;
        this.eventListeners.forEach(listeners => {
            totalListeners += listeners.size;
        });
        
        if (totalListeners > 1000) {
            leaks.push({
                type: 'excessive-listeners',
                count: totalListeners,
                description: 'Large number of event listeners may indicate leaks'
            });
        }
        
        // Check for excessive timers
        if (this.timers.size > 100) {
            leaks.push({
                type: 'excessive-timers',
                count: this.timers.size,
                description: 'Large number of active timers'
            });
        }
        
        return leaks;
    }
    
    findDetachedNodes() {
        // This is a simplified detection - in practice, you'd need more sophisticated tools
        const detached = [];
        
        this.eventListeners.forEach((listeners, element) => {
            if (!document.contains(element)) {
                detached.push(element);
            }
        });
        
        return detached;
    }
    
    // Force garbage collection (only works in dev tools)
    forceGC() {
        if (window.gc) {
            window.gc();
            console.log('Garbage collection forced');
        } else {
            console.warn('Garbage collection not available. Run with --expose-gc flag');
        }
    }
    
    // Complete cleanup
    cleanup() {
        console.log('Performing memory cleanup...');
        
        // Clear all timers
        this.timers.forEach(timerId => {
            clearTimeout(timerId);
            clearInterval(timerId);
        });
        this.timers.clear();
        
        // Remove all event listeners
        this.eventListeners.forEach((listeners, element) => {
            listeners.forEach(({ event, handler, options }) => {
                element.removeEventListener(event, handler, options);
            });
        });
        this.eventListeners.clear();
        
        // Disconnect all observers
        this.observers.forEach(observer => {
            if (observer && typeof observer.disconnect === 'function') {
                observer.disconnect();
            }
        });
        this.observers.clear();
        
        // Clear watchers
        this.watchers.clear();
        
        this.isMonitoring = false;
        
        console.log('Memory cleanup completed');
    }
    
    // Get memory report
    getMemoryReport() {
        const report = {
            timestamp: new Date().toISOString(),
            timers: this.timers.size,
            eventListeners: this.eventListeners.size,
            observers: this.observers.size,
            potentialLeaks: this.detectLeaks()
        };
        
        if (performance.memory) {
            report.memory = {
                used: performance.memory.usedJSHeapSize,
                total: performance.memory.totalJSHeapSize,
                limit: performance.memory.jsHeapSizeLimit
            };
        }
        
        return report;
    }
    
    logPerformanceMetric(entry) {
        console.log(`Performance: ${entry.name} - ${entry.duration.toFixed(2)}ms`);
    }
}

// Global memory manager instance
const memoryManager = new MemoryManager();

// Export utilities
window.MemoryUtils = {
    manager: memoryManager,
    
    // Convenient wrapper functions
    safeSetTimeout: (callback, delay) => memoryManager.setTimeout(callback, delay),
    safeSetInterval: (callback, interval) => memoryManager.setInterval(callback, interval),
    clearTimer: (timerId) => memoryManager.clearTimer(timerId),
    
    addEventListener: (element, event, handler, options, key) => 
        memoryManager.addEventListener(element, event, handler, options, key),
    removeEventListener: (element, key) => 
        memoryManager.removeEventListener(element, key),
    
    createWeakCache: () => memoryManager.createWeakCache(),
    detectLeaks: () => memoryManager.detectLeaks(),
    getReport: () => memoryManager.getMemoryReport(),
    
    cleanup: () => memoryManager.cleanup()
};

// Example usage
console.log('Browser & Runtime Environment guide loaded with comprehensive examples!');
```

---

*This completes the comprehensive Browser & Runtime Environment guide with detailed interview explanations covering DOM Manipulation, Event System, Storage Mechanisms, Web APIs, Security, and Performance Optimization.*
