# React Ecosystem Deep-Dive: Real-World Interview Mastery

> **Interview Focus:** This guide covers the essential React ecosystem tools and libraries that senior developers use daily. Expect deep questions about routing, forms, data fetching, and styling approaches.

## Table of Contents

1. [React Router v6: Modern Routing](#react-router-v6-modern-routing)
   - [Nested Routes & Layout Patterns](#nested-routes--layout-patterns)
   - [Lazy Loading & Code Splitting](#lazy-loading--code-splitting)
   - [Navigation Hooks & Dynamic Routing](#navigation-hooks--dynamic-routing)
   - [Protected Routes & Route Guards](#protected-routes--route-guards)

2. [Forms & Validation Ecosystem](#forms--validation-ecosystem)
   - [React Hook Form: Performance-First Forms](#react-hook-form-performance-first-forms)
   - [Formik: Feature-Rich Form Management](#formik-feature-rich-form-management)
   - [Validation with Yup & Zod](#validation-with-yup--zod)
   - [Form Libraries Comparison](#form-libraries-comparison)

3. [Data Fetching Strategies](#data-fetching-strategies)
   - [Native Fetch with AbortController](#native-fetch-with-abortcontroller)
   - [TanStack Query (React Query): Advanced Caching](#tanstack-query-react-query-advanced-caching)
   - [SWR: Stale-While-Revalidate](#swr-stale-while-revalidate)
   - [Data Fetching Comparison Matrix](#data-fetching-comparison-matrix)

4. [Styling Approaches & Trade-offs](#styling-approaches--trade-offs)
   - [CSS Modules: Scoped Styling](#css-modules-scoped-styling)
   - [Styled Components: CSS-in-JS](#styled-components-css-in-js)
   - [Tailwind CSS: Utility-First](#tailwind-css-utility-first)
   - [Styling Strategy Decision Matrix](#styling-strategy-decision-matrix)

5. [Integration Patterns & Best Practices](#integration-patterns--best-practices)
   - [Ecosystem Architecture Patterns](#ecosystem-architecture-patterns)
   - [Performance Optimization](#performance-optimization)
   - [Testing Strategies](#testing-strategies)

6. [Interview Questions & Real-World Scenarios](#interview-questions--real-world-scenarios)
   - [Architecture Design Questions](#architecture-design-questions)
   - [Performance & Optimization Scenarios](#performance--optimization-scenarios)
   - [Trade-off Analysis](#trade-off-analysis)

---

## React Router v6: Modern Routing

> **Interview Expectation:** Deep understanding of React Router v6's declarative routing, nested routes, and performance patterns.

### 🎯 Nested Routes & Layout Patterns

**Interview Critical Point:** React Router v6 uses a nested, declarative approach with `Outlet` for layout composition.

```jsx
import { 
  createBrowserRouter, 
  RouterProvider, 
  Route, 
  createRoutesFromElements,
  Outlet, 
  Link, 
  useLocation,
  useNavigate,
  useParams 
} from 'react-router-dom';

// Root layout component
function RootLayout() {
  const location = useLocation();
  
  return (
    <div className="app">
      {/* Global navigation */}
      <nav className="navbar">
        <div className="nav-brand">
          <Link to="/">MyApp</Link>
        </div>
        <div className="nav-links">
          <Link 
            to="/dashboard" 
            className={location.pathname.startsWith('/dashboard') ? 'active' : ''}
          >
            Dashboard
          </Link>
          <Link 
            to="/products" 
            className={location.pathname.startsWith('/products') ? 'active' : ''}
          >
            Products
          </Link>
          <Link 
            to="/users" 
            className={location.pathname.startsWith('/users') ? 'active' : ''}
          >
            Users
          </Link>
        </div>
      </nav>
      
      {/* Main content area */}
      <main className="main-content">
        {/* This is where nested routes will render */}
        <Outlet />
      </main>
      
      {/* Global footer */}
      <footer className="footer">
        <p>&copy; 2024 MyApp. All rights reserved.</p>
      </footer>
    </div>
  );
}

// Dashboard layout with sidebar
function DashboardLayout() {
  const location = useLocation();
  
  return (
    <div className="dashboard-layout">
      <aside className="sidebar">
        <nav className="sidebar-nav">
          <Link 
            to="/dashboard" 
            className={location.pathname === '/dashboard' ? 'active' : ''}
            end // Only active when exact match
          >
            Overview
          </Link>
          <Link 
            to="/dashboard/analytics" 
            className={location.pathname.includes('/analytics') ? 'active' : ''}
          >
            Analytics
          </Link>
          <Link 
            to="/dashboard/reports" 
            className={location.pathname.includes('/reports') ? 'active' : ''}
          >
            Reports
          </Link>
          <Link 
            to="/dashboard/settings" 
            className={location.pathname.includes('/settings') ? 'active' : ''}
          >
            Settings
          </Link>
        </nav>
      </aside>
      
      <div className="dashboard-content">
        {/* Breadcrumb navigation */}
        <DashboardBreadcrumb />
        
        {/* Dashboard nested routes render here */}
        <Outlet />
      </div>
    </div>
  );
}

// Breadcrumb component
function DashboardBreadcrumb() {
  const location = useLocation();
  const pathSegments = location.pathname.split('/').filter(Boolean);
  
  const breadcrumbItems = pathSegments.map((segment, index) => {
    const path = '/' + pathSegments.slice(0, index + 1).join('/');
    const isLast = index === pathSegments.length - 1;
    
    return {
      label: segment.charAt(0).toUpperCase() + segment.slice(1),
      path,
      isLast
    };
  });
  
  return (
    <nav className="breadcrumb" aria-label="Breadcrumb">
      <ol className="breadcrumb-list">
        <li>
          <Link to="/">Home</Link>
        </li>
        {breadcrumbItems.map((item, index) => (
          <li key={item.path}>
            <span className="separator"> / </span>
            {item.isLast ? (
              <span className="current" aria-current="page">
                {item.label}
              </span>
            ) : (
              <Link to={item.path}>{item.label}</Link>
            )}
          </li>
        ))}
      </ol>
    </nav>
  );
}

// Product layout with tabs
function ProductLayout() {
  const { productId } = useParams();
  const location = useLocation();
  
  return (
    <div className="product-layout">
      <div className="product-header">
        <h1>Product {productId}</h1>
        
        {/* Product tabs */}
        <nav className="product-tabs">
          <Link 
            to={`/products/${productId}`}
            className={location.pathname === `/products/${productId}` ? 'active' : ''}
            end
          >
            Details
          </Link>
          <Link 
            to={`/products/${productId}/reviews`}
            className={location.pathname.includes('/reviews') ? 'active' : ''}
          >
            Reviews
          </Link>
          <Link 
            to={`/products/${productId}/variants`}
            className={location.pathname.includes('/variants') ? 'active' : ''}
          >
            Variants
          </Link>
          <Link 
            to={`/products/${productId}/analytics`}
            className={location.pathname.includes('/analytics') ? 'active' : ''}
          >
            Analytics
          </Link>
        </nav>
      </div>
      
      <div className="product-content">
        <Outlet context={{ productId }} />
      </div>
    </div>
  );
}

// Router configuration using createBrowserRouter (recommended approach)
const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<RootLayout />}>
      {/* Home page */}
      <Route index element={<HomePage />} />
      
      {/* Dashboard routes with nested layout */}
      <Route path="dashboard" element={<DashboardLayout />}>
        <Route index element={<DashboardOverview />} />
        <Route path="analytics" element={<DashboardAnalytics />}>
          <Route index element={<AnalyticsOverview />} />
          <Route path="traffic" element={<TrafficAnalytics />} />
          <Route path="conversion" element={<ConversionAnalytics />} />
        </Route>
        <Route path="reports" element={<DashboardReports />}>
          <Route index element={<ReportsOverview />} />
          <Route path="sales" element={<SalesReport />} />
          <Route path="user-activity" element={<UserActivityReport />} />
        </Route>
        <Route path="settings" element={<DashboardSettings />}>
          <Route index element={<GeneralSettings />} />
          <Route path="account" element={<AccountSettings />} />
          <Route path="notifications" element={<NotificationSettings />} />
        </Route>
      </Route>
      
      {/* Product routes */}
      <Route path="products" element={<ProductsLayout />}>
        <Route index element={<ProductsList />} />
        <Route path=":productId" element={<ProductLayout />}>
          <Route index element={<ProductDetails />} />
          <Route path="reviews" element={<ProductReviews />} />
          <Route path="variants" element={<ProductVariants />} />
          <Route path="analytics" element={<ProductAnalytics />} />
        </Route>
      </Route>
      
      {/* User routes */}
      <Route path="users" element={<UsersLayout />}>
        <Route index element={<UsersList />} />
        <Route path=":userId" element={<UserProfile />} />
        <Route path=":userId/edit" element={<EditUser />} />
      </Route>
      
      {/* Authentication routes */}
      <Route path="auth" element={<AuthLayout />}>
        <Route path="login" element={<Login />} />
        <Route path="register" element={<Register />} />
        <Route path="forgot-password" element={<ForgotPassword />} />
        <Route path="reset-password/:token" element={<ResetPassword />} />
      </Route>
      
      {/* Error routes */}
      <Route path="*" element={<NotFound />} />
    </Route>
  )
);

// App component
function App() {
  return <RouterProvider router={router} />;
}

// Example page components
function HomePage() {
  const navigate = useNavigate();
  
  return (
    <div className="home-page">
      <h1>Welcome to MyApp</h1>
      <div className="home-actions">
        <button onClick={() => navigate('/dashboard')}>
          Go to Dashboard
        </button>
        <button onClick={() => navigate('/products')}>
          Browse Products
        </button>
      </div>
    </div>
  );
}

function DashboardOverview() {
  return (
    <div className="dashboard-overview">
      <h2>Dashboard Overview</h2>
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Users</h3>
          <div className="metric-value">12,543</div>
        </div>
        <div className="metric-card">
          <h3>Revenue</h3>
          <div className="metric-value">$45,231</div>
        </div>
        <div className="metric-card">
          <h3>Orders</h3>
          <div className="metric-value">1,234</div>
        </div>
        <div className="metric-card">
          <h3>Conversion Rate</h3>
          <div className="metric-value">3.2%</div>
        </div>
      </div>
    </div>
  );
}

export default App;
```

### 🎯 Lazy Loading & Code Splitting

**Interview Critical Point:** Lazy loading reduces initial bundle size and improves app performance through route-based code splitting.

```jsx
import { lazy, Suspense } from 'react';
import { createBrowserRouter, createRoutesFromElements, Route } from 'react-router-dom';

// Lazy-loaded components
const Dashboard = lazy(() => import('./pages/Dashboard'));
const Products = lazy(() => import('./pages/Products'));
const ProductDetails = lazy(() => import('./pages/ProductDetails'));
const Analytics = lazy(() => import('./pages/Analytics'));
const Reports = lazy(() => import('./pages/Reports'));
const UserProfile = lazy(() => import('./pages/UserProfile'));

// Advanced lazy loading with error handling and retry logic
const lazyWithRetry = (importFunc, retries = 3) => {
  return lazy(async () => {
    let lastError;
    
    for (let i = 0; i < retries; i++) {
      try {
        return await importFunc();
      } catch (error) {
        lastError = error;
        
        // Wait before retrying (exponential backoff)
        if (i < retries - 1) {
          await new Promise(resolve => setTimeout(resolve, 1000 * Math.pow(2, i)));
        }
      }
    }
    
    throw lastError;
  });
};

// Lazy components with retry logic
const DashboardWithRetry = lazyWithRetry(() => import('./pages/Dashboard'));
const ProductsWithRetry = lazyWithRetry(() => import('./pages/Products'));

// Loading component
function LoadingSpinner({ message = 'Loading...' }) {
  return (
    <div className="loading-container">
      <div className="spinner" aria-hidden="true">
        <div className="spinner-circle"></div>
      </div>
      <p className="loading-message">{message}</p>
    </div>
  );
}

// Error boundary for lazy loading failures
class LazyLoadErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('Lazy loading error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="error-container">
          <h2>Something went wrong</h2>
          <p>Failed to load this page. Please try refreshing.</p>
          <button onClick={() => window.location.reload()}>
            Refresh Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

// Preloading utility for better UX
const preloadRoute = (routeImport) => {
  const componentImport = routeImport();
  return componentImport;
};

// Navigation component with preloading
function Navigation() {
  const navigate = useNavigate();
  
  // Preload routes on hover for better perceived performance
  const handleMouseEnter = (routeImport) => {
    preloadRoute(routeImport);
  };
  
  return (
    <nav className="navigation">
      <Link 
        to="/dashboard"
        onMouseEnter={() => handleMouseEnter(() => import('./pages/Dashboard'))}
      >
        Dashboard
      </Link>
      <Link 
        to="/products"
        onMouseEnter={() => handleMouseEnter(() => import('./pages/Products'))}
      >
        Products
      </Link>
      <Link 
        to="/analytics"
        onMouseEnter={() => handleMouseEnter(() => import('./pages/Analytics'))}
      >
        Analytics
      </Link>
    </nav>
  );
}

// Router with lazy loading and proper suspense boundaries
const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<RootLayout />}>
      <Route index element={<HomePage />} />
      
      {/* Lazy-loaded routes with different loading states */}
      <Route 
        path="dashboard/*" 
        element={
          <LazyLoadErrorBoundary>
            <Suspense fallback={<LoadingSpinner message="Loading Dashboard..." />}>
              <DashboardWithRetry />
            </Suspense>
          </LazyLoadErrorBoundary>
        } 
      />
      
      <Route 
        path="products/*" 
        element={
          <LazyLoadErrorBoundary>
            <Suspense fallback={<LoadingSpinner message="Loading Products..." />}>
              <ProductsWithRetry />
            </Suspense>
          </LazyLoadErrorBoundary>
        } 
      />
      
      <Route 
        path="analytics/*" 
        element={
          <LazyLoadErrorBoundary>
            <Suspense fallback={<LoadingSpinner message="Loading Analytics..." />}>
              <Analytics />
            </Suspense>
          </LazyLoadErrorBoundary>
        } 
      />
      
      <Route 
        path="users/:userId" 
        element={
          <LazyLoadErrorBoundary>
            <Suspense fallback={<LoadingSpinner message="Loading User Profile..." />}>
              <UserProfile />
            </Suspense>
          </LazyLoadErrorBoundary>
        } 
      />
      
      <Route path="*" element={<NotFound />} />
    </Route>
  )
);

// Bundle analysis component for development
function BundleAnalyzer() {
  const [bundleInfo, setBundleInfo] = useState(null);
  
  useEffect(() => {
    // In development, you can analyze bundle sizes
    if (process.env.NODE_ENV === 'development') {
      import('webpack-bundle-analyzer').then(({ getBundleInfo }) => {
        setBundleInfo(getBundleInfo());
      });
    }
  }, []);
  
  if (process.env.NODE_ENV !== 'development') return null;
  
  return (
    <div className="bundle-analyzer">
      <h3>Bundle Analysis (Dev Only)</h3>
      {bundleInfo && (
        <pre>{JSON.stringify(bundleInfo, null, 2)}</pre>
      )}
    </div>
  );
}

// Performance monitoring for route loading
function RoutePerformanceMonitor() {
  useEffect(() => {
    const observer = new PerformanceObserver((list) => {
      list.getEntries().forEach((entry) => {
        if (entry.entryType === 'navigation') {
          console.log('Route load time:', entry.loadEventEnd - entry.loadEventStart);
        }
      });
    });
    
    observer.observe({ entryTypes: ['navigation'] });
    
    return () => observer.disconnect();
  }, []);
  
  return null;
}

export default router;
```

### 🎯 Navigation Hooks & Dynamic Routing

**Interview Critical Point:** Understanding useNavigate, useParams, useSearchParams, and programmatic navigation patterns.

```jsx
import { 
  useNavigate, 
  useParams, 
  useSearchParams, 
  useLocation,
  generatePath,
  matchPath,
  Navigate
} from 'react-router-dom';

// Advanced navigation component
function AdvancedNavigation() {
  const navigate = useNavigate();
  const location = useLocation();
  const [searchParams, setSearchParams] = useSearchParams();
  
  // Programmatic navigation with state
  const navigateWithState = (path, state = {}) => {
    navigate(path, { 
      state: { 
        ...state, 
        from: location.pathname,
        timestamp: Date.now()
      } 
    });
  };
  
  // Navigation with search params preservation
  const navigatePreservingParams = (path) => {
    const currentParams = Object.fromEntries(searchParams.entries());
    navigate({
      pathname: path,
      search: new URLSearchParams(currentParams).toString()
    });
  };
  
  // Conditional navigation based on user permissions
  const navigateWithPermissionCheck = async (path, requiredPermission) => {
    const hasPermission = await checkUserPermission(requiredPermission);
    
    if (hasPermission) {
      navigate(path);
    } else {
      navigate('/unauthorized', { 
        state: { 
          attemptedPath: path,
          requiredPermission 
        } 
      });
    }
  };
  
  // Navigation with confirmation
  const navigateWithConfirmation = (path, message = 'Are you sure you want to leave?') => {
    if (window.confirm(message)) {
      navigate(path);
    }
  };
  
  // Replace vs Push navigation
  const handleTabNavigation = (tabPath) => {
    // Use replace for tab navigation to avoid cluttering history
    navigate(tabPath, { replace: true });
  };
  
  return (
    <div className="advanced-navigation">
      <button onClick={() => navigateWithState('/dashboard', { section: 'overview' })}>
        Dashboard with State
      </button>
      
      <button onClick={() => navigatePreservingParams('/products')}>
        Products (Keep Filters)
      </button>
      
      <button onClick={() => navigateWithPermissionCheck('/admin', 'admin_access')}>
        Admin Panel
      </button>
      
      <button onClick={() => navigateWithConfirmation('/logout', 'Do you want to logout?')}>
        Logout
      </button>
      
      <button onClick={() => navigate(-1)}>
        Go Back
      </button>
      
      <button onClick={() => navigate(1)}>
        Go Forward
      </button>
    </div>
  );
}

// Dynamic routing with params validation
function DynamicProductPage() {
  const { productId, category, variant } = useParams();
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();
  
  // Validate params
  useEffect(() => {
    const validateParams = async () => {
      // Check if product exists
      const productExists = await checkProductExists(productId);
      if (!productExists) {
        navigate('/products/not-found', { replace: true });
        return;
      }
      
      // Validate category
      if (category) {
        const validCategories = await getValidCategories();
        if (!validCategories.includes(category)) {
          // Redirect to product without invalid category
          navigate(`/products/${productId}`, { replace: true });
          return;
        }
      }
    };
    
    validateParams();
  }, [productId, category, navigate]);
  
  // URL construction helpers
  const buildProductUrl = (id, options = {}) => {
    let path = `/products/${id}`;
    
    if (options.category) {
      path += `/category/${options.category}`;
    }
    
    if (options.variant) {
      path += `/variant/${options.variant}`;
    }
    
    return path;
  };
  
  // Search params management
  const updateFilters = (newFilters) => {
    const currentParams = Object.fromEntries(searchParams.entries());
    const updatedParams = { ...currentParams, ...newFilters };
    
    // Remove empty params
    Object.keys(updatedParams).forEach(key => {
      if (!updatedParams[key]) {
        delete updatedParams[key];
      }
    });
    
    setSearchParams(updatedParams);
  };
  
  // Get current filter values
  const filters = {
    sortBy: searchParams.get('sortBy') || 'name',
    order: searchParams.get('order') || 'asc',
    minPrice: searchParams.get('minPrice') || '',
    maxPrice: searchParams.get('maxPrice') || '',
    inStock: searchParams.get('inStock') === 'true'
  };
  
  return (
    <div className="dynamic-product-page">
      <h1>Product {productId}</h1>
      {category && <p>Category: {category}</p>}
      {variant && <p>Variant: {variant}</p>}
      
      {/* Filter controls */}
      <div className="filters">
        <select 
          value={filters.sortBy} 
          onChange={(e) => updateFilters({ sortBy: e.target.value })}
        >
          <option value="name">Name</option>
          <option value="price">Price</option>
          <option value="rating">Rating</option>
        </select>
        
        <select 
          value={filters.order} 
          onChange={(e) => updateFilters({ order: e.target.value })}
        >
          <option value="asc">Ascending</option>
          <option value="desc">Descending</option>
        </select>
        
        <input
          type="number"
          placeholder="Min Price"
          value={filters.minPrice}
          onChange={(e) => updateFilters({ minPrice: e.target.value })}
        />
        
        <input
          type="number"
          placeholder="Max Price"
          value={filters.maxPrice}
          onChange={(e) => updateFilters({ maxPrice: e.target.value })}
        />
        
        <label>
          <input
            type="checkbox"
            checked={filters.inStock}
            onChange={(e) => updateFilters({ inStock: e.target.checked })}
          />
          In Stock Only
        </label>
      </div>
      
      {/* Navigation helpers */}
      <div className="product-navigation">
        <button onClick={() => navigate(buildProductUrl(productId, { category: 'electronics' }))}>
          View in Electronics
        </button>
        
        <button onClick={() => navigate(buildProductUrl(productId, { variant: 'blue' }))}>
          Blue Variant
        </button>
        
        <button onClick={() => updateFilters({ sortBy: 'price', order: 'desc' })}>
          Sort by Price (High to Low)
        </button>
      </div>
    </div>
  );
}

// Route pattern matching utility
function useRouteMatch(pattern) {
  const location = useLocation();
  
  return useMemo(() => {
    return matchPath(pattern, location.pathname);
  }, [pattern, location.pathname]);
}

// Breadcrumb component using route matching
function SmartBreadcrumb() {
  const location = useLocation();
  const params = useParams();
  
  // Define route patterns and their labels
  const routePatterns = [
    { pattern: '/', label: 'Home' },
    { pattern: '/products', label: 'Products' },
    { pattern: '/products/:productId', label: (params) => `Product ${params.productId}` },
    { pattern: '/products/:productId/reviews', label: 'Reviews' },
    { pattern: '/users', label: 'Users' },
    { pattern: '/users/:userId', label: (params) => `User ${params.userId}` },
    { pattern: '/dashboard', label: 'Dashboard' },
    { pattern: '/dashboard/analytics', label: 'Analytics' }
  ];
  
  // Build breadcrumb items
  const breadcrumbItems = useMemo(() => {
    const items = [];
    const pathSegments = location.pathname.split('/').filter(Boolean);
    
    for (let i = 0; i <= pathSegments.length; i++) {
      const currentPath = '/' + pathSegments.slice(0, i).join('/');
      if (currentPath === '/') {
        items.push({ path: '/', label: 'Home' });
        continue;
      }
      
      // Find matching pattern
      const matchingPattern = routePatterns.find(pattern => 
        matchPath(pattern.pattern, currentPath)
      );
      
      if (matchingPattern) {
        const label = typeof matchingPattern.label === 'function' 
          ? matchingPattern.label(params)
          : matchingPattern.label;
          
        items.push({ path: currentPath, label });
      }
    }
    
    return items;
  }, [location.pathname, params]);
  
  return (
    <nav className="breadcrumb">
      {breadcrumbItems.map((item, index) => (
        <span key={item.path}>
          {index > 0 && <span className="separator"> / </span>}
          {index === breadcrumbItems.length - 1 ? (
            <span className="current">{item.label}</span>
          ) : (
            <Link to={item.path}>{item.label}</Link>
          )}
        </span>
      ))}
    </nav>
  );
}

// URL state synchronization hook
function useUrlState(key, defaultValue) {
  const [searchParams, setSearchParams] = useSearchParams();
  
  const value = searchParams.get(key) || defaultValue;
  
  const setValue = useCallback((newValue) => {
    const newParams = new URLSearchParams(searchParams);
    
    if (newValue) {
      newParams.set(key, newValue);
    } else {
      newParams.delete(key);
    }
    
    setSearchParams(newParams);
  }, [key, searchParams, setSearchParams]);
  
  return [value, setValue];
}

// Example usage of URL state
function SearchPage() {
  const [query, setQuery] = useUrlState('q', '');
  const [sortBy, setSortBy] = useUrlState('sort', 'relevance');
  const [page, setPage] = useUrlState('page', '1');
  
  return (
    <div className="search-page">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search..."
      />
      
      <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
        <option value="relevance">Relevance</option>
        <option value="date">Date</option>
        <option value="popularity">Popularity</option>
      </select>
      
      <div className="pagination">
        <button onClick={() => setPage(String(parseInt(page) - 1))}>
          Previous
        </button>
        <span>Page {page}</span>
        <button onClick={() => setPage(String(parseInt(page) + 1))}>
          Next
        </button>
      </div>
    </div>
  );
}

export { 
  AdvancedNavigation, 
  DynamicProductPage, 
  SmartBreadcrumb, 
  SearchPage,
  useRouteMatch,
  useUrlState 
};
```

### 🎯 Protected Routes & Route Guards

**Interview Critical Point:** Implementing authentication and authorization patterns with React Router.

```jsx
import { Navigate, useLocation, Outlet } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { usePermissions } from '../hooks/usePermissions';

// Basic protected route component
function ProtectedRoute({ children, fallback = '/login' }) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();
  
  if (isLoading) {
    return <LoadingSpinner />;
  }
  
  if (!isAuthenticated) {
    // Redirect to login with return path
    return (
      <Navigate 
        to={fallback} 
        state={{ from: location }} 
        replace 
      />
    );
  }
  
  return children || <Outlet />;
}

// Role-based route protection
function RoleProtectedRoute({ 
  children, 
  allowedRoles = [], 
  fallback = '/unauthorized' 
}) {
  const { user, isAuthenticated, isLoading } = useAuth();
  const location = useLocation();
  
  if (isLoading) {
    return <LoadingSpinner />;
  }
  
  if (!isAuthenticated) {
    return (
      <Navigate 
        to="/login" 
        state={{ from: location }} 
        replace 
      />
    );
  }
  
  const hasRequiredRole = allowedRoles.length === 0 || 
    allowedRoles.some(role => user?.roles?.includes(role));
  
  if (!hasRequiredRole) {
    return (
      <Navigate 
        to={fallback} 
        state={{ 
          from: location,
          requiredRoles: allowedRoles,
          userRoles: user?.roles 
        }} 
        replace 
      />
    );
  }
  
  return children || <Outlet />;
}

// Permission-based route protection
function PermissionProtectedRoute({ 
  children, 
  requiredPermissions = [],
  requireAll = false 
}) {
  const { hasPermission, hasAllPermissions, isLoading } = usePermissions();
  const { isAuthenticated } = useAuth();
  const location = useLocation();
  
  if (isLoading) {
    return <LoadingSpinner />;
  }
  
  if (!isAuthenticated) {
    return (
      <Navigate 
        to="/login" 
        state={{ from: location }} 
        replace 
      />
    );
  }
  
  const hasRequiredPermissions = requireAll
    ? hasAllPermissions(requiredPermissions)
    : requiredPermissions.some(permission => hasPermission(permission));
  
  if (!hasRequiredPermissions) {
    return (
      <Navigate 
        to="/unauthorized" 
        state={{ 
          from: location,
          requiredPermissions,
          requireAll 
        }} 
        replace 
      />
    );
  }
  
  return children || <Outlet />;
}

// Conditional route protection with custom logic
function ConditionalProtectedRoute({ 
  children, 
  condition,
  fallback = '/unauthorized',
  loadingComponent = <LoadingSpinner />
}) {
  const [isAllowed, setIsAllowed] = useState(null);
  const location = useLocation();
  
  useEffect(() => {
    const checkCondition = async () => {
      try {
        const result = await (typeof condition === 'function' ? condition() : condition);
        setIsAllowed(result);
      } catch (error) {
        console.error('Route condition check failed:', error);
        setIsAllowed(false);
      }
    };
    
    checkCondition();
  }, [condition]);
  
  if (isAllowed === null) {
    return loadingComponent;
  }
  
  if (!isAllowed) {
    return (
      <Navigate 
        to={fallback} 
        state={{ from: location }} 
        replace 
      />
    );
  }
  
  return children || <Outlet />;
}

// Route guard hook for programmatic checks
function useRouteGuard() {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated, user } = useAuth();
  const { hasPermission } = usePermissions();
  
  const requireAuth = useCallback((fallback = '/login') => {
    if (!isAuthenticated) {
      navigate(fallback, { 
        state: { from: location },
        replace: true 
      });
      return false;
    }
    return true;
  }, [isAuthenticated, navigate, location]);
  
  const requireRole = useCallback((roles, fallback = '/unauthorized') => {
    if (!requireAuth()) return false;
    
    const hasRole = Array.isArray(roles) 
      ? roles.some(role => user?.roles?.includes(role))
      : user?.roles?.includes(roles);
    
    if (!hasRole) {
      navigate(fallback, { 
        state: { 
          from: location,
          requiredRoles: Array.isArray(roles) ? roles : [roles]
        },
        replace: true 
      });
      return false;
    }
    return true;
  }, [requireAuth, user, navigate, location]);
  
  const requirePermission = useCallback((permissions, fallback = '/unauthorized') => {
    if (!requireAuth()) return false;
    
    const hasRequiredPermission = Array.isArray(permissions)
      ? permissions.some(perm => hasPermission(perm))
      : hasPermission(permissions);
    
    if (!hasRequiredPermission) {
      navigate(fallback, { 
        state: { 
          from: location,
          requiredPermissions: Array.isArray(permissions) ? permissions : [permissions]
        },
        replace: true 
      });
      return false;
    }
    return true;
  }, [requireAuth, hasPermission, navigate, location]);
  
  return { requireAuth, requireRole, requirePermission };
}

// Advanced route configuration with guards
const protectedRouter = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<RootLayout />}>
      {/* Public routes */}
      <Route index element={<HomePage />} />
      <Route path="about" element={<AboutPage />} />
      <Route path="contact" element={<ContactPage />} />
      
      {/* Auth routes (redirect if already logged in) */}
      <Route path="auth" element={<RedirectIfAuthenticated />}>
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />
        <Route path="forgot-password" element={<ForgotPasswordPage />} />
      </Route>
      
      {/* Protected routes - require authentication */}
      <Route element={<ProtectedRoute />}>
        <Route path="dashboard" element={<DashboardLayout />}>
          <Route index element={<DashboardHome />} />
          
          {/* Admin only routes */}
          <Route element={<RoleProtectedRoute allowedRoles={['admin']} />}>
            <Route path="admin" element={<AdminPanel />} />
            <Route path="users" element={<UserManagement />} />
            <Route path="system" element={<SystemSettings />} />
          </Route>
          
          {/* Manager and Admin routes */}
          <Route element={<RoleProtectedRoute allowedRoles={['admin', 'manager']} />}>
            <Route path="reports" element={<Reports />} />
            <Route path="analytics" element={<Analytics />} />
          </Route>
          
          {/* Permission-based routes */}
          <Route element={
            <PermissionProtectedRoute 
              requiredPermissions={['read_products', 'write_products']} 
              requireAll={true}
            />
          }>
            <Route path="products" element={<ProductManagement />} />
          </Route>
          
          {/* Conditional route example */}
          <Route element={
            <ConditionalProtectedRoute 
              condition={async () => {
                // Check if user has completed onboarding
                const user = await getCurrentUser();
                return user.onboardingCompleted;
              }}
              fallback="/onboarding"
            />
          }>
            <Route path="advanced-features" element={<AdvancedFeatures />} />
          </Route>
        </Route>
        
        {/* User profile routes */}
        <Route path="profile" element={<ProfileLayout />}>
          <Route index element={<ProfileView />} />
          <Route path="edit" element={<ProfileEdit />} />
          <Route path="settings" element={<ProfileSettings />} />
        </Route>
      </Route>
      
      {/* Error routes */}
      <Route path="unauthorized" element={<UnauthorizedPage />} />
      <Route path="*" element={<NotFoundPage />} />
    </Route>
  )
);

// Redirect component for authenticated users
function RedirectIfAuthenticated({ fallback = '/dashboard' }) {
  const { isAuthenticated, isLoading } = useAuth();
  
  if (isLoading) {
    return <LoadingSpinner />;
  }
  
  if (isAuthenticated) {
    return <Navigate to={fallback} replace />;
  }
  
  return <Outlet />;
}

// Example usage in a component
function ProductManagementPage() {
  const { requirePermission } = useRouteGuard();
  
  const handleDeleteProduct = async (productId) => {
    // Check permission before allowing action
    if (!requirePermission('delete_products')) {
      return;
    }
    
    await deleteProduct(productId);
  };
  
  const handleBulkEdit = () => {
    // Check multiple permissions
    if (!requirePermission(['edit_products', 'bulk_operations'])) {
      return;
    }
    
    // Proceed with bulk edit
  };
  
  return (
    <div className="product-management">
      <h1>Product Management</h1>
      <button onClick={handleBulkEdit}>Bulk Edit</button>
      {/* Product list with conditional delete buttons */}
    </div>
  );
}

export { 
  ProtectedRoute,
  RoleProtectedRoute,
  PermissionProtectedRoute,
  ConditionalProtectedRoute,
  useRouteGuard,
  protectedRouter
};
```

---

## Forms & Validation Ecosystem

> **Interview Expectation:** Deep knowledge of form libraries, validation strategies, and performance optimization patterns.

### 🎯 React Hook Form: Performance-First Forms

**Interview Critical Point:** React Hook Form minimizes re-renders and provides excellent performance with uncontrolled components.

```jsx
import { useForm, useFieldArray, Controller, useWatch } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';

// Validation schema with Yup
const userProfileSchema = yup.object({
  personalInfo: yup.object({
    firstName: yup.string().required('First name is required').min(2, 'Too short'),
    lastName: yup.string().required('Last name is required').min(2, 'Too short'),
    email: yup.string().email('Invalid email').required('Email is required'),
    phone: yup.string().matches(/^\+?[1-9]\d{1,14}$/, 'Invalid phone number'),
    dateOfBirth: yup.date().max(new Date(), 'Future date not allowed')
  }),
  address: yup.object({
    street: yup.string().required('Street is required'),
    city: yup.string().required('City is required'),
    zipCode: yup.string().matches(/^\d{5}(-\d{4})?$/, 'Invalid ZIP code'),
    country: yup.string().required('Country is required')
  }),
  preferences: yup.object({
    newsletter: yup.boolean(),
    notifications: yup.object({
      email: yup.boolean(),
      sms: yup.boolean(),
      push: yup.boolean()
    }),
    theme: yup.string().oneOf(['light', 'dark', 'auto'])
  }),
  skills: yup.array().of(
    yup.object({
      name: yup.string().required('Skill name is required'),
      level: yup.string().oneOf(['beginner', 'intermediate', 'advanced', 'expert']),
      yearsOfExperience: yup.number().min(0).max(50)
    })
  ).min(1, 'At least one skill is required')
});

// Advanced React Hook Form component
function AdvancedUserForm({ initialData, onSubmit }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isDirty, isValid, touchedFields },
    control,
    reset,
    setValue,
    getValues,
    trigger,
    watch,
    clearErrors
  } = useForm({
    resolver: yupResolver(userProfileSchema),
    defaultValues: {
      personalInfo: {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        dateOfBirth: null
      },
      address: {
        street: '',
        city: '',
        zipCode: '',
        country: ''
      },
      preferences: {
        newsletter: false,
        notifications: {
          email: true,
          sms: false,
          push: true
        },
        theme: 'light'
      },
      skills: [{ name: '', level: 'beginner', yearsOfExperience: 0 }]
    },
    mode: 'onBlur', // Validate on blur for better UX
    reValidateMode: 'onChange'
  });

  // Dynamic field array for skills
  const { fields, append, remove, move } = useFieldArray({
    control,
    name: 'skills'
  });

  // Watch specific fields for conditional logic
  const watchedCountry = useWatch({ control, name: 'address.country' });
  const watchedSkills = useWatch({ control, name: 'skills' });

  // Load initial data
  useEffect(() => {
    if (initialData) {
      reset(initialData);
    }
  }, [initialData, reset]);

  // Auto-save functionality
  const formValues = watch();
  useEffect(() => {
    const saveTimeout = setTimeout(() => {
      if (isDirty) {
        localStorage.setItem('formDraft', JSON.stringify(formValues));
      }
    }, 1000);

    return () => clearTimeout(saveTimeout);
  }, [formValues, isDirty]);

  // Load draft on mount
  useEffect(() => {
    const savedDraft = localStorage.getItem('formDraft');
    if (savedDraft && !initialData) {
      const draftData = JSON.parse(savedDraft);
      reset(draftData);
    }
  }, [reset, initialData]);

  // Custom validation for specific fields
  const validateSkillUniqueness = (skills) => {
    const skillNames = skills.map(skill => skill.name.toLowerCase());
    const uniqueNames = new Set(skillNames);
    return uniqueNames.size === skillNames.length;
  };

  // Form submission handler
  const onFormSubmit = async (data) => {
    try {
      // Additional validation
      if (!validateSkillUniqueness(data.skills)) {
        throw new Error('Skill names must be unique');
      }

      await onSubmit(data);
      
      // Clear draft after successful submission
      localStorage.removeItem('formDraft');
      
      // Reset form if needed
      // reset();
    } catch (error) {
      console.error('Form submission error:', error);
    }
  };

  // Field-level validation triggers
  const handleCountryChange = async (event) => {
    const country = event.target.value;
    setValue('address.country', country);
    
    // Trigger validation for ZIP code when country changes
    await trigger('address.zipCode');
    
    // Clear city if country changed (conditional logic)
    if (country !== getValues('address.country')) {
      setValue('address.city', '');
    }
  };

  // Add skill with validation
  const addSkill = () => {
    append({ name: '', level: 'beginner', yearsOfExperience: 0 });
  };

  // Remove skill with confirmation
  const removeSkill = (index) => {
    if (fields.length > 1) {
      remove(index);
    }
  };

  return (
    <form onSubmit={handleSubmit(onFormSubmit)} className="advanced-form">
      {/* Form progress indicator */}
      <FormProgress 
        totalSteps={4}
        currentStep={getCurrentStep(touchedFields)}
        isValid={isValid}
      />

      {/* Personal Information Section */}
      <fieldset className="form-section">
        <legend>Personal Information</legend>
        
        <div className="form-row">
          <div className="form-field">
            <label htmlFor="firstName">First Name *</label>
            <input
              id="firstName"
              {...register('personalInfo.firstName')}
              className={errors.personalInfo?.firstName ? 'error' : ''}
            />
            {errors.personalInfo?.firstName && (
              <span className="error-message">
                {errors.personalInfo.firstName.message}
              </span>
            )}
          </div>
          
          <div className="form-field">
            <label htmlFor="lastName">Last Name *</label>
            <input
              id="lastName"
              {...register('personalInfo.lastName')}
              className={errors.personalInfo?.lastName ? 'error' : ''}
            />
            {errors.personalInfo?.lastName && (
              <span className="error-message">
                {errors.personalInfo.lastName.message}
              </span>
            )}
          </div>
        </div>
        
        <div className="form-field">
          <label htmlFor="email">Email *</label>
          <input
            id="email"
            type="email"
            {...register('personalInfo.email')}
            className={errors.personalInfo?.email ? 'error' : ''}
          />
          {errors.personalInfo?.email && (
            <span className="error-message">
              {errors.personalInfo.email.message}
            </span>
          )}
        </div>
        
        <div className="form-field">
          <label htmlFor="phone">Phone</label>
          <input
            id="phone"
            type="tel"
            {...register('personalInfo.phone')}
            className={errors.personalInfo?.phone ? 'error' : ''}
          />
          {errors.personalInfo?.phone && (
            <span className="error-message">
              {errors.personalInfo.phone.message}
            </span>
          )}
        </div>
        
        <div className="form-field">
          <label htmlFor="dateOfBirth">Date of Birth</label>
          <Controller
            name="personalInfo.dateOfBirth"
            control={control}
            render={({ field }) => (
              <DatePicker
                {...field}
                selected={field.value}
                onChange={field.onChange}
                maxDate={new Date()}
                showYearDropdown
                scrollableYearDropdown
                yearDropdownItemNumber={100}
                placeholderText="Select date of birth"
                className={errors.personalInfo?.dateOfBirth ? 'error' : ''}
              />
            )}
          />
          {errors.personalInfo?.dateOfBirth && (
            <span className="error-message">
              {errors.personalInfo.dateOfBirth.message}
            </span>
          )}
        </div>
      </fieldset>

      {/* Address Section */}
      <fieldset className="form-section">
        <legend>Address</legend>
        
        <div className="form-field">
          <label htmlFor="street">Street Address *</label>
          <input
            id="street"
            {...register('address.street')}
            className={errors.address?.street ? 'error' : ''}
          />
          {errors.address?.street && (
            <span className="error-message">
              {errors.address.street.message}
            </span>
          )}
        </div>
        
        <div className="form-row">
          <div className="form-field">
            <label htmlFor="city">City *</label>
            <input
              id="city"
              {...register('address.city')}
              className={errors.address?.city ? 'error' : ''}
            />
            {errors.address?.city && (
              <span className="error-message">
                {errors.address.city.message}
              </span>
            )}
          </div>
          
          <div className="form-field">
            <label htmlFor="zipCode">ZIP Code</label>
            <input
              id="zipCode"
              {...register('address.zipCode')}
              className={errors.address?.zipCode ? 'error' : ''}
            />
            {errors.address?.zipCode && (
              <span className="error-message">
                {errors.address.zipCode.message}
              </span>
            )}
          </div>
        </div>
        
        <div className="form-field">
          <label htmlFor="country">Country *</label>
          <Controller
            name="address.country"
            control={control}
            render={({ field }) => (
              <CountrySelect
                {...field}
                onChange={(value) => {
                  field.onChange(value);
                  handleCountryChange({ target: { value } });
                }}
                className={errors.address?.country ? 'error' : ''}
              />
            )}
          />
          {errors.address?.country && (
            <span className="error-message">
              {errors.address.country.message}
            </span>
          )}
        </div>
      </fieldset>

      {/* Preferences Section */}
      <fieldset className="form-section">
        <legend>Preferences</legend>
        
        <div className="form-field">
          <label>
            <input
              type="checkbox"
              {...register('preferences.newsletter')}
            />
            Subscribe to newsletter
          </label>
        </div>
        
        <div className="form-field">
          <label>Notification Preferences</label>
          <div className="checkbox-group">
            <label>
              <input
                type="checkbox"
                {...register('preferences.notifications.email')}
              />
              Email notifications
            </label>
            <label>
              <input
                type="checkbox"
                {...register('preferences.notifications.sms')}
              />
              SMS notifications
            </label>
            <label>
              <input
                type="checkbox"
                {...register('preferences.notifications.push')}
              />
              Push notifications
            </label>
          </div>
        </div>
        
        <div className="form-field">
          <label htmlFor="theme">Theme</label>
          <select id="theme" {...register('preferences.theme')}>
            <option value="light">Light</option>
            <option value="dark">Dark</option>
            <option value="auto">Auto</option>
          </select>
        </div>
      </fieldset>

      {/* Skills Section (Dynamic Array) */}
      <fieldset className="form-section">
        <legend>Skills</legend>
        
        {fields.map((field, index) => (
          <div key={field.id} className="skill-item">
            <div className="form-row">
              <div className="form-field">
                <label htmlFor={`skill-name-${index}`}>Skill Name *</label>
                <input
                  id={`skill-name-${index}`}
                  {...register(`skills.${index}.name`)}
                  className={errors.skills?.[index]?.name ? 'error' : ''}
                />
                {errors.skills?.[index]?.name && (
                  <span className="error-message">
                    {errors.skills[index].name.message}
                  </span>
                )}
              </div>
              
              <div className="form-field">
                <label htmlFor={`skill-level-${index}`}>Level</label>
                <select
                  id={`skill-level-${index}`}
                  {...register(`skills.${index}.level`)}
                >
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                  <option value="expert">Expert</option>
                </select>
              </div>
              
              <div className="form-field">
                <label htmlFor={`skill-experience-${index}`}>Years of Experience</label>
                <input
                  id={`skill-experience-${index}`}
                  type="number"
                  min="0"
                  max="50"
                  {...register(`skills.${index}.yearsOfExperience`, {
                    valueAsNumber: true
                  })}
                  className={errors.skills?.[index]?.yearsOfExperience ? 'error' : ''}
                />
                {errors.skills?.[index]?.yearsOfExperience && (
                  <span className="error-message">
                    {errors.skills[index].yearsOfExperience.message}
                  </span>
                )}
              </div>
              
              <div className="form-actions">
                <button
                  type="button"
                  onClick={() => removeSkill(index)}
                  disabled={fields.length === 1}
                  className="btn-danger"
                >
                  Remove
                </button>
                
                {index > 0 && (
                  <button
                    type="button"
                    onClick={() => move(index, index - 1)}
                    className="btn-secondary"
                  >
                    Move Up
                  </button>
                )}
                
                {index < fields.length - 1 && (
                  <button
                    type="button"
                    onClick={() => move(index, index + 1)}
                    className="btn-secondary"
                  >
                    Move Down
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
        
        <button
          type="button"
          onClick={addSkill}
          className="btn-secondary"
        >
          Add Skill
        </button>
        
        {errors.skills && (
          <span className="error-message">
            {errors.skills.message}
          </span>
        )}
      </fieldset>

      {/* Form Actions */}
      <div className="form-actions">
        <button
          type="button"
          onClick={() => reset()}
          className="btn-secondary"
        >
          Reset Form
        </button>
        
        <button
          type="button"
          onClick={() => {
            const draft = localStorage.getItem('formDraft');
            if (draft) {
              reset(JSON.parse(draft));
            }
          }}
          className="btn-secondary"
        >
          Load Draft
        </button>
        
        <button
          type="submit"
          disabled={isSubmitting || !isValid}
          className="btn-primary"
        >
          {isSubmitting ? 'Submitting...' : 'Submit'}
        </button>
      </div>

      {/* Form Debug Info (development only) */}
      {process.env.NODE_ENV === 'development' && (
        <FormDebugInfo
          formState={{ errors, isDirty, isValid, touchedFields }}
          watchedValues={formValues}
        />
      )}
    </form>
  );
}

// Form progress component
function FormProgress({ totalSteps, currentStep, isValid }) {
  const progress = (currentStep / totalSteps) * 100;
  
  return (
    <div className="form-progress">
      <div className="progress-bar">
        <div 
          className="progress-fill"
          style={{ width: `${progress}%` }}
        />
      </div>
      <span className="progress-text">
        Step {currentStep} of {totalSteps} {isValid && '✓'}
      </span>
    </div>
  );
}

// Helper function to determine current step
function getCurrentStep(touchedFields) {
  if (touchedFields.skills) return 4;
  if (touchedFields.preferences) return 3;
  if (touchedFields.address) return 2;
  if (touchedFields.personalInfo) return 1;
  return 0;
}

// Form debug component
function FormDebugInfo({ formState, watchedValues }) {
  const [isExpanded, setIsExpanded] = useState(false);
  
  return (
    <details className="form-debug">
      <summary onClick={() => setIsExpanded(!isExpanded)}>
        Form Debug Info {isExpanded ? '▼' : '▶'}
      </summary>
      {isExpanded && (
        <div className="debug-content">
          <h4>Form State</h4>
          <pre>{JSON.stringify(formState, null, 2)}</pre>
          
          <h4>Watched Values</h4>
          <pre>{JSON.stringify(watchedValues, null, 2)}</pre>
        </div>
      )}
    </details>
  );
}

export { AdvancedUserForm, FormProgress };
```

## 📡 Data Fetching Strategies

### 🎯 Native Fetch with AbortController

**Interview Critical Point:** Understanding how to handle async operations, cancellation, and error boundaries in React.

```jsx
import { useState, useEffect, useRef, useCallback, useMemo } from 'react';

// Advanced fetch hook with cancellation and retry
function useFetch(url, options = {}) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [retryCount, setRetryCount] = useState(0);
  
  const abortControllerRef = useRef();
  const retryTimeoutRef = useRef();
  
  const {
    enabled = true,
    retries = 3,
    retryDelay = 1000,
    onSuccess,
    onError,
    transform,
    ...fetchOptions
  } = options;
  
  const fetchData = useCallback(async (retryAttempt = 0) => {
    if (!enabled) return;
    
    // Cancel previous request
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    
    // Create new abort controller
    abortControllerRef.current = new AbortController();
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(url, {
        ...fetchOptions,
        signal: abortControllerRef.current.signal
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      let result = await response.json();
      
      // Transform data if transformer provided
      if (transform) {
        result = transform(result);
      }
      
      setData(result);
      setRetryCount(0);
      
      if (onSuccess) {
        onSuccess(result);
      }
      
    } catch (err) {
      // Don't set error if request was aborted
      if (err.name === 'AbortError') {
        return;
      }
      
      const shouldRetry = retryAttempt < retries;
      
      if (shouldRetry) {
        const delay = retryDelay * Math.pow(2, retryAttempt); // Exponential backoff
        setRetryCount(retryAttempt + 1);
        
        retryTimeoutRef.current = setTimeout(() => {
          fetchData(retryAttempt + 1);
        }, delay);
      } else {
        setError(err);
        if (onError) {
          onError(err);
        }
      }
    } finally {
      setLoading(false);
    }
  }, [url, enabled, retries, retryDelay, onSuccess, onError, transform, fetchOptions]);
  
  useEffect(() => {
    fetchData();
    
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
      if (retryTimeoutRef.current) {
        clearTimeout(retryTimeoutRef.current);
      }
    };
  }, [fetchData]);
  
  const refetch = useCallback(() => {
    fetchData();
  }, [fetchData]);
  
  const abort = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    if (retryTimeoutRef.current) {
      clearTimeout(retryTimeoutRef.current);
    }
    setLoading(false);
  }, []);
  
  return {
    data,
    loading,
    error,
    refetch,
    abort,
    retryCount
  };
}

// Enhanced fetch manager for multiple requests
class FetchManager {
  constructor() {
    this.requests = new Map();
    this.cache = new Map();
    this.interceptors = {
      request: [],
      response: [],
      error: []
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
  
  // Add error interceptor
  addErrorInterceptor(interceptor) {
    this.interceptors.error.push(interceptor);
  }
  
  // Create request with interceptors
  async fetch(url, options = {}) {
    const requestId = `${options.method || 'GET'}_${url}`;
    
    // Cancel existing request with same ID
    if (this.requests.has(requestId)) {
      this.requests.get(requestId).abort();
    }
    
    const controller = new AbortController();
    this.requests.set(requestId, controller);
    
    try {
      // Apply request interceptors
      let processedOptions = { ...options, signal: controller.signal };
      for (const interceptor of this.interceptors.request) {
        processedOptions = await interceptor(url, processedOptions);
      }
      
      // Check cache first
      const cacheKey = `${url}_${JSON.stringify(processedOptions)}`;
      if (this.cache.has(cacheKey) && !processedOptions.skipCache) {
        const cached = this.cache.get(cacheKey);
        if (Date.now() - cached.timestamp < (processedOptions.cacheTime || 300000)) {
          return cached.data;
        }
      }
      
      const response = await fetch(url, processedOptions);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      let data = await response.json();
      
      // Apply response interceptors
      for (const interceptor of this.interceptors.response) {
        data = await interceptor(data, response);
      }
      
      // Cache response
      if (!processedOptions.skipCache) {
        this.cache.set(cacheKey, {
          data,
          timestamp: Date.now()
        });
      }
      
      this.requests.delete(requestId);
      return data;
      
    } catch (error) {
      this.requests.delete(requestId);
      
      // Apply error interceptors
      for (const interceptor of this.interceptors.error) {
        await interceptor(error, url, options);
      }
      
      throw error;
    }
  }
  
  // Cancel all requests
  cancelAll() {
    for (const controller of this.requests.values()) {
      controller.abort();
    }
    this.requests.clear();
  }
  
  // Clear cache
  clearCache() {
    this.cache.clear();
  }
  
  // Get cache stats
  getCacheStats() {
    return {
      size: this.cache.size,
      entries: Array.from(this.cache.keys())
    };
  }
}

// Singleton fetch manager instance
const fetchManager = new FetchManager();

// Add common interceptors
fetchManager.addRequestInterceptor(async (url, options) => {
  // Add auth token
  const token = localStorage.getItem('authToken');
  if (token) {
    options.headers = {
      ...options.headers,
      'Authorization': `Bearer ${token}`
    };
  }
  
  // Add request timestamp
  options.headers = {
    ...options.headers,
    'X-Request-Timestamp': Date.now().toString()
  };
  
  return options;
});

fetchManager.addResponseInterceptor(async (data, response) => {
  // Log response time
  const requestTime = response.headers.get('X-Request-Timestamp');
  if (requestTime) {
    const responseTime = Date.now() - parseInt(requestTime);
    console.log(`Request to ${response.url} took ${responseTime}ms`);
  }
  
  return data;
});

fetchManager.addErrorInterceptor(async (error, url, options) => {
  // Handle auth errors
  if (error.message.includes('401')) {
    // Redirect to login
    window.location.href = '/login';
  }
  
  // Log errors
  console.error(`Request to ${url} failed:`, error);
});

// Data fetching component with comprehensive error handling
function DataFetchingExample() {
  const [selectedEndpoint, setSelectedEndpoint] = useState('/api/users');
  const [fetchOptions, setFetchOptions] = useState({
    enabled: true,
    retries: 3,
    retryDelay: 1000
  });
  
  // Using the custom fetch hook
  const { data, loading, error, refetch, abort, retryCount } = useFetch(
    selectedEndpoint,
    {
      ...fetchOptions,
      transform: (data) => {
        // Transform data for consistency
        return {
          items: data.items || data.data || data,
          total: data.total || data.items?.length || 0,
          timestamp: Date.now()
        };
      },
      onSuccess: (data) => {
        console.log('Fetch successful:', data);
      },
      onError: (error) => {
        console.error('Fetch failed:', error);
      }
    }
  );
  
  // Parallel data fetching
  const endpoints = ['/api/users', '/api/posts', '/api/comments'];
  const [parallelData, setParallelData] = useState({});
  const [parallelLoading, setParallelLoading] = useState(false);
  const [parallelErrors, setParallelErrors] = useState({});
  
  const fetchParallelData = useCallback(async () => {
    setParallelLoading(true);
    setParallelErrors({});
    
    const promises = endpoints.map(async (endpoint) => {
      try {
        const data = await fetchManager.fetch(endpoint);
        return { endpoint, data, error: null };
      } catch (error) {
        return { endpoint, data: null, error };
      }
    });
    
    const results = await Promise.allSettled(promises);
    
    const newData = {};
    const newErrors = {};
    
    results.forEach((result, index) => {
      const endpoint = endpoints[index];
      if (result.status === 'fulfilled') {
        const { data, error } = result.value;
        if (error) {
          newErrors[endpoint] = error;
        } else {
          newData[endpoint] = data;
        }
      } else {
        newErrors[endpoint] = result.reason;
      }
    });
    
    setParallelData(newData);
    setParallelErrors(newErrors);
    setParallelLoading(false);
  }, []);
  
  return (
    <div className="data-fetching-example">
      <h3>Data Fetching Examples</h3>
      
      {/* Single Endpoint Fetching */}
      <section className="single-fetch">
        <h4>Single Endpoint Fetching</h4>
        
        <div className="controls">
          <select 
            value={selectedEndpoint}
            onChange={(e) => setSelectedEndpoint(e.target.value)}
          >
            <option value="/api/users">Users</option>
            <option value="/api/posts">Posts</option>
            <option value="/api/comments">Comments</option>
          </select>
          
          <label>
            <input
              type="checkbox"
              checked={fetchOptions.enabled}
              onChange={(e) => setFetchOptions(prev => ({
                ...prev,
                enabled: e.target.checked
              }))}
            />
            Enabled
          </label>
          
          <label>
            Retries:
            <input
              type="number"
              min="0"
              max="10"
              value={fetchOptions.retries}
              onChange={(e) => setFetchOptions(prev => ({
                ...prev,
                retries: parseInt(e.target.value)
              }))}
            />
          </label>
          
          <button onClick={refetch} disabled={loading}>
            {loading ? 'Loading...' : 'Refetch'}
          </button>
          
          <button onClick={abort}>
            Cancel
          </button>
        </div>
        
        <div className="fetch-status">
          {loading && (
            <div className="loading">
              Loading... 
              {retryCount > 0 && <span>(Retry {retryCount})</span>}
            </div>
          )}
          
          {error && (
            <div className="error">
              Error: {error.message}
              <button onClick={refetch}>Retry</button>
            </div>
          )}
          
          {data && (
            <div className="success">
              <h5>Data loaded successfully</h5>
              <p>Items: {data.total}</p>
              <p>Timestamp: {new Date(data.timestamp).toLocaleTimeString()}</p>
              <details>
                <summary>View Data</summary>
                <pre>{JSON.stringify(data.items.slice(0, 3), null, 2)}</pre>
              </details>
            </div>
          )}
        </div>
      </section>
      
      {/* Parallel Fetching */}
      <section className="parallel-fetch">
        <h4>Parallel Fetching</h4>
        
        <div className="controls">
          <button 
            onClick={fetchParallelData}
            disabled={parallelLoading}
          >
            {parallelLoading ? 'Fetching...' : 'Fetch All Endpoints'}
          </button>
          
          <button onClick={() => fetchManager.cancelAll()}>
            Cancel All
          </button>
          
          <button onClick={() => fetchManager.clearCache()}>
            Clear Cache
          </button>
        </div>
        
        <div className="parallel-results">
          {parallelLoading && <div>Fetching all endpoints...</div>}
          
          {Object.entries(parallelData).map(([endpoint, data]) => (
            <div key={endpoint} className="endpoint-result success">
              <h5>{endpoint}</h5>
              <p>✅ Loaded {data?.length || 0} items</p>
            </div>
          ))}
          
          {Object.entries(parallelErrors).map(([endpoint, error]) => (
            <div key={endpoint} className="endpoint-result error">
              <h5>{endpoint}</h5>
              <p>❌ {error.message}</p>
            </div>
          ))}
        </div>
      </section>
      
      {/* Cache Stats */}
      <section className="cache-stats">
        <h4>Cache Statistics</h4>
        <CacheStatsDisplay />
      </section>
    </div>
  );
}

// Cache statistics component
function CacheStatsDisplay() {
  const [stats, setStats] = useState(null);
  
  useEffect(() => {
    const updateStats = () => {
      setStats(fetchManager.getCacheStats());
    };
    
    updateStats();
    const interval = setInterval(updateStats, 1000);
    
    return () => clearInterval(interval);
  }, []);
  
  if (!stats) return null;
  
  return (
    <div className="cache-stats">
      <p>Cached entries: {stats.size}</p>
      {stats.entries.length > 0 && (
        <details>
          <summary>Cache Keys</summary>
          <ul>
            {stats.entries.map((key, index) => (
              <li key={index}>{key}</li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}

export { useFetch, FetchManager, fetchManager, DataFetchingExample };
```

### 🎯 TanStack Query (React Query)

**Interview Critical Point:** Understanding declarative data fetching, caching strategies, and background updates.

```jsx
import { 
  useQuery, 
  useMutation, 
  useQueryClient, 
  useInfiniteQuery,
  QueryClient,
  QueryClientProvider 
} from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

// Query client configuration
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000,   // 10 minutes (formerly cacheTime)
      retry: 3,
      retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000),
      refetchOnWindowFocus: false,
      refetchOnReconnect: true
    },
    mutations: {
      retry: 1,
      onError: (error) => {
        console.error('Mutation error:', error);
      }
    }
  }
});

// API service layer
const api = {
  // Users
  getUsers: async (page = 1, limit = 10) => {
    const response = await fetch(`/api/users?page=${page}&limit=${limit}`);
    if (!response.ok) throw new Error('Failed to fetch users');
    return response.json();
  },
  
  getUser: async (id) => {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) throw new Error('Failed to fetch user');
    return response.json();
  },
  
  createUser: async (userData) => {
    const response = await fetch('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    if (!response.ok) throw new Error('Failed to create user');
    return response.json();
  },
  
  updateUser: async ({ id, ...userData }) => {
    const response = await fetch(`/api/users/${id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(userData)
    });
    if (!response.ok) throw new Error('Failed to update user');
    return response.json();
  },
  
  deleteUser: async (id) => {
    const response = await fetch(`/api/users/${id}`, {
      method: 'DELETE'
    });
    if (!response.ok) throw new Error('Failed to delete user');
    return response.json();
  },
  
  // Posts with pagination
  getPosts: async ({ pageParam = 1, queryKey }) => {
    const [, filters] = queryKey;
    const params = new URLSearchParams({
      page: pageParam,
      limit: 10,
      ...filters
    });
    
    const response = await fetch(`/api/posts?${params}`);
    if (!response.ok) throw new Error('Failed to fetch posts');
    
    const data = await response.json();
    return {
      posts: data.posts,
      nextPage: data.hasMore ? pageParam + 1 : undefined,
      totalPages: data.totalPages
    };
  },
  
  // Search with debouncing
  searchPosts: async (query) => {
    if (!query.trim()) return { results: [] };
    
    const response = await fetch(`/api/posts/search?q=${encodeURIComponent(query)}`);
    if (!response.ok) throw new Error('Search failed');
    return response.json();
  }
};

// Custom hooks for data operations
function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: () => api.getUsers(),
    select: (data) => ({
      users: data.users,
      total: data.total,
      processed: true
    })
  });
}

function useUser(id, options = {}) {
  return useQuery({
    queryKey: ['user', id],
    queryFn: () => api.getUser(id),
    enabled: !!id,
    ...options
  });
}

// Optimistic updates with mutations
function useCreateUser() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: api.createUser,
    onMutate: async (newUser) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['users'] });
      
      // Snapshot previous value
      const previousUsers = queryClient.getQueryData(['users']);
      
      // Optimistically update
      const optimisticUser = {
        id: Date.now(), // Temporary ID
        ...newUser,
        createdAt: new Date().toISOString(),
        pending: true
      };
      
      queryClient.setQueryData(['users'], (old) => ({
        ...old,
        users: [...(old?.users || []), optimisticUser],
        total: (old?.total || 0) + 1
      }));
      
      return { previousUsers, optimisticUser };
    },
    onError: (err, newUser, context) => {
      // Rollback on error
      queryClient.setQueryData(['users'], context.previousUsers);
    },
    onSuccess: (data, variables, context) => {
      // Replace optimistic update with real data
      queryClient.setQueryData(['users'], (old) => ({
        ...old,
        users: old.users.map(user => 
          user.id === context.optimisticUser.id ? data : user
        )
      }));
    },
    onSettled: () => {
      // Always refetch after mutation
      queryClient.invalidateQueries({ queryKey: ['users'] });
    }
  });
}

function useUpdateUser() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: api.updateUser,
    onMutate: async (updatedUser) => {
      const { id } = updatedUser;
      
      // Cancel queries
      await queryClient.cancelQueries({ queryKey: ['user', id] });
      await queryClient.cancelQueries({ queryKey: ['users'] });
      
      // Snapshot
      const previousUser = queryClient.getQueryData(['user', id]);
      const previousUsers = queryClient.getQueryData(['users']);
      
      // Optimistic updates
      queryClient.setQueryData(['user', id], (old) => ({
        ...old,
        ...updatedUser,
        updatedAt: new Date().toISOString()
      }));
      
      queryClient.setQueryData(['users'], (old) => ({
        ...old,
        users: old?.users?.map(user => 
          user.id === id ? { ...user, ...updatedUser } : user
        ) || []
      }));
      
      return { previousUser, previousUsers, id };
    },
    onError: (err, variables, context) => {
      // Rollback
      if (context?.previousUser) {
        queryClient.setQueryData(['user', context.id], context.previousUser);
      }
      if (context?.previousUsers) {
        queryClient.setQueryData(['users'], context.previousUsers);
      }
    },
    onSettled: (data, error, variables) => {
      // Refetch
      queryClient.invalidateQueries({ queryKey: ['user', variables.id] });
      queryClient.invalidateQueries({ queryKey: ['users'] });
    }
  });
}

function useDeleteUser() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: api.deleteUser,
    onSuccess: (data, deletedId) => {
      // Remove from cache
      queryClient.removeQueries({ queryKey: ['user', deletedId] });
      
      // Update users list
      queryClient.setQueryData(['users'], (old) => ({
        ...old,
        users: old?.users?.filter(user => user.id !== deletedId) || [],
        total: Math.max((old?.total || 1) - 1, 0)
      }));
    }
  });
}

// Infinite query for pagination
function usePosts(filters = {}) {
  return useInfiniteQuery({
    queryKey: ['posts', filters],
    queryFn: api.getPosts,
    initialPageParam: 1,
    getNextPageParam: (lastPage) => lastPage.nextPage,
    getPreviousPageParam: (firstPage, allPages) => {
      return allPages.length > 1 ? allPages.length - 1 : undefined;
    },
    select: (data) => ({
      pages: data.pages,
      pageParams: data.pageParams,
      posts: data.pages.flatMap(page => page.posts),
      totalPosts: data.pages.reduce((acc, page) => acc + page.posts.length, 0)
    }),
    staleTime: 2 * 60 * 1000, // 2 minutes
    gcTime: 5 * 60 * 1000     // 5 minutes
  });
}

// Debounced search hook
function useSearchPosts(query) {
  const [debouncedQuery, setDebouncedQuery] = useState(query);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
    }, 300);
    
    return () => clearTimeout(timer);
  }, [query]);
  
  return useQuery({
    queryKey: ['search', 'posts', debouncedQuery],
    queryFn: () => api.searchPosts(debouncedQuery),
    enabled: debouncedQuery.length >= 2,
    staleTime: 30 * 1000, // 30 seconds
    select: (data) => data.results
  });
}

// Dependent queries
function useUserWithPosts(userId) {
  // First query: get user
  const { data: user, isLoading: userLoading, error: userError } = useUser(userId);
  
  // Second query: get user's posts (depends on user data)
  const { 
    data: posts, 
    isLoading: postsLoading, 
    error: postsError 
  } = useQuery({
    queryKey: ['posts', 'user', userId],
    queryFn: () => api.getPosts({ pageParam: 1, queryKey: [null, { userId }] }),
    enabled: !!user?.id, // Only run if user exists
    select: (data) => data.posts
  });
  
  return {
    user,
    posts,
    isLoading: userLoading || postsLoading,
    error: userError || postsError,
    isSuccess: !!user && !!posts
  };
}

// Background data synchronization
function useBackgroundSync() {
  const queryClient = useQueryClient();
  
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        // Refetch stale queries when tab becomes visible
        queryClient.refetchQueries({
          type: 'active',
          stale: true
        });
      }
    };
    
    const handleOnline = () => {
      // Refetch failed queries when coming back online
      queryClient.refetchQueries({
        type: 'active',
        predicate: (query) => query.state.fetchStatus === 'idle' && query.state.status === 'error'
      });
    };
    
    document.addEventListener('visibilitychange', handleVisibilityChange);
    window.addEventListener('online', handleOnline);
    
    return () => {
      document.removeEventListener('visibilitychange', handleVisibilityChange);
      window.removeEventListener('online', handleOnline);
    };
  }, [queryClient]);
}

// React Query powered component
function ReactQueryExample() {
  const [selectedUserId, setSelectedUserId] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [postFilters, setPostFilters] = useState({});
  
  // Background sync
  useBackgroundSync();
  
  // Queries
  const { data: users, isLoading: usersLoading, error: usersError } = useUsers();
  const { data: selectedUser, isLoading: userLoading } = useUser(selectedUserId);
  const { data: searchResults, isLoading: searchLoading } = useSearchPosts(searchQuery);
  
  // Infinite query for posts
  const {
    data: postsData,
    fetchNextPage,
    hasNextPage,
    isFetchingNextPage,
    isLoading: postsLoading
  } = usePosts(postFilters);
  
  // Mutations
  const createUserMutation = useCreateUser();
  const updateUserMutation = useUpdateUser();
  const deleteUserMutation = useDeleteUser();
  
  const handleCreateUser = (userData) => {
    createUserMutation.mutate(userData, {
      onSuccess: () => {
        console.log('User created successfully');
      },
      onError: (error) => {
        console.error('Failed to create user:', error);
      }
    });
  };
  
  const handleUpdateUser = (id, userData) => {
    updateUserMutation.mutate({ id, ...userData });
  };
  
  const handleDeleteUser = (id) => {
    if (window.confirm('Are you sure?')) {
      deleteUserMutation.mutate(id);
    }
  };
  
  return (
    <div className="react-query-example">
      <h3>React Query Examples</h3>
      
      {/* Users Section */}
      <section className="users-section">
        <h4>Users Management</h4>
        
        {usersLoading && <div>Loading users...</div>}
        {usersError && <div>Error: {usersError.message}</div>}
        
        {users && (
          <div className="users-list">
            <p>Total users: {users.total}</p>
            {users.users.map(user => (
              <div key={user.id} className="user-item">
                <span>{user.name} ({user.email})</span>
                <div className="user-actions">
                  <button onClick={() => setSelectedUserId(user.id)}>
                    View Details
                  </button>
                  <button onClick={() => handleUpdateUser(user.id, { 
                    name: `${user.name} (Updated)` 
                  })}>
                    Update
                  </button>
                  <button onClick={() => handleDeleteUser(user.id)}>
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
        
        <button 
          onClick={() => handleCreateUser({
            name: `User ${Date.now()}`,
            email: `user${Date.now()}@example.com`
          })}
          disabled={createUserMutation.isPending}
        >
          {createUserMutation.isPending ? 'Creating...' : 'Create User'}
        </button>
      </section>
      
      {/* Selected User Details */}
      {selectedUserId && (
        <section className="user-details">
          <h4>User Details</h4>
          {userLoading && <div>Loading user details...</div>}
          {selectedUser && (
            <div>
              <h5>{selectedUser.name}</h5>
              <p>Email: {selectedUser.email}</p>
              <p>Created: {new Date(selectedUser.createdAt).toLocaleDateString()}</p>
            </div>
          )}
        </section>
      )}
      
      {/* Search Section */}
      <section className="search-section">
        <h4>Search Posts</h4>
        <input
          type="text"
          placeholder="Search posts..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        
        {searchLoading && <div>Searching...</div>}
        {searchResults && (
          <div className="search-results">
            <h5>Search Results ({searchResults.length})</h5>
            {searchResults.map(post => (
              <div key={post.id} className="search-result">
                <h6>{post.title}</h6>
                <p>{post.excerpt}</p>
              </div>
            ))}
          </div>
        )}
      </section>
      
      {/* Infinite Posts */}
      <section className="posts-section">
        <h4>Posts (Infinite Scroll)</h4>
        
        <div className="posts-filters">
          <select 
            onChange={(e) => setPostFilters({ category: e.target.value })}
          >
            <option value="">All Categories</option>
            <option value="tech">Tech</option>
            <option value="lifestyle">Lifestyle</option>
            <option value="business">Business</option>
          </select>
        </div>
        
        {postsLoading && <div>Loading posts...</div>}
        
        {postsData && (
          <div className="posts-list">
            <p>Loaded {postsData.totalPosts} posts</p>
            {postsData.posts.map(post => (
              <div key={post.id} className="post-item">
                <h6>{post.title}</h6>
                <p>{post.excerpt}</p>
                <small>By {post.author} • {new Date(post.createdAt).toLocaleDateString()}</small>
              </div>
            ))}
            
            {hasNextPage && (
              <button 
                onClick={() => fetchNextPage()}
                disabled={isFetchingNextPage}
              >
                {isFetchingNextPage ? 'Loading more...' : 'Load More'}
              </button>
            )}
          </div>
        )}
      </section>
      
      {/* Query Cache Status */}
      <section className="cache-status">
        <h4>Cache Status</h4>
        <QueryCacheStatus />
      </section>
    </div>
  );
}

// Cache status component
function QueryCacheStatus() {
  const queryClient = useQueryClient();
  const [cacheStats, setCacheStats] = useState({});
  
  useEffect(() => {
    const updateStats = () => {
      const cache = queryClient.getQueryCache();
      const queries = cache.getAll();
      
      const stats = {
        totalQueries: queries.length,
        staleQueries: queries.filter(q => q.isStale()).length,
        fetchingQueries: queries.filter(q => q.state.fetchStatus === 'fetching').length,
        errorQueries: queries.filter(q => q.state.status === 'error').length,
        successQueries: queries.filter(q => q.state.status === 'success').length
      };
      
      setCacheStats(stats);
    };
    
    updateStats();
    const interval = setInterval(updateStats, 1000);
    
    return () => clearInterval(interval);
  }, [queryClient]);
  
  return (
    <div className="cache-stats">
      <div>Total Queries: {cacheStats.totalQueries}</div>
      <div>Stale: {cacheStats.staleQueries}</div>
      <div>Fetching: {cacheStats.fetchingQueries}</div>
      <div>Error: {cacheStats.errorQueries}</div>
      <div>Success: {cacheStats.successQueries}</div>
      
      <button onClick={() => queryClient.clear()}>
        Clear All Cache
      </button>
    </div>
  );
}

// App wrapper with QueryClient
function ReactQueryApp() {
  return (
    <QueryClientProvider client={queryClient}>
      <ReactQueryExample />
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}

export { 
  queryClient,
  ReactQueryApp,
  useUsers,
  useUser,
  useCreateUser,
  useUpdateUser,
  useDeleteUser,
  usePosts,
  useSearchPosts,
  useUserWithPosts
};
```

### 🎯 SWR (Stale-While-Revalidate)

**Interview Critical Point:** Understanding SWR's unique approach to data fetching and when it's preferable to React Query.

```jsx
import useSWR, { 
  useSWRConfig, 
  SWRConfig, 
  unstable_serialize as serialize,
  useSWRInfinite 
} from 'swr';
import { useState, useCallback, useMemo } from 'react';

// Global SWR configuration
const swrConfig = {
  // Default fetcher
  fetcher: async (url) => {
    const response = await fetch(url);
    if (!response.ok) {
      const error = new Error('An error occurred while fetching the data');
      error.info = await response.json();
      error.status = response.status;
      throw error;
    }
    return response.json();
  },
  
  // Error retry configuration
  errorRetryCount: 3,
  errorRetryInterval: 1000,
  onErrorRetry: (error, key, config, revalidate, { retryCount }) => {
    // Never retry on 404
    if (error.status === 404) return;
    
    // Never retry for specific keys
    if (key === '/api/user/me') return;
    
    // Only retry up to 3 times
    if (retryCount >= 3) return;
    
    // Exponential backoff
    setTimeout(() => revalidate({ retryCount }), 1000 * Math.pow(2, retryCount));
  },
  
  // Revalidation
  revalidateOnFocus: true,
  revalidateOnReconnect: true,
  refreshInterval: 0, // Disabled by default
  dedupingInterval: 2000,
  
  // Loading timeout
  loadingTimeout: 3000,
  
  // Global error handler
  onError: (error, key) => {
    console.error(`SWR Error for ${key}:`, error);
    
    // Global error handling
    if (error.status === 401) {
      // Redirect to login
      window.location.href = '/login';
    }
  },
  
  // Global success handler
  onSuccess: (data, key) => {
    console.log(`SWR Success for ${key}`);
  }
};

// Enhanced fetcher with interceptors
class SWRFetcher {
  constructor() {
    this.interceptors = {
      request: [],
      response: [],
      error: []
    };
  }
  
  // Add interceptors
  addRequestInterceptor(interceptor) {
    this.interceptors.request.push(interceptor);
  }
  
  addResponseInterceptor(interceptor) {
    this.interceptors.response.push(interceptor);
  }
  
  addErrorInterceptor(interceptor) {
    this.interceptors.error.push(interceptor);
  }
  
  // Main fetcher function
  async fetch(url, options = {}) {
    try {
      // Apply request interceptors
      let processedOptions = { ...options };
      for (const interceptor of this.interceptors.request) {
        processedOptions = await interceptor(url, processedOptions);
      }
      
      const response = await fetch(url, processedOptions);
      
      if (!response.ok) {
        const error = new Error(`HTTP error! status: ${response.status}`);
        error.status = response.status;
        error.info = await response.json().catch(() => ({}));
        throw error;
      }
      
      let data = await response.json();
      
      // Apply response interceptors
      for (const interceptor of this.interceptors.response) {
        data = await interceptor(data, response);
      }
      
      return data;
    } catch (error) {
      // Apply error interceptors
      for (const interceptor of this.interceptors.error) {
        await interceptor(error, url, options);
      }
      throw error;
    }
  }
}

// Create fetcher instance
const swrFetcher = new SWRFetcher();

// Add auth interceptor
swrFetcher.addRequestInterceptor(async (url, options) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    options.headers = {
      ...options.headers,
      'Authorization': `Bearer ${token}`
    };
  }
  return options;
});

// Add logging interceptor
swrFetcher.addResponseInterceptor(async (data, response) => {
  console.log(`Fetched ${response.url}:`, data);
  return data;
});

// SWR custom hooks
function useUsers(page = 1, limit = 10) {
  const { data, error, mutate, isValidating } = useSWR(
    `/api/users?page=${page}&limit=${limit}`,
    swrFetcher.fetch.bind(swrFetcher),
    {
      revalidateOnFocus: false,
      dedupingInterval: 5000,
      // Transform data
      onSuccess: (data) => ({
        users: data.users || [],
        total: data.total || 0,
        currentPage: page,
        totalPages: Math.ceil((data.total || 0) / limit)
      })
    }
  );
  
  return {
    users: data?.users || [],
    total: data?.total || 0,
    currentPage: data?.currentPage || page,
    totalPages: data?.totalPages || 1,
    isLoading: !error && !data,
    isError: !!error,
    error,
    mutate,
    isValidating
  };
}

function useUser(id, options = {}) {
  const shouldFetch = id && id !== 'undefined' && id !== 'null';
  
  const { data, error, mutate, isValidating } = useSWR(
    shouldFetch ? `/api/users/${id}` : null,
    swrFetcher.fetch.bind(swrFetcher),
    {
      refreshInterval: 30000, // Refresh every 30 seconds
      ...options
    }
  );
  
  return {
    user: data,
    isLoading: !error && !data && shouldFetch,
    isError: !!error,
    error,
    mutate,
    isValidating
  };
}

// Infinite loading with SWR
function usePostsInfinite(filters = {}) {
  const getKey = useCallback((pageIndex, previousPageData) => {
    // Reached the end
    if (previousPageData && !previousPageData.hasMore) return null;
    
    // First page
    if (pageIndex === 0) {
      return serialize(['/api/posts', { page: 1, ...filters }]);
    }
    
    // Next page
    return serialize(['/api/posts', { page: pageIndex + 1, ...filters }]);
  }, [filters]);
  
  const { data, error, mutate, size, setSize, isValidating } = useSWRInfinite(
    getKey,
    async ([url, params]) => {
      const queryString = new URLSearchParams(params).toString();
      return swrFetcher.fetch(`${url}?${queryString}`);
    },
    {
      revalidateFirstPage: false,
      revalidateOnFocus: false
    }
  );
  
  const posts = useMemo(() => {
    return data ? data.flatMap(page => page.posts || []) : [];
  }, [data]);
  
  const hasMore = useMemo(() => {
    return data ? data[data.length - 1]?.hasMore : false;
  }, [data]);
  
  const loadMore = useCallback(() => {
    if (!isValidating && hasMore) {
      setSize(size + 1);
    }
  }, [size, setSize, isValidating, hasMore]);
  
  return {
    posts,
    isLoading: !error && !data,
    isError: !!error,
    error,
    mutate,
    isValidating,
    hasMore,
    loadMore,
    size
  };
}

// Search hook with debouncing
function useSearchPosts(query, options = {}) {
  const [debouncedQuery, setDebouncedQuery] = useState(query);
  
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedQuery(query);
    }, options.debounceMs || 300);
    
    return () => clearTimeout(timer);
  }, [query, options.debounceMs]);
  
  const shouldFetch = debouncedQuery && debouncedQuery.length >= (options.minLength || 2);
  
  const { data, error, mutate, isValidating } = useSWR(
    shouldFetch ? `/api/posts/search?q=${encodeURIComponent(debouncedQuery)}` : null,
    swrFetcher.fetch.bind(swrFetcher),
    {
      dedupingInterval: 1000,
      revalidateOnFocus: false,
      ...options.swrOptions
    }
  );
  
  return {
    results: data?.results || [],
    isLoading: !error && !data && shouldFetch,
    isError: !!error,
    error,
    mutate,
    isValidating,
    query: debouncedQuery
  };
}

// Optimistic updates with SWR
function useOptimisticUsers() {
  const { mutate } = useSWRConfig();
  
  const createUser = useCallback(async (userData) => {
    const optimisticUser = {
      id: Date.now(),
      ...userData,
      createdAt: new Date().toISOString(),
      pending: true
    };
    
    // Optimistically update the users list
    await mutate(
      key => typeof key === 'string' && key.startsWith('/api/users?'),
      (currentData) => ({
        ...currentData,
        users: [...(currentData?.users || []), optimisticUser],
        total: (currentData?.total || 0) + 1
      }),
      { revalidate: false }
    );
    
    try {
      // Make the actual API call
      const newUser = await swrFetcher.fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      
      // Update with real data
      await mutate(
        key => typeof key === 'string' && key.startsWith('/api/users?'),
        (currentData) => ({
          ...currentData,
          users: currentData?.users?.map(user => 
            user.id === optimisticUser.id ? newUser : user
          ) || []
        }),
        { revalidate: false }
      );
      
      return newUser;
    } catch (error) {
      // Rollback on error
      await mutate(
        key => typeof key === 'string' && key.startsWith('/api/users?'),
        (currentData) => ({
          ...currentData,
          users: currentData?.users?.filter(user => user.id !== optimisticUser.id) || [],
          total: Math.max((currentData?.total || 1) - 1, 0)
        }),
        { revalidate: false }
      );
      throw error;
    }
  }, [mutate]);
  
  const updateUser = useCallback(async (id, updates) => {
    // Optimistically update all relevant caches
    await Promise.all([
      // Update user detail
      mutate(
        `/api/users/${id}`,
        (currentData) => ({ ...currentData, ...updates }),
        { revalidate: false }
      ),
      // Update users list
      mutate(
        key => typeof key === 'string' && key.startsWith('/api/users?'),
        (currentData) => ({
          ...currentData,
          users: currentData?.users?.map(user => 
            user.id === id ? { ...user, ...updates } : user
          ) || []
        }),
        { revalidate: false }
      )
    ]);
    
    try {
      const updatedUser = await swrFetcher.fetch(`/api/users/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updates)
      });
      
      // Update with server response
      await Promise.all([
        mutate(`/api/users/${id}`, updatedUser, { revalidate: false }),
        mutate(
          key => typeof key === 'string' && key.startsWith('/api/users?'),
          (currentData) => ({
            ...currentData,
            users: currentData?.users?.map(user => 
              user.id === id ? updatedUser : user
            ) || []
          }),
          { revalidate: false }
        )
      ]);
      
      return updatedUser;
    } catch (error) {
      // Revalidate to get fresh data on error
      await Promise.all([
        mutate(`/api/users/${id}`),
        mutate(key => typeof key === 'string' && key.startsWith('/api/users?'))
      ]);
      throw error;
    }
  }, [mutate]);
  
  const deleteUser = useCallback(async (id) => {
    // Optimistically remove user
    await Promise.all([
      mutate(`/api/users/${id}`, undefined, { revalidate: false }),
      mutate(
        key => typeof key === 'string' && key.startsWith('/api/users?'),
        (currentData) => ({
          ...currentData,
          users: currentData?.users?.filter(user => user.id !== id) || [],
          total: Math.max((currentData?.total || 1) - 1, 0)
        }),
        { revalidate: false }
      )
    ]);
    
    try {
      await swrFetcher.fetch(`/api/users/${id}`, {
        method: 'DELETE'
      });
      
      // Success - the optimistic update was correct
      return true;
    } catch (error) {
      // Revalidate to restore data on error
      await Promise.all([
        mutate(`/api/users/${id}`),
        mutate(key => typeof key === 'string' && key.startsWith('/api/users?'))
      ]);
      throw error;
    }
  }, [mutate]);
  
  return { createUser, updateUser, deleteUser };
}

// Real-time updates with SWR
function useRealTimeData(endpoint, options = {}) {
  const { data, mutate } = useSWR(endpoint, swrFetcher.fetch.bind(swrFetcher), {
    refreshInterval: options.refreshInterval || 5000,
    ...options
  });
  
  useEffect(() => {
    if (!options.enableWebSocket) return;
    
    const ws = new WebSocket(options.websocketUrl || 'ws://localhost:8080');
    
    ws.onmessage = (event) => {
      const update = JSON.parse(event.data);
      
      // Update SWR cache based on WebSocket message
      if (update.type === 'UPDATE' && update.key === endpoint) {
        mutate(update.data, { revalidate: false });
      } else if (update.type === 'INVALIDATE' && update.key === endpoint) {
        mutate();
      }
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
    };
    
    return () => {
      ws.close();
    };
  }, [endpoint, options.enableWebSocket, options.websocketUrl, mutate]);
  
  return { data, mutate };
}

// SWR powered component
function SWRExample() {
  const [page, setPage] = useState(1);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedUserId, setSelectedUserId] = useState(null);
  
  // Data hooks
  const { users, total, currentPage, totalPages, isLoading, isError, error, mutate } = useUsers(page);
  const { user: selectedUser, isLoading: userLoading } = useUser(selectedUserId);
  const { results: searchResults, isLoading: searchLoading } = useSearchPosts(searchQuery);
  const { posts, loadMore, hasMore, isValidating } = usePostsInfinite();
  
  // Mutations
  const { createUser, updateUser, deleteUser } = useOptimisticUsers();
  
  // Real-time data
  const { data: realtimeStats } = useRealTimeData('/api/stats', {
    refreshInterval: 10000,
    enableWebSocket: true,
    websocketUrl: 'ws://localhost:8080'
  });
  
  const handleCreateUser = async () => {
    try {
      await createUser({
        name: `User ${Date.now()}`,
        email: `user${Date.now()}@example.com`
      });
      console.log('User created successfully');
    } catch (error) {
      console.error('Failed to create user:', error);
    }
  };
  
  const handleUpdateUser = async (id, updates) => {
    try {
      await updateUser(id, updates);
      console.log('User updated successfully');
    } catch (error) {
      console.error('Failed to update user:', error);
    }
  };
  
  const handleDeleteUser = async (id) => {
    if (!window.confirm('Are you sure?')) return;
    
    try {
      await deleteUser(id);
      console.log('User deleted successfully');
    } catch (error) {
      console.error('Failed to delete user:', error);
    }
  };
  
  return (
    <div className="swr-example">
      <h3>SWR Examples</h3>
      
      {/* Real-time Stats */}
      {realtimeStats && (
        <div className="realtime-stats">
          <h4>Live Stats</h4>
          <div>Online Users: {realtimeStats.onlineUsers}</div>
          <div>Total Posts: {realtimeStats.totalPosts}</div>
          <div>Last Updated: {new Date(realtimeStats.lastUpdated).toLocaleTimeString()}</div>
        </div>
      )}
      
      {/* Users Section */}
      <section className="users-section">
        <h4>Users (Page {currentPage} of {totalPages})</h4>
        
        {isLoading && <div>Loading users...</div>}
        {isError && <div>Error: {error?.message}</div>}
        
        {users && (
          <div className="users-list">
            <p>Showing {users.length} of {total} users</p>
            {users.map(user => (
              <div key={user.id} className={`user-item ${user.pending ? 'pending' : ''}`}>
                <span>{user.name} ({user.email})</span>
                {user.pending && <em>Saving...</em>}
                <div className="user-actions">
                  <button onClick={() => setSelectedUserId(user.id)}>
                    View Details
                  </button>
                  <button onClick={() => handleUpdateUser(user.id, { 
                    name: `${user.name} (Updated)` 
                  })}>
                    Update
                  </button>
                  <button onClick={() => handleDeleteUser(user.id)}>
                    Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
        
        {/* Pagination */}
        <div className="pagination">
          <button 
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
          >
            Previous
          </button>
          <span>Page {page} of {totalPages}</span>
          <button 
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
          >
            Next
          </button>
        </div>
        
        <button onClick={handleCreateUser}>
          Create User
        </button>
        
        <button onClick={() => mutate()}>
          Refresh Users
        </button>
      </section>
      
      {/* Selected User Details */}
      {selectedUserId && (
        <section className="user-details">
          <h4>User Details</h4>
          {userLoading && <div>Loading user details...</div>}
          {selectedUser && (
            <div>
              <h5>{selectedUser.name}</h5>
              <p>Email: {selectedUser.email}</p>
              <p>Created: {new Date(selectedUser.createdAt).toLocaleDateString()}</p>
              <p>Last Login: {selectedUser.lastLogin ? 
                new Date(selectedUser.lastLogin).toLocaleString() : 'Never'}</p>
            </div>
          )}
        </section>
      )}
      
      {/* Search Section */}
      <section className="search-section">
        <h4>Search Posts</h4>
        <input
          type="text"
          placeholder="Search posts..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        
        {searchLoading && <div>Searching...</div>}
        {searchResults.length > 0 && (
          <div className="search-results">
            <h5>Search Results ({searchResults.length})</h5>
            {searchResults.map(post => (
              <div key={post.id} className="search-result">
                <h6>{post.title}</h6>
                <p>{post.excerpt}</p>
              </div>
            ))}
          </div>
        )}
      </section>
      
      {/* Infinite Posts */}
      <section className="posts-section">
        <h4>Posts (Infinite Scroll)</h4>
        
        <div className="posts-list">
          {posts.map(post => (
            <div key={post.id} className="post-item">
              <h6>{post.title}</h6>
              <p>{post.excerpt}</p>
              <small>By {post.author} • {new Date(post.createdAt).toLocaleDateString()}</small>
            </div>
          ))}
          
          {hasMore && (
            <button 
              onClick={loadMore}
              disabled={isValidating}
            >
              {isValidating ? 'Loading more...' : 'Load More'}
            </button>
          )}
        </div>
      </section>
      
      {/* Cache Actions */}
      <section className="cache-actions">
        <h4>Cache Management</h4>
        <SWRCacheManager />
      </section>
    </div>
  );
}

// Cache management component
function SWRCacheManager() {
  const { cache, mutate } = useSWRConfig();
  const [cacheKeys, setCacheKeys] = useState([]);
  
  useEffect(() => {
    const updateCacheKeys = () => {
      const keys = Array.from(cache.keys());
      setCacheKeys(keys);
    };
    
    updateCacheKeys();
    const interval = setInterval(updateCacheKeys, 2000);
    
    return () => clearInterval(interval);
  }, [cache]);
  
  const clearAllCache = () => {
    cacheKeys.forEach(key => {
      mutate(key, undefined, { revalidate: false });
    });
  };
  
  const revalidateAll = () => {
    cacheKeys.forEach(key => {
      mutate(key);
    });
  };
  
  return (
    <div className="cache-manager">
      <p>Cached keys: {cacheKeys.length}</p>
      
      <div className="cache-actions">
        <button onClick={clearAllCache}>
          Clear All Cache
        </button>
        <button onClick={revalidateAll}>
          Revalidate All
        </button>
      </div>
      
      {cacheKeys.length > 0 && (
        <details>
          <summary>Cache Keys</summary>
          <ul>
            {cacheKeys.map((key, index) => (
              <li key={index}>
                {typeof key === 'string' ? key : JSON.stringify(key)}
                <button onClick={() => mutate(key)}>Revalidate</button>
                <button onClick={() => mutate(key, undefined, { revalidate: false })}>
                  Clear
                </button>
              </li>
            ))}
          </ul>
        </details>
      )}
    </div>
  );
}

// App wrapper with SWR config
function SWRApp() {
  return (
    <SWRConfig value={swrConfig}>
      <SWRExample />
    </SWRConfig>
  );
}

export { 
  SWRApp,
  swrConfig,
  useUsers,
  useUser,
  usePostsInfinite,
  useSearchPosts,
  useOptimisticUsers,
  useRealTimeData
};
```

## 🎨 Styling Approaches & Architecture

### 🎯 CSS Modules

**Interview Critical Point:** Understanding scoped CSS and build-time optimization for component-based styling.

```jsx
// UserCard.module.css
.card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 1.5rem;
  margin-bottom: 1rem;
  transition: all 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.cardHeader {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  border-bottom: 1px solid #eee;
  padding-bottom: 0.5rem;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: 1.2rem;
}

.userInfo {
  flex: 1;
  margin-left: 1rem;
}

.userName {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin: 0 0 0.25rem 0;
}

.userEmail {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.status {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.statusActive {
  background: #d4edda;
  color: #155724;
}

.statusInactive {
  background: #f8d7da;
  color: #721c24;
}

.statusPending {
  background: #fff3cd;
  color: #856404;
}

.cardBody {
  margin-bottom: 1rem;
}

.metric {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.metricLabel {
  color: #666;
}

.metricValue {
  font-weight: 600;
  color: #333;
}

.cardActions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}

.button {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.buttonPrimary {
  background: #007bff;
  color: white;
}

.buttonPrimary:hover {
  background: #0056b3;
}

.buttonSecondary {
  background: #6c757d;
  color: white;
}

.buttonSecondary:hover {
  background: #545b62;
}

.buttonDanger {
  background: #dc3545;
  color: white;
}

.buttonDanger:hover {
  background: #c82333;
}

/* Responsive design */
@media (max-width: 768px) {
  .card {
    padding: 1rem;
  }
  
  .cardHeader {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.5rem;
  }
  
  .userInfo {
    margin-left: 0;
  }
  
  .cardActions {
    flex-direction: column;
  }
  
  .button {
    width: 100%;
  }
}

/* Dark theme support */
.card.darkTheme {
  background: #2d3748;
  color: #e2e8f0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

.card.darkTheme .cardHeader {
  border-bottom-color: #4a5568;
}

.card.darkTheme .userName {
  color: #e2e8f0;
}

.card.darkTheme .userEmail {
  color: #a0aec0;
}

.card.darkTheme .metricLabel {
  color: #a0aec0;
}

.card.darkTheme .metricValue {
  color: #e2e8f0;
}
```

```jsx
// UserCard component using CSS Modules
import React, { useState } from 'react';
import styles from './UserCard.module.css';

function UserCard({ 
  user, 
  onEdit, 
  onDelete, 
  onView, 
  theme = 'light',
  variant = 'default' 
}) {
  const [isExpanded, setIsExpanded] = useState(false);
  
  // Dynamic class composition
  const cardClasses = [
    styles.card,
    theme === 'dark' && styles.darkTheme,
    variant === 'compact' && styles.compact,
    isExpanded && styles.expanded
  ].filter(Boolean).join(' ');
  
  const statusClasses = [
    styles.status,
    user.status === 'active' && styles.statusActive,
    user.status === 'inactive' && styles.statusInactive,
    user.status === 'pending' && styles.statusPending
  ].filter(Boolean).join(' ');
  
  const getInitials = (name) => {
    return name.split(' ').map(n => n[0]).join('').toUpperCase();
  };
  
  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString();
  };
  
  return (
    <div className={cardClasses}>
      <div className={styles.cardHeader}>
        <div style={{ display: 'flex', alignItems: 'center' }}>
          <div className={styles.avatar}>
            {user.avatar ? (
              <img src={user.avatar} alt={user.name} />
            ) : (
              getInitials(user.name)
            )}
          </div>
          
          <div className={styles.userInfo}>
            <h3 className={styles.userName}>{user.name}</h3>
            <p className={styles.userEmail}>{user.email}</p>
          </div>
        </div>
        
        <div className={statusClasses}>
          {user.status}
        </div>
      </div>
      
      <div className={styles.cardBody}>
        <div className={styles.metric}>
          <span className={styles.metricLabel}>Joined:</span>
          <span className={styles.metricValue}>{formatDate(user.createdAt)}</span>
        </div>
        
        <div className={styles.metric}>
          <span className={styles.metricLabel}>Posts:</span>
          <span className={styles.metricValue}>{user.postsCount || 0}</span>
        </div>
        
        <div className={styles.metric}>
          <span className={styles.metricLabel}>Role:</span>
          <span className={styles.metricValue}>{user.role}</span>
        </div>
        
        {isExpanded && (
          <div className={styles.expandedContent}>
            <div className={styles.metric}>
              <span className={styles.metricLabel}>Last Login:</span>
              <span className={styles.metricValue}>
                {user.lastLogin ? formatDate(user.lastLogin) : 'Never'}
              </span>
            </div>
            
            <div className={styles.metric}>
              <span className={styles.metricLabel}>Department:</span>
              <span className={styles.metricValue}>{user.department || 'N/A'}</span>
            </div>
          </div>
        )}
        
        <button 
          className={`${styles.button} ${styles.buttonSecondary}`}
          onClick={() => setIsExpanded(!isExpanded)}
        >
          {isExpanded ? 'Show Less' : 'Show More'}
        </button>
      </div>
      
      <div className={styles.cardActions}>
        <button 
          className={`${styles.button} ${styles.buttonPrimary}`}
          onClick={() => onView(user.id)}
        >
          View
        </button>
        
        <button 
          className={`${styles.button} ${styles.buttonSecondary}`}
          onClick={() => onEdit(user.id)}
        >
          Edit
        </button>
        
        <button 
          className={`${styles.button} ${styles.buttonDanger}`}
          onClick={() => onDelete(user.id)}
        >
          Delete
        </button>
      </div>
    </div>
  );
}

// CSS Modules utilities
const cssUtils = {
  // Compose multiple classes
  compose: (...classes) => {
    return classes.filter(Boolean).join(' ');
  },
  
  // Conditional classes
  conditionalClass: (condition, trueClass, falseClass = '') => {
    return condition ? trueClass : falseClass;
  },
  
  // Variant classes
  variantClass: (baseClass, variant, variants) => {
    return `${baseClass} ${variants[variant] || ''}`;
  }
};

export { UserCard, cssUtils };
```

### 🎯 Styled Components

**Interview Critical Point:** Understanding CSS-in-JS, dynamic styling, and component-based architecture.

```jsx
import styled, { 
  css, 
  createGlobalStyle, 
  ThemeProvider,
  keyframes 
} from 'styled-components';
import { useState, useContext } from 'react';

// Theme definition
const lightTheme = {
  colors: {
    primary: '#007bff',
    primaryHover: '#0056b3',
    secondary: '#6c757d',
    success: '#28a745',
    danger: '#dc3545',
    warning: '#ffc107',
    info: '#17a2b8',
    light: '#f8f9fa',
    dark: '#343a40',
    background: '#ffffff',
    surface: '#f8f9fa',
    text: '#333333',
    textSecondary: '#666666',
    border: '#dee2e6',
    shadow: 'rgba(0, 0, 0, 0.1)'
  },
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    xxl: '3rem'
  },
  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    full: '50%'
  },
  shadows: {
    sm: '0 1px 3px rgba(0, 0, 0, 0.1)',
    md: '0 4px 8px rgba(0, 0, 0, 0.1)',
    lg: '0 8px 16px rgba(0, 0, 0, 0.1)'
  },
  breakpoints: {
    sm: '576px',
    md: '768px',
    lg: '992px',
    xl: '1200px'
  }
};

const darkTheme = {
  ...lightTheme,
  colors: {
    ...lightTheme.colors,
    primary: '#0d6efd',
    background: '#1a1a1a',
    surface: '#2d2d2d',
    text: '#ffffff',
    textSecondary: '#b3b3b3',
    border: '#404040',
    shadow: 'rgba(0, 0, 0, 0.3)'
  }
};

// Global styles
const GlobalStyle = createGlobalStyle`
  * {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }
  
  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 
                 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif;
    background-color: ${props => props.theme.colors.background};
    color: ${props => props.theme.colors.text};
    line-height: 1.6;
    transition: background-color 0.3s ease, color 0.3s ease;
  }
  
  button {
    font-family: inherit;
  }
  
  a {
    color: ${props => props.theme.colors.primary};
    text-decoration: none;
    
    &:hover {
      text-decoration: underline;
    }
  }
`;

// Animation keyframes
const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const slideIn = keyframes`
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(0);
  }
`;

const pulse = keyframes`
  0% {
    box-shadow: 0 0 0 0 ${props => props.theme.colors.primary}40;
  }
  70% {
    box-shadow: 0 0 0 10px transparent;
  }
  100% {
    box-shadow: 0 0 0 0 transparent;
  }
`;

// Styled components with complex logic
const Card = styled.div`
  background: ${props => props.theme.colors.surface};
  border-radius: ${props => props.theme.borderRadius.md};
  box-shadow: ${props => props.theme.shadows.md};
  padding: ${props => props.theme.spacing.lg};
  margin-bottom: ${props => props.theme.spacing.md};
  transition: all 0.3s ease;
  animation: ${fadeIn} 0.5s ease-out;
  
  ${props => props.hover && css`
    &:hover {
      transform: translateY(-4px);
      box-shadow: ${props => props.theme.shadows.lg};
    }
  `}
  
  ${props => props.variant === 'elevated' && css`
    border: 1px solid ${props => props.theme.colors.border};
  `}
  
  ${props => props.variant === 'outlined' && css`
    border: 2px solid ${props => props.theme.colors.primary};
    background: transparent;
  `}
  
  ${props => props.size === 'compact' && css`
    padding: ${props => props.theme.spacing.md};
  `}
  
  ${props => props.size === 'large' && css`
    padding: ${props => props.theme.spacing.xl};
  `}
  
  @media (max-width: ${props => props.theme.breakpoints.md}) {
    padding: ${props => props.theme.spacing.md};
    margin-bottom: ${props => props.theme.spacing.sm};
  }
`;

const Button = styled.button`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: ${props => props.theme.spacing.sm};
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.lg};
  border: none;
  border-radius: ${props => props.theme.borderRadius.sm};
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  text-decoration: none;
  position: relative;
  overflow: hidden;
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  /* Base variant styles */
  ${props => {
    switch (props.variant) {
      case 'primary':
        return css`
          background: ${props => props.theme.colors.primary};
          color: white;
          
          &:hover:not(:disabled) {
            background: ${props => props.theme.colors.primaryHover};
          }
          
          &:active {
            transform: scale(0.98);
          }
        `;
      
      case 'secondary':
        return css`
          background: ${props => props.theme.colors.secondary};
          color: white;
          
          &:hover:not(:disabled) {
            background: ${props => props.theme.colors.text};
          }
        `;
      
      case 'outlined':
        return css`
          background: transparent;
          color: ${props => props.theme.colors.primary};
          border: 2px solid ${props => props.theme.colors.primary};
          
          &:hover:not(:disabled) {
            background: ${props => props.theme.colors.primary};
            color: white;
          }
        `;
      
      case 'ghost':
        return css`
          background: transparent;
          color: ${props => props.theme.colors.text};
          
          &:hover:not(:disabled) {
            background: ${props => props.theme.colors.light};
          }
        `;
      
      case 'danger':
        return css`
          background: ${props => props.theme.colors.danger};
          color: white;
          
          &:hover:not(:disabled) {
            background: #c82333;
          }
        `;
      
      default:
        return css`
          background: ${props => props.theme.colors.light};
          color: ${props => props.theme.colors.text};
          
          &:hover:not(:disabled) {
            background: ${props => props.theme.colors.border};
          }
        `;
    }
  }}
  
  /* Size variants */
  ${props => {
    switch (props.size) {
      case 'small':
        return css`
          padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.md};
          font-size: 0.875rem;
        `;
      
      case 'large':
        return css`
          padding: ${props => props.theme.spacing.md} ${props => props.theme.spacing.xl};
          font-size: 1.125rem;
        `;
      
      default:
        return css`
          padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.lg};
          font-size: 1rem;
        `;
    }
  }}
  
  /* Loading state */
  ${props => props.loading && css`
    color: transparent;
    
    &::after {
      content: '';
      position: absolute;
      width: 16px;
      height: 16px;
      border: 2px solid transparent;
      border-top: 2px solid currentColor;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  `}
  
  /* Pulse effect for primary buttons */
  ${props => props.variant === 'primary' && props.pulse && css`
    animation: ${pulse} 2s infinite;
  `}
`;

const Input = styled.input`
  width: 100%;
  padding: ${props => props.theme.spacing.sm} ${props => props.theme.spacing.md};
  border: 2px solid ${props => props.theme.colors.border};
  border-radius: ${props => props.theme.borderRadius.sm};
  font-size: 1rem;
  background: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text};
  transition: all 0.2s ease;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 0 3px ${props => props.theme.colors.primary}20;
  }
  
  &::placeholder {
    color: ${props => props.theme.colors.textSecondary};
  }
  
  ${props => props.error && css`
    border-color: ${props => props.theme.colors.danger};
    
    &:focus {
      border-color: ${props => props.theme.colors.danger};
      box-shadow: 0 0 0 3px ${props => props.theme.colors.danger}20;
    }
  `}
  
  ${props => props.success && css`
    border-color: ${props => props.theme.colors.success};
    
    &:focus {
      border-color: ${props => props.theme.colors.success};
      box-shadow: 0 0 0 3px ${props => props.theme.colors.success}20;
    }
  `}
`;

const Avatar = styled.div`
  width: ${props => props.size || '40px'};
  height: ${props => props.size || '40px'};
  border-radius: ${props => props.theme.borderRadius.full};
  background: ${props => props.color || `linear-gradient(135deg, 
    ${props.theme.colors.primary} 0%, 
    ${props.theme.colors.secondary} 100%)`};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: bold;
  font-size: ${props => {
    const size = parseInt(props.size) || 40;
    return `${size * 0.4}px`;
  }};
  overflow: hidden;
  
  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  ${props => props.online && css`
    position: relative;
    
    &::after {
      content: '';
      position: absolute;
      bottom: 2px;
      right: 2px;
      width: 12px;
      height: 12px;
      background: ${props => props.theme.colors.success};
      border: 2px solid ${props => props.theme.colors.background};
      border-radius: 50%;
    }
  `}
`;

const Grid = styled.div`
  display: grid;
  gap: ${props => props.gap || props.theme.spacing.md};
  
  ${props => {
    if (props.columns) {
      return css`
        grid-template-columns: repeat(${props.columns}, 1fr);
      `;
    }
    
    return css`
      grid-template-columns: repeat(auto-fit, minmax(${props.minWidth || '300px'}, 1fr));
    `;
  }}
  
  @media (max-width: ${props => props.theme.breakpoints.md}) {
    grid-template-columns: 1fr;
  }
`;

const Flex = styled.div`
  display: flex;
  gap: ${props => props.gap || props.theme.spacing.md};
  
  ${props => props.direction && css`
    flex-direction: ${props.direction};
  `}
  
  ${props => props.align && css`
    align-items: ${props.align};
  `}
  
  ${props => props.justify && css`
    justify-content: ${props.justify};
  `}
  
  ${props => props.wrap && css`
    flex-wrap: wrap;
  `}
  
  @media (max-width: ${props => props.theme.breakpoints.md}) {
    ${props => props.responsive && css`
      flex-direction: column;
    `}
  }
`;

// Complex styled component with multiple states
const UserCard = styled(Card)`
  ${props => props.status === 'online' && css`
    border-left: 4px solid ${props => props.theme.colors.success};
  `}
  
  ${props => props.status === 'offline' && css`
    border-left: 4px solid ${props => props.theme.colors.textSecondary};
    opacity: 0.8;
  `}
  
  ${props => props.status === 'busy' && css`
    border-left: 4px solid ${props => props.theme.colors.danger};
  `}
  
  ${props => props.featured && css`
    background: linear-gradient(135deg, 
      ${props => props.theme.colors.primary}10 0%, 
      ${props => props.theme.colors.secondary}10 100%);
    border: 2px solid ${props => props.theme.colors.primary}30;
  `}
`;

const StatusBadge = styled.span`
  display: inline-flex;
  align-items: center;
  gap: ${props => props.theme.spacing.xs};
  padding: ${props => props.theme.spacing.xs} ${props => props.theme.spacing.sm};
  border-radius: ${props => props.theme.borderRadius.full};
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  
  &::before {
    content: '';
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: currentColor;
  }
  
  ${props => {
    switch (props.status) {
      case 'active':
        return css`
          background: ${props => props.theme.colors.success}20;
          color: ${props => props.theme.colors.success};
        `;
      
      case 'inactive':
        return css`
          background: ${props => props.theme.colors.danger}20;
          color: ${props => props.theme.colors.danger};
        `;
      
      case 'pending':
        return css`
          background: ${props => props.theme.colors.warning}20;
          color: ${props => props.theme.colors.warning};
        `;
      
      default:
        return css`
          background: ${props => props.theme.colors.textSecondary}20;
          color: ${props => props.theme.colors.textSecondary};
        `;
    }
  }}
`;

// Component using styled-components
function StyledUserCard({ user, onEdit, onDelete, onView, featured = false }) {
  const [isLoading, setIsLoading] = useState({});
  
  const handleAction = async (action, id) => {
    setIsLoading(prev => ({ ...prev, [action]: true }));
    
    try {
      await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
      
      switch (action) {
        case 'edit':
          onEdit(id);
          break;
        case 'delete':
          onDelete(id);
          break;
        case 'view':
          onView(id);
          break;
      }
    } finally {
      setIsLoading(prev => ({ ...prev, [action]: false }));
    }
  };
  
  return (
    <UserCard 
      status={user.status} 
      featured={featured}
      hover
    >
      <Flex align="center" justify="space-between">
        <Flex align="center">
          <Avatar 
            size="50px" 
            online={user.status === 'online'}
            color={user.avatarColor}
          >
            {user.avatar ? (
              <img src={user.avatar} alt={user.name} />
            ) : (
              user.name.charAt(0).toUpperCase()
            )}
          </Avatar>
          
          <div>
            <h3 style={{ margin: 0, marginBottom: '4px' }}>{user.name}</h3>
            <p style={{ margin: 0, color: 'var(--text-secondary)' }}>
              {user.email}
            </p>
          </div>
        </Flex>
        
        <StatusBadge status={user.status}>
          {user.status}
        </StatusBadge>
      </Flex>
      
      <div style={{ margin: '1rem 0' }}>
        <Flex justify="space-between" style={{ marginBottom: '0.5rem' }}>
          <span>Posts:</span>
          <strong>{user.postsCount || 0}</strong>
        </Flex>
        
        <Flex justify="space-between" style={{ marginBottom: '0.5rem' }}>
          <span>Role:</span>
          <strong>{user.role}</strong>
        </Flex>
        
        <Flex justify="space-between">
          <span>Joined:</span>
          <strong>{new Date(user.createdAt).toLocaleDateString()}</strong>
        </Flex>
      </div>
      
      <Flex gap="0.5rem" responsive>
        <Button 
          variant="primary" 
          onClick={() => handleAction('view', user.id)}
          loading={isLoading.view}
        >
          View
        </Button>
        
        <Button 
          variant="outlined" 
          onClick={() => handleAction('edit', user.id)}
          loading={isLoading.edit}
        >
          Edit
        </Button>
        
        <Button 
          variant="danger" 
          onClick={() => handleAction('delete', user.id)}
          loading={isLoading.delete}
        >
          Delete
        </Button>
      </Flex>
    </UserCard>
  );
}

// Theme toggle hook
function useTheme() {
  const [isDark, setIsDark] = useState(false);
  
  const toggleTheme = () => setIsDark(!isDark);
  const theme = isDark ? darkTheme : lightTheme;
  
  return { theme, isDark, toggleTheme };
}

// Styled components example app
function StyledComponentsExample() {
  const { theme, isDark, toggleTheme } = useTheme();
  
  const users = [
    {
      id: 1,
      name: 'John Doe',
      email: 'john@example.com',
      status: 'online',
      role: 'Admin',
      postsCount: 25,
      createdAt: '2023-01-15'
    },
    {
      id: 2,
      name: 'Jane Smith',
      email: 'jane@example.com',
      status: 'offline',
      role: 'User',
      postsCount: 12,
      createdAt: '2023-02-20'
    },
    {
      id: 3,
      name: 'Bob Johnson',
      email: 'bob@example.com',
      status: 'busy',
      role: 'Moderator',
      postsCount: 38,
      createdAt: '2023-01-10'
    }
  ];
  
  const handleEdit = (id) => console.log('Edit user:', id);
  const handleDelete = (id) => console.log('Delete user:', id);
  const handleView = (id) => console.log('View user:', id);
  
  return (
    <ThemeProvider theme={theme}>
      <GlobalStyle />
      
      <div style={{ padding: '2rem', minHeight: '100vh' }}>
        <Flex align="center" justify="space-between" style={{ marginBottom: '2rem' }}>
          <h1>Styled Components Example</h1>
          <Button variant="outlined" onClick={toggleTheme}>
            {isDark ? '☀️' : '🌙'} Toggle Theme
          </Button>
        </Flex>
        
        <Grid minWidth="350px">
          {users.map((user, index) => (
            <StyledUserCard
              key={user.id}
              user={user}
              onEdit={handleEdit}
              onDelete={handleDelete}
              onView={handleView}
              featured={index === 0}
            />
          ))}
        </Grid>
        
        <Card style={{ marginTop: '2rem' }}>
          <h3>Theme Configuration</h3>
          <p>Current theme: {isDark ? 'Dark' : 'Light'}</p>
          <p>Primary color: {theme.colors.primary}</p>
          <p>Background: {theme.colors.background}</p>
        </Card>
      </div>
    </ThemeProvider>
  );
}

export { 
  StyledComponentsExample, 
  lightTheme, 
  darkTheme, 
  Button, 
  Card, 
  Input, 
  Avatar, 
  Grid, 
  Flex,
  useTheme 
};
```

### 🎯 Tailwind CSS

**Interview Critical Point:** Understanding utility-first CSS and design system consistency.

```jsx
// tailwind.config.js
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        secondary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['Fira Code', 'monospace'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'bounce-in': 'bounceIn 0.6s ease-out',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        slideUp: {
          '0%': { transform: 'translateY(100%)' },
          '100%': { transform: 'translateY(0)' },
        },
        bounceIn: {
          '0%': { transform: 'scale(0.3)', opacity: '0' },
          '50%': { transform: 'scale(1.05)' },
          '70%': { transform: 'scale(0.9)' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        }
      },
      screens: {
        'xs': '475px',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
  ],
  darkMode: 'class',
}
```

```jsx
import React, { useState, useEffect } from 'react';
import { ChevronDownIcon, UserIcon, CogIcon } from '@heroicons/react/24/outline';

// Tailwind utility functions
const cn = (...classes) => {
  return classes.filter(Boolean).join(' ');
};

const variants = {
  button: {
    primary: 'bg-primary-600 hover:bg-primary-700 text-white',
    secondary: 'bg-secondary-600 hover:bg-secondary-700 text-white',
    outline: 'border-2 border-primary-600 text-primary-600 hover:bg-primary-600 hover:text-white',
    ghost: 'text-secondary-700 hover:bg-secondary-100',
    danger: 'bg-red-600 hover:bg-red-700 text-white',
  },
  size: {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-4 py-2 text-base',
    lg: 'px-6 py-3 text-lg',
  }
};

// Reusable Button component with Tailwind
function Button({ 
  children, 
  variant = 'primary', 
  size = 'md', 
  loading = false,
  disabled = false,
  className = '',
  ...props 
}) {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variantClasses = variants.button[variant] || variants.button.primary;
  const sizeClasses = variants.size[size] || variants.size.md;
  
  return (
    <button
      className={cn(
        baseClasses,
        variantClasses,
        sizeClasses,
        loading && 'cursor-wait',
        className
      )}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <svg className="animate-spin -ml-1 mr-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
        </svg>
      )}
      {children}
    </button>
  );
}

// Card component with Tailwind
function Card({ 
  children, 
  hover = false, 
  shadow = 'md',
  padding = 'lg',
  className = '',
  ...props 
}) {
  const shadowClasses = {
    sm: 'shadow-sm',
    md: 'shadow-md',
    lg: 'shadow-lg',
    xl: 'shadow-xl'
  };
  
  const paddingClasses = {
    sm: 'p-4',
    md: 'p-5',
    lg: 'p-6',
    xl: 'p-8'
  };
  
  return (
    <div
      className={cn(
        'bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700',
        shadowClasses[shadow],
        paddingClasses[padding],
        hover && 'hover:shadow-lg hover:-translate-y-1 transition-all duration-300',
        'animate-fade-in',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

// Avatar component with Tailwind
function Avatar({ 
  src, 
  alt, 
  size = 'md', 
  online = false, 
  initials,
  className = '',
  ...props 
}) {
  const sizes = {
    xs: 'w-6 h-6 text-xs',
    sm: 'w-8 h-8 text-sm',
    md: 'w-10 h-10 text-base',
    lg: 'w-12 h-12 text-lg',
    xl: 'w-16 h-16 text-xl',
    '2xl': 'w-20 h-20 text-2xl'
  };
  
  const onlineIndicatorSizes = {
    xs: 'w-1.5 h-1.5',
    sm: 'w-2 h-2',
    md: 'w-2.5 h-2.5',
    lg: 'w-3 h-3',
    xl: 'w-4 h-4',
    '2xl': 'w-5 h-5'
  };
  
  return (
    <div className={cn('relative inline-block', className)} {...props}>
      <div className={cn(
        'rounded-full overflow-hidden bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center text-white font-semibold',
        sizes[size]
      )}>
        {src ? (
          <img 
            src={src} 
            alt={alt} 
            className="w-full h-full object-cover"
          />
        ) : (
          <span>{initials || '?'}</span>
        )}
      </div>
      
      {online && (
        <div className={cn(
          'absolute bottom-0 right-0 bg-green-400 border-2 border-white dark:border-gray-800 rounded-full',
          onlineIndicatorSizes[size]
        )} />
      )}
    </div>
  );
}

// Status Badge component
function StatusBadge({ status, children, className = '' }) {
  const statusStyles = {
    active: 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
    inactive: 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200',
    pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200',
    draft: 'bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200',
  };
  
  return (
    <span className={cn(
      'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium',
      statusStyles[status] || statusStyles.draft,
      className
    )}>
      <span className={cn(
        'w-1.5 h-1.5 mr-1.5 rounded-full',
        status === 'active' && 'bg-green-400',
        status === 'inactive' && 'bg-red-400',
        status === 'pending' && 'bg-yellow-400',
        status === 'draft' && 'bg-gray-400'
      )} />
      {children || status}
    </span>
  );
}

// Tailwind UserCard component
function TailwindUserCard({ 
  user, 
  onEdit, 
  onDelete, 
  onView, 
  featured = false,
  compact = false 
}) {
  const [isLoading, setIsLoading] = useState({});
  const [isExpanded, setIsExpanded] = useState(false);
  
  const handleAction = async (action, id) => {
    setIsLoading(prev => ({ ...prev, [action]: true }));
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    switch (action) {
      case 'edit':
        onEdit(id);
        break;
      case 'delete':
        onDelete(id);
        break;
      case 'view':
        onView(id);
        break;
    }
    
    setIsLoading(prev => ({ ...prev, [action]: false }));
  };
  
  return (
    <Card 
      hover
      className={cn(
        'transition-all duration-300',
        featured && 'ring-2 ring-primary-500 ring-opacity-50 bg-gradient-to-br from-primary-50 to-transparent dark:from-primary-900/20',
        compact ? 'p-4' : 'p-6'
      )}
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <Avatar
            src={user.avatar}
            initials={user.name.charAt(0)}
            size={compact ? 'md' : 'lg'}
            online={user.status === 'active'}
            alt={user.name}
          />
          
          <div className="min-w-0 flex-1">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white truncate">
              {user.name}
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 truncate">
              {user.email}
            </p>
            {!compact && (
              <p className="text-xs text-gray-400 dark:text-gray-500 mt-1">
                {user.role} • Joined {new Date(user.createdAt).toLocaleDateString()}
              </p>
            )}
          </div>
        </div>
        
        <StatusBadge status={user.status}>
          {user.status}
        </StatusBadge>
      </div>
      
      {/* Metrics */}
      {!compact && (
        <div className="grid grid-cols-2 gap-4 mb-4 p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg">
          <div className="text-center">
            <div className="text-2xl font-bold text-primary-600 dark:text-primary-400">
              {user.postsCount || 0}
            </div>
            <div className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">
              Posts
            </div>
          </div>
          
          <div className="text-center">
            <div className="text-2xl font-bold text-secondary-600 dark:text-secondary-400">
              {user.commentsCount || 0}
            </div>
            <div className="text-xs text-gray-500 dark:text-gray-400 uppercase tracking-wide">
              Comments
            </div>
          </div>
        </div>
      )}
      
      {/* Expandable content */}
      {isExpanded && (
        <div className="mb-4 p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg animate-slide-up">
          <h4 className="text-sm font-medium text-gray-900 dark:text-white mb-2">
            Additional Information
          </h4>
          
          <div className="space-y-2 text-sm">
            <div className="flex justify-between">
              <span className="text-gray-500 dark:text-gray-400">Department:</span>
              <span className="text-gray-900 dark:text-white">{user.department || 'N/A'}</span>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-500 dark:text-gray-400">Last Login:</span>
              <span className="text-gray-900 dark:text-white">
                {user.lastLogin ? new Date(user.lastLogin).toLocaleDateString() : 'Never'}
              </span>
            </div>
            
            <div className="flex justify-between">
              <span className="text-gray-500 dark:text-gray-400">Location:</span>
              <span className="text-gray-900 dark:text-white">{user.location || 'Unknown'}</span>
            </div>
          </div>
        </div>
      )}
      
      {/* Actions */}
      <div className="flex flex-wrap gap-2">
        <Button
          variant="primary"
          size="sm"
          onClick={() => handleAction('view', user.id)}
          loading={isLoading.view}
          className="flex-1 sm:flex-none"
        >
          <UserIcon className="w-4 h-4 mr-1" />
          View
        </Button>
        
        <Button
          variant="outline"
          size="sm"
          onClick={() => handleAction('edit', user.id)}
          loading={isLoading.edit}
          className="flex-1 sm:flex-none"
        >
          <CogIcon className="w-4 h-4 mr-1" />
          Edit
        </Button>
        
        <Button
          variant="danger"
          size="sm"
          onClick={() => handleAction('delete', user.id)}
          loading={isLoading.delete}
          className="flex-1 sm:flex-none"
        >
          Delete
        </Button>
        
        {!compact && (
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
            className="ml-auto"
          >
            <ChevronDownIcon className={cn(
              'w-4 h-4 transition-transform duration-200',
              isExpanded && 'rotate-180'
            )} />
            {isExpanded ? 'Less' : 'More'}
          </Button>
        )}
      </div>
      
      {/* Featured badge */}
      {featured && (
        <div className="absolute -top-2 -right-2">
          <div className="bg-primary-500 text-white text-xs font-bold px-2 py-1 rounded-full">
            Featured
          </div>
        </div>
      )}
    </Card>
  );
}

// Dark mode toggle hook
function useDarkMode() {
  const [isDark, setIsDark] = useState(() => {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('darkMode') === 'true' ||
        (!localStorage.getItem('darkMode') && window.matchMedia('(prefers-color-scheme: dark)').matches);
    }
    return false;
  });
  
  useEffect(() => {
    const root = window.document.documentElement;
    if (isDark) {
      root.classList.add('dark');
    } else {
      root.classList.remove('dark');
    }
    localStorage.setItem('darkMode', isDark.toString());
  }, [isDark]);
  
  return { isDark, setIsDark, toggle: () => setIsDark(!isDark) };
}

// Responsive grid component
function ResponsiveGrid({ children, className = '' }) {
  return (
    <div className={cn(
      'grid gap-6',
      'grid-cols-1',
      'sm:grid-cols-2',
      'lg:grid-cols-3',
      'xl:grid-cols-4',
      '2xl:grid-cols-5',
      className
    )}>
      {children}
    </div>
  );
}

// Main Tailwind example component
function TailwindExample() {
  const { isDark, toggle } = useDarkMode();
  const [viewMode, setViewMode] = useState('grid');
  const [filter, setFilter] = useState('all');
  
  const users = [
    {
      id: 1,
      name: 'Alice Johnson',
      email: 'alice@example.com',
      status: 'active',
      role: 'Admin',
      postsCount: 42,
      commentsCount: 128,
      department: 'Engineering',
      location: 'San Francisco',
      createdAt: '2023-01-15',
      lastLogin: '2024-03-10'
    },
    {
      id: 2,
      name: 'Bob Smith',
      email: 'bob@example.com',
      status: 'inactive',
      role: 'User',
      postsCount: 18,
      commentsCount: 45,
      department: 'Marketing',
      location: 'New York',
      createdAt: '2023-02-20',
      lastLogin: '2024-02-28'
    },
    {
      id: 3,
      name: 'Carol Davis',
      email: 'carol@example.com',
      status: 'pending',
      role: 'Moderator',
      postsCount: 31,
      commentsCount: 87,
      department: 'Support',
      location: 'London',
      createdAt: '2023-01-10',
      lastLogin: '2024-03-09'
    },
    {
      id: 4,
      name: 'David Wilson',
      email: 'david@example.com',
      status: 'active',
      role: 'User',
      postsCount: 7,
      commentsCount: 23,
      department: 'Sales',
      location: 'Toronto',
      createdAt: '2023-03-05',
      lastLogin: '2024-03-08'
    }
  ];
  
  const filteredUsers = filter === 'all' 
    ? users 
    : users.filter(user => user.status === filter);
  
  const handleEdit = (id) => console.log('Edit user:', id);
  const handleDelete = (id) => console.log('Delete user:', id);
  const handleView = (id) => console.log('View user:', id);
  
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-300">
      <div className="max-w-7xl mx-auto p-6">
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-8">
          <div className="mb-4 sm:mb-0">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Tailwind CSS Example
            </h1>
            <p className="text-gray-600 dark:text-gray-400 mt-1">
              Utility-first CSS framework demonstration
            </p>
          </div>
          
          <div className="flex items-center space-x-4">
            {/* View mode toggle */}
            <div className="flex bg-white dark:bg-gray-800 rounded-lg p-1 border border-gray-200 dark:border-gray-700">
              <button
                onClick={() => setViewMode('grid')}
                className={cn(
                  'px-3 py-1 text-sm font-medium rounded-md transition-colors duration-200',
                  viewMode === 'grid'
                    ? 'bg-primary-500 text-white'
                    : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
                )}
              >
                Grid
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={cn(
                  'px-3 py-1 text-sm font-medium rounded-md transition-colors duration-200',
                  viewMode === 'list'
                    ? 'bg-primary-500 text-white'
                    : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
                )}
              >
                List
              </button>
            </div>
            
            {/* Dark mode toggle */}
            <Button
              variant="outline"
              onClick={toggle}
              className="p-2"
            >
              {isDark ? '☀️' : '🌙'}
            </Button>
          </div>
        </div>
        
        {/* Filters */}
        <div className="flex flex-wrap gap-2 mb-6">
          {['all', 'active', 'inactive', 'pending'].map((status) => (
            <button
              key={status}
              onClick={() => setFilter(status)}
              className={cn(
                'px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200',
                filter === status
                  ? 'bg-primary-500 text-white'
                  : 'bg-white dark:bg-gray-800 text-gray-700 dark:text-gray-300 border border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700'
              )}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
              <span className="ml-2 text-xs opacity-75">
                ({status === 'all' ? users.length : users.filter(u => u.status === status).length})
              </span>
            </button>
          ))}
        </div>
        
        {/* Users display */}
        {viewMode === 'grid' ? (
          <ResponsiveGrid>
            {filteredUsers.map((user, index) => (
              <TailwindUserCard
                key={user.id}
                user={user}
                onEdit={handleEdit}
                onDelete={handleDelete}
                onView={handleView}
                featured={index === 0}
              />
            ))}
          </ResponsiveGrid>
        ) : (
          <div className="space-y-4">
            {filteredUsers.map((user, index) => (
              <TailwindUserCard
                key={user.id}
                user={user}
                onEdit={handleEdit}
                onDelete={handleDelete}
                onView={handleView}
                featured={index === 0}
                compact
              />
            ))}
          </div>
        )}
        
        {/* Empty state */}
        {filteredUsers.length === 0 && (
          <Card className="text-center py-12">
            <div className="text-gray-400 dark:text-gray-500 mb-4">
              <UserIcon className="w-12 h-12 mx-auto" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              No users found
            </h3>
            <p className="text-gray-500 dark:text-gray-400">
              Try adjusting your filter to see more results.
            </p>
          </Card>
        )}
        
        {/* Stats footer */}
        <Card className="mt-8 bg-gradient-to-r from-primary-500 to-secondary-500 text-white">
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-3xl font-bold">{users.length}</div>
              <div className="text-sm opacity-90">Total Users</div>
            </div>
            <div>
              <div className="text-3xl font-bold">
                {users.filter(u => u.status === 'active').length}
              </div>
              <div className="text-sm opacity-90">Active Users</div>
            </div>
            <div>
              <div className="text-3xl font-bold">
                {users.reduce((acc, user) => acc + (user.postsCount || 0), 0)}
              </div>
              <div className="text-sm opacity-90">Total Posts</div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}

export { 
  TailwindExample, 
  Button, 
  Card, 
  Avatar, 
  StatusBadge, 
  useDarkMode, 
  ResponsiveGrid,
  cn 
};
```

## 🔄 Integration Patterns & Best Practices

### 🎯 Ecosystem Integration Architecture

**Interview Critical Point:** Understanding how to integrate multiple ecosystem tools effectively and avoid common pitfalls.

```jsx
// Modern React app architecture with ecosystem integration
import React, { Suspense, lazy, ErrorBoundary } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SWRConfig } from 'swr';
import { BrowserRouter } from 'react-router-dom';
import { ThemeProvider } from 'styled-components';
import { ErrorBoundary as ReactErrorBoundary } from 'react-error-boundary';

// Architecture patterns for ecosystem integration
class EcosystemArchitecture {
  constructor() {
    this.patterns = {
      // Data fetching strategy
      dataStrategy: 'hybrid', // 'react-query', 'swr', 'hybrid'
      
      // Styling approach
      stylingStrategy: 'utility-first', // 'css-modules', 'styled-components', 'utility-first'
      
      // Form management
      formStrategy: 'react-hook-form', // 'formik', 'react-hook-form'
      
      // Routing approach
      routingStrategy: 'declarative', // 'imperative', 'declarative'
      
      // State management
      stateStrategy: 'server-client-split' // 'all-client', 'server-client-split'
    };
  }
  
  // Data fetching integration pattern
  createDataLayer() {
    return {
      // Primary data fetching with React Query
      primary: 'react-query',
      
      // Real-time updates with SWR
      realtime: 'swr',
      
      // Critical data with native fetch
      critical: 'native-fetch',
      
      // Background sync
      background: 'service-worker'
    };
  }
  
  // Styling integration pattern
  createStylingLayer() {
    return {
      // Design system with Tailwind
      designSystem: 'tailwind',
      
      // Component styling with CSS Modules
      componentStyling: 'css-modules',
      
      // Dynamic styling with Styled Components
      dynamicStyling: 'styled-components',
      
      // Global styles
      globalStyles: 'css-custom-properties'
    };
  }
  
  // Form integration pattern
  createFormLayer() {
    return {
      // Complex forms with React Hook Form
      complex: 'react-hook-form',
      
      // Simple forms with controlled components
      simple: 'controlled',
      
      // Validation with Zod
      validation: 'zod',
      
      // Field-level validation
      fieldValidation: 'yup'
    };
  }
}

// Unified data fetching hook combining React Query and SWR
function useUnifiedData(key, options = {}) {
  const {
    strategy = 'react-query',
    realtime = false,
    background = false,
    fallback = null
  } = options;
  
  // React Query for primary data fetching
  const queryResult = useQuery({
    queryKey: [key],
    queryFn: options.queryFn,
    enabled: strategy === 'react-query' && !realtime,
    ...options.queryOptions
  });
  
  // SWR for real-time data
  const { data: swrData, error: swrError, mutate } = useSWR(
    realtime ? key : null,
    options.swrFetcher,
    {
      refreshInterval: realtime ? 5000 : 0,
      ...options.swrOptions
    }
  );
  
  // Background sync
  useEffect(() => {
    if (!background) return;
    
    const handleBackgroundSync = () => {
      if (strategy === 'react-query') {
        queryResult.refetch();
      } else {
        mutate();
      }
    };
    
    document.addEventListener('visibilitychange', handleBackgroundSync);
    window.addEventListener('online', handleBackgroundSync);
    
    return () => {
      document.removeEventListener('visibilitychange', handleBackgroundSync);
      window.removeEventListener('online', handleBackgroundSync);
    };
  }, [background, strategy, queryResult.refetch, mutate]);
  
  // Return unified interface
  if (realtime) {
    return {
      data: swrData || fallback,
      error: swrError,
      loading: !swrData && !swrError,
      refetch: mutate
    };
  }
  
  return {
    data: queryResult.data || fallback,
    error: queryResult.error,
    loading: queryResult.isLoading,
    refetch: queryResult.refetch
  };
}

// Multi-strategy form hook
function useMultiStrategyForm(schema, options = {}) {
  const {
    strategy = 'react-hook-form',
    validation = 'zod',
    optimistic = false
  } = options;
  
  // React Hook Form implementation
  const rhfForm = useForm({
    resolver: validation === 'zod' ? zodResolver(schema) : yupResolver(schema),
    ...options.rhfOptions
  });
  
  // Formik implementation (alternative)
  const formikBag = useFormik({
    initialValues: options.initialValues || {},
    validationSchema: validation === 'yup' ? schema : undefined,
    validate: validation === 'zod' ? (values) => {
      try {
        schema.parse(values);
        return {};
      } catch (error) {
        return error.flatten().fieldErrors;
      }
    } : undefined,
    ...options.formikOptions
  });
  
  // Optimistic updates
  const { mutate } = useSWRConfig();
  
  const submitForm = async (data) => {
    if (optimistic) {
      // Optimistic update
      await mutate(
        options.cacheKey,
        (currentData) => ({ ...currentData, ...data }),
        { revalidate: false }
      );
    }
    
    try {
      const result = await options.onSubmit(data);
      
      if (optimistic) {
        // Update with server response
        await mutate(options.cacheKey, result, { revalidate: false });
      }
      
      return result;
    } catch (error) {
      if (optimistic) {
        // Rollback on error
        await mutate(options.cacheKey);
      }
      throw error;
    }
  };
  
  // Return strategy-specific interface
  if (strategy === 'formik') {
    return {
      ...formikBag,
      handleSubmit: (e) => {
        e.preventDefault();
        return submitForm(formikBag.values);
      }
    };
  }
  
  return {
    ...rhfForm,
    handleSubmit: rhfForm.handleSubmit(submitForm)
  };
}

// Unified styling system
function useUnifiedStyling() {
  const [theme, setTheme] = useState('light');
  const [styleStrategy, setStyleStrategy] = useState('tailwind');
  
  // CSS-in-JS theme
  const styledTheme = {
    colors: {
      primary: theme === 'light' ? '#3b82f6' : '#60a5fa',
      background: theme === 'light' ? '#ffffff' : '#1f2937',
      text: theme === 'light' ? '#1f2937' : '#f9fafb'
    },
    spacing: {
      sm: '0.5rem',
      md: '1rem',
      lg: '1.5rem'
    }
  };
  
  // Tailwind classes
  const tailwindClasses = {
    card: theme === 'light' 
      ? 'bg-white text-gray-900 border-gray-200'
      : 'bg-gray-800 text-white border-gray-700',
    button: theme === 'light'
      ? 'bg-blue-500 hover:bg-blue-600 text-white'
      : 'bg-blue-600 hover:bg-blue-700 text-white'
  };
  
  // CSS Modules classes (would be imported)
  const cssModuleClasses = {
    card: `card ${theme === 'dark' ? 'dark' : ''}`,
    button: `button primary ${theme === 'dark' ? 'dark' : ''}`
  };
  
  const getStyles = (component) => {
    switch (styleStrategy) {
      case 'tailwind':
        return tailwindClasses[component];
      
      case 'css-modules':
        return cssModuleClasses[component];
      
      case 'styled-components':
        return styledTheme;
      
      default:
        return tailwindClasses[component];
    }
  };
  
  return {
    theme,
    setTheme,
    styleStrategy,
    setStyleStrategy,
    getStyles,
    styledTheme
  };
}

// Performance monitoring for ecosystem integration
function usePerformanceMonitoring() {
  const [metrics, setMetrics] = useState({});
  
  useEffect(() => {
    // Monitor React Query cache
    const queryClient = useQueryClient();
    const cache = queryClient.getQueryCache();
    
    const updateMetrics = () => {
      const queries = cache.getAll();
      
      setMetrics(prev => ({
        ...prev,
        reactQuery: {
          totalQueries: queries.length,
          staleQueries: queries.filter(q => q.isStale()).length,
          fetchingQueries: queries.filter(q => q.state.fetchStatus === 'fetching').length,
          errorQueries: queries.filter(q => q.state.status === 'error').length
        },
        performance: {
          renderTime: performance.now(),
          memoryUsage: performance.memory?.usedJSHeapSize || 0
        }
      }));
    };
    
    const interval = setInterval(updateMetrics, 5000);
    updateMetrics();
    
    return () => clearInterval(interval);
  }, []);
  
  return metrics;
}

// Error boundary integration
function EcosystemErrorBoundary({ children, fallback }) {
  const handleError = (error, errorInfo) => {
    console.error('Ecosystem Error:', error, errorInfo);
    
    // Log to monitoring service
    if (window.analytics) {
      window.analytics.track('Ecosystem Error', {
        error: error.message,
        stack: error.stack,
        componentStack: errorInfo.componentStack
      });
    }
  };
  
  return (
    <ReactErrorBoundary
      FallbackComponent={fallback || EcosystemErrorFallback}
      onError={handleError}
    >
      {children}
    </ReactErrorBoundary>
  );
}

function EcosystemErrorFallback({ error, resetError }) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="max-w-md w-full bg-white dark:bg-gray-800 shadow-lg rounded-lg p-6">
        <div className="flex items-center mb-4">
          <div className="flex-shrink-0">
            <svg className="h-8 w-8 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.96-.833-2.73 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
            </svg>
          </div>
          <div className="ml-3">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white">
              Something went wrong
            </h3>
          </div>
        </div>
        
        <div className="mb-4">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            {error.message}
          </p>
        </div>
        
        <div className="flex space-x-3">
          <button
            onClick={resetError}
            className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
          >
            Try again
          </button>
          
          <button
            onClick={() => window.location.reload()}
            className="flex-1 bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700 transition-colors"
          >
            Reload page
          </button>
        </div>
      </div>
    </div>
  );
}

// Main integration example
function EcosystemIntegration() {
  const { theme, setTheme, getStyles } = useUnifiedStyling();
  const metrics = usePerformanceMonitoring();
  
  // Unified data fetching
  const { data: users, loading: usersLoading } = useUnifiedData('/api/users', {
    strategy: 'react-query',
    background: true
  });
  
  const { data: notifications } = useUnifiedData('/api/notifications', {
    strategy: 'swr',
    realtime: true
  });
  
  // Multi-strategy form
  const userForm = useMultiStrategyForm(userSchema, {
    strategy: 'react-hook-form',
    validation: 'zod',
    optimistic: true,
    cacheKey: '/api/users',
    onSubmit: async (data) => {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      return response.json();
    }
  });
  
  return (
    <EcosystemErrorBoundary>
      <div className={getStyles('container')}>
        <header className="mb-8">
          <h1 className="text-3xl font-bold mb-4">
            React Ecosystem Integration
          </h1>
          
          <div className="flex items-center gap-4">
            <button
              onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}
              className={getStyles('button')}
            >
              Toggle Theme ({theme})
            </button>
            
            {notifications && (
              <div className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm">
                {notifications.length} notifications
              </div>
            )}
          </div>
        </header>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Users List */}
          <div className={getStyles('card')}>
            <h2 className="text-xl font-semibold mb-4">Users</h2>
            
            {usersLoading ? (
              <div>Loading users...</div>
            ) : (
              <div className="space-y-2">
                {users?.map(user => (
                  <div key={user.id} className="p-3 border rounded">
                    <div className="font-medium">{user.name}</div>
                    <div className="text-sm text-gray-500">{user.email}</div>
                  </div>
                ))}
              </div>
            )}
          </div>
          
          {/* Create User Form */}
          <div className={getStyles('card')}>
            <h2 className="text-xl font-semibold mb-4">Create User</h2>
            
            <form onSubmit={userForm.handleSubmit}>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Name</label>
                  <input
                    {...userForm.register('name')}
                    className="w-full p-2 border rounded"
                    placeholder="Enter name"
                  />
                  {userForm.formState.errors.name && (
                    <div className="text-red-500 text-sm mt-1">
                      {userForm.formState.errors.name.message}
                    </div>
                  )}
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">Email</label>
                  <input
                    {...userForm.register('email')}
                    type="email"
                    className="w-full p-2 border rounded"
                    placeholder="Enter email"
                  />
                  {userForm.formState.errors.email && (
                    <div className="text-red-500 text-sm mt-1">
                      {userForm.formState.errors.email.message}
                    </div>
                  )}
                </div>
                
                <button
                  type="submit"
                  disabled={userForm.formState.isSubmitting}
                  className={getStyles('button')}
                >
                  {userForm.formState.isSubmitting ? 'Creating...' : 'Create User'}
                </button>
              </div>
            </form>
          </div>
        </div>
        
        {/* Performance Metrics */}
        <div className={`${getStyles('card')} mt-8`}>
          <h2 className="text-xl font-semibold mb-4">Performance Metrics</h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div>
              <div className="text-2xl font-bold text-blue-600">
                {metrics.reactQuery?.totalQueries || 0}
              </div>
              <div className="text-sm text-gray-500">Total Queries</div>
            </div>
            
            <div>
              <div className="text-2xl font-bold text-green-600">
                {metrics.reactQuery?.staleQueries || 0}
              </div>
              <div className="text-sm text-gray-500">Stale Queries</div>
            </div>
            
            <div>
              <div className="text-2xl font-bold text-yellow-600">
                {metrics.reactQuery?.fetchingQueries || 0}
              </div>
              <div className="text-sm text-gray-500">Fetching</div>
            </div>
            
            <div>
              <div className="text-2xl font-bold text-red-600">
                {metrics.reactQuery?.errorQueries || 0}
              </div>
              <div className="text-sm text-gray-500">Errors</div>
            </div>
          </div>
        </div>
      </div>
    </EcosystemErrorBoundary>
  );
}

export { 
  EcosystemArchitecture,
  useUnifiedData,
  useMultiStrategyForm,
  useUnifiedStyling,
  usePerformanceMonitoring,
  EcosystemErrorBoundary,
  EcosystemIntegration
};
```

## 🎓 Interview Questions & Real-World Scenarios

### 🎯 Senior-Level Interview Questions

```jsx
// Interview scenarios and solutions
const interviewScenarios = {
  
  // Scenario 1: Large-scale form optimization
  largeFormOptimization: {
    question: `You have a form with 100+ fields that's causing performance issues. 
    How would you optimize it using React ecosystem tools?`,
    
    solution: `
    1. **Field-level Registration**: Use React Hook Form's field-level registration
       to prevent unnecessary re-renders
    
    2. **Virtual Scrolling**: Implement react-window for large field lists
    
    3. **Lazy Validation**: Use async validation with debouncing
    
    4. **Field Arrays Optimization**: Use useFieldArray for dynamic sections
    
    5. **Schema Splitting**: Break validation schemas into sections
    `,
    
    implementation: `
    // Optimized large form approach
    const useLargeFormOptimization = () => {
      const form = useForm({
        mode: 'onBlur', // Validate only on blur
        reValidateMode: 'onChange'
      });
      
      // Virtualize large field lists
      const VirtualizedFields = ({ fields }) => (
        <FixedSizeList height={400} itemCount={fields.length} itemSize={50}>
          {({ index, style }) => (
            <div style={style}>
              <Controller
                name={\`fields[\${index}].value\`}
                control={form.control}
                render={({ field }) => <input {...field} />}
              />
            </div>
          )}
        </FixedSizeList>
      );
      
      // Debounced validation
      const debouncedValidate = useMemo(
        () => debounce(form.trigger, 300),
        [form.trigger]
      );
      
      return { form, VirtualizedFields, debouncedValidate };
    };
    `
  },
  
  // Scenario 2: Data fetching strategy selection
  dataFetchingStrategy: {
    question: `When would you choose React Query vs SWR vs native fetch? 
    Provide specific use cases and trade-offs.`,
    
    solution: `
    **React Query**: 
    - Complex apps with heavy data requirements
    - Need advanced caching, background updates, optimistic updates
    - Offline support and retry logic
    - DevTools integration
    
    **SWR**:
    - Real-time applications
    - Simple caching needs
    - Smaller bundle size priority
    - Focus on data freshness
    
    **Native Fetch**:
    - One-off requests
    - Full control over caching
    - Minimal overhead
    - Custom retry logic
    `,
    
    implementation: `
    // Strategic data fetching decisions
    const useDataStrategy = (type, options) => {
      switch (type) {
        case 'critical':
          // Use native fetch for critical, one-time operations
          return useFetch(options.url, { 
            retries: 5, 
            timeout: 30000 
          });
          
        case 'realtime':
          // Use SWR for real-time data
          return useSWR(options.key, options.fetcher, {
            refreshInterval: 1000,
            revalidateOnFocus: true
          });
          
        case 'complex':
          // Use React Query for complex data management
          return useQuery({
            queryKey: options.key,
            queryFn: options.fetcher,
            staleTime: 5 * 60 * 1000,
            cacheTime: 10 * 60 * 1000,
            retry: 3
          });
          
        default:
          return useSWR(options.key, options.fetcher);
      }
    };
    `
  },
  
  // Scenario 3: Styling architecture decisions
  stylingArchitecture: {
    question: `Design a styling architecture for a large team with varying skill levels. 
    How would you combine CSS Modules, Styled Components, and Tailwind?`,
    
    solution: `
    **Layered Approach**:
    1. **Design System**: Tailwind for consistent spacing, colors, typography
    2. **Component Library**: Styled Components for reusable components
    3. **Page-specific**: CSS Modules for complex layouts
    4. **Utilities**: Tailwind utilities for quick styling
    
    **Team Guidelines**:
    - Junior developers: Use design system components + Tailwind utilities
    - Mid-level: Create CSS Modules for complex features
    - Senior: Build Styled Components for the design system
    `,
    
    implementation: `
    // Hybrid styling architecture
    const StylingArchitecture = {
      // Design system (Styled Components)
      DesignSystem: {
        Button: styled.button\`
          // Base styles from design system
        \`,
        Card: styled.div\`
          // Consistent card component
        \`
      },
      
      // Layout components (CSS Modules)
      Layout: {
        Dashboard: ({ children }) => (
          <div className={styles.dashboard}>
            <aside className={styles.sidebar}>
              {/* Sidebar content */}
            </aside>
            <main className={styles.content}>
              {children}
            </main>
          </div>
        )
      },
      
      // Utility combinations (Tailwind)
      Utilities: {
        cardWithHover: 'bg-white shadow-md hover:shadow-lg transition-shadow duration-200',
        centeredContent: 'flex items-center justify-center min-h-screen'
      }
    };
    `
  },
  
  // Scenario 4: Form library integration
  formIntegration: {
    question: `You need to migrate from Formik to React Hook Form in a large codebase. 
    How would you approach this migration?`,
    
    solution: `
    **Phased Migration Approach**:
    
    1. **Create Adapter Layer**: Build compatibility layer
    2. **Gradual Migration**: Migrate form by form
    3. **Shared Validation**: Keep validation schemas consistent
    4. **Testing Strategy**: Ensure no regression
    5. **Team Training**: Educate team on new patterns
    `,
    
    implementation: `
    // Migration adapter pattern
    const FormMigrationAdapter = {
      // Formik-like API using React Hook Form
      useFormikStyle: (initialValues, validationSchema, onSubmit) => {
        const form = useForm({
          defaultValues: initialValues,
          resolver: yupResolver(validationSchema)
        });
        
        // Formik-like interface
        return {
          values: form.watch(),
          errors: form.formState.errors,
          touched: form.formState.touchedFields,
          handleSubmit: form.handleSubmit(onSubmit),
          handleChange: (name) => (e) => {
            form.setValue(name, e.target.value);
          },
          setFieldValue: form.setValue,
          resetForm: form.reset
        };
      },
      
      // Migration utility
      migrateFormikComponent: (FormikComponent) => {
        return (props) => {
          const formikApi = FormMigrationAdapter.useFormikStyle(
            props.initialValues,
            props.validationSchema,
            props.onSubmit
          );
          
          return <FormikComponent {...formikApi} />;
        };
      }
    };
    `
  },
  
  // Scenario 5: Performance optimization
  performanceOptimization: {
    question: `Your React app is slow due to over-fetching and unnecessary re-renders. 
    How would you diagnose and fix these issues?`,
    
    solution: `
    **Diagnosis Tools**:
    1. React DevTools Profiler
    2. Network tab analysis
    3. React Query DevTools
    4. Bundle analyzer
    
    **Solutions**:
    1. **Data Fetching**: Implement pagination, infinite scroll
    2. **Caching**: Aggressive caching with React Query
    3. **Code Splitting**: Route-based and component-based
    4. **Memoization**: React.memo, useMemo, useCallback
    5. **Virtualization**: For large lists
    `,
    
    implementation: `
    // Performance optimization patterns
    const PerformanceOptimizations = {
      // Memoized components
      OptimizedUserList: React.memo(({ users, onUserClick }) => {
        return (
          <VirtualizedList
            items={users}
            renderItem={({ item, index }) => (
              <UserCard 
                key={item.id}
                user={item}
                onClick={onUserClick}
              />
            )}
          />
        );
      }),
      
      // Optimized data fetching
      useOptimizedUserData: (page, filters) => {
        // Cache with React Query
        const { data, fetchNextPage, hasNextPage } = useInfiniteQuery({
          queryKey: ['users', filters],
          queryFn: ({ pageParam = 1 }) => 
            fetchUsers({ page: pageParam, ...filters }),
          getNextPageParam: (lastPage) => lastPage.nextPage,
          staleTime: 5 * 60 * 1000,
          select: (data) => ({
            users: data.pages.flatMap(page => page.users),
            totalCount: data.pages[0]?.totalCount
          })
        });
        
        return { data, fetchNextPage, hasNextPage };
      },
      
      // Debounced search
      useOptimizedSearch: (query) => {
        const debouncedQuery = useDebounce(query, 300);
        
        return useQuery({
          queryKey: ['search', debouncedQuery],
          queryFn: () => searchUsers(debouncedQuery),
          enabled: debouncedQuery.length >= 2,
          staleTime: 30 * 1000
        });
      }
    };
    `
  }
};

// Advanced integration patterns
const advancedPatterns = {
  // Pattern 1: Micro-frontend integration
  microfrontendIntegration: `
  // Container app routing
  const MicrofrontendRouter = () => {
    return (
      <Router>
        <Routes>
          <Route path="/users/*" element={
            <Suspense fallback={<Loading />}>
              <UserMicrofrontend />
            </Suspense>
          } />
          <Route path="/products/*" element={
            <Suspense fallback={<Loading />}>
              <ProductMicrofrontend />
            </Suspense>
          } />
        </Routes>
      </Router>
    );
  };
  
  // Shared state between microfrontends
  const useSharedState = () => {
    const [state, setState] = useState(() => 
      JSON.parse(sessionStorage.getItem('sharedState') || '{}')
    );
    
    useEffect(() => {
      sessionStorage.setItem('sharedState', JSON.stringify(state));
      
      // Notify other microfrontends
      window.dispatchEvent(new CustomEvent('sharedStateUpdate', {
        detail: state
      }));
    }, [state]);
    
    return [state, setState];
  };
  `,
  
  // Pattern 2: Progressive enhancement
  progressiveEnhancement: `
  // Progressive form enhancement
  const ProgressiveForm = ({ children, fallback }) => {
    const [isEnhanced, setIsEnhanced] = useState(false);
    
    useEffect(() => {
      // Check for JavaScript capabilities
      const supportsAdvancedFeatures = 
        'IntersectionObserver' in window &&
        'requestIdleCallback' in window;
        
      setIsEnhanced(supportsAdvancedFeatures);
    }, []);
    
    if (!isEnhanced) {
      return fallback || <BasicForm />;
    }
    
    return children;
  };
  
  // Usage
  <ProgressiveForm fallback={<BasicHTMLForm />}>
    <AdvancedReactForm />
  </ProgressiveForm>
  `,
  
  // Pattern 3: Error recovery strategies
  errorRecoveryStrategies: `
  // Comprehensive error recovery
  const useErrorRecovery = () => {
    const queryClient = useQueryClient();
    const { mutate } = useSWRConfig();
    
    const recoverFromError = async (errorType, context) => {
      switch (errorType) {
        case 'network':
          // Retry failed queries
          await queryClient.refetchQueries({
            type: 'active',
            stale: true
          });
          break;
          
        case 'auth':
          // Clear auth-related cache
          queryClient.removeQueries({ 
            predicate: (query) => 
              query.queryKey[0]?.toString().includes('auth')
          });
          break;
          
        case 'stale-data':
          // Force revalidation
          mutate(() => true);
          break;
      }
    };
    
    return { recoverFromError };
  };
  `
};

export { interviewScenarios, advancedPatterns };
```

## 🎯 Summary & Trade-offs

### React Ecosystem Tool Selection Guide

| Aspect | React Router | React Hook Form | React Query | Tailwind CSS |
|--------|-------------|-----------------|-------------|--------------|
| **Learning Curve** | Medium | Medium-High | High | Low-Medium |
| **Performance** | Excellent | Excellent | Excellent | Excellent |
| **Bundle Size** | Small | Small | Medium | Small* |
| **TypeScript** | Excellent | Excellent | Excellent | Good |
| **Community** | Huge | Growing | Growing | Huge |
| **Best For** | All routing needs | Performance-critical forms | Complex data fetching | Rapid development |

### Key Decision Points

**Choose React Hook Form when:**

- Performance is critical
- Forms have many fields
- You need fine-grained control
- TypeScript is important

**Choose React Query when:**

- Complex data requirements
- Need caching and background updates
- Offline support needed
- Advanced features required

**Choose Tailwind when:**

- Rapid prototyping
- Design system consistency
- Team has varying CSS skills
- Utility-first approach preferred

**Choose CSS Modules when:**

- Component-scoped styles needed
- Existing CSS codebase
- Gradual migration strategy
- Build-time optimization important

This comprehensive guide covers the essential React ecosystem tools with real-world examples, performance considerations, and interview-focused scenarios. The patterns and practices shown here represent current industry standards for building scalable React applications.


Let me continue with the remaining sections of the React Ecosystem guide:
