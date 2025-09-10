# 🏗️ System Design & Architecture in React

> **For tough rounds & senior roles: Deep dive into scalable React architecture, project structure, code splitting, micro-frontends, SSR/SSG, i18n, feature flags, and analytics.**

---

## 1. 📁 Project Structure Best Practices

### Principles
- **Scalability:** Organize for growth, not just current needs
- **Separation of Concerns:** Group by feature/domain, not by type
- **Encapsulation:** Limit cross-feature dependencies
- **Discoverability:** Easy for new devs to find and understand code

### Example Structure (Feature-Based)
```
src/
  app/                # App-level config, providers, routing
  features/
    auth/
      components/
      hooks/
      services/
      types.ts
      index.ts
    dashboard/
      components/
      hooks/
      services/
      types.ts
      index.ts
  shared/
    components/
    hooks/
    utils/
    types/
  assets/
  locales/
  styles/
  config/
```

### Tips
- Use **barrel files** (`index.ts`) for exports
- Keep **feature boundaries** strict
- Shared code goes in `shared/`
- Avoid deep nesting (>3 levels)
- Document folder purpose with README.md

---

## 2. ⚡ Code Splitting Strategy

### Why?
- Reduce initial bundle size
- Improve load times for large apps

### How?
- **React.lazy** + **Suspense** for component-level splitting
- **Dynamic imports** for routes/features
- **Webpack SplitChunks** for vendor/code separation

### Example: Route-Based Splitting
```jsx
// src/app/AppRouter.jsx
import { Suspense, lazy } from 'react';
const Dashboard = lazy(() => import('../features/dashboard'));
const Auth = lazy(() => import('../features/auth'));

<Suspense fallback={<Loading />}>
  <Routes>
    <Route path="/dashboard" element={<Dashboard />} />
    <Route path="/auth/*" element={<Auth />} />
  </Routes>
</Suspense>
```

### Advanced
- **Preloading**: Use `import(/* webpackPrefetch: true */)`
- **Chunk naming**: `import(/* webpackChunkName: "dashboard" */)`
- **Split by feature, not just route**

---

## 3. 🧩 Micro-Frontends

### Approaches
- **Module Federation (Webpack 5):** Share code at runtime between apps
- **iframe-based:** Isolate apps, communicate via postMessage
- **single-spa:** Orchestrate multiple frameworks/apps in one shell

### Module Federation Example
```js
// webpack.config.js
module.exports = {
  plugins: [
    new ModuleFederationPlugin({
      name: 'dashboard',
      filename: 'remoteEntry.js',
      exposes: {
        './Widget': './src/features/dashboard/Widget',
      },
      remotes: {
        auth: 'auth@http://localhost:3001/remoteEntry.js',
      },
      shared: ['react', 'react-dom'],
    }),
  ],
};
```

### iframe-based Example
```jsx
// src/features/analytics/AnalyticsIframe.js
<iframe src="https://analytics.company.com" title="Analytics" />
// Use window.postMessage for communication
```

### single-spa Example
```js
// root-config.js
registerApplication({
  name: 'auth',
  app: () => System.import('auth'),
  activeWhen: ['/auth'],
});
registerApplication({
  name: 'dashboard',
  app: () => System.import('dashboard'),
  activeWhen: ['/dashboard'],
});
start();
```

### Considerations
- **Shared state**: Use events, custom hooks, or shared stores
- **Versioning**: Align dependencies, handle breaking changes
- **Deployment**: Independent CI/CD pipelines

---

## 4. 🏢 Designing Large-Scale React Apps

### Key Concerns
- **Permissions/RBAC**: Role-based access control at route/component level
- **Feature Flags**: Enable/disable features dynamically
- **Localization (i18n)**: Support multiple languages
- **Analytics**: Track user behavior, errors, performance

### Example: Permissions
```jsx
// src/shared/hooks/usePermission.js
export function usePermission(requiredRole) {
  const { user } = useAuth();
  return user?.roles.includes(requiredRole);
}

// Usage
if (!usePermission('admin')) return <NoAccess />;
```

### Example: Feature Flags
```jsx
// src/shared/hooks/useFeatureFlag.js
export function useFeatureFlag(flag) {
  const flags = useContext(FeatureFlagContext);
  return flags[flag];
}

// Usage
if (useFeatureFlag('newDashboard')) {
  return <NewDashboard />;
}
```

### Example: Localization
```jsx
// src/app/i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
i18n.use(initReactI18next).init({
  resources: { en: { translation: { welcome: 'Welcome' } }, fr: { translation: { welcome: 'Bienvenue' } } },
  lng: 'en',
  fallbackLng: 'en',
});

// Usage
import { useTranslation } from 'react-i18next';
const { t } = useTranslation();
return <h1>{t('welcome')}</h1>;
```

### Example: Analytics
```js
// src/shared/utils/analytics.js
export function trackEvent(event, data) {
  window.analytics?.track(event, data);
}

// Usage
trackEvent('login', { userId });
```

---

## 5. ⚡ SSR / SSG with Next.js

### Why?
- SEO, performance, initial load speed

### SSR Example
```js
// pages/dashboard.js
export async function getServerSideProps() {
  const data = await fetchDashboardData();
  return { props: { data } };
}

export default function Dashboard({ data }) {
  // ...
}
```

### SSG Example
```js
// pages/blog/[id].js
export async function getStaticPaths() {
  const posts = await fetchPosts();
  return { paths: posts.map(p => ({ params: { id: p.id } })), fallback: false };
}

export async function getStaticProps({ params }) {
  const post = await fetchPost(params.id);
  return { props: { post } };
}

export default function BlogPost({ post }) {
  // ...
}
```

### Next.js Features
- API routes
- Middleware
- Image optimization
- Internationalization

---

## 6. 🌍 i18n with react-i18next

### Setup
```js
// src/app/i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
i18n.use(initReactI18next).init({
  resources: {
    en: { translation: { welcome: 'Welcome' } },
    fr: { translation: { welcome: 'Bienvenue' } },
  },
  lng: 'en',
  fallbackLng: 'en',
});
```

### Usage
```jsx
import { useTranslation } from 'react-i18next';
const { t } = useTranslation();
return <h1>{t('welcome')}</h1>;
```

### Advanced
- Pluralization, interpolation
- Language detection
- Namespaces for large apps

---

## 7. 🚩 Feature Flagging

### LaunchDarkly Example
```js
// src/app/featureFlags.js
import { LDClient } from 'launchdarkly-js-client-sdk';
const ldClient = LDClient.initialize('YOUR_CLIENT_KEY', { key: userId });
ldClient.on('ready', () => {
  const showNewDashboard = ldClient.variation('new-dashboard', false);
  // Use flag in app
});
```

### Homemade Solution Example
```js
// src/shared/context/FeatureFlagContext.js
const FeatureFlagContext = createContext({});
export function FeatureFlagProvider({ children, flags }) {
  return (
    <FeatureFlagContext.Provider value={flags}>
      {children}
    </FeatureFlagContext.Provider>
  );
}

// Usage
const flags = { newDashboard: true, betaFeature: false };
<FeatureFlagProvider flags={flags}>
  <App />
</FeatureFlagProvider>
```

---

## 8. 📝 Interview Tips & Senior Insights

- **Explain trade-offs:** SSR vs SSG, micro-frontends vs monolith, code splitting granularity
- **Show real-world experience:** Discuss migration, scaling, team onboarding
- **Mention monitoring/analytics:** Error tracking, performance, user flows
- **Highlight security:** Permissions, data privacy, XSS/CSRF
- **Demonstrate leadership:** Code reviews, documentation, mentoring

---

> **Senior system design is about balancing scalability, maintainability, and developer experience. Every decision should be justified by business and technical needs.**

---

*Iterate for more details or deep dives on any section!*
