# 🔥 React Core Fundamentals - Interview Deep Dive

> **Master the absolute essentials of React with interview-ready explanations and code examples**

---

## 📋 Table of Contents

1. [JSX - The Foundation](#jsx---the-foundation)
2. [Components - Building Blocks](#components---building-blocks)
3. [Lifecycle - Class vs Hooks](#lifecycle---class-vs-hooks)
4. [Essential Hooks Mastery](#essential-hooks-mastery)
5. [Events & Forms](#events--forms)

---

## JSX - The Foundation

> **Interview Expectation:** You must clearly explain what JSX is, how it works internally, and why React chose this approach over alternatives.

### 🎯 What is JSX and Why It's Not HTML?

**Interview Critical Point:** JSX is syntactic sugar for `React.createElement()` calls. It looks like HTML but compiles to JavaScript function calls.

```jsx
// What you write (JSX)
const element = <h1 className="greeting">Hello, {name}!</h1>;

// What it becomes (JavaScript)
const element = React.createElement(
  'h1',
  { className: 'greeting' },
  'Hello, ',
  name,
  '!'
);

// Final result (React Element Object)
const element = {
  type: 'h1',
  props: {
    className: 'greeting',
    children: ['Hello, ', name, '!']
  },
  key: null,
  ref: null
};
```

**Key Differences from HTML:**

```jsx
// JSX uses camelCase for attributes
<div className="container" onClick={handleClick} />
// HTML uses lowercase
<div class="container" onclick="handleClick()" />

// JSX requires self-closing tags
<img src="image.jpg" />
<input type="text" />
// HTML allows unclosed tags
<img src="image.jpg">
<input type="text">

// JSX expressions must have single parent
return (
  <div>  {/* Single parent wrapper */}
    <h1>Title</h1>
    <p>Content</p>
  </div>
);

// React Fragments solve the wrapper problem
return (
  <>
    <h1>Title</h1>
    <p>Content</p>
  </>
);
```

### 🎯 How Babel Transpiles JSX

**Interview Deep Dive:** Understanding the compilation process shows mastery of React internals.

```jsx
// Original JSX
function Welcome({ name }) {
  return (
    <div className="welcome">
      <h1>Hello, {name}!</h1>
      <p>Welcome to our app.</p>
    </div>
  );
}

// Babel transformation (Classic Runtime - React 16)
function Welcome({ name }) {
  return React.createElement(
    'div',
    { className: 'welcome' },
    React.createElement('h1', null, 'Hello, ', name, '!'),
    React.createElement('p', null, 'Welcome to our app.')
  );
}

// Babel transformation (Automatic Runtime - React 17+)
import { jsx as _jsx, jsxs as _jsxs } from 'react/jsx-runtime';

function Welcome({ name }) {
  return _jsxs('div', {
    className: 'welcome',
    children: [
      _jsxs('h1', { children: ['Hello, ', name, '!'] }),
      _jsx('p', { children: 'Welcome to our app.' })
    ]
  });
}
```

**Interview Question:** *"Why did React introduce the automatic JSX transform?"*

**Answer:** The automatic runtime eliminates the need to import React in every file that uses JSX, reduces bundle size, and improves performance by using optimized helper functions.

---

## Components - Building Blocks

> **Interview Expectation:** Demonstrate deep understanding of component types, their differences, and when to use each approach.

### 🎯 Functional vs Class Components

**Interview Critical Point:** Functional components with hooks are the modern standard, but understanding class components is essential for legacy code and interviews.

```jsx
// Class Component (Legacy but still important to know)
class UserProfile extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      user: null,
      loading: true,
      error: null
    };
    
    // Binding methods (common interview topic)
    this.handleUpdate = this.handleUpdate.bind(this);
  }
  
  componentDidMount() {
    this.fetchUser();
  }
  
  componentDidUpdate(prevProps) {
    if (prevProps.userId !== this.props.userId) {
      this.fetchUser();
    }
  }
  
  fetchUser = async () => {
    try {
      this.setState({ loading: true });
      const user = await fetchUser(this.props.userId);
      this.setState({ user, loading: false });
    } catch (error) {
      this.setState({ error, loading: false });
    }
  }
  
  handleUpdate = (newData) => {
    this.setState(prevState => ({
      user: { ...prevState.user, ...newData }
    }));
  }
  
  render() {
    const { user, loading, error } = this.state;
    
    if (loading) return <div>Loading...</div>;
    if (error) return <div>Error: {error.message}</div>;
    
    return (
      <div>
        <h1>{user.name}</h1>
        <button onClick={() => this.handleUpdate({ name: 'Updated' })}>
          Update
        </button>
      </div>
    );
  }
}

// Functional Component (Modern approach)
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const fetchUser = useCallback(async () => {
    try {
      setLoading(true);
      const userData = await fetchUser(userId);
      setUser(userData);
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, [userId]);
  
  useEffect(() => {
    fetchUser();
  }, [fetchUser]);
  
  const handleUpdate = useCallback((newData) => {
    setUser(prevUser => ({ ...prevUser, ...newData }));
  }, []);
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;
  
  return (
    <div>
      <h1>{user.name}</h1>
      <button onClick={() => handleUpdate({ name: 'Updated' })}>
        Update
      </button>
    </div>
  );
}
```

### 🎯 Props vs State - The Data Flow Story

**Interview Critical Point:** Props flow down (parent to child), state is internal to component. This unidirectional data flow is fundamental to React's architecture.

```jsx
// Props: External data passed from parent
function UserCard({ user, onEdit, theme = 'light' }) {
  // Props are read-only - never modify them
  // user.name = 'Modified'; // ❌ Never do this!
  
  return (
    <div className={`card card--${theme}`}>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <button onClick={() => onEdit(user.id)}>Edit</button>
    </div>
  );
}

// State: Internal component data that can change
function UserList() {
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState(null);
  const [theme, setTheme] = useState('light');
  
  const handleEdit = useCallback((userId) => {
    const user = users.find(u => u.id === userId);
    setSelectedUser(user);
  }, [users]);
  
  return (
    <div>
      <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
        Toggle Theme
      </button>
      
      {users.map(user => (
        <UserCard
          key={user.id}
          user={user}          // Props: Data
          onEdit={handleEdit}  // Props: Callback
          theme={theme}        // Props: Configuration
        />
      ))}
      
      {selectedUser && (
        <EditModal user={selectedUser} onClose={() => setSelectedUser(null)} />
      )}
    </div>
  );
}
```

### 🎯 Props Validation & TypeScript

**Interview Deep Dive:** Show professionalism with proper prop validation and type safety.

```jsx
// PropTypes (Legacy but still used)
import PropTypes from 'prop-types';

function UserCard({ user, onEdit, theme }) {
  return (
    <div className={`card card--${theme}`}>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      <button onClick={() => onEdit(user.id)}>Edit</button>
    </div>
  );
}

UserCard.propTypes = {
  user: PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    email: PropTypes.string.isRequired
  }).isRequired,
  onEdit: PropTypes.func.isRequired,
  theme: PropTypes.oneOf(['light', 'dark'])
};

UserCard.defaultProps = {
  theme: 'light'
};

// TypeScript (Modern approach)
interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
}

interface UserCardProps {
  user: User;
  onEdit: (userId: string) => void;
  theme?: 'light' | 'dark';
  className?: string;
}

function UserCard({ 
  user, 
  onEdit, 
  theme = 'light',
  className = ''
}: UserCardProps) {
  return (
    <div className={`card card--${theme} ${className}`}>
      <h2>{user.name}</h2>
      <p>{user.email}</p>
      {user.avatar && <img src={user.avatar} alt={`${user.name}'s avatar`} />}
      <button onClick={() => onEdit(user.id)}>Edit</button>
    </div>
  );
}
```

---

## Lifecycle - Class vs Hooks

> **Interview Expectation:** Show how modern hooks replicate class lifecycle methods and explain the mental model shift.

### 🎯 Complete Lifecycle Mapping

**Interview Critical Point:** Each class lifecycle method has a hooks equivalent, but the mental model is different - think in terms of synchronizing with external systems.

```jsx
// Class Component Lifecycle
class DataComponent extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      data: null,
      loading: false,
      error: null
    };
  }
  
  // Mount phase
  componentDidMount() {
    console.log('Component mounted');
    this.fetchData();
    this.startPolling();
  }
  
  // Update phase
  componentDidUpdate(prevProps, prevState) {
    // Conditional updates based on prop changes
    if (prevProps.userId !== this.props.userId) {
      this.fetchData();
    }
    
    // Conditional updates based on state changes
    if (prevState.data !== this.state.data) {
      this.saveToLocalStorage();
    }
  }
  
  // Unmount phase
  componentWillUnmount() {
    console.log('Component will unmount');
    this.stopPolling();
    this.abortController.abort();
  }
  
  fetchData = async () => {
    this.setState({ loading: true });
    try {
      const data = await fetchUserData(this.props.userId);
      this.setState({ data, loading: false });
    } catch (error) {
      this.setState({ error, loading: false });
    }
  }
  
  startPolling = () => {
    this.pollInterval = setInterval(this.fetchData, 5000);
  }
  
  stopPolling = () => {
    if (this.pollInterval) {
      clearInterval(this.pollInterval);
    }
  }
  
  render() {
    // ... render logic
  }
}

// Hooks Equivalent
function DataComponent({ userId }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const abortControllerRef = useRef();
  const pollIntervalRef = useRef();
  
  // Replaces componentDidMount + componentDidUpdate for data fetching
  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      // Create new AbortController for this request
      abortControllerRef.current = new AbortController();
      
      try {
        const response = await fetchUserData(userId, {
          signal: abortControllerRef.current.signal
        });
        setData(response);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err);
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
    
    // Cleanup function (componentWillUnmount equivalent)
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, [userId]); // Dependency array - runs when userId changes
  
  // Separate effect for polling (componentDidMount + componentWillUnmount)
  useEffect(() => {
    console.log('Component mounted');
    
    const startPolling = () => {
      pollIntervalRef.current = setInterval(() => {
        // Trigger data refetch
        fetchData();
      }, 5000);
    };
    
    startPolling();
    
    // Cleanup function
    return () => {
      console.log('Component will unmount');
      if (pollIntervalRef.current) {
        clearInterval(pollIntervalRef.current);
      }
    };
  }, []); // Empty dependency - runs once on mount
  
  // Effect for side effects based on data changes
  useEffect(() => {
    if (data) {
      localStorage.setItem(`user-${userId}`, JSON.stringify(data));
    }
  }, [data, userId]); // Runs when data or userId changes
  
  // ... render logic
}
```

**Interview Questions & Answers:**

**Q: "What's the difference between componentDidUpdate and useEffect?"**

**A:** `componentDidUpdate` runs after every update, while `useEffect` can be controlled with dependencies. `useEffect` with no dependency array runs after every render, with empty array `[]` runs only once, and with dependencies runs only when those values change.

**Q: "How do you replicate componentDidMount exactly?"**

**A:** Use `useEffect` with an empty dependency array: `useEffect(() => { /* mount logic */ }, [])`

**Q: "What about componentWillUnmount?"**

**A:** Return a cleanup function from `useEffect`: `useEffect(() => { return () => { /* cleanup */ }; }, [])`

---

## Essential Hooks Mastery

> **Interview Expectation:** Demonstrate deep understanding of built-in hooks, their rules, and show practical custom hook implementations.

### 🎯 Built-in Hooks Deep Dive

```jsx
// useState - State management with functional updates
function Counter() {
  const [count, setCount] = useState(0);
  const [history, setHistory] = useState([]);
  
  // Functional updates for state based on previous state
  const increment = () => {
    setCount(prevCount => prevCount + 1);
    setHistory(prevHistory => [...prevHistory, 'increment']);
  };
  
  // Batch updates - React automatically batches multiple setState calls
  const incrementTwice = () => {
    setCount(prev => prev + 1); // Queued update
    setCount(prev => prev + 1); // Queued update
    // Result: count increases by 2
  };
  
  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={increment}>+1</button>
      <button onClick={incrementTwice}>+2</button>
    </div>
  );
}

// useEffect - Side effects and synchronization
function UserProfile({ userId }) {
  const [user, setUser] = useState(null);
  
  // Effect with dependency - runs when userId changes
  useEffect(() => {
    let cancelled = false;
    
    const fetchUser = async () => {
      try {
        const userData = await api.getUser(userId);
        if (!cancelled) {
          setUser(userData);
        }
      } catch (error) {
        if (!cancelled) {
          console.error('Failed to fetch user:', error);
        }
      }
    };
    
    fetchUser();
    
    // Cleanup function prevents race conditions
    return () => {
      cancelled = true;
    };
  }, [userId]);
  
  // Effect for document title (side effect)
  useEffect(() => {
    const originalTitle = document.title;
    document.title = user ? `Profile - ${user.name}` : 'Profile';
    
    return () => {
      document.title = originalTitle;
    };
  }, [user]);
  
  return user ? <div>{user.name}</div> : <div>Loading...</div>;
}

// useContext - Consuming context values
const ThemeContext = createContext();
const UserContext = createContext();

function ThemedButton() {
  const { theme, toggleTheme } = useContext(ThemeContext);
  const { user } = useContext(UserContext);
  
  return (
    <button 
      className={`btn btn--${theme}`}
      onClick={toggleTheme}
    >
      Hello, {user.name}!
    </button>
  );
}

// useRef - Accessing DOM elements and persisting values
function FocusInput() {
  const inputRef = useRef(null);
  const renderCountRef = useRef(0);
  
  // useRef doesn't trigger re-renders when changed
  useEffect(() => {
    renderCountRef.current += 1;
    console.log(`Component rendered ${renderCountRef.current} times`);
  });
  
  const focusInput = () => {
    inputRef.current.focus();
  };
  
  return (
    <div>
      <input ref={inputRef} type="text" />
      <button onClick={focusInput}>Focus Input</button>
      <p>Render count: {renderCountRef.current}</p>
    </div>
  );
}

// useReducer - Complex state logic
const initialState = {
  todos: [],
  filter: 'all',
  loading: false
};

function todoReducer(state, action) {
  switch (action.type) {
    case 'ADD_TODO':
      return {
        ...state,
        todos: [...state.todos, action.payload]
      };
    
    case 'TOGGLE_TODO':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === action.payload
            ? { ...todo, completed: !todo.completed }
            : todo
        )
      };
    
    case 'SET_FILTER':
      return {
        ...state,
        filter: action.payload
      };
    
    case 'SET_LOADING':
      return {
        ...state,
        loading: action.payload
      };
    
    default:
      return state;
  }
}

function TodoApp() {
  const [state, dispatch] = useReducer(todoReducer, initialState);
  
  const addTodo = (text) => {
    dispatch({
      type: 'ADD_TODO',
      payload: {
        id: Date.now(),
        text,
        completed: false
      }
    });
  };
  
  const toggleTodo = (id) => {
    dispatch({ type: 'TOGGLE_TODO', payload: id });
  };
  
  return (
    <div>
      {/* Todo app UI */}
    </div>
  );
}
```

### 🎯 Rules of Hooks

**Interview Critical Point:** These rules ensure hooks work correctly and consistently.

```jsx
// ✅ CORRECT: Hooks at top level
function MyComponent({ condition }) {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');
  
  useEffect(() => {
    document.title = `Count: ${count}`;
  }, [count]);
  
  // Conditional logic AFTER hooks
  if (condition) {
    return <div>Conditional render</div>;
  }
  
  return <div>{count}</div>;
}

// ❌ WRONG: Conditional hooks
function WrongComponent({ condition }) {
  if (condition) {
    const [count, setCount] = useState(0); // ❌ Hook in condition
  }
  
  const [name, setName] = useState(''); // ❌ Inconsistent hook order
  
  return <div>Wrong</div>;
}

// ❌ WRONG: Hooks in loops
function AnotherWrongComponent({ items }) {
  items.forEach(item => {
    const [selected, setSelected] = useState(false); // ❌ Hook in loop
  });
  
  return <div>Wrong</div>;
}

// ✅ CORRECT: Custom hooks can use other hooks
function useCounter(initialValue = 0) {
  const [count, setCount] = useState(initialValue);
  
  const increment = useCallback(() => {
    setCount(prev => prev + 1);
  }, []);
  
  const decrement = useCallback(() => {
    setCount(prev => prev - 1);
  }, []);
  
  return { count, increment, decrement };
}
```

### 🎯 Custom Hooks - Real-World Examples

**Interview Deep Dive:** Show practical custom hooks that solve common problems.

```jsx
// useFetch - API data fetching
function useFetch(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const abortController = new AbortController();
    
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await fetch(url, {
          ...options,
          signal: abortController.signal
        });
        
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        setData(result);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
    
    return () => {
      abortController.abort();
    };
  }, [url, JSON.stringify(options)]);
  
  return { data, loading, error };
}

// Usage
function UserList() {
  const { data: users, loading, error } = useFetch('/api/users');
  
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <ul>
      {users.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

// useDebounce - Performance optimization
function useDebounce(value, delay) {
  const [debouncedValue, setDebouncedValue] = useState(value);
  
  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);
    
    return () => {
      clearTimeout(handler);
    };
  }, [value, delay]);
  
  return debouncedValue;
}

// Usage with search
function SearchComponent() {
  const [searchTerm, setSearchTerm] = useState('');
  const debouncedSearchTerm = useDebounce(searchTerm, 300);
  const { data: results } = useFetch(
    debouncedSearchTerm ? `/api/search?q=${debouncedSearchTerm}` : null
  );
  
  return (
    <div>
      <input
        type="text"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        placeholder="Search..."
      />
      {results && (
        <ul>
          {results.map(result => (
            <li key={result.id}>{result.title}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

// useOutsideClick - UI interaction
function useOutsideClick(ref, callback) {
  useEffect(() => {
    function handleClickOutside(event) {
      if (ref.current && !ref.current.contains(event.target)) {
        callback();
      }
    }
    
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [ref, callback]);
}

// Usage with dropdown
function Dropdown({ children }) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);
  
  useOutsideClick(dropdownRef, () => setIsOpen(false));
  
  return (
    <div ref={dropdownRef} className="dropdown">
      <button onClick={() => setIsOpen(!isOpen)}>
        Toggle Dropdown
      </button>
      {isOpen && (
        <div className="dropdown-menu">
          {children}
        </div>
      )}
    </div>
  );
}

// useLocalStorage - Persistent state
function useLocalStorage(key, initialValue) {
  // Get value from localStorage or use initial value
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key);
      return item ? JSON.parse(item) : initialValue;
    } catch (error) {
      console.error(`Error reading localStorage key "${key}":`, error);
      return initialValue;
    }
  });
  
  const setValue = useCallback((value) => {
    try {
      // Allow value to be a function for consistent API with useState
      const valueToStore = value instanceof Function ? value(storedValue) : value;
      setStoredValue(valueToStore);
      window.localStorage.setItem(key, JSON.stringify(valueToStore));
    } catch (error) {
      console.error(`Error setting localStorage key "${key}":`, error);
    }
  }, [key, storedValue]);
  
  return [storedValue, setValue];
}

// Usage
function Settings() {
  const [theme, setTheme] = useLocalStorage('theme', 'light');
  const [language, setLanguage] = useLocalStorage('language', 'en');
  
  return (
    <div>
      <select value={theme} onChange={(e) => setTheme(e.target.value)}>
        <option value="light">Light</option>
        <option value="dark">Dark</option>
      </select>
      <select value={language} onChange={(e) => setLanguage(e.target.value)}>
        <option value="en">English</option>
        <option value="es">Spanish</option>
      </select>
    </div>
  );
}
```

---

## Events & Forms

> **Interview Expectation:** Demonstrate understanding of React's event system and form handling patterns.

### 🎯 Controlled vs Uncontrolled Components

**Interview Critical Point:** Controlled components give React control over form state, while uncontrolled components let the DOM handle state.

```jsx
// Controlled Component - React controls the input value
function ControlledForm() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    country: 'usa',
    newsletter: false
  });
  
  const [errors, setErrors] = useState({});
  
  // Single handler for all inputs
  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };
  
  const validate = () => {
    const newErrors = {};
    
    if (!formData.username.trim()) {
      newErrors.username = 'Username is required';
    }
    
    if (!formData.email.includes('@')) {
      newErrors.email = 'Valid email is required';
    }
    
    if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validate()) {
      console.log('Form submitted:', formData);
      // Submit to API
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <div>
        <input
          type="text"
          name="username"
          value={formData.username}
          onChange={handleChange}
          placeholder="Username"
        />
        {errors.username && <span className="error">{errors.username}</span>}
      </div>
      
      <div>
        <input
          type="email"
          name="email"
          value={formData.email}
          onChange={handleChange}
          placeholder="Email"
        />
        {errors.email && <span className="error">{errors.email}</span>}
      </div>
      
      <div>
        <input
          type="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
          placeholder="Password"
        />
        {errors.password && <span className="error">{errors.password}</span>}
      </div>
      
      <div>
        <select name="country" value={formData.country} onChange={handleChange}>
          <option value="usa">United States</option>
          <option value="canada">Canada</option>
          <option value="uk">United Kingdom</option>
        </select>
      </div>
      
      <div>
        <label>
          <input
            type="checkbox"
            name="newsletter"
            checked={formData.newsletter}
            onChange={handleChange}
          />
          Subscribe to newsletter
        </label>
      </div>
      
      <button type="submit">Submit</button>
    </form>
  );
}

// Uncontrolled Component - DOM controls the input value
function UncontrolledForm() {
  const formRef = useRef();
  const usernameRef = useRef();
  const emailRef = useRef();
  const passwordRef = useRef();
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Access values directly from DOM
    const formData = {
      username: usernameRef.current.value,
      email: emailRef.current.value,
      password: passwordRef.current.value
    };
    
    console.log('Form submitted:', formData);
    
    // Reset form
    formRef.current.reset();
  };
  
  // Focus first input on mount
  useEffect(() => {
    usernameRef.current.focus();
  }, []);
  
  return (
    <form ref={formRef} onSubmit={handleSubmit}>
      <input
        ref={usernameRef}
        type="text"
        name="username"
        defaultValue=""
        placeholder="Username"
        required
      />
      
      <input
        ref={emailRef}
        type="email"
        name="email"
        defaultValue=""
        placeholder="Email"
        required
      />
      
      <input
        ref={passwordRef}
        type="password"
        name="password"
        defaultValue=""
        placeholder="Password"
        minLength={6}
        required
      />
      
      <button type="submit">Submit</button>
    </form>
  );
}
```

**Interview Questions & Answers:**

**Q: "When would you use uncontrolled components?"**

**A:** For simple forms where you don't need real-time validation or complex state management. They're useful for file inputs (always uncontrolled) and when integrating with non-React libraries.

**Q: "What are the advantages of controlled components?"**

**A:** Real-time validation, conditional logic, dynamic form fields, easier testing, and complete control over form state. They follow React's unidirectional data flow principle.

### 🎯 Synthetic Events Deep Dive

**Interview Critical Point:** React wraps native events in SyntheticEvent objects for cross-browser compatibility and consistent behavior.

```jsx
function EventExamples() {
  // Synthetic event provides cross-browser compatibility
  const handleClick = (e) => {
    console.log('SyntheticEvent:', e);
    console.log('Native event:', e.nativeEvent);
    console.log('Event type:', e.type);
    console.log('Target element:', e.target);
    console.log('Current target:', e.currentTarget);
    
    // Prevent default behavior
    e.preventDefault();
    
    // Stop event propagation
    e.stopPropagation();
  };
  
  const handleKeyDown = (e) => {
    console.log('Key pressed:', e.key);
    console.log('Key code:', e.keyCode); // Deprecated, use e.key
    console.log('Modifier keys:', {
      ctrl: e.ctrlKey,
      shift: e.shiftKey,
      alt: e.altKey,
      meta: e.metaKey
    });
    
    // Handle specific keys
    if (e.key === 'Enter') {
      console.log('Enter key pressed');
    }
    
    if (e.key === 'Escape') {
      console.log('Escape key pressed');
    }
  };
  
  const handleMouseEvent = (e) => {
    console.log('Mouse event:', {
      type: e.type,
      clientX: e.clientX,
      clientY: e.clientY,
      button: e.button, // 0: left, 1: middle, 2: right
      buttons: e.buttons // Bitmask of pressed buttons
    });
  };
  
  const handleFormEvent = (e) => {
    console.log('Form event:', e.type);
    console.log('Form data:', new FormData(e.target));
  };
  
  // Event delegation - handle multiple similar elements
  const handleListClick = (e) => {
    // Check if clicked element is a list item
    if (e.target.tagName === 'LI') {
      console.log('List item clicked:', e.target.textContent);
    }
  };
  
  return (
    <div>
      <button onClick={handleClick}>
        Click me (check console)
      </button>
      
      <input
        type="text"
        onKeyDown={handleKeyDown}
        placeholder="Type something..."
      />
      
      <div
        onMouseDown={handleMouseEvent}
        onMouseUp={handleMouseEvent}
        onMouseMove={handleMouseEvent}
        style={{ 
          width: 200, 
          height: 100, 
          border: '1px solid black',
          margin: '10px 0'
        }}
      >
        Mouse interaction area
      </div>
      
      <form onSubmit={handleFormEvent}>
        <input name="username" placeholder="Username" />
        <button type="submit">Submit</button>
      </form>
      
      {/* Event delegation example */}
      <ul onClick={handleListClick}>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
      </ul>
    </div>
  );
}

// Advanced: Custom event handling with useCallback
function OptimizedEventHandling() {
  const [items, setItems] = useState([
    { id: 1, name: 'Item 1' },
    { id: 2, name: 'Item 2' },
    { id: 3, name: 'Item 3' }
  ]);
  
  // Optimized event handler that doesn't recreate on every render
  const handleItemClick = useCallback((itemId) => {
    setItems(prevItems =>
      prevItems.map(item =>
        item.id === itemId
          ? { ...item, selected: !item.selected }
          : item
      )
    );
  }, []);
  
  // Event handler with preventDefault and stopPropagation
  const handleLinkClick = useCallback((e, url) => {
    e.preventDefault();
    e.stopPropagation();
    
    // Custom navigation logic
    console.log('Navigating to:', url);
    // window.history.pushState(null, '', url);
  }, []);
  
  return (
    <div>
      <h3>Optimized Event Handling</h3>
      
      {items.map(item => (
        <div
          key={item.id}
          onClick={() => handleItemClick(item.id)}
          style={{
            padding: '10px',
            backgroundColor: item.selected ? '#e0e0e0' : 'white',
            cursor: 'pointer'
          }}
        >
          {item.name} {item.selected ? '✓' : ''}
        </div>
      ))}
      
      <a
        href="/some-page"
        onClick={(e) => handleLinkClick(e, '/some-page')}
      >
        Custom Link Handler
      </a>
    </div>
  );
}
```

**Interview Questions & Answers:**

**Q: "What are synthetic events and why does React use them?"**

**A:** Synthetic events are React's cross-browser wrapper around native events. They provide consistent behavior across browsers, enable event pooling for performance, and offer additional features like automatic event delegation.

**Q: "How do you access the native event from a synthetic event?"**

**A:** Use `e.nativeEvent` to access the underlying native event object.

**Q: "What's the difference between `e.target` and `e.currentTarget`?"**

**A:** `e.target` is the element that triggered the event, while `e.currentTarget` is the element the event handler is attached to. Due to event bubbling, these can be different elements.

---

## Interview Questions You Should Master

### Q: Why can't you use hooks inside conditions or loops?
**A:** Hooks rely on call order to maintain state consistency between renders. React uses the order of hook calls to associate each hook with its corresponding state. Conditional hooks would break this order.

### Q: What's the difference between `useState` and `useRef`?
**A:** `useState` triggers re-renders when updated and is for component state. `useRef` doesn't trigger re-renders, persists values between renders, and is used for DOM access or storing mutable values.

### Q: How do you prevent unnecessary re-renders in React?
**A:** Use `React.memo` for components, `useMemo` for expensive calculations, `useCallback` for functions, and proper dependency arrays in `useEffect`.

### Q: Explain the component lifecycle in hooks terms.
**A:** Mount = `useEffect(() => {}, [])`, Update = `useEffect(() => {})` or with dependencies, Unmount = return function from `useEffect`.

### Q: When would you use `useReducer` instead of `useState`?
**A:** For complex state logic with multiple sub-values, when next state depends on previous state, or when you want predictable state transitions (like Redux pattern).
