# 🔥 Core JavaScript Foundations - Detailed Guide

> **Master the fundamental building blocks of JavaScript with comprehensive explanations and practical examples**

---

## 📋 Table of Contents

1. [Variables & Scope](#1-variables--scope)
2. [Data Types](#2-data-types)
3. [Functions](#3-functions)
4. [Execution Context & Hoisting](#4-execution-context--hoisting)
5. [Closures](#5-closures)
6. [Objects & Prototypes](#6-objects--prototypes)

---

## 1. Variables & Scope

> **Interview Explanation:** Variables in JavaScript behave differently based on how they're declared. Understanding scope is crucial because it determines where variables can be accessed in your code. This is one of the most common interview topics.

### 🎯 `var` vs `let` vs `const`

**Quick Interview Answer:**

- `var`: Function-scoped, hoisted with `undefined`, can be re-declared
- `let`: Block-scoped, hoisted but in temporal dead zone, cannot be re-declared
- `const`: Block-scoped, hoisted but in temporal dead zone, cannot be re-declared or re-assigned

#### **Function Scope vs Block Scope**

> **Interview Tip:** Scope determines variable accessibility. Function scope means the variable is available throughout the entire function, while block scope means it's only available within the nearest curly braces `{}`.

```javascript
// var - Function Scoped
function varExample() {
    if (true) {
        var x = 1;
    }
    console.log(x); // 1 - accessible outside block
}

// let/const - Block Scoped
function letExample() {
    if (true) {
        let y = 1;
        const z = 2;
    }
    console.log(y); // ReferenceError: y is not defined
    console.log(z); // ReferenceError: z is not defined
}
```

#### **Hoisting Behavior Differences**

> **Interview Explanation:** Hoisting means variable declarations are moved to the top of their scope during compilation. However, `var` is initialized with `undefined`, while `let`/`const` remain uninitialized until their actual declaration line, creating a "temporal dead zone".

```javascript
// var hoisting
console.log(a); // undefined (not ReferenceError)
var a = 5;

// Equivalent to:
var a;
console.log(a); // undefined
a = 5;

// let/const hoisting
console.log(b); // ReferenceError: Cannot access 'b' before initialization
let b = 10;

console.log(c); // ReferenceError: Cannot access 'c' before initialization
const c = 15;
```

#### **Temporal Dead Zone (TDZ)**

> **Interview Explanation:** TDZ is the period between when a scope is entered and when a `let`/`const` variable is declared. During this time, accessing the variable throws a ReferenceError. This prevents the use of variables before they're properly initialized.

```javascript
// TDZ Example
function example() {
    console.log(typeof myVar); // "undefined"
    console.log(typeof myLet); // ReferenceError: Cannot access 'myLet' before initialization
    
    var myVar = 1;
    let myLet = 2;
}

// TDZ with const
{
    // TDZ starts
    console.log(typeof temp); // ReferenceError
    let temp = 5; // TDZ ends
}
```

#### **Re-declaration and Re-assignment**

```javascript
// var allows re-declaration
var name = "John";
var name = "Jane"; // No error
name = "Bob"; // No error

// let allows re-assignment but not re-declaration
let age = 25;
// let age = 30; // SyntaxError: Identifier 'age' has already been declared
age = 30; // OK

// const doesn't allow re-declaration or re-assignment
const PI = 3.14;
// const PI = 3.14159; // SyntaxError
// PI = 3.14159; // TypeError: Assignment to constant variable

// But objects/arrays can be mutated
const obj = { name: "John" };
obj.name = "Jane"; // OK - mutating the object
obj.age = 25; // OK

const arr = [1, 2, 3];
arr.push(4); // OK - mutating the array
```

#### **Loop Scope Issues**

> **Interview Explanation:** The classic `var` loop problem occurs because `var` is function-scoped, so all iterations share the same variable. By the time the setTimeout callbacks execute, the loop has finished and `i` equals the final value. `let` creates a new variable for each iteration, solving this issue.

```javascript
// Classic var problem in loops
for (var i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100); // Prints: 3, 3, 3
}

// Solution with let
for (let i = 0; i < 3; i++) {
    setTimeout(() => console.log(i), 100); // Prints: 0, 1, 2
}

// Solution with var using IIFE
for (var i = 0; i < 3; i++) {
    (function(j) {
        setTimeout(() => console.log(j), 100); // Prints: 0, 1, 2
    })(i);
}
```

---

## 2. Data Types

> **Interview Explanation:** JavaScript has 8 data types: 7 primitive (Number, String, Boolean, Undefined, Null, Symbol, BigInt) and 1 non-primitive (Object). Understanding the difference between primitive and reference types is crucial for understanding how JavaScript handles memory and variable assignment.

### 🎯 Primitive Types

> **Interview Key Point:** Primitive types are stored by value, meaning when you assign a primitive to another variable, you create a copy. Objects are stored by reference, meaning variables point to the same memory location.

#### **Number Type**

> **Interview Explanation:** JavaScript has only one number type (unlike other languages with int, float, etc.). All numbers are 64-bit floating point. Be aware of floating-point precision issues and special values like `Infinity`, `-Infinity`, and `NaN`.

```javascript
// Number representations
let decimal = 42;
let float = 3.14;
let scientific = 2.5e3; // 2500
let binary = 0b1010; // 10 in decimal
let octal = 0o12; // 10 in decimal
let hex = 0xFF; // 255 in decimal

// Special number values
console.log(1/0); // Infinity
console.log(-1/0); // -Infinity
console.log(0/0); // NaN
console.log(Number.MAX_VALUE); // 1.7976931348623157e+308
console.log(Number.MIN_VALUE); // 5e-324

// Floating point precision issues
console.log(0.1 + 0.2); // 0.30000000000000004
console.log(0.1 + 0.2 === 0.3); // false

// Safe way to compare floats
function isEqual(a, b, tolerance = Number.EPSILON) {
    return Math.abs(a - b) < tolerance;
}
console.log(isEqual(0.1 + 0.2, 0.3)); // true
```

#### **String Type**

```javascript
// String creation
let str1 = "Hello";
let str2 = 'World';
let str3 = `Template literal with ${str1}`;

// String methods
console.log(str1.length); // 5
console.log(str1.charAt(0)); // "H"
console.log(str1.indexOf('e')); // 1
console.log(str1.slice(1, 3)); // "el"
console.log(str1.substring(1, 3)); // "el"
console.log(str1.toLowerCase()); // "hello"

// Template literals
let name = "John";
let age = 25;
let message = `Hello, my name is ${name} and I'm ${age} years old.`;
console.log(message);

// Multi-line strings
let multiline = `
    This is a
    multi-line
    string
`;
```

#### **Boolean Type**

> **Interview Explanation:** JavaScript has 8 falsy values: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, and `NaN`. Everything else is truthy. This is crucial for conditional statements and logical operations.

```javascript
// Boolean values
let isTrue = true;
let isFalse = false;

// Falsy values in JavaScript
console.log(Boolean(false)); // false
console.log(Boolean(0)); // false
console.log(Boolean(-0)); // false
console.log(Boolean(0n)); // false (BigInt)
console.log(Boolean("")); // false
console.log(Boolean(null)); // false
console.log(Boolean(undefined)); // false
console.log(Boolean(NaN)); // false

// Everything else is truthy
console.log(Boolean([])); // true
console.log(Boolean({})); // true
console.log(Boolean("false")); // true
console.log(Boolean(" ")); // true
```

#### **Symbol Type**

```javascript
// Symbol creation
let sym1 = Symbol();
let sym2 = Symbol("description");
let sym3 = Symbol("description");

console.log(sym2 === sym3); // false - each symbol is unique

// Symbol use cases
const obj = {};
const sym = Symbol("key");
obj[sym] = "value";
console.log(obj[sym]); // "value"

// Symbols are not enumerable
for (let key in obj) {
    console.log(key); // Won't print the symbol key
}

// Global symbols
let globalSym1 = Symbol.for("global");
let globalSym2 = Symbol.for("global");
console.log(globalSym1 === globalSym2); // true
```

#### **BigInt Type**

```javascript
// BigInt creation
let bigInt1 = 123n;
let bigInt2 = BigInt(123);
let bigInt3 = BigInt("123");

// Large numbers
let largeNumber = 9007199254740991n + 1n; // Beyond Number.MAX_SAFE_INTEGER

// BigInt operations
console.log(10n + 20n); // 30n
console.log(10n * 20n); // 200n
console.log(10n / 3n); // 3n (truncated)

// Cannot mix BigInt with regular numbers
// console.log(10n + 5); // TypeError
console.log(10n + BigInt(5)); // 15n
```

### 🎯 Non-Primitive Types

#### **Objects**

```javascript
// Object creation methods
let obj1 = {}; // Object literal
let obj2 = new Object(); // Constructor
let obj3 = Object.create(null); // No prototype

// Property access
let person = {
    name: "John",
    age: 25,
    "complex-key": "value"
};

console.log(person.name); // "John"
console.log(person["age"]); // 25
console.log(person["complex-key"]); // "value"

// Dynamic property names
let key = "dynamicKey";
let obj = {
    [key]: "dynamicValue",
    [key + "2"]: "anotherValue"
};
```

#### **Arrays**

```javascript
// Array creation
let arr1 = [1, 2, 3];
let arr2 = new Array(3); // [empty × 3]
let arr3 = Array.of(3); // [3]
let arr4 = Array.from("hello"); // ["h", "e", "l", "l", "o"]

// Array methods
let numbers = [1, 2, 3, 4, 5];
console.log(numbers.length); // 5
numbers.push(6); // Add to end
numbers.unshift(0); // Add to beginning
numbers.pop(); // Remove from end
numbers.shift(); // Remove from beginning

// Array iteration
numbers.forEach(num => console.log(num));
let doubled = numbers.map(num => num * 2);
let evens = numbers.filter(num => num % 2 === 0);
let sum = numbers.reduce((acc, num) => acc + num, 0);
```

### 🎯 Type Coercion

#### **Implicit Coercion**

```javascript
// String coercion
console.log("5" + 3); // "53"
console.log("5" - 3); // 2
console.log("5" * 3); // 15
console.log("5" / 3); // 1.6666666666666667

// Boolean coercion
console.log(true + 1); // 2
console.log(false + 1); // 1
console.log(true * 2); // 2

// Null and undefined
console.log(null + 1); // 1
console.log(undefined + 1); // NaN

// Object coercion
console.log([1, 2] + [3, 4]); // "1,23,4"
console.log({} + {}); // "[object Object][object Object]"
console.log([] + {}); // "[object Object]"
console.log({} + []); // 0 (in some contexts)
```

#### **Explicit Coercion**

```javascript
// To String
console.log(String(123)); // "123"
console.log(String(true)); // "true"
console.log(String(null)); // "null"
console.log((123).toString()); // "123"

// To Number
console.log(Number("123")); // 123
console.log(Number("123.45")); // 123.45
console.log(Number("hello")); // NaN
console.log(parseInt("123.45")); // 123
console.log(parseFloat("123.45")); // 123.45

// To Boolean
console.log(Boolean(1)); // true
console.log(Boolean(0)); // false
console.log(Boolean("")); // false
console.log(Boolean("hello")); // true
```

#### **Equality Comparisons**

```javascript
// == (Abstract Equality)
console.log(5 == "5"); // true (type coercion)
console.log(true == 1); // true
console.log(false == 0); // true
console.log(null == undefined); // true
console.log("" == 0); // true

// === (Strict Equality)
console.log(5 === "5"); // false
console.log(true === 1); // false
console.log(null === undefined); // false

// Object comparison
let obj1 = { name: "John" };
let obj2 = { name: "John" };
let obj3 = obj1;

console.log(obj1 == obj2); // false (different references)
console.log(obj1 === obj2); // false
console.log(obj1 === obj3); // true (same reference)
```

### 🎯 typeof Operator Quirks

```javascript
// typeof returns
console.log(typeof 42); // "number"
console.log(typeof "hello"); // "string"
console.log(typeof true); // "boolean"
console.log(typeof undefined); // "undefined"
console.log(typeof Symbol()); // "symbol"
console.log(typeof 123n); // "bigint"

// typeof quirks
console.log(typeof null); // "object" (famous JavaScript bug)
console.log(typeof NaN); // "number"
console.log(typeof []); // "object"
console.log(typeof {}); // "object"
console.log(typeof function(){}); // "function"

// Better type checking
function getType(value) {
    if (value === null) return "null";
    if (Array.isArray(value)) return "array";
    return typeof value;
}

console.log(getType(null)); // "null"
console.log(getType([])); // "array"
console.log(getType({})); // "object"
```

---

## 3. Functions

> **Interview Explanation:** Functions are first-class citizens in JavaScript, meaning they can be assigned to variables, passed as arguments, and returned from other functions. Understanding different function types and their behavior is essential for JavaScript mastery.

### 🎯 Function Declarations vs Expressions

> **Interview Key Point:** Function declarations are fully hoisted (both declaration and implementation), while function expressions are only hoisted as variables (initialized as `undefined` until assignment).

#### **Function Declarations**

```javascript
// Function declaration - hoisted completely
console.log(add(2, 3)); // 5 - works due to hoisting

function add(a, b) {
    return a + b;
}

// Conditional function declarations (avoid in strict mode)
if (true) {
    function conditionalFunc() {
        return "declared conditionally";
    }
}
```

#### **Function Expressions**

```javascript
// Function expression - not hoisted
// console.log(subtract(5, 2)); // TypeError: subtract is not a function

var subtract = function(a, b) {
    return a - b;
};

// Named function expression
var factorial = function fact(n) {
    return n <= 1 ? 1 : n * fact(n - 1);
};

console.log(factorial(5)); // 120
// console.log(fact(5)); // ReferenceError: fact is not defined (outside scope)
```

### 🎯 Arrow Functions

> **Interview Explanation:** Arrow functions have lexical `this` binding (inherits `this` from the enclosing scope), no `arguments` object, cannot be used as constructors, and are always anonymous. They're perfect for callbacks but not for object methods when you need dynamic `this`.

#### **Syntax Variations**

```javascript
// Different arrow function syntaxes
const simple = () => "Hello World";
const withParam = (name) => `Hello ${name}`;
const withMultipleParams = (a, b) => a + b;
const withBlock = (x) => {
    const result = x * 2;
    return result;
};
const returningObject = () => ({ name: "John", age: 25 });

// Single parameter doesn't need parentheses
const square = x => x * x;
```

#### **Lexical `this` Binding**

```javascript
// Regular function vs Arrow function `this` binding
const obj = {
    name: "John",
    
    regularMethod: function() {
        console.log("Regular:", this.name); // "John"
        
        setTimeout(function() {
            console.log("Regular setTimeout:", this.name); // undefined (global this)
        }, 100);
        
        setTimeout(() => {
            console.log("Arrow setTimeout:", this.name); // "John" (lexical this)
        }, 100);
    },
    
    arrowMethod: () => {
        console.log("Arrow method:", this.name); // undefined (lexical this from global)
    }
};

obj.regularMethod();
obj.arrowMethod();

// Arrow functions cannot be constructors
const ArrowConstructor = () => {};
// new ArrowConstructor(); // TypeError: ArrowConstructor is not a constructor

// Arrow functions don't have arguments object
function regularFunc() {
    console.log(arguments); // Arguments object
}

const arrowFunc = () => {
    // console.log(arguments); // ReferenceError: arguments is not defined
};

// Use rest parameters instead
const arrowWithRest = (...args) => {
    console.log(args); // Array of arguments
};
```

### 🎯 Higher-Order Functions

```javascript
// Functions that take other functions as arguments
function applyOperation(arr, operation) {
    return arr.map(operation);
}

const numbers = [1, 2, 3, 4, 5];
const squared = applyOperation(numbers, x => x * x);
const doubled = applyOperation(numbers, x => x * 2);

console.log(squared); // [1, 4, 9, 16, 25]
console.log(doubled); // [2, 4, 6, 8, 10]

// Functions that return other functions
function createMultiplier(factor) {
    return function(number) {
        return number * factor;
    };
}

const double = createMultiplier(2);
const triple = createMultiplier(3);

console.log(double(5)); // 10
console.log(triple(5)); // 15

// Functional composition
const compose = (f, g) => (x) => f(g(x));

const addOne = x => x + 1;
const multiplyByTwo = x => x * 2;

const addOneThenDouble = compose(multiplyByTwo, addOne);
console.log(addOneThenDouble(3)); // 8 ((3 + 1) * 2)
```

### 🎯 IIFE (Immediately Invoked Function Expression)

```javascript
// Basic IIFE
(function() {
    console.log("IIFE executed!");
})();

// IIFE with parameters
(function(name) {
    console.log(`Hello, ${name}!`);
})("John");

// IIFE returning a value
const result = (function(a, b) {
    return a + b;
})(5, 3);

console.log(result); // 8

// Module pattern using IIFE
const mathModule = (function() {
    let pi = 3.14159;
    
    return {
        area: function(radius) {
            return pi * radius * radius;
        },
        circumference: function(radius) {
            return 2 * pi * radius;
        }
    };
})();

console.log(mathModule.area(5)); // 78.53975
// console.log(mathModule.pi); // undefined (private variable)

// Arrow function IIFE
(() => {
    console.log("Arrow IIFE executed!");
})();
```

### 🎯 First-Class Functions

```javascript
// Functions as values
const greet = function(name) {
    return `Hello, ${name}!`;
};

// Assign to variables
const sayHello = greet;
console.log(sayHello("Alice")); // "Hello, Alice!"

// Store in arrays
const operations = [
    (a, b) => a + b,
    (a, b) => a - b,
    (a, b) => a * b,
    (a, b) => a / b
];

console.log(operations[0](5, 3)); // 8
console.log(operations[2](5, 3)); // 15

// Store in objects
const calculator = {
    add: (a, b) => a + b,
    subtract: (a, b) => a - b,
    multiply: (a, b) => a * b,
    divide: (a, b) => a / b
};

console.log(calculator.add(10, 5)); // 15

// Pass as arguments
function executeOperation(operation, a, b) {
    return operation(a, b);
}

console.log(executeOperation((x, y) => x ** y, 2, 3)); // 8

// Return from functions
function getOperation(type) {
    switch(type) {
        case 'add': return (a, b) => a + b;
        case 'multiply': return (a, b) => a * b;
        default: return (a, b) => a;
    }
}

const addFunc = getOperation('add');
console.log(addFunc(4, 6)); // 10
```

---

## 4. Execution Context & Hoisting

> **Interview Explanation:** Execution context is the environment where JavaScript code is executed. It includes variable objects, scope chains, and the `this` value. Understanding this concept explains how hoisting works and how JavaScript manages function calls through the call stack.

### 🎯 Execution Context

> **Interview Key Point:** There are three types of execution contexts: Global, Function, and Block (ES6+). Each context has two phases: Creation (hoisting happens here) and Execution.

#### **Types of Execution Context**

```javascript
// Global Execution Context
var globalVar = "I'm global";

function outerFunction() {
    // Function Execution Context
    var outerVar = "I'm in outer function";
    
    function innerFunction() {
        // Another Function Execution Context
        var innerVar = "I'm in inner function";
        console.log(globalVar); // Accessible
        console.log(outerVar);  // Accessible
        console.log(innerVar);  // Accessible
    }
    
    innerFunction();
    // console.log(innerVar); // ReferenceError: innerVar is not defined
}

outerFunction();

// Block Execution Context (ES6+)
{
    let blockVar = "I'm in block";
    const blockConst = "I'm also in block";
    var notBlockScoped = "I'm not block scoped";
}

// console.log(blockVar); // ReferenceError
// console.log(blockConst); // ReferenceError
console.log(notBlockScoped); // "I'm not block scoped"
```

#### **Creation and Execution Phases**

```javascript
// During creation phase:
// 1. Variable object is created
// 2. Scope chain is established
// 3. 'this' value is determined

console.log(typeof myFunction); // "function" (hoisted)
console.log(typeof myVar); // "undefined" (hoisted but not initialized)
// console.log(typeof myLet); // ReferenceError (TDZ)

var myVar = "Hello";
let myLet = "World";

function myFunction() {
    return "I'm hoisted!";
}

// The above code is interpreted as:
/*
var myVar; // undefined
function myFunction() { return "I'm hoisted!"; }

console.log(typeof myFunction); // "function"
console.log(typeof myVar); // "undefined"

myVar = "Hello";
let myLet = "World";
*/
```

### 🎯 Call Stack

> **Interview Explanation:** The call stack is a LIFO (Last In, First Out) data structure that tracks function calls. When a function is called, it's pushed onto the stack; when it returns, it's popped off. Stack overflow occurs when too many functions are called without returning (usually infinite recursion).

```javascript
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
Call Stack visualization:
1. first() is pushed
2. second() is pushed (called from first)
3. third() is pushed (called from second)
4. third() executes and is popped
5. second() continues and is popped
6. first() continues and is popped

Output:
First function start
Second function start
Third function
Second function end
First function end
*/

// Stack overflow example
function recursiveFunction() {
    recursiveFunction(); // Will cause stack overflow
}

// recursiveFunction(); // RangeError: Maximum call stack size exceeded
```

### 🎯 Variable Hoisting

```javascript
// Variable hoisting with var
console.log(hoistedVar); // undefined (not ReferenceError)
var hoistedVar = "I'm hoisted";
console.log(hoistedVar); // "I'm hoisted"

// Equivalent to:
var hoistedVar;
console.log(hoistedVar); // undefined
hoistedVar = "I'm hoisted";
console.log(hoistedVar); // "I'm hoisted"

// let and const hoisting (TDZ)
function example() {
    console.log(a); // undefined
    console.log(b); // ReferenceError: Cannot access 'b' before initialization
    console.log(c); // ReferenceError: Cannot access 'c' before initialization
    
    var a = 1;
    let b = 2;
    const c = 3;
}

// Class hoisting
// console.log(new MyClass()); // ReferenceError: Cannot access 'MyClass' before initialization

class MyClass {
    constructor() {
        this.name = "MyClass";
    }
}
```

### 🎯 Function Hoisting

```javascript
// Function declaration hoisting
console.log(add(2, 3)); // 5 - works!

function add(a, b) {
    return a + b;
}

// Function expression hoisting
console.log(subtract); // undefined
// console.log(subtract(5, 2)); // TypeError: subtract is not a function

var subtract = function(a, b) {
    return a - b;
};

// Arrow function hoisting
// console.log(multiply(2, 3)); // TypeError: multiply is not a function

var multiply = (a, b) => a * b;

// Function hoisting precedence
var myFunc = "I'm a variable";

function myFunc() {
    return "I'm a function";
}

console.log(typeof myFunc); // "function" - function declaration wins
```

---

## 5. Closures

> **Interview Explanation:** A closure is when an inner function has access to variables from its outer function's scope even after the outer function has finished executing. Closures are created every time a function is created. This is fundamental to JavaScript and enables powerful patterns like module pattern and data privacy.

### 🎯 Lexical Scoping

> **Interview Explanation:** Lexical scoping means that the scope of a variable is determined by where it's declared in the code, not where it's called. Inner functions have access to variables in their outer scope, creating a scope chain.

```javascript
// Lexical scoping example
function outerFunction(x) {
    // Outer scope
    
    function innerFunction(y) {
        // Inner scope has access to outer scope
        console.log(x + y); // Can access 'x' from outer scope
    }
    
    return innerFunction;
}

const addFive = outerFunction(5);
addFive(3); // 8

// Scope chain example
var globalVar = "global";

function outer() {
    var outerVar = "outer";
    
    function middle() {
        var middleVar = "middle";
        
        function inner() {
            var innerVar = "inner";
            console.log(innerVar);   // "inner"
            console.log(middleVar);  // "middle"
            console.log(outerVar);   // "outer"
            console.log(globalVar);  // "global"
        }
        
        inner();
    }
    
    middle();
}

outer();
```

### 🎯 Basic Closures

```javascript
// Simple closure
function createGreeting(greeting) {
    return function(name) {
        return `${greeting}, ${name}!`;
    };
}

const sayHello = createGreeting("Hello");
const sayGoodbye = createGreeting("Goodbye");

console.log(sayHello("Alice")); // "Hello, Alice!"
console.log(sayGoodbye("Bob")); // "Goodbye, Bob!"

// Counter closure
function createCounter() {
    let count = 0;
    
    return function() {
        count++;
        return count;
    };
}

const counter1 = createCounter();
const counter2 = createCounter();

console.log(counter1()); // 1
console.log(counter1()); // 2
console.log(counter2()); // 1 (independent counter)
console.log(counter1()); // 3
```

### 🎯 Memory Retention

```javascript
// Closure keeps reference to outer variables
function heavyOperation() {
    const largeArray = new Array(1000000).fill("data");
    
    return function(index) {
        return largeArray[index]; // largeArray is retained in memory
    };
}

const accessor = heavyOperation();
console.log(accessor(100)); // "data"
// largeArray is still in memory because of closure

// Memory optimization - only keep what you need
function optimizedOperation() {
    const largeArray = new Array(1000000).fill("data");
    const firstElement = largeArray[0];
    
    return function() {
        return firstElement; // Only firstElement is retained
    };
}

// Cleanup closure
function createResourceManager() {
    let resource = "expensive resource";
    
    return {
        use: function() {
            return resource;
        },
        cleanup: function() {
            resource = null; // Help garbage collection
        }
    };
}
```

### 🎯 Private Variables

> **Interview Explanation:** Closures enable data privacy in JavaScript by keeping variables in an outer scope accessible only to inner functions. This is how you create "private" variables in JavaScript before ES6 classes with private fields.

```javascript
// Private variables using closures
function createBankAccount(initialBalance) {
    let balance = initialBalance;
    let transactionHistory = [];
    
    return {
        deposit: function(amount) {
            if (amount > 0) {
                balance += amount;
                transactionHistory.push(`Deposited ${amount}`);
                return balance;
            }
            throw new Error("Amount must be positive");
        },
        
        withdraw: function(amount) {
            if (amount > 0 && amount <= balance) {
                balance -= amount;
                transactionHistory.push(`Withdrew ${amount}`);
                return balance;
            }
            throw new Error("Invalid withdrawal amount");
        },
        
        getBalance: function() {
            return balance;
        },
        
        getHistory: function() {
            return [...transactionHistory]; // Return copy, not reference
        }
    };
}

const account = createBankAccount(1000);
console.log(account.deposit(500)); // 1500
console.log(account.withdraw(200)); // 1300
console.log(account.getBalance()); // 1300
console.log(account.getHistory()); // ["Deposited 500", "Withdrew 200"]

// Cannot access private variables directly
// console.log(account.balance); // undefined
// console.log(account.transactionHistory); // undefined
```

### 🎯 Module Pattern

> **Interview Explanation:** The module pattern uses IIFE (Immediately Invoked Function Expression) and closures to create encapsulation and expose only specific functionality. This was the primary way to create modules in JavaScript before ES6 modules.

```javascript
// Module pattern using IIFE and closures
const mathModule = (function() {
    // Private variables and functions
    let pi = 3.14159;
    let e = 2.71828;
    
    function validateNumber(num) {
        return typeof num === 'number' && !isNaN(num);
    }
    
    // Public API
    return {
        // Public methods
        circle: {
            area: function(radius) {
                if (!validateNumber(radius) || radius < 0) {
                    throw new Error("Invalid radius");
                }
                return pi * radius * radius;
            },
            
            circumference: function(radius) {
                if (!validateNumber(radius) || radius < 0) {
                    throw new Error("Invalid radius");
                }
                return 2 * pi * radius;
            }
        },
        
        exponential: function(power) {
            if (!validateNumber(power)) {
                throw new Error("Invalid power");
            }
            return Math.pow(e, power);
        },
        
        // Public constants (getters)
        get PI() {
            return pi;
        },
        
        get E() {
            return e;
        }
    };
})();

console.log(mathModule.circle.area(5)); // 78.53975
console.log(mathModule.PI); // 3.14159
// console.log(mathModule.validateNumber(5)); // undefined (private)

// Revealing module pattern
const userModule = (function() {
    let users = [];
    let currentUser = null;
    
    function addUser(user) {
        users.push(user);
    }
    
    function removeUser(userId) {
        users = users.filter(user => user.id !== userId);
    }
    
    function setCurrentUser(user) {
        currentUser = user;
    }
    
    function getCurrentUser() {
        return currentUser;
    }
    
    function getAllUsers() {
        return [...users]; // Return copy
    }
    
    // Reveal public methods
    return {
        add: addUser,
        remove: removeUser,
        setCurrent: setCurrentUser,
        getCurrent: getCurrentUser,
        getAll: getAllUsers
    };
})();
```

### 🎯 Common Closure Pitfalls

```javascript
// Loop closure problem
function createFunctions() {
    var functions = [];
    
    for (var i = 0; i < 3; i++) {
        functions[i] = function() {
            return i; // All functions will return 3
        };
    }
    
    return functions;
}

const funcs = createFunctions();
console.log(funcs[0]()); // 3 (not 0!)
console.log(funcs[1]()); // 3 (not 1!)
console.log(funcs[2]()); // 3 (not 2!)

// Solution 1: Use let
function createFunctionsFixed1() {
    var functions = [];
    
    for (let i = 0; i < 3; i++) { // let creates new binding each iteration
        functions[i] = function() {
            return i;
        };
    }
    
    return functions;
}

// Solution 2: Use IIFE
function createFunctionsFixed2() {
    var functions = [];
    
    for (var i = 0; i < 3; i++) {
        functions[i] = (function(index) {
            return function() {
                return index;
            };
        })(i);
    }
    
    return functions;
}

// Solution 3: Use bind
function createFunctionsFixed3() {
    var functions = [];
    
    for (var i = 0; i < 3; i++) {
        functions[i] = function(index) {
            return index;
        }.bind(null, i);
    }
    
    return functions;
}
```

---

## 6. Objects & Prototypes

> **Interview Explanation:** JavaScript uses prototype-based inheritance, not class-based inheritance. Every object has a prototype (except the base Object), and objects inherit properties and methods from their prototype chain. Understanding prototypes is crucial for mastering JavaScript's object-oriented features.

### 🎯 Object Creation Patterns

> **Interview Key Point:** There are multiple ways to create objects in JavaScript: object literals, constructor functions, Object.create(), factory functions, and ES6 classes. Each has different use cases and prototype relationships.

#### **Object Literal**

```javascript
// Basic object literal
const person = {
    name: "John",
    age: 30,
    greet: function() {
        return `Hello, I'm ${this.name}`;
    }
};

// ES6 shorthand properties and methods
const name = "Alice";
const age = 25;

const person2 = {
    name, // shorthand for name: name
    age,  // shorthand for age: age
    greet() { // shorthand method syntax
        return `Hello, I'm ${this.name}`;
    }
};

// Computed property names
const propertyName = "dynamicProperty";
const obj = {
    [propertyName]: "dynamic value",
    [`${propertyName}2`]: "another dynamic value"
};

console.log(obj.dynamicProperty); // "dynamic value"
```

#### **Constructor Functions**

```javascript
// Constructor function
function Person(name, age) {
    this.name = name;
    this.age = age;
    this.greet = function() {
        return `Hello, I'm ${this.name}`;
    };
}

// Creating instances
const john = new Person("John", 30);
const alice = new Person("Alice", 25);

console.log(john.greet()); // "Hello, I'm John"
console.log(alice.greet()); // "Hello, I'm Alice"

// Constructor function with prototype methods
function PersonOptimized(name, age) {
    this.name = name;
    this.age = age;
}

PersonOptimized.prototype.greet = function() {
    return `Hello, I'm ${this.name}`;
};

PersonOptimized.prototype.getAge = function() {
    return this.age;
};

// What happens when you call 'new'
function myNew(constructor, ...args) {
    // 1. Create a new object
    const obj = {};
    
    // 2. Set the prototype
    Object.setPrototypeOf(obj, constructor.prototype);
    
    // 3. Call constructor with 'this' bound to new object
    const result = constructor.apply(obj, args);
    
    // 4. Return the object (or constructor's return value if it's an object)
    return result instanceof Object ? result : obj;
}
```

#### **Object.create()**

```javascript
// Using Object.create()
const personPrototype = {
    greet: function() {
        return `Hello, I'm ${this.name}`;
    },
    
    setName: function(name) {
        this.name = name;
    }
};

const person1 = Object.create(personPrototype);
person1.name = "John";
person1.age = 30;

const person2 = Object.create(personPrototype, {
    name: { value: "Alice", writable: true, enumerable: true },
    age: { value: 25, writable: true, enumerable: true }
});

console.log(person1.greet()); // "Hello, I'm John"
console.log(person2.greet()); // "Hello, I'm Alice"

// Creating object with null prototype
const nullProtoObj = Object.create(null);
nullProtoObj.name = "No prototype";
console.log(nullProtoObj.toString); // undefined (no prototype methods)
```

#### **Factory Functions**

```javascript
// Factory function
function createPerson(name, age) {
    return {
        name: name,
        age: age,
        greet: function() {
            return `Hello, I'm ${this.name}`;
        },
        
        getAge: function() {
            return this.age;
        }
    };
}

const person3 = createPerson("Bob", 35);
console.log(person3.greet()); // "Hello, I'm Bob"

// Factory with closure (private variables)
function createSecurePerson(name, age) {
    // Private variables
    let _name = name;
    let _age = age;
    
    return {
        getName: function() {
            return _name;
        },
        
        setName: function(newName) {
            if (typeof newName === 'string' && newName.length > 0) {
                _name = newName;
            }
        },
        
        getAge: function() {
            return _age;
        },
        
        greet: function() {
            return `Hello, I'm ${_name}`;
        }
    };
}

const securePerson = createSecurePerson("Charlie", 40);
console.log(securePerson.getName()); // "Charlie"
// securePerson._name is undefined (private)
```

### 🎯 Prototype Chain

> **Interview Explanation:** The prototype chain is how JavaScript implements inheritance. When you access a property on an object, JavaScript first looks on the object itself, then on its prototype, then the prototype's prototype, and so on until it reaches `Object.prototype` or `null`.

#### **Understanding Prototypes**

```javascript
// Every function has a prototype property
function Animal(name) {
    this.name = name;
}

Animal.prototype.speak = function() {
    return `${this.name} makes a sound`;
};

const dog = new Animal("Rex");

// Prototype chain visualization
console.log(dog.__proto__ === Animal.prototype); // true
console.log(Animal.prototype.__proto__ === Object.prototype); // true
console.log(Object.prototype.__proto__ === null); // true

// Prototype chain lookup
console.log(dog.speak()); // "Rex makes a sound" (found in Animal.prototype)
console.log(dog.toString()); // "[object Object]" (found in Object.prototype)

// Adding methods to prototype
Animal.prototype.eat = function() {
    return `${this.name} is eating`;
};

console.log(dog.eat()); // "Rex is eating" (newly added method)
```

#### **`__proto__` vs `prototype`**

```javascript
function Person(name) {
    this.name = name;
}

const john = new Person("John");

// prototype: Property of constructor functions
console.log(Person.prototype); // Object with constructor property

// __proto__: Property of all objects, points to prototype
console.log(john.__proto__ === Person.prototype); // true

// Setting prototype vs __proto__
Person.prototype.greet = function() {
    return `Hello, I'm ${this.name}`;
};

// Don't do this (performance issues)
john.__proto__.sayGoodbye = function() {
    return `Goodbye from ${this.name}`;
};

// Modern way to access prototype
console.log(Object.getPrototypeOf(john) === Person.prototype); // true

// Setting prototype of existing object
const plainObj = { name: "Plain" };
Object.setPrototypeOf(plainObj, Person.prototype);
console.log(plainObj.greet()); // "Hello, I'm Plain"
```

#### **Prototype Inheritance**

```javascript
// Parent constructor
function Animal(name) {
    this.name = name;
}

Animal.prototype.speak = function() {
    return `${this.name} makes a sound`;
};

Animal.prototype.eat = function() {
    return `${this.name} is eating`;
};

// Child constructor
function Dog(name, breed) {
    Animal.call(this, name); // Call parent constructor
    this.breed = breed;
}

// Set up inheritance
Dog.prototype = Object.create(Animal.prototype);
Dog.prototype.constructor = Dog;

// Add child-specific methods
Dog.prototype.bark = function() {
    return `${this.name} barks`;
};

// Override parent method
Dog.prototype.speak = function() {
    return `${this.name} barks loudly`;
};

const rex = new Dog("Rex", "Golden Retriever");
console.log(rex.speak()); // "Rex barks loudly" (overridden)
console.log(rex.eat()); // "Rex is eating" (inherited)
console.log(rex.bark()); // "Rex barks" (child-specific)

// Check inheritance chain
console.log(rex instanceof Dog); // true
console.log(rex instanceof Animal); // true
console.log(rex instanceof Object); // true
```

### 🎯 Object Methods

#### **Object.create()**

```javascript
// Object.create() with property descriptors
const base = { type: "base" };

const derived = Object.create(base, {
    name: {
        value: "derived",
        writable: true,
        enumerable: true,
        configurable: true
    },
    id: {
        value: 123,
        writable: false, // Read-only
        enumerable: false, // Won't appear in for...in
        configurable: false // Can't be deleted or reconfigured
    }
});

console.log(derived.name); // "derived"
console.log(derived.type); // "base" (inherited)
console.log(derived.id); // 123

// derived.id = 456; // Silently fails (or TypeError in strict mode)
console.log(derived.id); // Still 123
```

#### **Object.assign()**

```javascript
// Object.assign() for copying properties
const target = { a: 1, b: 2 };
const source1 = { b: 3, c: 4 };
const source2 = { c: 5, d: 6 };

const result = Object.assign(target, source1, source2);

console.log(result); // { a: 1, b: 3, c: 5, d: 6 }
console.log(target === result); // true (target is modified)

// Shallow copy with Object.assign()
const original = {
    name: "John",
    address: {
        city: "New York",
        zip: "10001"
    }
};

const copy = Object.assign({}, original);
copy.name = "Jane"; // Doesn't affect original
copy.address.city = "Boston"; // Affects original (shallow copy)

console.log(original.address.city); // "Boston"

// ES6 spread operator (similar to Object.assign)
const copy2 = { ...original };
```

#### **Object.freeze()**

```javascript
// Object.freeze() makes object immutable
const frozen = {
    name: "Frozen",
    numbers: [1, 2, 3]
};

Object.freeze(frozen);

// These operations will fail silently (or throw in strict mode)
frozen.name = "Changed"; // No effect
frozen.newProp = "new"; // No effect
delete frozen.name; // No effect

console.log(frozen.name); // Still "Frozen"

// But nested objects are not frozen (shallow freeze)
frozen.numbers.push(4); // This works!
console.log(frozen.numbers); // [1, 2, 3, 4]

// Deep freeze implementation
function deepFreeze(obj) {
    Object.getOwnPropertyNames(obj).forEach(name => {
        const value = obj[name];
        if (value && typeof value === "object") {
            deepFreeze(value);
        }
    });
    return Object.freeze(obj);
}

// Object.seal() - prevents adding/removing properties but allows modification
const sealed = { name: "Sealed", age: 30 };
Object.seal(sealed);

sealed.name = "Changed"; // This works
sealed.newProp = "new"; // This doesn't work
delete sealed.age; // This doesn't work

console.log(sealed.name); // "Changed"

// Object.preventExtensions() - prevents adding new properties
const noExtensions = { name: "No Extensions" };
Object.preventExtensions(noExtensions);

noExtensions.name = "Changed"; // This works
noExtensions.newProp = "new"; // This doesn't work

console.log(noExtensions.name); // "Changed"
```

### 🎯 Property Descriptors

```javascript
// Property descriptors define property behavior
const obj = {};

Object.defineProperty(obj, 'name', {
    value: 'John',
    writable: true,      // Can be changed
    enumerable: true,    // Shows up in for...in loops
    configurable: true   // Can be deleted or reconfigured
});

// Get property descriptor
const descriptor = Object.getOwnPropertyDescriptor(obj, 'name');
console.log(descriptor);
// { value: 'John', writable: true, enumerable: true, configurable: true }

// Define multiple properties
Object.defineProperties(obj, {
    age: {
        value: 30,
        writable: false, // Read-only
        enumerable: true,
        configurable: true
    },
    email: {
        value: 'john@example.com',
        writable: true,
        enumerable: false, // Hidden from enumeration
        configurable: true
    }
});

// Enumerable demonstration
for (let key in obj) {
    console.log(key); // Only prints 'name' and 'age', not 'email'
}

console.log(Object.keys(obj)); // ['name', 'age']
console.log(Object.getOwnPropertyNames(obj)); // ['name', 'age', 'email']

// Getter and setter properties
const person = {};

Object.defineProperty(person, 'fullName', {
    get: function() {
        return `${this.firstName} ${this.lastName}`;
    },
    set: function(value) {
        const parts = value.split(' ');
        this.firstName = parts[0];
        this.lastName = parts[1];
    },
    enumerable: true,
    configurable: true
});

person.fullName = "John Doe";
console.log(person.firstName); // "John"
console.log(person.lastName); // "Doe"
console.log(person.fullName); // "John Doe"

// ES6 getter/setter syntax in object literals
const personES6 = {
    firstName: '',
    lastName: '',
    
    get fullName() {
        return `${this.firstName} ${this.lastName}`;
    },
    
    set fullName(value) {
        const parts = value.split(' ');
        this.firstName = parts[0];
        this.lastName = parts[1];
    }
};
```

---

## 💡 Interview Tips for Core JavaScript

---

## 🎯 Quick Interview Answers

### **Common Interview Questions with Straightforward Explanations**

#### **1. What is the difference between `null` and `undefined`?**
- `undefined`: Variable has been declared but not assigned a value, or property doesn't exist
- `null`: Intentionally assigned value representing "no value" or "empty"
- `typeof null` returns `"object"` (JavaScript bug), `typeof undefined` returns `"undefined"`

#### **2. Explain hoisting with examples**
- Hoisting: Variable and function declarations are moved to the top of their scope during compilation
- `var`: Hoisted and initialized with `undefined`
- `let`/`const`: Hoisted but not initialized (Temporal Dead Zone)
- Function declarations: Fully hoisted (both declaration and implementation)
- Function expressions: Only variable declaration is hoisted

#### **3. What is a closure? Give a practical example**
- Closure: Inner function has access to outer function's variables even after outer function returns
- Creates data privacy and maintains state
- Example: Module pattern, private variables, callback functions with state

#### **4. How does `this` binding work?**
- Default: `this` refers to global object (window/globalThis)
- Object method: `this` refers to the object
- Constructor: `this` refers to the new instance
- Arrow functions: `this` is lexically bound (inherits from outer scope)
- Explicit binding: `call()`, `apply()`, `bind()` set `this` explicitly

#### **5. What is the prototype chain?**
- Every object has a prototype (except the base Object)
- When accessing a property, JavaScript looks up the prototype chain
- Chain: object → prototype → prototype's prototype → ... → Object.prototype → null

#### **6. Difference between `==` and `===`?**
- `==`: Loose equality, allows type coercion
- `===`: Strict equality, no type coercion
- Always prefer `===` unless you specifically need type coercion

#### **7. Different ways to create objects?**
1. Object literal: `{}`
2. Constructor function: `new Person()`
3. `Object.create()`
4. Factory function
5. ES6 Classes
6. `Object.assign()`

#### **8. What are the JavaScript data types?**
**Primitives (7)**: Number, String, Boolean, Undefined, Null, Symbol, BigInt
**Non-primitive (1)**: Object (includes arrays, functions, dates, etc.)

#### **9. What are falsy values in JavaScript?**
**8 falsy values**: `false`, `0`, `-0`, `0n`, `""`, `null`, `undefined`, `NaN`
Everything else is truthy (including `"false"`, `[]`, `{}`)

#### **10. Explain event bubbling and capturing**
- **Bubbling**: Event starts from target element and bubbles up to root
- **Capturing**: Event starts from root and captures down to target
- Use `addEventListener(event, handler, true)` for capturing phase

---

### 🎯 Common Interview Questions

1. **What is the difference between `null` and `undefined`?**
2. **Explain hoisting with examples**
3. **What is a closure? Give a practical example**
4. **How does `this` binding work in different contexts?**
5. **What is the prototype chain?**
6. **Explain the difference between `==` and `===`**
7. **What are the different ways to create objects in JavaScript?**

### 🎯 Coding Challenges

1. **Implement a function that demonstrates closure**
2. **Create a constructor function with inheritance**
3. **Write a polyfill for `Array.prototype.map()`**
4. **Implement a deep clone function**
5. **Create a function that shows the difference between `var`, `let`, and `const`**

### 🎯 Key Points to Remember

- **Understand the fundamentals deeply** - don't just memorize
- **Practice explaining concepts** out loud
- **Know the edge cases** and quirks
- **Understand the "why"** behind JavaScript's behavior
- **Be able to provide practical examples** for each concept

---