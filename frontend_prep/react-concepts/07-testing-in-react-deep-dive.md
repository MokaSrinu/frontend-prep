# 🧪 React Testing Deep-Dive: Complete Testing Strategy

## 📋 Table of Contents

1. [Unit Testing with Jest & React Testing Library](#unit-testing-with-jest--react-testing-library)
2. [Integration Testing Strategies](#integration-testing-strategies)
3. [End-to-End Testing](#end-to-end-testing)
4. [Advanced Testing Patterns](#advanced-testing-patterns)
5. [Testing Best Practices & Interview Questions](#testing-best-practices--interview-questions)

---

## 🎯 Unit Testing with Jest & React Testing Library

### 📚 Fundamentals & Setup

**Interview Critical Point:** Understanding the difference between testing implementation details vs. user behavior.

```jsx
// jest.config.js
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.js'],
  moduleNameMapping: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
    '\\.(jpg|jpeg|png|gif|svg)$': '<rootDir>/src/__mocks__/fileMock.js'
  },
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.js',
    '!src/reportWebVitals.js'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{js,jsx,ts,tsx}',
    '<rootDir>/src/**/*.{spec,test}.{js,jsx,ts,tsx}'
  ],
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': 'babel-jest'
  },
  transformIgnorePatterns: [
    'node_modules/(?!(axios|some-es6-module)/)'
  ]
};
```

```jsx
// src/setupTests.js
import '@testing-library/jest-dom';
import { configure } from '@testing-library/react';
import { server } from './mocks/server';

// Configure React Testing Library
configure({ 
  testIdAttribute: 'data-testid',
  asyncUtilTimeout: 2000 
});

// Mock IntersectionObserver
global.IntersectionObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn()
}));

// Mock ResizeObserver
global.ResizeObserver = jest.fn().mockImplementation(() => ({
  observe: jest.fn(),
  unobserve: jest.fn(),
  disconnect: jest.fn()
}));

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: jest.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  })),
});

// Setup MSW
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

// Global test helpers
global.renderWithProviders = (ui, options = {}) => {
  // Will be defined later
};
```

### 🎯 Component Testing Fundamentals

**Interview Critical Point:** Testing user interactions and behavior, not implementation details.

```jsx
// components/Button/Button.jsx
import React from 'react';
import PropTypes from 'prop-types';
import './Button.css';

const Button = ({ 
  children, 
  variant = 'primary', 
  size = 'medium',
  disabled = false,
  loading = false,
  onClick,
  type = 'button',
  'data-testid': testId,
  ...props 
}) => {
  const handleClick = (e) => {
    if (disabled || loading) return;
    onClick?.(e);
  };

  const classes = [
    'btn',
    `btn--${variant}`,
    `btn--${size}`,
    disabled && 'btn--disabled',
    loading && 'btn--loading'
  ].filter(Boolean).join(' ');

  return (
    <button
      type={type}
      className={classes}
      onClick={handleClick}
      disabled={disabled}
      data-testid={testId}
      aria-label={loading ? 'Loading...' : undefined}
      {...props}
    >
      {loading && (
        <span className="btn__spinner" role="status" aria-hidden="true">
          <span className="sr-only">Loading...</span>
        </span>
      )}
      <span className={loading ? 'btn__text--hidden' : 'btn__text'}>
        {children}
      </span>
    </button>
  );
};

Button.propTypes = {
  children: PropTypes.node.isRequired,
  variant: PropTypes.oneOf(['primary', 'secondary', 'danger', 'ghost']),
  size: PropTypes.oneOf(['small', 'medium', 'large']),
  disabled: PropTypes.bool,
  loading: PropTypes.bool,
  onClick: PropTypes.func,
  type: PropTypes.oneOf(['button', 'submit', 'reset'])
};

export default Button;
```

```jsx
// components/Button/__tests__/Button.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Button from '../Button';

describe('Button Component', () => {
  // Basic rendering tests
  describe('Rendering', () => {
    it('renders with correct text', () => {
      render(<Button>Click me</Button>);
      
      expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument();
    });

    it('applies correct variant classes', () => {
      const { rerender } = render(<Button variant="primary">Primary</Button>);
      
      expect(screen.getByRole('button')).toHaveClass('btn--primary');
      
      rerender(<Button variant="secondary">Secondary</Button>);
      expect(screen.getByRole('button')).toHaveClass('btn--secondary');
    });

    it('applies correct size classes', () => {
      const { rerender } = render(<Button size="small">Small</Button>);
      
      expect(screen.getByRole('button')).toHaveClass('btn--small');
      
      rerender(<Button size="large">Large</Button>);
      expect(screen.getByRole('button')).toHaveClass('btn--large');
    });

    it('renders with custom test id', () => {
      render(<Button data-testid="custom-button">Test</Button>);
      
      expect(screen.getByTestId('custom-button')).toBeInTheDocument();
    });
  });

  // Interaction tests
  describe('Interactions', () => {
    it('calls onClick handler when clicked', async () => {
      const user = userEvent.setup();
      const handleClick = jest.fn();
      
      render(<Button onClick={handleClick}>Click me</Button>);
      
      await user.click(screen.getByRole('button'));
      
      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('does not call onClick when disabled', async () => {
      const user = userEvent.setup();
      const handleClick = jest.fn();
      
      render(
        <Button onClick={handleClick} disabled>
          Disabled Button
        </Button>
      );
      
      await user.click(screen.getByRole('button'));
      
      expect(handleClick).not.toHaveBeenCalled();
    });

    it('does not call onClick when loading', async () => {
      const user = userEvent.setup();
      const handleClick = jest.fn();
      
      render(
        <Button onClick={handleClick} loading>
          Loading Button
        </Button>
      );
      
      await user.click(screen.getByRole('button'));
      
      expect(handleClick).not.toHaveBeenCalled();
    });

    it('handles keyboard events correctly', async () => {
      const user = userEvent.setup();
      const handleClick = jest.fn();
      
      render(<Button onClick={handleClick}>Keyboard Test</Button>);
      
      const button = screen.getByRole('button');
      button.focus();
      
      await user.keyboard('{Enter}');
      expect(handleClick).toHaveBeenCalledTimes(1);
      
      await user.keyboard(' ');
      expect(handleClick).toHaveBeenCalledTimes(2);
    });
  });

  // State tests
  describe('States', () => {
    it('shows loading state correctly', () => {
      render(<Button loading>Loading Button</Button>);
      
      const button = screen.getByRole('button');
      
      expect(button).toHaveClass('btn--loading');
      expect(button).toHaveAttribute('aria-label', 'Loading...');
      expect(screen.getByRole('status')).toBeInTheDocument();
      expect(screen.getByText('Loading...')).toBeInTheDocument();
    });

    it('shows disabled state correctly', () => {
      render(<Button disabled>Disabled Button</Button>);
      
      const button = screen.getByRole('button');
      
      expect(button).toBeDisabled();
      expect(button).toHaveClass('btn--disabled');
    });

    it('handles multiple states correctly', () => {
      render(<Button disabled loading>Multi-state</Button>);
      
      const button = screen.getByRole('button');
      
      expect(button).toBeDisabled();
      expect(button).toHaveClass('btn--disabled', 'btn--loading');
    });
  });

  // Accessibility tests
  describe('Accessibility', () => {
    it('has correct button role', () => {
      render(<Button>Accessible Button</Button>);
      
      expect(screen.getByRole('button')).toBeInTheDocument();
    });

    it('supports custom aria attributes', () => {
      render(
        <Button aria-describedby="help-text" aria-expanded="false">
          Aria Button
        </Button>
      );
      
      const button = screen.getByRole('button');
      
      expect(button).toHaveAttribute('aria-describedby', 'help-text');
      expect(button).toHaveAttribute('aria-expanded', 'false');
    });

    it('provides proper loading announcement', () => {
      render(<Button loading>Submit</Button>);
      
      // Screen reader users should know the button is loading
      expect(screen.getByLabelText(/loading/i)).toBeInTheDocument();
      expect(screen.getByRole('status')).toBeInTheDocument();
    });
  });

  // Edge cases
  describe('Edge Cases', () => {
    it('handles missing onClick gracefully', async () => {
      const user = userEvent.setup();
      
      render(<Button>No Handler</Button>);
      
      // Should not throw error
      await user.click(screen.getByRole('button'));
      
      expect(screen.getByRole('button')).toBeInTheDocument();
    });

    it('handles rapid clicks correctly', async () => {
      const user = userEvent.setup();
      const handleClick = jest.fn();
      
      render(<Button onClick={handleClick}>Rapid Click</Button>);
      
      const button = screen.getByRole('button');
      
      // Simulate rapid clicking
      await user.click(button);
      await user.click(button);
      await user.click(button);
      
      expect(handleClick).toHaveBeenCalledTimes(3);
    });

    it('forwards ref correctly', () => {
      const ref = React.createRef();
      
      render(<Button ref={ref}>Ref Test</Button>);
      
      expect(ref.current).toBeInstanceOf(HTMLButtonElement);
    });
  });
});
```

### 🎯 Form Testing Strategies

**Interview Critical Point:** Testing form validation, submission, and user workflows.

```jsx
// components/ContactForm/ContactForm.jsx
import React from 'react';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import Button from '../Button/Button';

const contactSchema = z.object({
  name: z.string()
    .min(2, 'Name must be at least 2 characters')
    .max(50, 'Name must be less than 50 characters'),
  email: z.string()
    .email('Please enter a valid email address'),
  subject: z.string()
    .min(5, 'Subject must be at least 5 characters')
    .max(100, 'Subject must be less than 100 characters'),
  message: z.string()
    .min(10, 'Message must be at least 10 characters')
    .max(1000, 'Message must be less than 1000 characters'),
  agreeToTerms: z.boolean()
    .refine(val => val === true, 'You must agree to the terms')
});

const ContactForm = ({ onSubmit, initialValues = {} }) => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isValid },
    reset,
    watch
  } = useForm({
    resolver: zodResolver(contactSchema),
    defaultValues: {
      name: '',
      email: '',
      subject: '',
      message: '',
      agreeToTerms: false,
      ...initialValues
    },
    mode: 'onBlur'
  });

  const watchedMessage = watch('message');
  const remainingChars = 1000 - (watchedMessage?.length || 0);

  const handleFormSubmit = async (data) => {
    try {
      await onSubmit(data);
      reset();
    } catch (error) {
      console.error('Form submission failed:', error);
    }
  };

  return (
    <form 
      onSubmit={handleSubmit(handleFormSubmit)}
      noValidate
      data-testid="contact-form"
    >
      <div className="form-group">
        <label htmlFor="name">
          Name *
        </label>
        <input
          id="name"
          type="text"
          {...register('name')}
          aria-invalid={errors.name ? 'true' : 'false'}
          aria-describedby={errors.name ? 'name-error' : undefined}
        />
        {errors.name && (
          <div id="name-error" role="alert" className="error-message">
            {errors.name.message}
          </div>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="email">
          Email *
        </label>
        <input
          id="email"
          type="email"
          {...register('email')}
          aria-invalid={errors.email ? 'true' : 'false'}
          aria-describedby={errors.email ? 'email-error' : undefined}
        />
        {errors.email && (
          <div id="email-error" role="alert" className="error-message">
            {errors.email.message}
          </div>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="subject">
          Subject *
        </label>
        <input
          id="subject"
          type="text"
          {...register('subject')}
          aria-invalid={errors.subject ? 'true' : 'false'}
          aria-describedby={errors.subject ? 'subject-error' : undefined}
        />
        {errors.subject && (
          <div id="subject-error" role="alert" className="error-message">
            {errors.subject.message}
          </div>
        )}
      </div>

      <div className="form-group">
        <label htmlFor="message">
          Message *
        </label>
        <textarea
          id="message"
          rows={5}
          {...register('message')}
          aria-invalid={errors.message ? 'true' : 'false'}
          aria-describedby={`${errors.message ? 'message-error ' : ''}message-count`}
        />
        <div id="message-count" className="char-count">
          {remainingChars} characters remaining
        </div>
        {errors.message && (
          <div id="message-error" role="alert" className="error-message">
            {errors.message.message}
          </div>
        )}
      </div>

      <div className="form-group">
        <label className="checkbox-label">
          <input
            type="checkbox"
            {...register('agreeToTerms')}
            aria-invalid={errors.agreeToTerms ? 'true' : 'false'}
            aria-describedby={errors.agreeToTerms ? 'terms-error' : undefined}
          />
          I agree to the terms and conditions *
        </label>
        {errors.agreeToTerms && (
          <div id="terms-error" role="alert" className="error-message">
            {errors.agreeToTerms.message}
          </div>
        )}
      </div>

      <div className="form-actions">
        <Button
          type="submit"
          loading={isSubmitting}
          disabled={!isValid || isSubmitting}
        >
          Send Message
        </Button>
        
        <Button
          type="button"
          variant="secondary"
          onClick={() => reset()}
          disabled={isSubmitting}
        >
          Reset
        </Button>
      </div>
    </form>
  );
};

export default ContactForm;
```

```jsx
// components/ContactForm/__tests__/ContactForm.test.jsx
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import ContactForm from '../ContactForm';

describe('ContactForm', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  describe('Form Rendering', () => {
    it('renders all form fields', () => {
      render(<ContactForm onSubmit={mockOnSubmit} />);

      expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/subject/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/message/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/agree to the terms/i)).toBeInTheDocument();
    });

    it('renders submit and reset buttons', () => {
      render(<ContactForm onSubmit={mockOnSubmit} />);

      expect(screen.getByRole('button', { name: /send message/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /reset/i })).toBeInTheDocument();
    });

    it('populates initial values correctly', () => {
      const initialValues = {
        name: 'John Doe',
        email: 'john@example.com',
        subject: 'Test Subject',
        message: 'Test message content',
        agreeToTerms: true
      };

      render(<ContactForm onSubmit={mockOnSubmit} initialValues={initialValues} />);

      expect(screen.getByDisplayValue('John Doe')).toBeInTheDocument();
      expect(screen.getByDisplayValue('john@example.com')).toBeInTheDocument();
      expect(screen.getByDisplayValue('Test Subject')).toBeInTheDocument();
      expect(screen.getByDisplayValue('Test message content')).toBeInTheDocument();
      expect(screen.getByRole('checkbox')).toBeChecked();
    });
  });

  describe('Form Validation', () => {
    it('shows validation errors for empty required fields', async () => {
      const user = userEvent.setup();
      render(<ContactForm onSubmit={mockOnSubmit} />);

      // Try to submit empty form
      await user.click(screen.getByRole('button', { name: /send message/i }));

      await waitFor(() => {
        expect(screen.getByText(/name must be at least 2 characters/i)).toBeInTheDocument();
        expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument();
        expect(screen.getByText(/subject must be at least 5 characters/i)).toBeInTheDocument();
        expect(screen.getByText(/message must be at least 10 characters/i)).toBeInTheDocument();
        expect(screen.getByText(/you must agree to the terms/i)).toBeInTheDocument();
      });

      expect(mockOnSubmit).not.toHaveBeenCalled();
    });

    it('validates name field correctly', async () => {
      const user = userEvent.setup();
      render(<ContactForm onSubmit={mockOnSubmit} />);

      const nameInput = screen.getByLabelText(/name/i);

      // Test minimum length
      await user.type(nameInput, 'A');
      await user.tab(); // Trigger blur validation

      await waitFor(() => {
        expect(screen.getByText(/name must be at least 2 characters/i)).toBeInTheDocument();
      });

      // Test valid input
      await user.clear(nameInput);
      await user.type(nameInput, 'John Doe');
      await user.tab();

      await waitFor(() => {
        expect(screen.queryByText(/name must be at least 2 characters/i)).not.toBeInTheDocument();
      });
    });

    it('validates email field correctly', async () => {
      const user = userEvent.setup();
      render(<ContactForm onSubmit={mockOnSubmit} />);

      const emailInput = screen.getByLabelText(/email/i);

      // Test invalid email
      await user.type(emailInput, 'invalid-email');
      await user.tab();

      await waitFor(() => {
        expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument();
      });

      // Test valid email
      await user.clear(emailInput);
      await user.type(emailInput, 'test@example.com');
      await user.tab();

      await waitFor(() => {
        expect(screen.queryByText(/please enter a valid email address/i)).not.toBeInTheDocument();
      });
    });

    it('validates message field and shows character count', async () => {
      const user = userEvent.setup();
      render(<ContactForm onSubmit={mockOnSubmit} />);

      const messageInput = screen.getByLabelText(/message/i);

      // Test character counting
      await user.type(messageInput, 'Hello');
      expect(screen.getByText('995 characters remaining')).toBeInTheDocument();

      // Test minimum length validation
      await user.tab();

      await waitFor(() => {
        expect(screen.getByText(/message must be at least 10 characters/i)).toBeInTheDocument();
      });

      // Test valid message
      await user.type(messageInput, ' world! This is a valid message.');
      await user.tab();

      await waitFor(() => {
        expect(screen.queryByText(/message must be at least 10 characters/i)).not.toBeInTheDocument();
      });
    });
  });

  describe('Form Submission', () => {
    const validFormData = {
      name: 'John Doe',
      email: 'john@example.com',
      subject: 'Test Subject',
      message: 'This is a test message with enough characters.',
      agreeToTerms: true
    };

    it('submits form with valid data', async () => {
      const user = userEvent.setup();
      mockOnSubmit.mockResolvedValueOnce();

      render(<ContactForm onSubmit={mockOnSubmit} />);

      // Fill out form
      await user.type(screen.getByLabelText(/name/i), validFormData.name);
      await user.type(screen.getByLabelText(/email/i), validFormData.email);
      await user.type(screen.getByLabelText(/subject/i), validFormData.subject);
      await user.type(screen.getByLabelText(/message/i), validFormData.message);
      await user.click(screen.getByLabelText(/agree to the terms/i));

      // Submit form
      await user.click(screen.getByRole('button', { name: /send message/i }));

      await waitFor(() => {
        expect(mockOnSubmit).toHaveBeenCalledWith(validFormData);
      });
    });

    it('shows loading state during submission', async () => {
      const user = userEvent.setup();
      let resolveSubmit;
      mockOnSubmit.mockImplementation(() => new Promise(resolve => {
        resolveSubmit = resolve;
      }));

      render(<ContactForm onSubmit={mockOnSubmit} initialValues={validFormData} />);

      const submitButton = screen.getByRole('button', { name: /send message/i });
      
      await user.click(submitButton);

      // Button should show loading state
      expect(screen.getByRole('button', { name: /loading/i })).toBeInTheDocument();
      expect(submitButton).toBeDisabled();

      // Resolve the promise
      resolveSubmit();

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /send message/i })).toBeInTheDocument();
        expect(submitButton).not.toBeDisabled();
      });
    });

    it('resets form after successful submission', async () => {
      const user = userEvent.setup();
      mockOnSubmit.mockResolvedValueOnce();

      render(<ContactForm onSubmit={mockOnSubmit} />);

      // Fill out form
      await user.type(screen.getByLabelText(/name/i), validFormData.name);
      await user.type(screen.getByLabelText(/email/i), validFormData.email);
      await user.click(screen.getByLabelText(/agree to the terms/i));

      // Submit form
      await user.click(screen.getByRole('button', { name: /send message/i }));

      await waitFor(() => {
        expect(screen.getByLabelText(/name/i)).toHaveValue('');
        expect(screen.getByLabelText(/email/i)).toHaveValue('');
        expect(screen.getByLabelText(/agree to the terms/i)).not.toBeChecked();
      });
    });

    it('handles submission errors gracefully', async () => {
      const user = userEvent.setup();
      const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
      mockOnSubmit.mockRejectedValueOnce(new Error('Submission failed'));

      render(<ContactForm onSubmit={mockOnSubmit} initialValues={validFormData} />);

      await user.click(screen.getByRole('button', { name: /send message/i }));

      await waitFor(() => {
        expect(consoleError).toHaveBeenCalledWith(
          'Form submission failed:', 
          expect.any(Error)
        );
      });

      consoleError.mockRestore();
    });
  });

  describe('Form Reset', () => {
    it('resets form to initial state', async () => {
      const user = userEvent.setup();
      render(<ContactForm onSubmit={mockOnSubmit} />);

      // Fill out some fields
      await user.type(screen.getByLabelText(/name/i), 'Test Name');
      await user.type(screen.getByLabelText(/email/i), 'test@example.com');
      await user.click(screen.getByLabelText(/agree to the terms/i));

      // Reset form
      await user.click(screen.getByRole('button', { name: /reset/i }));

      // Check fields are empty
      expect(screen.getByLabelText(/name/i)).toHaveValue('');
      expect(screen.getByLabelText(/email/i)).toHaveValue('');
      expect(screen.getByLabelText(/agree to the terms/i)).not.toBeChecked();
    });

    it('resets form to initial values when provided', async () => {
      const user = userEvent.setup();
      const initialValues = {
        name: 'Initial Name',
        email: 'initial@example.com'
      };

      render(<ContactForm onSubmit={mockOnSubmit} initialValues={initialValues} />);

      // Change some values
      await user.clear(screen.getByLabelText(/name/i));
      await user.type(screen.getByLabelText(/name/i), 'Changed Name');

      // Reset form
      await user.click(screen.getByRole('button', { name: /reset/i }));

      // Should reset to initial values
      expect(screen.getByLabelText(/name/i)).toHaveValue('Initial Name');
      expect(screen.getByLabelText(/email/i)).toHaveValue('initial@example.com');
    });
  });

  describe('Accessibility', () => {
    it('associates labels with inputs correctly', () => {
      render(<ContactForm onSubmit={mockOnSubmit} />);

      const nameInput = screen.getByLabelText(/name/i);
      const emailInput = screen.getByLabelText(/email/i);
      const subjectInput = screen.getByLabelText(/subject/i);
      const messageInput = screen.getByLabelText(/message/i);

      expect(nameInput).toHaveAttribute('id', 'name');
      expect(emailInput).toHaveAttribute('id', 'email');
      expect(subjectInput).toHaveAttribute('id', 'subject');
      expect(messageInput).toHaveAttribute('id', 'message');
    });

    it('provides proper ARIA attributes for validation errors', async () => {
      const user = userEvent.setup();
      render(<ContactForm onSubmit={mockOnSubmit} />);

      const nameInput = screen.getByLabelText(/name/i);
      
      // Trigger validation error
      await user.type(nameInput, 'A');
      await user.tab();

      await waitFor(() => {
        expect(nameInput).toHaveAttribute('aria-invalid', 'true');
        expect(nameInput).toHaveAttribute('aria-describedby', 'name-error');
        
        const errorMessage = screen.getByText(/name must be at least 2 characters/i);
        expect(errorMessage).toHaveAttribute('role', 'alert');
        expect(errorMessage).toHaveAttribute('id', 'name-error');
      });
    });

    it('provides character count information for screen readers', () => {
      render(<ContactForm onSubmit={mockOnSubmit} />);

      const messageInput = screen.getByLabelText(/message/i);
      expect(messageInput).toHaveAttribute('aria-describedby', 'message-count');
      
      const charCount = screen.getByText(/characters remaining/i);
      expect(charCount).toHaveAttribute('id', 'message-count');
    });
  });
});
```

### 🎯 Hook Testing Strategies

**Interview Critical Point:** Testing custom hooks in isolation and with realistic scenarios.

```jsx
// hooks/useCounter.js
import { useState, useCallback } from 'react';

export const useCounter = (initialValue = 0, options = {}) => {
  const { min, max, step = 1 } = options;
  const [count, setCount] = useState(initialValue);

  const increment = useCallback(() => {
    setCount(prevCount => {
      const newValue = prevCount + step;
      return max !== undefined ? Math.min(newValue, max) : newValue;
    });
  }, [step, max]);

  const decrement = useCallback(() => {
    setCount(prevCount => {
      const newValue = prevCount - step;
      return min !== undefined ? Math.max(newValue, min) : newValue;
    });
  }, [step, min]);

  const reset = useCallback(() => {
    setCount(initialValue);
  }, [initialValue]);

  const setValue = useCallback((value) => {
    if (typeof value === 'function') {
      setCount(prevCount => {
        const newValue = value(prevCount);
        if (min !== undefined && newValue < min) return min;
        if (max !== undefined && newValue > max) return max;
        return newValue;
      });
    } else {
      if (min !== undefined && value < min) {
        setCount(min);
      } else if (max !== undefined && value > max) {
        setCount(max);
      } else {
        setCount(value);
      }
    }
  }, [min, max]);

  return {
    count,
    increment,
    decrement,
    reset,
    setValue
  };
};
```

```jsx
// hooks/__tests__/useCounter.test.js
import { renderHook, act } from '@testing-library/react';
import { useCounter } from '../useCounter';

describe('useCounter hook', () => {
  describe('Initial State', () => {
    it('initializes with default value of 0', () => {
      const { result } = renderHook(() => useCounter());
      
      expect(result.current.count).toBe(0);
    });

    it('initializes with custom initial value', () => {
      const { result } = renderHook(() => useCounter(5));
      
      expect(result.current.count).toBe(5);
    });

    it('provides all expected methods', () => {
      const { result } = renderHook(() => useCounter());
      
      expect(result.current).toEqual({
        count: expect.any(Number),
        increment: expect.any(Function),
        decrement: expect.any(Function),
        reset: expect.any(Function),
        setValue: expect.any(Function)
      });
    });
  });

  describe('Basic Operations', () => {
    it('increments count by 1', () => {
      const { result } = renderHook(() => useCounter(0));
      
      act(() => {
        result.current.increment();
      });
      
      expect(result.current.count).toBe(1);
    });

    it('decrements count by 1', () => {
      const { result } = renderHook(() => useCounter(5));
      
      act(() => {
        result.current.decrement();
      });
      
      expect(result.current.count).toBe(4);
    });

    it('resets to initial value', () => {
      const { result } = renderHook(() => useCounter(10));
      
      // Change the value
      act(() => {
        result.current.increment();
        result.current.increment();
      });
      
      expect(result.current.count).toBe(12);
      
      // Reset
      act(() => {
        result.current.reset();
      });
      
      expect(result.current.count).toBe(10);
    });

    it('sets specific value', () => {
      const { result } = renderHook(() => useCounter());
      
      act(() => {
        result.current.setValue(42);
      });
      
      expect(result.current.count).toBe(42);
    });

    it('sets value using function', () => {
      const { result } = renderHook(() => useCounter(10));
      
      act(() => {
        result.current.setValue(prev => prev * 2);
      });
      
      expect(result.current.count).toBe(20);
    });
  });

  describe('Step Configuration', () => {
    it('increments by custom step', () => {
      const { result } = renderHook(() => useCounter(0, { step: 5 }));
      
      act(() => {
        result.current.increment();
      });
      
      expect(result.current.count).toBe(5);
    });

    it('decrements by custom step', () => {
      const { result } = renderHook(() => useCounter(10, { step: 3 }));
      
      act(() => {
        result.current.decrement();
      });
      
      expect(result.current.count).toBe(7);
    });
  });

  describe('Boundary Constraints', () => {
    it('respects maximum boundary on increment', () => {
      const { result } = renderHook(() => useCounter(8, { max: 10 }));
      
      act(() => {
        result.current.increment(); // 9
        result.current.increment(); // 10
        result.current.increment(); // Should stay 10
      });
      
      expect(result.current.count).toBe(10);
    });

    it('respects minimum boundary on decrement', () => {
      const { result } = renderHook(() => useCounter(2, { min: 0 }));
      
      act(() => {
        result.current.decrement(); // 1
        result.current.decrement(); // 0
        result.current.decrement(); // Should stay 0
      });
      
      expect(result.current.count).toBe(0);
    });

    it('enforces boundaries on setValue', () => {
      const { result } = renderHook(() => useCounter(5, { min: 0, max: 10 }));
      
      // Test below minimum
      act(() => {
        result.current.setValue(-5);
      });
      expect(result.current.count).toBe(0);
      
      // Test above maximum
      act(() => {
        result.current.setValue(15);
      });
      expect(result.current.count).toBe(10);
      
      // Test within range
      act(() => {
        result.current.setValue(7);
      });
      expect(result.current.count).toBe(7);
    });

    it('enforces boundaries with function setValue', () => {
      const { result } = renderHook(() => useCounter(9, { min: 0, max: 10 }));
      
      act(() => {
        result.current.setValue(prev => prev + 5); // Would be 14, capped to 10
      });
      
      expect(result.current.count).toBe(10);
    });
  });

  describe('Function Stability', () => {
    it('maintains function reference stability', () => {
      const { result, rerender } = renderHook(() => useCounter(0));
      
      const firstRenderFunctions = {
        increment: result.current.increment,
        decrement: result.current.decrement,
        reset: result.current.reset,
        setValue: result.current.setValue
      };
      
      // Trigger re-render by changing count
      act(() => {
        result.current.increment();
      });
      
      rerender();
      
      expect(result.current.increment).toBe(firstRenderFunctions.increment);
      expect(result.current.decrement).toBe(firstRenderFunctions.decrement);
      expect(result.current.reset).toBe(firstRenderFunctions.reset);
      expect(result.current.setValue).toBe(firstRenderFunctions.setValue);
    });

    it('updates function references when dependencies change', () => {
      const { result, rerender } = renderHook(
        ({ step }) => useCounter(0, { step }),
        { initialProps: { step: 1 } }
      );
      
      const firstIncrement = result.current.increment;
      
      // Change step value
      rerender({ step: 2 });
      
      expect(result.current.increment).not.toBe(firstIncrement);
    });
  });

  describe('Edge Cases', () => {
    it('handles negative initial values', () => {
      const { result } = renderHook(() => useCounter(-5));
      
      expect(result.current.count).toBe(-5);
      
      act(() => {
        result.current.increment();
      });
      
      expect(result.current.count).toBe(-4);
    });

    it('handles zero step value', () => {
      const { result } = renderHook(() => useCounter(5, { step: 0 }));
      
      act(() => {
        result.current.increment();
      });
      
      expect(result.current.count).toBe(5); // No change with 0 step
    });

    it('handles negative step value', () => {
      const { result } = renderHook(() => useCounter(5, { step: -1 }));
      
      act(() => {
        result.current.increment(); // Should actually decrement
      });
      
      expect(result.current.count).toBe(4);
    });

    it('handles min equals max boundary', () => {
      const { result } = renderHook(() => useCounter(5, { min: 5, max: 5 }));
      
      act(() => {
        result.current.increment();
      });
      expect(result.current.count).toBe(5);
      
      act(() => {
        result.current.decrement();
      });
      expect(result.current.count).toBe(5);
      
      act(() => {
        result.current.setValue(10);
      });
      expect(result.current.count).toBe(5);
    });
  });
});
```

### 🎯 Context and Provider Testing

**Interview Critical Point:** Testing React Context providers and consumers.

```jsx
// contexts/ThemeContext.jsx
import React, { createContext, useContext, useState, useEffect } from 'react';

const ThemeContext = createContext();

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

export const ThemeProvider = ({ children, defaultTheme = 'light' }) => {
  const [theme, setTheme] = useState(() => {
    // Check localStorage for saved theme
    if (typeof window !== 'undefined') {
      return localStorage.getItem('theme') || defaultTheme;
    }
    return defaultTheme;
  });

  const [isSystemTheme, setIsSystemTheme] = useState(false);

  useEffect(() => {
    // Save theme to localStorage
    localStorage.setItem('theme', theme);
    
    // Apply theme to document
    document.documentElement.setAttribute('data-theme', theme);
    
    // Update CSS custom properties
    const root = document.documentElement;
    if (theme === 'dark') {
      root.style.setProperty('--bg-color', '#1a1a1a');
      root.style.setProperty('--text-color', '#ffffff');
    } else {
      root.style.setProperty('--bg-color', '#ffffff');
      root.style.setProperty('--text-color', '#000000');
    }
  }, [theme]);

  useEffect(() => {
    if (isSystemTheme) {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      
      const handleChange = (e) => {
        setTheme(e.matches ? 'dark' : 'light');
      };
      
      mediaQuery.addEventListener('change', handleChange);
      
      // Set initial theme based on system preference
      setTheme(mediaQuery.matches ? 'dark' : 'light');
      
      return () => mediaQuery.removeEventListener('change', handleChange);
    }
  }, [isSystemTheme]);

  const toggleTheme = () => {
    setIsSystemTheme(false);
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  };

  const setSystemTheme = () => {
    setIsSystemTheme(true);
  };

  const value = {
    theme,
    setTheme,
    toggleTheme,
    setSystemTheme,
    isSystemTheme
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};
```

```jsx
// contexts/__tests__/ThemeContext.test.jsx
import React from 'react';
import { render, screen, act } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { ThemeProvider, useTheme } from '../ThemeContext';

// Test component that uses the theme context
const TestComponent = () => {
  const { theme, toggleTheme, setSystemTheme, isSystemTheme } = useTheme();
  
  return (
    <div>
      <div data-testid="current-theme">{theme}</div>
      <div data-testid="is-system-theme">{isSystemTheme.toString()}</div>
      <button onClick={toggleTheme}>Toggle Theme</button>
      <button onClick={setSystemTheme}>Use System Theme</button>
    </div>
  );
};

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
  clear: jest.fn(),
};
global.localStorage = localStorageMock;

// Mock matchMedia
const mockMatchMedia = (matches) => {
  return jest.fn().mockImplementation(query => ({
    matches,
    media: query,
    onchange: null,
    addListener: jest.fn(),
    removeListener: jest.fn(),
    addEventListener: jest.fn(),
    removeEventListener: jest.fn(),
    dispatchEvent: jest.fn(),
  }));
};

describe('ThemeContext', () => {
  beforeEach(() => {
    localStorageMock.getItem.mockClear();
    localStorageMock.setItem.mockClear();
    window.matchMedia = mockMatchMedia(false);
    
    // Mock document methods
    document.documentElement.setAttribute = jest.fn();
    document.documentElement.style.setProperty = jest.fn();
  });

  describe('ThemeProvider', () => {
    it('provides default light theme', () => {
      localStorageMock.getItem.mockReturnValue(null);
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(screen.getByTestId('current-theme')).toHaveTextContent('light');
    });

    it('uses custom default theme', () => {
      localStorageMock.getItem.mockReturnValue(null);
      
      render(
        <ThemeProvider defaultTheme="dark">
          <TestComponent />
        </ThemeProvider>
      );

      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');
    });

    it('loads theme from localStorage', () => {
      localStorageMock.getItem.mockReturnValue('dark');
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');
      expect(localStorageMock.getItem).toHaveBeenCalledWith('theme');
    });

    it('saves theme to localStorage when changed', async () => {
      const user = userEvent.setup();
      localStorageMock.getItem.mockReturnValue(null);
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      await user.click(screen.getByText('Toggle Theme'));

      expect(localStorageMock.setItem).toHaveBeenCalledWith('theme', 'dark');
    });

    it('applies theme to document element', () => {
      localStorageMock.getItem.mockReturnValue('dark');
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(document.documentElement.setAttribute).toHaveBeenCalledWith('data-theme', 'dark');
    });

    it('sets CSS custom properties for dark theme', () => {
      localStorageMock.getItem.mockReturnValue('dark');
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(document.documentElement.style.setProperty).toHaveBeenCalledWith('--bg-color', '#1a1a1a');
      expect(document.documentElement.style.setProperty).toHaveBeenCalledWith('--text-color', '#ffffff');
    });

    it('sets CSS custom properties for light theme', () => {
      localStorageMock.getItem.mockReturnValue('light');
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(document.documentElement.style.setProperty).toHaveBeenCalledWith('--bg-color', '#ffffff');
      expect(document.documentElement.style.setProperty).toHaveBeenCalledWith('--text-color', '#000000');
    });
  });

  describe('Theme Operations', () => {
    it('toggles theme from light to dark', async () => {
      const user = userEvent.setup();
      localStorageMock.getItem.mockReturnValue('light');
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(screen.getByTestId('current-theme')).toHaveTextContent('light');

      await user.click(screen.getByText('Toggle Theme'));

      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');
    });

    it('toggles theme from dark to light', async () => {
      const user = userEvent.setup();
      localStorageMock.getItem.mockReturnValue('dark');
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');

      await user.click(screen.getByText('Toggle Theme'));

      expect(screen.getByTestId('current-theme')).toHaveTextContent('light');
    });

    it('disables system theme when manually toggling', async () => {
      const user = userEvent.setup();
      localStorageMock.getItem.mockReturnValue('light');
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      // Enable system theme first
      await user.click(screen.getByText('Use System Theme'));
      expect(screen.getByTestId('is-system-theme')).toHaveTextContent('true');

      // Toggle theme manually
      await user.click(screen.getByText('Toggle Theme'));
      expect(screen.getByTestId('is-system-theme')).toHaveTextContent('false');
    });
  });

  describe('System Theme', () => {
    it('follows system preference when enabled', async () => {
      const user = userEvent.setup();
      window.matchMedia = mockMatchMedia(true); // Dark system preference
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      await user.click(screen.getByText('Use System Theme'));

      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');
      expect(screen.getByTestId('is-system-theme')).toHaveTextContent('true');
    });

    it('responds to system theme changes', async () => {
      const user = userEvent.setup();
      let mediaQueryListener;
      
      window.matchMedia = jest.fn().mockImplementation(query => ({
        matches: false,
        media: query,
        onchange: null,
        addListener: jest.fn(),
        removeListener: jest.fn(),
        addEventListener: jest.fn((event, listener) => {
          if (event === 'change') {
            mediaQueryListener = listener;
          }
        }),
        removeEventListener: jest.fn(),
        dispatchEvent: jest.fn(),
      }));
      
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      await user.click(screen.getByText('Use System Theme'));

      expect(screen.getByTestId('current-theme')).toHaveTextContent('light');

      // Simulate system theme change to dark
      act(() => {
        mediaQueryListener({ matches: true });
      });

      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');
    });
  });

  describe('useTheme Hook', () => {
    it('throws error when used outside provider', () => {
      const TestComponentWithoutProvider = () => {
        useTheme();
        return <div>Test</div>;
      };

      // Suppress console.error for this test
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

      expect(() => {
        render(<TestComponentWithoutProvider />);
      }).toThrow('useTheme must be used within a ThemeProvider');

      consoleSpy.mockRestore();
    });

    it('provides theme context values', () => {
      render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      // All context values should be available
      expect(screen.getByTestId('current-theme')).toBeInTheDocument();
      expect(screen.getByTestId('is-system-theme')).toBeInTheDocument();
      expect(screen.getByText('Toggle Theme')).toBeInTheDocument();
      expect(screen.getByText('Use System Theme')).toBeInTheDocument();
    });
  });

  describe('Integration', () => {
    it('maintains theme across component updates', async () => {
      const user = userEvent.setup();
      localStorageMock.getItem.mockReturnValue('light');
      
      const { rerender } = render(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      // Change theme
      await user.click(screen.getByText('Toggle Theme'));
      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');

      // Re-render provider
      rerender(
        <ThemeProvider>
          <TestComponent />
        </ThemeProvider>
      );

      // Theme should persist
      expect(screen.getByTestId('current-theme')).toHaveTextContent('dark');
    });

    it('handles multiple consumers correctly', () => {
      const AnotherTestComponent = () => {
        const { theme } = useTheme();
        return <div data-testid="another-theme">{theme}</div>;
      };

      render(
        <ThemeProvider>
          <TestComponent />
          <AnotherTestComponent />
        </ThemeProvider>
      );

      expect(screen.getByTestId('current-theme')).toHaveTextContent('light');
      expect(screen.getByTestId('another-theme')).toHaveTextContent('light');
    });
  });
});
```

---

## 🔄 Integration Testing Strategies

### 📚 Mock Service Worker (MSW) Setup

**Interview Critical Point:** Testing API interactions without hitting real endpoints.

```jsx
// src/mocks/handlers.js
import { rest } from 'msw';

export const handlers = [
  // User authentication
  rest.post('/api/auth/login', (req, res, ctx) => {
    const { email, password } = req.body;
    
    if (email === 'user@example.com' && password === 'password123') {
      return res(
        ctx.status(200),
        ctx.json({
          user: {
            id: 1,
            email: 'user@example.com',
            name: 'John Doe',
            role: 'user'
          },
          token: 'mock-jwt-token'
        })
      );
    }
    
    return res(
      ctx.status(401),
      ctx.json({
        error: 'Invalid credentials'
      })
    );
  }),

  // Get user profile
  rest.get('/api/user/profile', (req, res, ctx) => {
    const authHeader = req.headers.get('Authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res(
        ctx.status(401),
        ctx.json({ error: 'Unauthorized' })
      );
    }
    
    return res(
      ctx.status(200),
      ctx.json({
        id: 1,
        email: 'user@example.com',
        name: 'John Doe',
        role: 'user',
        preferences: {
          theme: 'light',
          language: 'en'
        }
      })
    );
  }),

  // Get posts with pagination
  rest.get('/api/posts', (req, res, ctx) => {
    const page = Number(req.url.searchParams.get('page')) || 1;
    const limit = Number(req.url.searchParams.get('limit')) || 10;
    const search = req.url.searchParams.get('search') || '';
    
    const allPosts = Array.from({ length: 50 }, (_, i) => ({
      id: i + 1,
      title: `Post ${i + 1}`,
      content: `Content for post ${i + 1}`,
      author: 'John Doe',
      createdAt: new Date(Date.now() - i * 24 * 60 * 60 * 1000).toISOString(),
      tags: ['tag1', 'tag2']
    }));
    
    let filteredPosts = allPosts;
    if (search) {
      filteredPosts = allPosts.filter(post => 
        post.title.toLowerCase().includes(search.toLowerCase()) ||
        post.content.toLowerCase().includes(search.toLowerCase())
      );
    }
    
    const startIndex = (page - 1) * limit;
    const endIndex = startIndex + limit;
    const posts = filteredPosts.slice(startIndex, endIndex);
    
    return res(
      ctx.status(200),
      ctx.json({
        posts,
        pagination: {
          currentPage: page,
          totalPages: Math.ceil(filteredPosts.length / limit),
          totalItems: filteredPosts.length,
          hasNext: endIndex < filteredPosts.length,
          hasPrev: page > 1
        }
      })
    );
  }),

  // Create post
  rest.post('/api/posts', (req, res, ctx) => {
    const { title, content, tags } = req.body;
    
    if (!title || !content) {
      return res(
        ctx.status(400),
        ctx.json({
          error: 'Title and content are required'
        })
      );
    }
    
    return res(
      ctx.status(201),
      ctx.json({
        id: Date.now(),
        title,
        content,
        tags: tags || [],
        author: 'John Doe',
        createdAt: new Date().toISOString()
      })
    );
  }),

  // Error simulation
  rest.get('/api/posts/error', (req, res, ctx) => {
    return res(
      ctx.status(500),
      ctx.json({
        error: 'Internal server error'
      })
    );
  }),

  // Slow response simulation
  rest.get('/api/posts/slow', (req, res, ctx) => {
    return res(
      ctx.delay(3000),
      ctx.status(200),
      ctx.json({
        posts: [],
        pagination: { currentPage: 1, totalPages: 0, totalItems: 0 }
      })
    );
  })
];
```

```jsx
// src/mocks/server.js
import { setupServer } from 'msw/node';
import { handlers } from './handlers';

export const server = setupServer(...handlers);
```

### 🎯 Testing Custom Hooks with API Calls

**Interview Critical Point:** Testing data fetching hooks with realistic async behavior.

```jsx
// hooks/usePosts.js
import { useState, useEffect, useCallback } from 'react';

const API_BASE = process.env.REACT_APP_API_BASE || '/api';

export const usePosts = (options = {}) => {
  const { initialPage = 1, limit = 10, search = '', autoFetch = true } = options;
  
  const [posts, setPosts] = useState([]);
  const [pagination, setPagination] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isRefetching, setIsRefetching] = useState(false);

  const fetchPosts = useCallback(async (page = initialPage, searchQuery = search, isRefetch = false) => {
    try {
      if (isRefetch) {
        setIsRefetching(true);
      } else {
        setLoading(true);
      }
      setError(null);

      const params = new URLSearchParams({
        page: page.toString(),
        limit: limit.toString(),
        ...(searchQuery && { search: searchQuery })
      });

      const response = await fetch(`${API_BASE}/posts?${params}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      setPosts(data.posts);
      setPagination(data.pagination);
    } catch (err) {
      setError(err.message);
      setPosts([]);
      setPagination(null);
    } finally {
      setLoading(false);
      setIsRefetching(false);
    }
  }, [initialPage, limit, search]);

  const createPost = useCallback(async (postData) => {
    try {
      setLoading(true);
      setError(null);

      const response = await fetch(`${API_BASE}/posts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData)
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Failed to create post');
      }

      const newPost = await response.json();
      
      // Add new post to the beginning of the list
      setPosts(prevPosts => [newPost, ...prevPosts]);
      
      return newPost;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const refetch = useCallback(() => {
    return fetchPosts(pagination?.currentPage || 1, search, true);
  }, [fetchPosts, pagination?.currentPage, search]);

  const loadMore = useCallback(() => {
    if (pagination?.hasNext) {
      return fetchPosts(pagination.currentPage + 1, search);
    }
  }, [fetchPosts, pagination, search]);

  const searchPosts = useCallback((searchQuery) => {
    return fetchPosts(1, searchQuery);
  }, [fetchPosts]);

  useEffect(() => {
    if (autoFetch) {
      fetchPosts();
    }
  }, [fetchPosts, autoFetch]);

  return {
    posts,
    pagination,
    loading,
    error,
    isRefetching,
    refetch,
    loadMore,
    searchPosts,
    createPost,
    fetchPosts
  };
};
```

```jsx
// hooks/__tests__/usePosts.test.js
import { renderHook, act, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import { server } from '../../mocks/server';
import { usePosts } from '../usePosts';

describe('usePosts hook', () => {
  beforeEach(() => {
    // Reset any runtime request handlers
    server.resetHandlers();
  });

  describe('Initial State and Fetching', () => {
    it('initializes with correct default state', () => {
      const { result } = renderHook(() => usePosts({ autoFetch: false }));

      expect(result.current.posts).toEqual([]);
      expect(result.current.pagination).toBeNull();
      expect(result.current.loading).toBe(false);
      expect(result.current.error).toBeNull();
      expect(result.current.isRefetching).toBe(false);
    });

    it('fetches posts automatically by default', async () => {
      const { result } = renderHook(() => usePosts());

      expect(result.current.loading).toBe(true);

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.posts).toHaveLength(10);
      expect(result.current.pagination).toEqual({
        currentPage: 1,
        totalPages: 5,
        totalItems: 50,
        hasNext: true,
        hasPrev: false
      });
      expect(result.current.error).toBeNull();
    });

    it('does not auto-fetch when autoFetch is false', () => {
      const { result } = renderHook(() => usePosts({ autoFetch: false }));

      expect(result.current.loading).toBe(false);
      expect(result.current.posts).toEqual([]);
    });

    it('applies custom pagination options', async () => {
      const { result } = renderHook(() => 
        usePosts({ initialPage: 2, limit: 5 })
      );

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.pagination?.currentPage).toBe(2);
      expect(result.current.posts).toHaveLength(5);
    });
  });

  describe('Search Functionality', () => {
    it('searches posts with query', async () => {
      const { result } = renderHook(() => usePosts({ autoFetch: false }));

      act(() => {
        result.current.searchPosts('Post 1');
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      // Should return posts containing "Post 1" (Post 1, Post 10-19)
      expect(result.current.posts.length).toBeGreaterThan(0);
      expect(result.current.posts.every(post => 
        post.title.includes('Post 1') || post.content.includes('Post 1')
      )).toBe(true);
    });

    it('handles empty search results', async () => {
      const { result } = renderHook(() => usePosts({ autoFetch: false }));

      act(() => {
        result.current.searchPosts('nonexistent query');
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.posts).toEqual([]);
      expect(result.current.pagination?.totalItems).toBe(0);
    });
  });

  describe('Pagination', () => {
    it('loads more posts when available', async () => {
      const { result } = renderHook(() => usePosts());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      const initialPostsCount = result.current.posts.length;
      expect(result.current.pagination?.hasNext).toBe(true);

      act(() => {
        result.current.loadMore();
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.posts.length).toBeGreaterThan(initialPostsCount);
      expect(result.current.pagination?.currentPage).toBe(2);
    });

    it('does not load more when no next page available', async () => {
      const { result } = renderHook(() => 
        usePosts({ initialPage: 5 }) // Last page
      );

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.pagination?.hasNext).toBe(false);

      const beforeLoadMore = result.current.posts.length;

      act(() => {
        result.current.loadMore();
      });

      // Should not trigger loading or change posts
      expect(result.current.loading).toBe(false);
      expect(result.current.posts.length).toBe(beforeLoadMore);
    });
  });

  describe('Refetching', () => {
    it('refetches current page data', async () => {
      const { result } = renderHook(() => usePosts());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      act(() => {
        result.current.refetch();
      });

      expect(result.current.isRefetching).toBe(true);
      expect(result.current.loading).toBe(false); // Should not show main loading

      await waitFor(() => {
        expect(result.current.isRefetching).toBe(false);
      });

      expect(result.current.posts).toHaveLength(10);
      expect(result.current.pagination?.currentPage).toBe(1);
    });
  });

  describe('Post Creation', () => {
    it('creates a new post successfully', async () => {
      const { result } = renderHook(() => usePosts());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      const newPostData = {
        title: 'New Test Post',
        content: 'This is a test post content',
        tags: ['test', 'new']
      };

      let createdPost;
      await act(async () => {
        createdPost = await result.current.createPost(newPostData);
      });

      expect(createdPost).toMatchObject(newPostData);
      expect(createdPost.id).toBeDefined();
      expect(createdPost.createdAt).toBeDefined();

      // New post should be added to the beginning of the list
      expect(result.current.posts[0]).toEqual(createdPost);
    });

    it('handles post creation errors', async () => {
      const { result } = renderHook(() => usePosts());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      const invalidPostData = {
        title: '', // Invalid: empty title
        content: 'Content without title'
      };

      await act(async () => {
        try {
          await result.current.createPost(invalidPostData);
        } catch (error) {
          expect(error.message).toBe('Title and content are required');
        }
      });

      expect(result.current.error).toBe('Title and content are required');
    });
  });

  describe('Error Handling', () => {
    it('handles fetch errors gracefully', async () => {
      // Override default handler to return error
      server.use(
        rest.get('/api/posts', (req, res, ctx) => {
          return res(
            ctx.status(500),
            ctx.json({ error: 'Server error' })
          );
        })
      );

      const { result } = renderHook(() => usePosts());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.error).toBe('HTTP error! status: 500');
      expect(result.current.posts).toEqual([]);
      expect(result.current.pagination).toBeNull();
    });

    it('handles network errors', async () => {
      // Override handler to simulate network error
      server.use(
        rest.get('/api/posts', (req, res, ctx) => {
          return res.networkError('Network error');
        })
      );

      const { result } = renderHook(() => usePosts());

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.error).toContain('fetch');
      expect(result.current.posts).toEqual([]);
    });

    it('clears error on successful refetch', async () => {
      // First, cause an error
      server.use(
        rest.get('/api/posts', (req, res, ctx) => {
          return res(
            ctx.status(500),
            ctx.json({ error: 'Server error' })
          );
        })
      );

      const { result } = renderHook(() => usePosts());

      await waitFor(() => {
        expect(result.current.error).toBeTruthy();
      });

      // Reset to successful handler
      server.resetHandlers();

      act(() => {
        result.current.refetch();
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.error).toBeNull();
      expect(result.current.posts.length).toBeGreaterThan(0);
    });
  });

  describe('Performance and Stability', () => {
    it('maintains function reference stability', () => {
      const { result, rerender } = renderHook(() => usePosts({ autoFetch: false }));

      const firstRenderFunctions = {
        refetch: result.current.refetch,
        loadMore: result.current.loadMore,
        searchPosts: result.current.searchPosts,
        createPost: result.current.createPost,
        fetchPosts: result.current.fetchPosts
      };

      rerender();

      expect(result.current.refetch).toBe(firstRenderFunctions.refetch);
      expect(result.current.loadMore).toBe(firstRenderFunctions.loadMore);
      expect(result.current.searchPosts).toBe(firstRenderFunctions.searchPosts);
      expect(result.current.createPost).toBe(firstRenderFunctions.createPost);
      expect(result.current.fetchPosts).toBe(firstRenderFunctions.fetchPosts);
    });

    it('handles rapid successive calls correctly', async () => {
      const { result } = renderHook(() => usePosts({ autoFetch: false }));

      // Make multiple rapid calls
      act(() => {
        result.current.fetchPosts();
        result.current.fetchPosts();
        result.current.fetchPosts();
      });

      await waitFor(() => {
        expect(result.current.loading).toBe(false);
      });

      expect(result.current.posts).toHaveLength(10);
      expect(result.current.error).toBeNull();
    });
  });
});
```

### 🎯 Testing Component Integration with Context and API

**Interview Critical Point:** Testing full component workflows with realistic data flow.

```jsx
// components/PostList/PostList.jsx
import React, { useState } from 'react';
import { usePosts } from '../../hooks/usePosts';
import { useTheme } from '../../contexts/ThemeContext';
import Button from '../Button/Button';

const PostList = ({ searchQuery = '', onPostClick }) => {
  const { theme } = useTheme();
  const {
    posts,
    pagination,
    loading,
    error,
    isRefetching,
    loadMore,
    refetch,
    searchPosts
  } = usePosts({ search: searchQuery });

  const [localSearchQuery, setLocalSearchQuery] = useState(searchQuery);

  const handleSearch = (e) => {
    e.preventDefault();
    searchPosts(localSearchQuery);
  };

  const handlePostClick = (post) => {
    onPostClick?.(post);
  };

  const handleRetry = () => {
    refetch();
  };

  if (error) {
    return (
      <div className={`post-list post-list--${theme}`} data-testid="post-list-error">
        <div className="error-state">
          <h3>Something went wrong</h3>
          <p>{error}</p>
          <Button onClick={handleRetry}>Try Again</Button>
        </div>
      </div>
    );
  }

  return (
    <div className={`post-list post-list--${theme}`} data-testid="post-list">
      {/* Search Form */}
      <form onSubmit={handleSearch} className="search-form">
        <div className="search-input-group">
          <input
            type="text"
            value={localSearchQuery}
            onChange={(e) => setLocalSearchQuery(e.target.value)}
            placeholder="Search posts..."
            disabled={loading}
            aria-label="Search posts"
          />
          <Button 
            type="submit" 
            disabled={loading}
            loading={loading && !isRefetching}
          >
            Search
          </Button>
        </div>
      </form>

      {/* Refresh Button */}
      <div className="list-controls">
        <Button
          onClick={refetch}
          variant="secondary"
          disabled={loading}
          loading={isRefetching}
        >
          {isRefetching ? 'Refreshing...' : 'Refresh'}
        </Button>
      </div>

      {/* Loading State */}
      {loading && !isRefetching && (
        <div className="loading-state" data-testid="loading-state">
          <div className="spinner" role="status" aria-label="Loading posts">
            Loading posts...
          </div>
        </div>
      )}

      {/* Empty State */}
      {!loading && posts.length === 0 && (
        <div className="empty-state" data-testid="empty-state">
          <h3>No posts found</h3>
          <p>
            {searchQuery 
              ? `No posts match "${searchQuery}". Try a different search term.`
              : 'No posts available at the moment.'
            }
          </p>
        </div>
      )}

      {/* Posts List */}
      {posts.length > 0 && (
        <>
          <div className="posts-grid" data-testid="posts-grid">
            {posts.map((post) => (
              <article
                key={post.id}
                className="post-card"
                onClick={() => handlePostClick(post)}
                role="button"
                tabIndex={0}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    handlePostClick(post);
                  }
                }}
                aria-label={`Post: ${post.title}`}
              >
                <h3 className="post-title">{post.title}</h3>
                <p className="post-content">{post.content}</p>
                <div className="post-meta">
                  <span className="post-author">By {post.author}</span>
                  <time className="post-date">
                    {new Date(post.createdAt).toLocaleDateString()}
                  </time>
                </div>
                {post.tags && post.tags.length > 0 && (
                  <div className="post-tags">
                    {post.tags.map((tag) => (
                      <span key={tag} className="tag">
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </article>
            ))}
          </div>

          {/* Pagination */}
          {pagination && (
            <div className="pagination-controls" data-testid="pagination-controls">
              <div className="pagination-info">
                Page {pagination.currentPage} of {pagination.totalPages} 
                ({pagination.totalItems} total posts)
              </div>
              
              {pagination.hasNext && (
                <Button
                  onClick={loadMore}
                  disabled={loading}
                  loading={loading && !isRefetching}
                >
                  Load More
                </Button>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default PostList;
```

```jsx
// components/PostList/__tests__/PostList.integration.test.jsx
import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { rest } from 'msw';
import { server } from '../../../mocks/server';
import { ThemeProvider } from '../../../contexts/ThemeContext';
import PostList from '../PostList';

// Test wrapper that provides all necessary providers
const TestWrapper = ({ children, themeProps = {} }) => (
  <ThemeProvider {...themeProps}>
    {children}
  </ThemeProvider>
);

const renderWithProviders = (ui, options = {}) => {
  const { providerProps = {}, ...renderOptions } = options;
  
  return render(
    <TestWrapper {...providerProps}>
      {ui}
    </TestWrapper>,
    renderOptions
  );
};

describe('PostList Integration Tests', () => {
  const mockOnPostClick = jest.fn();

  beforeEach(() => {
    mockOnPostClick.mockClear();
  });

  describe('Initial Loading and Display', () => {
    it('renders loading state then posts', async () => {
      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      // Should show loading state initially
      expect(screen.getByTestId('loading-state')).toBeInTheDocument();
      expect(screen.getByLabelText(/loading posts/i)).toBeInTheDocument();

      // Wait for posts to load
      await waitFor(() => {
        expect(screen.queryByTestId('loading-state')).not.toBeInTheDocument();
      });

      // Should show posts grid
      expect(screen.getByTestId('posts-grid')).toBeInTheDocument();
      expect(screen.getAllByRole('article')).toHaveLength(10);
    });

    it('displays posts with correct content', async () => {
      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getByText('Post 1')).toBeInTheDocument();
      });

      // Check first post content
      expect(screen.getByText('Post 1')).toBeInTheDocument();
      expect(screen.getByText('Content for post 1')).toBeInTheDocument();
      expect(screen.getByText('By John Doe')).toBeInTheDocument();
      expect(screen.getByText('tag1')).toBeInTheDocument();
      expect(screen.getByText('tag2')).toBeInTheDocument();
    });

    it('shows pagination controls', async () => {
      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getByTestId('pagination-controls')).toBeInTheDocument();
      });

      expect(screen.getByText(/page 1 of 5/i)).toBeInTheDocument();
      expect(screen.getByText(/50 total posts/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /load more/i })).toBeInTheDocument();
    });
  });

  describe('Theme Integration', () => {
    it('applies light theme class', async () => {
      renderWithProviders(
        <PostList onPostClick={mockOnPostClick} />,
        { providerProps: { defaultTheme: 'light' } }
      );

      await waitFor(() => {
        expect(screen.getByTestId('post-list')).toHaveClass('post-list--light');
      });
    });

    it('applies dark theme class', async () => {
      renderWithProviders(
        <PostList onPostClick={mockOnPostClick} />,
        { providerProps: { defaultTheme: 'dark' } }
      );

      await waitFor(() => {
        expect(screen.getByTestId('post-list')).toHaveClass('post-list--dark');
      });
    });
  });

  describe('Search Functionality', () => {
    it('performs search and shows filtered results', async () => {
      const user = userEvent.setup();
      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getAllByRole('article')).toHaveLength(10);
      });

      // Perform search
      const searchInput = screen.getByLabelText(/search posts/i);
      await user.clear(searchInput);
      await user.type(searchInput, 'Post 1');
      await user.click(screen.getByRole('button', { name: /search/i }));

      // Should show loading state
      expect(screen.getByRole('button', { name: /search/i })).toBeDisabled();

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /search/i })).not.toBeDisabled();
      });

      // Should show filtered results
      const articles = screen.getAllByRole('article');
      expect(articles.length).toBeGreaterThan(0);
      
      // All visible posts should contain "Post 1"
      articles.forEach(article => {
        expect(article.textContent).toMatch(/Post 1/);
      });
    });

    it('shows empty state for no search results', async () => {
      const user = userEvent.setup();
      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getAllByRole('article')).toHaveLength(10);
      });

      // Search for non-existent content
      const searchInput = screen.getByLabelText(/search posts/i);
      await user.clear(searchInput);
      await user.type(searchInput, 'nonexistent query');
      await user.click(screen.getByRole('button', { name: /search/i }));

      await waitFor(() => {
        expect(screen.getByTestId('empty-state')).toBeInTheDocument();
      });

      expect(screen.getByText(/no posts found/i)).toBeInTheDocument();
      expect(screen.getByText(/no posts match "nonexistent query"/i)).toBeInTheDocument();
    });

    it('handles search with initial search query prop', async () => {
      renderWithProviders(
        <PostList searchQuery="Post 2" onPostClick={mockOnPostClick} />
      );

      await waitFor(() => {
        expect(screen.getByDisplayValue('Post 2')).toBeInTheDocument();
      });

      // Should show filtered results immediately
      const articles = screen.getAllByRole('article');
      articles.forEach(article => {
        expect(article.textContent).toMatch(/Post 2/);
      });
    });
  });

  describe('Post Interaction', () => {
    it('calls onPostClick when post is clicked', async () => {
      const user = userEvent.setup();
      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getByText('Post 1')).toBeInTheDocument();
      });

      const firstPost = screen.getAllByRole('article')[0];
      await user.click(firstPost);

      expect(mockOnPostClick).toHaveBeenCalledWith(
        expect.objectContaining({
          id: 1,
          title: 'Post 1',
          content: 'Content for post 1'
        })
      );
    });

    it('handles keyboard navigation for post selection', async () => {
      const user = userEvent.setup();
      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getByText('Post 1')).toBeInTheDocument();
      });

      const firstPost = screen.getAllByRole('article')[0];
      firstPost.focus();

      await user.keyboard('{Enter}');

      expect(mockOnPostClick).toHaveBeenCalledWith(
        expect.objectContaining({
          id: 1,
          title: 'Post 1'
        })
      );

      mockOnPostClick.mockClear();

      await user.keyboard(' ');

      expect(mockOnPostClick).toHaveBeenCalledWith(
        expect.objectContaining({
          id: 1,
          title: 'Post 1'
        })
      );
    });

    it('handles missing onPostClick gracefully', async () => {
      const user = userEvent.setup();
      renderWithProviders(<PostList />); // No onPostClick prop

      await waitFor(() => {
        expect(screen.getByText('Post 1')).toBeInTheDocument();
      });

      const firstPost = screen.getAllByRole('article')[0];

      // Should not throw error
      await user.click(firstPost);

      expect(screen.getByText('Post 1')).toBeInTheDocument();
    });
  });

  describe('Pagination', () => {
    it('loads more posts when Load More is clicked', async () => {
      const user = userEvent.setup();
      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getAllByRole('article')).toHaveLength(10);
      });

      expect(screen.getByText(/page 1 of 5/i)).toBeInTheDocument();

      const loadMoreButton = screen.getByRole('button', { name: /load more/i });
      await user.click(loadMoreButton);

      // Should show loading state on button
      expect(loadMoreButton).toBeDisabled();

      await waitFor(() => {
        expect(loadMoreButton).not.toBeDisabled();
      });

      // Should have more posts now
      expect(screen.getAllByRole('article')).toHaveLength(15); // 10 + 5 more
      expect(screen.getByText(/page 2 of 5/i)).toBeInTheDocument();
    });

    it('hides Load More button on last page', async () => {
      const user = userEvent.setup();
      
      // Start on page 5 (last page)
      server.use(
        rest.get('/api/posts', (req, res, ctx) => {
          return res(
            ctx.status(200),
            ctx.json({
              posts: Array.from({ length: 10 }, (_, i) => ({
                id: i + 41,
                title: `Post ${i + 41}`,
                content: `Content for post ${i + 41}`,
                author: 'John Doe',
                createdAt: new Date().toISOString(),
                tags: ['tag1', 'tag2']
              })),
              pagination: {
                currentPage: 5,
                totalPages: 5,
                totalItems: 50,
                hasNext: false,
                hasPrev: true
              }
            })
          );
        })
      );

      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getByText(/page 5 of 5/i)).toBeInTheDocument();
      });

      expect(screen.queryByRole('button', { name: /load more/i })).not.toBeInTheDocument();
    });
  });

  describe('Refresh Functionality', () => {
    it('refreshes posts when refresh button is clicked', async () => {
      const user = userEvent.setup();
      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getAllByRole('article')).toHaveLength(10);
      });

      const refreshButton = screen.getByRole('button', { name: /^refresh$/i });
      await user.click(refreshButton);

      // Should show refreshing state
      expect(screen.getByRole('button', { name: /refreshing/i })).toBeInTheDocument();

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /^refresh$/i })).toBeInTheDocument();
      });

      // Posts should still be there (data didn't change, but request was made)
      expect(screen.getAllByRole('article')).toHaveLength(10);
    });
  });

  describe('Error Handling', () => {
    it('displays error state with retry option', async () => {
      const user = userEvent.setup();
      
      // Force API to return error
      server.use(
        rest.get('/api/posts', (req, res, ctx) => {
          return res(
            ctx.status(500),
            ctx.json({ error: 'Internal server error' })
          );
        })
      );

      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getByTestId('post-list-error')).toBeInTheDocument();
      });

      expect(screen.getByText(/something went wrong/i)).toBeInTheDocument();
      expect(screen.getByText(/http error! status: 500/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument();

      // Reset to successful response
      server.resetHandlers();

      // Click retry
      await user.click(screen.getByRole('button', { name: /try again/i }));

      await waitFor(() => {
        expect(screen.queryByTestId('post-list-error')).not.toBeInTheDocument();
      });

      expect(screen.getByTestId('post-list')).toBeInTheDocument();
      expect(screen.getAllByRole('article')).toHaveLength(10);
    });

    it('applies theme class even in error state', async () => {
      server.use(
        rest.get('/api/posts', (req, res, ctx) => {
          return res(
            ctx.status(500),
            ctx.json({ error: 'Server error' })
          );
        })
      );

      renderWithProviders(
        <PostList onPostClick={mockOnPostClick} />,
        { providerProps: { defaultTheme: 'dark' } }
      );

      await waitFor(() => {
        expect(screen.getByTestId('post-list-error')).toHaveClass('post-list--dark');
      });
    });
  });

  describe('Accessibility', () => {
    it('provides proper ARIA labels and roles', async () => {
      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getByLabelText(/search posts/i)).toBeInTheDocument();
      });

      expect(screen.getByLabelText(/search posts/i)).toHaveAttribute('type', 'text');
      
      const articles = screen.getAllByRole('article');
      expect(articles[0]).toHaveAttribute('role', 'button');
      expect(articles[0]).toHaveAttribute('tabIndex', '0');
      expect(articles[0]).toHaveAttribute('aria-label', 'Post: Post 1');
    });

    it('provides loading announcement for screen readers', async () => {
      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      expect(screen.getByLabelText(/loading posts/i)).toBeInTheDocument();

      await waitFor(() => {
        expect(screen.queryByLabelText(/loading posts/i)).not.toBeInTheDocument();
      });
    });

    it('handles keyboard navigation correctly', async () => {
      const user = userEvent.setup();
      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getAllByRole('article')).toHaveLength(10);
      });

      const searchInput = screen.getByLabelText(/search posts/i);
      const searchButton = screen.getByRole('button', { name: /search/i });
      const firstPost = screen.getAllByRole('article')[0];

      // Tab navigation
      searchInput.focus();
      expect(document.activeElement).toBe(searchInput);

      await user.tab();
      expect(document.activeElement).toBe(searchButton);

      await user.tab();
      expect(document.activeElement).toBe(screen.getByRole('button', { name: /refresh/i }));

      // Can focus on posts
      firstPost.focus();
      expect(document.activeElement).toBe(firstPost);
    });
  });

  describe('Performance and Edge Cases', () => {
    it('handles rapid search queries correctly', async () => {
      const user = userEvent.setup();
      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getAllByRole('article')).toHaveLength(10);
      });

      const searchInput = screen.getByLabelText(/search posts/i);

      // Rapidly change search input
      await user.clear(searchInput);
      await user.type(searchInput, 'rapid');
      await user.clear(searchInput);
      await user.type(searchInput, 'test');

      // Submit final search
      await user.click(screen.getByRole('button', { name: /search/i }));

      await waitFor(() => {
        expect(screen.getByDisplayValue('test')).toBeInTheDocument();
      });

      // Should handle it without errors
      expect(screen.getByTestId('post-list')).toBeInTheDocument();
    });

    it('maintains component state during theme changes', async () => {
      const { rerender } = renderWithProviders(
        <PostList searchQuery="Post 1" onPostClick={mockOnPostClick} />,
        { providerProps: { defaultTheme: 'light' } }
      );

      await waitFor(() => {
        expect(screen.getByDisplayValue('Post 1')).toBeInTheDocument();
      });

      // Change theme
      rerender(
        <TestWrapper themeProps={{ defaultTheme: 'dark' }}>
          <PostList searchQuery="Post 1" onPostClick={mockOnPostClick} />
        </TestWrapper>
      );

      // Search input should maintain its value
      expect(screen.getByDisplayValue('Post 1')).toBeInTheDocument();
      expect(screen.getByTestId('post-list')).toHaveClass('post-list--dark');
    });

    it('handles empty posts array correctly', async () => {
      server.use(
        rest.get('/api/posts', (req, res, ctx) => {
          return res(
            ctx.status(200),
            ctx.json({
              posts: [],
              pagination: {
                currentPage: 1,
                totalPages: 0,
                totalItems: 0,
                hasNext: false,
                hasPrev: false
              }
            })
          );
        })
      );

      renderWithProviders(<PostList onPostClick={mockOnPostClick} />);

      await waitFor(() => {
        expect(screen.getByTestId('empty-state')).toBeInTheDocument();
      });

      expect(screen.getByText(/no posts available/i)).toBeInTheDocument();
      expect(screen.queryByTestId('posts-grid')).not.toBeInTheDocument();
      expect(screen.queryByTestId('pagination-controls')).not.toBeInTheDocument();
    });
  });
});
```

---

## 🎯 End-to-End Testing

### 📚 Cypress Setup and Configuration

**Interview Critical Point:** Understanding the difference between integration and E2E testing scope.

```javascript
// cypress.config.js
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    experimentalStudio: true,
    
    // Test file patterns
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    
    // Browser launch options
    chromeWebSecurity: false,
    
    // Timeouts
    defaultCommandTimeout: 10000,
    requestTimeout: 10000,
    responseTimeout: 10000,
    pageLoadTimeout: 30000,
    
    // Test isolation
    testIsolation: true,
    
    setupNodeEvents(on, config) {
      // Code coverage
      require('@cypress/code-coverage/task')(on, config);
      
      // Environment variables
      on('before:browser:launch', (browser = {}, launchOptions) => {
        if (browser.name === 'chrome') {
          launchOptions.args.push('--disable-dev-shm-usage');
          launchOptions.args.push('--no-sandbox');
        }
        return launchOptions;
      });

      // Task for database seeding (if needed)
      on('task', {
        seedDatabase() {
          // Seed test data
          return null;
        },
        
        clearDatabase() {
          // Clear test data
          return null;
        },

        log(message) {
          console.log(message);
          return null;
        }
      });

      return config;
    },
  },

  component: {
    devServer: {
      framework: 'create-react-app',
      bundler: 'webpack',
    },
    specPattern: 'src/**/*.cy.{js,jsx,ts,tsx}',
    indexHtmlFile: 'cypress/support/component-index.html',
    setupNodeEvents(on, config) {
      require('@cypress/code-coverage/task')(on, config);
      return config;
    },
  },

  env: {
    // API endpoints
    apiUrl: 'http://localhost:3001/api',
    
    // Test user credentials
    testUser: {
      email: 'test@example.com',
      password: 'testpassword123'
    },
    
    // Feature flags
    features: {
      newDashboard: true,
      advancedSearch: true
    }
  }
});
```

```javascript
// cypress/support/e2e.js
import './commands';
import '@cypress/code-coverage/support';

// Global before hook
beforeEach(() => {
  // Clear localStorage and sessionStorage
  cy.clearLocalStorage();
  cy.clearCookies();
  
  // Set up API interception defaults
  cy.intercept('GET', '/api/health', { fixture: 'health.json' });
  
  // Handle uncaught exceptions
  cy.on('uncaught:exception', (err, runnable) => {
    // Don't fail on certain expected errors
    if (err.message.includes('ResizeObserver loop limit exceeded')) {
      return false;
    }
    return true;
  });
});

// Global after hook
afterEach(() => {
  // Take screenshot on failure
  cy.screenshot({ capture: 'viewport', onlyOnFailure: true });
});
```

```javascript
// cypress/support/commands.js

// Custom commands for authentication
Cypress.Commands.add('login', (email, password) => {
  cy.session([email, password], () => {
    cy.visit('/login');
    cy.get('[data-testid="email-input"]').type(email);
    cy.get('[data-testid="password-input"]').type(password);
    cy.get('[data-testid="login-button"]').click();
    
    // Wait for redirect to dashboard
    cy.url().should('include', '/dashboard');
    cy.get('[data-testid="user-menu"]').should('be.visible');
  });
});

Cypress.Commands.add('loginApi', (email, password) => {
  cy.request({
    method: 'POST',
    url: `${Cypress.env('apiUrl')}/auth/login`,
    body: { email, password }
  }).then((response) => {
    window.localStorage.setItem('authToken', response.body.token);
    window.localStorage.setItem('user', JSON.stringify(response.body.user));
  });
});

// Custom commands for data manipulation
Cypress.Commands.add('seedData', (type, data) => {
  cy.request({
    method: 'POST',
    url: `${Cypress.env('apiUrl')}/test/seed`,
    body: { type, data },
    headers: {
      'Authorization': `Bearer ${window.localStorage.getItem('authToken')}`
    }
  });
});

Cypress.Commands.add('clearData', (type) => {
  cy.request({
    method: 'DELETE',
    url: `${Cypress.env('apiUrl')}/test/clear/${type}`,
    headers: {
      'Authorization': `Bearer ${window.localStorage.getItem('authToken')}`
    }
  });
});

// Custom commands for UI interactions
Cypress.Commands.add('getByTestId', (testId) => {
  return cy.get(`[data-testid="${testId}"]`);
});

Cypress.Commands.add('findByTestId', (testId) => {
  return cy.find(`[data-testid="${testId}"]`);
});

Cypress.Commands.add('waitForSpinner', () => {
  cy.get('[data-testid="loading-spinner"]', { timeout: 1000 }).should('exist');
  cy.get('[data-testid="loading-spinner"]', { timeout: 10000 }).should('not.exist');
});

Cypress.Commands.add('waitForToast', (message) => {
  cy.get('[data-testid="toast"]').should('be.visible');
  if (message) {
    cy.get('[data-testid="toast"]').should('contain.text', message);
  }
  cy.get('[data-testid="toast"]', { timeout: 5000 }).should('not.exist');
});

// Custom commands for accessibility
Cypress.Commands.add('checkA11y', (context, options) => {
  cy.injectAxe();
  cy.checkA11y(context, options, violations => {
    violations.forEach(violation => {
      cy.task('log', `Accessibility violation: ${violation.id}`);
      cy.task('log', `Description: ${violation.description}`);
      cy.task('log', `Impact: ${violation.impact}`);
      cy.task('log', `Help: ${violation.helpUrl}`);
    });
  });
});

// Custom commands for visual testing
Cypress.Commands.add('matchImageSnapshot', (name, options = {}) => {
  const defaultOptions = {
    threshold: 0.2,
    thresholdType: 'percent',
    customDiffConfig: {
      threshold: 0.1
    },
    capture: 'viewport'
  };
  
  cy.screenshot(name, { ...defaultOptions, ...options });
});

// Custom commands for network testing
Cypress.Commands.add('mockApiResponse', (method, url, response, statusCode = 200) => {
  cy.intercept(method, url, {
    statusCode,
    body: response
  }).as('apiCall');
});

Cypress.Commands.add('mockApiError', (method, url, statusCode = 500, message = 'Server Error') => {
  cy.intercept(method, url, {
    statusCode,
    body: { error: message }
  }).as('apiError');
});

// Custom commands for form interactions
Cypress.Commands.add('fillForm', (formData) => {
  Object.entries(formData).forEach(([field, value]) => {
    if (Array.isArray(value)) {
      // Handle multi-select or checkbox groups
      value.forEach(item => {
        cy.get(`[data-testid="${field}"] [value="${item}"]`).check();
      });
    } else if (typeof value === 'boolean') {
      // Handle checkboxes
      if (value) {
        cy.get(`[data-testid="${field}"]`).check();
      } else {
        cy.get(`[data-testid="${field}"]`).uncheck();
      }
    } else {
      // Handle regular inputs
      cy.get(`[data-testid="${field}"]`).clear().type(value);
    }
  });
});

Cypress.Commands.add('submitForm', (formTestId = 'form') => {
  cy.get(`[data-testid="${formTestId}"]`).submit();
});
```

### 🎯 Authentication and User Flow Testing

**Interview Critical Point:** Testing complete user journeys and state persistence.

```javascript
// cypress/e2e/auth/authentication.cy.js
describe('Authentication Flow', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  describe('Login Process', () => {
    it('should login successfully with valid credentials', () => {
      const { email, password } = Cypress.env('testUser');
      
      // Navigate to login
      cy.getByTestId('login-link').click();
      cy.url().should('include', '/login');
      
      // Fill login form
      cy.getByTestId('email-input').type(email);
      cy.getByTestId('password-input').type(password);
      cy.getByTestId('login-button').click();
      
      // Verify successful login
      cy.waitForSpinner();
      cy.url().should('include', '/dashboard');
      cy.getByTestId('user-menu').should('be.visible');
      cy.getByTestId('user-menu').should('contain.text', 'John Doe');
      
      // Verify localStorage has auth token
      cy.window().its('localStorage.authToken').should('exist');
    });

    it('should show error for invalid credentials', () => {
      cy.getByTestId('login-link').click();
      
      // Try invalid credentials
      cy.getByTestId('email-input').type('invalid@example.com');
      cy.getByTestId('password-input').type('wrongpassword');
      cy.getByTestId('login-button').click();
      
      // Verify error handling
      cy.getByTestId('error-message')
        .should('be.visible')
        .and('contain.text', 'Invalid credentials');
      
      // Should stay on login page
      cy.url().should('include', '/login');
      cy.window().its('localStorage.authToken').should('not.exist');
    });

    it('should validate required fields', () => {
      cy.getByTestId('login-link').click();
      
      // Try to submit empty form
      cy.getByTestId('login-button').click();
      
      // Check validation messages
      cy.getByTestId('email-error')
        .should('be.visible')
        .and('contain.text', 'Email is required');
      
      cy.getByTestId('password-error')
        .should('be.visible')
        .and('contain.text', 'Password is required');
    });

    it('should validate email format', () => {
      cy.getByTestId('login-link').click();
      
      cy.getByTestId('email-input').type('invalid-email');
      cy.getByTestId('password-input').type('password123');
      cy.getByTestId('login-button').click();
      
      cy.getByTestId('email-error')
        .should('be.visible')
        .and('contain.text', 'Please enter a valid email');
    });

    it('should handle loading states correctly', () => {
      // Mock slow API response
      cy.intercept('POST', '/api/auth/login', (req) => {
        req.reply((res) => {
          res.delay(2000);
          res.send({ fixture: 'auth/login-success.json' });
        });
      }).as('slowLogin');
      
      cy.getByTestId('login-link').click();
      cy.getByTestId('email-input').type(Cypress.env('testUser.email'));
      cy.getByTestId('password-input').type(Cypress.env('testUser.password'));
      
      cy.getByTestId('login-button').click();
      
      // Verify loading state
      cy.getByTestId('login-button')
        .should('contain.text', 'Signing in...')
        .and('be.disabled');
      
      cy.getByTestId('loading-spinner').should('be.visible');
      
      // Wait for completion
      cy.wait('@slowLogin');
      cy.url().should('include', '/dashboard');
    });
  });

  describe('Logout Process', () => {
    beforeEach(() => {
      cy.login(Cypress.env('testUser.email'), Cypress.env('testUser.password'));
      cy.visit('/dashboard');
    });

    it('should logout successfully', () => {
      cy.getByTestId('user-menu').click();
      cy.getByTestId('logout-button').click();
      
      // Verify logout
      cy.url().should('include', '/');
      cy.getByTestId('login-link').should('be.visible');
      
      // Verify localStorage is cleared
      cy.window().its('localStorage.authToken').should('not.exist');
    });

    it('should logout on token expiration', () => {
      // Mock API calls to return 401
      cy.intercept('GET', '/api/**', { statusCode: 401 }).as('unauthorizedRequest');
      
      // Try to access protected content
      cy.getByTestId('posts-link').click();
      
      // Should redirect to login
      cy.url().should('include', '/login');
      cy.getByTestId('error-message')
        .should('contain.text', 'Session expired');
    });
  });

  describe('Protected Routes', () => {
    it('should redirect to login when accessing protected routes without auth', () => {
      cy.visit('/dashboard');
      cy.url().should('include', '/login');
      
      cy.visit('/posts');
      cy.url().should('include', '/login');
      
      cy.visit('/profile');
      cy.url().should('include', '/login');
    });

    it('should redirect to intended route after login', () => {
      // Try to access protected route
      cy.visit('/posts');
      cy.url().should('include', '/login');
      
      // Login
      cy.getByTestId('email-input').type(Cypress.env('testUser.email'));
      cy.getByTestId('password-input').type(Cypress.env('testUser.password'));
      cy.getByTestId('login-button').click();
      
      // Should redirect to originally requested route
      cy.url().should('include', '/posts');
    });

    it('should maintain authentication across page refreshes', () => {
      cy.login(Cypress.env('testUser.email'), Cypress.env('testUser.password'));
      cy.visit('/dashboard');
      
      // Refresh page
      cy.reload();
      
      // Should still be authenticated
      cy.url().should('include', '/dashboard');
      cy.getByTestId('user-menu').should('be.visible');
    });
  });

  describe('Registration Process', () => {
    it('should register new user successfully', () => {
      const newUser = {
        name: 'New User',
        email: `newuser+${Date.now()}@example.com`,
        password: 'newpassword123',
        confirmPassword: 'newpassword123'
      };
      
      cy.getByTestId('register-link').click();
      cy.url().should('include', '/register');
      
      // Fill registration form
      cy.fillForm({
        'name': newUser.name,
        'email': newUser.email,
        'password': newUser.password,
        'confirm-password': newUser.confirmPassword,
        'agree-terms': true
      });
      
      cy.getByTestId('register-button').click();
      
      // Verify successful registration
      cy.waitForToast('Account created successfully');
      cy.url().should('include', '/dashboard');
      cy.getByTestId('user-menu').should('contain.text', newUser.name);
    });

    it('should validate password confirmation', () => {
      cy.getByTestId('register-link').click();
      
      cy.getByTestId('password-input').type('password123');
      cy.getByTestId('confirm-password-input').type('different123');
      cy.getByTestId('register-button').click();
      
      cy.getByTestId('confirm-password-error')
        .should('contain.text', 'Passwords must match');
    });

    it('should validate password strength', () => {
      cy.getByTestId('register-link').click();
      
      cy.getByTestId('password-input').type('weak');
      cy.getByTestId('password-error')
        .should('contain.text', 'Password must be at least 8 characters');
    });

    it('should require terms acceptance', () => {
      cy.getByTestId('register-link').click();
      
      cy.fillForm({
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123',
        'confirm-password': 'password123'
        // Don't check agree-terms
      });
      
      cy.getByTestId('register-button').click();
      
      cy.getByTestId('terms-error')
        .should('contain.text', 'You must agree to the terms');
    });
  });

  describe('Password Reset', () => {
    it('should send password reset email', () => {
      cy.getByTestId('login-link').click();
      cy.getByTestId('forgot-password-link').click();
      
      cy.url().should('include', '/forgot-password');
      
      cy.getByTestId('email-input').type('user@example.com');
      cy.getByTestId('reset-password-button').click();
      
      cy.waitForToast('Password reset email sent');
      cy.getByTestId('success-message')
        .should('contain.text', 'Check your email for reset instructions');
    });

    it('should reset password with valid token', () => {
      const resetToken = 'valid-reset-token';
      
      cy.visit(`/reset-password?token=${resetToken}`);
      
      cy.getByTestId('new-password-input').type('newpassword123');
      cy.getByTestId('confirm-password-input').type('newpassword123');
      cy.getByTestId('reset-password-button').click();
      
      cy.waitForToast('Password reset successfully');
      cy.url().should('include', '/login');
    });

    it('should handle invalid reset token', () => {
      cy.visit('/reset-password?token=invalid-token');
      
      cy.getByTestId('error-message')
        .should('contain.text', 'Invalid or expired reset token');
      
      cy.getByTestId('back-to-login-link').should('be.visible');
    });
  });
});
```

---

## 🚀 Advanced Testing Patterns

### 📚 Test Utilities and Helpers

**Interview Critical Point:** Creating reusable testing utilities for maintainable test suites.

```jsx
// src/test-utils/index.js
import React from 'react';
import { render, queries } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ThemeProvider } from '../contexts/ThemeContext';
import { AuthProvider } from '../contexts/AuthContext';
import * as customQueries from './custom-queries';

// Custom queries for better testing
const customRender = (
  ui,
  {
    route = '/',
    user = null,
    theme = 'light',
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false,
          cacheTime: 0,
        },
        mutations: {
          retry: false,
        },
      },
    }),
    ...renderOptions
  } = {}
) => {
  // Mock router state
  window.history.pushState({}, 'Test page', route);

  const AllTheProviders = ({ children }) => {
    return (
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <AuthProvider initialUser={user}>
            <ThemeProvider defaultTheme={theme}>
              {children}
            </ThemeProvider>
          </AuthProvider>
        </BrowserRouter>
      </QueryClientProvider>
    );
  };

  return render(ui, { 
    wrapper: AllTheProviders, 
    queries: { ...queries, ...customQueries },
    ...renderOptions 
  });
};

// Custom render for hook testing
export const renderHookWithProviders = (hook, options = {}) => {
  const { renderHook } = require('@testing-library/react');
  const { queryClient, user, theme, ...restOptions } = options;
  
  const wrapper = ({ children }) => {
    const client = queryClient || new QueryClient({
      defaultOptions: {
        queries: { retry: false, cacheTime: 0 },
        mutations: { retry: false },
      },
    });

    return (
      <QueryClientProvider client={client}>
        <BrowserRouter>
          <AuthProvider initialUser={user}>
            <ThemeProvider defaultTheme={theme}>
              {children}
            </ThemeProvider>
          </AuthProvider>
        </BrowserRouter>
      </QueryClientProvider>
    );
  };

  return renderHook(hook, { wrapper, ...restOptions });
};

// Factory functions for test data
export const createMockUser = (overrides = {}) => ({
  id: 1,
  email: 'test@example.com',
  name: 'Test User',
  role: 'user',
  preferences: {
    theme: 'light',
    language: 'en'
  },
  ...overrides
});

export const createMockPost = (overrides = {}) => ({
  id: Math.floor(Math.random() * 1000),
  title: 'Test Post',
  content: 'This is test content',
  author: 'Test Author',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  status: 'published',
  tags: ['test'],
  category: 'General',
  ...overrides
});

export const createMockPosts = (count = 10, overrides = {}) => 
  Array.from({ length: count }, (_, i) => 
    createMockPost({ 
      id: i + 1, 
      title: `Test Post ${i + 1}`,
      ...overrides 
    })
  );

// Wait utilities
export const waitForLoadingToFinish = () => 
  import('@testing-library/react').then(({ waitForElementToBeRemoved, screen }) => 
    waitForElementToBeRemoved(
      () => screen.queryByTestId('loading-spinner'),
      { timeout: 3000 }
    ).catch(() => {}) // Ignore if not found
  );

export const waitForErrorToAppear = () =>
  import('@testing-library/react').then(({ waitFor, screen }) =>
    waitFor(() => screen.getByTestId('error-message'))
  );

// Mock API response builders
export const createApiResponse = (data, status = 200) => ({
  status,
  ok: status >= 200 && status < 300,
  json: () => Promise.resolve(data),
  text: () => Promise.resolve(JSON.stringify(data)),
  headers: new Headers({
    'content-type': 'application/json',
  }),
});

export const createApiError = (message = 'API Error', status = 500) => ({
  status,
  ok: false,
  json: () => Promise.resolve({ error: message }),
  text: () => Promise.resolve(JSON.stringify({ error: message })),
  headers: new Headers({
    'content-type': 'application/json',
  }),
});

// Local Storage mock
export const mockLocalStorage = () => {
  const storage = {};
  
  return {
    getItem: jest.fn((key) => storage[key] || null),
    setItem: jest.fn((key, value) => {
      storage[key] = value;
    }),
    removeItem: jest.fn((key) => {
      delete storage[key];
    }),
    clear: jest.fn(() => {
      Object.keys(storage).forEach(key => delete storage[key]);
    }),
    get length() {
      return Object.keys(storage).length;
    },
    key: jest.fn((index) => Object.keys(storage)[index] || null)
  };
};

// Session Storage mock
export const mockSessionStorage = () => mockLocalStorage();

// IntersectionObserver mock
export const mockIntersectionObserver = () => {
  const mockIntersectionObserver = jest.fn();
  mockIntersectionObserver.mockReturnValue({
    observe: jest.fn(),
    unobserve: jest.fn(),
    disconnect: jest.fn(),
  });
  
  global.IntersectionObserver = mockIntersectionObserver;
  return mockIntersectionObserver;
};

// ResizeObserver mock
export const mockResizeObserver = () => {
  const mockResizeObserver = jest.fn();
  mockResizeObserver.mockReturnValue({
    observe: jest.fn(),
    unobserve: jest.fn(),
    disconnect: jest.fn(),
  });
  
  global.ResizeObserver = mockResizeObserver;
  return mockResizeObserver;
};

// Clipboard API mock
export const mockClipboard = () => {
  const mockClipboard = {
    writeText: jest.fn(() => Promise.resolve()),
    readText: jest.fn(() => Promise.resolve('')),
  };
  
  Object.defineProperty(navigator, 'clipboard', {
    value: mockClipboard,
    writable: true,
  });
  
  return mockClipboard;
};

// File API mock
export const createMockFile = (name = 'test.txt', content = 'test content', type = 'text/plain') => {
  const blob = new Blob([content], { type });
  blob.lastModifiedDate = new Date();
  blob.name = name;
  return blob;
};

// Custom matchers
export const customMatchers = {
  toHaveBeenCalledWithUser: (received, expectedUser) => {
    const pass = received.mock.calls.some(call => 
      call.some(arg => 
        arg && 
        typeof arg === 'object' && 
        arg.id === expectedUser.id &&
        arg.email === expectedUser.email
      )
    );

    return {
      pass,
      message: () => 
        pass 
          ? `Expected function not to have been called with user ${expectedUser.email}`
          : `Expected function to have been called with user ${expectedUser.email}`
    };
  },

  toHaveLoadingState: (received) => {
    const hasSpinner = received.querySelector('[data-testid="loading-spinner"]');
    const hasLoadingText = received.textContent.includes('Loading');
    const pass = hasSpinner || hasLoadingText;

    return {
      pass,
      message: () => 
        pass 
          ? 'Expected element not to have loading state'
          : 'Expected element to have loading state (spinner or loading text)'
    };
  },

  toHaveErrorState: (received, expectedError) => {
    const errorElement = received.querySelector('[data-testid="error-message"]');
    const pass = errorElement && (!expectedError || errorElement.textContent.includes(expectedError));

    return {
      pass,
      message: () => 
        pass 
          ? `Expected element not to have error state${expectedError ? ` with message "${expectedError}"` : ''}`
          : `Expected element to have error state${expectedError ? ` with message "${expectedError}"` : ''}`
    };
  }
};

// Re-export everything from React Testing Library
export * from '@testing-library/react';

// Override render method
export { customRender as render };
```

```jsx
// src/test-utils/custom-queries.js
import { queryHelpers, buildQueries } from '@testing-library/react';

// Custom query for finding elements by test id with timeout
const queryAllByTestIdWithTimeout = (container, testId, timeout = 1000) => {
  return new Promise((resolve) => {
    const startTime = Date.now();
    const checkForElement = () => {
      const elements = container.querySelectorAll(`[data-testid="${testId}"]`);
      if (elements.length > 0) {
        resolve(Array.from(elements));
      } else if (Date.now() - startTime < timeout) {
        setTimeout(checkForElement, 50);
      } else {
        resolve([]);
      }
    };
    checkForElement();
  });
};

const getMultipleError = (c, testId) => 
  `Found multiple elements with data-testid="${testId}"`;
const getMissingError = (c, testId) => 
  `Unable to find an element with data-testid="${testId}"`;

// Build queries
const [
  queryByTestIdWithTimeout,
  getAllByTestIdWithTimeout,
  getByTestIdWithTimeout,
  findAllByTestIdWithTimeout,
  findByTestIdWithTimeout
] = buildQueries(
  queryAllByTestIdWithTimeout,
  getMultipleError,
  getMissingError
);

// Custom query for finding form elements by label
const queryAllByLabelText = (container, text) => {
  const labels = Array.from(container.querySelectorAll('label'));
  return labels
    .filter(label => label.textContent.includes(text))
    .map(label => {
      const forAttr = label.getAttribute('for');
      if (forAttr) {
        return container.querySelector(`#${forAttr}`);
      }
      return label.querySelector('input, select, textarea');
    })
    .filter(Boolean);
};

const [
  queryByLabelText,
  getAllByLabelText,
  getByLabelText,
  findAllByLabelText,
  findByLabelText
] = buildQueries(
  queryAllByLabelText,
  (c, text) => `Found multiple elements with label text: ${text}`,
  (c, text) => `Unable to find an element with label text: ${text}`
);

// Custom query for finding elements by aria-label
const queryAllByAriaLabel = (container, label) => 
  Array.from(container.querySelectorAll(`[aria-label*="${label}"]`));

const [
  queryByAriaLabel,
  getAllByAriaLabel,
  getByAriaLabel,
  findAllByAriaLabel,
  findByAriaLabel
] = buildQueries(
  queryAllByAriaLabel,
  (c, label) => `Found multiple elements with aria-label containing: ${label}`,
  (c, label) => `Unable to find an element with aria-label containing: ${label}`
);

// Export all custom queries
export {
  queryByTestIdWithTimeout,
  getAllByTestIdWithTimeout,
  getByTestIdWithTimeout,
  findAllByTestIdWithTimeout,
  findByTestIdWithTimeout,
  
  queryByLabelText,
  getAllByLabelText,
  getByLabelText,
  findAllByLabelText,
  findByLabelText,
  
  queryByAriaLabel,
  getAllByAriaLabel,
  getByAriaLabel,
  findAllByAriaLabel,
  findByAriaLabel
};
```

### 🎯 Performance Testing

**Interview Critical Point:** Testing React application performance and rendering optimization.

```jsx
// src/test-utils/performance.js
export const measureComponentRenderTime = async (Component, props = {}) => {
  const { performance } = window;
  const startTime = performance.now();
  
  const { render } = await import('@testing-library/react');
  render(<Component {...props} />);
  
  const endTime = performance.now();
  return endTime - startTime;
};

export const measureReRenderTime = async (Component, initialProps, updatedProps) => {
  const { render } = await import('@testing-library/react');
  const { rerender } = render(<Component {...initialProps} />);
  
  const startTime = performance.now();
  rerender(<Component {...updatedProps} />);
  const endTime = performance.now();
  
  return endTime - startTime;
};

export const measureMemoryUsage = () => {
  if (performance.memory) {
    return {
      usedJSHeapSize: performance.memory.usedJSHeapSize,
      totalJSHeapSize: performance.memory.totalJSHeapSize,
      jsHeapSizeLimit: performance.memory.jsHeapSizeLimit
    };
  }
  return null;
};

export const createLargeDataset = (size = 1000) => 
  Array.from({ length: size }, (_, i) => ({
    id: i,
    title: `Item ${i}`,
    description: `Description for item ${i}`,
    data: Array.from({ length: 10 }, (_, j) => `data-${j}`)
  }));
```

```jsx
// components/__tests__/PostList.performance.test.jsx
import React from 'react';
import { render, screen } from '../../test-utils';
import { 
  measureComponentRenderTime, 
  measureReRenderTime,
  createLargeDataset 
} from '../../test-utils/performance';
import PostList from '../PostList/PostList';

describe('PostList Performance', () => {
  describe('Initial Render Performance', () => {
    it('should render small dataset quickly', async () => {
      const posts = createLargeDataset(10);
      const renderTime = await measureComponentRenderTime(PostList, { posts });
      
      expect(renderTime).toBeLessThan(50); // Should render in under 50ms
    });

    it('should handle medium dataset efficiently', async () => {
      const posts = createLargeDataset(100);
      const renderTime = await measureComponentRenderTime(PostList, { posts });
      
      expect(renderTime).toBeLessThan(200); // Should render in under 200ms
    });

    it('should virtualize large datasets', async () => {
      const posts = createLargeDataset(1000);
      
      render(<PostList posts={posts} virtualized />);
      
      // Should only render visible items
      const renderedItems = screen.getAllByTestId('post-item');
      expect(renderedItems.length).toBeLessThan(50); // Only visible items
      
      // All data should be available via scrolling
      expect(screen.getByText('1000 items total')).toBeInTheDocument();
    });
  });

  describe('Re-render Performance', () => {
    it('should re-render efficiently when props change', async () => {
      const initialPosts = createLargeDataset(50);
      const updatedPosts = [...initialPosts, ...createLargeDataset(10).map(p => ({ ...p, id: p.id + 50 }))];
      
      const reRenderTime = await measureReRenderTime(
        PostList,
        { posts: initialPosts },
        { posts: updatedPosts }
      );
      
      expect(reRenderTime).toBeLessThan(100); // Re-render should be fast
    });

    it('should use React.memo to prevent unnecessary re-renders', () => {
      const PostItem = jest.fn(({ post }) => <div>{post.title}</div>);
      const MemoizedPostItem = React.memo(PostItem);
      
      const posts = createLargeDataset(5);
      const { rerender } = render(
        <div>
          {posts.map(post => <MemoizedPostItem key={post.id} post={post} />)}
        </div>
      );
      
      PostItem.mockClear();
      
      // Re-render with same data
      rerender(
        <div>
          {posts.map(post => <MemoizedPostItem key={post.id} post={post} />)}
        </div>
      );
      
      expect(PostItem).not.toHaveBeenCalled(); // Should not re-render
    });

    it('should only re-render changed items', () => {
      const renderCounts = new Map();
      const TrackingPostItem = ({ post }) => {
        renderCounts.set(post.id, (renderCounts.get(post.id) || 0) + 1);
        return <div data-testid={`post-${post.id}`}>{post.title}</div>;
      };
      
      const MemoizedTrackingPostItem = React.memo(TrackingPostItem);
      
      const posts = createLargeDataset(5);
      const { rerender } = render(
        <div>
          {posts.map(post => 
            <MemoizedTrackingPostItem key={post.id} post={post} />
          )}
        </div>
      );
      
      // Clear render counts
      renderCounts.clear();
      
      // Update only one post
      const updatedPosts = posts.map(post => 
        post.id === 2 ? { ...post, title: 'Updated Title' } : post
      );
      
      rerender(
        <div>
          {updatedPosts.map(post => 
            <MemoizedTrackingPostItem key={post.id} post={post} />
          )}
        </div>
      );
      
      // Only the updated post should re-render
      expect(renderCounts.get(2)).toBe(1);
      expect(renderCounts.get(1)).toBeUndefined();
      expect(renderCounts.get(3)).toBeUndefined();
    });
  });

  describe('Memory Usage', () => {
    it('should not leak memory on unmount', () => {
      const posts = createLargeDataset(100);
      
      const { unmount } = render(<PostList posts={posts} />);
      
      // Force garbage collection if available
      if (global.gc) {
        global.gc();
      }
      
      const beforeUnmount = measureMemoryUsage();
      unmount();
      
      if (global.gc) {
        global.gc();
      }
      
      const afterUnmount = measureMemoryUsage();
      
      if (beforeUnmount && afterUnmount) {
        const memoryDiff = afterUnmount.usedJSHeapSize - beforeUnmount.usedJSHeapSize;
        expect(memoryDiff).toBeLessThan(1024 * 1024); // Less than 1MB difference
      }
    });

    it('should handle rapid mount/unmount cycles', () => {
      const posts = createLargeDataset(50);
      
      // Mount and unmount multiple times
      for (let i = 0; i < 10; i++) {
        const { unmount } = render(<PostList posts={posts} />);
        unmount();
      }
      
      // Should not crash or show memory warnings
      expect(true).toBe(true);
    });
  });

  describe('Scroll Performance', () => {
    it('should handle scroll events efficiently', async () => {
      const posts = createLargeDataset(1000);
      
      render(<PostList posts={posts} virtualized />);
      
      const scrollContainer = screen.getByTestId('scroll-container');
      
      // Measure scroll performance
      const startTime = performance.now();
      
      // Simulate multiple scroll events
      for (let i = 0; i < 100; i++) {
        fireEvent.scroll(scrollContainer, { target: { scrollTop: i * 10 } });
      }
      
      const endTime = performance.now();
      const scrollTime = endTime - startTime;
      
      expect(scrollTime).toBeLessThan(500); // Should handle scrolling smoothly
    });

    it('should throttle scroll events', () => {
      const onScroll = jest.fn();
      const posts = createLargeDataset(100);
      
      render(<PostList posts={posts} onScroll={onScroll} />);
      
      const scrollContainer = screen.getByTestId('scroll-container');
      
      // Fire many scroll events rapidly
      for (let i = 0; i < 100; i++) {
        fireEvent.scroll(scrollContainer, { target: { scrollTop: i } });
      }
      
      // Should be throttled to prevent excessive calls
      expect(onScroll).toHaveBeenCalledTimes(lessThan(50));
    });
  });

  describe('Bundle Size Impact', () => {
    it('should lazy load heavy components', async () => {
      const LazyHeavyComponent = React.lazy(() => 
        import('../HeavyComponent/HeavyComponent')
      );
      
      render(
        <React.Suspense fallback={<div>Loading...</div>}>
          <LazyHeavyComponent />
        </React.Suspense>
      );
      
      // Should show loading state initially
      expect(screen.getByText('Loading...')).toBeInTheDocument();
      
      // Should load the component
      await waitFor(() => {
        expect(screen.getByTestId('heavy-component')).toBeInTheDocument();
      });
    });

    it('should code-split by route', () => {
      // This would typically be tested with bundle analysis tools
      // but we can verify the lazy loading setup
      const routes = [
        React.lazy(() => import('../Dashboard/Dashboard')),
        React.lazy(() => import('../Posts/Posts')),
        React.lazy(() => import('../Profile/Profile'))
      ];
      
      routes.forEach(Component => {
        expect(Component).toBeDefined();
        expect(Component.$$typeof).toBe(Symbol.for('react.lazy'));
      });
    });
  });
});
```

---

## 🎯 Testing Best Practices & Interview Questions

### 📚 Senior-Level Interview Scenarios

#### Interview Question 1: "How would you test a complex form with dynamic fields and validation?"

```jsx
// Example Answer - Testing Dynamic Form
describe('Dynamic Form with Conditional Fields', () => {
  it('should show/hide fields based on form state', async () => {
    const user = userEvent.setup();
    render(<DynamicUserForm />);

    // Initially, advanced fields should be hidden
    expect(screen.queryByLabelText(/company/i)).not.toBeInTheDocument();
    
    // Select user type that shows company field
    await user.selectOptions(screen.getByLabelText(/user type/i), 'business');
    
    // Company field should now be visible
    expect(screen.getByLabelText(/company/i)).toBeInTheDocument();
    
    // Fill and validate the conditional field
    await user.type(screen.getByLabelText(/company/i), 'Test Corp');
    await user.tab(); // Trigger validation
    
    expect(screen.queryByText(/company name is required/i)).not.toBeInTheDocument();
  });

  it('should handle async validation correctly', async () => {
    const user = userEvent.setup();
    
    // Mock API for email validation
    server.use(
      rest.post('/api/validate-email', (req, res, ctx) => {
        const { email } = req.body;
        if (email === 'taken@example.com') {
          return res(ctx.status(400), ctx.json({ error: 'Email already exists' }));
        }
        return res(ctx.status(200), ctx.json({ valid: true }));
      })
    );

    render(<DynamicUserForm />);
    
    const emailInput = screen.getByLabelText(/email/i);
    await user.type(emailInput, 'taken@example.com');
    await user.tab();
    
    // Should show loading state during validation
    expect(screen.getByText(/validating/i)).toBeInTheDocument();
    
    // Should show error after validation
    await waitFor(() => {
      expect(screen.getByText(/email already exists/i)).toBeInTheDocument();
    });
  });
});
```

#### Interview Question 2: "How do you test data fetching with error recovery and retry logic?"

```jsx
// Example Answer - Testing Data Fetching with Retry
describe('Data Fetching with Retry Logic', () => {
  it('should retry failed requests and eventually succeed', async () => {
    let attemptCount = 0;
    
    server.use(
      rest.get('/api/posts', (req, res, ctx) => {
        attemptCount++;
        if (attemptCount < 3) {
          return res(ctx.status(500), ctx.json({ error: 'Server error' }));
        }
        return res(ctx.status(200), ctx.json({ posts: mockPosts }));
      })
    );

    render(<PostsWithRetry />);
    
    // Should show loading initially
    expect(screen.getByTestId('loading-spinner')).toBeInTheDocument();
    
    // Should show error after first failure
    await waitFor(() => {
      expect(screen.getByText(/failed to load/i)).toBeInTheDocument();
    });
    
    // Should show retry attempt
    expect(screen.getByText(/retrying/i)).toBeInTheDocument();
    
    // Should eventually succeed and show posts
    await waitFor(() => {
      expect(screen.getByTestId('posts-list')).toBeInTheDocument();
    });
    
    expect(attemptCount).toBe(3);
  });

  it('should respect maximum retry attempts', async () => {
    server.use(
      rest.get('/api/posts', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ error: 'Persistent error' }));
      })
    );

    render(<PostsWithRetry maxRetries={2} />);
    
    await waitFor(() => {
      expect(screen.getByText(/failed after 2 attempts/i)).toBeInTheDocument();
    });
    
    // Should show manual retry option
    expect(screen.getByRole('button', { name: /try again/i })).toBeInTheDocument();
  });
});
```

#### Interview Question 3: "How would you test a component that uses multiple React hooks and context?"

```jsx
// Example Answer - Testing Complex Hook Integration
describe('Component with Multiple Hooks and Context', () => {
  it('should handle complex state interactions correctly', async () => {
    const user = userEvent.setup();
    const mockUser = createMockUser({ role: 'admin' });
    
    render(
      <AdminDashboard />, 
      { 
        user: mockUser,
        route: '/admin/dashboard'
      }
    );

    // Test theme context integration
    expect(document.documentElement).toHaveAttribute('data-theme', 'light');
    
    await user.click(screen.getByTestId('theme-toggle'));
    expect(document.documentElement).toHaveAttribute('data-theme', 'dark');
    
    // Test auth context integration
    expect(screen.getByText(`Welcome, ${mockUser.name}`)).toBeInTheDocument();
    expect(screen.getByTestId('admin-panel')).toBeInTheDocument();
    
    // Test data fetching hook integration
    await waitFor(() => {
      expect(screen.getByTestId('dashboard-stats')).toBeInTheDocument();
    });
    
    // Test local state with useReducer
    await user.click(screen.getByTestId('add-widget-button'));
    expect(screen.getAllByTestId('dashboard-widget')).toHaveLength(4);
  });

  it('should handle context provider errors gracefully', () => {
    const ConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
    
    expect(() => {
      render(<AdminDashboard />); // No providers
    }).toThrow(/must be used within/i);
    
    ConsoleError.mockRestore();
  });
});
```

#### Interview Question 4: "How do you test performance-critical components with large datasets?"

```jsx
// Example Answer - Performance Testing Strategy
describe('Large Dataset Performance', () => {
  it('should virtualize large lists for performance', async () => {
    const largeDataset = createLargeDataset(10000);
    
    const startTime = performance.now();
    render(<VirtualizedList items={largeDataset} />);
    const renderTime = performance.now() - startTime;
    
    // Should render quickly despite large dataset
    expect(renderTime).toBeLessThan(100);
    
    // Should only render visible items
    const renderedItems = screen.getAllByTestId('list-item');
    expect(renderedItems.length).toBeLessThan(50);
    
    // Should maintain total count
    expect(screen.getByText('10,000 items')).toBeInTheDocument();
  });

  it('should handle scroll performance efficiently', async () => {
    const items = createLargeDataset(1000);
    render(<VirtualizedList items={items} />);
    
    const scrollContainer = screen.getByTestId('scroll-container');
    const scrollHandler = jest.fn();
    
    scrollContainer.addEventListener('scroll', scrollHandler);
    
    // Simulate rapid scrolling
    act(() => {
      for (let i = 0; i < 100; i++) {
        fireEvent.scroll(scrollContainer, { target: { scrollTop: i * 10 } });
      }
    });
    
    // Should throttle scroll events
    expect(scrollHandler).toHaveBeenCalledTimes(lessThan(20));
  });

  it('should memoize expensive calculations', () => {
    const expensiveCalculation = jest.fn((items) => {
      return items.reduce((sum, item) => sum + item.value, 0);
    });
    
    const MemoizedComponent = ({ items }) => {
      const total = useMemo(() => expensiveCalculation(items), [items]);
      return <div>Total: {total}</div>;
    };
    
    const items = [{ value: 1 }, { value: 2 }, { value: 3 }];
    const { rerender } = render(<MemoizedComponent items={items} />);
    
    expect(expensiveCalculation).toHaveBeenCalledTimes(1);
    
    // Re-render with same items
    rerender(<MemoizedComponent items={items} />);
    
    // Should not recalculate
    expect(expensiveCalculation).toHaveBeenCalledTimes(1);
    
    // Re-render with different items
    rerender(<MemoizedComponent items={[...items, { value: 4 }]} />);
    
    // Should recalculate
    expect(expensiveCalculation).toHaveBeenCalledTimes(2);
  });
});
```

### 📚 Testing Philosophy and Best Practices

**Interview Critical Points:**

1. **Test Pyramid Strategy**

   - **Unit Tests (70%)**: Fast, isolated, testing individual functions/components
   - **Integration Tests (20%)**: Testing component interactions, API integration
   - **E2E Tests (10%)**: Full user workflows, critical business paths

2. **What to Test vs What Not to Test**

   ```jsx
   // ✅ Test user behavior and outcomes
   it('should show success message after form submission', () => {
     // Test the user-visible result
   });
   
   // ❌ Don't test implementation details
   it('should call setState when button is clicked', () => {
     // Testing internal implementation
   });
   
   // ✅ Test error boundaries and edge cases
   it('should handle API errors gracefully', () => {
     // Test error handling
   });
   
   // ❌ Don't test third-party library internals
   it('should call axios.get with correct parameters', () => {
     // Testing library implementation
   });
   ```

3. **Test Organization Principles**

   ```jsx
   describe('ComponentName', () => {
     describe('Rendering', () => {
       // Test what renders under different conditions
     });
     
     describe('User Interactions', () => {
       // Test click, type, form submission
     });
     
     describe('Data Loading', () => {
       // Test loading states, success, errors
     });
     
     describe('Edge Cases', () => {
       // Test boundary conditions, error states
     });
     
     describe('Accessibility', () => {
       // Test ARIA, keyboard navigation, screen reader support
     });
   });
   ```

4. **Testing Anti-Patterns to Avoid**

   - Testing implementation details instead of behavior
   - Overmocking (mocking everything instead of testing real interactions)
   - Test pollution (tests affecting each other)
   - Testing libraries instead of your code
   - Snapshot testing without understanding what's being captured

5. **Senior Developer Testing Mindset**

   - Think like a user, not a developer
   - Test the happy path, error paths, and edge cases
   - Prefer integration tests over unit tests for UI components
   - Test accessibility as a first-class concern
   - Write tests that give confidence in deployments
   - Balance test coverage with maintenance cost

**Final Interview Wisdom:**
> "The best tests are those that catch real bugs, not just increase coverage numbers. Focus on testing user journeys and critical business logic. A well-tested application should allow you to refactor with confidence and deploy without fear."
