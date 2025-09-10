# State Management Deep-Dive Guide

> **Interview Level:** Senior React Developer  
> **Focus:** State management patterns, Redux ecosystem, and architectural decisions  
> **Time Investment:** 15-20 hours of deep study and practice

This guide covers **state management** concepts that are extremely common in senior-level React interviews. Understanding when and how to use different state management solutions is crucial for system design questions.

---

## Table of Contents

1. [React State Fundamentals](#react-state-fundamentals)
2. [Context API Deep Dive](#context-api-deep-dive)
3. [Redux Architecture & Concepts](#redux-architecture--concepts)
4. [Redux Toolkit & Modern Redux](#redux-toolkit--modern-redux)
5. [Middleware: Thunk vs Saga](#middleware-thunk-vs-saga)
6. [Zustand: Lightweight State Management](#zustand-lightweight-state-management)
7. [MobX: Reactive State Management](#mobx-reactive-state-management)
8. [State Management Decision Matrix](#state-management-decision-matrix)
9. [Interview Questions & Scenarios](#interview-questions--scenarios)

---

## React State Fundamentals

> **Interview Expectation:** Deep understanding of React's built-in state mechanisms and when to use each pattern.

### 🎯 Local Component State

**Interview Critical Point:** Local state should be your first choice. Only lift state up when multiple components need access.

```jsx
import React, { useState, useEffect, useReducer, useCallback } from 'react';

// Simple local state example
function CounterComponent() {
  const [count, setCount] = useState(0);
  const [step, setStep] = useState(1);
  
  // Derived state (computed from other state)
  const isEven = count % 2 === 0;
  const canDecrement = count > 0;
  
  const increment = useCallback(() => {
    setCount(prev => prev + step);
  }, [step]);
  
  const decrement = useCallback(() => {
    setCount(prev => Math.max(0, prev - step));
  }, [step]);
  
  return (
    <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '4px' }}>
      <h3>Local State Example</h3>
      <div style={{ fontSize: '24px', marginBottom: '10px' }}>
        Count: {count} {isEven ? '(Even)' : '(Odd)'}
      </div>
      
      <div style={{ marginBottom: '15px' }}>
        <label>
          Step size: 
          <input 
            type="number" 
            value={step} 
            onChange={(e) => setStep(parseInt(e.target.value) || 1)}
            style={{ marginLeft: '10px', width: '60px' }}
          />
        </label>
      </div>
      
      <div>
        <button 
          onClick={increment}
          style={{ marginRight: '10px', padding: '8px 16px' }}
        >
          +{step}
        </button>
        <button 
          onClick={decrement}
          disabled={!canDecrement}
          style={{ padding: '8px 16px' }}
        >
          -{step}
        </button>
      </div>
    </div>
  );
}
```

### 🎯 useReducer for Complex State Logic

**Interview Critical Point:** useReducer is preferred when state updates are complex or involve multiple related values.

```jsx
// Complex state management with useReducer
const initialState = {
  todos: [],
  filter: 'all', // all, active, completed
  editingId: null,
  editingText: ''
};

function todoReducer(state, action) {
  switch (action.type) {
    case 'ADD_TODO':
      return {
        ...state,
        todos: [
          ...state.todos,
          {
            id: Date.now(),
            text: action.payload,
            completed: false,
            createdAt: new Date().toISOString()
          }
        ]
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
      
    case 'DELETE_TODO':
      return {
        ...state,
        todos: state.todos.filter(todo => todo.id !== action.payload)
      };
      
    case 'START_EDITING':
      const todoToEdit = state.todos.find(todo => todo.id === action.payload);
      return {
        ...state,
        editingId: action.payload,
        editingText: todoToEdit ? todoToEdit.text : ''
      };
      
    case 'UPDATE_EDITING_TEXT':
      return {
        ...state,
        editingText: action.payload
      };
      
    case 'SAVE_EDIT':
      return {
        ...state,
        todos: state.todos.map(todo =>
          todo.id === state.editingId
            ? { ...todo, text: state.editingText }
            : todo
        ),
        editingId: null,
        editingText: ''
      };
      
    case 'CANCEL_EDIT':
      return {
        ...state,
        editingId: null,
        editingText: ''
      };
      
    case 'SET_FILTER':
      return {
        ...state,
        filter: action.payload
      };
      
    case 'CLEAR_COMPLETED':
      return {
        ...state,
        todos: state.todos.filter(todo => !todo.completed)
      };
      
    default:
      return state;
  }
}

function TodoApp() {
  const [state, dispatch] = useReducer(todoReducer, initialState);
  const [newTodoText, setNewTodoText] = useState('');
  
  // Selectors (derived state)
  const filteredTodos = state.todos.filter(todo => {
    switch (state.filter) {
      case 'active':
        return !todo.completed;
      case 'completed':
        return todo.completed;
      default:
        return true;
    }
  });
  
  const stats = {
    total: state.todos.length,
    active: state.todos.filter(todo => !todo.completed).length,
    completed: state.todos.filter(todo => todo.completed).length
  };
  
  const addTodo = () => {
    if (newTodoText.trim()) {
      dispatch({ type: 'ADD_TODO', payload: newTodoText.trim() });
      setNewTodoText('');
    }
  };
  
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      addTodo();
    }
  };
  
  return (
    <div style={{ maxWidth: '500px', margin: '0 auto', padding: '20px' }}>
      <h3>useReducer Todo App</h3>
      
      {/* Add new todo */}
      <div style={{ marginBottom: '20px', display: 'flex' }}>
        <input
          type="text"
          value={newTodoText}
          onChange={(e) => setNewTodoText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Add a new todo..."
          style={{ 
            flex: 1, 
            padding: '8px', 
            marginRight: '10px',
            border: '1px solid #ddd',
            borderRadius: '4px'
          }}
        />
        <button 
          onClick={addTodo}
          disabled={!newTodoText.trim()}
          style={{ padding: '8px 16px' }}
        >
          Add
        </button>
      </div>
      
      {/* Stats */}
      <div style={{ 
        marginBottom: '20px', 
        padding: '10px', 
        backgroundColor: '#f8f9fa',
        borderRadius: '4px',
        display: 'flex',
        justifyContent: 'space-between'
      }}>
        <span>Total: {stats.total}</span>
        <span>Active: {stats.active}</span>
        <span>Completed: {stats.completed}</span>
      </div>
      
      {/* Filters */}
      <div style={{ marginBottom: '20px' }}>
        {['all', 'active', 'completed'].map(filter => (
          <button
            key={filter}
            onClick={() => dispatch({ type: 'SET_FILTER', payload: filter })}
            style={{
              marginRight: '10px',
              padding: '4px 12px',
              backgroundColor: state.filter === filter ? '#007bff' : '#f8f9fa',
              color: state.filter === filter ? 'white' : 'black',
              border: '1px solid #ddd',
              borderRadius: '4px',
              textTransform: 'capitalize'
            }}
          >
            {filter}
          </button>
        ))}
        
        {stats.completed > 0 && (
          <button
            onClick={() => dispatch({ type: 'CLEAR_COMPLETED' })}
            style={{ 
              padding: '4px 12px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px'
            }}
          >
            Clear Completed
          </button>
        )}
      </div>
      
      {/* Todo list */}
      <div>
        {filteredTodos.length === 0 ? (
          <div style={{ textAlign: 'center', color: '#666', padding: '20px' }}>
            {state.filter === 'all' ? 'No todos yet' : `No ${state.filter} todos`}
          </div>
        ) : (
          filteredTodos.map(todo => (
            <TodoItem 
              key={todo.id} 
              todo={todo} 
              dispatch={dispatch}
              isEditing={state.editingId === todo.id}
              editingText={state.editingText}
            />
          ))
        )}
      </div>
    </div>
  );
}

function TodoItem({ todo, dispatch, isEditing, editingText }) {
  if (isEditing) {
    return (
      <div style={{ 
        display: 'flex', 
        alignItems: 'center', 
        marginBottom: '8px',
        padding: '8px',
        border: '2px solid #007bff',
        borderRadius: '4px'
      }}>
        <input
          type="text"
          value={editingText}
          onChange={(e) => dispatch({ type: 'UPDATE_EDITING_TEXT', payload: e.target.value })}
          onKeyPress={(e) => {
            if (e.key === 'Enter') {
              dispatch({ type: 'SAVE_EDIT' });
            } else if (e.key === 'Escape') {
              dispatch({ type: 'CANCEL_EDIT' });
            }
          }}
          style={{ 
            flex: 1, 
            padding: '4px',
            border: '1px solid #ddd',
            borderRadius: '4px'
          }}
          autoFocus
        />
        <button 
          onClick={() => dispatch({ type: 'SAVE_EDIT' })}
          style={{ marginLeft: '8px', padding: '4px 8px', fontSize: '12px' }}
        >
          Save
        </button>
        <button 
          onClick={() => dispatch({ type: 'CANCEL_EDIT' })}
          style={{ marginLeft: '4px', padding: '4px 8px', fontSize: '12px' }}
        >
          Cancel
        </button>
      </div>
    );
  }
  
  return (
    <div style={{ 
      display: 'flex', 
      alignItems: 'center', 
      marginBottom: '8px',
      padding: '8px',
      border: '1px solid #ddd',
      borderRadius: '4px',
      backgroundColor: todo.completed ? '#f8f9fa' : 'white'
    }}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => dispatch({ type: 'TOGGLE_TODO', payload: todo.id })}
        style={{ marginRight: '10px' }}
      />
      <span 
        style={{ 
          flex: 1, 
          textDecoration: todo.completed ? 'line-through' : 'none',
          color: todo.completed ? '#666' : 'black'
        }}
        onDoubleClick={() => dispatch({ type: 'START_EDITING', payload: todo.id })}
      >
        {todo.text}
      </span>
      <button 
        onClick={() => dispatch({ type: 'START_EDITING', payload: todo.id })}
        style={{ marginLeft: '8px', padding: '4px 8px', fontSize: '12px' }}
      >
        Edit
      </button>
      <button 
        onClick={() => dispatch({ type: 'DELETE_TODO', payload: todo.id })}
        style={{ 
          marginLeft: '4px', 
          padding: '4px 8px', 
          fontSize: '12px',
          backgroundColor: '#dc3545',
          color: 'white',
          border: 'none',
          borderRadius: '4px'
        }}
      >
        Delete
      </button>
    </div>
  );
}
```

---

## Context API Deep Dive

> **Interview Expectation:** Understand Context patterns, performance implications, and when Context is the right choice.

### 🎯 Context Patterns & Performance

**Interview Critical Point:** Context re-renders all consumers when value changes. Split contexts and memoize values to optimize performance.

```jsx
// ❌ Problematic: Single large context
const AppContext = createContext();

function ProblematicProvider({ children }) {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(false);
  
  // This object is recreated on every render!
  const value = {
    user, setUser,
    theme, setTheme,
    notifications, setNotifications,
    loading, setLoading
  };
  
  return (
    <AppContext.Provider value={value}>
      {children}
    </AppContext.Provider>
  );
}

// ✅ Better: Split contexts by concern
const UserContext = createContext();
const ThemeContext = createContext();
const NotificationContext = createContext();
const LoadingContext = createContext();

// User context with optimized value
function UserProvider({ children }) {
  const [user, setUser] = useState(null);
  
  // Memoize the context value
  const value = useMemo(() => ({
    user,
    setUser,
    login: async (credentials) => {
      setLoading(true);
      try {
        const userData = await authService.login(credentials);
        setUser(userData);
      } catch (error) {
        console.error('Login failed:', error);
      } finally {
        setLoading(false);
      }
    },
    logout: () => {
      setUser(null);
      localStorage.removeItem('authToken');
    }
  }), [user]);
  
  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
}

// Theme context with system preference detection
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState(() => {
    // Initialize from localStorage or system preference
    const saved = localStorage.getItem('theme');
    if (saved) return saved;
    
    return window.matchMedia('(prefers-color-scheme: dark)').matches 
      ? 'dark' 
      : 'light';
  });
  
  useEffect(() => {
    localStorage.setItem('theme', theme);
    document.documentElement.setAttribute('data-theme', theme);
  }, [theme]);
  
  const value = useMemo(() => ({
    theme,
    setTheme,
    toggleTheme: () => setTheme(prev => prev === 'light' ? 'dark' : 'light'),
    isDark: theme === 'dark'
  }), [theme]);
  
  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
}

// Notification context with queue management
function NotificationProvider({ children }) {
  const [notifications, setNotifications] = useState([]);
  
  const addNotification = useCallback((message, type = 'info', duration = 5000) => {
    const id = Date.now() + Math.random();
    const notification = { id, message, type, timestamp: Date.now() };
    
    setNotifications(prev => [...prev, notification]);
    
    if (duration > 0) {
      setTimeout(() => {
        setNotifications(prev => prev.filter(n => n.id !== id));
      }, duration);
    }
  }, []);
  
  const removeNotification = useCallback((id) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  }, []);
  
  const clearAll = useCallback(() => {
    setNotifications([]);
  }, []);
  
  const value = useMemo(() => ({
    notifications,
    addNotification,
    removeNotification,
    clearAll,
    // Derived state
    hasNotifications: notifications.length > 0,
    unreadCount: notifications.filter(n => !n.read).length
  }), [notifications, addNotification, removeNotification, clearAll]);
  
  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
}

// Loading context for global loading states
function LoadingProvider({ children }) {
  const [loadingStates, setLoadingStates] = useState({});
  
  const setLoading = useCallback((key, isLoading) => {
    setLoadingStates(prev => ({
      ...prev,
      [key]: isLoading
    }));
  }, []);
  
  const value = useMemo(() => ({
    loadingStates,
    setLoading,
    isLoading: (key) => !!loadingStates[key],
    isAnyLoading: Object.values(loadingStates).some(Boolean)
  }), [loadingStates, setLoading]);
  
  return (
    <LoadingContext.Provider value={value}>
      {children}
    </LoadingContext.Provider>
  );
}

// Combined provider with proper composition
function AppProviders({ children }) {
  return (
    <UserProvider>
      <ThemeProvider>
        <NotificationProvider>
          <LoadingProvider>
            {children}
          </LoadingProvider>
        </NotificationProvider>
      </ThemeProvider>
    </UserProvider>
  );
}

// Custom hooks for each context
function useUser() {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within UserProvider');
  }
  return context;
}

function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within ThemeProvider');
  }
  return context;
}

function useNotifications() {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotifications must be used within NotificationProvider');
  }
  return context;
}

function useLoading() {
  const context = useContext(LoadingContext);
  if (!context) {
    throw new Error('useLoading must be used within LoadingProvider');
  }
  return context;
}
```

### 🎯 Context Performance Optimization Demo

```jsx
function ContextPerformanceDemo() {
  const [renderCounts, setRenderCounts] = useState({
    user: 0,
    theme: 0,
    notifications: 0,
    combined: 0
  });
  
  const trackRender = (component) => {
    setRenderCounts(prev => ({
      ...prev,
      [component]: prev[component] + 1
    }));
  };
  
  return (
    <div>
      <h3>Context Performance Comparison</h3>
      
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', 
        gap: '15px',
        marginBottom: '20px'
      }}>
        {Object.entries(renderCounts).map(([component, count]) => (
          <div key={component} style={{ 
            padding: '10px', 
            backgroundColor: '#f8f9fa', 
            borderRadius: '4px',
            textAlign: 'center'
          }}>
            <div style={{ fontSize: '18px', fontWeight: 'bold' }}>{count}</div>
            <div style={{ fontSize: '12px' }}>{component} renders</div>
          </div>
        ))}
      </div>
      
      <AppProviders>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
          <div>
            <h4>Optimized: Split Contexts</h4>
            <UserComponent onRender={() => trackRender('user')} />
            <ThemeComponent onRender={() => trackRender('theme')} />
            <NotificationComponent onRender={() => trackRender('notifications')} />
          </div>
          
          <div>
            <h4>Control Panel</h4>
            <ContextControls />
          </div>
        </div>
      </AppProviders>
    </div>
  );
}

function UserComponent({ onRender }) {
  const { user, login, logout } = useUser();
  
  useEffect(() => {
    onRender();
  });
  
  return (
    <div style={{ 
      padding: '15px', 
      border: '2px solid #28a745', 
      borderRadius: '4px', 
      marginBottom: '10px'
    }}>
      <h5>User Component</h5>
      <div>User: {user?.name || 'Not logged in'}</div>
      <button onClick={() => user ? logout() : login({ name: 'John Doe' })}>
        {user ? 'Logout' : 'Login'}
      </button>
    </div>
  );
}

function ThemeComponent({ onRender }) {
  const { theme, toggleTheme, isDark } = useTheme();
  
  useEffect(() => {
    onRender();
  });
  
  return (
    <div style={{ 
      padding: '15px', 
      border: '2px solid #007bff', 
      borderRadius: '4px', 
      marginBottom: '10px',
      backgroundColor: isDark ? '#343a40' : '#f8f9fa',
      color: isDark ? 'white' : 'black'
    }}>
      <h5>Theme Component</h5>
      <div>Current theme: {theme}</div>
      <button onClick={toggleTheme}>Toggle Theme</button>
    </div>
  );
}

function NotificationComponent({ onRender }) {
  const { notifications, addNotification, clearAll, hasNotifications } = useNotifications();
  
  useEffect(() => {
    onRender();
  });
  
  return (
    <div style={{ 
      padding: '15px', 
      border: '2px solid #ffc107', 
      borderRadius: '4px', 
      marginBottom: '10px'
    }}>
      <h5>Notification Component</h5>
      <div>Notifications: {notifications.length}</div>
      <button 
        onClick={() => addNotification('Test notification', 'info')}
        style={{ marginRight: '10px' }}
      >
        Add Notification
      </button>
      {hasNotifications && (
        <button onClick={clearAll}>Clear All</button>
      )}
    </div>
  );
}

function ContextControls() {
  const { user, login, logout } = useUser();
  const { theme, toggleTheme } = useTheme();
  const { addNotification } = useNotifications();
  
  return (
    <div style={{ padding: '15px', border: '1px solid #ddd', borderRadius: '4px' }}>
      <h5>Context Controls</h5>
      
      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => user ? logout() : login({ name: 'Jane Smith' })}>
          {user ? 'Switch User' : 'Login User'}
        </button>
      </div>
      
      <div style={{ marginBottom: '10px' }}>
        <button onClick={toggleTheme}>
          Switch to {theme === 'light' ? 'Dark' : 'Light'} Theme
        </button>
      </div>
      
      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => addNotification('Random notification', 'success')}>
          Add Random Notification
        </button>
      </div>
      
      <div style={{ fontSize: '12px', color: '#666' }}>
        Notice how each component only re-renders when its specific context changes!
      </div>
    </div>
  );
}

// Mock auth service
const authService = {
  login: async (credentials) => {
    await new Promise(resolve => setTimeout(resolve, 1000));
    return { name: credentials.name, id: Date.now() };
  }
};
```

---

## Redux Architecture & Concepts

> **Interview Expectation:** Deep understanding of Redux principles, data flow, and when Redux is the right choice.

### 🎯 Core Redux Concepts

**Interview Critical Point:** Redux follows unidirectional data flow: Action → Reducer → Store → View. The store is the single source of truth.

```jsx
// Traditional Redux setup (before Redux Toolkit)
import { createStore, combineReducers, applyMiddleware } from 'redux';
import { thunk } from 'redux-thunk';

// Action Types (constants prevent typos)
const USER_ACTIONS = {
  LOGIN_REQUEST: 'USER/LOGIN_REQUEST',
  LOGIN_SUCCESS: 'USER/LOGIN_SUCCESS',
  LOGIN_FAILURE: 'USER/LOGIN_FAILURE',
  LOGOUT: 'USER/LOGOUT',
  UPDATE_PROFILE: 'USER/UPDATE_PROFILE'
};

const TODO_ACTIONS = {
  ADD_TODO: 'TODO/ADD_TODO',
  TOGGLE_TODO: 'TODO/TOGGLE_TODO',
  DELETE_TODO: 'TODO/DELETE_TODO',
  SET_FILTER: 'TODO/SET_FILTER',
  LOAD_TODOS_REQUEST: 'TODO/LOAD_TODOS_REQUEST',
  LOAD_TODOS_SUCCESS: 'TODO/LOAD_TODOS_SUCCESS',
  LOAD_TODOS_FAILURE: 'TODO/LOAD_TODOS_FAILURE'
};

// Action Creators
const userActions = {
  loginRequest: () => ({ type: USER_ACTIONS.LOGIN_REQUEST }),
  
  loginSuccess: (user) => ({ 
    type: USER_ACTIONS.LOGIN_SUCCESS, 
    payload: user 
  }),
  
  loginFailure: (error) => ({ 
    type: USER_ACTIONS.LOGIN_FAILURE, 
    payload: error 
  }),
  
  logout: () => ({ type: USER_ACTIONS.LOGOUT }),
  
  updateProfile: (updates) => ({ 
    type: USER_ACTIONS.UPDATE_PROFILE, 
    payload: updates 
  }),
  
  // Thunk action creator for async operations
  login: (credentials) => async (dispatch, getState) => {
    dispatch(userActions.loginRequest());
    
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials)
      });
      
      if (!response.ok) {
        throw new Error('Login failed');
      }
      
      const user = await response.json();
      dispatch(userActions.loginSuccess(user));
      
      // Store token
      localStorage.setItem('authToken', user.token);
      
    } catch (error) {
      dispatch(userActions.loginFailure(error.message));
    }
  }
};

const todoActions = {
  addTodo: (text) => ({
    type: TODO_ACTIONS.ADD_TODO,
    payload: {
      id: Date.now(),
      text,
      completed: false,
      createdAt: new Date().toISOString()
    }
  }),
  
  toggleTodo: (id) => ({
    type: TODO_ACTIONS.TOGGLE_TODO,
    payload: id
  }),
  
  deleteTodo: (id) => ({
    type: TODO_ACTIONS.DELETE_TODO,
    payload: id
  }),
  
  setFilter: (filter) => ({
    type: TODO_ACTIONS.SET_FILTER,
    payload: filter
  }),
  
  loadTodos: () => async (dispatch) => {
    dispatch({ type: TODO_ACTIONS.LOAD_TODOS_REQUEST });
    
    try {
      const response = await fetch('/api/todos');
      const todos = await response.json();
      dispatch({ 
        type: TODO_ACTIONS.LOAD_TODOS_SUCCESS, 
        payload: todos 
      });
    } catch (error) {
      dispatch({ 
        type: TODO_ACTIONS.LOAD_TODOS_FAILURE, 
        payload: error.message 
      });
    }
  }
};

// Reducers
const initialUserState = {
  currentUser: null,
  isLoading: false,
  error: null,
  isAuthenticated: false
};

function userReducer(state = initialUserState, action) {
  switch (action.type) {
    case USER_ACTIONS.LOGIN_REQUEST:
      return {
        ...state,
        isLoading: true,
        error: null
      };
      
    case USER_ACTIONS.LOGIN_SUCCESS:
      return {
        ...state,
        currentUser: action.payload,
        isLoading: false,
        error: null,
        isAuthenticated: true
      };
      
    case USER_ACTIONS.LOGIN_FAILURE:
      return {
        ...state,
        currentUser: null,
        isLoading: false,
        error: action.payload,
        isAuthenticated: false
      };
      
    case USER_ACTIONS.LOGOUT:
      return {
        ...state,
        currentUser: null,
        isAuthenticated: false,
        error: null
      };
      
    case USER_ACTIONS.UPDATE_PROFILE:
      return {
        ...state,
        currentUser: {
          ...state.currentUser,
          ...action.payload
        }
      };
      
    default:
      return state;
  }
}

const initialTodoState = {
  items: [],
  filter: 'all',
  isLoading: false,
  error: null
};

function todoReducer(state = initialTodoState, action) {
  switch (action.type) {
    case TODO_ACTIONS.ADD_TODO:
      return {
        ...state,
        items: [...state.items, action.payload]
      };
      
    case TODO_ACTIONS.TOGGLE_TODO:
      return {
        ...state,
        items: state.items.map(todo =>
          todo.id === action.payload
            ? { ...todo, completed: !todo.completed }
            : todo
        )
      };
      
    case TODO_ACTIONS.DELETE_TODO:
      return {
        ...state,
        items: state.items.filter(todo => todo.id !== action.payload)
      };
      
    case TODO_ACTIONS.SET_FILTER:
      return {
        ...state,
        filter: action.payload
      };
      
    case TODO_ACTIONS.LOAD_TODOS_REQUEST:
      return {
        ...state,
        isLoading: true,
        error: null
      };
      
    case TODO_ACTIONS.LOAD_TODOS_SUCCESS:
      return {
        ...state,
        items: action.payload,
        isLoading: false,
        error: null
      };
      
    case TODO_ACTIONS.LOAD_TODOS_FAILURE:
      return {
        ...state,
        isLoading: false,
        error: action.payload
      };
      
    default:
      return state;
  }
}

// Root reducer
const rootReducer = combineReducers({
  user: userReducer,
  todos: todoReducer
});

// Store creation
const store = createStore(
  rootReducer,
  applyMiddleware(thunk)
);

// Selectors (functions that extract specific data from state)
const selectors = {
  // User selectors
  getCurrentUser: (state) => state.user.currentUser,
  isAuthenticated: (state) => state.user.isAuthenticated,
  isUserLoading: (state) => state.user.isLoading,
  getUserError: (state) => state.user.error,
  
  // Todo selectors
  getAllTodos: (state) => state.todos.items,
  getTodoFilter: (state) => state.todos.filter,
  isTodosLoading: (state) => state.todos.isLoading,
  getTodosError: (state) => state.todos.error,
  
  // Computed selectors
  getFilteredTodos: (state) => {
    const todos = selectors.getAllTodos(state);
    const filter = selectors.getTodoFilter(state);
    
    switch (filter) {
      case 'active':
        return todos.filter(todo => !todo.completed);
      case 'completed':
        return todos.filter(todo => todo.completed);
      default:
        return todos;
    }
  },
  
  getTodoStats: (state) => {
    const todos = selectors.getAllTodos(state);
    return {
      total: todos.length,
      active: todos.filter(todo => !todo.completed).length,
      completed: todos.filter(todo => todo.completed).length
    };
  }
};
```

### 🎯 Redux Data Flow Visualization

```jsx
function ReduxFlowDemo() {
  const [selectedStep, setSelectedStep] = useState(0);
  
  const flowSteps = [
    {
      title: "1. User Interaction",
      description: "User clicks a button or interacts with the UI",
      code: `// User clicks 'Add Todo' button
<button onClick={() => handleAddTodo('Learn Redux')}>
  Add Todo
</button>`,
      highlight: "UI Component"
    },
    {
      title: "2. Dispatch Action",
      description: "Component dispatches an action to the store",
      code: `// Component dispatches action
const handleAddTodo = (text) => {
  dispatch(todoActions.addTodo(text));
};

// Action creator returns action object
const addTodo = (text) => ({
  type: 'TODO/ADD_TODO',
  payload: { id: Date.now(), text, completed: false }
});`,
      highlight: "Action Creator"
    },
    {
      title: "3. Reducer Processes",
      description: "Reducer receives action and returns new state",
      code: `function todoReducer(state = initialState, action) {
  switch (action.type) {
    case 'TODO/ADD_TODO':
      return {
        ...state,
        items: [...state.items, action.payload]
      };
    default:
      return state;
  }
}`,
      highlight: "Reducer"
    },
    {
      title: "4. Store Updates",
      description: "Store updates with new state from reducer",
      code: `// Before: state.todos.items = []
// After:  state.todos.items = [{ id: 1, text: 'Learn Redux', completed: false }]

// Store notifies all subscribers of state change`,
      highlight: "Store"
    },
    {
      title: "5. Components Re-render",
      description: "Connected components re-render with new state",
      code: `// Component receives new state via useSelector
const todos = useSelector(state => state.todos.items);

// Component re-renders with updated todos
return (
  <ul>
    {todos.map(todo => <li key={todo.id}>{todo.text}</li>)}
  </ul>
);`,
      highlight: "UI Update"
    }
  ];
  
  return (
    <div style={{ maxWidth: '800px', margin: '0 auto' }}>
      <h3>Redux Data Flow</h3>
      
      {/* Step navigation */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        marginBottom: '30px',
        flexWrap: 'wrap',
        gap: '10px'
      }}>
        {flowSteps.map((step, index) => (
          <button
            key={index}
            onClick={() => setSelectedStep(index)}
            style={{
              padding: '8px 16px',
              backgroundColor: selectedStep === index ? '#007bff' : '#f8f9fa',
              color: selectedStep === index ? 'white' : 'black',
              border: '1px solid #ddd',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '12px',
              flex: '1',
              minWidth: '120px'
            }}
          >
            {step.title}
          </button>
        ))}
      </div>
      
      {/* Current step details */}
      <div style={{ 
        border: '2px solid #007bff', 
        borderRadius: '8px', 
        padding: '20px',
        backgroundColor: '#f8f9fa'
      }}>
        <h4 style={{ color: '#007bff', marginTop: 0 }}>
          {flowSteps[selectedStep].title}
        </h4>
        
        <p style={{ fontSize: '16px', marginBottom: '20px' }}>
          {flowSteps[selectedStep].description}
        </p>
        
        <div style={{ 
          backgroundColor: '#343a40', 
          color: '#f8f9fa', 
          padding: '15px', 
          borderRadius: '4px',
          fontSize: '14px',
          fontFamily: 'monospace',
          whiteSpace: 'pre-wrap',
          overflow: 'auto'
        }}>
          {flowSteps[selectedStep].code}
        </div>
        
        <div style={{ 
          marginTop: '15px', 
          padding: '10px', 
          backgroundColor: '#d4edda',
          borderRadius: '4px',
          fontSize: '14px',
          fontWeight: 'bold',
          textAlign: 'center'
        }}>
          Focus: {flowSteps[selectedStep].highlight}
        </div>
      </div>
      
      {/* Navigation buttons */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        marginTop: '20px' 
      }}>
        <button
          onClick={() => setSelectedStep(Math.max(0, selectedStep - 1))}
          disabled={selectedStep === 0}
          style={{ 
            padding: '8px 16px',
            backgroundColor: selectedStep === 0 ? '#e9ecef' : '#007bff',
            color: selectedStep === 0 ? '#6c757d' : 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: selectedStep === 0 ? 'not-allowed' : 'pointer'
          }}
        >
          Previous
        </button>
        
        <span style={{ 
          padding: '8px 16px', 
          backgroundColor: '#e9ecef', 
          borderRadius: '4px' 
        }}>
          Step {selectedStep + 1} of {flowSteps.length}
        </span>
        
        <button
          onClick={() => setSelectedStep(Math.min(flowSteps.length - 1, selectedStep + 1))}
          disabled={selectedStep === flowSteps.length - 1}
          style={{ 
            padding: '8px 16px',
            backgroundColor: selectedStep === flowSteps.length - 1 ? '#e9ecef' : '#007bff',
            color: selectedStep === flowSteps.length - 1 ? '#6c757d' : 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: selectedStep === flowSteps.length - 1 ? 'not-allowed' : 'pointer'
          }}
        >
          Next
        </button>
      </div>
    </div>
  );
}
```

---

## Redux Toolkit & Modern Redux

> **Interview Expectation:** Understand Redux Toolkit's benefits, RTK Query, and how it simplifies Redux development.

### 🎯 Redux Toolkit Fundamentals

**Interview Critical Point:** Redux Toolkit eliminates boilerplate, includes Immer for immutable updates, and provides opinionated defaults.

```jsx
import { createSlice, configureStore, createAsyncThunk, createSelector } from '@reduxjs/toolkit';

// Async thunk for API calls
export const fetchTodos = createAsyncThunk(
  'todos/fetchTodos',
  async (userId, { rejectWithValue }) => {
    try {
      const response = await fetch(`/api/users/${userId}/todos`);
      if (!response.ok) {
        throw new Error('Failed to fetch todos');
      }
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

export const addTodo = createAsyncThunk(
  'todos/addTodo',
  async (todoData, { getState, rejectWithValue }) => {
    try {
      const state = getState();
      const response = await fetch('/api/todos', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${state.user.token}`
        },
        body: JSON.stringify(todoData)
      });
      
      if (!response.ok) {
        throw new Error('Failed to add todo');
      }
      
      return await response.json();
    } catch (error) {
      return rejectWithValue(error.message);
    }
  }
);

// Redux Toolkit slice (combines actions, reducers, and action creators)
const todosSlice = createSlice({
  name: 'todos',
  initialState: {
    items: [],
    filter: 'all',
    loading: false,
    error: null,
    lastFetch: null
  },
  reducers: {
    // Regular reducers for synchronous actions
    todoToggled: (state, action) => {
      // Immer allows "mutative" logic that's actually immutable
      const todo = state.items.find(todo => todo.id === action.payload);
      if (todo) {
        todo.completed = !todo.completed;
        todo.updatedAt = new Date().toISOString();
      }
    },
    
    todoDeleted: (state, action) => {
      state.items = state.items.filter(todo => todo.id !== action.payload);
    },
    
    filterChanged: (state, action) => {
      state.filter = action.payload;
    },
    
    todoTextUpdated: (state, action) => {
      const { id, text } = action.payload;
      const todo = state.items.find(todo => todo.id === id);
      if (todo) {
        todo.text = text;
        todo.updatedAt = new Date().toISOString();
      }
    },
    
    allTodosCleared: (state) => {
      state.items = [];
    },
    
    completedTodosCleared: (state) => {
      state.items = state.items.filter(todo => !todo.completed);
    }
  },
  extraReducers: (builder) => {
    // Handle async actions
    builder
      .addCase(fetchTodos.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTodos.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
        state.lastFetch = new Date().toISOString();
      })
      .addCase(fetchTodos.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      .addCase(addTodo.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(addTodo.fulfilled, (state, action) => {
        state.loading = false;
        state.items.push(action.payload);
      })
      .addCase(addTodo.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  }
});

// Export actions (automatically generated)
export const { 
  todoToggled, 
  todoDeleted, 
  filterChanged, 
  todoTextUpdated,
  allTodosCleared,
  completedTodosCleared 
} = todosSlice.actions;

// User slice with authentication
const userSlice = createSlice({
  name: 'user',
  initialState: {
    currentUser: null,
    token: localStorage.getItem('authToken'),
    loading: false,
    error: null
  },
  reducers: {
    loginStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    loginSuccess: (state, action) => {
      state.loading = false;
      state.currentUser = action.payload.user;
      state.token = action.payload.token;
      localStorage.setItem('authToken', action.payload.token);
    },
    loginFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
      state.currentUser = null;
      state.token = null;
      localStorage.removeItem('authToken');
    },
    logout: (state) => {
      state.currentUser = null;
      state.token = null;
      localStorage.removeItem('authToken');
    },
    profileUpdated: (state, action) => {
      if (state.currentUser) {
        Object.assign(state.currentUser, action.payload);
      }
    }
  }
});

export const { loginStart, loginSuccess, loginFailure, logout, profileUpdated } = userSlice.actions;

// Configure store with Redux Toolkit
const store = configureStore({
  reducer: {
    todos: todosSlice.reducer,
    user: userSlice.reducer
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE']
      }
    }),
  devTools: process.env.NODE_ENV !== 'production'
});

// Selectors with createSelector for memoization
export const selectTodos = createSelector(
  [(state) => state.todos.items, (state) => state.todos.filter],
  (todos, filter) => {
    switch (filter) {
      case 'active':
        return todos.filter(todo => !todo.completed);
      case 'completed':
        return todos.filter(todo => todo.completed);
      default:
        return todos;
    }
  }
);

export const selectTodoStats = createSelector(
  [(state) => state.todos.items],
  (todos) => ({
    total: todos.length,
    active: todos.filter(todo => !todo.completed).length,
    completed: todos.filter(todo => todo.completed).length,
    completionRate: todos.length > 0 ? 
      (todos.filter(todo => todo.completed).length / todos.length * 100).toFixed(1) : 0
  })
);

export const selectUserInfo = createSelector(
  [(state) => state.user],
  (user) => ({
    isAuthenticated: !!user.token && !!user.currentUser,
    username: user.currentUser?.name || 'Guest',
    role: user.currentUser?.role || 'user',
    isLoading: user.loading
  })
);
```

### 🎯 RTK Query for API Management

**Interview Critical Point:** RTK Query eliminates the need for writing thunks and managing loading states manually.

```jsx
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react';

// Define API slice
export const todosApi = createApi({
  reducerPath: 'todosApi',
  baseQuery: fetchBaseQuery({
    baseUrl: '/api/',
    prepareHeaders: (headers, { getState }) => {
      const token = getState().user.token;
      if (token) {
        headers.set('authorization', `Bearer ${token}`);
      }
      return headers;
    },
  }),
  tagTypes: ['Todo', 'User'],
  endpoints: (builder) => ({
    // Queries (for fetching data)
    getTodos: builder.query({
      query: (userId) => `users/${userId}/todos`,
      providesTags: (result) =>
        result
          ? [
              ...result.map(({ id }) => ({ type: 'Todo', id })),
              { type: 'Todo', id: 'LIST' },
            ]
          : [{ type: 'Todo', id: 'LIST' }],
    }),
    
    getTodoById: builder.query({
      query: (id) => `todos/${id}`,
      providesTags: (result, error, id) => [{ type: 'Todo', id }],
    }),
    
    // Mutations (for modifying data)
    addTodo: builder.mutation({
      query: (newTodo) => ({
        url: 'todos',
        method: 'POST',
        body: newTodo,
      }),
      invalidatesTags: [{ type: 'Todo', id: 'LIST' }],
    }),
    
    updateTodo: builder.mutation({
      query: ({ id, ...patch }) => ({
        url: `todos/${id}`,
        method: 'PATCH',
        body: patch,
      }),
      invalidatesTags: (result, error, { id }) => [{ type: 'Todo', id }],
    }),
    
    deleteTodo: builder.mutation({
      query: (id) => ({
        url: `todos/${id}`,
        method: 'DELETE',
      }),
      invalidatesTags: (result, error, id) => [{ type: 'Todo', id }],
    }),
  }),
});

// Export hooks for usage in functional components
export const {
  useGetTodosQuery,
  useGetTodoByIdQuery,
  useAddTodoMutation,
  useUpdateTodoMutation,
  useDeleteTodoMutation,
} = todosApi;

// RTK Query component example
function RTKTodoList({ userId }) {
  const {
    data: todos,
    error,
    isLoading,
    isFetching,
    refetch
  } = useGetTodosQuery(userId, {
    pollingInterval: 30000, // Poll every 30 seconds
    refetchOnMountOrArgChange: true,
    refetchOnFocus: true,
  });

  const [addTodo, { isLoading: isAdding }] = useAddTodoMutation();
  const [updateTodo] = useUpdateTodoMutation();
  const [deleteTodo] = useDeleteTodoMutation();

  const [newTodoText, setNewTodoText] = useState('');

  const handleAddTodo = async () => {
    if (newTodoText.trim()) {
      try {
        await addTodo({
          text: newTodoText,
          userId,
          completed: false
        }).unwrap();
        setNewTodoText('');
      } catch (error) {
        console.error('Failed to add todo:', error);
      }
    }
  };

  const handleToggleTodo = async (todo) => {
    try {
      await updateTodo({
        id: todo.id,
        completed: !todo.completed
      }).unwrap();
    } catch (error) {
      console.error('Failed to update todo:', error);
    }
  };

  const handleDeleteTodo = async (id) => {
    try {
      await deleteTodo(id).unwrap();
    } catch (error) {
      console.error('Failed to delete todo:', error);
    }
  };

  if (isLoading) return <div>Loading todos...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div>
      <h3>RTK Query Todo List</h3>
      
      {/* Add new todo */}
      <div style={{ marginBottom: '20px', display: 'flex' }}>
        <input
          type="text"
          value={newTodoText}
          onChange={(e) => setNewTodoText(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleAddTodo()}
          placeholder="Add a new todo..."
          style={{ flex: 1, padding: '8px', marginRight: '10px' }}
        />
        <button 
          onClick={handleAddTodo}
          disabled={isAdding || !newTodoText.trim()}
          style={{ padding: '8px 16px' }}
        >
          {isAdding ? 'Adding...' : 'Add'}
        </button>
      </div>

      {/* Refresh controls */}
      <div style={{ marginBottom: '15px' }}>
        <button 
          onClick={refetch}
          disabled={isFetching}
          style={{ marginRight: '10px', padding: '4px 12px' }}
        >
          {isFetching ? 'Refreshing...' : 'Refresh'}
        </button>
        <span style={{ fontSize: '12px', color: '#666' }}>
          {isFetching && 'Updating data...'}
        </span>
      </div>

      {/* Todo list */}
      <div>
        {todos?.length === 0 ? (
          <div style={{ textAlign: 'center', color: '#666', padding: '20px' }}>
            No todos found. Add one above!
          </div>
        ) : (
          todos?.map(todo => (
            <div 
              key={todo.id} 
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                padding: '8px',
                marginBottom: '8px',
                border: '1px solid #ddd',
                borderRadius: '4px',
                backgroundColor: todo.completed ? '#f8f9fa' : 'white'
              }}
            >
              <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => handleToggleTodo(todo)}
                style={{ marginRight: '10px' }}
              />
              <span 
                style={{ 
                  flex: 1, 
                  textDecoration: todo.completed ? 'line-through' : 'none',
                  color: todo.completed ? '#666' : 'black'
                }}
              >
                {todo.text}
              </span>
              <button 
                onClick={() => handleDeleteTodo(todo.id)}
                style={{ 
                  padding: '4px 8px', 
                  backgroundColor: '#dc3545', 
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px'
                }}
              >
                Delete
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

// Store configuration with RTK Query
const storeWithRTK = configureStore({
  reducer: {
    todos: todosSlice.reducer,
    user: userSlice.reducer,
    todosApi: todosApi.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(todosApi.middleware),
});
```

---

## Middleware: Thunk vs Saga

> **Interview Expectation:** Understand different middleware options for handling async operations and side effects.

### 🎯 Redux Thunk

**Interview Critical Point:** Thunk allows action creators to return functions instead of plain objects, enabling async operations.

```jsx
// Thunk middleware examples
const thunkActions = {
  // Simple async thunk
  fetchUserProfile: (userId) => async (dispatch, getState) => {
    dispatch({ type: 'USER_PROFILE_REQUEST' });
    
    try {
      const response = await fetch(`/api/users/${userId}`);
      const user = await response.json();
      
      dispatch({ 
        type: 'USER_PROFILE_SUCCESS', 
        payload: user 
      });
      
      // Can dispatch multiple actions
      dispatch({ 
        type: 'LAST_FETCH_TIME_UPDATED', 
        payload: Date.now() 
      });
      
    } catch (error) {
      dispatch({ 
        type: 'USER_PROFILE_FAILURE', 
        payload: error.message 
      });
    }
  },

  // Complex thunk with conditional logic
  smartFetchTodos: () => async (dispatch, getState) => {
    const state = getState();
    const { todos, user } = state;
    
    // Check if data is fresh (less than 5 minutes old)
    const fiveMinutesAgo = Date.now() - 5 * 60 * 1000;
    if (todos.lastFetch && todos.lastFetch > fiveMinutesAgo) {
      console.log('Data is fresh, skipping fetch');
      return;
    }
    
    // Check if user is authenticated
    if (!user.token) {
      dispatch({ 
        type: 'FETCH_ERROR', 
        payload: 'User not authenticated' 
      });
      return;
    }
    
    dispatch({ type: 'TODOS_FETCH_START' });
    
    try {
      const response = await fetch('/api/todos', {
        headers: {
          'Authorization': `Bearer ${user.token}`
        }
      });
      
      if (response.status === 401) {
        // Token expired, redirect to login
        dispatch({ type: 'AUTH_TOKEN_EXPIRED' });
        dispatch({ type: 'LOGOUT' });
        return;
      }
      
      const todos = await response.json();
      
      dispatch({ 
        type: 'TODOS_FETCH_SUCCESS', 
        payload: todos 
      });
      
      // Update fetch timestamp
      dispatch({ 
        type: 'TODOS_LAST_FETCH_UPDATED', 
        payload: Date.now() 
      });
      
    } catch (error) {
      dispatch({ 
        type: 'TODOS_FETCH_FAILURE', 
        payload: error.message 
      });
    }
  },

  // Thunk with retry logic
  fetchWithRetry: (url, maxRetries = 3) => async (dispatch) => {
    let retryCount = 0;
    
    const attemptFetch = async () => {
      try {
        dispatch({ 
          type: 'FETCH_ATTEMPT', 
          payload: { url, attempt: retryCount + 1 } 
        });
        
        const response = await fetch(url);
        
        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        
        const data = await response.json();
        
        dispatch({ 
          type: 'FETCH_SUCCESS', 
          payload: data 
        });
        
      } catch (error) {
        retryCount++;
        
        if (retryCount <= maxRetries) {
          console.log(`Retry ${retryCount}/${maxRetries} in 2 seconds...`);
          
          setTimeout(() => {
            attemptFetch();
          }, 2000 * retryCount); // Exponential backoff
          
        } else {
          dispatch({ 
            type: 'FETCH_FAILURE', 
            payload: `Failed after ${maxRetries} retries: ${error.message}` 
          });
        }
      }
    };
    
    await attemptFetch();
  }
};
```

### 🎯 Redux Saga

**Interview Critical Point:** Saga uses generator functions for complex async flows, cancellation, and testing.

```jsx
// Redux Saga examples
import { 
  call, 
  put, 
  take, 
  takeEvery, 
  takeLatest, 
  select, 
  fork, 
  cancel, 
  delay,
  race,
  all
} from 'redux-saga/effects';

// API functions
const api = {
  fetchUser: (id) => fetch(`/api/users/${id}`).then(res => res.json()),
  fetchTodos: () => fetch('/api/todos').then(res => res.json()),
  login: (credentials) => fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(credentials)
  }).then(res => res.json())
};

// Basic saga
function* fetchUserSaga(action) {
  try {
    yield put({ type: 'USER_FETCH_REQUEST' });
    
    // call() is used for calling functions
    const user = yield call(api.fetchUser, action.payload.userId);
    
    // put() is used for dispatching actions
    yield put({ 
      type: 'USER_FETCH_SUCCESS', 
      payload: user 
    });
    
  } catch (error) {
    yield put({ 
      type: 'USER_FETCH_FAILURE', 
      payload: error.message 
    });
  }
}

// Saga with timeout and cancellation
function* fetchTodosWithTimeoutSaga() {
  try {
    yield put({ type: 'TODOS_FETCH_REQUEST' });
    
    // Race between fetch and timeout
    const { response, timeout } = yield race({
      response: call(api.fetchTodos),
      timeout: delay(5000) // 5 second timeout
    });
    
    if (timeout) {
      yield put({ 
        type: 'TODOS_FETCH_FAILURE', 
        payload: 'Request timed out' 
      });
    } else {
      yield put({ 
        type: 'TODOS_FETCH_SUCCESS', 
        payload: response 
      });
    }
    
  } catch (error) {
    yield put({ 
      type: 'TODOS_FETCH_FAILURE', 
      payload: error.message 
    });
  }
}

// Login flow with automatic logout
function* loginFlowSaga() {
  while (true) {
    try {
      // Wait for login action
      const { credentials } = yield take('LOGIN_REQUEST');
      
      yield put({ type: 'LOGIN_PENDING' });
      
      // Attempt login
      const response = yield call(api.login, credentials);
      
      if (response.success) {
        yield put({ 
          type: 'LOGIN_SUCCESS', 
          payload: response.user 
        });
        
        // Start session monitoring
        const sessionTask = yield fork(sessionMonitorSaga, response.token);
        
        // Wait for logout
        yield take('LOGOUT_REQUEST');
        
        // Cancel session monitoring
        yield cancel(sessionTask);
        
        yield put({ type: 'LOGOUT_SUCCESS' });
        
      } else {
        yield put({ 
          type: 'LOGIN_FAILURE', 
          payload: response.error 
        });
      }
      
    } catch (error) {
      yield put({ 
        type: 'LOGIN_FAILURE', 
        payload: error.message 
      });
    }
  }
}

// Session monitoring saga
function* sessionMonitorSaga(token) {
  while (true) {
    try {
      // Check session every 30 seconds
      yield delay(30000);
      
      const response = yield call(fetch, '/api/session/validate', {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (!response.ok) {
        yield put({ type: 'SESSION_EXPIRED' });
        yield put({ type: 'LOGOUT_REQUEST' });
        break;
      }
      
    } catch (error) {
      console.error('Session check failed:', error);
    }
  }
}

// Background sync saga
function* backgroundSyncSaga() {
  while (true) {
    try {
      // Get offline actions from state
      const offlineActions = yield select(state => state.offline.queue);
      
      if (offlineActions.length > 0) {
        yield put({ type: 'SYNC_START' });
        
        // Process each offline action
        for (const action of offlineActions) {
          try {
            yield call(processOfflineAction, action);
            yield put({ 
              type: 'SYNC_ACTION_SUCCESS', 
              payload: action.id 
            });
          } catch (error) {
            yield put({ 
              type: 'SYNC_ACTION_FAILURE', 
              payload: { id: action.id, error: error.message } 
            });
          }
        }
        
        yield put({ type: 'SYNC_COMPLETE' });
      }
      
      // Wait 60 seconds before next sync attempt
      yield delay(60000);
      
    } catch (error) {
      yield put({ 
        type: 'SYNC_ERROR', 
        payload: error.message 
      });
      yield delay(60000);
    }
  }
}

function* processOfflineAction(action) {
  switch (action.type) {
    case 'CREATE_TODO_OFFLINE':
      yield call(api.createTodo, action.payload);
      break;
    case 'UPDATE_TODO_OFFLINE':
      yield call(api.updateTodo, action.payload.id, action.payload.updates);
      break;
    case 'DELETE_TODO_OFFLINE':
      yield call(api.deleteTodo, action.payload.id);
      break;
    default:
      throw new Error(`Unknown offline action: ${action.type}`);
  }
}

// Root saga
function* rootSaga() {
  yield all([
    // Watch for specific actions
    takeEvery('FETCH_USER_REQUEST', fetchUserSaga),
    takeLatest('FETCH_TODOS_REQUEST', fetchTodosWithTimeoutSaga), // takeLatest cancels previous
    
    // Long-running sagas
    fork(loginFlowSaga),
    fork(backgroundSyncSaga),
  ]);
}

// Saga middleware comparison component
function MiddlewareComparison() {
  const [selectedMiddleware, setSelectedMiddleware] = useState('thunk');
  
  const middlewareOptions = {
    thunk: {
      name: 'Redux Thunk',
      pros: [
        'Simple to understand and use',
        'Small bundle size',
        'Good for basic async operations',
        'Widely adopted'
      ],
      cons: [
        'Limited control flow',
        'Difficult to test complex async logic',
        'No built-in cancellation',
        'Can become nested and hard to read'
      ],
      useCase: 'Simple async operations, API calls, small to medium apps'
    },
    saga: {
      name: 'Redux Saga',
      pros: [
        'Powerful control flow with generators',
        'Easy testing with declarative effects',
        'Built-in cancellation',
        'Great for complex async patterns'
      ],
      cons: [
        'Steeper learning curve',
        'Larger bundle size',
        'Generator syntax can be confusing',
        'Overkill for simple use cases'
      ],
      useCase: 'Complex async flows, background tasks, real-time apps'
    }
  };
  
  const currentOption = middlewareOptions[selectedMiddleware];
  
  return (
    <div>
      <h3>Redux Middleware Comparison</h3>
      
      <div style={{ marginBottom: '20px' }}>
        {Object.entries(middlewareOptions).map(([key, option]) => (
          <button
            key={key}
            onClick={() => setSelectedMiddleware(key)}
            style={{
              margin: '0 10px 10px 0',
              padding: '10px 20px',
              backgroundColor: selectedMiddleware === key ? '#007bff' : '#f8f9fa',
              color: selectedMiddleware === key ? 'white' : 'black',
              border: '1px solid #ddd',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            {option.name}
          </button>
        ))}
      </div>
      
      <div style={{ 
        padding: '20px', 
        border: '1px solid #ddd', 
        borderRadius: '4px',
        backgroundColor: '#f9f9f9'
      }}>
        <h4>{currentOption.name}</h4>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '20px', marginTop: '15px' }}>
          <div>
            <h5 style={{ color: '#28a745' }}>Pros:</h5>
            <ul style={{ margin: 0, paddingLeft: '20px' }}>
              {currentOption.pros.map((pro, index) => (
                <li key={index} style={{ marginBottom: '5px', fontSize: '14px' }}>{pro}</li>
              ))}
            </ul>
          </div>
          
          <div>
            <h5 style={{ color: '#dc3545' }}>Cons:</h5>
            <ul style={{ margin: 0, paddingLeft: '20px' }}>
              {currentOption.cons.map((con, index) => (
                <li key={index} style={{ marginBottom: '5px', fontSize: '14px' }}>{con}</li>
              ))}
            </ul>
          </div>
          
          <div>
            <h5 style={{ color: '#007bff' }}>Best Use Case:</h5>
            <p style={{ margin: 0, fontSize: '14px' }}>{currentOption.useCase}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MiddlewareComparison;
```

---

## Zustand: Lightweight State Management

> **Interview Expectation:** Understand Zustand as a modern alternative to Redux with less boilerplate.

### 🎯 Zustand Store Creation

**Interview Critical Point:** Zustand stores are simple functions that return state and actions, with built-in TypeScript support.

```jsx
import { create } from 'zustand';
import { devtools, persist, subscribeWithSelector } from 'zustand/middleware';
import { immer } from 'zustand/middleware/immer';

// Basic Zustand store
const useCounterStore = create((set, get) => ({
  // State
  count: 0,
  step: 1,
  
  // Actions
  increment: () => set((state) => ({ count: state.count + state.step })),
  decrement: () => set((state) => ({ count: state.count - state.step })),
  setStep: (step) => set({ step }),
  reset: () => set({ count: 0, step: 1 }),
  
  // Computed values (getters)
  get doubled() {
    return get().count * 2;
  },
  
  get isEven() {
    return get().count % 2 === 0;
  }
}));

// Advanced store with middleware
const useTodoStore = create(
  devtools(
    persist(
      subscribeWithSelector(
        immer((set, get) => ({
          // State
          todos: [],
          filter: 'all',
          loading: false,
          error: null,
          
          // Actions
          addTodo: (text) => set((state) => {
            state.todos.push({
              id: Date.now(),
              text,
              completed: false,
              createdAt: new Date().toISOString()
            });
          }),
          
          toggleTodo: (id) => set((state) => {
            const todo = state.todos.find(t => t.id === id);
            if (todo) {
              todo.completed = !todo.completed;
            }
          }),
          
          deleteTodo: (id) => set((state) => {
            state.todos = state.todos.filter(t => t.id !== id);
          }),
          
          updateTodo: (id, updates) => set((state) => {
            const todo = state.todos.find(t => t.id === id);
            if (todo) {
              Object.assign(todo, updates);
            }
          }),
          
          setFilter: (filter) => set({ filter }),
          
          clearCompleted: () => set((state) => {
            state.todos = state.todos.filter(t => !t.completed);
          }),
          
          // Async actions
          fetchTodos: async () => {
            set({ loading: true, error: null });
            
            try {
              const response = await fetch('/api/todos');
              const todos = await response.json();
              
              set({ todos, loading: false });
            } catch (error) {
              set({ error: error.message, loading: false });
            }
          },
          
          saveTodo: async (todo) => {
            set({ loading: true });
            
            try {
              const response = await fetch('/api/todos', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(todo)
              });
              
              const savedTodo = await response.json();
              
              set((state) => {
                state.todos.push(savedTodo);
                state.loading = false;
              });
              
            } catch (error) {
              set({ error: error.message, loading: false });
            }
          },
          
          // Computed selectors
          get filteredTodos() {
            const state = get();
            switch (state.filter) {
              case 'active':
                return state.todos.filter(t => !t.completed);
              case 'completed':
                return state.todos.filter(t => t.completed);
              default:
                return state.todos;
            }
          },
          
          get stats() {
            const todos = get().todos;
            return {
              total: todos.length,
              active: todos.filter(t => !t.completed).length,
              completed: todos.filter(t => t.completed).length
            };
          }
        }))
      ),
      {
        name: 'todo-storage', // localStorage key
        partialize: (state) => ({ 
          todos: state.todos, 
          filter: state.filter 
        }), // Only persist specific fields
      }
    ),
    {
      name: 'todo-store', // DevTools name
    }
  )
);

// Store slicing for performance
const useUserStore = create((set, get) => ({
  profile: null,
  preferences: {
    theme: 'light',
    language: 'en',
    notifications: true
  },
  
  setProfile: (profile) => set({ profile }),
  
  updatePreferences: (updates) => set((state) => ({
    preferences: { ...state.preferences, ...updates }
  })),
  
  toggleTheme: () => set((state) => ({
    preferences: {
      ...state.preferences,
      theme: state.preferences.theme === 'light' ? 'dark' : 'light'
    }
  }))
}));

// Zustand usage examples
function ZustandExample() {
  // Subscribe to entire store
  const { count, step, increment, decrement, setStep, reset, doubled, isEven } = useCounterStore();
  
  // Subscribe to specific slices (better performance)
  const todos = useTodoStore(state => state.todos);
  const filteredTodos = useTodoStore(state => state.filteredTodos);
  const stats = useTodoStore(state => state.stats);
  const filter = useTodoStore(state => state.filter);
  const { addTodo, toggleTodo, deleteTodo, setFilter, clearCompleted } = useTodoStore();
  
  const [newTodoText, setNewTodoText] = useState('');
  
  const handleAddTodo = () => {
    if (newTodoText.trim()) {
      addTodo(newTodoText.trim());
      setNewTodoText('');
    }
  };
  
  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h3>Zustand Example</h3>
      
      {/* Counter section */}
      <div style={{ 
        marginBottom: '30px', 
        padding: '20px', 
        border: '1px solid #ddd', 
        borderRadius: '4px' 
      }}>
        <h4>Counter Store</h4>
        <div style={{ fontSize: '24px', marginBottom: '10px' }}>
          Count: {count} (Doubled: {doubled}) {isEven ? '(Even)' : '(Odd)'}
        </div>
        
        <div style={{ marginBottom: '15px' }}>
          <label>
            Step size: 
            <input 
              type="number" 
              value={step} 
              onChange={(e) => setStep(parseInt(e.target.value) || 1)}
              style={{ marginLeft: '10px', width: '60px' }}
            />
          </label>
        </div>
        
        <div>
          <button onClick={increment} style={{ marginRight: '10px' }}>
            +{step}
          </button>
          <button onClick={decrement} style={{ marginRight: '10px' }}>
            -{step}
          </button>
          <button onClick={reset}>Reset</button>
        </div>
      </div>
      
      {/* Todo section */}
      <div style={{ 
        padding: '20px', 
        border: '1px solid #ddd', 
        borderRadius: '4px' 
      }}>
        <h4>Todo Store</h4>
        
        {/* Stats */}
        <div style={{ 
          marginBottom: '20px', 
          padding: '10px', 
          backgroundColor: '#f8f9fa',
          borderRadius: '4px',
          display: 'flex',
          justifyContent: 'space-between'
        }}>
          <span>Total: {stats.total}</span>
          <span>Active: {stats.active}</span>
          <span>Completed: {stats.completed}</span>
        </div>
        
        {/* Add todo */}
        <div style={{ marginBottom: '20px', display: 'flex' }}>
          <input
            type="text"
            value={newTodoText}
            onChange={(e) => setNewTodoText(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleAddTodo()}
            placeholder="Add a new todo..."
            style={{ flex: 1, padding: '8px', marginRight: '10px' }}
          />
          <button onClick={handleAddTodo} disabled={!newTodoText.trim()}>
            Add
          </button>
        </div>
        
        {/* Filters */}
        <div style={{ marginBottom: '20px' }}>
          {['all', 'active', 'completed'].map(f => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              style={{
                marginRight: '10px',
                padding: '4px 12px',
                backgroundColor: filter === f ? '#007bff' : '#f8f9fa',
                color: filter === f ? 'white' : 'black',
                border: '1px solid #ddd',
                borderRadius: '4px',
                textTransform: 'capitalize'
              }}
            >
              {f}
            </button>
          ))}
          
          {stats.completed > 0 && (
            <button
              onClick={clearCompleted}
              style={{ 
                padding: '4px 12px',
                backgroundColor: '#dc3545',
                color: 'white',
                border: 'none',
                borderRadius: '4px'
              }}
            >
              Clear Completed
            </button>
          )}
        </div>
        
        {/* Todo list */}
        <div>
          {filteredTodos.length === 0 ? (
            <div style={{ textAlign: 'center', color: '#666', padding: '20px' }}>
              {filter === 'all' ? 'No todos yet' : `No ${filter} todos`}
            </div>
          ) : (
            filteredTodos.map(todo => (
              <div 
                key={todo.id} 
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  marginBottom: '8px',
                  padding: '8px',
                  border: '1px solid #ddd',
                  borderRadius: '4px',
                  backgroundColor: todo.completed ? '#f8f9fa' : 'white'
                }}
              >
                <input
                  type="checkbox"
                  checked={todo.completed}
                  onChange={() => toggleTodo(todo.id)}
                  style={{ marginRight: '10px' }}
                />
                <span 
                  style={{ 
                    flex: 1, 
                    textDecoration: todo.completed ? 'line-through' : 'none',
                    color: todo.completed ? '#666' : 'black'
                  }}
                >
                  {todo.text}
                </span>
                <button 
                  onClick={() => deleteTodo(todo.id)}
                  style={{ 
                    padding: '4px 8px', 
                    backgroundColor: '#dc3545', 
                    color: 'white',
                    border: 'none',
                    borderRadius: '4px'
                  }}
                >
                  Delete
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}

// Store subscription example
function ZustandSubscriptions() {
  const [logs, setLogs] = useState([]);
  
  useEffect(() => {
    // Subscribe to count changes only
    const unsubscribeCount = useCounterStore.subscribe(
      (state) => state.count,
      (count, prevCount) => {
        setLogs(prev => [...prev, `Count changed: ${prevCount} → ${count}`]);
      }
    );
    
    // Subscribe to todo additions
    const unsubscribeTodos = useTodoStore.subscribe(
      (state) => state.todos.length,
      (length, prevLength) => {
        if (length > prevLength) {
          setLogs(prev => [...prev, `Todo added. Total: ${length}`]);
        } else if (length < prevLength) {
          setLogs(prev => [...prev, `Todo deleted. Total: ${length}`]);
        }
      }
    );
    
    return () => {
      unsubscribeCount();
      unsubscribeTodos();
    };
  }, []);
  
  return (
    <div style={{ marginTop: '20px', padding: '15px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
      <h5>Store Subscriptions</h5>
      <div style={{ maxHeight: '200px', overflow: 'auto' }}>
        {logs.length === 0 ? (
          <div style={{ color: '#666' }}>No changes yet...</div>
        ) : (
          logs.map((log, index) => (
            <div key={index} style={{ fontSize: '12px', marginBottom: '4px' }}>
              {new Date().toLocaleTimeString()}: {log}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export { ZustandExample, ZustandSubscriptions };
```

---

## MobX: Reactive State Management

> **Interview Expectation:** Understand MobX's reactive programming model and how it compares to Redux.

### 🎯 MobX Store with Observables

**Interview Critical Point:** MobX uses observables and reactions to automatically track state changes.

```jsx
import { makeObservable, observable, action, computed, runInAction, reaction } from 'mobx';
import { observer } from 'mobx-react-lite';

// MobX Todo Store
class TodoStore {
  todos = [];
  filter = 'all';
  loading = false;
  error = null;

  constructor() {
    makeObservable(this, {
      // Observables (reactive state)
      todos: observable,
      filter: observable,
      loading: observable,
      error: observable,
      
      // Actions (methods that modify state)
      addTodo: action,
      toggleTodo: action,
      deleteTodo: action,
      updateTodo: action,
      setFilter: action,
      clearCompleted: action,
      setLoading: action,
      setError: action,
      
      // Computed (derived state)
      filteredTodos: computed,
      stats: computed,
      hasCompletedTodos: computed
    });
    
    // Reactions (side effects)
    this.setupReactions();
  }

  // Actions
  addTodo = (text) => {
    const todo = {
      id: Date.now(),
      text: text.trim(),
      completed: false,
      createdAt: new Date().toISOString()
    };
    this.todos.push(todo);
  };

  toggleTodo = (id) => {
    const todo = this.todos.find(t => t.id === id);
    if (todo) {
      todo.completed = !todo.completed;
    }
  };

  deleteTodo = (id) => {
    const index = this.todos.findIndex(t => t.id === id);
    if (index !== -1) {
      this.todos.splice(index, 1);
    }
  };

  updateTodo = (id, updates) => {
    const todo = this.todos.find(t => t.id === id);
    if (todo) {
      Object.assign(todo, updates);
    }
  };

  setFilter = (filter) => {
    this.filter = filter;
  };

  clearCompleted = () => {
    this.todos = this.todos.filter(t => !t.completed);
  };

  setLoading = (loading) => {
    this.loading = loading;
  };

  setError = (error) => {
    this.error = error;
  };

  // Async actions
  fetchTodos = async () => {
    this.setLoading(true);
    this.setError(null);

    try {
      const response = await fetch('/api/todos');
      const todos = await response.json();
      
      // Use runInAction for async state updates
      runInAction(() => {
        this.todos = todos;
        this.loading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error = error.message;
        this.loading = false;
      });
    }
  };

  saveTodo = async (todo) => {
    this.setLoading(true);

    try {
      const response = await fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(todo)
      });

      const savedTodo = await response.json();

      runInAction(() => {
        this.todos.push(savedTodo);
        this.loading = false;
      });
    } catch (error) {
      runInAction(() => {
        this.error = error.message;
        this.loading = false;
      });
    }
  };

  // Computed values (automatically recalculated when dependencies change)
  get filteredTodos() {
    switch (this.filter) {
      case 'active':
        return this.todos.filter(t => !t.completed);
      case 'completed':
        return this.todos.filter(t => t.completed);
      default:
        return this.todos;
    }
  }

  get stats() {
    return {
      total: this.todos.length,
      active: this.todos.filter(t => !t.completed).length,
      completed: this.todos.filter(t => t.completed).length
    };
  }

  get hasCompletedTodos() {
    return this.todos.some(t => t.completed);
  }

  // Reactions (side effects)
  setupReactions() {
    // Log when todos change
    reaction(
      () => this.todos.length,
      (length, reaction) => {
        console.log(`Todo count changed: ${length}`);
        
        // Save to localStorage
        localStorage.setItem('todos', JSON.stringify(this.todos));
      }
    );

    // Auto-save when todos change
    reaction(
      () => this.todos.map(t => ({ id: t.id, completed: t.completed, text: t.text })),
      (todos) => {
        // Debounced auto-save
        clearTimeout(this.autoSaveTimeout);
        this.autoSaveTimeout = setTimeout(() => {
          this.autoSave(todos);
        }, 1000);
      }
    );
  }

  autoSave = async (todos) => {
    try {
      await fetch('/api/todos/bulk-update', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(todos)
      });
      console.log('Todos auto-saved');
    } catch (error) {
      console.error('Auto-save failed:', error);
    }
  };
}

// Store instances
const todoStore = new TodoStore();

// MobX components (must be wrapped with observer)
const MobXTodoList = observer(() => {
  const [newTodoText, setNewTodoText] = useState('');

  const handleAddTodo = () => {
    if (newTodoText.trim()) {
      todoStore.addTodo(newTodoText);
      setNewTodoText('');
    }
  };

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h3>MobX Todo List</h3>

      {/* Stats - automatically updates when todos change */}
      <div style={{ 
        marginBottom: '20px', 
        padding: '10px', 
        backgroundColor: '#f8f9fa',
        borderRadius: '4px',
        display: 'flex',
        justifyContent: 'space-between'
      }}>
        <span>Total: {todoStore.stats.total}</span>
        <span>Active: {todoStore.stats.active}</span>
        <span>Completed: {todoStore.stats.completed}</span>
      </div>

      {/* Add todo */}
      <div style={{ marginBottom: '20px', display: 'flex' }}>
        <input
          type="text"
          value={newTodoText}
          onChange={(e) => setNewTodoText(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleAddTodo()}
          placeholder="Add a new todo..."
          style={{ flex: 1, padding: '8px', marginRight: '10px' }}
        />
        <button onClick={handleAddTodo} disabled={!newTodoText.trim()}>
          Add
        </button>
      </div>

      {/* Filters */}
      <div style={{ marginBottom: '20px' }}>
        {['all', 'active', 'completed'].map(f => (
          <button
            key={f}
            onClick={() => todoStore.setFilter(f)}
            style={{
              marginRight: '10px',
              padding: '4px 12px',
              backgroundColor: todoStore.filter === f ? '#007bff' : '#f8f9fa',
              color: todoStore.filter === f ? 'white' : 'black',
              border: '1px solid #ddd',
              borderRadius: '4px',
              textTransform: 'capitalize'
            }}
          >
            {f}
          </button>
        ))}
        
        {todoStore.hasCompletedTodos && (
          <button
            onClick={() => todoStore.clearCompleted()}
            style={{ 
              padding: '4px 12px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px'
            }}
          >
            Clear Completed
          </button>
        )}
      </div>

      {/* Todo list - filteredTodos automatically recalculates */}
      <div>
        {todoStore.filteredTodos.length === 0 ? (
          <div style={{ textAlign: 'center', color: '#666', padding: '20px' }}>
            {todoStore.filter === 'all' ? 'No todos yet' : `No ${todoStore.filter} todos`}
          </div>
        ) : (
          todoStore.filteredTodos.map(todo => (
            <TodoItem key={todo.id} todo={todo} />
          ))
        )}
      </div>
    </div>
  );
});

// Individual todo item component
const TodoItem = observer(({ todo }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(todo.text);

  const handleSave = () => {
    if (editText.trim()) {
      todoStore.updateTodo(todo.id, { text: editText.trim() });
      setIsEditing(false);
    }
  };

  const handleCancel = () => {
    setEditText(todo.text);
    setIsEditing(false);
  };

  return (
    <div 
      style={{ 
        display: 'flex', 
        alignItems: 'center', 
        marginBottom: '8px',
        padding: '8px',
        border: '1px solid #ddd',
        borderRadius: '4px',
        backgroundColor: todo.completed ? '#f8f9fa' : 'white'
      }}
    >
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => todoStore.toggleTodo(todo.id)}
        style={{ marginRight: '10px' }}
      />
      
      {isEditing ? (
        <>
          <input
            type="text"
            value={editText}
            onChange={(e) => setEditText(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') handleSave();
              if (e.key === 'Escape') handleCancel();
            }}
            style={{ flex: 1, marginRight: '10px', padding: '4px' }}
            autoFocus
          />
          <button 
            onClick={handleSave}
            style={{ marginRight: '5px', padding: '4px 8px' }}
          >
            Save
          </button>
          <button 
            onClick={handleCancel}
            style={{ marginRight: '10px', padding: '4px 8px' }}
          >
            Cancel
          </button>
        </>
      ) : (
        <>
          <span 
            style={{ 
              flex: 1, 
              textDecoration: todo.completed ? 'line-through' : 'none',
              color: todo.completed ? '#666' : 'black',
              cursor: 'pointer'
            }}
            onDoubleClick={() => setIsEditing(true)}
          >
            {todo.text}
          </span>
          <button 
            onClick={() => setIsEditing(true)}
            style={{ 
              marginRight: '5px', 
              padding: '4px 8px',
              backgroundColor: '#6c757d',
              color: 'white',
              border: 'none',
              borderRadius: '4px'
            }}
          >
            Edit
          </button>
        </>
      )}
      
      <button 
        onClick={() => todoStore.deleteTodo(todo.id)}
        style={{ 
          padding: '4px 8px', 
          backgroundColor: '#dc3545', 
          color: 'white',
          border: 'none',
          borderRadius: '4px'
        }}
      >
        Delete
      </button>
    </div>
  );
});

export { MobXTodoList, TodoItem, todoStore };
```

---

## State Management Decision Matrix

> **Interview Gold:** This matrix helps you choose the right state management approach based on project requirements.

### 🎯 Decision Framework

**Interview Critical Point:** The choice depends on complexity, team preference, performance needs, and long-term maintainability.

| Criteria | Local State | Context API | Redux | Zustand | MobX |
|----------|-------------|-------------|--------|---------|------|
| **Complexity** | Simple | Simple-Medium | High | Medium | Medium |
| **Learning Curve** | None | Low | High | Low | Medium |
| **Boilerplate** | None | Low | High | Low | Low |
| **Performance** | Excellent | Good* | Excellent | Good | Excellent |
| **DevTools** | Basic | Limited | Excellent | Good | Good |
| **Bundle Size** | 0KB | 0KB | ~15KB | ~3KB | ~20KB |
| **TypeScript** | Excellent | Good | Excellent | Excellent | Good |
| **Testing** | Easy | Easy | Excellent | Easy | Medium |
| **Time Travel** | No | No | Yes | No | Limited |
| **Middleware** | No | No | Excellent | Good | Limited |

*Context performance depends on implementation

### 🎯 When to Use Each Approach

```jsx
// Decision Tree Component
function StateManagementDecisionTree() {
  const [answers, setAnswers] = useState({});
  const [recommendation, setRecommendation] = useState(null);

  const questions = [
    {
      id: 'scope',
      question: 'What is the scope of your state?',
      options: [
        { value: 'component', label: 'Single component or small component tree' },
        { value: 'section', label: 'Section of the app (multiple related components)' },
        { value: 'global', label: 'Global app state (shared across many components)' }
      ]
    },
    {
      id: 'complexity',
      question: 'How complex is your state logic?',
      options: [
        { value: 'simple', label: 'Simple values (strings, numbers, booleans)' },
        { value: 'medium', label: 'Objects and arrays with some nesting' },
        { value: 'complex', label: 'Complex nested objects with relationships' }
      ]
    },
    {
      id: 'async',
      question: 'How much async logic do you have?',
      options: [
        { value: 'none', label: 'Little to no async operations' },
        { value: 'some', label: 'Some API calls and async operations' },
        { value: 'heavy', label: 'Heavy async operations, background sync, real-time data' }
      ]
    },
    {
      id: 'team',
      question: 'What is your team\'s experience level?',
      options: [
        { value: 'junior', label: 'Junior developers, prefer simplicity' },
        { value: 'mixed', label: 'Mixed experience levels' },
        { value: 'senior', label: 'Senior developers, comfortable with complexity' }
      ]
    },
    {
      id: 'debugging',
      question: 'How important is debugging capability?',
      options: [
        { value: 'basic', label: 'Basic debugging is sufficient' },
        { value: 'important', label: 'Good debugging tools are important' },
        { value: 'critical', label: 'Advanced debugging and time travel are critical' }
      ]
    }
  ];

  const getRecommendation = (answers) => {
    const { scope, complexity, async, team, debugging } = answers;

    // Local State
    if (scope === 'component' && complexity === 'simple') {
      return {
        primary: 'Local State (useState/useReducer)',
        reason: 'Perfect for component-level simple state',
        implementation: `
const [count, setCount] = useState(0);
const [user, setUser] = useState({ name: '', email: '' });

// For complex local state:
const [state, dispatch] = useReducer(reducer, initialState);`,
        alternatives: []
      };
    }

    // Context API
    if (scope === 'section' && complexity !== 'complex' && async !== 'heavy') {
      return {
        primary: 'Context API',
        reason: 'Great for medium-scope state without heavy async operations',
        implementation: `
const ThemeContext = createContext();

function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}`,
        alternatives: ['Zustand for less boilerplate', 'Local state if scope is smaller']
      };
    }

    // Redux
    if ((complexity === 'complex' || async === 'heavy' || debugging === 'critical') && team !== 'junior') {
      return {
        primary: 'Redux (with Redux Toolkit)',
        reason: 'Best for complex state, heavy async operations, and advanced debugging needs',
        implementation: `
const store = configureStore({
  reducer: {
    todos: todosSlice.reducer,
    user: userSlice.reducer
  }
});

const todosSlice = createSlice({
  name: 'todos',
  initialState: { items: [], loading: false },
  reducers: {
    todoAdded: (state, action) => {
      state.items.push(action.payload);
    }
  }
});`,
        alternatives: ['MobX for OOP preference', 'Zustand for simpler async needs']
      };
    }

    // Zustand
    if (scope === 'global' && team !== 'senior' && complexity !== 'complex') {
      return {
        primary: 'Zustand',
        reason: 'Perfect balance of simplicity and global state management',
        implementation: `
const useStore = create((set, get) => ({
  count: 0,
  increment: () => set(state => ({ count: state.count + 1 })),
  
  // Async action
  fetchData: async () => {
    const data = await api.fetchData();
    set({ data });
  }
}));`,
        alternatives: ['Context API for smaller scope', 'Redux for more complex needs']
      };
    }

    // MobX
    if (team === 'senior' && complexity === 'complex') {
      return {
        primary: 'MobX',
        reason: 'Excellent for complex state with reactive programming paradigm',
        implementation: `
class TodoStore {
  todos = [];
  
  constructor() {
    makeObservable(this, {
      todos: observable,
      addTodo: action,
      completedTodos: computed
    });
  }
  
  addTodo = (text) => {
    this.todos.push({ text, completed: false });
  };
  
  get completedTodos() {
    return this.todos.filter(t => t.completed);
  }
}`,
        alternatives: ['Redux for more predictable updates', 'Zustand for simpler syntax']
      };
    }

    // Default recommendation
    return {
      primary: 'Start with Local State, upgrade as needed',
      reason: 'Begin simple and add complexity only when necessary',
      implementation: 'Start with useState/useReducer, then consider Context API or Zustand',
      alternatives: ['Context API for shared state', 'Zustand for global state']
    };
  };

  useEffect(() => {
    if (Object.keys(answers).length === questions.length) {
      setRecommendation(getRecommendation(answers));
    }
  }, [answers]);

  const handleAnswer = (questionId, value) => {
    setAnswers(prev => ({ ...prev, [questionId]: value }));
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h3>State Management Decision Tree</h3>
      <p style={{ marginBottom: '30px', color: '#666' }}>
        Answer these questions to get a personalized recommendation for your project.
      </p>

      {questions.map((q, index) => (
        <div key={q.id} style={{ 
          marginBottom: '25px', 
          padding: '20px', 
          border: '1px solid #ddd', 
          borderRadius: '4px',
          backgroundColor: answers[q.id] ? '#f8f9fa' : 'white'
        }}>
          <h4 style={{ marginBottom: '15px' }}>
            {index + 1}. {q.question}
          </h4>
          
          {q.options.map(option => (
            <label 
              key={option.value} 
              style={{ 
                display: 'block', 
                marginBottom: '10px', 
                cursor: 'pointer',
                padding: '8px',
                borderRadius: '4px',
                backgroundColor: answers[q.id] === option.value ? '#007bff' : 'transparent',
                color: answers[q.id] === option.value ? 'white' : 'black'
              }}
            >
              <input
                type="radio"
                name={q.id}
                value={option.value}
                checked={answers[q.id] === option.value}
                onChange={() => handleAnswer(q.id, option.value)}
                style={{ marginRight: '10px' }}
              />
              {option.label}
            </label>
          ))}
        </div>
      ))}

      {recommendation && (
        <div style={{ 
          marginTop: '30px', 
          padding: '25px', 
          border: '2px solid #28a745', 
          borderRadius: '8px',
          backgroundColor: '#d4edda'
        }}>
          <h3 style={{ color: '#155724', marginBottom: '15px' }}>
            🎯 Recommendation: {recommendation.primary}
          </h3>
          
          <p style={{ marginBottom: '20px', fontSize: '16px' }}>
            <strong>Why:</strong> {recommendation.reason}
          </p>
          
          <h4 style={{ marginBottom: '10px' }}>Implementation Example:</h4>
          <pre style={{ 
            backgroundColor: '#f8f8f8', 
            padding: '15px', 
            borderRadius: '4px', 
            overflow: 'auto',
            fontSize: '12px',
            lineHeight: '1.4',
            marginBottom: '20px'
          }}>
            {recommendation.implementation}
          </pre>
          
          {recommendation.alternatives.length > 0 && (
            <div>
              <h4 style={{ marginBottom: '10px' }}>Alternative Options:</h4>
              <ul style={{ marginLeft: '20px' }}>
                {recommendation.alternatives.map((alt, index) => (
                  <li key={index} style={{ marginBottom: '5px' }}>{alt}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export { StateManagementDecisionTree };
```

---

## Interview Questions & Scenarios

> **Interview Mastery:** Real scenarios and questions asked in senior React interviews.

### 🎯 Technical Interview Questions

#### Q: "How would you design state management for a large e-commerce application?"

**Answer:**

```jsx
// Multi-layer state management architecture
const ecommerceStateArchitecture = {
  // User & Authentication (Redux)
  user: {
    profile: { id, name, email, preferences },
    authentication: { token, isAuthenticated, role },
    orders: [], // Order history
    management: 'Redux - complex auth flows, order tracking'
  },
  
  // Shopping Cart (Zustand - frequently changing)
  cart: {
    items: [{ productId, quantity, price, variant }],
    totals: { subtotal, tax, shipping, total },
    discounts: [],
    management: 'Zustand - simple but frequent updates'
  },
  
  // Product Catalog (RTK Query - server state)
  products: {
    categories: [],
    searchResults: [],
    productDetails: {},
    management: 'RTK Query - server state with caching'
  },
  
  // UI State (Context API)
  ui: {
    modals: { isCheckoutOpen, isLoginOpen },
    navigation: { currentPage, breadcrumbs },
    filters: { category, priceRange, rating },
    management: 'Context API - UI state that changes moderately'
  }
};

// Implementation strategy:
// 1. Redux for user state (complex flows, time travel debugging)
// 2. RTK Query for all server state (products, orders)
// 3. Zustand for cart (simple but frequent updates)
// 4. Context for UI state (moderate sharing, infrequent changes)
// 5. Local state for component-specific interactions
```

---

## Summary: State Management Mastery

### 🎯 Key Takeaways

You've mastered:

1. **React State Fundamentals** - useState, useReducer, state lifting patterns
2. **Context API Deep Dive** - Performance optimization, split contexts
3. **Redux Architecture** - Actions, reducers, store, data flow
4. **Redux Toolkit** - Modern Redux with less boilerplate, RTK Query
5. **Middleware Patterns** - Thunk vs Saga for async operations
6. **Zustand** - Lightweight state management alternative
7. **MobX** - Reactive programming with observables
8. **Decision Matrix** - When to use each approach
9. **Performance** - Optimization strategies and benchmarking
10. **Interview Scenarios** - Real-world architecture decisions

### 🎯 Interview Readiness

You can now:

- **Architect state management** for any application size
- **Choose the right tool** based on requirements
- **Optimize performance** and avoid common pitfalls
- **Explain trade-offs** clearly in technical discussions
- **Handle complex scenarios** like real-time collaboration

Remember: Start simple, add complexity only when needed. The best solution fits your specific requirements, team, and project constraints!

---

*This guide represents current best practices as of 2024. Continue learning and stay updated with the evolving React ecosystem!*
