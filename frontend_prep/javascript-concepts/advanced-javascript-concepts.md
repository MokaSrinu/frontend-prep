# 🚀 Advanced JavaScript Concepts - Detailed Guide

> **Master the advanced building blocks of JavaScript with comprehensive explanations and practical examples**

---

## 📋 Table of Contents

1. [Event Loop & Concurrency](#1-event-loop--concurrency)
2. [Asynchronous Programming](#2-asynchronous-programming)
3. [Advanced Function Concepts](#3-advanced-function-concepts)
4. [Modules & Code Organization](#4-modules--code-organization)
5. [Generators & Iterators](#5-generators--iterators)
6. [Functional Programming](#6-functional-programming)

---

## 1. Event Loop & Concurrency

> **Interview Explanation:** The Event Loop is JavaScript's mechanism for handling asynchronous operations in a single-threaded environment. Understanding this is crucial for explaining how JavaScript can be non-blocking despite being single-threaded.

### 🎯 Call Stack

> **Interview Key Point:** The call stack is where JavaScript tracks function execution. It's a LIFO (Last In, First Out) structure that manages execution contexts.

```javascript
// Call stack visualization
function first() {
    console.log("First function start");
    second();
    console.log("First function end");
}

function second() {
    console.log("Second function start");
    third();
    console.log("Second function end");
}

function third() {
    console.log("Third function");
}

first();

/*
Call Stack Execution:
1. first() pushed to stack
2. second() pushed to stack
3. third() pushed to stack
4. third() executes and pops
5. second() continues and pops
6. first() continues and pops

Output:
First function start
Second function start
Third function
Second function end
First function end
*/

// Stack overflow example
function recursiveFunction(count = 0) {
    console.log(`Call ${count}`);
    if (count < 10000) {
        recursiveFunction(count + 1); // Will eventually cause stack overflow
    }
}

// recursiveFunction(); // RangeError: Maximum call stack size exceeded
```

### 🎯 Web APIs / Node.js APIs

> **Interview Explanation:** Web APIs (in browsers) or Node.js APIs provide asynchronous capabilities like timers, HTTP requests, and file operations. These run outside the main JavaScript thread.

```javascript
// Web APIs examples
console.log("Start");

// setTimeout - Web API
setTimeout(() => {
    console.log("Timer completed");
}, 1000);

// DOM API
document.addEventListener('click', () => {
    console.log("Document clicked");
});

// Fetch API
fetch('https://api.example.com/data')
    .then(response => response.json())
    .then(data => console.log(data));

console.log("End");

// The APIs handle these operations asynchronously
// while JavaScript continues executing synchronously
```

### 🎯 Task Queue vs Microtask Queue

> **Interview Explanation:** There are two queues: Task Queue (macrotasks) for setTimeout, setInterval, and DOM events; Microtask Queue for Promises, queueMicrotask, and async/await. Microtasks have higher priority.

```javascript
// Queue priority demonstration
console.log("1"); // Synchronous

setTimeout(() => console.log("2"), 0); // Task Queue (macrotask)

Promise.resolve().then(() => console.log("3")); // Microtask Queue

queueMicrotask(() => console.log("4")); // Microtask Queue

setTimeout(() => console.log("5"), 0); // Task Queue (macrotask)

Promise.resolve().then(() => {
    console.log("6"); // Microtask
    return Promise.resolve();
}).then(() => console.log("7")); // Chained microtask

console.log("8"); // Synchronous

/*
Output: 1, 8, 3, 4, 6, 7, 2, 5

Execution order:
1. Synchronous code: 1, 8
2. All microtasks: 3, 4, 6, 7
3. First macrotask: 2
4. Check microtasks (none)
5. Next macrotask: 5
*/

// Complex example
function complexEventLoop() {
    console.log("Start");
    
    setTimeout(() => {
        console.log("Timeout 1");
        Promise.resolve().then(() => console.log("Promise in timeout 1"));
    }, 0);
    
    Promise.resolve().then(() => {
        console.log("Promise 1");
        setTimeout(() => console.log("Timeout in promise 1"), 0);
    });
    
    setTimeout(() => {
        console.log("Timeout 2");
    }, 0);
    
    Promise.resolve().then(() => console.log("Promise 2"));
    
    console.log("End");
}

complexEventLoop();
/*
Output:
Start
End
Promise 1
Promise 2
Timeout 1
Promise in timeout 1
Timeout in promise 1
Timeout 2
*/
```

### 🎯 Event Loop Phases

> **Interview Explanation:** The event loop has specific phases: Check call stack → Execute microtasks → Execute one macrotask → Repeat. This ensures predictable execution order.

```javascript
// Event loop phases demonstration
function demonstrateEventLoop() {
    // Phase 1: Execute synchronous code
    console.log("=== Synchronous Phase ===");
    console.log("Sync 1");
    console.log("Sync 2");
    
    // Phase 2: Schedule macrotasks
    setTimeout(() => console.log("Macrotask 1"), 0);
    setTimeout(() => console.log("Macrotask 2"), 0);
    
    // Phase 3: Schedule microtasks
    Promise.resolve().then(() => console.log("Microtask 1"));
    Promise.resolve().then(() => console.log("Microtask 2"));
    
    // More synchronous code
    console.log("Sync 3");
    
    // Nested scheduling
    Promise.resolve().then(() => {
        console.log("Microtask 3");
        setTimeout(() => console.log("Nested Macrotask"), 0);
        return Promise.resolve();
    }).then(() => console.log("Microtask 4"));
}

demonstrateEventLoop();

// Event loop visualization helper
function visualizeEventLoop() {
    const phases = [];
    
    console.log("📍 Phase 1: Call Stack Execution");
    phases.push("Call Stack: Synchronous code");
    
    setTimeout(() => {
        console.log("📍 Phase 3: Macrotask Execution");
        phases.push("Macrotask: setTimeout callback");
    }, 0);
    
    Promise.resolve().then(() => {
        console.log("📍 Phase 2: Microtask Execution");
        phases.push("Microtask: Promise.then callback");
    });
    
    console.log("Call Stack continues...");
}
```

---

## 2. Asynchronous Programming

> **Interview Explanation:** Asynchronous programming allows JavaScript to handle operations that take time (like API calls) without blocking the main thread. It evolved from callbacks to Promises to async/await.

### 🎯 Callbacks & Callback Hell

> **Interview Key Point:** Callbacks are functions passed as arguments to be executed later. Callback hell occurs when multiple nested callbacks make code hard to read and maintain.

```javascript
// Simple callback example
function fetchData(callback) {
    setTimeout(() => {
        const data = { id: 1, name: "User" };
        callback(null, data); // Node.js convention: error first, then data
    }, 1000);
}

function handleData(error, data) {
    if (error) {
        console.error("Error:", error);
    } else {
        console.log("Data received:", data);
    }
}

fetchData(handleData);

// Callback hell example
function callbackHell() {
    // Simulating nested API calls
    fetchUser(1, (userError, user) => {
        if (userError) {
            console.error("User fetch error:", userError);
            return;
        }
        
        fetchUserPosts(user.id, (postsError, posts) => {
            if (postsError) {
                console.error("Posts fetch error:", postsError);
                return;
            }
            
            fetchPostComments(posts[0].id, (commentsError, comments) => {
                if (commentsError) {
                    console.error("Comments fetch error:", commentsError);
                    return;
                }
                
                fetchCommentReplies(comments[0].id, (repliesError, replies) => {
                    if (repliesError) {
                        console.error("Replies fetch error:", repliesError);
                        return;
                    }
                    
                    // Finally got all data - but look at this nesting!
                    console.log("All data:", { user, posts, comments, replies });
                });
            });
        });
    });
}

// Callback implementation helpers
function fetchUser(id, callback) {
    setTimeout(() => {
        callback(null, { id, name: `User ${id}` });
    }, 100);
}

function fetchUserPosts(userId, callback) {
    setTimeout(() => {
        callback(null, [{ id: 1, userId, title: "Post 1" }]);
    }, 100);
}

function fetchPostComments(postId, callback) {
    setTimeout(() => {
        callback(null, [{ id: 1, postId, text: "Comment 1" }]);
    }, 100);
}

function fetchCommentReplies(commentId, callback) {
    setTimeout(() => {
        callback(null, [{ id: 1, commentId, text: "Reply 1" }]);
    }, 100);
}
```

### 🎯 Promises

> **Interview Explanation:** Promises represent eventual completion or failure of an asynchronous operation. They have three states: pending, fulfilled, or rejected. They solve callback hell through chaining.

```javascript
// Promise creation and basic usage
function createPromise() {
    return new Promise((resolve, reject) => {
        const success = Math.random() > 0.5;
        
        setTimeout(() => {
            if (success) {
                resolve("Operation successful!");
            } else {
                reject(new Error("Operation failed!"));
            }
        }, 1000);
    });
}

// Promise consumption
createPromise()
    .then(result => {
        console.log("Success:", result);
        return "Modified result";
    })
    .then(modifiedResult => {
        console.log("Modified:", modifiedResult);
    })
    .catch(error => {
        console.error("Error:", error.message);
    })
    .finally(() => {
        console.log("Promise completed");
    });

// Promise chaining to solve callback hell
function promisifyFetch(id) {
    return new Promise(resolve => {
        setTimeout(() => resolve({ id, name: `Item ${id}` }), 100);
    });
}

function solvingCallbackHell() {
    promisifyFetch(1)
        .then(user => {
            console.log("User:", user);
            return promisifyFetch(user.id + 10); // Return promise for chaining
        })
        .then(posts => {
            console.log("Posts:", posts);
            return promisifyFetch(posts.id + 10);
        })
        .then(comments => {
            console.log("Comments:", comments);
            return promisifyFetch(comments.id + 10);
        })
        .then(replies => {
            console.log("Replies:", replies);
        })
        .catch(error => {
            console.error("Any step failed:", error);
        });
}

// Promise states demonstration
function demonstratePromiseStates() {
    // Pending promise
    const pendingPromise = new Promise(resolve => {
        // Never resolves - stays pending
    });
    console.log("Pending promise:", pendingPromise);
    
    // Fulfilled promise
    const fulfilledPromise = Promise.resolve("Fulfilled value");
    console.log("Fulfilled promise:", fulfilledPromise);
    
    // Rejected promise
    const rejectedPromise = Promise.reject(new Error("Rejected reason"));
    console.log("Rejected promise:", rejectedPromise);
    
    // Catching rejected promise to prevent unhandled rejection
    rejectedPromise.catch(error => console.log("Caught:", error.message));
}
```

### 🎯 Promise Combinators

> **Interview Explanation:** Promise combinators allow handling multiple promises simultaneously. Each has different behavior: `all` fails fast, `allSettled` waits for all, `race` returns first completed, `any` returns first fulfilled.

```javascript
// Promise.all - Fails fast, succeeds when all succeed
function demonstratePromiseAll() {
    const promises = [
        Promise.resolve("Result 1"),
        Promise.resolve("Result 2"),
        Promise.resolve("Result 3")
    ];
    
    Promise.all(promises)
        .then(results => {
            console.log("Promise.all results:", results);
            // ["Result 1", "Result 2", "Result 3"]
        });
    
    // With one rejection
    const mixedPromises = [
        Promise.resolve("Success 1"),
        Promise.reject(new Error("Failed")),
        Promise.resolve("Success 2")
    ];
    
    Promise.all(mixedPromises)
        .then(results => {
            console.log("Won't reach here");
        })
        .catch(error => {
            console.log("Promise.all failed:", error.message);
            // Fails immediately when any promise rejects
        });
}

// Promise.allSettled - Waits for all regardless of outcome
function demonstratePromiseAllSettled() {
    const promises = [
        Promise.resolve("Success 1"),
        Promise.reject(new Error("Failed")),
        Promise.resolve("Success 2"),
        Promise.reject(new Error("Failed 2"))
    ];
    
    Promise.allSettled(promises)
        .then(results => {
            console.log("Promise.allSettled results:");
            results.forEach((result, index) => {
                if (result.status === 'fulfilled') {
                    console.log(`Promise ${index}: Fulfilled with ${result.value}`);
                } else {
                    console.log(`Promise ${index}: Rejected with ${result.reason.message}`);
                }
            });
        });
}

// Promise.race - Returns first completed (fulfilled or rejected)
function demonstratePromiseRace() {
    const promises = [
        new Promise(resolve => setTimeout(() => resolve("Slow result"), 2000)),
        new Promise(resolve => setTimeout(() => resolve("Fast result"), 500)),
        new Promise((_, reject) => setTimeout(() => reject(new Error("Error")), 1000))
    ];
    
    Promise.race(promises)
        .then(result => {
            console.log("Promise.race winner:", result);
            // "Fast result" - first to complete
        })
        .catch(error => {
            console.log("Promise.race error:", error.message);
        });
}

// Promise.any - Returns first fulfilled (ignores rejections until all reject)
function demonstratePromiseAny() {
    const promises = [
        Promise.reject(new Error("Failed 1")),
        Promise.reject(new Error("Failed 2")),
        Promise.resolve("Success!"),
        Promise.resolve("Another success")
    ];
    
    Promise.any(promises)
        .then(result => {
            console.log("Promise.any result:", result);
            // "Success!" - first fulfilled promise
        })
        .catch(error => {
            console.log("All promises rejected:", error);
        });
    
    // All rejections case
    const allFailures = [
        Promise.reject(new Error("Failed 1")),
        Promise.reject(new Error("Failed 2")),
        Promise.reject(new Error("Failed 3"))
    ];
    
    Promise.any(allFailures)
        .catch(error => {
            console.log("Promise.any - all failed:", error.name);
            // AggregateError: All promises were rejected
        });
}

// Practical example: Timeout pattern
function createTimeoutPromise(promise, timeout) {
    const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error("Operation timed out")), timeout);
    });
    
    return Promise.race([promise, timeoutPromise]);
}

function demonstrateTimeout() {
    const slowOperation = new Promise(resolve => {
        setTimeout(() => resolve("Operation completed"), 3000);
    });
    
    createTimeoutPromise(slowOperation, 2000)
        .then(result => console.log(result))
        .catch(error => console.log(error.message)); // "Operation timed out"
}
```

### 🎯 async/await

> **Interview Explanation:** async/await is syntactic sugar over Promises that makes asynchronous code look and behave more like synchronous code. It's easier to read and debug than Promise chains.

```javascript
// Basic async/await usage
async function basicAsyncAwait() {
    try {
        console.log("Starting async operation");
        
        const result = await createPromise(); // Wait for promise to resolve
        console.log("Result:", result);
        
        const secondResult = await promisifyFetch(2);
        console.log("Second result:", secondResult);
        
        return "All operations completed";
    } catch (error) {
        console.error("Error in async function:", error.message);
        throw error; // Re-throw if needed
    }
}

// Async function always returns a Promise
basicAsyncAwait()
    .then(result => console.log("Final:", result))
    .catch(error => console.log("Caught outside:", error.message));

// Converting callback hell to async/await
async function cleanAsyncCode() {
    try {
        const user = await promisifyFetch(1);
        console.log("User:", user);
        
        const posts = await promisifyFetch(user.id + 10);
        console.log("Posts:", posts);
        
        const comments = await promisifyFetch(posts.id + 10);
        console.log("Comments:", comments);
        
        const replies = await promisifyFetch(comments.id + 10);
        console.log("Replies:", replies);
        
        return { user, posts, comments, replies };
    } catch (error) {
        console.error("Error in any step:", error);
        throw error;
    }
}

// Parallel vs Sequential execution
async function sequentialExecution() {
    console.time("Sequential");
    
    const result1 = await promisifyFetch(1); // Wait 100ms
    const result2 = await promisifyFetch(2); // Wait another 100ms
    const result3 = await promisifyFetch(3); // Wait another 100ms
    
    console.timeEnd("Sequential"); // ~300ms total
    return [result1, result2, result3];
}

async function parallelExecution() {
    console.time("Parallel");
    
    // Start all promises simultaneously
    const promise1 = promisifyFetch(1);
    const promise2 = promisifyFetch(2);
    const promise3 = promisifyFetch(3);
    
    // Wait for all to complete
    const results = await Promise.all([promise1, promise2, promise3]);
    
    console.timeEnd("Parallel"); // ~100ms total
    return results;
}

// Error handling patterns
async function errorHandlingPatterns() {
    // Pattern 1: Try-catch for entire function
    try {
        const result1 = await promisifyFetch(1);
        const result2 = await promisifyFetch(2);
        return [result1, result2];
    } catch (error) {
        console.error("Error in entire operation:", error);
        return null;
    }
}

async function individualErrorHandling() {
    let result1, result2;
    
    // Pattern 2: Individual error handling
    try {
        result1 = await promisifyFetch(1);
    } catch (error) {
        console.error("Error fetching result1:", error);
        result1 = { default: true };
    }
    
    try {
        result2 = await promisifyFetch(2);
    } catch (error) {
        console.error("Error fetching result2:", error);
        result2 = { default: true };
    }
    
    return [result1, result2];
}

// Async/await with Promise combinators
async function combiningAsyncAwaitWithCombinators() {
    try {
        // Using Promise.all with async/await
        const [user, settings, preferences] = await Promise.all([
            promisifyFetch(1),
            promisifyFetch(2),
            promisifyFetch(3)
        ]);
        
        console.log("All data loaded:", { user, settings, preferences });
        
        // Using Promise.allSettled
        const results = await Promise.allSettled([
            promisifyFetch(4),
            Promise.reject(new Error("Intentional error")),
            promisifyFetch(5)
        ]);
        
        console.log("All settled results:", results);
        
    } catch (error) {
        console.error("Error:", error);
    }
}

// Async generators (advanced)
async function* asyncGenerator() {
    for (let i = 1; i <= 3; i++) {
        const result = await promisifyFetch(i);
        yield result;
    }
}

async function useAsyncGenerator() {
    for await (const result of asyncGenerator()) {
        console.log("Generated:", result);
    }
}
```

---

## 3. Advanced Function Concepts

> **Interview Explanation:** Advanced function concepts include understanding `this` binding, function manipulation techniques like currying, and functional programming patterns. These are essential for writing sophisticated JavaScript code.

### 🎯 `this` Binding Rules

> **Interview Key Point:** `this` binding depends on how a function is called, not where it's defined. There are four rules: default, implicit, explicit, and arrow function binding.

```javascript
// Rule 1: Default Binding
function defaultBinding() {
    console.log(this); // Global object (window/global) or undefined in strict mode
}

defaultBinding(); // Global context

"use strict";
function strictModeDefault() {
    console.log(this); // undefined in strict mode
}

// Rule 2: Implicit Binding
const obj = {
    name: "Alice",
    greet: function() {
        console.log(`Hello, ${this.name}`); // this = obj
    },
    
    nested: {
        name: "Bob",
        greet: function() {
            console.log(`Hello, ${this.name}`); // this = nested object
        }
    }
};

obj.greet(); // "Hello, Alice"
obj.nested.greet(); // "Hello, Bob"

// Implicit binding loss
const greetFunction = obj.greet;
greetFunction(); // "Hello, undefined" - lost context

// Rule 3: Explicit Binding (call, apply, bind)
function introduce(age, city) {
    console.log(`Hi, I'm ${this.name}, ${age} years old from ${city}`);
}

const person1 = { name: "Alice" };
const person2 = { name: "Bob" };

// call - immediate invocation
introduce.call(person1, 25, "New York");
introduce.call(person2, 30, "London");

// apply - array of arguments
introduce.apply(person1, [25, "New York"]);
introduce.apply(person2, [30, "London"]);

// bind - returns new function
const boundIntroduce = introduce.bind(person1);
boundIntroduce(25, "New York");

const boundWithArgs = introduce.bind(person1, 25);
boundWithArgs("New York");

// Rule 4: Arrow Function Binding (Lexical this)
const arrowObj = {
    name: "Charlie",
    
    regularMethod: function() {
        console.log("Regular method this:", this.name);
        
        // Arrow function inherits this from enclosing scope
        const innerArrow = () => {
            console.log("Arrow function this:", this.name);
        };
        
        // Regular function gets its own this
        const innerRegular = function() {
            console.log("Inner regular this:", this.name);
        };
        
        innerArrow(); // "Charlie" - inherits from regularMethod
        innerRegular(); // undefined - new this context
        
        // Demonstrating with setTimeout
        setTimeout(() => {
            console.log("Arrow in setTimeout:", this.name); // "Charlie"
        }, 100);
        
        setTimeout(function() {
            console.log("Regular in setTimeout:", this.name); // undefined
        }, 100);
    },
    
    arrowMethod: () => {
        console.log("Arrow method this:", this.name); // undefined - inherits from global
    }
};

arrowObj.regularMethod();
arrowObj.arrowMethod();

// Practical this binding examples
class EventHandler {
    constructor(name) {
        this.name = name;
        this.clickCount = 0;
    }
    
    // Method that needs proper this binding
    handleClick() {
        this.clickCount++;
        console.log(`${this.name} clicked ${this.clickCount} times`);
    }
    
    // Incorrect way - this binding will be lost
    setupIncorrect() {
        document.addEventListener('click', this.handleClick); // Wrong!
    }
    
    // Correct ways to maintain this binding
    setupWithBind() {
        document.addEventListener('click', this.handleClick.bind(this));
    }
    
    setupWithArrow() {
        document.addEventListener('click', () => this.handleClick());
    }
    
    // Arrow method automatically binds
    handleClickArrow = () => {
        this.clickCount++;
        console.log(`${this.name} clicked ${this.clickCount} times`);
    }
}

// this in different contexts
const thisExamples = {
    // Object method
    objectMethod: function() {
        return this; // Returns the object
    },
    
    // Arrow function in object
    arrowInObject: () => {
        return this; // Returns global/window object
    },
    
    // Method that returns arrow function
    methodReturningArrow: function() {
        return () => this; // Arrow inherits this from method
    },
    
    // Nested functions
    nestedFunctions: function() {
        function inner() {
            return this; // Global object or undefined (strict mode)
        }
        
        const innerArrow = () => this; // Inherits this from nestedFunctions
        
        return {
            inner: inner(),
            innerArrow: innerArrow()
        };
    }
};
```

### 🎯 Currying

> **Interview Explanation:** Currying transforms a function that takes multiple arguments into a sequence of functions that each take a single argument. It enables partial application and function reuse.

```javascript
// Basic currying example
function add(a) {
    return function(b) {
        return function(c) {
            return a + b + c;
        };
    };
}

const result = add(1)(2)(3); // 6

// ES6 arrow function currying
const addArrow = a => b => c => a + b + c;
const result2 = addArrow(1)(2)(3); // 6

// Practical currying - configuration functions
function createAPIRequest(baseURL) {
    return function(endpoint) {
        return function(method) {
            return function(data) {
                return {
                    url: `${baseURL}${endpoint}`,
                    method: method,
                    data: data
                };
            };
        };
    };
}

// Usage
const apiRequest = createAPIRequest('https://api.example.com');
const userAPI = apiRequest('/users');
const getUsersGET = userAPI('GET');
const createUserPOST = userAPI('POST');

console.log(getUsersGET(null)); // GET request to /users
console.log(createUserPOST({ name: 'Alice' })); // POST request with data

// Generic curry function
function curry(fn) {
    return function curried(...args) {
        if (args.length >= fn.length) {
            return fn.apply(this, args);
        } else {
            return function(...nextArgs) {
                return curried.apply(this, args.concat(nextArgs));
            };
        }
    };
}

// Example with curry utility
function multiply(a, b, c) {
    return a * b * c;
}

const curriedMultiply = curry(multiply);

console.log(curriedMultiply(2)(3)(4)); // 24
console.log(curriedMultiply(2, 3)(4)); // 24
console.log(curriedMultiply(2)(3, 4)); // 24
console.log(curriedMultiply(2, 3, 4)); // 24

// Practical currying examples
const curriedFilter = curry((predicate, array) => array.filter(predicate));
const curriedMap = curry((fn, array) => array.map(fn));

const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Reusable predicates
const isEven = n => n % 2 === 0;
const isGreaterThan5 = n => n > 5;

// Reusable transformations
const double = n => n * 2;
const square = n => n * n;

// Create specialized functions
const filterEvens = curriedFilter(isEven);
const filterGreaterThan5 = curriedFilter(isGreaterThan5);
const mapDouble = curriedMap(double);
const mapSquare = curriedMap(square);

console.log(filterEvens(numbers)); // [2, 4, 6, 8, 10]
console.log(mapDouble(numbers)); // [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

// Function composition with currying
const compose = (f, g) => x => f(g(x));

const addTax = curry((rate, price) => price * (1 + rate));
const addShipping = curry((cost, price) => price + cost);

const calculateTotal = compose(
    addShipping(10),
    addTax(0.08)
);

console.log(calculateTotal(100)); // 118 (100 * 1.08 + 10)
```

### 🎯 Partial Application

> **Interview Explanation:** Partial application is the process of fixing a number of arguments to a function, producing another function with fewer arguments. It's similar to currying but more flexible.

```javascript
// Basic partial application
function partial(fn, ...argsToApply) {
    return function(...remainingArgs) {
        return fn(...argsToApply, ...remainingArgs);
    };
}

function greetPerson(greeting, title, firstName, lastName) {
    return `${greeting}, ${title} ${firstName} ${lastName}!`;
}

// Create specialized greeting functions
const sayHello = partial(greetPerson, "Hello");
const sayGoodMorning = partial(greetPerson, "Good morning");
const sayHelloMr = partial(greetPerson, "Hello", "Mr.");

console.log(sayHello("Dr.", "John", "Doe")); // "Hello, Dr. John Doe!"
console.log(sayGoodMorning("Ms.", "Jane", "Smith")); // "Good morning, Ms. Jane Smith!"
console.log(sayHelloMr("Bob", "Johnson")); // "Hello, Mr. Bob Johnson!"

// Practical example: Event handling
function handleEvent(eventType, selector, callback) {
    document.addEventListener(eventType, function(event) {
        if (event.target.matches(selector)) {
            callback(event);
        }
    });
}

// Create specialized event handlers
const handleClick = partial(handleEvent, 'click');
const handleButtonClick = partial(handleEvent, 'click', 'button');
const handleLinkHover = partial(handleEvent, 'mouseover', 'a');

// Usage
handleButtonClick(function(event) {
    console.log('Button clicked:', event.target.textContent);
});

// Partial application with bind
function multiply(a, b, c) {
    return a * b * c;
}

const double = multiply.bind(null, 2); // Partially apply first argument
const tripleByFour = multiply.bind(null, 3, 4); // Partially apply first two

console.log(double(5, 6)); // 60 (2 * 5 * 6)
console.log(tripleByFour(7)); // 84 (3 * 4 * 7)

// Advanced partial application - positional arguments
function partialAny(fn, ...args) {
    return function(...remainingArgs) {
        const finalArgs = [];
        let remainingIndex = 0;
        
        for (let i = 0; i < args.length; i++) {
            if (args[i] === partialAny.PLACEHOLDER) {
                finalArgs[i] = remainingArgs[remainingIndex++];
            } else {
                finalArgs[i] = args[i];
            }
        }
        
        // Add any remaining arguments
        finalArgs.push(...remainingArgs.slice(remainingIndex));
        
        return fn(...finalArgs);
    };
}

partialAny.PLACEHOLDER = Symbol('placeholder');
const _ = partialAny.PLACEHOLDER;

function subtract(a, b, c) {
    return a - b - c;
}

const subtractFromTen = partialAny(subtract, 10, _, _);
const subtractFiveFrom = partialAny(subtract, _, 5, _);

console.log(subtractFromTen(3, 2)); // 5 (10 - 3 - 2)
console.log(subtractFiveFrom(20, 8)); // 7 (20 - 5 - 8)
```

### 🎯 Function Composition

> **Interview Explanation:** Function composition is combining two or more functions to produce a new function. It follows mathematical composition where (f ∘ g)(x) = f(g(x)).

```javascript
// Basic function composition
const compose = (f, g) => x => f(g(x));

// Simple functions
const addOne = x => x + 1;
const double = x => x * 2;
const square = x => x * x;

// Compose functions
const addOneThenDouble = compose(double, addOne);
const doubleThenSquare = compose(square, double);

console.log(addOneThenDouble(5)); // 12 ((5 + 1) * 2)
console.log(doubleThenSquare(3)); // 36 ((3 * 2) ^ 2)

// Multi-function composition
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x);
const composeMany = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);

// Data transformation pipeline
const data = [1, 2, 3, 4, 5];

const transformData = pipe(
    arr => arr.filter(x => x % 2 === 0), // Filter evens
    arr => arr.map(x => x * 3),          // Multiply by 3
    arr => arr.reduce((sum, x) => sum + x, 0) // Sum all
);

console.log(transformData(data)); // 18 ([2, 4] -> [6, 12] -> 18)

// Practical composition example
const trim = str => str.trim();
const toLowerCase = str => str.toLowerCase();
const removeSpaces = str => str.replace(/\s+/g, '');
const capitalize = str => str.charAt(0).toUpperCase() + str.slice(1);

// Create composed functions for different use cases
const normalizeText = pipe(trim, toLowerCase);
const createSlug = pipe(trim, toLowerCase, removeSpaces);
const formatName = pipe(trim, toLowerCase, capitalize);

console.log(normalizeText("  Hello World  ")); // "hello world"
console.log(createSlug("  Hello World  ")); // "helloworld"
console.log(formatName("  alice  ")); // "Alice"

// Async function composition
const composeAsync = (...fns) => x => 
    fns.reduce(async (acc, fn) => fn(await acc), Promise.resolve(x));

const asyncAdd = x => Promise.resolve(x + 1);
const asyncMultiply = x => Promise.resolve(x * 2);
const asyncSquare = x => Promise.resolve(x * x);

const asyncTransform = composeAsync(asyncSquare, asyncMultiply, asyncAdd);

asyncTransform(3)
    .then(result => console.log(result)); // 64 ((3 + 1) * 2)^2

// Point-free style programming
const isEven = x => x % 2 === 0;
const isPositive = x => x > 0;

// Without composition (not point-free)
const filterEvenPositive = arr => arr.filter(x => isEven(x) && isPositive(x));

// With composition (point-free style)
const and = (f, g) => x => f(x) && g(x);
const filter = predicate => arr => arr.filter(predicate);

const filterEvenPositiveComposed = filter(and(isEven, isPositive));

const numbers = [-2, -1, 0, 1, 2, 3, 4, 5];
console.log(filterEvenPositiveComposed(numbers)); // [2, 4]

// Memoization with composition
function memoize(fn) {
    const cache = new Map();
    return function(...args) {
        const key = JSON.stringify(args);
        if (cache.has(key)) {
            return cache.get(key);
        }
        const result = fn(...args);
        cache.set(key, result);
        return result;
    };
}

// Expensive function
const fibonacci = n => {
    if (n <= 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
};

const memoizedFibonacci = memoize(fibonacci);

// Compose with memoization
const enhancedFibonacci = compose(
    x => `Result: ${x}`,
    memoizedFibonacci
);

console.time('First call');
console.log(enhancedFibonacci(40));
console.timeEnd('First call');

console.time('Second call');
console.log(enhancedFibonacci(40)); // Much faster due to memoization
console.timeEnd('Second call');
```

---

*[Continue with remaining sections: Modules & Code Organization, Generators & Iterators, and Functional Programming]*

## 4. Modules & Code Organization

> **Interview Explanation:** Modules are reusable pieces of code that encapsulate functionality and expose only what's necessary. JavaScript evolved from no native modules to CommonJS (Node.js) to ES Modules (modern standard).

### 🎯 CommonJS vs ES Modules

> **Interview Key Point:** CommonJS uses `require()/module.exports` (synchronous, Node.js), while ES Modules use `import/export` (asynchronous, browser and modern Node.js). ES Modules are statically analyzable and support tree shaking.

```javascript
// CommonJS (Node.js)
// math.js
function add(a, b) {
    return a + b;
}

function multiply(a, b) {
    return a * b;
}

// Exporting in CommonJS
module.exports = {
    add,
    multiply
};

// Alternative CommonJS export
exports.subtract = (a, b) => a - b;

// main.js
const { add, multiply } = require('./math');
const math = require('./math');

console.log(add(2, 3)); // 5
console.log(math.multiply(4, 5)); // 20

// ES Modules (Modern JavaScript)
// math.mjs or math.js (with "type": "module" in package.json)

// Named exports
export function add(a, b) {
    return a + b;
}

export const multiply = (a, b) => a * b;

// Export after declaration
function subtract(a, b) {
    return a - b;
}

export { subtract };

// Default export
export default function divide(a, b) {
    return a / b;
}

// main.mjs
import divide, { add, multiply, subtract } from './math.mjs';
import * as math from './math.mjs';

console.log(add(2, 3)); // 5
console.log(divide(10, 2)); // 5
console.log(math.multiply(4, 5)); // 20

// Key differences
/*
CommonJS:
- Synchronous loading
- Runtime dependency resolution
- Dynamic imports with require()
- Entire module object is loaded
- this = module.exports in module scope

ES Modules:
- Asynchronous loading
- Static dependency analysis
- Static imports (compile-time)
- Tree shaking support
- this = undefined in module scope
*/
```

### 🎯 Import/Export Syntax

> **Interview Explanation:** ES Modules provide various import/export patterns for different use cases: named exports for multiple functions, default exports for main functionality, and namespace imports for entire modules.

```javascript
// Different export patterns
// utils.js

// 1. Named exports
export const PI = 3.14159;
export let counter = 0;

export function increment() {
    return ++counter;
}

export class Calculator {
    add(a, b) {
        return a + b;
    }
}

// 2. Export list
function helper1() { return "helper1"; }
function helper2() { return "helper2"; }

export { helper1, helper2 };

// 3. Renamed exports
function internalFunction() { return "internal"; }
export { internalFunction as publicFunction };

// 4. Default export
export default function mainUtility() {
    return "main utility";
}

// 5. Re-exports
export { someFunction } from './other-module.js';
export * from './another-module.js';

// Different import patterns
// main.js

// 1. Named imports
import { PI, increment, Calculator } from './utils.js';

// 2. Renamed imports
import { publicFunction as myFunction } from './utils.js';

// 3. Default import
import mainUtility from './utils.js';

// 4. Mixed imports
import mainUtility, { PI, increment } from './utils.js';

// 5. Namespace import
import * as Utils from './utils.js';

// 6. Side-effect only import
import './polyfills.js';

// Usage examples
console.log(PI); // 3.14159
console.log(increment()); // 1

const calc = new Calculator();
console.log(calc.add(2, 3)); // 5

console.log(mainUtility()); // "main utility"
console.log(Utils.PI); // 3.14159

// Advanced import/export patterns
// config.js
const config = {
    apiUrl: 'https://api.example.com',
    timeout: 5000
};

export { config as default, config as appConfig };

// Multiple ways to import the same thing
import config from './config.js';
import { appConfig } from './config.js';
import { default as myConfig } from './config.js';

// Conditional exports (package.json)
/*
{
  "exports": {
    ".": {
      "import": "./esm/index.js",
      "require": "./cjs/index.js",
      "types": "./types/index.d.ts"
    },
    "./utils": {
      "import": "./esm/utils.js",
      "require": "./cjs/utils.js"
    }
  }
}
*/
```

### 🎯 Dynamic Imports

> **Interview Explanation:** Dynamic imports allow loading modules at runtime using `import()` function. This enables code splitting, lazy loading, and conditional module loading, which are crucial for performance optimization.

```javascript
// Basic dynamic import
async function loadModule() {
    try {
        const module = await import('./math.js');
        console.log(module.add(2, 3)); // 5
        
        // Destructure default and named exports
        const { default: divide, add, multiply } = await import('./math.js');
        console.log(divide(10, 2)); // 5
    } catch (error) {
        console.error('Failed to load module:', error);
    }
}

// Conditional loading
async function loadFeature(featureName) {
    let module;
    
    switch (featureName) {
        case 'charts':
            module = await import('./charts.js');
            break;
        case 'maps':
            module = await import('./maps.js');
            break;
        case 'analytics':
            module = await import('./analytics.js');
            break;
        default:
            throw new Error(`Unknown feature: ${featureName}`);
    }
    
    return module.default;
}

// Usage
document.getElementById('chartsBtn').addEventListener('click', async () => {
    const Charts = await loadFeature('charts');
    const chart = new Charts();
    chart.render();
});

// Lazy loading with caching
class ModuleLoader {
    constructor() {
        this.cache = new Map();
    }
    
    async loadModule(modulePath) {
        if (this.cache.has(modulePath)) {
            return this.cache.get(modulePath);
        }
        
        try {
            const module = await import(modulePath);
            this.cache.set(modulePath, module);
            return module;
        } catch (error) {
            console.error(`Failed to load ${modulePath}:`, error);
            throw error;
        }
    }
}

const loader = new ModuleLoader();

// Dynamic imports with webpack magic comments (bundler-specific)
async function loadWithWebpackComments() {
    // Chunk naming
    const module1 = await import(
        /* webpackChunkName: "math-utils" */ './math.js'
    );
    
    // Prefetch (load in idle time)
    const module2 = await import(
        /* webpackPrefetch: true */ './optional-feature.js'
    );
    
    // Preload (load immediately)
    const module3 = await import(
        /* webpackPreload: true */ './critical-feature.js'
    );
    
    return { module1, module2, module3 };
}

// Error handling and fallbacks
async function robustModuleLoading() {
    const fallbackModule = {
        default: class FallbackComponent {
            render() {
                return '<div>Fallback component</div>';
            }
        }
    };
    
    try {
        return await import('./preferred-component.js');
    } catch (error) {
        console.warn('Failed to load preferred component, using fallback');
        return fallbackModule;
    }
}

// Dynamic imports for internationalization
async function loadTranslations(locale) {
    try {
        const translations = await import(`./i18n/${locale}.js`);
        return translations.default;
    } catch (error) {
        // Fallback to English
        console.warn(`Translations for ${locale} not found, falling back to English`);
        const fallback = await import('./i18n/en.js');
        return fallback.default;
    }
}

// Progressive enhancement with dynamic imports
class ProgressiveFeature {
    constructor(element) {
        this.element = element;
        this.enhanced = false;
    }
    
    async enhance() {
        if (this.enhanced) return;
        
        try {
            const { EnhancementModule } = await import('./enhancements.js');
            this.enhancement = new EnhancementModule(this.element);
            this.enhanced = true;
            console.log('Feature enhanced successfully');
        } catch (error) {
            console.warn('Enhancement failed, continuing with basic functionality');
        }
    }
    
    basicRender() {
        this.element.innerHTML = 'Basic functionality';
    }
    
    async render() {
        await this.enhance();
        
        if (this.enhanced) {
            this.enhancement.render();
        } else {
            this.basicRender();
        }
    }
}
```

### 🎯 Tree Shaking

> **Interview Explanation:** Tree shaking is dead code elimination that removes unused exports from the final bundle. It only works with ES Modules because they have static structure, allowing bundlers to analyze dependencies at build time.

```javascript
// Tree shaking friendly code
// utils.js - Multiple named exports

// This will be included only if imported
export function usedFunction() {
    return 'This function is used';
}

// This will be removed if not imported
export function unusedFunction() {
    return 'This function is never used';
}

// This will be removed if not imported
export const unusedConstant = 'unused';

// This will be included only if imported
export const usedConstant = 'used';

// Class that might be partially shaken
export class UtilityClass {
    // Only used methods will be included
    usedMethod() {
        return 'used';
    }
    
    // This might be removed if not used
    unusedMethod() {
        return 'unused';
    }
}

// main.js - Only import what you need
import { usedFunction, usedConstant } from './utils.js';

console.log(usedFunction()); // Only this function will be in the bundle
console.log(usedConstant);   // Only this constant will be in the bundle

// Tree shaking anti-patterns (avoid these)

// Anti-pattern 1: Default export of object
// bad-utils.js
export default {
    usedFunction: () => 'used',
    unusedFunction: () => 'unused' // Can't be tree-shaken
};

// Anti-pattern 2: Side effects in modules
// bad-module.js
console.log('This runs when module is imported'); // Side effect

export function myFunction() {
    return 'function';
}

// Anti-pattern 3: Importing entire module
import * as allUtils from './utils.js'; // Imports everything

// Better: Import only what you need
import { usedFunction } from './utils.js';

// Tree shaking friendly patterns

// Pattern 1: Pure functions as named exports
// math.js
export const add = (a, b) => a + b;
export const multiply = (a, b) => a * b;
export const divide = (a, b) => a / b;

// Pattern 2: Conditional exports
// features.js
export function coreFeature() {
    return 'core';
}

// Optional feature that might not be needed
export function optionalFeature() {
    if (process.env.NODE_ENV === 'development') {
        return 'optional development feature';
    }
    return 'optional production feature';
}

// Pattern 3: Modular architecture
// Instead of one large utility file, split into smaller modules

// string-utils.js
export const capitalize = str => str.charAt(0).toUpperCase() + str.slice(1);
export const reverse = str => str.split('').reverse().join('');

// array-utils.js
export const unique = arr => [...new Set(arr)];
export const chunk = (arr, size) => {
    const chunks = [];
    for (let i = 0; i < arr.length; i += size) {
        chunks.push(arr.slice(i, i + size));
    }
    return chunks;
};

// Package.json configuration for tree shaking
/*
{
  "name": "my-library",
  "main": "dist/index.js",
  "module": "src/index.js",  // ES module entry point
  "sideEffects": false,      // No side effects, safe to tree shake
  // OR specify files with side effects
  "sideEffects": ["./src/polyfills.js", "*.css"]
}
*/

// Webpack configuration for tree shaking
/*
// webpack.config.js
module.exports = {
  mode: 'production', // Enables tree shaking
  optimization: {
    usedExports: true,  // Mark unused exports
    sideEffects: false  // Safe to remove unused code
  }
};
*/

// Testing tree shaking effectiveness
// Create a bundle analyzer report to see what's included

// Example: Large library with tree shaking
// lodash-es (tree-shakable) vs lodash (not tree-shakable)

// Bad: Imports entire lodash
import _ from 'lodash';
const result = _.map([1, 2, 3], x => x * 2);

// Good: Tree-shakable import
import { map } from 'lodash-es';
const result = map([1, 2, 3], x => x * 2);

// Even better: Individual function imports
import map from 'lodash-es/map';
const result = map([1, 2, 3], x => x * 2);
```

---

## 5. Generators & Iterators

> **Interview Explanation:** Generators are functions that can pause and resume execution, yielding values one at a time. Iterators provide a standard way to traverse collections. Together, they enable lazy evaluation and custom iteration patterns.

### 🎯 Generator Functions

> **Interview Key Point:** Generator functions use `function*` syntax and `yield` keyword to produce a sequence of values lazily. They return an iterator object and can maintain state between yield points.

```javascript
// Basic generator function
function* simpleGenerator() {
    console.log('Generator started');
    yield 1;
    console.log('After first yield');
    yield 2;
    console.log('After second yield');
    yield 3;
    console.log('Generator finished');
}

const gen = simpleGenerator();
console.log(gen.next()); // { value: 1, done: false }
console.log(gen.next()); // { value: 2, done: false }
console.log(gen.next()); // { value: 3, done: false }
console.log(gen.next()); // { value: undefined, done: true }

// Generator with parameters and return
function* generatorWithParams(start, end) {
    console.log(`Starting from ${start} to ${end}`);
    
    for (let i = start; i <= end; i++) {
        const received = yield i;
        if (received) {
            console.log(`Received: ${received}`);
        }
    }
    
    return 'Generator completed';
}

const paramGen = generatorWithParams(1, 3);
console.log(paramGen.next());        // { value: 1, done: false }
console.log(paramGen.next('hello')); // { value: 2, done: false }
console.log(paramGen.next());        // { value: 3, done: false }
console.log(paramGen.next());        // { value: 'Generator completed', done: true }

// Infinite generators
function* infiniteSequence() {
    let i = 0;
    while (true) {
        yield i++;
    }
}

const infinite = infiniteSequence();
console.log(infinite.next().value); // 0
console.log(infinite.next().value); // 1
console.log(infinite.next().value); // 2

// Fibonacci generator
function* fibonacci() {
    let a = 0, b = 1;
    while (true) {
        yield a;
        [a, b] = [b, a + b];
    }
}

const fib = fibonacci();
for (let i = 0; i < 10; i++) {
    console.log(fib.next().value);
}
// Output: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34

// Generator delegation with yield*
function* innerGenerator() {
    yield 'a';
    yield 'b';
}

function* outerGenerator() {
    yield 1;
    yield* innerGenerator(); // Delegate to another generator
    yield 2;
}

const delegated = outerGenerator();
console.log([...delegated]); // [1, 'a', 'b', 2]

// Practical example: ID generator
function* createIDGenerator(prefix = 'id') {
    let counter = 1;
    while (true) {
        yield `${prefix}_${counter++}`;
    }
}

const userIDGen = createIDGenerator('user');
const productIDGen = createIDGenerator('product');

console.log(userIDGen.next().value);    // 'user_1'
console.log(userIDGen.next().value);    // 'user_2'
console.log(productIDGen.next().value); // 'product_1'

// Generator for async operations
function* asyncDataProcessor() {
    console.log('Starting data processing...');
    
    const users = yield fetch('/api/users');
    console.log(`Loaded ${users.length} users`);
    
    const posts = yield fetch('/api/posts');
    console.log(`Loaded ${posts.length} posts`);
    
    const processed = users.map(user => ({
        ...user,
        posts: posts.filter(post => post.userId === user.id)
    }));
    
    return processed;
}

// Helper to run async generator
async function runAsyncGenerator(generator) {
    const gen = generator();
    let result = gen.next();
    
    while (!result.done) {
        try {
            const response = await result.value;
            const data = await response.json();
            result = gen.next(data);
        } catch (error) {
            result = gen.throw(error);
        }
    }
    
    return result.value;
}

// Generator for state machines
function* trafficLight() {
    while (true) {
        yield 'red';
        yield 'yellow';
        yield 'green';
        yield 'yellow';
    }
}

const lights = trafficLight();
setInterval(() => {
    console.log(`Light is: ${lights.next().value}`);
}, 1000);
```

### 🎯 Iterator Protocol

> **Interview Explanation:** The iterator protocol defines a standard way to produce a sequence of values. Objects implementing this protocol have a `Symbol.iterator` method that returns an iterator with a `next()` method.

```javascript
// Custom iterator implementation
class Range {
    constructor(start, end, step = 1) {
        this.start = start;
        this.end = end;
        this.step = step;
    }
    
    // Make the object iterable
    [Symbol.iterator]() {
        let current = this.start;
        const end = this.end;
        const step = this.step;
        
        return {
            next() {
                if (current < end) {
                    const value = current;
                    current += step;
                    return { value, done: false };
                } else {
                    return { done: true };
                }
            }
        };
    }
}

const range = new Range(1, 5);
for (const num of range) {
    console.log(num); // 1, 2, 3, 4
}

// Convert to array
console.log([...range]); // [1, 2, 3, 4]

// Manual iteration
const iterator = range[Symbol.iterator]();
console.log(iterator.next()); // { value: 1, done: false }
console.log(iterator.next()); // { value: 2, done: false }

// Iterator with generator (simpler)
class SimpleRange {
    constructor(start, end) {
        this.start = start;
        this.end = end;
    }
    
    *[Symbol.iterator]() {
        for (let i = this.start; i < this.end; i++) {
            yield i;
        }
    }
}

const simpleRange = new SimpleRange(10, 13);
console.log([...simpleRange]); // [10, 11, 12]

// Built-in iterables
const builtInIterables = {
    string: 'hello',
    array: [1, 2, 3],
    map: new Map([['a', 1], ['b', 2]]),
    set: new Set([1, 2, 3])
};

// All of these work with for...of
for (const char of builtInIterables.string) {
    console.log(char); // h, e, l, l, o
}

// Custom collection with iterator
class TodoList {
    constructor() {
        this.todos = [];
    }
    
    add(todo) {
        this.todos.push(todo);
    }
    
    // Make it iterable - only incomplete todos
    *[Symbol.iterator]() {
        for (const todo of this.todos) {
            if (!todo.completed) {
                yield todo;
            }
        }
    }
    
    // Additional iterator for completed todos
    *completed() {
        for (const todo of this.todos) {
            if (todo.completed) {
                yield todo;
            }
        }
    }
    
    // Iterator for all todos
    *all() {
        yield* this.todos;
    }
}

const todoList = new TodoList();
todoList.add({ text: 'Learn iterators', completed: false });
todoList.add({ text: 'Practice coding', completed: true });
todoList.add({ text: 'Build project', completed: false });

// Iterate incomplete todos (default iterator)
for (const todo of todoList) {
    console.log(todo.text); // 'Learn iterators', 'Build project'
}

// Iterate completed todos
for (const todo of todoList.completed()) {
    console.log(todo.text); // 'Practice coding'
}

// Iterator helpers and utilities
class IteratorUtils {
    static *map(iterable, mapFn) {
        for (const item of iterable) {
            yield mapFn(item);
        }
    }
    
    static *filter(iterable, predicate) {
        for (const item of iterable) {
            if (predicate(item)) {
                yield item;
            }
        }
    }
    
    static *take(iterable, count) {
        let taken = 0;
        for (const item of iterable) {
            if (taken >= count) break;
            yield item;
            taken++;
        }
    }
    
    static *enumerate(iterable, start = 0) {
        let index = start;
        for (const item of iterable) {
            yield [index++, item];
        }
    }
    
    static *zip(...iterables) {
        const iterators = iterables.map(it => it[Symbol.iterator]());
        
        while (true) {
            const results = iterators.map(it => it.next());
            
            if (results.some(result => result.done)) {
                break;
            }
            
            yield results.map(result => result.value);
        }
    }
}

// Usage examples
const numbers = [1, 2, 3, 4, 5];

// Chain iterator operations
const result = IteratorUtils.take(
    IteratorUtils.filter(
        IteratorUtils.map(numbers, x => x * 2),
        x => x > 4
    ),
    2
);

console.log([...result]); // [6, 8]

// Enumerate example
for (const [index, value] of IteratorUtils.enumerate(['a', 'b', 'c'])) {
    console.log(`${index}: ${value}`); // 0: a, 1: b, 2: c
}

// Zip example
const names = ['Alice', 'Bob', 'Charlie'];
const ages = [25, 30, 35];
const cities = ['NYC', 'LA', 'Chicago'];

for (const [name, age, city] of IteratorUtils.zip(names, ages, cities)) {
    console.log(`${name}, ${age}, from ${city}`);
}
```

### 🎯 Custom Iterables

> **Interview Explanation:** Custom iterables allow you to define how objects are iterated. By implementing `Symbol.iterator`, you can make any object work with `for...of`, spread operator, and other iteration contexts.

```javascript
// Linked list with custom iterator
class LinkedListNode {
    constructor(value, next = null) {
        this.value = value;
        this.next = next;
    }
}

class LinkedList {
    constructor() {
        this.head = null;
        this.size = 0;
    }
    
    append(value) {
        const newNode = new LinkedListNode(value);
        
        if (!this.head) {
            this.head = newNode;
        } else {
            let current = this.head;
            while (current.next) {
                current = current.next;
            }
            current.next = newNode;
        }
        
        this.size++;
    }
    
    // Make it iterable
    *[Symbol.iterator]() {
        let current = this.head;
        while (current) {
            yield current.value;
            current = current.next;
        }
    }
    
    // Additional iterators
    *reverse() {
        const values = [...this]; // Use default iterator
        for (let i = values.length - 1; i >= 0; i--) {
            yield values[i];
        }
    }
    
    *pairs() {
        const iterator = this[Symbol.iterator]();
        let current = iterator.next();
        
        while (!current.done) {
            const next = iterator.next();
            if (!next.done) {
                yield [current.value, next.value];
            }
            current = next;
        }
    }
}

const list = new LinkedList();
list.append(1);
list.append(2);
list.append(3);
list.append(4);

console.log([...list]); // [1, 2, 3, 4]
console.log([...list.reverse()]); // [4, 3, 2, 1]
console.log([...list.pairs()]); // [[1, 2], [3, 4]]

// Binary tree traversal iterators
class TreeNode {
    constructor(value, left = null, right = null) {
        this.value = value;
        this.left = left;
        this.right = right;
    }
}

class BinaryTree {
    constructor(root = null) {
        this.root = root;
    }
    
    // In-order traversal (default)
    *[Symbol.iterator]() {
        yield* this.inOrder(this.root);
    }
    
    *inOrder(node) {
        if (node) {
            yield* this.inOrder(node.left);
            yield node.value;
            yield* this.inOrder(node.right);
        }
    }
    
    *preOrder(node = this.root) {
        if (node) {
            yield node.value;
            yield* this.preOrder(node.left);
            yield* this.preOrder(node.right);
        }
    }
    
    *postOrder(node = this.root) {
        if (node) {
            yield* this.postOrder(node.left);
            yield* this.postOrder(node.right);
            yield node.value;
        }
    }
    
    *levelOrder() {
        if (!this.root) return;
        
        const queue = [this.root];
        
        while (queue.length > 0) {
            const node = queue.shift();
            yield node.value;
            
            if (node.left) queue.push(node.left);
            if (node.right) queue.push(node.right);
        }
    }
}

//     4
//   /   \
//  2     6
// / \   / \
//1   3 5   7

const tree = new BinaryTree(
    new TreeNode(4,
        new TreeNode(2,
            new TreeNode(1),
            new TreeNode(3)
        ),
        new TreeNode(6,
            new TreeNode(5),
            new TreeNode(7)
        )
    )
);

console.log('In-order:', [...tree]); // [1, 2, 3, 4, 5, 6, 7]
console.log('Pre-order:', [...tree.preOrder()]); // [4, 2, 1, 3, 6, 5, 7]
console.log('Post-order:', [...tree.postOrder()]); // [1, 3, 2, 5, 7, 6, 4]
console.log('Level-order:', [...tree.levelOrder()]); // [4, 2, 6, 1, 3, 5, 7]

// Async iterables
class AsyncDataSource {
    constructor(data) {
        this.data = data;
    }
    
    // Async iterator
    async *[Symbol.asyncIterator]() {
        for (let i = 0; i < this.data.length; i++) {
            // Simulate async data fetching
            await new Promise(resolve => setTimeout(resolve, 100));
            yield this.data[i];
        }
    }
}

async function processAsyncData() {
    const asyncSource = new AsyncDataSource([1, 2, 3, 4, 5]);
    
    for await (const item of asyncSource) {
        console.log(`Processed: ${item}`);
    }
}

// Matrix iterator (2D array)
class Matrix {
    constructor(rows, cols, initialValue = 0) {
        this.rows = rows;
        this.cols = cols;
        this.data = Array(rows).fill().map(() => Array(cols).fill(initialValue));
    }
    
    set(row, col, value) {
        this.data[row][col] = value;
    }
    
    get(row, col) {
        return this.data[row][col];
    }
    
    // Iterate by rows (default)
    *[Symbol.iterator]() {
        for (let row of this.data) {
            yield [...row];
        }
    }
    
    // Iterate by columns
    *columns() {
        for (let col = 0; col < this.cols; col++) {
            const column = [];
            for (let row = 0; row < this.rows; row++) {
                column.push(this.data[row][col]);
            }
            yield column;
        }
    }
    
    // Iterate all elements
    *elements() {
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                yield this.data[row][col];
            }
        }
    }
    
    // Iterate with coordinates
    *coordinates() {
        for (let row = 0; row < this.rows; row++) {
            for (let col = 0; col < this.cols; col++) {
                yield [row, col, this.data[row][col]];
            }
        }
    }
}

const matrix = new Matrix(3, 3);
matrix.set(0, 0, 1);
matrix.set(1, 1, 5);
matrix.set(2, 2, 9);

console.log('By rows:');
for (const row of matrix) {
    console.log(row); // [1, 0, 0], [0, 5, 0], [0, 0, 9]
}

console.log('By columns:');
for (const col of matrix.columns()) {
    console.log(col); // [1, 0, 0], [0, 5, 0], [0, 0, 9]
}

console.log('All elements:', [...matrix.elements()]); // [1, 0, 0, 0, 5, 0, 0, 0, 9]
```

---

## 6. Functional Programming

> **Interview Explanation:** Functional programming is a paradigm that treats computation as evaluation of mathematical functions. Key principles include immutability, pure functions, higher-order functions, and avoiding side effects.

### 🎯 Pure Functions

> **Interview Key Point:** Pure functions always return the same output for the same input and have no side effects. They're predictable, testable, and enable optimizations like memoization.

```javascript
// Pure function examples
function add(a, b) {
    return a + b; // Always returns same result for same inputs
}

function multiply(x, y) {
    return x * y; // No side effects, no external dependencies
}

function calculateCircleArea(radius) {
    return Math.PI * radius * radius; // Math.PI is a constant, so this is pure
}

// Impure function examples (avoid these)
let counter = 0;

function impureIncrement() {
    counter++; // Side effect: modifies external state
    return counter;
}

function impureRandom() {
    return Math.random(); // Different output each time
}

function impureGetTime() {
    return new Date().getTime(); // Depends on current time
}

function impureLog(value) {
    console.log(value); // Side effect: I/O operation
    return value;
}

// Making impure functions pure
function pureIncrement(currentValue) {
    return currentValue + 1; // Takes state as parameter
}

function pureCalculateWithTax(price, taxRate) {
    return price * (1 + taxRate); // All dependencies as parameters
}

// Pure function for array operations
function pureFilter(array, predicate) {
    const result = [];
    for (let i = 0; i < array.length; i++) {
        if (predicate(array[i])) {
            result.push(array[i]);
        }
    }
    return result; // Returns new array, doesn't modify original
}

function pureMap(array, transform) {
    const result = [];
    for (let i = 0; i < array.length; i++) {
        result.push(transform(array[i]));
    }
    return result;
}

// Pure function composition
const double = x => x * 2;
const addTen = x => x + 10;
const square = x => x * x;

function compose(f, g) {
    return x => f(g(x));
}

const doubleAndAddTen = compose(addTen, double);
const squareAndDouble = compose(double, square);

console.log(doubleAndAddTen(5)); // 20 ((5 * 2) + 10)
console.log(squareAndDouble(3)); // 18 ((3 * 3) * 2)

// Referential transparency
const x = 5;
const y = 3;

// These expressions are referentially transparent
const result1 = add(x, y);
const result2 = add(5, 3);
const result3 = 8; // Can be replaced with the result

console.log(result1 === result2); // true
console.log(result2 === result3); // true

// Memoization with pure functions
function memoize(fn) {
    const cache = new Map();
    
    return function(...args) {
        const key = JSON.stringify(args);
        
        if (cache.has(key)) {
            return cache.get(key);
        }
        
        const result = fn(...args);
        cache.set(key, result);
        return result;
    };
}

// Expensive pure function
function expensiveFibonacci(n) {
    if (n <= 1) return n;
    return expensiveFibonacci(n - 1) + expensiveFibonacci(n - 2);
}

const memoizedFibonacci = memoize(expensiveFibonacci);

console.time('First call');
console.log(memoizedFibonacci(40)); // Slow first time
console.timeEnd('First call');

console.time('Second call');
console.log(memoizedFibonacci(40)); // Fast, retrieved from cache
console.timeEnd('Second call');
```

### 🎯 Immutability

> **Interview Explanation:** Immutability means data cannot be changed after creation. Instead of modifying existing data, you create new data structures. This prevents bugs from unexpected mutations and enables optimizations.

```javascript
// Primitive values are immutable by nature
let a = 5;
let b = a; // b gets a copy of a's value
a = 10;   // a changes, but b remains 5
console.log(a, b); // 10, 5

// Objects and arrays are mutable (need special handling)
const mutableArray = [1, 2, 3];
mutableArray.push(4); // Mutates original array
console.log(mutableArray); // [1, 2, 3, 4]

// Immutable array operations
const originalArray = [1, 2, 3];

// Adding elements (immutable)
const withNewElement = [...originalArray, 4];
const withPrepended = [0, ...originalArray];
const withInserted = [
    ...originalArray.slice(0, 1),
    'inserted',
    ...originalArray.slice(1)
];

console.log(originalArray);   // [1, 2, 3] - unchanged
console.log(withNewElement);  // [1, 2, 3, 4]
console.log(withPrepended);   // [0, 1, 2, 3]
console.log(withInserted);    // [1, 'inserted', 2, 3]

// Removing elements (immutable)
const withoutFirst = originalArray.slice(1);
const withoutLast = originalArray.slice(0, -1);
const withoutMiddle = [
    ...originalArray.slice(0, 1),
    ...originalArray.slice(2)
];

// Updating elements (immutable)
const updated = originalArray.map((item, index) => 
    index === 1 ? 'updated' : item
);

console.log(updated); // [1, 'updated', 3]

// Immutable object operations
const originalObject = { name: 'Alice', age: 25, city: 'NYC' };

// Adding properties (immutable)
const withNewProperty = { ...originalObject, job: 'Developer' };

// Updating properties (immutable)
const withUpdatedAge = { ...originalObject, age: 26 };

// Removing properties (immutable)
const { city, ...withoutCity } = originalObject;

console.log(originalObject);     // { name: 'Alice', age: 25, city: 'NYC' }
console.log(withNewProperty);    // { name: 'Alice', age: 25, city: 'NYC', job: 'Developer' }
console.log(withUpdatedAge);     // { name: 'Alice', age: 26, city: 'NYC' }
console.log(withoutCity);        // { name: 'Alice', age: 25 }

// Deep immutable updates
const complexObject = {
    user: {
        profile: {
            name: 'Alice',
            settings: {
                theme: 'dark',
                notifications: true
            }
        },
        posts: [
            { id: 1, title: 'First post' },
            { id: 2, title: 'Second post' }
        ]
    }
};

// Deep update helper
function updateNested(obj, path, value) {
    const [head, ...tail] = path.split('.');
    
    if (tail.length === 0) {
        return { ...obj, [head]: value };
    }
    
    return {
        ...obj,
        [head]: updateNested(obj[head], tail.join('.'), value)
    };
}

const updatedComplex = updateNested(
    complexObject,
    'user.profile.settings.theme',
    'light'
);

console.log(complexObject.user.profile.settings.theme); // 'dark' - unchanged
console.log(updatedComplex.user.profile.settings.theme); // 'light'

// Immutable array of objects updates
const users = [
    { id: 1, name: 'Alice', active: true },
    { id: 2, name: 'Bob', active: false },
    { id: 3, name: 'Charlie', active: true }
];

// Update specific user
const updatedUsers = users.map(user =>
    user.id === 2 ? { ...user, active: true } : user
);

// Add new user
const usersWithNew = [...users, { id: 4, name: 'David', active: true }];

// Remove user
const usersWithoutBob = users.filter(user => user.id !== 2);

// Sort users (immutable)
const sortedUsers = [...users].sort((a, b) => a.name.localeCompare(b.name));

console.log(users);        // Original unchanged
console.log(updatedUsers); // Bob is now active
console.log(sortedUsers);  // Sorted by name

// Immutability utilities
class ImmutableArray {
    constructor(items = []) {
        this.items = Object.freeze([...items]);
    }
    
    push(item) {
        return new ImmutableArray([...this.items, item]);
    }
    
    pop() {
        return new ImmutableArray(this.items.slice(0, -1));
    }
    
    map(fn) {
        return new ImmutableArray(this.items.map(fn));
    }
    
    filter(predicate) {
        return new ImmutableArray(this.items.filter(predicate));
    }
    
    get(index) {
        return this.items[index];
    }
    
    get length() {
        return this.items.length;
    }
    
    toArray() {
        return [...this.items];
    }
}

const immutableArray = new ImmutableArray([1, 2, 3]);
const newArray = immutableArray.push(4).map(x => x * 2);

console.log(immutableArray.toArray()); // [1, 2, 3] - unchanged
console.log(newArray.toArray());       // [2, 4, 6, 8]

// Using libraries for immutability (concept)
// Immer example (conceptual)
function updateWithImmer(state, updates) {
    // Immer allows "mutations" that create immutable updates
    return produce(state, draft => {
        Object.assign(draft, updates);
    });
}

// ImmutableJS example (conceptual)
/*
const { Map, List } = require('immutable');

const immutableMap = Map({ name: 'Alice', age: 25 });
const updatedMap = immutableMap.set('age', 26);

const immutableList = List([1, 2, 3]);
const updatedList = immutableList.push(4);
*/
```

### 🎯 Array Methods & Function Composition

> **Interview Explanation:** Array methods like `map`, `filter`, `reduce` are the foundation of functional programming in JavaScript. They enable declarative programming and can be composed to create complex data transformations.

```javascript
// Core array methods
const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// map: Transform each element
const doubled = numbers.map(n => n * 2);
console.log(doubled); // [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

// filter: Select elements that match criteria
const evens = numbers.filter(n => n % 2 === 0);
console.log(evens); // [2, 4, 6, 8, 10]

// reduce: Combine all elements into single value
const sum = numbers.reduce((acc, n) => acc + n, 0);
console.log(sum); // 55

const product = numbers.reduce((acc, n) => acc * n, 1);
console.log(product); // 3628800

// Advanced reduce examples
const words = ['hello', 'world', 'how', 'are', 'you'];

// Count characters
const totalChars = words.reduce((acc, word) => acc + word.length, 0);
console.log(totalChars); // 17

// Group by length
const groupedByLength = words.reduce((acc, word) => {
    const length = word.length;
    if (!acc[length]) {
        acc[length] = [];
    }
    acc[length].push(word);
    return acc;
}, {});
console.log(groupedByLength); // { 3: ['how', 'are', 'you'], 5: ['hello', 'world'] }

// Find min/max
const findMinMax = arr => arr.reduce(
    (acc, n) => ({
        min: Math.min(acc.min, n),
        max: Math.max(acc.max, n)
    }),
    { min: Infinity, max: -Infinity }
);
console.log(findMinMax(numbers)); // { min: 1, max: 10 }

// Chaining array methods
const result = numbers
    .filter(n => n % 2 === 0)    // Get even numbers
    .map(n => n * n)             // Square them
    .filter(n => n > 10)         // Only keep > 10
    .reduce((acc, n) => acc + n, 0); // Sum them

console.log(result); // 220 (16 + 36 + 64 + 100)

// Complex data transformations
const users = [
    { id: 1, name: 'Alice', age: 25, city: 'NYC', active: true },
    { id: 2, name: 'Bob', age: 30, city: 'LA', active: false },
    { id: 3, name: 'Charlie', age: 35, city: 'NYC', active: true },
    { id: 4, name: 'David', age: 28, city: 'Chicago', active: true },
    { id: 5, name: 'Eve', age: 22, city: 'LA', active: false }
];

// Get active users from NYC, sorted by age
const activeNYCUsers = users
    .filter(user => user.active && user.city === 'NYC')
    .sort((a, b) => a.age - b.age)
    .map(user => ({ name: user.name, age: user.age }));

console.log(activeNYCUsers); // [{ name: 'Alice', age: 25 }, { name: 'Charlie', age: 35 }]

// Group users by city and calculate average age
const cityStats = users.reduce((acc, user) => {
    const { city, age } = user;
    
    if (!acc[city]) {
        acc[city] = { count: 0, totalAge: 0, users: [] };
    }
    
    acc[city].count++;
    acc[city].totalAge += age;
    acc[city].users.push(user.name);
    acc[city].averageAge = acc[city].totalAge / acc[city].count;
    
    return acc;
}, {});

console.log(cityStats);

// Function composition with array methods
const pipe = (...fns) => value => fns.reduce((acc, fn) => fn(acc), value);

const processNumbers = pipe(
    arr => arr.filter(n => n > 0),           // Remove non-positive
    arr => arr.map(n => Math.sqrt(n)),       // Square root
    arr => arr.filter(n => n % 1 === 0),     // Keep only integers
    arr => arr.sort((a, b) => a - b)         // Sort ascending
);

const testNumbers = [-1, 0, 1, 4, 9, 16, 25, 30];
console.log(processNumbers(testNumbers)); // [1, 2, 3, 4, 5]

// Custom array method implementations
const customArrayMethods = {
    map: (array, fn) => {
        const result = [];
        for (let i = 0; i < array.length; i++) {
            result.push(fn(array[i], i, array));
        }
        return result;
    },
    
    filter: (array, predicate) => {
        const result = [];
        for (let i = 0; i < array.length; i++) {
            if (predicate(array[i], i, array)) {
                result.push(array[i]);
            }
        }
        return result;
    },
    
    reduce: (array, reducer, initialValue) => {
        let acc = initialValue;
        let startIndex = 0;
        
        if (initialValue === undefined) {
            acc = array[0];
            startIndex = 1;
        }
        
        for (let i = startIndex; i < array.length; i++) {
            acc = reducer(acc, array[i], i, array);
        }
        
        return acc;
    },
    
    find: (array, predicate) => {
        for (let i = 0; i < array.length; i++) {
            if (predicate(array[i], i, array)) {
                return array[i];
            }
        }
        return undefined;
    },
    
    some: (array, predicate) => {
        for (let i = 0; i < array.length; i++) {
            if (predicate(array[i], i, array)) {
                return true;
            }
        }
        return false;
    },
    
    every: (array, predicate) => {
        for (let i = 0; i < array.length; i++) {
            if (!predicate(array[i], i, array)) {
                return false;
            }
        }
        return true;
    }
};

// Functional programming utilities
const curry = fn => {
    return function curried(...args) {
        if (args.length >= fn.length) {
            return fn.apply(this, args);
        }
        return (...nextArgs) => curried(...args, ...nextArgs);
    };
};

// Curried array operations
const curriedMap = curry((fn, array) => array.map(fn));
const curriedFilter = curry((predicate, array) => array.filter(predicate));
const curriedReduce = curry((reducer, initial, array) => array.reduce(reducer, initial));

// Create reusable functions
const double = x => x * 2;
const isEven = x => x % 2 === 0;
const sum = (acc, n) => acc + n;

const mapDouble = curriedMap(double);
const filterEvens = curriedFilter(isEven);
const sumAll = curriedReduce(sum, 0);

// Compose operations
const processEvenNumbers = pipe(
    filterEvens,
    mapDouble,
    sumAll
);

console.log(processEvenNumbers([1, 2, 3, 4, 5, 6])); // 24 ((2 + 4 + 6) * 2)

// Transducers (advanced functional programming)
const transducer = {
    map: fn => reducer => (acc, value) => reducer(acc, fn(value)),
    filter: predicate => reducer => (acc, value) => 
        predicate(value) ? reducer(acc, value) : acc,
    take: n => reducer => {
        let taken = 0;
        return (acc, value) => {
            if (taken < n) {
                taken++;
                return reducer(acc, value);
            }
            return acc;
        };
    }
};

const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);

const xform = compose(
    transducer.filter(x => x % 2 === 0),
    transducer.map(x => x * x),
    transducer.take(3)
);

const transduce = (xf, reducer, initial, collection) => {
    const transformedReducer = xf(reducer);
    return collection.reduce(transformedReducer, initial);
};

const largeNumbers = Array.from({ length: 100 }, (_, i) => i + 1);
const transducedResult = transduce(
    xform,
    (acc, x) => acc.concat(x),
    [],
    largeNumbers
);

console.log(transducedResult); // [4, 16, 36] - first 3 squares of even numbers
```

---

## 🎯 Quick Interview Questions & Answers

### **1. What is the difference between the Task Queue and Microtask Queue?**

- **Task Queue (Macrotasks)**: Contains callbacks from `setTimeout`, `setInterval`, DOM events
- **Microtask Queue**: Contains `Promise.then`, `queueMicrotask`, `async/await` callbacks
- **Priority**: Microtasks are processed completely before any macrotask
- **Execution**: After each macrotask, all microtasks are processed

### **2. Explain the four rules of `this` binding**

- **Default Binding**: `this` refers to global object (or `undefined` in strict mode)
- **Implicit Binding**: `this` refers to the object that called the method
- **Explicit Binding**: `this` is explicitly set using `call`, `apply`, or `bind`
- **Arrow Function Binding**: `this` is lexically inherited from enclosing scope

### **3. What's the difference between currying and partial application?**

- **Currying**: Transforms a function to take one argument at a time
- **Partial Application**: Fixes some arguments and returns a function expecting the remaining ones
- **Flexibility**: Partial application is more flexible in argument positioning

### **4. How do you handle errors in async/await?**

- Use `try-catch` blocks around `await` expressions
- Handle at function level or individual operation level
- Combine with `Promise.allSettled()` for multiple operations
- Always propagate or handle errors appropriately

### **5. Explain function composition**

- **Definition**: Combining functions where output of one becomes input of another
- **Mathematical**: `(f ∘ g)(x) = f(g(x))`
- **Benefits**: Reusability, readability, testability
- **Implementation**: Using `compose` or `pipe` functions

### **6. What are generators and when would you use them?**

- **Definition**: Functions that can pause and resume execution using `yield`
- **Use Cases**: Lazy evaluation, infinite sequences, async flow control, state machines
- **Benefits**: Memory efficient, controllable iteration, elegant async patterns

### **7. Difference between CommonJS and ES Modules**

- **CommonJS**: Synchronous, `require()/module.exports`, runtime resolution, Node.js
- **ES Modules**: Asynchronous, `import/export`, static analysis, modern standard, tree-shakable

### **8. What is tree shaking?**

- **Definition**: Dead code elimination that removes unused exports
- **Requirements**: ES Modules with static structure
- **Benefits**: Smaller bundle size, better performance
- **Configuration**: Requires proper bundler setup and side-effect declarations

### **9. What are pure functions and their benefits?**

- **Definition**: Functions with no side effects that always return same output for same input
- **Benefits**: Predictable, testable, cacheable, parallelizable
- **Examples**: Mathematical operations, data transformations
- **Contrast**: Impure functions have side effects or depend on external state

### **10. Explain the iterator protocol**

- **Definition**: Standard way to produce sequence of values using `Symbol.iterator`
- **Interface**: Objects with `next()` method returning `{value, done}`
- **Usage**: `for...of` loops, spread operator, destructuring
- **Custom**: Implement `Symbol.iterator` to make objects iterable

---

**This comprehensive guide covers advanced JavaScript concepts with detailed explanations and practical examples. Master these concepts to excel in senior-level JavaScript interviews! 🚀**
