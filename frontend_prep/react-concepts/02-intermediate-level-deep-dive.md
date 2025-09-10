# 🎯 React Intermediate Level - Interview Deep Dive

> **Master intermediate React concepts where most interviews dig deep. These patterns separate junior from mid-level developers.**

---

## 📋 Table of Contents

1. [Conditional Rendering Patterns](#conditional-rendering-patterns)
2. [Lists & Keys Mastery](#lists--keys-mastery)
3. [Context API vs Prop Drilling](#context-api-vs-prop-drilling)
4. [Error Boundaries](#error-boundaries)
5. [Portals](#portals)
6. [Refs & Forwarding Refs](#refs--forwarding-refs)
7. [Fragments & StrictMode](#fragments--strictmode)

---

## Conditional Rendering Patterns

> **Interview Expectation:** Show mastery of different rendering patterns and when to use each approach. Understanding these patterns demonstrates React composition skills.

### 🎯 Ternary Operator - The Classic Choice

**Interview Critical Point:** Ternary operators are perfect for simple true/false rendering but can become unreadable when nested.

```jsx
// Simple conditional rendering
function UserProfile({ user, isLoading }) {
  return (
    <div>
      {isLoading ? (
        <div className="spinner">Loading...</div>
      ) : (
        <div className="profile">
          <h1>{user.name}</h1>
          <p>{user.email}</p>
        </div>
      )}
    </div>
  );
}

// Nested ternary (can become hard to read)
function UserStatus({ user, isLoading, error }) {
  return (
    <div>
      {isLoading ? (
        <div>Loading...</div>
      ) : error ? (
        <div className="error">Error: {error.message}</div>
      ) : user ? (
        <div className="profile">{user.name}</div>
      ) : (
        <div>No user found</div>
      )}
    </div>
  );
}

// Better approach for complex conditions
function UserStatus({ user, isLoading, error }) {
  if (isLoading) return <div>Loading...</div>;
  if (error) return <div className="error">Error: {error.message}</div>;
  if (!user) return <div>No user found</div>;
  
  return (
    <div className="profile">
      <h1>{user.name}</h1>
      <p>{user.email}</p>
    </div>
  );
}
```

### 🎯 Short-Circuit Evaluation - The Performance Pattern

**Interview Critical Point:** Short-circuit evaluation is efficient but can cause issues with falsy values. Understanding when it fails is crucial.

```jsx
// Basic short-circuit rendering
function NotificationBell({ notifications }) {
  return (
    <div className="bell">
      🔔
      {notifications.length > 0 && (
        <span className="badge">{notifications.length}</span>
      )}
    </div>
  );
}

// ❌ Dangerous short-circuit - renders 0 instead of nothing
function BadExample({ items }) {
  return (
    <div>
      {items.length && <ItemList items={items} />}
      {/* If items.length is 0, it renders 0 on screen! */}
    </div>
  );
}

// ✅ Safe short-circuit patterns
function SafeExample({ items, showItems }) {
  return (
    <div>
      {/* Method 1: Convert to boolean */}
      {!!items.length && <ItemList items={items} />}
      
      {/* Method 2: Explicit comparison */}
      {items.length > 0 && <ItemList items={items} />}
      
      {/* Method 3: Use boolean variable */}
      {showItems && <ItemList items={items} />}
    </div>
  );
}

// Advanced short-circuit with multiple conditions
function Dashboard({ user, permissions, isOnline }) {
  return (
    <div className="dashboard">
      <h1>Dashboard</h1>
      
      {/* Multiple conditions */}
      {user && permissions.canViewReports && (
        <ReportsSection />
      )}
      
      {/* Complex condition extraction */}
      {user && permissions.canManageUsers && isOnline && (
        <UserManagement />
      )}
      
      {/* Offline indicator */}
      {!isOnline && (
        <div className="offline-warning">
          You're currently offline. Some features may be unavailable.
        </div>
      )}
    </div>
  );
}
```

### 🎯 Render Props Pattern - The Flexible Approach

**Interview Critical Point:** Render props provide flexibility by letting components control what they render while sharing logic.

```jsx
// Data fetcher with render props
function DataFetcher({ url, render, renderLoading, renderError }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch');
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [url]);
  
  if (loading) return renderLoading ? renderLoading() : <div>Loading...</div>;
  if (error) return renderError ? renderError(error) : <div>Error occurred</div>;
  
  return render(data);
}

// Usage of render props
function UserList() {
  return (
    <DataFetcher
      url="/api/users"
      render={(users) => (
        <div>
          <h2>Users ({users.length})</h2>
          {users.map(user => (
            <div key={user.id} className="user-card">
              {user.name}
            </div>
          ))}
        </div>
      )}
      renderLoading={() => (
        <div className="loading-spinner">
          <div className="spinner"></div>
          <p>Fetching users...</p>
        </div>
      )}
      renderError={(error) => (
        <div className="error-container">
          <h3>Failed to load users</h3>
          <p>{error.message}</p>
          <button onClick={() => window.location.reload()}>
            Retry
          </button>
        </div>
      )}
    />
  );
}

// Mouse position tracker with render props
function MouseTracker({ render, children }) {
  const [position, setPosition] = useState({ x: 0, y: 0 });
  
  useEffect(() => {
    const handleMouseMove = (e) => {
      setPosition({ x: e.clientX, y: e.clientY });
    };
    
    document.addEventListener('mousemove', handleMouseMove);
    return () => document.removeEventListener('mousemove', handleMouseMove);
  }, []);
  
  // Support both render prop and children function
  return render ? render(position) : children(position);
}

// Usage examples
function App() {
  return (
    <div>
      {/* Render prop approach */}
      <MouseTracker
        render={({ x, y }) => (
          <div>Mouse is at ({x}, {y})</div>
        )}
      />
      
      {/* Children function approach */}
      <MouseTracker>
        {({ x, y }) => (
          <div 
            style={{
              position: 'absolute',
              left: x,
              top: y,
              width: 10,
              height: 10,
              backgroundColor: 'red',
              borderRadius: '50%'
            }}
          />
        )}
      </MouseTracker>
    </div>
  );
}
```

### 🎯 Higher-Order Components (HOC) - The Composition Pattern

**Interview Critical Point:** HOCs are functions that take a component and return a new component with additional props or behavior.

```jsx
// Authentication HOC
function withAuth(WrappedComponent) {
  return function AuthenticatedComponent(props) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
      const checkAuth = async () => {
        try {
          const userData = await getCurrentUser();
          setUser(userData);
        } catch (error) {
          console.error('Authentication failed:', error);
        } finally {
          setLoading(false);
        }
      };
      
      checkAuth();
    }, []);
    
    if (loading) {
      return <div className="auth-loading">Checking authentication...</div>;
    }
    
    if (!user) {
      return <LoginForm onLogin={setUser} />;
    }
    
    // Pass through all props plus user
    return <WrappedComponent {...props} user={user} />;
  };
}

// Usage
const ProtectedDashboard = withAuth(Dashboard);
const ProtectedProfile = withAuth(UserProfile);

// Loading HOC
function withLoading(WrappedComponent) {
  return function LoadingComponent({ isLoading, loadingMessage, ...props }) {
    if (isLoading) {
      return (
        <div className="loading-container">
          <div className="spinner" />
          <p>{loadingMessage || 'Loading...'}</p>
        </div>
      );
    }
    
    return <WrappedComponent {...props} />;
  };
}

// Error boundary HOC
function withErrorBoundary(WrappedComponent, fallbackComponent) {
  return class extends React.Component {
    constructor(props) {
      super(props);
      this.state = { hasError: false, error: null };
    }
    
    static getDerivedStateFromError(error) {
      return { hasError: true, error };
    }
    
    componentDidCatch(error, errorInfo) {
      console.error('Error caught by HOC:', error, errorInfo);
    }
    
    render() {
      if (this.state.hasError) {
        const FallbackComponent = fallbackComponent || DefaultErrorFallback;
        return <FallbackComponent error={this.state.error} />;
      }
      
      return <WrappedComponent {...this.props} />;
    }
  };
}

// Compose multiple HOCs
const EnhancedComponent = withErrorBoundary(
  withAuth(
    withLoading(Dashboard)
  )
);

// Modern alternative: Custom hooks (preferred approach)
function useAuth() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    getCurrentUser()
      .then(setUser)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);
  
  return { user, loading };
}

function ModernProtectedComponent() {
  const { user, loading } = useAuth();
  
  if (loading) return <div>Loading...</div>;
  if (!user) return <LoginForm />;
  
  return <Dashboard user={user} />;
}
```

---

## Lists & Keys Mastery

> **Interview Expectation:** Deep understanding of React's reconciliation algorithm and why keys are crucial for performance and correctness.

### 🎯 Why Keys Are Essential

**Interview Critical Point:** Keys help React identify which items have changed, been added, or removed. Without proper keys, React may update the wrong elements or recreate elements unnecessarily.

```jsx
// ❌ Without keys - React can't track items efficiently
function BadTodoList({ todos }) {
  return (
    <ul>
      {todos.map((todo) => (
        <li>  {/* No key - React warning */}
          <input type="checkbox" checked={todo.completed} />
          <span>{todo.text}</span>
          <button>Delete</button>
        </li>
      ))}
    </ul>
  );
}

// ✅ With proper keys - React can efficiently update
function GoodTodoList({ todos, onToggle, onDelete }) {
  return (
    <ul>
      {todos.map((todo) => (
        <li key={todo.id}>  {/* Unique, stable key */}
          <input 
            type="checkbox" 
            checked={todo.completed}
            onChange={() => onToggle(todo.id)}
          />
          <span style={{ 
            textDecoration: todo.completed ? 'line-through' : 'none' 
          }}>
            {todo.text}
          </span>
          <button onClick={() => onDelete(todo.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
}

// Demonstrating the key problem
function KeyProblemDemo() {
  const [items, setItems] = useState([
    { id: 1, name: 'Apple', selected: false },
    { id: 2, name: 'Banana', selected: false },
    { id: 3, name: 'Cherry', selected: false }
  ]);
  
  const removeFirst = () => {
    setItems(items.slice(1));
  };
  
  const toggleSelected = (id) => {
    setItems(items.map(item =>
      item.id === id ? { ...item, selected: !item.selected } : item
    ));
  };
  
  return (
    <div>
      <button onClick={removeFirst}>Remove First Item</button>
      
      {/* ❌ Using index as key - causes issues */}
      <div>
        <h3>Bad: Using Index as Key</h3>
        {items.map((item, index) => (
          <div key={index}>  {/* Index as key - problematic */}
            <input 
              type="checkbox"
              checked={item.selected}
              onChange={() => toggleSelected(item.id)}
            />
            <span>{item.name}</span>
          </div>
        ))}
      </div>
      
      {/* ✅ Using stable unique key */}
      <div>
        <h3>Good: Using Stable Unique Key</h3>
        {items.map((item) => (
          <div key={item.id}>  {/* Stable unique key */}
            <input 
              type="checkbox"
              checked={item.selected}
              onChange={() => toggleSelected(item.id)}
            />
            <span>{item.name}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 🎯 Index as Key Problem

**Interview Critical Point:** Using array index as key can cause rendering bugs when the list order changes.

```jsx
// Demonstrating why index keys are problematic
function ContactList() {
  const [contacts, setContacts] = useState([
    { id: 1, name: 'Alice', email: 'alice@example.com' },
    { id: 2, name: 'Bob', email: 'bob@example.com' },
    { id: 3, name: 'Charlie', email: 'charlie@example.com' }
  ]);
  
  const [inputValues, setInputValues] = useState({});
  
  const updateInput = (id, value) => {
    setInputValues(prev => ({ ...prev, [id]: value }));
  };
  
  const removeContact = (idToRemove) => {
    setContacts(contacts.filter(contact => contact.id !== idToRemove));
  };
  
  const addContact = () => {
    const newContact = {
      id: Date.now(),
      name: 'New Contact',
      email: 'new@example.com'
    };
    setContacts([newContact, ...contacts]); // Add to beginning
  };
  
  return (
    <div>
      <button onClick={addContact}>Add Contact to Top</button>
      
      {/* ❌ Index as key - input values get mixed up */}
      <div>
        <h3>Problematic: Index as Key</h3>
        {contacts.map((contact, index) => (
          <div key={index} style={{ border: '1px solid #ccc', margin: '5px', padding: '10px' }}>
            <div>{contact.name} - {contact.email}</div>
            <input 
              type="text"
              placeholder="Add a note..."
              value={inputValues[`${index}-note`] || ''}
              onChange={(e) => updateInput(`${index}-note`, e.target.value)}
            />
            <button onClick={() => removeContact(contact.id)}>Remove</button>
          </div>
        ))}
      </div>
      
      {/* ✅ Proper key - input values stay with correct items */}
      <div>
        <h3>Correct: Unique ID as Key</h3>
        {contacts.map((contact) => (
          <div key={contact.id} style={{ border: '1px solid #ccc', margin: '5px', padding: '10px' }}>
            <div>{contact.name} - {contact.email}</div>
            <input 
              type="text"
              placeholder="Add a note..."
              value={inputValues[`${contact.id}-note`] || ''}
              onChange={(e) => updateInput(`${contact.id}-note`, e.target.value)}
            />
            <button onClick={() => removeContact(contact.id)}>Remove</button>
          </div>
        ))}
      </div>
    </div>
  );
}
```

### 🎯 When Index Keys Are Acceptable

**Interview Key Point:** Index keys are okay when the list is static, doesn't reorder, and items don't have local state.

```jsx
// ✅ Index keys are fine here - static list, no reordering
function StaticMenu({ menuItems }) {
  return (
    <nav>
      <ul>
        {menuItems.map((item, index) => (
          <li key={index}>  {/* OK: static list, no state */}
            <a href={item.href}>{item.label}</a>
          </li>
        ))}
      </ul>
    </nav>
  );
}

// ✅ Index keys acceptable - read-only display
function ReadOnlyList({ items }) {
  return (
    <ul>
      {items.map((item, index) => (
        <li key={index}>  {/* OK: no interaction, no reordering */}
          {item}
        </li>
      ))}
    </ul>
  );
}

// ❌ Index keys problematic - dynamic list with interactions
function SearchResults({ results, onSelect }) {
  return (
    <div>
      {results.map((result, index) => (
        <div 
          key={index}  // BAD: search results can change order
          onClick={() => onSelect(result)}
          className="search-result"
        >
          {result.title}
        </div>
      ))}
    </div>
  );
}

// ✅ Better approach for search results
function BetterSearchResults({ results, onSelect }) {
  return (
    <div>
      {results.map((result) => (
        <div 
          key={result.id || result.title}  // Unique identifier
          onClick={() => onSelect(result)}
          className="search-result"
        >
          {result.title}
        </div>
      ))}
    </div>
  );
}
```

---

## Context API vs Prop Drilling

> **Interview Expectation:** Understand when to use Context vs props, and demonstrate proper Context API usage patterns.

### 🎯 The Prop Drilling Problem

**Interview Critical Point:** Prop drilling happens when you pass props through multiple component levels just to reach a deeply nested component.

```jsx
// ❌ Prop drilling example - props passed through multiple levels
function App() {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  const [language, setLanguage] = useState('en');
  
  return (
    <Layout 
      user={user} 
      theme={theme} 
      language={language}
      onThemeChange={setTheme}
      onLanguageChange={setLanguage}
    />
  );
}

function Layout({ user, theme, language, onThemeChange, onLanguageChange }) {
  return (
    <div className={`layout layout--${theme}`}>
      <Header 
        user={user} 
        theme={theme} 
        language={language}
        onThemeChange={onThemeChange}
      />
      <Sidebar 
        user={user} 
        theme={theme} 
        language={language}
      />
      <MainContent 
        theme={theme} 
        language={language}
        onLanguageChange={onLanguageChange}
      />
    </div>
  );
}

function Header({ user, theme, onThemeChange }) {
  return (
    <header className={`header header--${theme}`}>
      <Navigation user={user} theme={theme} />
      <UserMenu user={user} theme={theme} onThemeChange={onThemeChange} />
    </header>
  );
}

function UserMenu({ user, theme, onThemeChange }) {
  // Finally using the props at the leaf component
  return (
    <div className={`user-menu user-menu--${theme}`}>
      {user && <span>Welcome, {user.name}</span>}
      <button onClick={() => onThemeChange(theme === 'light' ? 'dark' : 'light')}>
        Toggle Theme
      </button>
    </div>
  );
}
```

### 🎯 Context API Solution

**Interview Critical Point:** Context provides a way to share values between components without explicitly passing props through every level.

```jsx
// ✅ Context API solution
import React, { createContext, useContext, useState } from 'react';

// Create contexts
const UserContext = createContext();
const ThemeContext = createContext();
const LanguageContext = createContext();

// Custom hooks for consuming contexts (best practice)
function useUser() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
}

function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}

function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within a LanguageProvider');
  }
  return context;
}

// Provider components
function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  
  const login = async (credentials) => {
    try {
      const userData = await authenticateUser(credentials);
      setUser(userData);
    } catch (error) {
      console.error('Login failed:', error);
    }
  };
  
  const logout = () => {
    setUser(null);
  };
  
  return (
    <UserContext.Provider value={{ user, login, logout }}>
      {children}
    </UserContext.Provider>
  );
}

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  
  const toggleTheme = () => {
    setTheme(prev => prev === 'light' ? 'dark' : 'light');
  };
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

function LanguageProvider({ children }) {
  const [language, setLanguage] = useState('en');
  
  const changeLanguage = (newLang) => {
    setLanguage(newLang);
  };
  
  return (
    <LanguageContext.Provider value={{ language, changeLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
}

// App with providers
function App() {
  return (
    <UserProvider>
      <ThemeProvider>
        <LanguageProvider>
          <Layout />
        </LanguageProvider>
      </ThemeProvider>
    </UserProvider>
  );
}

// Simplified components - no prop drilling
function Layout() {
  const { theme } = useTheme();
  
  return (
    <div className={`layout layout--${theme}`}>
      <Header />
      <Sidebar />
      <MainContent />
    </div>
  );
}

function UserMenu() {
  const { user, logout } = useUser();
  const { theme, toggleTheme } = useTheme();
  
  return (
    <div className={`user-menu user-menu--${theme}`}>
      {user && (
        <div>
          <span>Welcome, {user.name}</span>
          <button onClick={logout}>Logout</button>
        </div>
      )}
      <button onClick={toggleTheme}>
        Switch to {theme === 'light' ? 'dark' : 'light'} mode
      </button>
    </div>
  );
}
```

### 🎯 Context Performance Considerations

**Interview Critical Point:** Context re-renders all consumers when the value changes. Understanding optimization patterns is crucial.

```jsx
// ❌ Problematic: Creating new object on every render
function BadThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}

// ✅ Optimized: Stable reference with useMemo
function OptimizedThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  
  const value = useMemo(() => ({
    theme,
    setTheme,
    toggleTheme: () => setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }), [theme]);
  
  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

// ✅ Split contexts for better performance
const ThemeStateContext = createContext();
const ThemeActionsContext = createContext();

function SplitThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  
  const actions = useMemo(() => ({
    setTheme,
    toggleTheme: () => setTheme(prev => prev === 'light' ? 'dark' : 'light')
  }), []);
  
  return (
    <ThemeStateContext.Provider value={theme}>
      <ThemeActionsContext.Provider value={actions}>
        {children}
      </ThemeActionsContext.Provider>
    </ThemeStateContext.Provider>
  );
}

// Separate hooks for state and actions
function useThemeState() {
  const context = useContext(ThemeStateContext);
  if (context === undefined) {
    throw new Error('useThemeState must be used within ThemeProvider');
  }
  return context;
}

function useThemeActions() {
  const context = useContext(ThemeActionsContext);
  if (context === undefined) {
    throw new Error('useThemeActions must be used within ThemeProvider');
  }
  return context;
}

// Components only re-render when needed
function ThemeDisplay() {
  const theme = useThemeState(); // Only re-renders when theme changes
  return <div>Current theme: {theme}</div>;
}

function ThemeToggler() {
  const { toggleTheme } = useThemeActions(); // Doesn't re-render when theme changes
  return <button onClick={toggleTheme}>Toggle Theme</button>;
}
```

### 🎯 When to Use Context vs Props

**Interview Decision Matrix:**

```jsx
// ✅ Use Context for:
// - Global app state (user, theme, language)
// - Deeply nested components
// - Configuration that many components need

// ✅ Use Props for:
// - Parent-child communication
// - Component-specific data
// - When you want explicit data flow

// Example: Mixed approach
function BlogPost({ post }) {
  // Props for direct parent-child communication
  return (
    <article>
      <PostHeader title={post.title} author={post.author} />
      <PostContent content={post.content} />
      <PostFooter postId={post.id} />
    </article>
  );
}

function PostFooter({ postId }) {
  // Context for global state
  const { user } = useUser();
  const { theme } = useTheme();
  
  return (
    <footer className={`post-footer post-footer--${theme}`}>
      <LikeButton postId={postId} userId={user?.id} />
      <ShareButton postId={postId} />
    </footer>
  );
}
```

---

**This completes the first part of the Intermediate Level guide. Should I continue with the remaining sections (Error Boundaries, Portals, Refs & Forwarding Refs, Fragments & StrictMode)?**

---

## Error Boundaries

> **Interview Expectation:** Understand React's error handling mechanism and how to implement robust error boundaries for production applications.

### 🎯 What Are Error Boundaries?

**Interview Critical Point:** Error boundaries are React components that catch JavaScript errors anywhere in their child component tree and display fallback UI instead of crashing the entire app.

```jsx
// ✅ Class-based Error Boundary (only way to create them)
class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      hasError: false, 
      error: null, 
      errorInfo: null 
    };
  }
  
  // Catch errors during rendering
  static getDerivedStateFromError(error) {
    // Update state to show fallback UI
    return { hasError: true };
  }
  
  // Log error information
  componentDidCatch(error, errorInfo) {
    console.error('Error Boundary caught an error:', error);
    console.error('Error Info:', errorInfo);
    
    // Log to error reporting service
    this.logErrorToService(error, errorInfo);
    
    this.setState({
      error,
      errorInfo
    });
  }
  
  logErrorToService = (error, errorInfo) => {
    // Send to error tracking service (Sentry, LogRocket, etc.)
    if (window.Sentry) {
      window.Sentry.captureException(error, {
        contexts: {
          react: {
            componentStack: errorInfo.componentStack
          }
        }
      });
    }
  }
  
  render() {
    if (this.state.hasError) {
      // Custom fallback UI
      return (
        <div className="error-boundary">
          <h2>Something went wrong.</h2>
          <details style={{ whiteSpace: 'pre-wrap' }}>
            <summary>Error Details (Click to expand)</summary>
            <p><strong>Error:</strong> {this.state.error && this.state.error.toString()}</p>
            <p><strong>Component Stack:</strong> {this.state.errorInfo.componentStack}</p>
          </details>
          <button 
            onClick={() => this.setState({ hasError: false, error: null, errorInfo: null })}
          >
            Try Again
          </button>
        </div>
      );
    }
    
    return this.props.children;
  }
}

// Usage
function App() {
  return (
    <ErrorBoundary>
      <Header />
      <ErrorBoundary> {/* Nested boundaries for granular error handling */}
        <MainContent />
      </ErrorBoundary>
      <Footer />
    </ErrorBoundary>
  );
}
```

### 🎯 Advanced Error Boundary Patterns

```jsx
// Reusable Error Boundary with custom fallback
function withErrorBoundary(Component, fallbackComponent) {
  return class extends React.Component {
    constructor(props) {
      super(props);
      this.state = { hasError: false, error: null };
    }
    
    static getDerivedStateFromError(error) {
      return { hasError: true, error };
    }
    
    componentDidCatch(error, errorInfo) {
      console.error('Error in', Component.name, ':', error, errorInfo);
    }
    
    render() {
      if (this.state.hasError) {
        const FallbackComponent = fallbackComponent || DefaultErrorFallback;
        return (
          <FallbackComponent 
            error={this.state.error} 
            resetError={() => this.setState({ hasError: false, error: null })}
          />
        );
      }
      
      return <Component {...this.props} />;
    }
  };
}

// Default fallback component
function DefaultErrorFallback({ error, resetError }) {
  return (
    <div className="error-fallback">
      <h2>Oops! Something went wrong</h2>
      <p>We apologize for the inconvenience. Please try again.</p>
      <button onClick={resetError}>Try Again</button>
      {process.env.NODE_ENV === 'development' && (
        <details>
          <summary>Error Details (Development Only)</summary>
          <pre>{error.message}</pre>
        </details>
      )}
    </div>
  );
}

// Custom fallback for specific features
function FeatureErrorFallback({ error, resetError }) {
  return (
    <div className="feature-error">
      <h3>This feature is temporarily unavailable</h3>
      <p>We're working to fix this issue. You can continue using other parts of the app.</p>
      <button onClick={resetError}>Reload Feature</button>
    </div>
  );
}

// Usage with HOC
const SafeUserProfile = withErrorBoundary(UserProfile, FeatureErrorFallback);
const SafeDashboard = withErrorBoundary(Dashboard);
```

### 🎯 What Error Boundaries DON'T Catch

**Interview Critical Point:** Error boundaries have limitations and don't catch certain types of errors.

```jsx
// ❌ Error boundaries DON'T catch these:
function ProblematicComponent() {
  const [count, setCount] = useState(0);
  
  // 1. Event handlers (use try-catch instead)
  const handleClick = () => {
    try {
      // This error won't be caught by error boundary
      throw new Error('Event handler error');
    } catch (error) {
      console.error('Caught in event handler:', error);
      // Handle gracefully
    }
  };
  
  // 2. Async code (use try-catch with async/await)
  const fetchData = async () => {
    try {
      const response = await fetch('/api/data');
      if (!response.ok) throw new Error('Failed to fetch');
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Async error:', error);
      // Handle async errors appropriately
    }
  };
  
  // 3. Errors in setTimeout/setInterval
  useEffect(() => {
    const timer = setTimeout(() => {
      try {
        // This error won't be caught by error boundary
        throw new Error('Timer error');
      } catch (error) {
        console.error('Timer error:', error);
      }
    }, 1000);
    
    return () => clearTimeout(timer);
  }, []);
  
  // ✅ This WILL be caught by error boundary
  if (count > 5) {
    throw new Error('Count is too high!');
  }
  
  return (
    <div>
      <button onClick={handleClick}>Click me</button>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      <button onClick={fetchData}>Fetch Data</button>
    </div>
  );
}
```

---

## Portals

> **Interview Expectation:** Understand how to render components outside the normal component tree hierarchy while maintaining React's event system.

### 🎯 Basic Portal Implementation

**Interview Critical Point:** Portals allow you to render a child into a DOM node that exists outside the parent component's DOM hierarchy.

```jsx
import ReactDOM from 'react-dom';

// Basic portal setup
function Portal({ children, target }) {
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
    return () => setMounted(false);
  }, []);
  
  if (!mounted) return null;
  
  return ReactDOM.createPortal(
    children,
    target || document.body
  );
}

// Modal using portal
function Modal({ isOpen, onClose, children }) {
  const [modalRoot, setModalRoot] = useState(null);
  
  useEffect(() => {
    // Create modal root if it doesn't exist
    let root = document.getElementById('modal-root');
    if (!root) {
      root = document.createElement('div');
      root.id = 'modal-root';
      document.body.appendChild(root);
    }
    setModalRoot(root);
    
    // Cleanup on unmount
    return () => {
      if (root && root.children.length === 0) {
        document.body.removeChild(root);
      }
    };
  }, []);
  
  useEffect(() => {
    if (isOpen) {
      // Prevent body scroll when modal is open
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }
    
    // Cleanup on unmount or close
    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);
  
  if (!isOpen || !modalRoot) return null;
  
  return ReactDOM.createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div 
        className="modal-content" 
        onClick={(e) => e.stopPropagation()}
      >
        <button className="modal-close" onClick={onClose}>
          ×
        </button>
        {children}
      </div>
    </div>,
    modalRoot
  );
}

// Usage
function App() {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  return (
    <div className="app">
      <h1>My App</h1>
      <button onClick={() => setIsModalOpen(true)}>
        Open Modal
      </button>
      
      <Modal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)}
      >
        <h2>Modal Content</h2>
        <p>This modal is rendered outside the app's DOM tree!</p>
      </Modal>
    </div>
  );
}
```

### 🎯 Advanced Portal Patterns

```jsx
// Tooltip using portal with positioning
function Tooltip({ children, content, position = 'top' }) {
  const [isVisible, setIsVisible] = useState(false);
  const [coordinates, setCoordinates] = useState({ x: 0, y: 0 });
  const triggerRef = useRef(null);
  
  const showTooltip = (e) => {
    const rect = triggerRef.current.getBoundingClientRect();
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
    
    let x, y;
    
    switch (position) {
      case 'top':
        x = rect.left + scrollLeft + rect.width / 2;
        y = rect.top + scrollTop - 10;
        break;
      case 'bottom':
        x = rect.left + scrollLeft + rect.width / 2;
        y = rect.bottom + scrollTop + 10;
        break;
      case 'left':
        x = rect.left + scrollLeft - 10;
        y = rect.top + scrollTop + rect.height / 2;
        break;
      case 'right':
        x = rect.right + scrollLeft + 10;
        y = rect.top + scrollTop + rect.height / 2;
        break;
      default:
        x = rect.left + scrollLeft;
        y = rect.top + scrollTop;
    }
    
    setCoordinates({ x, y });
    setIsVisible(true);
  };
  
  const hideTooltip = () => {
    setIsVisible(false);
  };
  
  return (
    <>
      <span
        ref={triggerRef}
        onMouseEnter={showTooltip}
        onMouseLeave={hideTooltip}
        onFocus={showTooltip}
        onBlur={hideTooltip}
      >
        {children}
      </span>
      
      {isVisible && ReactDOM.createPortal(
        <div 
          className={`tooltip tooltip--${position}`}
          style={{
            position: 'absolute',
            left: coordinates.x,
            top: coordinates.y,
            transform: position === 'top' || position === 'bottom' 
              ? 'translateX(-50%)' 
              : position === 'left' || position === 'right'
              ? 'translateY(-50%)'
              : 'none',
            zIndex: 9999
          }}
        >
          {content}
        </div>,
        document.body
      )}
    </>
  );
}

// Notification system using portals
function NotificationProvider({ children }) {
  const [notifications, setNotifications] = useState([]);
  
  const addNotification = useCallback((notification) => {
    const id = Date.now().toString();
    const newNotification = { id, ...notification };
    
    setNotifications(prev => [...prev, newNotification]);
    
    // Auto-remove after timeout
    if (notification.timeout !== false) {
      setTimeout(() => {
        removeNotification(id);
      }, notification.timeout || 5000);
    }
    
    return id;
  }, []);
  
  const removeNotification = useCallback((id) => {
    setNotifications(prev => prev.filter(notif => notif.id !== id));
  }, []);
  
  const contextValue = useMemo(() => ({
    addNotification,
    removeNotification
  }), [addNotification, removeNotification]);
  
  return (
    <NotificationContext.Provider value={contextValue}>
      {children}
      
      {ReactDOM.createPortal(
        <div className="notification-container">
          {notifications.map(notification => (
            <div 
              key={notification.id}
              className={`notification notification--${notification.type || 'info'}`}
            >
              <span>{notification.message}</span>
              <button 
                onClick={() => removeNotification(notification.id)}
                className="notification-close"
              >
                ×
              </button>
            </div>
          ))}
        </div>,
        document.body
      )}
    </NotificationContext.Provider>
  );
}

// Custom hook for notifications
const NotificationContext = createContext();

function useNotifications() {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotifications must be used within NotificationProvider');
  }
  return context;
}

// Usage
function SomeComponent() {
  const { addNotification } = useNotifications();
  
  const handleSuccess = () => {
    addNotification({
      type: 'success',
      message: 'Operation completed successfully!',
      timeout: 3000
    });
  };
  
  const handleError = () => {
    addNotification({
      type: 'error',
      message: 'Something went wrong. Please try again.',
      timeout: false // Persistent notification
    });
  };
  
  return (
    <div>
      <button onClick={handleSuccess}>Show Success</button>
      <button onClick={handleError}>Show Error</button>
    </div>
  );
}
```

### 🎯 Portal Event Bubbling

**Interview Critical Point:** Even though the child is rendered in a different DOM node, events bubble up through the React component tree, not the DOM tree.

```jsx
function PortalEventDemo() {
  const [clickCount, setClickCount] = useState(0);
  
  // This handler will catch clicks from the portal content
  const handleParentClick = () => {
    console.log('Parent clicked! Events bubble through React tree, not DOM tree');
    setClickCount(count => count + 1);
  };
  
  return (
    <div onClick={handleParentClick} style={{ padding: '20px', border: '1px solid blue' }}>
      <h3>Parent Component (clicks: {clickCount})</h3>
      <p>Click the button in the portal below:</p>
      
      {ReactDOM.createPortal(
        <div style={{ 
          position: 'fixed', 
          top: '50px', 
          right: '50px', 
          padding: '20px', 
          backgroundColor: 'yellow',
          border: '1px solid red'
        }}>
          <p>This is rendered in a portal!</p>
          <button onClick={() => console.log('Portal button clicked')}>
            Click me - Event will bubble to parent!
          </button>
        </div>,
        document.body
      )}
    </div>
  );
}
```

---

## Refs & Forwarding Refs

> **Interview Expectation:** Understand how to access DOM elements directly and how to properly forward refs through component hierarchies.

### 🎯 Basic Ref Usage

**Interview Critical Point:** Refs provide a way to access DOM nodes or React elements directly without triggering re-renders.

```jsx
// Basic ref usage for DOM access
function FocusableInput() {
  const inputRef = useRef(null);
  const [value, setValue] = useState('');
  
  const focusInput = () => {
    inputRef.current.focus();
  };
  
  const selectAll = () => {
    inputRef.current.select();
  };
  
  const getInputInfo = () => {
    const input = inputRef.current;
    console.log('Input info:', {
      value: input.value,
      selectionStart: input.selectionStart,
      selectionEnd: input.selectionEnd,
      scrollWidth: input.scrollWidth,
      clientWidth: input.clientWidth
    });
  };
  
  return (
    <div>
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder="Type something..."
      />
      <div>
        <button onClick={focusInput}>Focus Input</button>
        <button onClick={selectAll}>Select All</button>
        <button onClick={getInputInfo}>Get Input Info</button>
      </div>
    </div>
  );
}

// Ref for storing mutable values (doesn't trigger re-render)
function Timer() {
  const [seconds, setSeconds] = useState(0);
  const [isRunning, setIsRunning] = useState(false);
  const intervalRef = useRef(null);
  const startTimeRef = useRef(null);
  
  const startTimer = () => {
    if (!isRunning) {
      setIsRunning(true);
      startTimeRef.current = Date.now() - seconds * 1000;
      
      intervalRef.current = setInterval(() => {
        setSeconds(Math.floor((Date.now() - startTimeRef.current) / 1000));
      }, 100);
    }
  };
  
  const stopTimer = () => {
    setIsRunning(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };
  
  const resetTimer = () => {
    stopTimer();
    setSeconds(0);
  };
  
  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);
  
  return (
    <div>
      <h3>Timer: {seconds}s</h3>
      <button onClick={startTimer} disabled={isRunning}>
        Start
      </button>
      <button onClick={stopTimer} disabled={!isRunning}>
        Stop
      </button>
      <button onClick={resetTimer}>Reset</button>
    </div>
  );
}
```

### 🎯 Forwarding Refs

**Interview Critical Point:** forwardRef allows a component to pass a ref through to one of its children, enabling parent components to access child DOM nodes.

```jsx
// Basic ref forwarding
const FancyInput = React.forwardRef((props, ref) => {
  return (
    <div className="fancy-input-container">
      <label>{props.label}</label>
      <input
        ref={ref}
        type={props.type || 'text'}
        placeholder={props.placeholder}
        {...props}
      />
    </div>
  );
});

// Usage of forwarded ref
function ParentComponent() {
  const inputRef = useRef(null);
  
  const focusInput = () => {
    inputRef.current.focus();
  };
  
  return (
    <div>
      <FancyInput
        ref={inputRef}
        label="Username:"
        placeholder="Enter your username"
      />
      <button onClick={focusInput}>Focus Input</button>
    </div>
  );
}

// Advanced: Forwarding refs with useImperativeHandle
const AdvancedInput = React.forwardRef((props, ref) => {
  const inputRef = useRef(null);
  const [value, setValue] = useState(props.defaultValue || '');
  
  // Expose custom methods to parent
  useImperativeHandle(ref, () => ({
    focus: () => {
      inputRef.current.focus();
    },
    clear: () => {
      setValue('');
      inputRef.current.focus();
    },
    getValue: () => {
      return value;
    },
    setValue: (newValue) => {
      setValue(newValue);
    },
    selectAll: () => {
      inputRef.current.select();
    }
  }));
  
  return (
    <div className="advanced-input">
      <input
        ref={inputRef}
        type="text"
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={props.placeholder}
      />
      {props.showClearButton && value && (
        <button 
          onClick={() => setValue('')}
          className="clear-button"
        >
          Clear
        </button>
      )}
    </div>
  );
});

// Usage with useImperativeHandle
function FormWithAdvancedInputs() {
  const usernameRef = useRef(null);
  const emailRef = useRef(null);
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    const formData = {
      username: usernameRef.current.getValue(),
      email: emailRef.current.getValue()
    };
    
    console.log('Form data:', formData);
  };
  
  const clearForm = () => {
    usernameRef.current.clear();
    emailRef.current.clear();
  };
  
  const focusFirstEmpty = () => {
    if (!usernameRef.current.getValue()) {
      usernameRef.current.focus();
    } else if (!emailRef.current.getValue()) {
      emailRef.current.focus();
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <AdvancedInput
        ref={usernameRef}
        placeholder="Username"
        showClearButton
      />
      <AdvancedInput
        ref={emailRef}
        placeholder="Email"
        showClearButton
      />
      <div>
        <button type="submit">Submit</button>
        <button type="button" onClick={clearForm}>Clear All</button>
        <button type="button" onClick={focusFirstEmpty}>Focus First Empty</button>
      </div>
    </form>
  );
}
```

### 🎯 Ref Patterns and Best Practices

```jsx
// Callback refs for dynamic elements
function DynamicList({ items }) {
  const itemRefs = useRef({});
  
  const setItemRef = (id) => (element) => {
    if (element) {
      itemRefs.current[id] = element;
    } else {
      delete itemRefs.current[id];
    }
  };
  
  const scrollToItem = (id) => {
    const element = itemRefs.current[id];
    if (element) {
      element.scrollIntoView({ behavior: 'smooth' });
    }
  };
  
  return (
    <div>
      <div className="navigation">
        {items.map(item => (
          <button key={item.id} onClick={() => scrollToItem(item.id)}>
            Go to {item.title}
          </button>
        ))}
      </div>
      
      <div className="content">
        {items.map(item => (
          <div
            key={item.id}
            ref={setItemRef(item.id)}
            className="item"
            style={{ height: '200px', margin: '20px 0' }}
          >
            <h3>{item.title}</h3>
            <p>{item.content}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

// Measuring DOM elements
function MeasuredComponent() {
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  const elementRef = useRef(null);
  
  const measureElement = useCallback(() => {
    if (elementRef.current) {
      const { offsetWidth, offsetHeight } = elementRef.current;
      setDimensions({ width: offsetWidth, height: offsetHeight });
    }
  }, []);
  
  useEffect(() => {
    measureElement();
    
    const resizeObserver = new ResizeObserver(measureElement);
    if (elementRef.current) {
      resizeObserver.observe(elementRef.current);
    }
    
    return () => {
      resizeObserver.disconnect();
    };
  }, [measureElement]);
  
  return (
    <div>
      <div
        ref={elementRef}
        style={{
          padding: '20px',
          border: '1px solid #ccc',
          resize: 'both',
          overflow: 'auto',
          minWidth: '100px',
          minHeight: '100px'
        }}
      >
        <p>Resize me!</p>
        <p>Width: {dimensions.width}px</p>
        <p>Height: {dimensions.height}px</p>
      </div>
    </div>
  );
}
```

---

## Fragments & StrictMode

> **Interview Expectation:** Understand React's utility components and development tools that improve code quality and debugging.

### 🎯 React Fragments

**Interview Critical Point:** Fragments let you group multiple elements without adding extra DOM nodes, solving the "wrapper div" problem.

```jsx
// ❌ Problem: Unnecessary wrapper div
function BadList({ items }) {
  return (
    <div>  {/* Unnecessary wrapper */}
      <li>Header Item</li>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </div>
  );
}

// ✅ Solution: React Fragment
function GoodList({ items }) {
  return (
    <React.Fragment>
      <li>Header Item</li>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </React.Fragment>
  );
}

// ✅ Short syntax
function ShortSyntaxList({ items }) {
  return (
    <>
      <li>Header Item</li>
      {items.map(item => (
        <li key={item.id}>{item.name}</li>
      ))}
    </>
  );
}

// Fragment with key (only full syntax supports keys)
function TableRows({ data }) {
  return (
    <tbody>
      {data.map(section => (
        <React.Fragment key={section.id}>
          <tr>
            <td colSpan="2">{section.title}</td>
          </tr>
          {section.items.map(item => (
            <tr key={item.id}>
              <td>{item.name}</td>
              <td>{item.value}</td>
            </tr>
          ))}
        </React.Fragment>
      ))}
    </tbody>
  );
}

// Real-world example: Modal content without wrapper
function Modal({ children, isOpen, onClose }) {
  if (!isOpen) return null;
  
  return ReactDOM.createPortal(
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        {children}
      </div>
    </div>,
    document.body
  );
}

function ModalContent() {
  return (
    <>  {/* No wrapper div needed */}
      <h2>Modal Title</h2>
      <p>Modal content goes here.</p>
      <div className="modal-actions">
        <button>Cancel</button>
        <button>Confirm</button>
      </div>
    </>
  );
}
```

### 🎯 React StrictMode

**Interview Critical Point:** StrictMode is a development tool that helps identify potential problems by intentionally double-invoking functions and running additional checks.

```jsx
// Basic StrictMode usage
function App() {
  return (
    <React.StrictMode>
      <Header />
      <MainContent />
      <Footer />
    </React.StrictMode>
  );
}

// Partial StrictMode (only for specific components)
function App() {
  return (
    <div>
      <Header />
      <React.StrictMode>
        <ExperimentalFeature />  {/* Only this component gets strict mode */}
      </React.StrictMode>
      <Footer />
    </div>
  );
}

// What StrictMode detects:
function ProblematicComponent() {
  const [count, setCount] = useState(0);
  
  // ❌ Side effect in render (StrictMode will warn)
  console.log('Rendering component'); // This will log twice in StrictMode
  
  // ❌ Unsafe lifecycle method (if this were a class component)
  // componentWillMount() { ... } // StrictMode warns about deprecated lifecycles
  
  useEffect(() => {
    // ✅ Effects run normally, but StrictMode may double-invoke them
    console.log('Effect running');
    
    // ❌ Missing cleanup (StrictMode helps detect memory leaks)
    const timer = setInterval(() => {
      console.log('Timer tick');
    }, 1000);
    
    // ✅ Proper cleanup
    return () => clearInterval(timer);
  }, []);
  
  // ❌ Non-pure function (StrictMode double-invokes to catch this)
  const impureFunction = () => {
    window.globalCounter = (window.globalCounter || 0) + 1; // Side effect!
    return count * 2;
  };
  
  // ✅ Pure function
  const pureFunction = (value) => {
    return value * 2;
  };
  
  return (
    <div>
      <p>Count: {count}</p>
      <p>Impure result: {impureFunction()}</p>
      <p>Pure result: {pureFunction(count)}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}

// StrictMode best practices
function StrictModeCompatibleComponent() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  
  // ✅ Effects with proper cleanup
  useEffect(() => {
    let cancelled = false;
    
    const fetchData = async () => {
      setLoading(true);
      try {
        const response = await fetch('/api/data');
        const result = await response.json();
        
        if (!cancelled) {
          setData(result);
        }
      } catch (error) {
        if (!cancelled) {
          console.error('Fetch error:', error);
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    };
    
    fetchData();
    
    return () => {
      cancelled = true;
    };
  }, []);
  
  // ✅ Pure render logic
  const renderData = () => {
    if (loading) return <div>Loading...</div>;
    if (!data) return <div>No data</div>;
    return <div>Data: {JSON.stringify(data)}</div>;
  };
  
  return (
    <div>
      <h3>StrictMode Compatible Component</h3>
      {renderData()}
    </div>
  );
}
```

### 🎯 StrictMode Migration Tips

```jsx
// Common issues and solutions when adopting StrictMode

// Issue 1: Side effects in render
// ❌ Problematic
function BadComponent() {
  localStorage.setItem('lastRender', Date.now()); // Side effect in render
  return <div>Component</div>;
}

// ✅ Fixed
function GoodComponent() {
  useEffect(() => {
    localStorage.setItem('lastRender', Date.now()); // Side effect in effect
  });
  return <div>Component</div>;
}

// Issue 2: Non-idempotent effects
// ❌ Problematic
function BadEffectComponent() {
  useEffect(() => {
    window.globalCounter++; // Not idempotent
  }, []);
  
  return <div>Counter: {window.globalCounter}</div>;
}

// ✅ Fixed
function GoodEffectComponent() {
  const [counter, setCounter] = useState(0);
  
  useEffect(() => {
    // Idempotent effect
    setCounter(prev => prev + 1);
  }, []);
  
  return <div>Counter: {counter}</div>;
}

// Issue 3: Missing effect dependencies
// ❌ Problematic
function BadDependenciesComponent({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser); // Missing userId dependency
  }, []); // Empty deps but uses userId
  
  return <div>{user?.name}</div>;
}

// ✅ Fixed
function GoodDependenciesComponent({ userId }) {
  const [user, setUser] = useState(null);
  
  useEffect(() => {
    fetchUser(userId).then(setUser);
  }, [userId]); // Correct dependencies
  
  return <div>{user?.name}</div>;
}
```

---

## Interview Questions You Should Master

### Q: When would you use short-circuit evaluation vs ternary operator?
**A:** Use short-circuit (`&&`) for conditional rendering when you only need to show/hide elements. Use ternary for true/false scenarios. Avoid short-circuit with numbers that could be 0.

### Q: Why are keys important in React lists?
**A:** Keys help React identify which items have changed, been added, or removed during reconciliation. They enable efficient DOM updates and prevent state mixing between list items.

### Q: When should you use Context vs props?
**A:** Use Context for global state (user, theme, language) or data needed by many components. Use props for direct parent-child communication and component-specific data.

### Q: What errors do Error Boundaries NOT catch?
**A:** Event handlers, async code (promises, setTimeout), errors during SSR, and errors in the error boundary itself.

### Q: What's the difference between Portals and normal rendering?
**A:** Portals render children into a different DOM node while maintaining React's event bubbling through the component tree, not the DOM tree.

### Q: When would you use useImperativeHandle?
**A:** To expose specific methods from child components to parents, typically for focus management, form validation, or triggering animations imperatively.

### Q: What does React.StrictMode do?
**A:** Helps identify potential problems by double-invoking functions, detecting unsafe lifecycles, warning about deprecated APIs, and detecting side effects during rendering.
