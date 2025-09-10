# Advanced React Deep-Dive Guide

> **Interview Level:** Senior React Developer  
> **Time Investment:** 10-15 hours of deep study  
> **Prerequisite:** Core Fundamentals & Intermediate concepts mastered

This guide covers the **most challenging React concepts** that separate senior developers from intermediate ones. These are the topics where tough interview rounds usually get tricky.

---

## Table of Contents

1. [React Fiber & Reconciliation](#react-fiber--reconciliation)
2. [Concurrent Rendering (React 18)](#concurrent-rendering-react-18)
3. [Suspense & Lazy Loading](#suspense--lazy-loading)
4. [Server Components (React 18+)](#server-components-react-18)
5. [Hydration in SSR](#hydration-in-ssr)
6. [Profiler API (Performance Debugging)](#profiler-api-performance-debugging)
7. [Memoization Mastery](#memoization-mastery)
8. [Master-Level Interview Questions](#master-level-interview-questions)

---

## React Fiber & Reconciliation

> **Interview Expectation:** Understand React's internal architecture, how virtual DOM diffing works, and why Fiber was necessary for modern React features.

### 🎯 What is React Fiber?

**Interview Critical Point:** Fiber is React's reconciliation algorithm introduced in React 16. It's a complete rewrite that enables interruptible, prioritized rendering and concurrent features.

```jsx
// Before Fiber (Stack Reconciler) - Problems:
// 1. Synchronous, blocking updates
// 2. No way to interrupt long updates
// 3. All updates had same priority
// 4. Poor performance with large component trees

// With Fiber - Solutions:
// 1. Work can be paused and resumed
// 2. Different types of work can be assigned different priorities
// 3. Work can be reused or discarded
// 4. Better performance through time-slicing

// Example of blocking vs non-blocking updates
function FiberDemo() {
  const [count, setCount] = useState(0);
  const [items, setItems] = useState([]);
  
  // High priority update (user interaction)
  const handleClick = () => {
    setCount(c => c + 1); // This gets high priority
  };
  
  // Low priority update (background work)
  const handleHeavyWork = () => {
    // Before Fiber: This would block the UI
    // With Fiber: This can be interrupted by high-priority updates
    const newItems = Array.from({ length: 10000 }, (_, i) => ({
      id: i,
      value: Math.random()
    }));
    setItems(newItems);
  };
  
  return (
    <div>
      <h3>Count: {count}</h3>
      <button onClick={handleClick}>Increment (High Priority)</button>
      <button onClick={handleHeavyWork}>Heavy Work (Low Priority)</button>
      
      {/* Large list that could block rendering */}
      <div style={{ maxHeight: '200px', overflow: 'auto' }}>
        {items.map(item => (
          <div key={item.id}>{item.value}</div>
        ))}
      </div>
    </div>
  );
}
```

### 🎯 Virtual DOM Diffing Algorithm

**Interview Critical Point:** React uses a heuristic O(n) algorithm instead of O(n³) by making assumptions about real-world usage.

```jsx
// React's diffing assumptions and how they work:

// 1. Different element types produce different trees
function DiffingExample() {
  const [showDiv, setShowDiv] = useState(true);
  
  return (
    <div>
      {showDiv ? (
        <div key="content">  {/* Will be completely replaced */}
          <span>Hello</span>
        </div>
      ) : (
        <p key="content">    {/* New tree, span is destroyed */}
          Hello
        </p>
      )}
    </div>
  );
}

// 2. Keys help identify stable elements across renders
function ListDiffing() {
  const [items, setItems] = useState([
    { id: 1, name: 'Item 1' },
    { id: 2, name: 'Item 2' },
    { id: 3, name: 'Item 3' }
  ]);
  
  const addItem = () => {
    const newItem = { id: Date.now(), name: `Item ${items.length + 1}` };
    setItems([newItem, ...items]); // Adding to beginning
  };
  
  return (
    <div>
      <button onClick={addItem}>Add Item</button>
      
      {/* ❌ Without keys - React will update all elements */}
      <div>
        <h4>Without Keys (Bad):</h4>
        {items.map((item, index) => (
          <div>{item.name} - {Math.random()}</div> // Notice random changes
        ))}
      </div>
      
      {/* ✅ With keys - React will only insert new element */}
      <div>
        <h4>With Keys (Good):</h4>
        {items.map(item => (
          <div key={item.id}>{item.name} - {Math.random()}</div> // Random stays same for existing items
        ))}
      </div>
    </div>
  );
}

// 3. Component reconciliation
function ComponentReconciliation() {
  const [version, setVersion] = useState(1);
  
  // Same component type with different props - React will update
  const ComponentA = ({ version }) => (
    <div>
      <h4>Component A - Version {version}</h4>
      <ExpensiveChild version={version} />
    </div>
  );
  
  // Different component type - React will unmount/remount
  const ComponentB = ({ version }) => (
    <div>
      <h4>Component B - Version {version}</h4>
      <ExpensiveChild version={version} />
    </div>
  );
  
  return (
    <div>
      <button onClick={() => setVersion(v => v + 1)}>
        Update Version
      </button>
      
      {version % 2 === 0 ? (
        <ComponentA version={version} /> // Will update in place
      ) : (
        <ComponentB version={version} /> // Will unmount A and mount B
      )}
    </div>
  );
}

const ExpensiveChild = ({ version }) => {
  useEffect(() => {
    console.log('ExpensiveChild mounted/updated with version:', version);
    return () => console.log('ExpensiveChild unmounting');
  }, [version]);
  
  return <p>Expensive child component</p>;
};
```

### 🎯 Fiber Work Loop and Prioritization

```jsx
// Understanding how Fiber prioritizes work
function PriorityDemo() {
  const [urgentCount, setUrgentCount] = useState(0);
  const [backgroundCount, setBackgroundCount] = useState(0);
  const [items, setItems] = useState([]);
  
  // Simulate user interaction (high priority)
  const handleUrgentUpdate = () => {
    setUrgentCount(c => c + 1);
  };
  
  // Simulate background work (low priority)
  const handleBackgroundUpdate = () => {
    setBackgroundCount(c => c + 1);
    
    // Heavy computation that might block
    const heavyItems = Array.from({ length: 1000 }, (_, i) => ({
      id: i,
      computed: fibonacci(20) // Expensive calculation
    }));
    setItems(heavyItems);
  };
  
  // Start both types of updates rapidly
  const startMixedUpdates = () => {
    // Background work
    handleBackgroundUpdate();
    
    // Urgent work (should interrupt background work)
    setTimeout(() => handleUrgentUpdate(), 10);
    setTimeout(() => handleUrgentUpdate(), 20);
    setTimeout(() => handleUrgentUpdate(), 30);
  };
  
  return (
    <div>
      <h3>Fiber Priority Demo</h3>
      <div>
        <p>Urgent Count: {urgentCount}</p>
        <p>Background Count: {backgroundCount}</p>
        <p>Items: {items.length}</p>
      </div>
      
      <button onClick={handleUrgentUpdate}>
        Urgent Update (High Priority)
      </button>
      <button onClick={handleBackgroundUpdate}>
        Background Update (Low Priority)
      </button>
      <button onClick={startMixedUpdates}>
        Start Mixed Updates
      </button>
      
      {/* This heavy list won't block urgent updates in React 18+ */}
      <div style={{ maxHeight: '100px', overflow: 'auto' }}>
        {items.slice(0, 100).map(item => (
          <div key={item.id}>Item {item.id}: {item.computed}</div>
        ))}
      </div>
    </div>
  );
}

function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}
```

---

## Concurrent Rendering (React 18)

> **Interview Expectation:** Understand React 18's concurrent features, how they improve user experience, and when to use useTransition vs useDeferredValue.

### 🎯 useTransition Hook

**Interview Critical Point:** useTransition lets you mark state updates as non-urgent, allowing React to interrupt them for more urgent updates.

```jsx
import { useState, useTransition, startTransition } from 'react';

function SearchWithTransition() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();
  
  // Simulate expensive search operation
  const performSearch = (searchQuery) => {
    // This would typically be an API call
    const mockResults = Array.from({ length: 10000 }, (_, i) => ({
      id: i,
      title: `Result ${i} for "${searchQuery}"`,
      description: `This is a detailed description for result ${i}`,
      relevance: Math.random()
    })).filter(item => 
      item.title.toLowerCase().includes(searchQuery.toLowerCase())
    ).sort((a, b) => b.relevance - a.relevance);
    
    return mockResults;
  };
  
  const handleSearch = (e) => {
    const value = e.target.value;
    setQuery(value); // Urgent update (immediate UI feedback)
    
    // Non-urgent update (can be interrupted)
    startTransition(() => {
      if (value.trim()) {
        const searchResults = performSearch(value);
        setResults(searchResults);
      } else {
        setResults([]);
      }
    });
  };
  
  return (
    <div>
      <h3>Search with useTransition</h3>
      <input
        type="text"
        value={query}
        onChange={handleSearch}
        placeholder="Type to search..."
        style={{
          width: '300px',
          padding: '8px',
          fontSize: '16px'
        }}
      />
      
      {isPending && <div>Searching...</div>}
      
      <div style={{ marginTop: '20px' }}>
        <p>Found {results.length} results</p>
        <div style={{ maxHeight: '300px', overflow: 'auto' }}>
          {results.slice(0, 50).map(result => (
            <div 
              key={result.id} 
              style={{ 
                padding: '10px', 
                borderBottom: '1px solid #eee' 
              }}
            >
              <h4>{result.title}</h4>
              <p>{result.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

// Comparing with and without useTransition
function ComparisonDemo() {
  const [tab, setTab] = useState('without');
  
  return (
    <div>
      <div>
        <button 
          onClick={() => setTab('without')}
          style={{ 
            backgroundColor: tab === 'without' ? '#007bff' : '#fff',
            color: tab === 'without' ? '#fff' : '#000'
          }}
        >
          Without Transition
        </button>
        <button 
          onClick={() => setTab('with')}
          style={{ 
            backgroundColor: tab === 'with' ? '#007bff' : '#fff',
            color: tab === 'with' ? '#fff' : '#000'
          }}
        >
          With Transition
        </button>
      </div>
      
      {tab === 'without' ? <SearchWithoutTransition /> : <SearchWithTransition />}
    </div>
  );
}

function SearchWithoutTransition() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  
  const handleSearch = (e) => {
    const value = e.target.value;
    setQuery(value);
    
    // Both updates have same priority - can block UI
    if (value.trim()) {
      const searchResults = performSearch(value);
      setResults(searchResults);
    } else {
      setResults([]);
    }
  };
  
  // ... rest similar to SearchWithTransition
}
```

### 🎯 useDeferredValue Hook

**Interview Critical Point:** useDeferredValue lets you defer updating a value until more urgent updates are finished.

```jsx
import { useState, useDeferredValue, useMemo } from 'react';

function ExpensiveList({ query }) {
  // Expensive computation that depends on query
  const items = useMemo(() => {
    console.log('Computing expensive list for:', query);
    
    // Simulate expensive operation
    const start = performance.now();
    while (performance.now() - start < 50) {
      // Busy wait to simulate expensive work
    }
    
    return Array.from({ length: 20000 }, (_, i) => ({
      id: i,
      name: `Item ${i}`,
      description: `Description for item ${i}`,
      matches: query ? `Item ${i}`.toLowerCase().includes(query.toLowerCase()) : true
    })).filter(item => item.matches);
  }, [query]);
  
  return (
    <div style={{ maxHeight: '200px', overflow: 'auto' }}>
      <p>Showing {items.length} items</p>
      {items.slice(0, 100).map(item => (
        <div key={item.id} style={{ padding: '4px', borderBottom: '1px solid #eee' }}>
          <strong>{item.name}</strong>
          <br />
          <small>{item.description}</small>
        </div>
      ))}
    </div>
  );
}

function DeferredValueDemo() {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  
  // Show whether we're showing stale data
  const isStale = query !== deferredQuery;
  
  return (
    <div>
      <h3>useDeferredValue Demo</h3>
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Filter items..."
        style={{
          width: '300px',
          padding: '8px',
          fontSize: '16px'
        }}
      />
      
      {isStale && (
        <div style={{ color: 'orange', marginTop: '10px' }}>
          Updating results...
        </div>
      )}
      
      <div style={{ 
        marginTop: '20px',
        opacity: isStale ? 0.5 : 1,
        transition: 'opacity 0.2s'
      }}>
        <ExpensiveList query={deferredQuery} />
      </div>
    </div>
  );
}

// Advanced: Combining useTransition and useDeferredValue
function AdvancedConcurrentDemo() {
  const [query, setQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [isPending, startTransition] = useTransition();
  const deferredQuery = useDeferredValue(query);
  
  const categories = ['all', 'electronics', 'clothing', 'books', 'home'];
  
  const handleCategoryChange = (category) => {
    startTransition(() => {
      setSelectedCategory(category);
    });
  };
  
  const filteredItems = useMemo(() => {
    console.log('Filtering items:', { deferredQuery, selectedCategory });
    
    // Simulate expensive filtering
    const allItems = Array.from({ length: 50000 }, (_, i) => ({
      id: i,
      name: `Product ${i}`,
      category: categories[i % (categories.length - 1) + 1], // Skip 'all'
      price: Math.random() * 1000
    }));
    
    return allItems.filter(item => {
      const matchesQuery = !deferredQuery || 
        item.name.toLowerCase().includes(deferredQuery.toLowerCase());
      const matchesCategory = selectedCategory === 'all' || 
        item.category === selectedCategory;
      return matchesQuery && matchesCategory;
    });
  }, [deferredQuery, selectedCategory]);
  
  return (
    <div>
      <h3>Advanced Concurrent Features</h3>
      
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search products..."
          style={{ width: '300px', padding: '8px', marginRight: '10px' }}
        />
        
        <select
          value={selectedCategory}
          onChange={(e) => handleCategoryChange(e.target.value)}
          style={{ padding: '8px' }}
        >
          {categories.map(category => (
            <option key={category} value={category}>
              {category.charAt(0).toUpperCase() + category.slice(1)}
            </option>
          ))}
        </select>
      </div>
      
      {isPending && (
        <div style={{ color: 'blue' }}>
          Updating category filter...
        </div>
      )}
      
      {query !== deferredQuery && (
        <div style={{ color: 'orange' }}>
          Updating search results...
        </div>
      )}
      
      <div style={{ 
        marginTop: '10px',
        opacity: (isPending || query !== deferredQuery) ? 0.7 : 1,
        transition: 'opacity 0.2s'
      }}>
        <p>Found {filteredItems.length} products</p>
        <div style={{ maxHeight: '300px', overflow: 'auto' }}>
          {filteredItems.slice(0, 100).map(item => (
            <div 
              key={item.id}
              style={{ 
                padding: '8px', 
                borderBottom: '1px solid #eee',
                display: 'flex',
                justifyContent: 'space-between'
              }}
            >
              <span>{item.name}</span>
              <span>{item.category}</span>
              <span>${item.price.toFixed(2)}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
```

### 🎯 Concurrent Rendering Best Practices

```jsx
// When to use each concurrent feature:

// 1. useTransition - For updates that can be interrupted
function TabsWithTransition() {
  const [tab, setTab] = useState('home');
  const [isPending, startTransition] = useTransition();
  
  const tabs = {
    home: <HomeContent />,
    about: <AboutContent />,
    products: <ExpensiveProductList />, // Heavy component
    contact: <ContactContent />
  };
  
  const handleTabClick = (newTab) => {
    startTransition(() => {
      setTab(newTab); // Non-urgent tab change
    });
  };
  
  return (
    <div>
      <div>
        {Object.keys(tabs).map(tabName => (
          <button
            key={tabName}
            onClick={() => handleTabClick(tabName)}
            style={{
              backgroundColor: tab === tabName ? '#007bff' : '#fff',
              color: tab === tabName ? '#fff' : '#000',
              opacity: isPending ? 0.7 : 1
            }}
          >
            {tabName.charAt(0).toUpperCase() + tabName.slice(1)}
          </button>
        ))}
      </div>
      
      {isPending && <div>Loading tab...</div>}
      
      <div style={{ marginTop: '20px' }}>
        {tabs[tab]}
      </div>
    </div>
  );
}

// 2. useDeferredValue - For expensive computations based on input
function SearchResults({ query }) {
  const deferredQuery = useDeferredValue(query);
  
  const results = useMemo(() => {
    // Expensive search that should use deferred value
    return performExpensiveSearch(deferredQuery);
  }, [deferredQuery]);
  
  return (
    <div style={{ opacity: query !== deferredQuery ? 0.5 : 1 }}>
      {results.map(result => (
        <div key={result.id}>{result.title}</div>
      ))}
    </div>
  );
}

// 3. Combining both for complex UIs
function DataDashboard() {
  const [filters, setFilters] = useState({
    dateRange: 'last-30-days',
    category: 'all',
    sortBy: 'date'
  });
  const [searchQuery, setSearchQuery] = useState('');
  const [isPending, startTransition] = useTransition();
  const deferredSearchQuery = useDeferredValue(searchQuery);
  
  const updateFilter = (key, value) => {
    startTransition(() => {
      setFilters(prev => ({ ...prev, [key]: value }));
    });
  };
  
  const data = useMemo(() => {
    return computeDashboardData(filters, deferredSearchQuery);
  }, [filters, deferredSearchQuery]);
  
  return (
    <div>
      {/* Quick search - immediate feedback */}
      <input
        value={searchQuery}
        onChange={(e) => setSearchQuery(e.target.value)}
        placeholder="Search..."
      />
      
      {/* Filter controls - can be interrupted */}
      <FilterControls 
        filters={filters} 
        onChange={updateFilter}
        disabled={isPending}
      />
      
      {/* Data visualization */}
      <div style={{ 
        opacity: (isPending || searchQuery !== deferredSearchQuery) ? 0.7 : 1 
      }}>
        <DashboardCharts data={data} />
      </div>
    </div>
  );
}
```

---

## Suspense & Lazy Loading

> **Interview Expectation:** Master React's declarative loading states and code-splitting strategies for better performance and user experience.

### 🎯 Basic Lazy Loading with Suspense

**Interview Critical Point:** Suspense provides a declarative way to handle async operations, starting with lazy-loaded components.

```jsx
import { Suspense, lazy, useState } from 'react';

// Lazy load components
const HeavyChart = lazy(() => import('./HeavyChart'));
const DataTable = lazy(() => import('./DataTable'));
const UserProfile = lazy(() => import('./UserProfile'));

// Simulate dynamic imports with delay
const LazyComponent = lazy(() => 
  new Promise(resolve => {
    setTimeout(() => {
      resolve({
        default: function ActualComponent({ name }) {
          return (
            <div style={{ padding: '20px', backgroundColor: '#f0f0f0' }}>
              <h3>Lazy Loaded: {name}</h3>
              <p>This component was loaded on demand!</p>
            </div>
          );
        }
      });
    }, 2000); // 2 second delay to see loading
  })
);

function SuspenseDemo() {
  const [currentView, setCurrentView] = useState(null);
  
  const views = {
    chart: { component: HeavyChart, name: 'Chart' },
    table: { component: DataTable, name: 'Data Table' },
    profile: { component: UserProfile, name: 'User Profile' },
    lazy: { component: LazyComponent, name: 'Lazy Demo' }
  };
  
  return (
    <div>
      <h3>Suspense & Lazy Loading Demo</h3>
      
      <div style={{ marginBottom: '20px' }}>
        {Object.entries(views).map(([key, view]) => (
          <button
            key={key}
            onClick={() => setCurrentView(key)}
            style={{
              margin: '5px',
              padding: '10px',
              backgroundColor: currentView === key ? '#007bff' : '#fff',
              color: currentView === key ? '#fff' : '#000'
            }}
          >
            Load {view.name}
          </button>
        ))}
        <button onClick={() => setCurrentView(null)}>
          Clear
        </button>
      </div>
      
      {currentView && (
        <Suspense 
          fallback={
            <div style={{ 
              padding: '40px', 
              textAlign: 'center', 
              backgroundColor: '#f8f9fa' 
            }}>
              <div>Loading {views[currentView].name}...</div>
              <div style={{ marginTop: '10px' }}>
                <div className="spinner">⏳</div>
              </div>
            </div>
          }
        >
          {React.createElement(views[currentView].component, { 
            name: views[currentView].name 
          })}
        </Suspense>
      )}
    </div>
  );
}

// Advanced: Nested Suspense boundaries
function NestedSuspenseDemo() {
  const [loadMain, setLoadMain] = useState(false);
  
  return (
    <div>
      <h3>Nested Suspense Boundaries</h3>
      <button onClick={() => setLoadMain(!loadMain)}>
        {loadMain ? 'Hide' : 'Show'} Main Content
      </button>
      
      {loadMain && (
        <Suspense fallback={<div>Loading main layout...</div>}>
          <MainLayout />
        </Suspense>
      )}
    </div>
  );
}

const MainLayout = lazy(() => 
  import('./components/MainLayout').catch(() => ({
    default: function MainLayout() {
      return (
        <div style={{ padding: '20px', border: '2px solid #007bff' }}>
          <h4>Main Layout Loaded</h4>
          
          {/* Nested Suspense for sidebar */}
          <div style={{ display: 'flex', gap: '20px' }}>
            <Suspense fallback={<div>Loading sidebar...</div>}>
              <Sidebar />
            </Suspense>
            
            <div style={{ flex: 1 }}>
              <Suspense fallback={<div>Loading content...</div>}>
                <MainContent />
              </Suspense>
            </div>
          </div>
        </div>
      );
    }
  }))
);

const Sidebar = lazy(() => 
  new Promise(resolve => {
    setTimeout(() => {
      resolve({
        default: function Sidebar() {
          return (
            <div style={{ width: '200px', backgroundColor: '#e9ecef', padding: '15px' }}>
              <h5>Sidebar</h5>
              <nav>
                <div>Dashboard</div>
                <div>Settings</div>
                <div>Profile</div>
              </nav>
            </div>
          );
        }
      });
    }, 1000);
  })
);

const MainContent = lazy(() => 
  new Promise(resolve => {
    setTimeout(() => {
      resolve({
        default: function MainContent() {
          return (
            <div style={{ backgroundColor: '#fff3cd', padding: '15px' }}>
              <h5>Main Content</h5>
              <p>This is the main content area.</p>
              
              {/* Even more nested Suspense */}
              <Suspense fallback={<div>Loading widget...</div>}>
                <Widget />
              </Suspense>
            </div>
          );
        }
      });
    }, 1500);
  })
);

const Widget = lazy(() => 
  new Promise(resolve => {
    setTimeout(() => {
      resolve({
        default: function Widget() {
          return (
            <div style={{ 
              marginTop: '10px', 
              padding: '10px', 
              backgroundColor: '#d1ecf1' 
            }}>
              <h6>Widget Loaded</h6>
              <p>This widget loaded last!</p>
            </div>
          );
        }
      });
    }, 500);
  })
);
```

### 🎯 Suspense with Data Fetching

**Interview Critical Point:** While React 18 includes basic Suspense for data fetching, most production apps use libraries like React Query or SWR with Suspense integration.

```jsx
// Simulating Suspense-compatible data fetching
function createSuspenseResource(promise) {
  let status = 'pending';
  let result;
  
  const suspender = promise.then(
    (data) => {
      status = 'success';
      result = data;
    },
    (error) => {
      status = 'error';
      result = error;
    }
  );
  
  return {
    read() {
      if (status === 'pending') {
        throw suspender; // This triggers Suspense
      } else if (status === 'error') {
        throw result;
      } else {
        return result;
      }
    }
  };
}

// Simulate API calls
const fetchUser = (id) => 
  new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        id,
        name: `User ${id}`,
        email: `user${id}@example.com`,
        avatar: `https://via.placeholder.com/100?text=User${id}`
      });
    }, 2000);
  });

const fetchPosts = (userId) =>
  new Promise((resolve) => {
    setTimeout(() => {
      resolve(
        Array.from({ length: 5 }, (_, i) => ({
          id: i + 1,
          title: `Post ${i + 1} by User ${userId}`,
          content: `This is the content of post ${i + 1}`,
          likes: Math.floor(Math.random() * 100)
        }))
      );
    }, 1500);
  });

// Components that use Suspense resources
function UserProfile({ userId }) {
  const userResource = createSuspenseResource(fetchUser(userId));
  const user = userResource.read(); // This will suspend if not ready
  
  return (
    <div style={{ padding: '15px', border: '1px solid #ddd' }}>
      <img 
        src={user.avatar} 
        alt={user.name}
        style={{ width: '50px', height: '50px', borderRadius: '50%' }}
      />
      <h4>{user.name}</h4>
      <p>{user.email}</p>
    </div>
  );
}

function UserPosts({ userId }) {
  const postsResource = createSuspenseResource(fetchPosts(userId));
  const posts = postsResource.read(); // This will suspend if not ready
  
  return (
    <div style={{ marginTop: '20px' }}>
      <h4>Posts</h4>
      {posts.map(post => (
        <div 
          key={post.id}
          style={{ 
            padding: '10px', 
            marginBottom: '10px', 
            backgroundColor: '#f8f9fa',
            borderRadius: '4px'
          }}
        >
          <h5>{post.title}</h5>
          <p>{post.content}</p>
          <small>👍 {post.likes} likes</small>
        </div>
      ))}
    </div>
  );
}

// Main component orchestrating the Suspense boundaries
function SuspenseDataDemo() {
  const [userId, setUserId] = useState(null);
  
  return (
    <div>
      <h3>Suspense with Data Fetching</h3>
      
      <div style={{ marginBottom: '20px' }}>
        {[1, 2, 3].map(id => (
          <button
            key={id}
            onClick={() => setUserId(id)}
            style={{
              margin: '5px',
              padding: '10px',
              backgroundColor: userId === id ? '#007bff' : '#fff',
              color: userId === id ? '#fff' : '#000'
            }}
          >
            Load User {id}
          </button>
        ))}
        <button onClick={() => setUserId(null)}>Clear</button>
      </div>
      
      {userId && (
        <div>
          {/* User profile loads first */}
          <Suspense 
            fallback={
              <div style={{ padding: '15px', backgroundColor: '#e9ecef' }}>
                Loading user profile...
              </div>
            }
          >
            <UserProfile userId={userId} />
          </Suspense>
          
          {/* Posts load separately */}
          <Suspense 
            fallback={
              <div style={{ padding: '15px', backgroundColor: '#fff3cd' }}>
                Loading user posts...
              </div>
            }
          >
            <UserPosts userId={userId} />
          </Suspense>
        </div>
      )}
    </div>
  );
}
```

### 🎯 Advanced Suspense Patterns

```jsx
// Error boundaries with Suspense
class SuspenseErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }
  
  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }
  
  componentDidCatch(error, errorInfo) {
    console.error('Suspense Error:', error, errorInfo);
  }
  
  render() {
    if (this.state.hasError) {
      return (
        <div style={{ 
          padding: '20px', 
          backgroundColor: '#f8d7da', 
          color: '#721c24',
          borderRadius: '4px'
        }}>
          <h4>Something went wrong</h4>
          <p>{this.state.error?.message}</p>
          <button 
            onClick={() => this.setState({ hasError: false, error: null })}
          >
            Try Again
          </button>
        </div>
      );
    }
    
    return this.props.children;
  }
}

// Suspense with loading priorities
function PriorityLoadingDemo() {
  const [loadCritical, setLoadCritical] = useState(false);
  const [loadSecondary, setLoadSecondary] = useState(false);
  
  return (
    <div>
      <h3>Priority Loading with Suspense</h3>
      
      <div style={{ marginBottom: '20px' }}>
        <button onClick={() => setLoadCritical(!loadCritical)}>
          {loadCritical ? 'Hide' : 'Show'} Critical Content
        </button>
        <button onClick={() => setLoadSecondary(!loadSecondary)}>
          {loadSecondary ? 'Hide' : 'Show'} Secondary Content
        </button>
      </div>
      
      {/* Critical content with high priority fallback */}
      {loadCritical && (
        <SuspenseErrorBoundary>
          <Suspense 
            fallback={
              <div style={{ 
                padding: '20px', 
                backgroundColor: '#dc3545', 
                color: 'white',
                textAlign: 'center'
              }}>
                ⚡ Loading critical content...
              </div>
            }
          >
            <CriticalContent />
          </Suspense>
        </SuspenseErrorBoundary>
      )}
      
      {/* Secondary content with lower priority */}
      {loadSecondary && (
        <SuspenseErrorBoundary>
          <Suspense 
            fallback={
              <div style={{ 
                padding: '10px', 
                backgroundColor: '#6c757d', 
                color: 'white',
                fontSize: '14px'
              }}>
                Loading additional content...
              </div>
            }
          >
            <SecondaryContent />
          </Suspense>
        </SuspenseErrorBoundary>
      )}
    </div>
  );
}

const CriticalContent = lazy(() => 
  new Promise((resolve, reject) => {
    setTimeout(() => {
      // Randomly fail sometimes to test error boundary
      if (Math.random() > 0.7) {
        reject(new Error('Failed to load critical content'));
      } else {
        resolve({
          default: function CriticalContent() {
            return (
              <div style={{ 
                padding: '20px', 
                backgroundColor: '#d4edda', 
                border: '1px solid #c3e6cb' 
              }}>
                <h4>✅ Critical Content Loaded</h4>
                <p>This content is essential for the user experience.</p>
              </div>
            );
          }
        });
      }
    }, 1000);
  })
);

const SecondaryContent = lazy(() => 
  new Promise(resolve => {
    setTimeout(() => {
      resolve({
        default: function SecondaryContent() {
          return (
            <div style={{ 
              padding: '15px', 
              backgroundColor: '#e2e3e5', 
              marginTop: '10px' 
            }}>
              <h5>Secondary Content</h5>
              <p>This content enhances the experience but isn't critical.</p>
            </div>
          );
        }
      });
    }, 2000);
  })
);

// Preloading strategy
function PreloadingDemo() {
  const [showContent, setShowContent] = useState(false);
  const [preloaded, setPreloaded] = useState(false);
  
  // Preload on hover or focus
  const handlePreload = () => {
    if (!preloaded) {
      // Start loading the component
      import('./HeavyComponent')
        .then(() => setPreloaded(true))
        .catch(console.error);
    }
  };
  
  return (
    <div>
      <h3>Preloading Strategy</h3>
      
      <button
        onMouseEnter={handlePreload} // Preload on hover
        onFocus={handlePreload}      // Preload on focus
        onClick={() => setShowContent(true)}
        style={{
          padding: '15px 30px',
          fontSize: '16px',
          backgroundColor: preloaded ? '#28a745' : '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '4px'
        }}
      >
        {preloaded ? '✅ Ready to Load' : 'Load Heavy Content'}
      </button>
      
      <p style={{ fontSize: '14px', color: '#666' }}>
        Hover over the button to preload the component
      </p>
      
      {showContent && (
        <Suspense 
          fallback={
            preloaded ? 
              <div>Rendering preloaded content...</div> :
              <div>Loading content...</div>
          }
        >
          <HeavyComponent />
        </Suspense>
      )}
    </div>
  );
}
```

---

## Server Components (React 18+)

> **Interview Expectation:** Understand the paradigm shift of React Server Components, how they differ from traditional SSR, and their impact on application architecture.

### 🎯 Understanding React Server Components

**Interview Critical Point:** Server Components run on the server and send their output to the client as a special format, not HTML. They never re-render on the client.

```jsx
// Traditional Client Component (runs in browser)
'use client'; // This directive marks it as a Client Component

import { useState, useEffect } from 'react';

function TraditionalUserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    // Client-side data fetching
    fetch('/api/users')
      .then(res => res.json())
      .then(data => {
        setUsers(data);
        setLoading(false);
      });
  }, []);
  
  if (loading) return <div>Loading users...</div>;
  
  return (
    <div>
      <h3>Users (Client Component)</h3>
      {users.map(user => (
        <div key={user.id}>
          <UserCard user={user} />
        </div>
      ))}
    </div>
  );
}

// React Server Component (runs on server)
// No 'use client' directive = Server Component by default
async function ServerUserList() {
  // Direct database/API access on server
  const users = await getUsersFromDatabase();
  
  return (
    <div>
      <h3>Users (Server Component)</h3>
      {users.map(user => (
        <div key={user.id}>
          <UserCard user={user} />
          {/* Can mix Server and Client components */}
          <InteractiveButton userId={user.id} />
        </div>
      ))}
    </div>
  );
}

// Client Component for interactivity
'use client';
function InteractiveButton({ userId }) {
  const [liked, setLiked] = useState(false);
  
  return (
    <button 
      onClick={() => setLiked(!liked)}
      style={{ 
        backgroundColor: liked ? '#007bff' : '#fff',
        color: liked ? '#fff' : '#000'
      }}
    >
      {liked ? '❤️ Liked' : '🤍 Like'}
    </button>
  );
}

// Server Component with nested data fetching
async function UserProfile({ userId }) {
  // Parallel data fetching on server
  const [user, posts, comments] = await Promise.all([
    getUser(userId),
    getUserPosts(userId),
    getUserComments(userId)
  ]);
  
  return (
    <div>
      <h2>{user.name}</h2>
      <p>{user.bio}</p>
      
      {/* Nested Server Component */}
      <UserPosts posts={posts} />
      
      {/* Client Component for interactivity */}
      <CommentForm userId={userId} />
      
      {/* Another Server Component */}
      <UserComments comments={comments} />
    </div>
  );
}

async function UserPosts({ posts }) {
  return (
    <section>
      <h3>Posts</h3>
      {posts.map(post => (
        <article key={post.id}>
          <h4>{post.title}</h4>
          <p>{post.content}</p>
          
          {/* Client Component for post interactions */}
          <PostActions postId={post.id} />
        </article>
      ))}
    </section>
  );
}

'use client';
function CommentForm({ userId }) {
  const [comment, setComment] = useState('');
  const [submitting, setSubmitting] = useState(false);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    
    try {
      await fetch('/api/comments', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId, comment })
      });
      setComment('');
    } catch (error) {
      console.error('Failed to submit comment:', error);
    } finally {
      setSubmitting(false);
    }
  };
  
  return (
    <form onSubmit={handleSubmit}>
      <textarea
        value={comment}
        onChange={(e) => setComment(e.target.value)}
        placeholder="Write a comment..."
        rows={3}
        style={{ width: '100%', padding: '8px' }}
      />
      <button 
        type="submit" 
        disabled={submitting || !comment.trim()}
      >
        {submitting ? 'Posting...' : 'Post Comment'}
      </button>
    </form>
  );
}
```

### 🎯 Server vs Client Component Boundaries

**Interview Critical Point:** Understanding when components can be Server vs Client components and how data flows between them.

```jsx
// ✅ Valid: Server Component rendering Client Component
async function ServerParent() {
  const data = await fetchServerData();
  
  return (
    <div>
      <h1>Server Content</h1>
      <ClientChild data={data} />
    </div>
  );
}

'use client';
function ClientChild({ data }) {
  const [selected, setSelected] = useState(null);
  
  return (
    <div>
      <h2>Client Interactivity</h2>
      {data.map(item => (
        <button
          key={item.id}
          onClick={() => setSelected(item)}
          style={{
            backgroundColor: selected?.id === item.id ? '#007bff' : '#fff'
          }}
        >
          {item.name}
        </button>
      ))}
    </div>
  );
}

// ❌ Invalid: Client Component cannot render Server Component as child
'use client';
function ClientParent() {
  const [count, setCount] = useState(0);
  
  return (
    <div>
      <button onClick={() => setCount(count + 1)}>Count: {count}</button>
      {/* This won't work! Server Components can't be children of Client Components */}
      <ServerChild />
    </div>
  );
}

// ✅ Solution: Pass Server Component as prop
async function AppLayout() {
  return (
    <ClientWrapper>
      <ServerContent />
    </ClientWrapper>
  );
}

'use client';
function ClientWrapper({ children }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  return (
    <div style={{ display: 'flex' }}>
      <button onClick={() => setSidebarOpen(!sidebarOpen)}>
        Toggle Sidebar
      </button>
      
      {sidebarOpen && (
        <div style={{ width: '200px', backgroundColor: '#f0f0f0' }}>
          Sidebar Content
        </div>
      )}
      
      <main style={{ flex: 1 }}>
        {children} {/* Server Component rendered here */}
      </main>
    </div>
  );
}

async function ServerContent() {
  const articles = await getArticles();
  
  return (
    <div>
      {articles.map(article => (
        <article key={article.id}>
          <h3>{article.title}</h3>
          <p>{article.excerpt}</p>
          
          {/* Client Component for interactions */}
          <ArticleActions articleId={article.id} />
        </article>
      ))}
    </div>
  );
}
```

### 🎯 Server Actions (React 19+)

```jsx
// Server Actions for form handling
'use server';

async function createPost(formData) {
  const title = formData.get('title');
  const content = formData.get('content');
  
  // Direct database access
  const post = await db.posts.create({
    title,
    content,
    authorId: getCurrentUserId()
  });
  
  // Revalidate cache
  revalidatePath('/posts');
  
  return { success: true, post };
}

async function deletePost(postId) {
  await db.posts.delete({ where: { id: postId } });
  revalidatePath('/posts');
}

// Client Component using Server Actions
'use client';
function PostForm() {
  const [pending, startTransition] = useTransition();
  
  const handleSubmit = async (formData) => {
    startTransition(async () => {
      const result = await createPost(formData);
      if (result.success) {
        // Form reset or redirect
        console.log('Post created:', result.post);
      }
    });
  };
  
  return (
    <form action={handleSubmit}>
      <input
        name="title"
        placeholder="Post title"
        required
        style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
      />
      <textarea
        name="content"
        placeholder="Post content"
        required
        rows={4}
        style={{ width: '100%', padding: '8px', marginBottom: '10px' }}
      />
      <button 
        type="submit"
        disabled={pending}
        style={{
          padding: '10px 20px',
          backgroundColor: pending ? '#ccc' : '#007bff',
          color: 'white',
          border: 'none'
        }}
      >
        {pending ? 'Creating...' : 'Create Post'}
      </button>
    </form>
  );
}

// Server Component with progressive enhancement
async function PostList() {
  const posts = await getPosts();
  
  return (
    <div>
      <h2>Posts</h2>
      {posts.map(post => (
        <div key={post.id} style={{ 
          padding: '15px', 
          border: '1px solid #ddd', 
          marginBottom: '10px' 
        }}>
          <h3>{post.title}</h3>
          <p>{post.content}</p>
          
          {/* Progressive enhancement with Server Action */}
          <form action={deletePost.bind(null, post.id)}>
            <button 
              type="submit"
              style={{ 
                backgroundColor: '#dc3545', 
                color: 'white', 
                border: 'none',
                padding: '5px 10px'
              }}
            >
              Delete
            </button>
          </form>
        </div>
      ))}
    </div>
  );
}
```

---

## Hydration in SSR

> **Interview Expectation:** Understand the hydration process, common pitfalls, and strategies for optimal server-side rendering performance.

### 🎯 Understanding Hydration

**Interview Critical Point:** Hydration is the process where React takes over server-rendered HTML and makes it interactive by attaching event listeners and state.

```jsx
// Server-side rendering setup (Next.js example)
// pages/users.js
export async function getServerSideProps() {
  // This runs on the server
  const users = await fetch('https://api.example.com/users').then(r => r.json());
  
  return {
    props: {
      users,
      serverTime: new Date().toISOString()
    }
  };
}

function UsersPage({ users, serverTime }) {
  const [hydrated, setHydrated] = useState(false);
  const [clientTime, setClientTime] = useState('');
  
  useEffect(() => {
    // This only runs on client after hydration
    setHydrated(true);
    setClientTime(new Date().toISOString());
  }, []);
  
  return (
    <div>
      <h1>Users</h1>
      <p>Server time: {serverTime}</p>
      <p>Client time: {hydrated ? clientTime : 'Hydrating...'}</p>
      <p>Hydrated: {hydrated ? 'Yes' : 'No'}</p>
      
      <UserList users={users} />
    </div>
  );
}

function UserList({ users }) {
  const [selectedUser, setSelectedUser] = useState(null);
  
  return (
    <div>
      {users.map(user => (
        <div 
          key={user.id}
          onClick={() => setSelectedUser(user)}
          style={{
            padding: '10px',
            border: '1px solid #ddd',
            margin: '5px 0',
            cursor: 'pointer',
            backgroundColor: selectedUser?.id === user.id ? '#e7f3ff' : 'white'
          }}
        >
          <h3>{user.name}</h3>
          <p>{user.email}</p>
        </div>
      ))}
      
      {selectedUser && (
        <div style={{ 
          marginTop: '20px', 
          padding: '15px', 
          backgroundColor: '#f8f9fa' 
        }}>
          <h4>Selected: {selectedUser.name}</h4>
          <p>Email: {selectedUser.email}</p>
        </div>
      )}
    </div>
  );
}
```

### 🎯 Hydration Mismatches and Solutions

**Interview Critical Point:** When server and client render different content, React throws hydration errors. These must be handled carefully.

```jsx
// ❌ Common hydration mismatch - different content on server vs client
function ProblematicComponent() {
  // This will cause hydration mismatch!
  const randomId = Math.random(); // Different on server vs client
  
  return (
    <div>
      <h3>Random ID: {randomId}</h3>
      <p>Current time: {new Date().toLocaleString()}</p>
    </div>
  );
}

// ✅ Solution 1: useEffect for client-only content
function FixedWithUseEffect() {
  const [clientOnlyData, setClientOnlyData] = useState(null);
  const [mounted, setMounted] = useState(false);
  
  useEffect(() => {
    setMounted(true);
    setClientOnlyData({
      randomId: Math.random(),
      currentTime: new Date().toLocaleString()
    });
  }, []);
  
  if (!mounted) {
    // Return server-safe content
    return (
      <div>
        <h3>Loading...</h3>
      </div>
    );
  }
  
  return (
    <div>
      <h3>Random ID: {clientOnlyData.randomId}</h3>
      <p>Current time: {clientOnlyData.currentTime}</p>
    </div>
  );
}

// ✅ Solution 2: Custom hook for safe hydration
function useIsomorphicData(serverData, getClientData) {
  const [data, setData] = useState(serverData);
  const [isHydrated, setIsHydrated] = useState(false);
  
  useEffect(() => {
    setIsHydrated(true);
    setData(getClientData());
  }, [getClientData]);
  
  return { data, isHydrated };
}

function SafeComponent({ serverTime }) {
  const { data: timeData, isHydrated } = useIsomorphicData(
    { time: serverTime, source: 'server' },
    () => ({ time: new Date().toISOString(), source: 'client' })
  );
  
  return (
    <div>
      <h3>Safe Time Display</h3>
      <p>Time: {timeData.time}</p>
      <p>Source: {timeData.source}</p>
      <p>Hydrated: {isHydrated ? 'Yes' : 'No'}</p>
    </div>
  );
}

// ✅ Solution 3: Conditional rendering with suppressHydrationWarning
function ConditionalRender() {
  const [isClient, setIsClient] = useState(false);
  
  useEffect(() => {
    setIsClient(true);
  }, []);
  
  return (
    <div>
      <h3>Conditional Content</h3>
      
      {/* Always rendered content */}
      <p>This content is the same on server and client</p>
      
      {/* Client-only content */}
      <div suppressHydrationWarning>
        {isClient ? (
          <p>Client-only: {Math.random()}</p>
        ) : (
          <p>Server placeholder</p>
        )}
      </div>
    </div>
  );
}

// ✅ Solution 4: Dynamic imports with no SSR
import dynamic from 'next/dynamic';

const ClientOnlyComponent = dynamic(
  () => import('./ClientOnlyComponent'),
  { 
    ssr: false,
    loading: () => <p>Loading client component...</p>
  }
);

function ParentComponent() {
  return (
    <div>
      <h3>Parent Component</h3>
      <p>This content is server-rendered</p>
      
      {/* This component only renders on client */}
      <ClientOnlyComponent />
    </div>
  );
}
```

### 🎯 Progressive Hydration Strategies

```jsx
// Strategy 1: Lazy hydration based on intersection
function useLazyHydration(ref, threshold = 0.1) {
  const [shouldHydrate, setShouldHydrate] = useState(false);
  
  useEffect(() => {
    if (!ref.current) return;
    
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setShouldHydrate(true);
          observer.disconnect();
        }
      },
      { threshold }
    );
    
    observer.observe(ref.current);
    
    return () => observer.disconnect();
  }, [ref, threshold]);
  
  return shouldHydrate;
}

function LazyHydratedComponent({ content }) {
  const ref = useRef(null);
  const shouldHydrate = useLazyHydration(ref);
  const [interactions, setInteractions] = useState(0);
  
  const handleInteraction = () => {
    setInteractions(prev => prev + 1);
  };
  
  return (
    <div ref={ref} style={{ minHeight: '200px', padding: '20px', border: '1px solid #ccc' }}>
      <h4>Lazy Hydrated Component</h4>
      <p>{content}</p>
      
      {shouldHydrate ? (
        <div>
          <button onClick={handleInteraction}>
            Interactive! Clicks: {interactions}
          </button>
          <p>This component is now hydrated and interactive.</p>
        </div>
      ) : (
        <div>
          <button disabled>
            Loading interactivity...
          </button>
          <p>This component will become interactive when scrolled into view.</p>
        </div>
      )}
    </div>
  );
}

// Strategy 2: Idle hydration
function useIdleHydration(timeout = 2000) {
  const [shouldHydrate, setShouldHydrate] = useState(false);
  
  useEffect(() => {
    const requestIdleCallback = window.requestIdleCallback || 
      ((cb) => setTimeout(cb, timeout));
    
    const idleCallbackId = requestIdleCallback(() => {
      setShouldHydrate(true);
    });
    
    return () => {
      if (window.cancelIdleCallback) {
        window.cancelIdleCallback(idleCallbackId);
      } else {
        clearTimeout(idleCallbackId);
      }
    };
  }, [timeout]);
  
  return shouldHydrate;
}

function IdleHydratedWidget() {
  const shouldHydrate = useIdleHydration();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  
  const fetchData = async () => {
    setLoading(true);
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));
      setData(['Item 1', 'Item 2', 'Item 3']);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div style={{ padding: '20px', backgroundColor: '#f8f9fa' }}>
      <h4>Idle Hydrated Widget</h4>
      
      {shouldHydrate ? (
        <div>
          <button onClick={fetchData} disabled={loading}>
            {loading ? 'Loading...' : 'Fetch Data'}
          </button>
          
          {data.length > 0 && (
            <ul>
              {data.map((item, index) => (
                <li key={index}>{item}</li>
              ))}
            </ul>
          )}
        </div>
      ) : (
        <div>
          <button disabled>Hydrating...</button>
          <p>Widget will become interactive when browser is idle.</p>
        </div>
      )}
    </div>
  );
}

// Strategy 3: User interaction hydration
function useInteractionHydration() {
  const [shouldHydrate, setShouldHydrate] = useState(false);
  const ref = useRef(null);
  
  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    
    const events = ['mouseenter', 'focus', 'touchstart'];
    
    const handleInteraction = () => {
      setShouldHydrate(true);
      // Remove listeners once hydrated
      events.forEach(event => {
        element.removeEventListener(event, handleInteraction);
      });
    };
    
    events.forEach(event => {
      element.addEventListener(event, handleInteraction, { passive: true });
    });
    
    return () => {
      events.forEach(event => {
        element.removeEventListener(event, handleInteraction);
      });
    };
  }, []);
  
  return { ref, shouldHydrate };
}

function InteractionHydratedForm() {
  const { ref, shouldHydrate } = useInteractionHydration();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    message: ''
  });
  
  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form submitted:', formData);
    alert('Form submitted successfully!');
  };
  
  const handleChange = (field) => (e) => {
    setFormData(prev => ({
      ...prev,
      [field]: e.target.value
    }));
  };
  
  return (
    <div ref={ref} style={{ padding: '20px', border: '2px solid #007bff' }}>
      <h4>Interaction Hydrated Form</h4>
      <p>Hover, focus, or touch to activate this form</p>
      
      {shouldHydrate ? (
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: '10px' }}>
            <input
              type="text"
              placeholder="Your name"
              value={formData.name}
              onChange={handleChange('name')}
              style={{ width: '100%', padding: '8px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <input
              type="email"
              placeholder="Your email"
              value={formData.email}
              onChange={handleChange('email')}
              style={{ width: '100%', padding: '8px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <textarea
              placeholder="Your message"
              value={formData.message}
              onChange={handleChange('message')}
              rows={4}
              style={{ width: '100%', padding: '8px' }}
            />
          </div>
          <button 
            type="submit"
            style={{ 
              padding: '10px 20px', 
              backgroundColor: '#007bff', 
              color: 'white',
              border: 'none'
            }}
          >
            Submit
          </button>
        </form>
      ) : (
        <div style={{ opacity: 0.6 }}>
          <div style={{ marginBottom: '10px' }}>
            <input
              type="text"
              placeholder="Your name"
              disabled
              style={{ width: '100%', padding: '8px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <input
              type="email"
              placeholder="Your email"
              disabled
              style={{ width: '100%', padding: '8px' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <textarea
              placeholder="Your message"
              disabled
              rows={4}
              style={{ width: '100%', padding: '8px' }}
            />
          </div>
          <button 
            disabled
            style={{ 
              padding: '10px 20px', 
              backgroundColor: '#ccc', 
              color: 'white',
              border: 'none'
            }}
          >
            Form will activate on interaction
          </button>
        </div>
      )}
    </div>
  );
}
```

---

## Profiler API (Performance Debugging)

> **Interview Expectation:** Know how to use React's built-in profiling tools to identify performance bottlenecks and optimize rendering.

### 🎯 React Profiler Component

**Interview Critical Point:** The Profiler API measures the cost of rendering parts of your React application.

```jsx
import { Profiler } from 'react';

function ProfilerDemo() {
  const [items, setItems] = useState([]);
  const [renderCount, setRenderCount] = useState(0);
  
  // Profiler callback function
  const onRenderCallback = (id, phase, actualDuration, baseDuration, startTime, commitTime) => {
    console.log('Profiler Results:', {
      id,           // The "id" prop of the Profiler tree that has just committed
      phase,        // Either "mount" (if the tree just mounted) or "update" (if it re-rendered)
      actualDuration, // Time spent rendering the committed update
      baseDuration,   // Estimated time to render the entire subtree without memoization
      startTime,      // When React began rendering this update
      commitTime      // When React committed this update
    });
    
    // Track render performance
    if (actualDuration > 16) { // More than one frame (60fps = 16.67ms per frame)
      console.warn(`Slow render detected: ${actualDuration}ms`);
    }
  };
  
  const addItems = (count) => {
    const newItems = Array.from({ length: count }, (_, i) => ({
      id: Date.now() + i,
      value: Math.random(),
      heavy: fibonacci(35) // Expensive computation
    }));
    setItems(prev => [...prev, ...newItems]);
    setRenderCount(prev => prev + 1);
  };
  
  return (
    <div>
      <h3>Profiler API Demo</h3>
      
      <div style={{ marginBottom: '20px' }}>
        <button onClick={() => addItems(10)}>Add 10 Items</button>
        <button onClick={() => addItems(100)}>Add 100 Items (Slow)</button>
        <button onClick={() => setItems([])}>Clear</button>
        <span style={{ marginLeft: '20px' }}>
          Renders: {renderCount} | Items: {items.length}
        </span>
      </div>
      
      {/* Wrap component tree in Profiler */}
      <Profiler id="ItemList" onRender={onRenderCallback}>
        <ExpensiveItemList items={items} />
      </Profiler>
    </div>
  );
}

// Component that's expensive to render
function ExpensiveItemList({ items }) {
  return (
    <div style={{ maxHeight: '300px', overflow: 'auto' }}>
      {items.map(item => (
        <Profiler key={item.id} id={`Item-${item.id}`} onRender={(id, phase, actualDuration) => {
          if (actualDuration > 5) {
            console.log(`Slow item render: ${id} took ${actualDuration}ms`);
          }
        }}>
          <ExpensiveItem item={item} />
        </Profiler>
      ))}
    </div>
  );
}

function ExpensiveItem({ item }) {
  // Simulate expensive rendering
  const computedValue = useMemo(() => {
    // Complex calculation
    let result = item.value;
    for (let i = 0; i < 1000; i++) {
      result = Math.sin(result) + Math.cos(result);
    }
    return result;
  }, [item.value]);
  
  return (
    <div style={{ 
      padding: '10px', 
      margin: '5px', 
      border: '1px solid #ddd',
      backgroundColor: item.heavy > 9 ? '#ffebee' : '#e8f5e8' 
    }}>
      <strong>ID:</strong> {item.id}<br />
      <strong>Value:</strong> {item.value.toFixed(4)}<br />
      <strong>Heavy:</strong> {item.heavy}<br />
      <strong>Computed:</strong> {computedValue.toFixed(4)}
    </div>
  );
}

function fibonacci(n) {
  if (n <= 1) return n;
  return fibonacci(n - 1) + fibonacci(n - 2);
}
```

### 🎯 Custom Performance Monitoring

```jsx
// Custom hook for performance monitoring
function useRenderProfiler(componentName) {
  const renderCount = useRef(0);
  const lastRenderTime = useRef(performance.now());
  const renderTimes = useRef([]);
  
  useEffect(() => {
    renderCount.current += 1;
    const currentTime = performance.now();
    const renderDuration = currentTime - lastRenderTime.current;
    
    renderTimes.current.push(renderDuration);
    
    // Keep only last 100 renders
    if (renderTimes.current.length > 100) {
      renderTimes.current.shift();
    }
    
    const avgRenderTime = renderTimes.current.reduce((a, b) => a + b, 0) / renderTimes.current.length;
    
    console.log(`${componentName} render #${renderCount.current}:`, {
      renderDuration: renderDuration.toFixed(2) + 'ms',
      avgRenderTime: avgRenderTime.toFixed(2) + 'ms',
      totalRenders: renderCount.current
    });
    
    lastRenderTime.current = currentTime;
  });
  
  return {
    renderCount: renderCount.current,
    averageRenderTime: renderTimes.current.length > 0 
      ? renderTimes.current.reduce((a, b) => a + b, 0) / renderTimes.current.length 
      : 0
  };
}

// Component using custom profiler
function MonitoredComponent({ data }) {
  const { renderCount, averageRenderTime } = useRenderProfiler('MonitoredComponent');
  const [localState, setLocalState] = useState(0);
  
  // Expensive computation
  const processedData = useMemo(() => {
    console.log('Processing data...');
    return data.map(item => ({
      ...item,
      processed: item.value * 2 + Math.random()
    }));
  }, [data]);
  
  return (
    <div style={{ padding: '20px', border: '2px solid #28a745' }}>
      <h4>Monitored Component</h4>
      <div style={{ marginBottom: '10px', fontSize: '12px', color: '#666' }}>
        Renders: {renderCount} | Avg: {averageRenderTime.toFixed(2)}ms
      </div>
      
      <button onClick={() => setLocalState(prev => prev + 1)}>
        Local State: {localState}
      </button>
      
      <div style={{ marginTop: '10px', maxHeight: '150px', overflow: 'auto' }}>
        {processedData.slice(0, 20).map(item => (
          <div key={item.id} style={{ padding: '5px', borderBottom: '1px solid #eee' }}>
            {item.name}: {item.processed.toFixed(3)}
          </div>
        ))}
      </div>
    </div>
  );
}

// Performance comparison component
function PerformanceComparison() {
  const [data, setData] = useState([]);
  const [showOptimized, setShowOptimized] = useState(true);
  
  const generateData = (count) => {
    return Array.from({ length: count }, (_, i) => ({
      id: i,
      name: `Item ${i}`,
      value: Math.random() * 100
    }));
  };
  
  useEffect(() => {
    setData(generateData(1000));
  }, []);
  
  const updateData = () => {
    setData(generateData(1000));
  };
  
  return (
    <div>
      <h3>Performance Comparison</h3>
      
      <div style={{ marginBottom: '20px' }}>
        <button onClick={updateData}>Update Data</button>
        <label style={{ marginLeft: '20px' }}>
          <input
            type="checkbox"
            checked={showOptimized}
            onChange={(e) => setShowOptimized(e.target.checked)}
          />
          Show Optimized Version
        </label>
      </div>
      
      <div style={{ display: 'flex', gap: '20px' }}>
        <div style={{ flex: 1 }}>
          <h4>Unoptimized</h4>
          <Profiler id="Unoptimized" onRender={(id, phase, actualDuration) => {
            console.log(`${id} (${phase}): ${actualDuration}ms`);
          }}>
            <UnoptimizedComponent data={data} />
          </Profiler>
        </div>
        
        {showOptimized && (
          <div style={{ flex: 1 }}>
            <h4>Optimized</h4>
            <Profiler id="Optimized" onRender={(id, phase, actualDuration) => {
              console.log(`${id} (${phase}): ${actualDuration}ms`);
            }}>
              <OptimizedComponent data={data} />
            </Profiler>
          </div>
        )}
      </div>
    </div>
  );
}

// Unoptimized component (re-renders everything)
function UnoptimizedComponent({ data }) {
  const [filter, setFilter] = useState('');
  
  // No memoization - filters on every render
  const filteredData = data.filter(item => 
    item.name.toLowerCase().includes(filter.toLowerCase())
  );
  
  return (
    <div style={{ border: '1px solid #dc3545', padding: '10px' }}>
      <input
        type="text"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Filter items..."
        style={{ width: '100%', marginBottom: '10px' }}
      />
      
      <div style={{ maxHeight: '200px', overflow: 'auto' }}>
        {filteredData.map(item => (
          <UnoptimizedItem key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
}

function UnoptimizedItem({ item }) {
  // Expensive operation on every render
  const expensiveValue = () => {
    let result = 0;
    for (let i = 0; i < 10000; i++) {
      result += Math.sin(item.value + i);
    }
    return result;
  };
  
  return (
    <div style={{ padding: '5px', borderBottom: '1px solid #eee' }}>
      {item.name}: {expensiveValue().toFixed(3)}
    </div>
  );
}

// Optimized component (with memoization)
const OptimizedComponent = React.memo(function OptimizedComponent({ data }) {
  const [filter, setFilter] = useState('');
  
  // Memoized filtering
  const filteredData = useMemo(() => {
    return data.filter(item => 
      item.name.toLowerCase().includes(filter.toLowerCase())
    );
  }, [data, filter]);
  
  return (
    <div style={{ border: '1px solid #28a745', padding: '10px' }}>
      <input
        type="text"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        placeholder="Filter items..."
        style={{ width: '100%', marginBottom: '10px' }}
      />
      
      <div style={{ maxHeight: '200px', overflow: 'auto' }}>
        {filteredData.map(item => (
          <OptimizedItem key={item.id} item={item} />
        ))}
      </div>
    </div>
  );
});

const OptimizedItem = React.memo(function OptimizedItem({ item }) {
  // Memoized expensive operation
  const expensiveValue = useMemo(() => {
    let result = 0;
    for (let i = 0; i < 10000; i++) {
      result += Math.sin(item.value + i);
    }
    return result;
  }, [item.value]);
  
  return (
    <div style={{ padding: '5px', borderBottom: '1px solid #eee' }}>
      {item.name}: {expensiveValue.toFixed(3)}
    </div>
  );
});
```

---

## Memoization Mastery

> **Interview Expectation:** Master when and how to use React.memo, useMemo, and useCallback effectively. Equally important: know when NOT to use them.

### 🎯 React.memo - Component Memoization

**Interview Critical Point:** React.memo prevents re-renders when props haven't changed, but it's not always beneficial.

```jsx
// ✅ Good use case: Expensive component with stable props
const ExpensiveChart = React.memo(function ExpensiveChart({ data, config }) {
  console.log('ExpensiveChart rendering');
  
  // Simulate expensive chart rendering
  const processedData = useMemo(() => {
    console.log('Processing chart data...');
    return data.map(point => ({
      ...point,
      processed: heavyComputation(point.value)
    }));
  }, [data]);
  
  return (
    <div style={{ 
      padding: '20px', 
      border: '2px solid #007bff',
      minHeight: '200px'
    }}>
      <h4>Expensive Chart</h4>
      <pre>{JSON.stringify(config, null, 2)}</pre>
      <div>Data points: {processedData.length}</div>
    </div>
  );
});

// ❌ Bad use case: Simple component that re-renders frequently
const BadMemoizedButton = React.memo(function BadMemoizedButton({ onClick, children }) {
  console.log('BadMemoizedButton rendering');
  
  // This is a simple component - memo overhead > benefit
  return (
    <button onClick={onClick} style={{ padding: '5px 10px' }}>
      {children}
    </button>
  );
});

// ✅ Better: Just a regular component
function SimpleButton({ onClick, children }) {
  return (
    <button onClick={onClick} style={{ padding: '5px 10px' }}>
      {children}
    </button>
  );
}

// Custom comparison function for React.memo
const UserCard = React.memo(function UserCard({ user, onSelect }) {
  console.log('UserCard rendering for user:', user.id);
  
  return (
    <div 
      style={{ 
        padding: '15px', 
        border: '1px solid #ddd', 
        margin: '5px',
        cursor: 'pointer'
      }}
      onClick={() => onSelect(user.id)}
    >
      <h4>{user.name}</h4>
      <p>{user.email}</p>
      <small>Last active: {user.lastActive}</small>
    </div>
  );
}, (prevProps, nextProps) => {
  // Custom comparison: only re-render if user data actually changed
  return (
    prevProps.user.id === nextProps.user.id &&
    prevProps.user.name === nextProps.user.name &&
    prevProps.user.email === nextProps.user.email &&
    prevProps.user.lastActive === nextProps.user.lastActive
    // Note: onSelect function reference might change, but we ignore it
  );
});

function MemoDemo() {
  const [count, setCount] = useState(0);
  const [users, setUsers] = useState([
    { id: 1, name: 'Alice', email: 'alice@example.com', lastActive: '2024-01-01' },
    { id: 2, name: 'Bob', email: 'bob@example.com', lastActive: '2024-01-02' },
  ]);
  
  const chartConfig = { theme: 'dark', animated: true };
  const chartData = [
    { x: 1, value: 10 },
    { x: 2, value: 20 },
    { x: 3, value: 15 }
  ];
  
  const handleUserSelect = (userId) => {
    console.log('Selected user:', userId);
  };
  
  return (
    <div>
      <h3>React.memo Demo</h3>
      
      <div style={{ marginBottom: '20px' }}>
        <button onClick={() => setCount(count + 1)}>
          Count: {count} (triggers parent re-render)
        </button>
      </div>
      
      {/* This won't re-render when count changes */}
      <ExpensiveChart data={chartData} config={chartConfig} />
      
      {/* These won't re-render when count changes (custom comparison) */}
      <div>
        {users.map(user => (
          <UserCard 
            key={user.id} 
            user={user} 
            onSelect={handleUserSelect}
          />
        ))}
      </div>
      
      {/* These WILL re-render on every count change */}
      <div>
        <BadMemoizedButton onClick={() => console.log('Bad button')}>
          Bad Memoized Button
        </BadMemoizedButton>
        <SimpleButton onClick={() => console.log('Simple button')}>
          Simple Button (Better)
        </SimpleButton>
      </div>
    </div>
  );
}

function heavyComputation(value) {
  // Simulate expensive computation
  let result = value;
  for (let i = 0; i < 100000; i++) {
    result = Math.sin(result) + Math.cos(result);
  }
  return result;
}
```

### 🎯 useMemo - Value Memoization

**Interview Critical Point:** useMemo caches expensive computations, but comes with its own overhead. Use it judiciously.

```jsx
function UseMemoDemo() {
  const [items, setItems] = useState([]);
  const [filter, setFilter] = useState('');
  const [sortBy, setSortBy] = useState('name');
  const [count, setCount] = useState(0); // Unrelated state
  
  // ✅ Good use case: Expensive computation that depends on specific values
  const processedItems = useMemo(() => {
    console.log('🔄 Processing items (expensive operation)');
    
    let filtered = items.filter(item => 
      item.name.toLowerCase().includes(filter.toLowerCase())
    );
    
    // Expensive sorting
    filtered.sort((a, b) => {
      if (sortBy === 'name') return a.name.localeCompare(b.name);
      if (sortBy === 'value') return b.value - a.value;
      if (sortBy === 'date') return new Date(b.date) - new Date(a.date);
      return 0;
    });
    
    // Expensive processing for each item
    return filtered.map(item => ({
      ...item,
      processed: heavyComputation(item.value),
      formatted: formatItem(item)
    }));
  }, [items, filter, sortBy]); // Only depends on relevant values, NOT count
  
  // ❌ Bad use case: Simple computation
  const badMemoizedValue = useMemo(() => {
    return count * 2; // This is too simple to justify useMemo overhead
  }, [count]);
  
  // ✅ Better: Just calculate directly
  const simpleValue = count * 2;
  
  // ❌ Another bad use case: No dependencies
  const alwaysNewObject = useMemo(() => {
    return { timestamp: Date.now() }; // Always different!
  }, []); // Empty deps but value always changes
  
  // ✅ Good use case: Stable object reference
  const stableConfig = useMemo(() => {
    return {
      theme: 'dark',
      locale: 'en-US',
      features: ['feature1', 'feature2']
    };
  }, []); // Truly stable
  
  const addItems = () => {
    const newItems = Array.from({ length: 1000 }, (_, i) => ({
      id: Date.now() + i,
      name: `Item ${i}`,
      value: Math.random() * 100,
      date: new Date(Date.now() - Math.random() * 10000000000).toISOString()
    }));
    setItems(prev => [...prev, ...newItems]);
  };
  
  return (
    <div>
      <h3>useMemo Demo</h3>
      
      <div style={{ marginBottom: '20px' }}>
        <button onClick={addItems}>Add 1000 Items</button>
        <button onClick={() => setCount(count + 1)}>
          Count: {count} (doesn't affect processing)
        </button>
        <button onClick={() => setItems([])}>Clear Items</button>
      </div>
      
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Filter items..."
          style={{ marginRight: '10px', padding: '5px' }}
        />
        
        <select 
          value={sortBy} 
          onChange={(e) => setSortBy(e.target.value)}
          style={{ padding: '5px' }}
        >
          <option value="name">Sort by Name</option>
          <option value="value">Sort by Value</option>
          <option value="date">Sort by Date</option>
        </select>
      </div>
      
      <div style={{ marginBottom: '10px' }}>
        <strong>Results:</strong> {processedItems.length} items
        <br />
        <small>Simple value: {simpleValue}</small>
        <br />
        <small>Bad memoized: {badMemoizedValue}</small>
      </div>
      
      <div style={{ maxHeight: '200px', overflow: 'auto' }}>
        {processedItems.slice(0, 50).map(item => (
          <div key={item.id} style={{ padding: '5px', borderBottom: '1px solid #eee' }}>
            {item.formatted}
          </div>
        ))}
      </div>
    </div>
  );
}

function formatItem(item) {
  // Simulate expensive formatting
  return `${item.name} (${item.value.toFixed(2)}) - ${new Date(item.date).toLocaleDateString()}`;
}
```

### 🎯 useCallback - Function Memoization

**Interview Critical Point:** useCallback is only useful when passing functions to memoized components or as dependencies to other hooks.

```jsx
function UseCallbackDemo() {
  const [users, setUsers] = useState([]);
  const [filter, setFilter] = useState('');
  const [sortOrder, setSortOrder] = useState('asc');
  
  // ❌ Bad use case: Function not passed to memoized component
  const badMemoizedHandler = useCallback(() => {
    console.log('This useCallback is unnecessary');
  }, []);
  
  // ✅ Good use case: Function passed to memoized component
  const handleUserClick = useCallback((userId) => {
    console.log('User clicked:', userId);
    // In real app, might navigate or update state
  }, []); // No dependencies, stable function
  
  // ✅ Good use case: Function used in effect dependencies
  const fetchUsers = useCallback(async (searchTerm) => {
    console.log('Fetching users with term:', searchTerm);
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 500));
    
    const mockUsers = Array.from({ length: 100 }, (_, i) => ({
      id: i,
      name: `User ${i}`,
      email: `user${i}@example.com`,
      active: Math.random() > 0.5
    })).filter(user => 
      user.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
    
    setUsers(mockUsers);
  }, []); // No dependencies, could also include API base URL etc.
  
  // ✅ Good use case: Function with dependencies used by memoized component
  const handleSort = useCallback((field) => {
    setUsers(prevUsers => {
      const sorted = [...prevUsers].sort((a, b) => {
        const aVal = a[field];
        const bVal = b[field];
        
        if (sortOrder === 'asc') {
          return aVal > bVal ? 1 : -1;
        } else {
          return aVal < bVal ? 1 : -1;
        }
      });
      return sorted;
    });
  }, [sortOrder]); // Depends on sortOrder
  
  // Effect using memoized function
  useEffect(() => {
    fetchUsers(filter);
  }, [fetchUsers, filter]);
  
  return (
    <div>
      <h3>useCallback Demo</h3>
      
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="Search users..."
          style={{ marginRight: '10px', padding: '5px' }}
        />
        
        <select
          value={sortOrder}
          onChange={(e) => setSortOrder(e.target.value)}
          style={{ padding: '5px' }}
        >
          <option value="asc">Ascending</option>
          <option value="desc">Descending</option>
        </select>
      </div>
      
      <div style={{ marginBottom: '10px' }}>
        <button onClick={() => handleSort('name')}>Sort by Name</button>
        <button onClick={() => handleSort('email')}>Sort by Email</button>
        <button onClick={badMemoizedHandler}>Bad Memoized Handler</button>
      </div>
      
      <UserList 
        users={users} 
        onUserClick={handleUserClick}
        onSort={handleSort}
      />
    </div>
  );
}

// Memoized component that benefits from useCallback
const UserList = React.memo(function UserList({ users, onUserClick, onSort }) {
  console.log('UserList rendering with', users.length, 'users');
  
  return (
    <div>
      <div style={{ marginBottom: '10px' }}>
        <strong>Found {users.length} users</strong>
      </div>
      
      <div style={{ maxHeight: '300px', overflow: 'auto' }}>
        {users.map(user => (
          <MemoizedUserItem 
            key={user.id}
            user={user}
            onClick={onUserClick}
          />
        ))}
      </div>
    </div>
  );
});

const MemoizedUserItem = React.memo(function MemoizedUserItem({ user, onClick }) {
  console.log('Rendering user item:', user.id);
  
  return (
    <div 
      style={{ 
        padding: '10px', 
        border: '1px solid #ddd', 
        margin: '2px',
        cursor: 'pointer',
        backgroundColor: user.active ? '#e8f5e8' : '#f8f8f8'
      }}
      onClick={() => onClick(user.id)}
    >
      <strong>{user.name}</strong>
      <br />
      <small>{user.email}</small>
      <span style={{ 
        float: 'right', 
        color: user.active ? 'green' : 'gray' 
      }}>
        {user.active ? 'Active' : 'Inactive'}
      </span>
    </div>
  );
});
```

### 🎯 When NOT to Use Memoization

**Interview Critical Point:** Over-memoization can hurt performance. Know when to avoid it.

```jsx
function AntiPatternsDemo() {
  const [count, setCount] = useState(0);
  const [name, setName] = useState('');
  
  // ❌ Don't memoize primitive values that are cheap to compute
  const badMemoizedString = useMemo(() => {
    return `Hello ${name}`; // String concatenation is fast
  }, [name]);
  
  // ❌ Don't memoize objects that always change
  const badMemoizedObject = useMemo(() => {
    return {
      timestamp: Date.now(), // Always different!
      random: Math.random()   // Always different!
    };
  }, [count]);
  
  // ❌ Don't memoize with too many dependencies
  const overMemoizedValue = useMemo(() => {
    return count + name.length; // Simple computation
  }, [count, name]); // Dependencies cost more than computation
  
  // ❌ Don't use useCallback for inline functions in simple components
  const badInlineCallback = useCallback(() => {
    console.log('This callback is unnecessary overhead');
  }, []);
  
  // ❌ Don't memoize components that always re-render
  const AlwaysChangingComponent = React.memo(function AlwaysChangingComponent() {
    const [timestamp] = useState(Date.now()); // Always different initial state
    return <div>Timestamp: {timestamp}</div>;
  });
  
  // ✅ Better patterns
  const simpleString = `Hello ${name}`; // Direct computation
  const simpleSum = count + name.length; // Direct computation
  
  const handleSimpleClick = () => {
    console.log('Simple handler without useCallback');
  };
  
  return (
    <div>
      <h3>When NOT to Use Memoization</h3>
      
      <div style={{ marginBottom: '20px' }}>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter name"
          style={{ marginRight: '10px', padding: '5px' }}
        />
        
        <button onClick={() => setCount(count + 1)}>
          Count: {count}
        </button>
      </div>
      
      <div style={{ marginBottom: '20px' }}>
        <h4>Anti-patterns (avoid these):</h4>
        <p>Bad memoized string: {badMemoizedString}</p>
        <p>Bad memoized object: {JSON.stringify(badMemoizedObject)}</p>
        <p>Over-memoized value: {overMemoizedValue}</p>
        <button onClick={badInlineCallback}>Bad Callback</button>
        <AlwaysChangingComponent />
      </div>
      
      <div>
        <h4>Better patterns:</h4>
        <p>Simple string: {simpleString}</p>
        <p>Simple sum: {simpleSum}</p>
        <button onClick={handleSimpleClick}>Simple Handler</button>
      </div>
    </div>
  );
}

// Performance comparison
function MemoizationComparison() {
  const [data, setData] = useState([]);
  const [trigger, setTrigger] = useState(0);
  
  useEffect(() => {
    const items = Array.from({ length: 10000 }, (_, i) => ({
      id: i,
      value: Math.random() * 100,
      category: ['A', 'B', 'C'][i % 3]
    }));
    setData(items);
  }, []);
  
  return (
    <div>
      <h3>Memoization Performance Comparison</h3>
      
      <button 
        onClick={() => setTrigger(trigger + 1)}
        style={{ marginBottom: '20px' }}
      >
        Trigger Re-render ({trigger})
      </button>
      
      <div style={{ display: 'flex', gap: '20px' }}>
        <div style={{ flex: 1 }}>
          <h4>Without Memoization</h4>
          <Profiler id="Without-Memo" onRender={(id, phase, actualDuration) => {
            console.log(`${id}: ${actualDuration}ms`);
          }}>
            <UnmemoizedExpensiveComponent data={data} trigger={trigger} />
          </Profiler>
        </div>
        
        <div style={{ flex: 1 }}>
          <h4>With Proper Memoization</h4>
          <Profiler id="With-Memo" onRender={(id, phase, actualDuration) => {
            console.log(`${id}: ${actualDuration}ms`);
          }}>
            <MemoizedExpensiveComponent data={data} trigger={trigger} />
          </Profiler>
        </div>
      </div>
    </div>
  );
}

function UnmemoizedExpensiveComponent({ data, trigger }) {
  console.log('UnmemoizedExpensiveComponent rendering');
  
  // Expensive computation on every render
  const processedData = data.reduce((acc, item) => {
    const category = item.category;
    if (!acc[category]) acc[category] = [];
    acc[category].push(item);
    return acc;
  }, {});
  
  const stats = Object.entries(processedData).map(([category, items]) => ({
    category,
    count: items.length,
    average: items.reduce((sum, item) => sum + item.value, 0) / items.length
  }));
  
  return (
    <div style={{ padding: '10px', border: '1px solid #dc3545' }}>
      <p>Trigger: {trigger}</p>
      {stats.map(stat => (
        <div key={stat.category}>
          {stat.category}: {stat.count} items (avg: {stat.average.toFixed(2)})
        </div>
      ))}
    </div>
  );
}

const MemoizedExpensiveComponent = React.memo(function MemoizedExpensiveComponent({ data, trigger }) {
  console.log('MemoizedExpensiveComponent rendering');
  
  // Memoized expensive computation
  const processedData = useMemo(() => {
    return data.reduce((acc, item) => {
      const category = item.category;
      if (!acc[category]) acc[category] = [];
      acc[category].push(item);
      return acc;
    }, {});
  }, [data]); // Only depends on data, not trigger
  
  const stats = useMemo(() => {
    return Object.entries(processedData).map(([category, items]) => ({
      category,
      count: items.length,
      average: items.reduce((sum, item) => sum + item.value, 0) / items.length
    }));
  }, [processedData]);
  
  return (
    <div style={{ padding: '10px', border: '1px solid #28a745' }}>
      <p>Trigger: {trigger}</p>
      {stats.map(stat => (
        <div key={stat.category}>
          {stat.category}: {stat.count} items (avg: {stat.average.toFixed(2)})
        </div>
      ))}
    </div>
  );
});
```

---

## Master-Level Interview Questions

### Q: Explain React Fiber and how it enables concurrent rendering.

**A:** Fiber is React's reconciliation algorithm that breaks work into units and can pause/resume rendering. It uses a linked list structure where each fiber node represents a component. This enables:
- **Time slicing**: Breaking work into chunks that fit in frame budgets
- **Priority-based scheduling**: High-priority updates (user input) interrupt low-priority ones
- **Concurrent features**: useTransition, useDeferredValue, Suspense

The work loop can yield control back to the browser, preventing blocking.

### Q: When would you use useTransition vs useDeferredValue?

**A:** 
- **useTransition**: For state updates you control that can be interrupted (tab switching, filters)
- **useDeferredValue**: For values from props/external sources that you want to defer (search results, heavy computations)

useTransition gives you control over the update itself, useDeferredValue defers using a value until more urgent work is done.

### Q: How does hydration work and what are common pitfalls?

**A:** Hydration attaches event listeners and state to server-rendered HTML. Pitfalls:
- **Mismatches**: Different content on server vs client (timestamps, random values)
- **Blocking**: Large hydration can block the main thread
- **All-or-nothing**: Traditional hydration happens all at once

Solutions: useEffect for client-only content, suppressHydrationWarning for intentional mismatches, progressive hydration strategies.

### Q: What's the difference between Server Components and traditional SSR?

**A:** 
- **SSR**: Renders components to HTML on server, then hydrates on client
- **Server Components**: Run only on server, send serialized output (not HTML) to client, never hydrate

Server Components can access databases directly, have zero client bundle impact, but can't use state/effects. Mix with Client Components for interactivity.

### Q: When should you NOT use React.memo?

**A:** Avoid when:
- Component is simple and renders quickly
- Props change frequently 
- Component always re-renders (has changing internal state)
- The memoization overhead exceeds the rendering cost

Profile first, optimize second.

### Q: How does React's reconciliation decide what to update?

**A:** Uses heuristic diffing:
1. **Element type changes**: Unmount old tree, mount new
2. **Same type**: Update props, recurse into children  
3. **Keys**: Help identify moved/added/removed elements
4. **Bailout conditions**: Shallow prop comparison, state comparison

This achieves O(n) instead of O(n³) complexity.

### Q: Explain the difference between useMemo dependencies and effect dependencies.

**A:** 
- **useMemo**: Recalculates when dependencies change, returns cached value otherwise
- **useEffect**: Runs when dependencies change, for side effects

Both use `Object.is` for comparison. Missing dependencies cause stale closures. useMemo is for computed values, useEffect is for side effects.

---

**🎯 Key Takeaways for Senior React Interviews:**

1. **Fiber Architecture**: Understand reconciliation, work units, and priority scheduling
2. **Concurrent Features**: Master useTransition, useDeferredValue, and their use cases  
3. **Suspense**: Know lazy loading, data fetching patterns, and error boundaries
4. **Server Components**: Understand the paradigm shift and boundaries with Client Components
5. **Hydration**: Know SSR process, mismatches, and progressive strategies
6. **Performance**: Use Profiler API and understand when/when not to memoize
7. **Real-world Application**: Can implement complex UIs with proper performance considerations

This advanced knowledge demonstrates deep React expertise and architectural thinking required for senior roles.
