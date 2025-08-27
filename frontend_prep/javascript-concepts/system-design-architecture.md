# 🏗️ System Design & Architecture - Detailed Guide

> **Master system design patterns, architecture concepts, and scalable application development with comprehensive explanations and practical examples**

---

## 📋 Table of Contents

1. [Design Patterns](#1-design-patterns)
2. [Large-Scale Applications](#2-large-scale-applications)
3. [Code Quality & Maintainability](#3-code-quality--maintainability)

---

## 1. Design Patterns

> **Interview Explanation:** Design patterns are reusable solutions to commonly occurring problems in software design. They represent best practices and provide a common vocabulary for developers. Understanding these patterns is crucial for building maintainable and scalable applications.

### 🎯 Singleton Pattern

> **Interview Key Point:** The Singleton pattern ensures that a class has only one instance and provides global access to that instance. It's useful for managing shared resources like database connections, loggers, or configuration objects.

#### **Modern Singleton Implementation**

```javascript
// ES6 Module-based Singleton (Recommended)
class DatabaseConnection {
    constructor() {
        if (DatabaseConnection.instance) {
            return DatabaseConnection.instance;
        }
        
        this.connection = null;
        this.isConnected = false;
        this.config = {
            host: 'localhost',
            port: 5432,
            database: 'myapp'
        };
        
        DatabaseConnection.instance = this;
        return this;
    }
    
    async connect() {
        if (this.isConnected) {
            return this.connection;
        }
        
        try {
            // Simulate database connection
            this.connection = await this.createConnection();
            this.isConnected = true;
            console.log('Database connected successfully');
            return this.connection;
        } catch (error) {
            console.error('Database connection failed:', error);
            throw error;
        }
    }
    
    async createConnection() {
        // Simulate async connection creation
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve({
                    id: Math.random().toString(36),
                    host: this.config.host,
                    port: this.config.port,
                    status: 'connected'
                });
            }, 1000);
        });
    }
    
    async disconnect() {
        if (!this.isConnected) return;
        
        this.connection = null;
        this.isConnected = false;
        console.log('Database disconnected');
    }
    
    getConnection() {
        if (!this.isConnected) {
            throw new Error('Database not connected. Call connect() first.');
        }
        return this.connection;
    }
    
    updateConfig(newConfig) {
        if (this.isConnected) {
            throw new Error('Cannot update config while connected');
        }
        this.config = { ...this.config, ...newConfig };
    }
}

// Ensure singleton behavior
DatabaseConnection.instance = null;

// Advanced Singleton with lazy initialization and thread safety
class ConfigManager {
    constructor() {
        if (ConfigManager._instance) {
            return ConfigManager._instance;
        }
        
        this._config = new Map();
        this._observers = new Set();
        this._isInitialized = false;
        
        ConfigManager._instance = this;
        Object.freeze(this);
    }
    
    static getInstance() {
        if (!ConfigManager._instance) {
            ConfigManager._instance = new ConfigManager();
        }
        return ConfigManager._instance;
    }
    
    async initialize(configPath = '/api/config') {
        if (this._isInitialized) {
            return this._config;
        }
        
        try {
            const response = await fetch(configPath);
            const config = await response.json();
            
            Object.entries(config).forEach(([key, value]) => {
                this._config.set(key, value);
            });
            
            this._isInitialized = true;
            this._notifyObservers('initialized', this._config);
            
            return this._config;
        } catch (error) {
            console.error('Failed to initialize config:', error);
            throw error;
        }
    }
    
    get(key, defaultValue = null) {
        if (!this._isInitialized) {
            throw new Error('ConfigManager not initialized. Call initialize() first.');
        }
        return this._config.get(key) ?? defaultValue;
    }
    
    set(key, value) {
        const oldValue = this._config.get(key);
        this._config.set(key, value);
        
        this._notifyObservers('changed', { key, oldValue, newValue: value });
    }
    
    has(key) {
        return this._config.has(key);
    }
    
    addObserver(callback) {
        this._observers.add(callback);
    }
    
    removeObserver(callback) {
        this._observers.delete(callback);
    }
    
    _notifyObservers(event, data) {
        this._observers.forEach(callback => {
            try {
                callback(event, data);
            } catch (error) {
                console.error('Observer error:', error);
            }
        });
    }
    
    // Reset singleton (useful for testing)
    static reset() {
        if (ConfigManager._instance) {
            ConfigManager._instance._config.clear();
            ConfigManager._instance._observers.clear();
            ConfigManager._instance._isInitialized = false;
            ConfigManager._instance = null;
        }
    }
}

// Usage examples
const db1 = new DatabaseConnection();
const db2 = new DatabaseConnection();
console.log(db1 === db2); // true - same instance

// Modern module-based singleton (recommended approach)
// config-singleton.js
let instance = null;

class ModernConfigManager {
    constructor() {
        if (instance) {
            throw new Error('Use ConfigManager.getInstance() instead of new');
        }
        
        this.config = new Map();
        this.initialized = false;
    }
    
    static getInstance() {
        if (!instance) {
            instance = new ModernConfigManager();
        }
        return instance;
    }
    
    async load(source) {
        if (this.initialized) return;
        
        const config = await this.fetchConfig(source);
        this.config = new Map(Object.entries(config));
        this.initialized = true;
    }
    
    async fetchConfig(source) {
        // Implementation depends on source type
        if (typeof source === 'string') {
            const response = await fetch(source);
            return response.json();
        }
        return source;
    }
    
    get(key) {
        return this.config.get(key);
    }
    
    set(key, value) {
        this.config.set(key, value);
    }
}

export default ModernConfigManager.getInstance();
```

### 🎯 Observer Pattern

> **Interview Key Point:** The Observer pattern defines a one-to-many dependency between objects. When one object (subject) changes state, all dependent objects (observers) are automatically notified. This promotes loose coupling between objects.

#### **Comprehensive Observer Implementation**

```javascript
// Advanced Observer Pattern with typed events
class TypedEventEmitter {
    constructor() {
        this.events = new Map();
        this.onceEvents = new Map();
        this.maxListeners = 10;
        this.listenerCount = new Map();
    }
    
    // Add event listener
    on(event, listener, context = null) {
        if (typeof listener !== 'function') {
            throw new TypeError('Listener must be a function');
        }
        
        this._addListener(event, listener, context, false);
        return this;
    }
    
    // Add one-time event listener
    once(event, listener, context = null) {
        if (typeof listener !== 'function') {
            throw new TypeError('Listener must be a function');
        }
        
        this._addListener(event, listener, context, true);
        return this;
    }
    
    // Remove event listener
    off(event, listener, context = null) {
        if (!this.events.has(event)) {
            return this;
        }
        
        const listeners = this.events.get(event);
        const index = listeners.findIndex(item => 
            item.listener === listener && 
            item.context === context
        );
        
        if (index !== -1) {
            listeners.splice(index, 1);
            this._decrementListenerCount(event);
            
            if (listeners.length === 0) {
                this.events.delete(event);
                this.listenerCount.delete(event);
            }
        }
        
        return this;
    }
    
    // Emit event
    emit(event, ...args) {
        const listeners = this.events.get(event);
        if (!listeners || listeners.length === 0) {
            return false;
        }
        
        // Create a copy to avoid issues if listeners are modified during iteration
        const listenersCopy = [...listeners];
        
        listenersCopy.forEach(({ listener, context, once }) => {
            try {
                if (context) {
                    listener.apply(context, args);
                } else {
                    listener(...args);
                }
                
                // Remove one-time listeners
                if (once) {
                    this.off(event, listener, context);
                }
            } catch (error) {
                console.error(`Error in listener for event '${event}':`, error);
            }
        });
        
        return true;
    }
    
    // Remove all listeners for an event
    removeAllListeners(event = null) {
        if (event === null) {
            this.events.clear();
            this.listenerCount.clear();
        } else {
            this.events.delete(event);
            this.listenerCount.delete(event);
        }
        return this;
    }
    
    // Get listeners for an event
    listeners(event) {
        const listeners = this.events.get(event);
        return listeners ? listeners.map(item => item.listener) : [];
    }
    
    // Get listener count
    listenerCount(event) {
        return this.listenerCount.get(event) || 0;
    }
    
    // Set max listeners
    setMaxListeners(n) {
        this.maxListeners = n;
        return this;
    }
    
    // Get event names
    eventNames() {
        return Array.from(this.events.keys());
    }
    
    // Private helper methods
    _addListener(event, listener, context, once) {
        if (!this.events.has(event)) {
            this.events.set(event, []);
            this.listenerCount.set(event, 0);
        }
        
        const count = this.listenerCount.get(event);
        if (count >= this.maxListeners) {
            console.warn(
                `MaxListenersExceededWarning: Possible memory leak detected. ` +
                `${count} listeners added for event '${event}'. ` +
                `Use setMaxListeners() to increase limit.`
            );
        }
        
        this.events.get(event).push({
            listener,
            context,
            once
        });
        
        this._incrementListenerCount(event);
    }
    
    _incrementListenerCount(event) {
        const current = this.listenerCount.get(event) || 0;
        this.listenerCount.set(event, current + 1);
    }
    
    _decrementListenerCount(event) {
        const current = this.listenerCount.get(event) || 0;
        this.listenerCount.set(event, Math.max(0, current - 1));
    }
}

// Observable State Management
class ObservableState {
    constructor(initialState = {}) {
        this.state = { ...initialState };
        this.eventEmitter = new TypedEventEmitter();
        this.history = [{ ...initialState }];
        this.maxHistorySize = 50;
        
        // Create proxied state for automatic change detection
        this.proxiedState = this._createStateProxy();
    }
    
    _createStateProxy() {
        return new Proxy(this.state, {
            set: (target, property, value) => {
                const oldValue = target[property];
                
                if (oldValue !== value) {
                    const previousState = { ...target };
                    target[property] = value;
                    
                    // Add to history
                    this._addToHistory({ ...target });
                    
                    // Emit specific property change
                    this.eventEmitter.emit(`change:${property}`, {
                        property,
                        newValue: value,
                        oldValue,
                        state: { ...target }
                    });
                    
                    // Emit general change event
                    this.eventEmitter.emit('change', {
                        property,
                        newValue: value,
                        oldValue,
                        previousState,
                        currentState: { ...target }
                    });
                }
                
                return true;
            },
            
            get: (target, property) => {
                return target[property];
            }
        });
    }
    
    // Get current state
    getState() {
        return { ...this.state };
    }
    
    // Set state
    setState(updates) {
        if (typeof updates === 'function') {
            updates = updates(this.getState());
        }
        
        const previousState = { ...this.state };
        Object.assign(this.state, updates);
        
        this._addToHistory({ ...this.state });
        
        // Emit change events for each updated property
        Object.keys(updates).forEach(property => {
            this.eventEmitter.emit(`change:${property}`, {
                property,
                newValue: this.state[property],
                oldValue: previousState[property],
                state: this.getState()
            });
        });
        
        // Emit general change event
        this.eventEmitter.emit('change', {
            updates,
            previousState,
            currentState: this.getState()
        });
    }
    
    // Subscribe to state changes
    subscribe(callback) {
        this.eventEmitter.on('change', callback);
        
        // Return unsubscribe function
        return () => {
            this.eventEmitter.off('change', callback);
        };
    }
    
    // Subscribe to specific property changes
    subscribeToProperty(property, callback) {
        this.eventEmitter.on(`change:${property}`, callback);
        
        return () => {
            this.eventEmitter.off(`change:${property}`, callback);
        };
    }
    
    // Get state history
    getHistory() {
        return [...this.history];
    }
    
    // Undo last change
    undo() {
        if (this.history.length > 1) {
            this.history.pop(); // Remove current state
            const previousState = this.history[this.history.length - 1];
            this.state = { ...previousState };
            
            this.eventEmitter.emit('undo', {
                state: this.getState()
            });
        }
    }
    
    // Clear history
    clearHistory() {
        this.history = [{ ...this.state }];
    }
    
    _addToHistory(state) {
        this.history.push(state);
        
        // Limit history size
        if (this.history.length > this.maxHistorySize) {
            this.history.shift();
        }
    }
}

// Model-View pattern with Observer
class Model extends TypedEventEmitter {
    constructor(data = {}) {
        super();
        this.data = { ...data };
        this.validators = new Map();
        this.isDirty = false;
    }
    
    // Get property value
    get(property) {
        return this.data[property];
    }
    
    // Set property value with validation
    set(property, value) {
        // Validate if validator exists
        if (this.validators.has(property)) {
            const validator = this.validators.get(property);
            const isValid = validator(value);
            
            if (!isValid) {
                this.emit('validation:error', {
                    property,
                    value,
                    message: `Validation failed for property '${property}'`
                });
                return false;
            }
        }
        
        const oldValue = this.data[property];
        
        if (oldValue !== value) {
            this.data[property] = value;
            this.isDirty = true;
            
            this.emit('change', {
                property,
                newValue: value,
                oldValue,
                model: this
            });
            
            this.emit(`change:${property}`, {
                newValue: value,
                oldValue,
                model: this
            });
        }
        
        return true;
    }
    
    // Set multiple properties
    setAll(updates) {
        const changes = [];
        
        Object.entries(updates).forEach(([property, value]) => {
            const oldValue = this.data[property];
            if (this.set(property, value)) {
                changes.push({ property, newValue: value, oldValue });
            }
        });
        
        if (changes.length > 0) {
            this.emit('batch:change', {
                changes,
                model: this
            });
        }
    }
    
    // Add property validator
    addValidator(property, validator) {
        this.validators.set(property, validator);
    }
    
    // Get all data
    toJSON() {
        return { ...this.data };
    }
    
    // Reset dirty flag
    markClean() {
        this.isDirty = false;
        this.emit('clean', { model: this });
    }
    
    // Check if model has unsaved changes
    isDirtyState() {
        return this.isDirty;
    }
}

// View component that observes model
class View {
    constructor(model, element) {
        this.model = model;
        this.element = element;
        this.bindings = new Map();
        
        this.setupObservers();
    }
    
    setupObservers() {
        // Listen to model changes
        this.model.on('change', (data) => {
            this.render(data);
        });
        
        this.model.on('validation:error', (error) => {
            this.showValidationError(error);
        });
    }
    
    // Bind model property to DOM element
    bindProperty(property, element, attribute = 'textContent') {
        this.bindings.set(property, { element, attribute });
        
        // Set initial value
        element[attribute] = this.model.get(property);
        
        // Listen for changes
        this.model.on(`change:${property}`, (data) => {
            element[attribute] = data.newValue;
        });
    }
    
    render(data) {
        // Update bound elements
        this.bindings.forEach(({ element, attribute }, property) => {
            element[attribute] = this.model.get(property);
        });
        
        // Custom render logic can be implemented here
        this.onRender(data);
    }
    
    onRender(data) {
        // Override in subclasses
    }
    
    showValidationError(error) {
        console.error('Validation error:', error);
        // Show error in UI
    }
    
    destroy() {
        this.model.removeAllListeners();
        this.bindings.clear();
    }
}

// Usage Examples
const appState = new ObservableState({
    user: { name: 'John', email: 'john@example.com' },
    settings: { theme: 'dark', language: 'en' }
});

// Subscribe to all changes
const unsubscribe = appState.subscribe((change) => {
    console.log('State changed:', change);
});

// Subscribe to specific property
const unsubscribeUser = appState.subscribeToProperty('user', (change) => {
    console.log('User changed:', change);
});

// Update state
appState.setState({
    user: { name: 'Jane', email: 'jane@example.com' }
});

// Model-View example
const userModel = new Model({
    name: 'John Doe',
    email: 'john@example.com',
    age: 30
});

// Add validation
userModel.addValidator('email', (value) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
});

userModel.addValidator('age', (value) => {
    return typeof value === 'number' && value >= 0 && value <= 150;
});

// Create view
const userView = new View(userModel, document.getElementById('user-profile'));

// Bind properties to DOM elements
userView.bindProperty('name', document.getElementById('user-name'));
userView.bindProperty('email', document.getElementById('user-email'));
```

### 🎯 Factory Pattern

> **Interview Key Point:** The Factory pattern provides an interface for creating objects without specifying their exact classes. It promotes loose coupling by eliminating the need to bind application-specific classes into your code.

#### **Advanced Factory Implementations**

```javascript
// Abstract Factory Pattern
class UIComponentFactory {
    constructor(theme = 'default') {
        this.theme = theme;
        this.componentRegistry = new Map();
        this.registerDefaultComponents();
    }
    
    registerDefaultComponents() {
        // Register default component creators
        this.register('button', ButtonFactory);
        this.register('input', InputFactory);
        this.register('modal', ModalFactory);
        this.register('card', CardFactory);
    }
    
    // Register component factory
    register(type, factory) {
        this.componentRegistry.set(type, factory);
    }
    
    // Create component
    create(type, props = {}, children = []) {
        const Factory = this.componentRegistry.get(type);
        
        if (!Factory) {
            throw new Error(`Component type '${type}' not registered`);
        }
        
        return Factory.create({
            ...props,
            theme: this.theme,
            children
        });
    }
    
    // Create multiple components
    createBatch(components) {
        return components.map(({ type, props, children }) => 
            this.create(type, props, children)
        );
    }
    
    // Get available component types
    getAvailableTypes() {
        return Array.from(this.componentRegistry.keys());
    }
    
    // Clone factory with different theme
    withTheme(theme) {
        const newFactory = new UIComponentFactory(theme);
        // Copy registered components
        this.componentRegistry.forEach((factory, type) => {
            newFactory.register(type, factory);
        });
        return newFactory;
    }
}

// Individual Component Factories
class ButtonFactory {
    static create({ theme = 'default', variant = 'primary', size = 'medium', children = [], ...props }) {
        const button = document.createElement('button');
        
        // Apply theme-specific classes
        const themeClasses = this.getThemeClasses(theme, variant, size);
        button.className = themeClasses.join(' ');
        
        // Set properties
        Object.entries(props).forEach(([key, value]) => {
            if (key.startsWith('on') && typeof value === 'function') {
                // Event handler
                const eventName = key.slice(2).toLowerCase();
                button.addEventListener(eventName, value);
            } else if (key === 'disabled') {
                button.disabled = value;
            } else {
                button.setAttribute(key, value);
            }
        });
        
        // Add children
        children.forEach(child => {
            if (typeof child === 'string') {
                button.appendChild(document.createTextNode(child));
            } else {
                button.appendChild(child);
            }
        });
        
        return button;
    }
    
    static getThemeClasses(theme, variant, size) {
        const baseClasses = ['btn'];
        
        switch (theme) {
            case 'dark':
                baseClasses.push('btn-dark', `btn-${variant}-dark`, `btn-${size}`);
                break;
            case 'light':
                baseClasses.push('btn-light', `btn-${variant}-light`, `btn-${size}`);
                break;
            default:
                baseClasses.push(`btn-${variant}`, `btn-${size}`);
        }
        
        return baseClasses;
    }
}

class InputFactory {
    static create({ theme = 'default', type = 'text', validation = null, ...props }) {
        const container = document.createElement('div');
        container.className = `input-container input-container-${theme}`;
        
        const input = document.createElement('input');
        input.type = type;
        input.className = `input input-${theme}`;
        
        // Set properties
        Object.entries(props).forEach(([key, value]) => {
            if (key.startsWith('on') && typeof value === 'function') {
                const eventName = key.slice(2).toLowerCase();
                input.addEventListener(eventName, value);
            } else {
                input.setAttribute(key, value);
            }
        });
        
        // Add validation
        if (validation) {
            this.addValidation(input, validation);
        }
        
        // Add label if provided
        if (props.label) {
            const label = document.createElement('label');
            label.textContent = props.label;
            label.className = `label label-${theme}`;
            if (props.id) label.setAttribute('for', props.id);
            container.appendChild(label);
        }
        
        container.appendChild(input);
        
        // Add error container
        const errorContainer = document.createElement('div');
        errorContainer.className = `error-container error-container-${theme}`;
        container.appendChild(errorContainer);
        
        return container;
    }
    
    static addValidation(input, validation) {
        input.addEventListener('blur', () => {
            const value = input.value;
            const isValid = validation.validator(value);
            
            const errorContainer = input.parentNode.querySelector('.error-container');
            
            if (isValid) {
                input.classList.remove('invalid');
                input.classList.add('valid');
                errorContainer.textContent = '';
            } else {
                input.classList.remove('valid');
                input.classList.add('invalid');
                errorContainer.textContent = validation.message || 'Invalid input';
            }
        });
    }
}

class ModalFactory {
    static create({ theme = 'default', title = '', closable = true, ...props }) {
        const overlay = document.createElement('div');
        overlay.className = `modal-overlay modal-overlay-${theme}`;
        
        const modal = document.createElement('div');
        modal.className = `modal modal-${theme}`;
        
        // Header
        if (title || closable) {
            const header = document.createElement('div');
            header.className = `modal-header modal-header-${theme}`;
            
            if (title) {
                const titleElement = document.createElement('h2');
                titleElement.className = `modal-title modal-title-${theme}`;
                titleElement.textContent = title;
                header.appendChild(titleElement);
            }
            
            if (closable) {
                const closeButton = document.createElement('button');
                closeButton.className = `modal-close modal-close-${theme}`;
                closeButton.textContent = '×';
                closeButton.addEventListener('click', () => {
                    this.close(overlay);
                });
                header.appendChild(closeButton);
            }
            
            modal.appendChild(header);
        }
        
        // Body
        const body = document.createElement('div');
        body.className = `modal-body modal-body-${theme}`;
        modal.appendChild(body);
        
        // Footer
        const footer = document.createElement('div');
        footer.className = `modal-footer modal-footer-${theme}`;
        modal.appendChild(footer);
        
        overlay.appendChild(modal);
        
        // Add methods
        overlay.setContent = (content) => {
            if (typeof content === 'string') {
                body.innerHTML = content;
            } else {
                body.innerHTML = '';
                body.appendChild(content);
            }
        };
        
        overlay.addFooterButton = (text, onClick, variant = 'primary') => {
            const button = ButtonFactory.create({
                theme,
                variant,
                children: [text],
                onclick: onClick
            });
            footer.appendChild(button);
        };
        
        overlay.show = () => {
            document.body.appendChild(overlay);
            overlay.style.display = 'flex';
        };
        
        overlay.hide = () => {
            this.close(overlay);
        };
        
        return overlay;
    }
    
    static close(overlay) {
        overlay.style.display = 'none';
        if (overlay.parentNode) {
            overlay.parentNode.removeChild(overlay);
        }
    }
}

// Plugin Factory for extensible architecture
class PluginFactory {
    constructor() {
        this.plugins = new Map();
        this.hooks = new Map();
    }
    
    // Register plugin
    register(name, plugin) {
        if (typeof plugin.init !== 'function') {
            throw new Error('Plugin must have an init method');
        }
        
        this.plugins.set(name, plugin);
        
        // Initialize plugin
        plugin.init(this);
        
        return this;
    }
    
    // Get plugin instance
    get(name) {
        return this.plugins.get(name);
    }
    
    // Check if plugin exists
    has(name) {
        return this.plugins.has(name);
    }
    
    // Register hook
    addHook(hookName, callback) {
        if (!this.hooks.has(hookName)) {
            this.hooks.set(hookName, []);
        }
        this.hooks.get(hookName).push(callback);
    }
    
    // Execute hook
    executeHook(hookName, ...args) {
        const hooks = this.hooks.get(hookName) || [];
        return hooks.map(hook => hook(...args));
    }
    
    // Remove plugin
    unregister(name) {
        const plugin = this.plugins.get(name);
        if (plugin && typeof plugin.destroy === 'function') {
            plugin.destroy();
        }
        this.plugins.delete(name);
    }
    
    // Get all plugin names
    getPluginNames() {
        return Array.from(this.plugins.keys());
    }
}

// Usage Examples
const uiFactory = new UIComponentFactory('dark');

// Create components
const button = uiFactory.create('button', {
    variant: 'primary',
    size: 'large',
    onclick: () => console.log('Button clicked!'),
    children: ['Click Me']
});

const input = uiFactory.create('input', {
    type: 'email',
    label: 'Email Address',
    placeholder: 'Enter your email',
    validation: {
        validator: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
        message: 'Please enter a valid email address'
    }
});

const modal = uiFactory.create('modal', {
    title: 'Confirmation',
    closable: true
});

modal.setContent('<p>Are you sure you want to delete this item?</p>');
modal.addFooterButton('Cancel', () => modal.hide(), 'secondary');
modal.addFooterButton('Delete', () => {
    console.log('Item deleted');
    modal.hide();
}, 'danger');

// Plugin system example
const pluginFactory = new PluginFactory();

// Analytics plugin
const analyticsPlugin = {
    init(factory) {
        this.factory = factory;
        console.log('Analytics plugin initialized');
        
        // Add hook for tracking events
        factory.addHook('user:action', (action, data) => {
            this.track(action, data);
        });
    },
    
    track(event, data) {
        console.log('Analytics:', event, data);
        // Send to analytics service
    },
    
    destroy() {
        console.log('Analytics plugin destroyed');
    }
};

pluginFactory.register('analytics', analyticsPlugin);
```

### 🎯 Module Pattern

> **Interview Key Point:** The Module pattern provides encapsulation and creates a public API while keeping implementation details private. It's essential for organizing code and preventing global namespace pollution.

#### **Modern Module Implementations**

```javascript
// Classic Module Pattern (IIFE)
const UserModule = (function() {
    // Private variables and functions
    let users = [];
    let currentUser = null;
    const API_BASE = '/api/users';
    
    // Private helper functions
    function validateUser(user) {
        return user && 
               typeof user.name === 'string' && 
               typeof user.email === 'string' &&
               user.name.length > 0 &&
               /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(user.email);
    }
    
    function generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
    
    async function apiRequest(endpoint, options = {}) {
        const response = await fetch(API_BASE + endpoint, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`API request failed: ${response.statusText}`);
        }
        
        return response.json();
    }
    
    // Public API
    return {
        // Create user
        async createUser(userData) {
            if (!validateUser(userData)) {
                throw new Error('Invalid user data');
            }
            
            const user = {
                id: generateId(),
                ...userData,
                createdAt: new Date().toISOString()
            };
            
            try {
                const savedUser = await apiRequest('/', {
                    method: 'POST',
                    body: JSON.stringify(user)
                });
                
                users.push(savedUser);
                return savedUser;
            } catch (error) {
                console.error('Failed to create user:', error);
                throw error;
            }
        },
        
        // Get all users
        async getUsers() {
            try {
                users = await apiRequest('/');
                return [...users]; // Return copy to prevent mutation
            } catch (error) {
                console.error('Failed to fetch users:', error);
                return [...users]; // Return cached users on error
            }
        },
        
        // Get user by ID
        getUserById(id) {
            return users.find(user => user.id === id) || null;
        },
        
        // Update user
        async updateUser(id, updates) {
            const userIndex = users.findIndex(user => user.id === id);
            if (userIndex === -1) {
                throw new Error('User not found');
            }
            
            const updatedUser = { ...users[userIndex], ...updates };
            
            if (!validateUser(updatedUser)) {
                throw new Error('Invalid user data');
            }
            
            try {
                const savedUser = await apiRequest(`/${id}`, {
                    method: 'PUT',
                    body: JSON.stringify(updatedUser)
                });
                
                users[userIndex] = savedUser;
                return savedUser;
            } catch (error) {
                console.error('Failed to update user:', error);
                throw error;
            }
        },
        
        // Delete user
        async deleteUser(id) {
            const userIndex = users.findIndex(user => user.id === id);
            if (userIndex === -1) {
                throw new Error('User not found');
            }
            
            try {
                await apiRequest(`/${id}`, { method: 'DELETE' });
                users.splice(userIndex, 1);
                
                if (currentUser && currentUser.id === id) {
                    currentUser = null;
                }
                
                return true;
            } catch (error) {
                console.error('Failed to delete user:', error);
                throw error;
            }
        },
        
        // Current user management
        setCurrentUser(user) {
            currentUser = user;
        },
        
        getCurrentUser() {
            return currentUser ? { ...currentUser } : null;
        },
        
        // Search users
        searchUsers(query) {
            const lowercaseQuery = query.toLowerCase();
            return users.filter(user => 
                user.name.toLowerCase().includes(lowercaseQuery) ||
                user.email.toLowerCase().includes(lowercaseQuery)
            );
        },
        
        // Get user count
        getUserCount() {
            return users.length;
        },
        
        // Clear all users (for testing)
        clearUsers() {
            users = [];
            currentUser = null;
        }
    };
})();

// ES6 Module Pattern
class ModuleManager {
    constructor() {
        this.modules = new Map();
        this.dependencies = new Map();
        this.instances = new Map();
    }
    
    // Define module
    define(name, dependencies = [], factory) {
        if (this.modules.has(name)) {
            throw new Error(`Module '${name}' already defined`);
        }
        
        this.modules.set(name, { dependencies, factory });
        this.dependencies.set(name, dependencies);
    }
    
    // Require module
    require(name) {
        if (this.instances.has(name)) {
            return this.instances.get(name);
        }
        
        if (!this.modules.has(name)) {
            throw new Error(`Module '${name}' not found`);
        }
        
        const module = this.modules.get(name);
        const deps = module.dependencies.map(dep => this.require(dep));
        
        const instance = module.factory(...deps);
        this.instances.set(name, instance);
        
        return instance;
    }
    
    // Check if module exists
    has(name) {
        return this.modules.has(name);
    }
    
    // Get dependency graph
    getDependencyGraph() {
        const graph = {};
        this.dependencies.forEach((deps, name) => {
            graph[name] = deps;
        });
        return graph;
    }
    
    // Detect circular dependencies
    detectCircularDependencies() {
        const visited = new Set();
        const recursionStack = new Set();
        const circular = [];
        
        const visit = (module, path = []) => {
            if (recursionStack.has(module)) {
                circular.push([...path, module]);
                return;
            }
            
            if (visited.has(module)) {
                return;
            }
            
            visited.add(module);
            recursionStack.add(module);
            
            const deps = this.dependencies.get(module) || [];
            deps.forEach(dep => {
                visit(dep, [...path, module]);
            });
            
            recursionStack.delete(module);
        };
        
        this.modules.forEach((_, name) => {
            visit(name);
        });
        
        return circular;
    }
    
    // Clear module cache
    clearCache(name = null) {
        if (name) {
            this.instances.delete(name);
        } else {
            this.instances.clear();
        }
    }
}

// Namespace Module Pattern
const App = {
    // Core modules
    Core: {
        Utils: {
            // Utility functions
            debounce(func, wait) {
                let timeout;
                return function executedFunction(...args) {
                    const later = () => {
                        clearTimeout(timeout);
                        func(...args);
                    };
                    clearTimeout(timeout);
                    timeout = setTimeout(later, wait);
                };
            },
            
            throttle(func, limit) {
                let inThrottle;
                return function() {
                    const args = arguments;
                    const context = this;
                    if (!inThrottle) {
                        func.apply(context, args);
                        inThrottle = true;
                        setTimeout(() => inThrottle = false, limit);
                    }
                };
            },
            
            deepClone(obj) {
                if (obj === null || typeof obj !== 'object') return obj;
                if (obj instanceof Date) return new Date(obj.getTime());
                if (obj instanceof Array) return obj.map(item => this.deepClone(item));
                if (typeof obj === 'object') {
                    const clonedObj = {};
                    for (const key in obj) {
                        if (obj.hasOwnProperty(key)) {
                            clonedObj[key] = this.deepClone(obj[key]);
                        }
                    }
                    return clonedObj;
                }
            }
        },
        
        EventBus: (function() {
            const events = {};
            
            return {
                on(event, callback) {
                    if (!events[event]) {
                        events[event] = [];
                    }
                    events[event].push(callback);
                },
                
                off(event, callback) {
                    if (events[event]) {
                        events[event] = events[event].filter(cb => cb !== callback);
                    }
                },
                
                emit(event, data) {
                    if (events[event]) {
                        events[event].forEach(callback => callback(data));
                    }
                },
                
                once(event, callback) {
                    const onceCallback = (data) => {
                        callback(data);
                        this.off(event, onceCallback);
                    };
                    this.on(event, onceCallback);
                }
            };
        })(),
        
        Storage: (function() {
            const isLocalStorageAvailable = () => {
                try {
                    const test = '__localStorage_test__';
                    localStorage.setItem(test, test);
                    localStorage.removeItem(test);
                    return true;
                } catch (e) {
                    return false;
                }
            };
            
            const fallbackStorage = new Map();
            const useLocalStorage = isLocalStorageAvailable();
            
            return {
                set(key, value) {
                    const serialized = JSON.stringify(value);
                    if (useLocalStorage) {
                        localStorage.setItem(key, serialized);
                    } else {
                        fallbackStorage.set(key, serialized);
                    }
                },
                
                get(key, defaultValue = null) {
                    let value;
                    if (useLocalStorage) {
                        value = localStorage.getItem(key);
                    } else {
                        value = fallbackStorage.get(key);
                    }
                    
                    if (value === null) return defaultValue;
                    
                    try {
                        return JSON.parse(value);
                    } catch (e) {
                        return defaultValue;
                    }
                },
                
                remove(key) {
                    if (useLocalStorage) {
                        localStorage.removeItem(key);
                    } else {
                        fallbackStorage.delete(key);
                    }
                },
                
                clear() {
                    if (useLocalStorage) {
                        localStorage.clear();
                    } else {
                        fallbackStorage.clear();
                    }
                },
                
                keys() {
                    if (useLocalStorage) {
                        return Object.keys(localStorage);
                    } else {
                        return Array.from(fallbackStorage.keys());
                    }
                }
            };
        })()
    },
    
    // UI modules
    UI: {
        Components: {},
        Themes: {},
        Layout: {}
    },
    
    // Data modules
    Data: {
        Models: {},
        Services: {},
        Cache: {}
    },
    
    // Initialize application
    init() {
        console.log('App initialized');
        this.Core.EventBus.emit('app:init');
    }
};

// Usage Examples
const moduleManager = new ModuleManager();

// Define modules
moduleManager.define('logger', [], () => {
    return {
        log: (message) => console.log(`[LOG] ${message}`),
        error: (message) => console.error(`[ERROR] ${message}`),
        warn: (message) => console.warn(`[WARN] ${message}`)
    };
});

moduleManager.define('api', ['logger'], (logger) => {
    return {
        async get(url) {
            logger.log(`GET request to ${url}`);
            // Implementation
        },
        async post(url, data) {
            logger.log(`POST request to ${url}`);
            // Implementation
        }
    };
});

moduleManager.define('userService', ['api', 'logger'], (api, logger) => {
    return {
        async getUsers() {
            logger.log('Fetching users');
            return api.get('/users');
        },
        async createUser(userData) {
            logger.log('Creating user');
            return api.post('/users', userData);
        }
    };
});

// Use modules
const userService = moduleManager.require('userService');
```

### 🎯 Publish-Subscribe Pattern

> **Interview Key Point:** The Publish-Subscribe pattern allows objects to subscribe to events and be notified when those events occur. Unlike the Observer pattern, publishers and subscribers don't need to know about each other directly, promoting loose coupling.

#### **Advanced Pub-Sub Implementation**

```javascript
// Enhanced PubSub with channels, wildcards, and middleware
class PubSubManager {
    constructor() {
        this.subscribers = new Map();
        this.channels = new Map();
        this.middleware = [];
        this.history = [];
        this.maxHistorySize = 1000;
        this.isEnabled = true;
    }
    
    // Subscribe to events with optional channel
    subscribe(event, callback, options = {}) {
        const {
            channel = 'default',
            priority = 0,
            once = false,
            condition = null
        } = options;
        
        const subscription = {
            id: this.generateId(),
            event,
            callback,
            channel,
            priority,
            once,
            condition,
            subscribedAt: Date.now()
        };
        
        // Create channel if it doesn't exist
        if (!this.channels.has(channel)) {
            this.channels.set(channel, new Map());
        }
        
        const channelEvents = this.channels.get(channel);
        
        // Create event array if it doesn't exist
        if (!channelEvents.has(event)) {
            channelEvents.set(event, []);
        }
        
        // Add subscription and sort by priority
        const eventSubscriptions = channelEvents.get(event);
        eventSubscriptions.push(subscription);
        eventSubscriptions.sort((a, b) => b.priority - a.priority);
        
        // Store in main subscribers map for quick lookup
        this.subscribers.set(subscription.id, subscription);
        
        // Return unsubscribe function
        return () => this.unsubscribe(subscription.id);
    }
    
    // Unsubscribe from events
    unsubscribe(subscriptionId) {
        const subscription = this.subscribers.get(subscriptionId);
        if (!subscription) return false;
        
        const { event, channel } = subscription;
        const channelEvents = this.channels.get(channel);
        
        if (channelEvents && channelEvents.has(event)) {
            const eventSubscriptions = channelEvents.get(event);
            const index = eventSubscriptions.findIndex(sub => sub.id === subscriptionId);
            
            if (index !== -1) {
                eventSubscriptions.splice(index, 1);
                
                // Clean up empty arrays
                if (eventSubscriptions.length === 0) {
                    channelEvents.delete(event);
                }
            }
        }
        
        // Clean up empty channels
        if (channelEvents && channelEvents.size === 0) {
            this.channels.delete(channel);
        }
        
        this.subscribers.delete(subscriptionId);
        return true;
    }
    
    // Publish event to subscribers
    async publish(event, data = null, options = {}) {
        if (!this.isEnabled) return [];
        
        const {
            channel = 'default',
            async = false,
            timeout = 5000
        } = options;
        
        const eventData = {
            event,
            data,
            channel,
            timestamp: Date.now(),
            id: this.generateId()
        };
        
        // Add to history
        this.addToHistory(eventData);
        
        // Apply middleware
        const processedData = await this.applyMiddleware(eventData);
        
        if (processedData === false) {
            // Middleware cancelled the event
            return [];
        }
        
        // Get subscribers for this event
        const subscribers = this.getEventSubscribers(event, channel);
        
        if (subscribers.length === 0) {
            return [];
        }
        
        // Execute callbacks
        const results = [];
        
        if (async) {
            // Execute all callbacks in parallel
            const promises = subscribers.map(sub => 
                this.executeCallback(sub, processedData, timeout)
            );
            
            try {
                const allResults = await Promise.allSettled(promises);
                results.push(...allResults.map(result => 
                    result.status === 'fulfilled' ? result.value : result.reason
                ));
            } catch (error) {
                console.error('Error in async publish:', error);
            }
        } else {
            // Execute callbacks synchronously
            for (const subscription of subscribers) {
                try {
                    const result = await this.executeCallback(subscription, processedData, timeout);
                    results.push(result);
                } catch (error) {
                    console.error('Error executing callback:', error);
                    results.push(error);
                }
            }
        }
        
        return results;
    }
    
    // Execute individual callback
    async executeCallback(subscription, eventData, timeout) {
        const { callback, condition, once, id } = subscription;
        
        // Check condition if provided
        if (condition && !condition(eventData)) {
            return null;
        }
        
        // Remove one-time subscriptions
        if (once) {
            this.unsubscribe(id);
        }
        
        // Execute callback with timeout
        try {
            const timeoutPromise = new Promise((_, reject) => {
                setTimeout(() => reject(new Error('Callback timeout')), timeout);
            });
            
            const callbackPromise = Promise.resolve(callback(eventData));
            
            return await Promise.race([callbackPromise, timeoutPromise]);
        } catch (error) {
            throw new Error(`Callback execution failed: ${error.message}`);
        }
    }
    
    // Get subscribers for an event (including wildcard matches)
    getEventSubscribers(event, channel) {
        const channelEvents = this.channels.get(channel);
        if (!channelEvents) return [];
        
        const subscribers = [];
        
        // Direct event matches
        if (channelEvents.has(event)) {
            subscribers.push(...channelEvents.get(event));
        }
        
        // Wildcard matches
        for (const [eventPattern, eventSubscribers] of channelEvents) {
            if (eventPattern.includes('*') && this.matchesWildcard(event, eventPattern)) {
                subscribers.push(...eventSubscribers);
            }
        }
        
        return subscribers;
    }
    
    // Check if event matches wildcard pattern
    matchesWildcard(event, pattern) {
        const regex = new RegExp(
            '^' + pattern.replace(/\*/g, '.*').replace(/\?/g, '.') + '$'
        );
        return regex.test(event);
    }
    
    // Add middleware function
    addMiddleware(middleware) {
        if (typeof middleware !== 'function') {
            throw new Error('Middleware must be a function');
        }
        this.middleware.push(middleware);
    }
    
    // Apply middleware to event data
    async applyMiddleware(eventData) {
        let processedData = { ...eventData };
        
        for (const middleware of this.middleware) {
            try {
                const result = await middleware(processedData);
                
                if (result === false) {
                    // Middleware cancelled the event
                    return false;
                } else if (result && typeof result === 'object') {
                    // Middleware modified the data
                    processedData = result;
                }
            } catch (error) {
                console.error('Middleware error:', error);
            }
        }
        
        return processedData;
    }
    
    // Get event history
    getHistory(filter = null) {
        if (!filter) return [...this.history];
        
        return this.history.filter(eventData => {
            if (filter.event && eventData.event !== filter.event) return false;
            if (filter.channel && eventData.channel !== filter.channel) return false;
            if (filter.since && eventData.timestamp < filter.since) return false;
            if (filter.until && eventData.timestamp > filter.until) return false;
            return true;
        });
    }
    
    // Clear event history
    clearHistory() {
        this.history = [];
    }
    
    // Add event to history
    addToHistory(eventData) {
        this.history.push(eventData);
        
        // Limit history size
        if (this.history.length > this.maxHistorySize) {
            this.history.shift();
        }
    }
    
    // Get statistics
    getStats() {
        const channelStats = {};
        let totalSubscribers = 0;
        
        this.channels.forEach((events, channel) => {
            let channelSubscribers = 0;
            const eventCounts = {};
            
            events.forEach((subscribers, event) => {
                eventCounts[event] = subscribers.length;
                channelSubscribers += subscribers.length;
            });
            
            channelStats[channel] = {
                events: Object.keys(eventCounts).length,
                subscribers: channelSubscribers,
                eventCounts
            };
            
            totalSubscribers += channelSubscribers;
        });
        
        return {
            totalChannels: this.channels.size,
            totalSubscribers,
            totalEvents: this.history.length,
            channelStats
        };
    }
    
    // Enable/disable event system
    enable() {
        this.isEnabled = true;
    }
    
    disable() {
        this.isEnabled = false;
    }
    
    // Clear all subscriptions
    clear() {
        this.subscribers.clear();
        this.channels.clear();
    }
    
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
}

// Message Queue Implementation
class MessageQueue {
    constructor(options = {}) {
        this.options = {
            maxSize: 1000,
            persistent: false,
            retryAttempts: 3,
            retryDelay: 1000,
            ...options
        };
        
        this.queue = [];
        this.processing = false;
        this.subscribers = new Map();
        this.deadLetterQueue = [];
        
        if (this.options.persistent) {
            this.loadFromStorage();
        }
    }
    
    // Add message to queue
    enqueue(message, priority = 0) {
        if (this.queue.length >= this.options.maxSize) {
            throw new Error('Queue is full');
        }
        
        const queueItem = {
            id: this.generateId(),
            message,
            priority,
            timestamp: Date.now(),
            attempts: 0,
            status: 'pending'
        };
        
        this.queue.push(queueItem);
        this.queue.sort((a, b) => b.priority - a.priority);
        
        if (this.options.persistent) {
            this.saveToStorage();
        }
        
        // Start processing if not already running
        if (!this.processing) {
            this.processQueue();
        }
        
        return queueItem.id;
    }
    
    // Process queue
    async processQueue() {
        if (this.processing || this.queue.length === 0) {
            return;
        }
        
        this.processing = true;
        
        while (this.queue.length > 0) {
            const item = this.queue.shift();
            
            try {
                await this.processMessage(item);
                item.status = 'completed';
            } catch (error) {
                item.attempts++;
                item.error = error.message;
                
                if (item.attempts < this.options.retryAttempts) {
                    // Retry after delay
                    setTimeout(() => {
                        this.queue.unshift(item);
                        this.queue.sort((a, b) => b.priority - a.priority);
                    }, this.options.retryDelay * item.attempts);
                } else {
                    // Move to dead letter queue
                    item.status = 'failed';
                    this.deadLetterQueue.push(item);
                }
            }
            
            if (this.options.persistent) {
                this.saveToStorage();
            }
        }
        
        this.processing = false;
    }
    
    // Process individual message
    async processMessage(item) {
        const { message } = item;
        const handlers = this.subscribers.get(message.type) || [];
        
        if (handlers.length === 0) {
            throw new Error(`No handlers for message type: ${message.type}`);
        }
        
        for (const handler of handlers) {
            await handler(message.data, item);
        }
    }
    
    // Subscribe to message type
    subscribe(messageType, handler) {
        if (!this.subscribers.has(messageType)) {
            this.subscribers.set(messageType, []);
        }
        
        this.subscribers.get(messageType).push(handler);
        
        return () => {
            const handlers = this.subscribers.get(messageType);
            const index = handlers.indexOf(handler);
            if (index !== -1) {
                handlers.splice(index, 1);
            }
        };
    }
    
    // Get queue status
    getStatus() {
        return {
            queueSize: this.queue.length,
            processing: this.processing,
            deadLetterQueueSize: this.deadLetterQueue.length,
            subscriberCount: this.subscribers.size
        };
    }
    
    // Clear queue
    clear() {
        this.queue = [];
        this.deadLetterQueue = [];
        if (this.options.persistent) {
            this.saveToStorage();
        }
    }
    
    // Save to localStorage (if persistent)
    saveToStorage() {
        if (typeof localStorage !== 'undefined') {
            localStorage.setItem('messageQueue', JSON.stringify({
                queue: this.queue,
                deadLetterQueue: this.deadLetterQueue
            }));
        }
    }
    
    // Load from localStorage (if persistent)
    loadFromStorage() {
        if (typeof localStorage !== 'undefined') {
            const saved = localStorage.getItem('messageQueue');
            if (saved) {
                try {
                    const data = JSON.parse(saved);
                    this.queue = data.queue || [];
                    this.deadLetterQueue = data.deadLetterQueue || [];
                } catch (error) {
                    console.error('Failed to load queue from storage:', error);
                }
            }
        }
    }
    
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }
}

// Real-time Event System
class RealTimeEventSystem {
    constructor(options = {}) {
        this.options = {
            websocketUrl: null,
            fallbackPolling: true,
            pollingInterval: 5000,
            reconnectAttempts: 5,
            reconnectDelay: 1000,
            ...options
        };
        
        this.pubsub = new PubSubManager();
        this.websocket = null;
        this.isConnected = false;
        this.reconnectCount = 0;
        this.pollingTimer = null;
        
        this.setupConnection();
    }
    
    // Setup connection (WebSocket or polling)
    async setupConnection() {
        if (this.options.websocketUrl) {
            await this.connectWebSocket();
        } else if (this.options.fallbackPolling) {
            this.startPolling();
        }
    }
    
    // Connect via WebSocket
    async connectWebSocket() {
        try {
            this.websocket = new WebSocket(this.options.websocketUrl);
            
            this.websocket.onopen = () => {
                this.isConnected = true;
                this.reconnectCount = 0;
                this.pubsub.publish('connection:opened');
            };
            
            this.websocket.onmessage = (event) => {
                try {
                    const message = JSON.parse(event.data);
                    this.handleMessage(message);
                } catch (error) {
                    console.error('Failed to parse WebSocket message:', error);
                }
            };
            
            this.websocket.onclose = () => {
                this.isConnected = false;
                this.pubsub.publish('connection:closed');
                this.attemptReconnect();
            };
            
            this.websocket.onerror = (error) => {
                console.error('WebSocket error:', error);
                this.pubsub.publish('connection:error', error);
            };
            
        } catch (error) {
            console.error('Failed to connect WebSocket:', error);
            if (this.options.fallbackPolling) {
                this.startPolling();
            }
        }
    }
    
    // Attempt to reconnect WebSocket
    attemptReconnect() {
        if (this.reconnectCount < this.options.reconnectAttempts) {
            this.reconnectCount++;
            const delay = this.options.reconnectDelay * this.reconnectCount;
            
            setTimeout(() => {
                this.connectWebSocket();
            }, delay);
        } else {
            console.error('Max reconnection attempts reached');
            if (this.options.fallbackPolling) {
                this.startPolling();
            }
        }
    }
    
    // Start polling fallback
    startPolling() {
        if (this.pollingTimer) return;
        
        this.pollingTimer = setInterval(async () => {
            try {
                const response = await fetch('/api/events/poll');
                const events = await response.json();
                
                events.forEach(event => this.handleMessage(event));
            } catch (error) {
                console.error('Polling error:', error);
            }
        }, this.options.pollingInterval);
    }
    
    // Stop polling
    stopPolling() {
        if (this.pollingTimer) {
            clearInterval(this.pollingTimer);
            this.pollingTimer = null;
        }
    }
    
    // Handle incoming message
    handleMessage(message) {
        const { type, data, channel = 'default' } = message;
        this.pubsub.publish(type, data, { channel });
    }
    
    // Send message (if WebSocket connected)
    send(message) {
        if (this.isConnected && this.websocket) {
            this.websocket.send(JSON.stringify(message));
        } else {
            console.warn('Cannot send message: not connected');
        }
    }
    
    // Subscribe to events
    subscribe(event, callback, options) {
        return this.pubsub.subscribe(event, callback, options);
    }
    
    // Publish local events
    publish(event, data, options) {
        return this.pubsub.publish(event, data, options);
    }
    
    // Disconnect
    disconnect() {
        if (this.websocket) {
            this.websocket.close();
        }
        this.stopPolling();
    }
}

// Usage Examples
const pubsub = new PubSubManager();

// Add logging middleware
pubsub.addMiddleware(async (eventData) => {
    console.log(`Event: ${eventData.event}`, eventData);
    return eventData;
});

// Subscribe to events
const unsubscribe1 = pubsub.subscribe('user:login', (data) => {
    console.log('User logged in:', data.data);
}, {
    channel: 'auth',
    priority: 10
});

const unsubscribe2 = pubsub.subscribe('user:*', (data) => {
    console.log('Any user event:', data);
}, {
    channel: 'auth',
    priority: 5
});

// Publish events
pubsub.publish('user:login', { userId: 123, name: 'John' }, { channel: 'auth' });

// Message queue example
const messageQueue = new MessageQueue({
    persistent: true,
    retryAttempts: 3
});

messageQueue.subscribe('email:send', async (data) => {
    console.log('Sending email:', data);
    // Simulate email sending
    await new Promise(resolve => setTimeout(resolve, 1000));
});

messageQueue.enqueue({
    type: 'email:send',
    data: {
        to: 'user@example.com',
        subject: 'Welcome!',
        body: 'Welcome to our platform!'
    }
}, 5); // High priority

// Real-time system
const realTimeSystem = new RealTimeEventSystem({
    websocketUrl: 'ws://localhost:8080/events',
    fallbackPolling: true
});

realTimeSystem.subscribe('notification:new', (data) => {
    console.log('New notification:', data.data);
});
```

---

## 2. Large-Scale Applications

> **Interview Explanation:** Large-scale applications require careful architecture planning to ensure maintainability, scalability, and performance. Understanding state management, component architecture, and modular design is crucial for building enterprise-level applications.

### 🎯 State Management Patterns

> **Interview Key Point:** State management becomes critical in large applications. Centralized state management helps maintain consistency, enables time-travel debugging, and makes the application more predictable.

#### **Advanced State Management Implementation**

```javascript
// Redux-like State Management
class StateManager {
    constructor(initialState = {}, options = {}) {
        this.state = initialState;
        this.listeners = new Set();
        this.middlewares = [];
        this.reducers = new Map();
        this.actionCreators = new Map();
        this.selectors = new Map();
        this.isDispatching = false;
        
        this.options = {
            enableDevTools: false,
            enableTimeTravel: false,
            maxHistorySize: 50,
            ...options
        };
        
        if (this.options.enableTimeTravel) {
            this.history = [{ ...initialState }];
            this.currentHistoryIndex = 0;
        }
        
        if (this.options.enableDevTools && typeof window !== 'undefined') {
            this.setupDevTools();
        }
    }
    
    // Register reducer
    registerReducer(name, reducer) {
        if (typeof reducer !== 'function') {
            throw new Error('Reducer must be a function');
        }
        
        this.reducers.set(name, reducer);
        
        // Initialize state slice if not exists
        if (!(name in this.state)) {
            this.state[name] = undefined;
        }
    }
    
    // Register action creator
    registerActionCreator(name, actionCreator) {
        if (typeof actionCreator !== 'function') {
            throw new Error('Action creator must be a function');
        }
        
        this.actionCreators.set(name, actionCreator);
    }
    
    // Register selector
    registerSelector(name, selector) {
        if (typeof selector !== 'function') {
            throw new Error('Selector must be a function');
        }
        
        this.selectors.set(name, selector);
    }
    
    // Add middleware
    addMiddleware(middleware) {
        if (typeof middleware !== 'function') {
            throw new Error('Middleware must be a function');
        }
        
        this.middlewares.push(middleware);
    }
    
    // Dispatch action
    dispatch(action) {
        if (this.isDispatching) {
            throw new Error('Cannot dispatch action while dispatching');
        }
        
        if (!action || typeof action.type !== 'string') {
            throw new Error('Action must be an object with a type property');
        }
        
        this.isDispatching = true;
        
        try {
            // Apply middlewares
            const dispatchWithMiddleware = this.applyMiddlewares(action);
            return dispatchWithMiddleware;
        } finally {
            this.isDispatching = false;
        }
    }
    
    // Apply middlewares to action
    applyMiddlewares(action) {
        let index = 0;
        
        const next = (actionToDispatch = action) => {
            if (index >= this.middlewares.length) {
                return this.executeDispatch(actionToDispatch);
            }
            
            const middleware = this.middlewares[index++];
            return middleware({
                getState: () => this.getState(),
                dispatch: (nextAction) => this.dispatch(nextAction)
            })(next)(actionToDispatch);
        };
        
        return next();
    }
    
    // Execute actual dispatch
    executeDispatch(action) {
        const previousState = { ...this.state };
        
        // Apply reducers
        this.reducers.forEach((reducer, name) => {
            const previousSliceState = this.state[name];
            const newSliceState = reducer(previousSliceState, action);
            
            if (newSliceState !== previousSliceState) {
                this.state[name] = newSliceState;
            }
        });
        
        // Add to history if time travel is enabled
        if (this.options.enableTimeTravel) {
            this.addToHistory();
        }
        
        // Notify listeners
        this.notifyListeners(action, previousState);
        
        // Update dev tools
        if (this.options.enableDevTools) {
            this.updateDevTools(action);
        }
        
        return action;
    }
    
    // Get current state
    getState() {
        return { ...this.state };
    }
    
    // Subscribe to state changes
    subscribe(listener) {
        if (typeof listener !== 'function') {
            throw new Error('Listener must be a function');
        }
        
        this.listeners.add(listener);
        
        // Return unsubscribe function
        return () => {
            this.listeners.delete(listener);
        };
    }
    
    // Notify all listeners
    notifyListeners(action, previousState) {
        this.listeners.forEach(listener => {
            try {
                listener(this.state, previousState, action);
            } catch (error) {
                console.error('Error in state listener:', error);
            }
        });
    }
    
    // Get selector result
    select(selectorName, ...args) {
        const selector = this.selectors.get(selectorName);
        if (!selector) {
            throw new Error(`Selector '${selectorName}' not found`);
        }
        
        return selector(this.state, ...args);
    }
    
    // Get action creator
    getActionCreator(name) {
        return this.actionCreators.get(name);
    }
    
    // Time travel methods
    addToHistory() {
        if (!this.options.enableTimeTravel) return;
        
        // Remove future history if we're not at the end
        if (this.currentHistoryIndex < this.history.length - 1) {
            this.history = this.history.slice(0, this.currentHistoryIndex + 1);
        }
        
        this.history.push({ ...this.state });
        this.currentHistoryIndex = this.history.length - 1;
        
        // Limit history size
        if (this.history.length > this.options.maxHistorySize) {
            this.history.shift();
            this.currentHistoryIndex--;
        }
    }
    
    // Undo last action
    undo() {
        if (!this.options.enableTimeTravel || this.currentHistoryIndex <= 0) {
            return false;
        }
        
        this.currentHistoryIndex--;
        this.state = { ...this.history[this.currentHistoryIndex] };
        this.notifyListeners({ type: '@@UNDO' }, this.state);
        return true;
    }
    
    // Redo last undone action
    redo() {
        if (!this.options.enableTimeTravel || 
            this.currentHistoryIndex >= this.history.length - 1) {
            return false;
        }
        
        this.currentHistoryIndex++;
        this.state = { ...this.history[this.currentHistoryIndex] };
        this.notifyListeners({ type: '@@REDO' }, this.state);
        return true;
    }
    
    // Get time travel state
    getTimeTravelState() {
        if (!this.options.enableTimeTravel) return null;
        
        return {
            history: this.history,
            currentIndex: this.currentHistoryIndex,
            canUndo: this.currentHistoryIndex > 0,
            canRedo: this.currentHistoryIndex < this.history.length - 1
        };
    }
    
    // Setup dev tools integration
    setupDevTools() {
        if (typeof window !== 'undefined' && window.__REDUX_DEVTOOLS_EXTENSION__) {
            this.devTools = window.__REDUX_DEVTOOLS_EXTENSION__.connect();
            this.devTools.init(this.state);
        }
    }
    
    updateDevTools(action) {
        if (this.devTools) {
            this.devTools.send(action, this.state);
        }
    }
    
    // Reset state
    reset(newState = {}) {
        this.state = { ...newState };
        
        if (this.options.enableTimeTravel) {
            this.history = [{ ...newState }];
            this.currentHistoryIndex = 0;
        }
        
        this.notifyListeners({ type: '@@RESET' }, {});
    }
}

// Async Action Middleware
const asyncMiddleware = ({ getState, dispatch }) => next => action => {
    if (typeof action === 'function') {
        return action(dispatch, getState);
    }
    
    return next(action);
};

// Logger Middleware
const loggerMiddleware = ({ getState }) => next => action => {
    console.group(`Action: ${action.type}`);
    console.log('Previous State:', getState());
    console.log('Action:', action);
    
    const result = next(action);
    
    console.log('Next State:', getState());
    console.groupEnd();
    
    return result;
};

// Error Handling Middleware
const errorMiddleware = ({ getState, dispatch }) => next => action => {
    try {
        return next(action);
    } catch (error) {
        console.error('Error in reducer:', error);
        
        // Dispatch error action
        dispatch({
            type: 'ERROR_OCCURRED',
            payload: {
                error: error.message,
                action,
                state: getState()
            }
        });
        
        throw error;
    }
};

// Usage Example
const stateManager = new StateManager({}, {
    enableTimeTravel: true,
    enableDevTools: true
});

// Add middlewares
stateManager.addMiddleware(asyncMiddleware);
stateManager.addMiddleware(loggerMiddleware);
stateManager.addMiddleware(errorMiddleware);

// Register reducers
stateManager.registerReducer('users', (state = [], action) => {
    switch (action.type) {
        case 'ADD_USER':
            return [...state, action.payload];
        case 'REMOVE_USER':
            return state.filter(user => user.id !== action.payload.id);
        case 'UPDATE_USER':
            return state.map(user => 
                user.id === action.payload.id 
                    ? { ...user, ...action.payload.updates }
                    : user
            );
        default:
            return state;
    }
});

stateManager.registerReducer('ui', (state = { loading: false, error: null }, action) => {
    switch (action.type) {
        case 'SET_LOADING':
            return { ...state, loading: action.payload };
        case 'SET_ERROR':
            return { ...state, error: action.payload };
        case 'CLEAR_ERROR':
            return { ...state, error: null };
        default:
            return state;
    }
});

// Register action creators
stateManager.registerActionCreator('addUser', (userData) => ({
    type: 'ADD_USER',
    payload: {
        id: Date.now(),
        ...userData,
        createdAt: new Date().toISOString()
    }
}));

stateManager.registerActionCreator('fetchUsers', () => {
    return async (dispatch, getState) => {
        dispatch({ type: 'SET_LOADING', payload: true });
        
        try {
            const response = await fetch('/api/users');
            const users = await response.json();
            
            dispatch({ type: 'SET_USERS', payload: users });
        } catch (error) {
            dispatch({ type: 'SET_ERROR', payload: error.message });
        } finally {
            dispatch({ type: 'SET_LOADING', payload: false });
        }
    };
});

// Register selectors
stateManager.registerSelector('getUserById', (state, userId) => {
    return state.users.find(user => user.id === userId);
});

stateManager.registerSelector('getActiveUsers', (state) => {
    return state.users.filter(user => user.active);
});

stateManager.registerSelector('getUserCount', (state) => {
    return state.users.length;
});

// Subscribe to changes
const unsubscribe = stateManager.subscribe((state, previousState, action) => {
    console.log('State changed:', { state, previousState, action });
});

// Dispatch actions
const addUserAction = stateManager.getActionCreator('addUser');
stateManager.dispatch(addUserAction({
    name: 'John Doe',
    email: 'john@example.com',
    active: true
}));

// Use selectors
const userCount = stateManager.select('getUserCount');
const activeUsers = stateManager.select('getActiveUsers');
const specificUser = stateManager.select('getUserById', 1);
```

### 🎯 Component Architecture

> **Interview Key Point:** Component architecture defines how UI components are structured, communicate, and manage their lifecycle. A well-designed component architecture promotes reusability, maintainability, and testability.

#### **Component System Implementation**

```javascript
// Base Component Class
class Component {
    constructor(element, options = {}) {
        this.element = typeof element === 'string' 
            ? document.querySelector(element) 
            : element;
            
        if (!this.element) {
            throw new Error('Element not found');
        }
        
        this.options = { ...this.defaultOptions, ...options };
        this.state = { ...this.defaultState };
        this.children = new Map();
        this.parent = null;
        this.eventListeners = new Map();
        this.destroyed = false;
        
        this.init();
    }
    
    // Default options (can be overridden)
    get defaultOptions() {
        return {};
    }
    
    // Default state (can be overridden)
    get defaultState() {
        return {};
    }
    
    // Initialize component
    init() {
        this.bindEvents();
        this.render();
        this.onMounted();
    }
    
    // Bind event listeners
    bindEvents() {
        // Override in subclasses
    }
    
    // Render component
    render() {
        // Override in subclasses
    }
    
    // Called after component is mounted
    onMounted() {
        // Override in subclasses
    }
    
    // Called before component is destroyed
    onBeforeDestroy() {
        // Override in subclasses
    }
    
    // Update component state
    setState(newState, callback) {
        if (this.destroyed) return;
        
        const previousState = { ...this.state };
        this.state = { ...this.state, ...newState };
        
        this.onStateChange(this.state, previousState);
        
        if (this.shouldUpdate(this.state, previousState)) {
            this.render();
        }
        
        if (callback && typeof callback === 'function') {
            callback(this.state, previousState);
        }
    }
    
    // Check if component should update
    shouldUpdate(newState, previousState) {
        return JSON.stringify(newState) !== JSON.stringify(previousState);
    }
    
    // Called when state changes
    onStateChange(newState, previousState) {
        // Override in subclasses
    }
    
    // Add child component
    addChild(name, component) {
        if (this.children.has(name)) {
            this.removeChild(name);
        }
        
        this.children.set(name, component);
        component.parent = this;
        
        return component;
    }
    
    // Remove child component
    removeChild(name) {
        const child = this.children.get(name);
        if (child) {
            child.destroy();
            this.children.delete(name);
        }
    }
    
    // Get child component
    getChild(name) {
        return this.children.get(name);
    }
    
    // Add event listener
    addEventListener(event, selector, handler) {
        const boundHandler = (e) => {
            const target = e.target.closest(selector);
            if (target && this.element.contains(target)) {
                handler.call(this, e, target);
            }
        };
        
        this.element.addEventListener(event, boundHandler);
        
        if (!this.eventListeners.has(event)) {
            this.eventListeners.set(event, []);
        }
        
        this.eventListeners.get(event).push({
            selector,
            handler,
            boundHandler
        });
    }
    
    // Remove event listener
    removeEventListener(event, selector, handler) {
        const listeners = this.eventListeners.get(event);
        if (!listeners) return;
        
        const index = listeners.findIndex(listener => 
            listener.selector === selector && listener.handler === handler
        );
        
        if (index !== -1) {
            const listener = listeners[index];
            this.element.removeEventListener(event, listener.boundHandler);
            listeners.splice(index, 1);
        }
    }
    
    // Emit custom event
    emit(eventName, detail = null) {
        const event = new CustomEvent(eventName, {
            detail,
            bubbles: true,
            cancelable: true
        });
        
        this.element.dispatchEvent(event);
        return event;
    }
    
    // Listen to custom events
    on(eventName, handler) {
        this.element.addEventListener(eventName, handler);
    }
    
    // Remove custom event listener
    off(eventName, handler) {
        this.element.removeEventListener(eventName, handler);
    }
    
    // Find elements within component
    $(selector) {
        return this.element.querySelector(selector);
    }
    
    $$(selector) {
        return Array.from(this.element.querySelectorAll(selector));
    }
    
    // Destroy component
    destroy() {
        if (this.destroyed) return;
        
        this.onBeforeDestroy();
        
        // Destroy all children
        this.children.forEach(child => child.destroy());
        this.children.clear();
        
        // Remove all event listeners
        this.eventListeners.forEach((listeners, event) => {
            listeners.forEach(listener => {
                this.element.removeEventListener(event, listener.boundHandler);
            });
        });
        this.eventListeners.clear();
        
        // Remove from parent
        if (this.parent) {
            this.parent.children.forEach((child, name) => {
                if (child === this) {
                    this.parent.children.delete(name);
                }
            });
        }
        
        this.destroyed = true;
    }
}

// Modal Component Example
class Modal extends Component {
    get defaultOptions() {
        return {
            closable: true,
            backdrop: true,
            keyboard: true,
            animation: true,
            size: 'medium'
        };
    }
    
    get defaultState() {
        return {
            visible: false,
            loading: false
        };
    }
    
    bindEvents() {
        if (this.options.closable) {
            this.addEventListener('click', '.modal-close', this.hide);
        }
        
        if (this.options.backdrop) {
            this.addEventListener('click', '.modal-backdrop', this.hide);
        }
        
        if (this.options.keyboard) {
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.state.visible) {
                    this.hide();
                }
            });
        }
    }
    
    render() {
        const { visible, loading } = this.state;
        const { size, animation } = this.options;
        
        this.element.className = `modal ${size} ${animation ? 'animated' : ''} ${visible ? 'visible' : 'hidden'}`;
        
        if (!this.rendered) {
            this.element.innerHTML = `
                <div class="modal-backdrop"></div>
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title">${this.options.title || ''}</h3>
                        ${this.options.closable ? '<button class="modal-close">&times;</button>' : ''}
                    </div>
                    <div class="modal-body">
                        ${loading ? '<div class="loading">Loading...</div>' : this.options.content || ''}
                    </div>
                    <div class="modal-footer">
                        ${this.options.footer || ''}
                    </div>
                </div>
            `;
            this.rendered = true;
        }
        
        // Update content if not loading
        if (!loading && this.options.content) {
            const body = this.$('.modal-body');
            if (body) {
                body.innerHTML = this.options.content;
            }
        }
    }
    
    show() {
        this.setState({ visible: true });
        this.emit('modal:show');
        
        // Focus management
        if (this.state.visible) {
            this.element.focus();
        }
    }
    
    hide() {
        this.setState({ visible: false });
        this.emit('modal:hide');
    }
    
    setContent(content) {
        this.options.content = content;
        this.setState({ loading: false });
    }
    
    setLoading(loading = true) {
        this.setState({ loading });
    }
}

// Data Table Component
class DataTable extends Component {
    get defaultOptions() {
        return {
            columns: [],
            data: [],
            sortable: true,
            filterable: true,
            paginated: true,
            pageSize: 10,
            selectable: false,
            expandable: false
        };
    }
    
    get defaultState() {
        return {
            currentPage: 1,
            sortColumn: null,
            sortDirection: 'asc',
            filterText: '',
            selectedRows: new Set(),
            expandedRows: new Set()
        };
    }
    
    bindEvents() {
        if (this.options.sortable) {
            this.addEventListener('click', '.sortable', this.handleSort);
        }
        
        if (this.options.filterable) {
            this.addEventListener('input', '.filter-input', this.handleFilter);
        }
        
        if (this.options.paginated) {
            this.addEventListener('click', '.pagination button', this.handlePagination);
        }
        
        if (this.options.selectable) {
            this.addEventListener('change', '.row-select', this.handleRowSelect);
            this.addEventListener('change', '.select-all', this.handleSelectAll);
        }
        
        if (this.options.expandable) {
            this.addEventListener('click', '.expand-toggle', this.handleRowExpand);
        }
    }
    
    render() {
        const filteredData = this.getFilteredData();
        const sortedData = this.getSortedData(filteredData);
        const paginatedData = this.getPaginatedData(sortedData);
        
        this.element.innerHTML = `
            ${this.options.filterable ? this.renderFilter() : ''}
            <table class="data-table">
                ${this.renderHeader()}
                ${this.renderBody(paginatedData)}
            </table>
            ${this.options.paginated ? this.renderPagination(sortedData.length) : ''}
        `;
    }
    
    renderFilter() {
        return `
            <div class="table-filter">
                <input type="text" 
                       class="filter-input" 
                       placeholder="Filter table..." 
                       value="${this.state.filterText}">
            </div>
        `;
    }
    
    renderHeader() {
        return `
            <thead>
                <tr>
                    ${this.options.selectable ? '<th><input type="checkbox" class="select-all"></th>' : ''}
                    ${this.options.expandable ? '<th></th>' : ''}
                    ${this.options.columns.map(column => `
                        <th class="${this.options.sortable && column.sortable !== false ? 'sortable' : ''}" 
                            data-column="${column.key}">
                            ${column.title}
                            ${this.renderSortIcon(column.key)}
                        </th>
                    `).join('')}
                </tr>
            </thead>
        `;
    }
    
    renderBody(data) {
        return `
            <tbody>
                ${data.map((row, index) => `
                    <tr data-row="${index}" class="${this.state.selectedRows.has(index) ? 'selected' : ''}">
                        ${this.options.selectable ? `
                            <td><input type="checkbox" class="row-select" data-index="${index}" ${this.state.selectedRows.has(index) ? 'checked' : ''}></td>
                        ` : ''}
                        ${this.options.expandable ? `
                            <td><button class="expand-toggle" data-index="${index}">${this.state.expandedRows.has(index) ? '−' : '+'}</button></td>
                        ` : ''}
                        ${this.options.columns.map(column => `
                            <td data-column="${column.key}">
                                ${this.renderCell(row, column)}
                            </td>
                        `).join('')}
                    </tr>
                    ${this.options.expandable && this.state.expandedRows.has(index) ? `
                        <tr class="expanded-row">
                            <td colspan="${this.getColumnCount()}">
                                ${this.renderExpandedContent(row)}
                            </td>
                        </tr>
                    ` : ''}
                `).join('')}
            </tbody>
        `;
    }
    
    renderCell(row, column) {
        const value = this.getCellValue(row, column.key);
        
        if (column.render) {
            return column.render(value, row);
        }
        
        if (column.type === 'date') {
            return new Date(value).toLocaleDateString();
        }
        
        if (column.type === 'currency') {
            return new Intl.NumberFormat('en-US', {
                style: 'currency',
                currency: 'USD'
            }).format(value);
        }
        
        return value;
    }
    
    renderSortIcon(columnKey) {
        if (this.state.sortColumn !== columnKey) {
            return '<span class="sort-icon">⇅</span>';
        }
        
        return this.state.sortDirection === 'asc' 
            ? '<span class="sort-icon">↑</span>' 
            : '<span class="sort-icon">↓</span>';
    }
    
    renderPagination(totalItems) {
        const totalPages = Math.ceil(totalItems / this.options.pageSize);
        const currentPage = this.state.currentPage;
        
        return `
            <div class="pagination">
                <button ${currentPage === 1 ? 'disabled' : ''} data-page="${currentPage - 1}">Previous</button>
                ${Array.from({ length: totalPages }, (_, i) => i + 1).map(page => `
                    <button class="${page === currentPage ? 'active' : ''}" data-page="${page}">${page}</button>
                `).join('')}
                <button ${currentPage === totalPages ? 'disabled' : ''} data-page="${currentPage + 1}">Next</button>
            </div>
        `;
    }
    
    renderExpandedContent(row) {
        if (this.options.expandedRowRender) {
            return this.options.expandedRowRender(row);
        }
        
        return `<pre>${JSON.stringify(row, null, 2)}</pre>`;
    }
    
    // Event handlers
    handleSort(e, target) {
        const column = target.dataset.column;
        const newDirection = this.state.sortColumn === column && this.state.sortDirection === 'asc' 
            ? 'desc' 
            : 'asc';
        
        this.setState({
            sortColumn: column,
            sortDirection: newDirection
        });
        
        this.emit('table:sort', { column, direction: newDirection });
    }
    
    handleFilter(e, target) {
        this.setState({
            filterText: target.value,
            currentPage: 1
        });
        
        this.emit('table:filter', { text: target.value });
    }
    
    handlePagination(e, target) {
        const page = parseInt(target.dataset.page);
        if (!isNaN(page)) {
            this.setState({ currentPage: page });
            this.emit('table:page', { page });
        }
    }
    
    handleRowSelect(e, target) {
        const index = parseInt(target.dataset.index);
        const selected = new Set(this.state.selectedRows);
        
        if (target.checked) {
            selected.add(index);
        } else {
            selected.delete(index);
        }
        
        this.setState({ selectedRows: selected });
        this.emit('table:select', { selectedRows: Array.from(selected) });
    }
    
    handleSelectAll(e, target) {
        const selected = new Set();
        
        if (target.checked) {
            this.getFilteredData().forEach((_, index) => selected.add(index));
        }
        
        this.setState({ selectedRows: selected });
        this.emit('table:selectAll', { selected: target.checked });
    }
    
    handleRowExpand(e, target) {
        const index = parseInt(target.dataset.index);
        const expanded = new Set(this.state.expandedRows);
        
        if (expanded.has(index)) {
            expanded.delete(index);
        } else {
            expanded.add(index);
        }
        
        this.setState({ expandedRows: expanded });
        this.emit('table:expand', { index, expanded: expanded.has(index) });
    }
    
    // Data manipulation methods
    getFilteredData() {
        if (!this.state.filterText) {
            return this.options.data;
        }
        
        const filterText = this.state.filterText.toLowerCase();
        
        return this.options.data.filter(row => {
            return this.options.columns.some(column => {
                const value = this.getCellValue(row, column.key);
                return String(value).toLowerCase().includes(filterText);
            });
        });
    }
    
    getSortedData(data) {
        if (!this.state.sortColumn) {
            return data;
        }
        
        return [...data].sort((a, b) => {
            const aValue = this.getCellValue(a, this.state.sortColumn);
            const bValue = this.getCellValue(b, this.state.sortColumn);
            
            let comparison = 0;
            
            if (aValue < bValue) comparison = -1;
            if (aValue > bValue) comparison = 1;
            
            return this.state.sortDirection === 'desc' ? -comparison : comparison;
        });
    }
    
    getPaginatedData(data) {
        if (!this.options.paginated) {
            return data;
        }
        
        const start = (this.state.currentPage - 1) * this.options.pageSize;
        const end = start + this.options.pageSize;
        
        return data.slice(start, end);
    }
    
    getCellValue(row, key) {
        return key.split('.').reduce((obj, k) => obj && obj[k], row);
    }
    
    getColumnCount() {
        let count = this.options.columns.length;
        if (this.options.selectable) count++;
        if (this.options.expandable) count++;
        return count;
    }
    
    // Public API methods
    setData(data) {
        this.options.data = data;
        this.setState({ currentPage: 1 });
    }
    
    addRow(row) {
        this.options.data.push(row);
        this.render();
    }
    
    removeRow(index) {
        this.options.data.splice(index, 1);
        this.render();
    }
    
    getSelectedRows() {
        return Array.from(this.state.selectedRows).map(index => this.options.data[index]);
    }
    
    clearSelection() {
        this.setState({ selectedRows: new Set() });
    }
}

// Usage Examples
const modal = new Modal('#myModal', {
    title: 'User Profile',
    content: '<p>Loading user data...</p>',
    closable: true,
    backdrop: true,
    size: 'large'
});

modal.show();

// Data table example
const table = new DataTable('#myTable', {
    columns: [
        { key: 'id', title: 'ID', sortable: true },
        { key: 'name', title: 'Name', sortable: true },
        { key: 'email', title: 'Email', sortable: true },
        { 
            key: 'salary', 
            title: 'Salary', 
            type: 'currency',
            sortable: true 
        },
        {
            key: 'actions',
            title: 'Actions',
            render: (value, row) => `
                <button onclick="editUser(${row.id})">Edit</button>
                <button onclick="deleteUser(${row.id})">Delete</button>
            `
        }
    ],
    data: [
        { id: 1, name: 'John Doe', email: 'john@example.com', salary: 50000 },
        { id: 2, name: 'Jane Smith', email: 'jane@example.com', salary: 60000 }
    ],
    sortable: true,
    filterable: true,
    paginated: true,
    selectable: true,
    expandable: true
});

table.on('table:select', (e) => {
    console.log('Selected rows:', e.detail.selectedRows);
});
```

### 🎯 Micro-frontends Architecture

> **Interview Key Point:** Micro-frontends extend microservice principles to frontend development, allowing teams to work independently on different parts of the application while maintaining a cohesive user experience.

#### **Micro-frontend Implementation**

```javascript
// Micro-frontend Registry
class MicrofrontendRegistry {
    constructor() {
        this.applications = new Map();
        this.containers = new Map();
        this.eventBus = new EventTarget();
        this.loadingPromises = new Map();
        this.sharedDependencies = new Map();
    }
    
    // Register a micro-frontend application
    register(name, config) {
        if (this.applications.has(name)) {
            console.warn(`Application ${name} is already registered`);
            return;
        }
        
        const appConfig = {
            name,
            entry: config.entry,
            container: config.container,
            activeWhen: config.activeWhen,
            props: config.props || {},
            lifecycle: {
                mount: config.mount,
                unmount: config.unmount,
                update: config.update
            },
            assets: {
                js: config.assets?.js || [],
                css: config.assets?.css || []
            },
            dependencies: config.dependencies || [],
            isolated: config.isolated !== false,
            ...config
        };
        
        this.applications.set(name, appConfig);
        this.emit('app:registered', { name, config: appConfig });
    }
    
    // Unregister application
    unregister(name) {
        if (this.applications.has(name)) {
            this.unmount(name);
            this.applications.delete(name);
            this.emit('app:unregistered', { name });
        }
    }
    
    // Load and mount application
    async mount(name, container, props = {}) {
        const app = this.applications.get(name);
        if (!app) {
            throw new Error(`Application ${name} not found`);
        }
        
        try {
            this.emit('app:mounting', { name });
            
            // Load dependencies first
            await this.loadDependencies(app.dependencies);
            
            // Load application assets
            const appInstance = await this.loadApplication(app);
            
            // Prepare container
            const containerElement = this.prepareContainer(container, app);
            
            // Mount application
            const mountedApp = await this.mountApplication(appInstance, containerElement, {
                ...app.props,
                ...props
            });
            
            // Store mounted application
            this.containers.set(name, {
                app: mountedApp,
                container: containerElement,
                instance: appInstance
            });
            
            this.emit('app:mounted', { name, container: containerElement });
            
            return mountedApp;
            
        } catch (error) {
            this.emit('app:mount-error', { name, error });
            throw error;
        }
    }
    
    // Unmount application
    async unmount(name) {
        const mounted = this.containers.get(name);
        if (!mounted) {
            return;
        }
        
        try {
            this.emit('app:unmounting', { name });
            
            // Call unmount lifecycle
            if (mounted.instance.unmount) {
                await mounted.instance.unmount(mounted.app);
            }
            
            // Clean up container
            if (mounted.container) {
                mounted.container.innerHTML = '';
            }
            
            this.containers.delete(name);
            this.emit('app:unmounted', { name });
            
        } catch (error) {
            this.emit('app:unmount-error', { name, error });
            throw error;
        }
    }
    
    // Update application props
    async update(name, props) {
        const mounted = this.containers.get(name);
        if (!mounted) {
            throw new Error(`Application ${name} is not mounted`);
        }
        
        try {
            if (mounted.instance.update) {
                await mounted.instance.update(mounted.app, props);
            }
            
            this.emit('app:updated', { name, props });
            
        } catch (error) {
            this.emit('app:update-error', { name, error });
            throw error;
        }
    }
    
    // Load application module
    async loadApplication(app) {
        const cacheKey = `${app.name}:${app.entry}`;
        
        if (this.loadingPromises.has(cacheKey)) {
            return this.loadingPromises.get(cacheKey);
        }
        
        const loadPromise = this._loadApplicationModule(app);
        this.loadingPromises.set(cacheKey, loadPromise);
        
        try {
            const result = await loadPromise;
            return result;
        } catch (error) {
            this.loadingPromises.delete(cacheKey);
            throw error;
        }
    }
    
    async _loadApplicationModule(app) {
        if (app.isolated) {
            // Load in isolated context (iframe or web components)
            return this.loadIsolatedApplication(app);
        } else {
            // Load in shared context
            return this.loadSharedApplication(app);
        }
    }
    
    // Load application in shared context
    async loadSharedApplication(app) {
        // Load CSS assets
        await Promise.all(app.assets.css.map(css => this.loadCSS(css)));
        
        // Load JS assets
        await Promise.all(app.assets.js.map(js => this.loadScript(js)));
        
        // Load main entry
        const module = await this.loadModule(app.entry);
        
        return {
            mount: module.mount || app.lifecycle.mount,
            unmount: module.unmount || app.lifecycle.unmount,
            update: module.update || app.lifecycle.update
        };
    }
    
    // Load application in isolated context
    async loadIsolatedApplication(app) {
        const iframe = document.createElement('iframe');
        iframe.style.width = '100%';
        iframe.style.height = '100%';
        iframe.style.border = 'none';
        
        return new Promise((resolve, reject) => {
            iframe.onload = () => {
                try {
                    const iframeWindow = iframe.contentWindow;
                    const iframeDocument = iframe.contentDocument;
                    
                    // Setup communication bridge
                    const bridge = this.setupIframeBridge(iframe, app);
                    
                    // Load application in iframe
                    this.loadApplicationInIframe(iframeDocument, app)
                        .then(() => {
                            resolve({
                                mount: (container, props) => {
                                    container.appendChild(iframe);
                                    return bridge.mount(props);
                                },
                                unmount: () => {
                                    return bridge.unmount();
                                },
                                update: (props) => {
                                    return bridge.update(props);
                                }
                            });
                        })
                        .catch(reject);
                        
                } catch (error) {
                    reject(error);
                }
            };
            
            iframe.onerror = reject;
            iframe.src = 'about:blank';
        });
    }
    
    // Setup iframe communication bridge
    setupIframeBridge(iframe, app) {
        const messageCallbacks = new Map();
        let messageId = 0;
        
        const sendMessage = (type, data) => {
            return new Promise((resolve, reject) => {
                const id = ++messageId;
                messageCallbacks.set(id, { resolve, reject });
                
                iframe.contentWindow.postMessage({
                    id,
                    type,
                    data
                }, '*');
                
                // Timeout after 10 seconds
                setTimeout(() => {
                    if (messageCallbacks.has(id)) {
                        messageCallbacks.delete(id);
                        reject(new Error('Message timeout'));
                    }
                }, 10000);
            });
        };
        
        // Listen for responses
        window.addEventListener('message', (event) => {
            if (event.source !== iframe.contentWindow) return;
            
            const { id, type, data, error } = event.data;
            const callback = messageCallbacks.get(id);
            
            if (callback) {
                messageCallbacks.delete(id);
                if (error) {
                    callback.reject(new Error(error));
                } else {
                    callback.resolve(data);
                }
            }
        });
        
        return {
            mount: (props) => sendMessage('mount', props),
            unmount: () => sendMessage('unmount'),
            update: (props) => sendMessage('update', props)
        };
    }
    
    // Load dependencies
    async loadDependencies(dependencies) {
        const loadPromises = dependencies.map(dep => {
            if (typeof dep === 'string') {
                return this.loadSharedDependency(dep);
            } else {
                return this.loadSharedDependency(dep.name, dep.version, dep.url);
            }
        });
        
        await Promise.all(loadPromises);
    }
    
    // Load shared dependency
    async loadSharedDependency(name, version = 'latest', url = null) {
        const key = `${name}@${version}`;
        
        if (this.sharedDependencies.has(key)) {
            return this.sharedDependencies.get(key);
        }
        
        const dependencyUrl = url || this.resolveDependencyUrl(name, version);
        const dependency = await this.loadModule(dependencyUrl);
        
        this.sharedDependencies.set(key, dependency);
        return dependency;
    }
    
    // Resolve dependency URL
    resolveDependencyUrl(name, version) {
        // This could integrate with a CDN or package registry
        return `https://unpkg.com/${name}@${version}/dist/index.js`;
    }
    
    // Prepare container element
    prepareContainer(container, app) {
        const containerElement = typeof container === 'string'
            ? document.querySelector(container)
            : container;
            
        if (!containerElement) {
            throw new Error(`Container not found: ${container}`);
        }
        
        // Add application-specific classes
        containerElement.classList.add('microfrontend-container');
        containerElement.classList.add(`app-${app.name}`);
        
        // Set up isolation if needed
        if (app.isolated) {
            containerElement.style.isolation = 'isolate';
        }
        
        return containerElement;
    }
    
    // Mount application instance
    async mountApplication(instance, container, props) {
        if (!instance.mount) {
            throw new Error('Application must provide a mount function');
        }
        
        return await instance.mount(container, props);
    }
    
    // Utility methods for loading assets
    async loadScript(src) {
        return new Promise((resolve, reject) => {
            const script = document.createElement('script');
            script.src = src;
            script.onload = resolve;
            script.onerror = reject;
            document.head.appendChild(script);
        });
    }
    
    async loadCSS(href) {
        return new Promise((resolve, reject) => {
            const link = document.createElement('link');
            link.rel = 'stylesheet';
            link.href = href;
            link.onload = resolve;
            link.onerror = reject;
            document.head.appendChild(link);
        });
    }
    
    async loadModule(url) {
        if (url.endsWith('.js')) {
            // Dynamic import
            return await import(url);
        } else {
            // System.js or other module loader
            return await System.import(url);
        }
    }
    
    // Event system
    emit(event, data) {
        this.eventBus.dispatchEvent(new CustomEvent(event, { detail: data }));
    }
    
    on(event, handler) {
        this.eventBus.addEventListener(event, handler);
    }
    
    off(event, handler) {
        this.eventBus.removeEventListener(event, handler);
    }
    
    // Get application status
    getStatus(name) {
        const app = this.applications.get(name);
        const mounted = this.containers.get(name);
        
        return {
            registered: !!app,
            mounted: !!mounted,
            config: app
        };
    }
    
    // List all applications
    list() {
        return Array.from(this.applications.keys());
    }
    
    // Get mounted applications
    getMounted() {
        return Array.from(this.containers.keys());
    }
}

// Usage Example
const registry = new MicrofrontendRegistry();

// Register applications
registry.register('header', {
    entry: './header/index.js',
    mount: (container, props) => {
        // Mount header application
    },
    unmount: (app) => {
        // Cleanup header
    },
    assets: {
        css: ['./header/styles.css'],
        js: ['./header/bundle.js']
    },
    dependencies: ['react@17', 'react-dom@17']
});

registry.register('sidebar', {
    entry: './sidebar/index.js',
    isolated: true, // Load in iframe
    mount: (container, props) => {
        // Mount sidebar
    }
});

// Mount applications
await registry.mount('header', '#header-container', {
    user: { name: 'John Doe' },
    theme: 'dark'
});

await registry.mount('sidebar', '#sidebar-container');
```

---

## 3. Code Quality & Maintainability

> **Interview Explanation:** Code quality and maintainability are essential for long-term project success. This includes implementing SOLID principles, clean code practices, comprehensive error handling, and robust testing strategies.

### 🎯 SOLID Principles Implementation

> **Interview Key Point:** SOLID principles help create maintainable, flexible, and extensible code. Understanding and applying these principles is crucial for building scalable applications.

#### **SOLID Principles in JavaScript**

```javascript
// S - Single Responsibility Principle
// Each class should have only one reason to change

// ❌ Bad: Multiple responsibilities
class UserManager {
    constructor() {
        this.users = [];
    }
    
    addUser(user) {
        // Validation logic
        if (!user.email || !user.name) {
            throw new Error('Invalid user data');
        }
        
        // Database logic
        this.users.push(user);
        
        // Email logic
        this.sendWelcomeEmail(user);
        
        // Logging logic
        console.log(`User ${user.name} added`);
    }
    
    sendWelcomeEmail(user) {
        // Email sending logic
    }
}

// ✅ Good: Single responsibilities
class UserValidator {
    validate(user) {
        if (!user.email || !user.name) {
            throw new Error('Invalid user data');
        }
        return true;
    }
}

class UserRepository {
    constructor() {
        this.users = [];
    }
    
    save(user) {
        this.users.push(user);
        return user;
    }
    
    findById(id) {
        return this.users.find(user => user.id === id);
    }
}

class EmailService {
    sendWelcomeEmail(user) {
        console.log(`Sending welcome email to ${user.email}`);
        // Email sending logic
    }
}

class Logger {
    log(message) {
        console.log(`[${new Date().toISOString()}] ${message}`);
    }
}

class UserService {
    constructor(validator, repository, emailService, logger) {
        this.validator = validator;
        this.repository = repository;
        this.emailService = emailService;
        this.logger = logger;
    }
    
    addUser(user) {
        this.validator.validate(user);
        const savedUser = this.repository.save(user);
        this.emailService.sendWelcomeEmail(savedUser);
        this.logger.log(`User ${savedUser.name} added`);
        return savedUser;
    }
}

// O - Open/Closed Principle
// Open for extension, closed for modification

// Base shape class
class Shape {
    area() {
        throw new Error('Area method must be implemented');
    }
}

class Circle extends Shape {
    constructor(radius) {
        super();
        this.radius = radius;
    }
    
    area() {
        return Math.PI * this.radius * this.radius;
    }
}

class Rectangle extends Shape {
    constructor(width, height) {
        super();
        this.width = width;
        this.height = height;
    }
    
    area() {
        return this.width * this.height;
    }
}

class Triangle extends Shape {
    constructor(base, height) {
        super();
        this.base = base;
        this.height = height;
    }
    
    area() {
        return 0.5 * this.base * this.height;
    }
}

// Area calculator that works with any shape
class AreaCalculator {
    calculateTotalArea(shapes) {
        return shapes.reduce((total, shape) => total + shape.area(), 0);
    }
}

// L - Liskov Substitution Principle
// Derived classes must be substitutable for their base classes

// ❌ Bad: Violates LSP
class Bird {
    fly() {
        console.log('Flying...');
    }
}

class Penguin extends Bird {
    fly() {
        throw new Error('Penguins cannot fly');
    }
}

// ✅ Good: Follows LSP
class Animal {
    move() {
        console.log('Moving...');
    }
}

class FlyingBird extends Animal {
    move() {
        this.fly();
    }
    
    fly() {
        console.log('Flying...');
    }
}

class SwimmingBird extends Animal {
    move() {
        this.swim();
    }
    
    swim() {
        console.log('Swimming...');
    }
}

// I - Interface Segregation Principle
// Clients should not be forced to depend on interfaces they don't use

// ❌ Bad: Fat interface
class AllInOneDevice {
    print() { /* implementation */ }
    scan() { /* implementation */ }
    fax() { /* implementation */ }
    copy() { /* implementation */ }
}

// ✅ Good: Segregated interfaces
class Printer {
    print(document) {
        console.log('Printing document');
    }
}

class Scanner {
    scan(document) {
        console.log('Scanning document');
        return 'scanned-data';
    }
}

class FaxMachine {
    sendFax(document, number) {
        console.log(`Sending fax to ${number}`);
    }
}

// Compose devices as needed
class MultiFunctionPrinter {
    constructor(printer, scanner, faxMachine) {
        this.printer = printer;
        this.scanner = scanner;
        this.faxMachine = faxMachine;
    }
    
    print(document) {
        return this.printer.print(document);
    }
    
    scan(document) {
        return this.scanner.scan(document);
    }
    
    sendFax(document, number) {
        return this.faxMachine.sendFax(document, number);
    }
}

// D - Dependency Inversion Principle
// Depend on abstractions, not concretions

// ❌ Bad: High-level module depends on low-level module
class EmailNotification {
    send(message) {
        console.log(`Email: ${message}`);
    }
}

class OrderService {
    constructor() {
        this.emailNotification = new EmailNotification(); // Direct dependency
    }
    
    processOrder(order) {
        // Process order logic
        this.emailNotification.send('Order processed');
    }
}

// ✅ Good: Depend on abstraction
class NotificationInterface {
    send(message) {
        throw new Error('Send method must be implemented');
    }
}

class EmailNotificationService extends NotificationInterface {
    send(message) {
        console.log(`Email: ${message}`);
    }
}

class SMSNotificationService extends NotificationInterface {
    send(message) {
        console.log(`SMS: ${message}`);
    }
}

class PushNotificationService extends NotificationInterface {
    send(message) {
        console.log(`Push: ${message}`);
    }
}

class ImprovedOrderService {
    constructor(notificationService) {
        this.notificationService = notificationService; // Dependency injection
    }
    
    processOrder(order) {
        // Process order logic
        this.notificationService.send('Order processed');
    }
}

// Usage with dependency injection
const emailService = new EmailNotificationService();
const orderService = new ImprovedOrderService(emailService);
```

### 🎯 Error Handling Strategies

> **Interview Key Point:** Robust error handling prevents application crashes, provides meaningful feedback to users, and helps with debugging. Understanding different error handling patterns is essential for production applications.

#### **Comprehensive Error Handling Implementation**

```javascript
// Custom Error Classes
class AppError extends Error {
    constructor(message, statusCode = 500, isOperational = true) {
        super(message);
        this.name = this.constructor.name;
        this.statusCode = statusCode;
        this.isOperational = isOperational;
        this.timestamp = new Date().toISOString();
        
        Error.captureStackTrace(this, this.constructor);
    }
}

class ValidationError extends AppError {
    constructor(message, field = null) {
        super(message, 400);
        this.field = field;
        this.type = 'validation';
    }
}

class NotFoundError extends AppError {
    constructor(resource = 'Resource') {
        super(`${resource} not found`, 404);
        this.type = 'not_found';
    }
}

class UnauthorizedError extends AppError {
    constructor(message = 'Unauthorized access') {
        super(message, 401);
        this.type = 'unauthorized';
    }
}

class NetworkError extends AppError {
    constructor(message = 'Network error occurred', originalError = null) {
        super(message, 503);
        this.type = 'network';
        this.originalError = originalError;
    }
}

// Error Handler Class
class ErrorHandler {
    constructor(options = {}) {
        this.options = {
            logErrors: true,
            showStackTrace: false,
            notifyExternal: false,
            ...options
        };
        
        this.errorCallbacks = new Map();
        this.globalErrorHandler = this.globalErrorHandler.bind(this);
        this.unhandledRejectionHandler = this.unhandledRejectionHandler.bind(this);
        
        this.setupGlobalHandlers();
    }
    
    setupGlobalHandlers() {
        if (typeof window !== 'undefined') {
            window.addEventListener('error', this.globalErrorHandler);
            window.addEventListener('unhandledrejection', this.unhandledRejectionHandler);
        }
        
        if (typeof process !== 'undefined') {
            process.on('uncaughtException', this.globalErrorHandler);
            process.on('unhandledRejection', this.unhandledRejectionHandler);
        }
    }
    
    globalErrorHandler(event) {
        const error = event.error || event;
        this.handleError(error, 'global');
    }
    
    unhandledRejectionHandler(event) {
        const error = event.reason;
        this.handleError(error, 'unhandled_promise');
    }
    
    handleError(error, context = 'application') {
        const errorInfo = this.normalizeError(error);
        
        // Log error
        if (this.options.logErrors) {
            this.logError(errorInfo, context);
        }
        
        // Execute registered callbacks
        this.executeErrorCallbacks(errorInfo, context);
        
        // Notify external services
        if (this.options.notifyExternal) {
            this.notifyExternalService(errorInfo, context);
        }
        
        return errorInfo;
    }
    
    normalizeError(error) {
        if (error instanceof AppError) {
            return {
                name: error.name,
                message: error.message,
                statusCode: error.statusCode,
                isOperational: error.isOperational,
                timestamp: error.timestamp,
                stack: error.stack,
                type: error.type || 'application',
                field: error.field,
                originalError: error.originalError
            };
        }
        
        if (error instanceof Error) {
            return {
                name: error.name,
                message: error.message,
                stack: error.stack,
                statusCode: 500,
                isOperational: false,
                timestamp: new Date().toISOString(),
                type: 'system'
            };
        }
        
        // Handle non-Error objects
        return {
            name: 'UnknownError',
            message: String(error),
            statusCode: 500,
            isOperational: false,
            timestamp: new Date().toISOString(),
            type: 'unknown'
        };
    }
    
    logError(errorInfo, context) {
        const logData = {
            context,
            error: {
                name: errorInfo.name,
                message: errorInfo.message,
                statusCode: errorInfo.statusCode,
                type: errorInfo.type,
                timestamp: errorInfo.timestamp
            }
        };
        
        if (this.options.showStackTrace && errorInfo.stack) {
            logData.error.stack = errorInfo.stack;
        }
        
        if (errorInfo.isOperational) {
            console.warn('Operational Error:', logData);
        } else {
            console.error('System Error:', logData);
        }
    }
    
    executeErrorCallbacks(errorInfo, context) {
        const callbacks = this.errorCallbacks.get(errorInfo.type) || [];
        
        callbacks.forEach(callback => {
            try {
                callback(errorInfo, context);
            } catch (callbackError) {
                console.error('Error in error callback:', callbackError);
            }
        });
    }
    
    onError(errorType, callback) {
        if (!this.errorCallbacks.has(errorType)) {
            this.errorCallbacks.set(errorType, []);
        }
        
        this.errorCallbacks.get(errorType).push(callback);
        
        // Return unsubscribe function
        return () => {
            const callbacks = this.errorCallbacks.get(errorType);
            const index = callbacks.indexOf(callback);
            if (index !== -1) {
                callbacks.splice(index, 1);
            }
        };
    }
    
    async notifyExternalService(errorInfo, context) {
        try {
            // This could integrate with services like Sentry, Rollbar, etc.
            await fetch('/api/errors', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    error: errorInfo,
                    context,
                    userAgent: navigator.userAgent,
                    url: window.location.href,
                    userId: this.getCurrentUserId()
                })
            });
        } catch (notificationError) {
            console.error('Failed to notify external service:', notificationError);
        }
    }
    
    getCurrentUserId() {
        // Implementation depends on your auth system
        return localStorage.getItem('userId') || 'anonymous';
    }
    
    // Async error wrapper
    async wrapAsync(asyncFunction, context = 'async') {
        try {
            return await asyncFunction();
        } catch (error) {
            throw this.handleError(error, context);
        }
    }
    
    // Promise error handler
    handlePromise(promise, context = 'promise') {
        return promise.catch(error => {
            this.handleError(error, context);
            throw error;
        });
    }
    
    destroy() {
        if (typeof window !== 'undefined') {
            window.removeEventListener('error', this.globalErrorHandler);
            window.removeEventListener('unhandledrejection', this.unhandledRejectionHandler);
        }
        
        if (typeof process !== 'undefined') {
            process.removeListener('uncaughtException', this.globalErrorHandler);
            process.removeListener('unhandledRejection', this.unhandledRejectionHandler);
        }
    }
}

// Retry Mechanism
class RetryHandler {
    constructor(options = {}) {
        this.options = {
            maxRetries: 3,
            baseDelay: 1000,
            maxDelay: 10000,
            backoffMultiplier: 2,
            jitter: true,
            retryCondition: this.defaultRetryCondition,
            ...options
        };
    }
    
    defaultRetryCondition(error, attempt) {
        // Retry on network errors, timeouts, and 5xx status codes
        return (
            error instanceof NetworkError ||
            error.statusCode >= 500 ||
            error.code === 'TIMEOUT'
        ) && attempt < this.options.maxRetries;
    }
    
    async execute(operation, context = {}) {
        let lastError;
        
        for (let attempt = 0; attempt <= this.options.maxRetries; attempt++) {
            try {
                const result = await operation();
                
                if (attempt > 0) {
                    console.log(`Operation succeeded on attempt ${attempt + 1}`);
                }
                
                return result;
                
            } catch (error) {
                lastError = error;
                
                if (!this.options.retryCondition(error, attempt)) {
                    throw error;
                }
                
                if (attempt < this.options.maxRetries) {
                    const delay = this.calculateDelay(attempt);
                    console.warn(`Operation failed, retrying in ${delay}ms (attempt ${attempt + 1}/${this.options.maxRetries})`);
                    await this.delay(delay);
                }
            }
        }
        
        throw new AppError(
            `Operation failed after ${this.options.maxRetries} retries: ${lastError.message}`,
            lastError.statusCode || 500
        );
    }
    
    calculateDelay(attempt) {
        let delay = this.options.baseDelay * Math.pow(this.options.backoffMultiplier, attempt);
        delay = Math.min(delay, this.options.maxDelay);
        
        if (this.options.jitter) {
            delay = delay * (0.5 + Math.random() * 0.5);
        }
        
        return Math.round(delay);
    }
    
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Circuit Breaker Pattern
class CircuitBreaker {
    constructor(operation, options = {}) {
        this.operation = operation;
        this.options = {
            failureThreshold: 5,
            recoveryTimeout: 30000,
            monitoringPeriod: 60000,
            ...options
        };
        
        this.state = 'CLOSED'; // CLOSED, OPEN, HALF_OPEN
        this.failureCount = 0;
        this.lastFailureTime = null;
        this.nextAttemptTime = null;
        
        this.setupMonitoring();
    }
    
    async execute(...args) {
        if (this.state === 'OPEN') {
            if (Date.now() < this.nextAttemptTime) {
                throw new AppError('Circuit breaker is OPEN', 503);
            } else {
                this.state = 'HALF_OPEN';
                console.log('Circuit breaker entering HALF_OPEN state');
            }
        }
        
        try {
            const result = await this.operation(...args);
            this.onSuccess();
            return result;
            
        } catch (error) {
            this.onFailure();
            throw error;
        }
    }
    
    onSuccess() {
        this.failureCount = 0;
        
        if (this.state === 'HALF_OPEN') {
            this.state = 'CLOSED';
            console.log('Circuit breaker entering CLOSED state');
        }
    }
    
    onFailure() {
        this.failureCount++;
        this.lastFailureTime = Date.now();
        
        if (this.failureCount >= this.options.failureThreshold) {
            this.state = 'OPEN';
            this.nextAttemptTime = Date.now() + this.options.recoveryTimeout;
            console.log('Circuit breaker entering OPEN state');
        }
    }
    
    setupMonitoring() {
        setInterval(() => {
            console.log(`Circuit Breaker Status: ${this.state}, Failures: ${this.failureCount}`);
        }, this.options.monitoringPeriod);
    }
    
    getStatus() {
        return {
            state: this.state,
            failureCount: this.failureCount,
            lastFailureTime: this.lastFailureTime,
            nextAttemptTime: this.nextAttemptTime
        };
    }
    
    reset() {
        this.state = 'CLOSED';
        this.failureCount = 0;
        this.lastFailureTime = null;
        this.nextAttemptTime = null;
    }
}

// Usage Examples
const errorHandler = new ErrorHandler({
    logErrors: true,
    showStackTrace: true,
    notifyExternal: true
});

// Register error callbacks
errorHandler.onError('validation', (error, context) => {
    // Show user-friendly validation message
    console.log('Validation error occurred:', error.message);
});

errorHandler.onError('network', (error, context) => {
    // Show network error notification
    console.log('Network issue detected:', error.message);
});

// Retry handler
const retryHandler = new RetryHandler({
    maxRetries: 3,
    baseDelay: 1000
});

// Circuit breaker for API calls
const apiCall = async (url) => {
    const response = await fetch(url);
    if (!response.ok) {
        throw new NetworkError(`API call failed: ${response.status}`);
    }
    return response.json();
};

const circuitBreaker = new CircuitBreaker(apiCall, {
    failureThreshold: 3,
    recoveryTimeout: 10000
});

// Combined usage
async function robustApiCall(url) {
    try {
        return await retryHandler.execute(async () => {
            return await circuitBreaker.execute(url);
        });
    } catch (error) {
        errorHandler.handleError(error, 'api_call');
        throw error;
    }
}
```

### 🎯 Testing Strategies

> **Interview Key Point:** Testing ensures code quality, prevents regressions, and provides confidence when making changes. Understanding different testing strategies and implementing them effectively is crucial for maintainable applications.

#### **Comprehensive Testing Implementation**

```javascript
// Test Framework Foundation
class TestRunner {
    constructor() {
        this.suites = [];
        this.currentSuite = null;
        this.stats = {
            passed: 0,
            failed: 0,
            skipped: 0,
            total: 0
        };
        this.hooks = {
            beforeAll: [],
            afterAll: [],
            beforeEach: [],
            afterEach: []
        };
    }
    
    describe(name, callback) {
        const suite = {
            name,
            tests: [],
            hooks: {
                beforeAll: [],
                afterAll: [],
                beforeEach: [],
                afterEach: []
            },
            stats: {
                passed: 0,
                failed: 0,
                skipped: 0,
                total: 0
            }
        };
        
        this.suites.push(suite);
        this.currentSuite = suite;
        callback();
        this.currentSuite = null;
    }
    
    it(name, callback, options = {}) {
        if (!this.currentSuite) {
            throw new Error('Tests must be defined within a describe block');
        }
        
        const test = {
            name,
            callback,
            skip: options.skip || false,
            only: options.only || false,
            timeout: options.timeout || 5000
        };
        
        this.currentSuite.tests.push(test);
    }
    
    beforeAll(callback) {
        if (this.currentSuite) {
            this.currentSuite.hooks.beforeAll.push(callback);
        } else {
            this.hooks.beforeAll.push(callback);
        }
    }
    
    afterAll(callback) {
        if (this.currentSuite) {
            this.currentSuite.hooks.afterAll.push(callback);
        } else {
            this.hooks.afterAll.push(callback);
        }
    }
    
    beforeEach(callback) {
        if (this.currentSuite) {
            this.currentSuite.hooks.beforeEach.push(callback);
        } else {
            this.hooks.beforeEach.push(callback);
        }
    }
    
    afterEach(callback) {
        if (this.currentSuite) {
            this.currentSuite.hooks.afterEach.push(callback);
        } else {
            this.hooks.afterEach.push(callback);
        }
    }
    
    async run() {
        console.log('🧪 Running tests...\n');
        
        // Run global beforeAll hooks
        await this.runHooks(this.hooks.beforeAll);
        
        for (const suite of this.suites) {
            await this.runSuite(suite);
        }
        
        // Run global afterAll hooks
        await this.runHooks(this.hooks.afterAll);
        
        this.printResults();
    }
    
    async runSuite(suite) {
        console.log(`📦 ${suite.name}`);
        
        // Run suite beforeAll hooks
        await this.runHooks(suite.hooks.beforeAll);
        
        for (const test of suite.tests) {
            if (test.skip) {
                suite.stats.skipped++;
                this.stats.skipped++;
                console.log(`  ⏭️  ${test.name} (skipped)`);
                continue;
            }
            
            suite.stats.total++;
            this.stats.total++;
            
            try {
                // Run beforeEach hooks
                await this.runHooks([...this.hooks.beforeEach, ...suite.hooks.beforeEach]);
                
                // Run test with timeout
                await this.runWithTimeout(test.callback, test.timeout);
                
                suite.stats.passed++;
                this.stats.passed++;
                console.log(`  ✅ ${test.name}`);
                
            } catch (error) {
                suite.stats.failed++;
                this.stats.failed++;
                console.log(`  ❌ ${test.name}`);
                console.log(`     ${error.message}`);
                
                if (error.stack) {
                    console.log(`     ${error.stack.split('\n')[1]?.trim()}`);
                }
            } finally {
                // Run afterEach hooks
                await this.runHooks([...this.hooks.afterEach, ...suite.hooks.afterEach]);
            }
        }
        
        // Run suite afterAll hooks
        await this.runHooks(suite.hooks.afterAll);
        
        console.log(`  📊 ${suite.stats.passed} passed, ${suite.stats.failed} failed, ${suite.stats.skipped} skipped\n`);
    }
    
    async runHooks(hooks) {
        for (const hook of hooks) {
            await hook();
        }
    }
    
    async runWithTimeout(callback, timeout) {
        return new Promise((resolve, reject) => {
            const timer = setTimeout(() => {
                reject(new Error(`Test timed out after ${timeout}ms`));
            }, timeout);
            
            Promise.resolve(callback())
                .then(resolve)
                .catch(reject)
                .finally(() => clearTimeout(timer));
        });
    }
    
    printResults() {
        console.log('📈 Test Results:');
        console.log(`  Total: ${this.stats.total}`);
        console.log(`  ✅ Passed: ${this.stats.passed}`);
        console.log(`  ❌ Failed: ${this.stats.failed}`);
        console.log(`  ⏭️  Skipped: ${this.stats.skipped}`);
        
        if (this.stats.failed > 0) {
            console.log('\n❌ Tests failed!');
            process.exit && process.exit(1);
        } else {
            console.log('\n✅ All tests passed!');
        }
    }
}

// Assertion Library
class Assertions {
    constructor(actual) {
        this.actual = actual;
    }
    
    toBe(expected) {
        if (this.actual !== expected) {
            throw new Error(`Expected ${JSON.stringify(expected)}, but got ${JSON.stringify(this.actual)}`);
        }
        return this;
    }
    
    toEqual(expected) {
        if (!this.deepEqual(this.actual, expected)) {
            throw new Error(`Expected ${JSON.stringify(expected)}, but got ${JSON.stringify(this.actual)}`);
        }
        return this;
    }
    
    toBeNull() {
        if (this.actual !== null) {
            throw new Error(`Expected null, but got ${JSON.stringify(this.actual)}`);
        }
        return this;
    }
    
    toBeUndefined() {
        if (this.actual !== undefined) {
            throw new Error(`Expected undefined, but got ${JSON.stringify(this.actual)}`);
        }
        return this;
    }
    
    toBeTruthy() {
        if (!this.actual) {
            throw new Error(`Expected truthy value, but got ${JSON.stringify(this.actual)}`);
        }
        return this;
    }
    
    toBeFalsy() {
        if (this.actual) {
            throw new Error(`Expected falsy value, but got ${JSON.stringify(this.actual)}`);
        }
        return this;
    }
    
    toContain(expected) {
        if (Array.isArray(this.actual)) {
            if (!this.actual.includes(expected)) {
                throw new Error(`Expected array to contain ${JSON.stringify(expected)}`);
            }
        } else if (typeof this.actual === 'string') {
            if (!this.actual.includes(expected)) {
                throw new Error(`Expected string to contain "${expected}"`);
            }
        } else {
            throw new Error('toContain can only be used with arrays or strings');
        }
        return this;
    }
    
    toThrow(expectedError) {
        if (typeof this.actual !== 'function') {
            throw new Error('toThrow can only be used with functions');
        }
        
        let didThrow = false;
        let thrownError;
        
        try {
            this.actual();
        } catch (error) {
            didThrow = true;
            thrownError = error;
        }
        
        if (!didThrow) {
            throw new Error('Expected function to throw an error');
        }
        
        if (expectedError && thrownError.message !== expectedError) {
            throw new Error(`Expected error message "${expectedError}", but got "${thrownError.message}"`);
        }
        
        return this;
    }
    
    async toReject(expectedError) {
        if (typeof this.actual !== 'function' && !this.actual?.then) {
            throw new Error('toReject can only be used with functions or promises');
        }
        
        let didReject = false;
        let rejectionReason;
        
        try {
            if (typeof this.actual === 'function') {
                await this.actual();
            } else {
                await this.actual;
            }
        } catch (error) {
            didReject = true;
            rejectionReason = error;
        }
        
        if (!didReject) {
            throw new Error('Expected promise to reject');
        }
        
        if (expectedError && rejectionReason.message !== expectedError) {
            throw new Error(`Expected rejection message "${expectedError}", but got "${rejectionReason.message}"`);
        }
        
        return this;
    }
    
    deepEqual(a, b) {
        if (a === b) return true;
        
        if (a == null || b == null) return a === b;
        
        if (typeof a !== typeof b) return false;
        
        if (typeof a === 'object') {
            if (Array.isArray(a) !== Array.isArray(b)) return false;
            
            const keysA = Object.keys(a);
            const keysB = Object.keys(b);
            
            if (keysA.length !== keysB.length) return false;
            
            for (const key of keysA) {
                if (!keysB.includes(key)) return false;
                if (!this.deepEqual(a[key], b[key])) return false;
            }
            
            return true;
        }
        
        return false;
    }
}

// Mock System
class MockFunction {
    constructor(implementation) {
        this.implementation = implementation || (() => {});
        this.calls = [];
        this.results = [];
        
        const mockFn = (...args) => {
            this.calls.push({
                args,
                timestamp: Date.now()
            });
            
            try {
                const result = this.implementation(...args);
                this.results.push({ type: 'return', value: result });
                return result;
            } catch (error) {
                this.results.push({ type: 'throw', value: error });
                throw error;
            }
        };
        
        // Add mock methods
        mockFn.mockImplementation = (impl) => {
            this.implementation = impl;
            return mockFn;
        };
        
        mockFn.mockReturnValue = (value) => {
            this.implementation = () => value;
            return mockFn;
        };
        
        mockFn.mockResolvedValue = (value) => {
            this.implementation = () => Promise.resolve(value);
            return mockFn;
        };
        
        mockFn.mockRejectedValue = (error) => {
            this.implementation = () => Promise.reject(error);
            return mockFn;
        };
        
        mockFn.mockClear = () => {
            this.calls = [];
            this.results = [];
            return mockFn;
        };
        
        mockFn.mockReset = () => {
            this.calls = [];
            this.results = [];
            this.implementation = () => {};
            return mockFn;
        };
        
        // Getters for call information
        Object.defineProperty(mockFn, 'mock', {
            get: () => ({
                calls: this.calls,
                results: this.results,
                instances: []
            })
        });
        
        return mockFn;
    }
}

// Global test functions
const testRunner = new TestRunner();

function describe(name, callback) {
    return testRunner.describe(name, callback);
}

function it(name, callback, options) {
    return testRunner.it(name, callback, options);
}

function expect(actual) {
    return new Assertions(actual);
}

function jest() {
    return {
        fn: (implementation) => new MockFunction(implementation)
    };
}

function beforeAll(callback) {
    return testRunner.beforeAll(callback);
}

function afterAll(callback) {
    return testRunner.afterAll(callback);
}

function beforeEach(callback) {
    return testRunner.beforeEach(callback);
}

function afterEach(callback) {
    return testRunner.afterEach(callback);
}

// Example Usage
describe('User Service', () => {
    let userService;
    let mockRepository;
    let mockEmailService;
    
    beforeEach(() => {
        mockRepository = {
            save: jest().fn(),
            findById: jest().fn()
        };
        
        mockEmailService = {
            sendWelcomeEmail: jest().fn()
        };
        
        userService = new UserService(
            new UserValidator(),
            mockRepository,
            mockEmailService,
            new Logger()
        );
    });
    
    describe('addUser', () => {
        it('should add a valid user successfully', () => {
            const userData = { name: 'John Doe', email: 'john@example.com' };
            const savedUser = { id: 1, ...userData };
            
            mockRepository.save.mockReturnValue(savedUser);
            
            const result = userService.addUser(userData);
            
            expect(result).toEqual(savedUser);
            expect(mockRepository.save).toHaveBeenCalledWith(userData);
            expect(mockEmailService.sendWelcomeEmail).toHaveBeenCalledWith(savedUser);
        });
        
        it('should throw error for invalid user data', () => {
            const invalidUser = { name: 'John' }; // Missing email
            
            expect(() => userService.addUser(invalidUser)).toThrow('Invalid user data');
        });
    });
    
    describe('async operations', () => {
        it('should handle async user creation', async () => {
            const userData = { name: 'Jane Doe', email: 'jane@example.com' };
            
            mockRepository.save.mockResolvedValue({ id: 2, ...userData });
            
            const result = await userService.addUserAsync(userData);
            
            expect(result.id).toBe(2);
        });
        
        it('should handle async errors', async () => {
            const userData = { name: 'Jane Doe', email: 'jane@example.com' };
            
            mockRepository.save.mockRejectedValue(new Error('Database error'));
            
            await expect(() => userService.addUserAsync(userData)).toReject('Database error');
        });
    });
});

// Run tests
testRunner.run();
```

---

## 🎯 Summary

This comprehensive guide covers essential system design and architecture patterns for JavaScript applications:

**Design Patterns:**

- ✅ Singleton Pattern with dependency injection
- ✅ Observer Pattern with typed events
- ✅ Factory Pattern for UI components
- ✅ Module Pattern with ES6 modules
- ✅ Publish-Subscribe with advanced messaging

**Large-Scale Applications:**

- ✅ State Management with Redux-like implementation
- ✅ Component Architecture with lifecycle management
- ✅ Micro-frontends with isolation and communication

**Code Quality:**

- ✅ SOLID Principles implementation
- ✅ Comprehensive error handling strategies
- ✅ Testing frameworks with mocking and assertions

These patterns provide the foundation for building maintainable, scalable, and robust JavaScript applications that can handle enterprise-level requirements while maintaining code quality and developer productivity.

---

*This completes the System Design & Architecture guide. Each pattern includes practical implementations with modern JavaScript features, error handling, and real-world usage examples.*
