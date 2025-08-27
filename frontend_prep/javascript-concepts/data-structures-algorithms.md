# 📊 Data Structures & Algorithms in JavaScript

> **Complete Interview Preparation Guide** - Master essential data structures, algorithms, and problem-solving patterns for JavaScript technical interviews.

---

## � Table of Contents

### 📊 Basic Data Structures
- [Arrays & Array Methods](#-arrays--array-methods)
- [Objects & Hash Maps](#-objects--hash-maps)  
- [Sets & Maps](#-sets--maps)
- [Stacks & Queues](#-stacks--queues)

### 📊 Advanced Data Structures
- [Linked Lists](#-linked-lists)
- [Trees & Binary Trees](#-trees--binary-trees)
- [Graphs](#️-graphs)
- [Hash Tables](#-hash-tables--advanced-hashing)

### 📊 Common Algorithms
- [Sorting: QuickSort, MergeSort, BubbleSort](#-common-algorithms)
- [Searching: Binary Search, Linear Search](#-common-algorithms)
- [Recursion & Dynamic Programming](#-dynamic-programming)

### 📊 Problem-Solving Patterns
- [Two Pointers Technique](#-string--array-problems)
- [Sliding Window](#-string--array-problems)
- [String & Array Problems](#-string--array-problems)
- [Palindrome Check, Anagram Detection](#-string--array-problems)
- [Array Rotation, Subsequence Problems](#-string--array-problems)

### 📊 Complexity Analysis
- [Time & Space Complexity](#️-time--space-complexity-analysis)

---

## Example: Stack Implementation
```javascript
// Stack implementation
class Stack {
    constructor() {
        this.items = [];
    }
    
    push(item) { this.items.push(item); }
    pop() { return this.items.pop(); }
    peek() { return this.items[this.items.length - 1]; }
    isEmpty() { return this.items.length === 0; }
}
```

---

> **Interview Explanation:** Understanding basic data structures is fundamental for any programming interview. These structures form the building blocks for more complex algorithms and system designs.

### 🎯 Arrays & Array Methods

> **Interview Key Point:** Arrays are the most commonly used data structure in JavaScript. Mastering array methods and their time complexities is crucial for solving most algorithmic problems efficiently.

#### **Comprehensive Array Implementation & Methods**

```javascript
// Enhanced Array with Custom Methods
class EnhancedArray {
    constructor(...items) {
        this.data = [...items];
        this.length = this.data.length;
    }
    
    // Basic operations
    get(index) {
        if (index < 0 || index >= this.length) {
            throw new Error('Index out of bounds');
        }
        return this.data[index];
    }
    
    set(index, value) {
        if (index < 0 || index >= this.length) {
            throw new Error('Index out of bounds');
        }
        this.data[index] = value;
        return this;
    }
    
    push(...items) {
        this.data.push(...items);
        this.length = this.data.length;
        return this.length;
    }
    
    pop() {
        if (this.length === 0) return undefined;
        const item = this.data.pop();
        this.length = this.data.length;
        return item;
    }
    
    unshift(...items) {
        this.data.unshift(...items);
        this.length = this.data.length;
        return this.length;
    }
    
    shift() {
        if (this.length === 0) return undefined;
        const item = this.data.shift();
        this.length = this.data.length;
        return item;
    }
    
    // Custom map implementation
    map(callback, thisArg) {
        const result = new EnhancedArray();
        for (let i = 0; i < this.length; i++) {
            if (i in this.data) {
                result.push(callback.call(thisArg, this.data[i], i, this));
            }
        }
        return result;
    }
    
    // Custom filter implementation
    filter(callback, thisArg) {
        const result = new EnhancedArray();
        for (let i = 0; i < this.length; i++) {
            if (i in this.data && callback.call(thisArg, this.data[i], i, this)) {
                result.push(this.data[i]);
            }
        }
        return result;
    }
    
    // Custom reduce implementation
    reduce(callback, initialValue) {
        let accumulator = initialValue;
        let startIndex = 0;
        
        if (accumulator === undefined) {
            if (this.length === 0) {
                throw new TypeError('Reduce of empty array with no initial value');
            }
            accumulator = this.data[0];
            startIndex = 1;
        }
        
        for (let i = startIndex; i < this.length; i++) {
            if (i in this.data) {
                accumulator = callback(accumulator, this.data[i], i, this);
            }
        }
        
        return accumulator;
    }
    
    // Custom find implementation
    find(callback, thisArg) {
        for (let i = 0; i < this.length; i++) {
            if (i in this.data && callback.call(thisArg, this.data[i], i, this)) {
                return this.data[i];
            }
        }
        return undefined;
    }
    
    // Custom indexOf implementation
    indexOf(searchElement, fromIndex = 0) {
        const startIndex = fromIndex < 0 ? Math.max(0, this.length + fromIndex) : fromIndex;
        
        for (let i = startIndex; i < this.length; i++) {
            if (this.data[i] === searchElement) {
                return i;
            }
        }
        return -1;
    }
    
    // Custom includes implementation
    includes(searchElement, fromIndex = 0) {
        return this.indexOf(searchElement, fromIndex) !== -1;
    }
    
    // Custom reverse implementation
    reverse() {
        const result = new EnhancedArray();
        for (let i = this.length - 1; i >= 0; i--) {
            result.push(this.data[i]);
        }
        return result;
    }
    
    // Custom slice implementation
    slice(start = 0, end = this.length) {
        const startIndex = start < 0 ? Math.max(0, this.length + start) : Math.min(start, this.length);
        const endIndex = end < 0 ? Math.max(0, this.length + end) : Math.min(end, this.length);
        
        const result = new EnhancedArray();
        for (let i = startIndex; i < endIndex; i++) {
            result.push(this.data[i]);
        }
        return result;
    }
    
    // Custom splice implementation
    splice(start, deleteCount = this.length - start, ...items) {
        const startIndex = start < 0 ? Math.max(0, this.length + start) : Math.min(start, this.length);
        const actualDeleteCount = Math.max(0, Math.min(deleteCount, this.length - startIndex));
        
        const deletedElements = new EnhancedArray();
        const newData = [];
        
        // Copy elements before start
        for (let i = 0; i < startIndex; i++) {
            newData.push(this.data[i]);
        }
        
        // Collect deleted elements
        for (let i = startIndex; i < startIndex + actualDeleteCount; i++) {
            deletedElements.push(this.data[i]);
        }
        
        // Insert new items
        newData.push(...items);
        
        // Copy remaining elements
        for (let i = startIndex + actualDeleteCount; i < this.length; i++) {
            newData.push(this.data[i]);
        }
        
        this.data = newData;
        this.length = this.data.length;
        
        return deletedElements;
    }
    
    // Advanced array operations
    
    // Flatten array (any depth)
    flatten(depth = Infinity) {
        const flattenRecursive = (arr, currentDepth) => {
            const result = new EnhancedArray();
            
            for (const item of arr.data) {
                if (Array.isArray(item) && currentDepth > 0) {
                    const flattened = flattenRecursive(new EnhancedArray(...item), currentDepth - 1);
                    result.push(...flattened.data);
                } else {
                    result.push(item);
                }
            }
            
            return result;
        };
        
        return flattenRecursive(this, depth);
    }
    
    // Remove duplicates
    unique() {
        const seen = new Set();
        const result = new EnhancedArray();
        
        for (const item of this.data) {
            if (!seen.has(item)) {
                seen.add(item);
                result.push(item);
            }
        }
        
        return result;
    }
    
    // Group by function
    groupBy(keyFunction) {
        const groups = new Map();
        
        for (let i = 0; i < this.length; i++) {
            const key = keyFunction(this.data[i], i, this);
            
            if (!groups.has(key)) {
                groups.set(key, new EnhancedArray());
            }
            
            groups.get(key).push(this.data[i]);
        }
        
        return groups;
    }
    
    // Chunk array into smaller arrays
    chunk(size) {
        if (size <= 0) throw new Error('Chunk size must be positive');
        
        const result = new EnhancedArray();
        
        for (let i = 0; i < this.length; i += size) {
            const chunk = this.slice(i, i + size);
            result.push(chunk.data);
        }
        
        return result;
    }
    
    // Sort with custom comparator
    sort(compareFunction) {
        if (!compareFunction) {
            compareFunction = (a, b) => {
                const aStr = String(a);
                const bStr = String(b);
                return aStr < bStr ? -1 : aStr > bStr ? 1 : 0;
            };
        }
        
        // Merge sort implementation
        const mergeSort = (arr) => {
            if (arr.length <= 1) return arr;
            
            const mid = Math.floor(arr.length / 2);
            const left = mergeSort(arr.slice(0, mid));
            const right = mergeSort(arr.slice(mid));
            
            return merge(left, right);
        };
        
        const merge = (left, right) => {
            const result = [];
            let leftIndex = 0;
            let rightIndex = 0;
            
            while (leftIndex < left.length && rightIndex < right.length) {
                if (compareFunction(left[leftIndex], right[rightIndex]) <= 0) {
                    result.push(left[leftIndex]);
                    leftIndex++;
                } else {
                    result.push(right[rightIndex]);
                    rightIndex++;
                }
            }
            
            return result.concat(left.slice(leftIndex)).concat(right.slice(rightIndex));
        };
        
        this.data = mergeSort(this.data);
        return this;
    }
    
    // Binary search (requires sorted array)
    binarySearch(target, compareFunction) {
        if (!compareFunction) {
            compareFunction = (a, b) => a < b ? -1 : a > b ? 1 : 0;
        }
        
        let left = 0;
        let right = this.length - 1;
        
        while (left <= right) {
            const mid = Math.floor((left + right) / 2);
            const comparison = compareFunction(this.data[mid], target);
            
            if (comparison === 0) {
                return mid;
            } else if (comparison < 0) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1;
    }
    
    // Convert to regular array
    toArray() {
        return [...this.data];
    }
    
    // String representation
    toString() {
        return this.data.join(',');
    }
    
    // JSON representation
    toJSON() {
        return this.data;
    }
    
    // Iterator implementation
    *[Symbol.iterator]() {
        for (let i = 0; i < this.length; i++) {
            yield this.data[i];
        }
    }
}

// Array Problem-Solving Utilities
class ArrayUtils {
    // Two Sum problem - find indices of two numbers that add up to target
    static twoSum(nums, target) {
        const map = new Map();
        
        for (let i = 0; i < nums.length; i++) {
            const complement = target - nums[i];
            
            if (map.has(complement)) {
                return [map.get(complement), i];
            }
            
            map.set(nums[i], i);
        }
        
        return [];
    }
    
    // Three Sum problem - find all unique triplets that sum to zero
    static threeSum(nums) {
        const result = [];
        nums.sort((a, b) => a - b);
        
        for (let i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] === nums[i - 1]) continue;
            
            let left = i + 1;
            let right = nums.length - 1;
            
            while (left < right) {
                const sum = nums[i] + nums[left] + nums[right];
                
                if (sum === 0) {
                    result.push([nums[i], nums[left], nums[right]]);
                    
                    while (left < right && nums[left] === nums[left + 1]) left++;
                    while (left < right && nums[right] === nums[right - 1]) right--;
                    
                    left++;
                    right--;
                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        
        return result;
    }
    
    // Maximum subarray sum (Kadane's algorithm)
    static maxSubarraySum(nums) {
        if (nums.length === 0) return 0;
        
        let maxSum = nums[0];
        let currentSum = nums[0];
        
        for (let i = 1; i < nums.length; i++) {
            currentSum = Math.max(nums[i], currentSum + nums[i]);
            maxSum = Math.max(maxSum, currentSum);
        }
        
        return maxSum;
    }
    
    // Product of array except self
    static productExceptSelf(nums) {
        const result = new Array(nums.length);
        
        // Left pass
        result[0] = 1;
        for (let i = 1; i < nums.length; i++) {
            result[i] = result[i - 1] * nums[i - 1];
        }
        
        // Right pass
        let rightProduct = 1;
        for (let i = nums.length - 1; i >= 0; i--) {
            result[i] *= rightProduct;
            rightProduct *= nums[i];
        }
        
        return result;
    }
    
    // Rotate array right by k steps
    static rotateArray(nums, k) {
        const n = nums.length;
        k = k % n;
        
        const reverse = (start, end) => {
            while (start < end) {
                [nums[start], nums[end]] = [nums[end], nums[start]];
                start++;
                end--;
            }
        };
        
        reverse(0, n - 1);
        reverse(0, k - 1);
        reverse(k, n - 1);
        
        return nums;
    }
    
    // Merge sorted arrays
    static mergeSortedArrays(nums1, m, nums2, n) {
        let i = m - 1;
        let j = n - 1;
        let k = m + n - 1;
        
        while (i >= 0 && j >= 0) {
            if (nums1[i] > nums2[j]) {
                nums1[k] = nums1[i];
                i--;
            } else {
                nums1[k] = nums2[j];
                j--;
            }
            k--;
        }
        
        while (j >= 0) {
            nums1[k] = nums2[j];
            j--;
            k--;
        }
        
        return nums1;
    }
}

// Usage Examples
const arr = new EnhancedArray(1, 2, 3, 4, 5);

// Basic operations
console.log(arr.map(x => x * 2)); // [2, 4, 6, 8, 10]
console.log(arr.filter(x => x % 2 === 0)); // [2, 4]
console.log(arr.reduce((sum, x) => sum + x, 0)); // 15

// Advanced operations
const nestedArr = new EnhancedArray([1, 2], [3, [4, 5]], 6);
console.log(nestedArr.flatten()); // [1, 2, 3, 4, 5, 6]

const duplicates = new EnhancedArray(1, 2, 2, 3, 3, 3);
console.log(duplicates.unique()); // [1, 2, 3]

// Algorithm examples
console.log(ArrayUtils.twoSum([2, 7, 11, 15], 9)); // [0, 1]
console.log(ArrayUtils.maxSubarraySum([-2, 1, -3, 4, -1, 2, 1, -5, 4])); // 6
```

### 🎯 Objects & Hash Maps

> **Interview Key Point:** Objects in JavaScript serve as hash maps and are essential for O(1) lookups. Understanding object property access, iteration, and hash map implementations is crucial for optimizing algorithmic solutions.

#### **Advanced Object & Hash Map Implementation**

```javascript
// Custom Hash Map Implementation
class HashMap {
    constructor(initialCapacity = 16, loadFactor = 0.75) {
        this.buckets = new Array(initialCapacity).fill(null).map(() => []);
        this.size = 0;
        this.capacity = initialCapacity;
        this.loadFactor = loadFactor;
    }
    
    // Hash function
    hash(key) {
        let hash = 0;
        const str = String(key);
        
        for (let i = 0; i < str.length; i++) {
            const char = str.charCodeAt(i);
            hash = ((hash << 5) - hash) + char;
            hash = hash & hash; // Convert to 32-bit integer
        }
        
        return Math.abs(hash) % this.capacity;
    }
    
    // Set key-value pair
    set(key, value) {
        const index = this.hash(key);
        const bucket = this.buckets[index];
        
        // Check if key already exists
        for (let i = 0; i < bucket.length; i++) {
            if (bucket[i][0] === key) {
                bucket[i][1] = value;
                return this;
            }
        }
        
        // Add new key-value pair
        bucket.push([key, value]);
        this.size++;
        
        // Resize if load factor exceeded
        if (this.size > this.capacity * this.loadFactor) {
            this.resize();
        }
        
        return this;
    }
    
    // Get value by key
    get(key) {
        const index = this.hash(key);
        const bucket = this.buckets[index];
        
        for (const [k, v] of bucket) {
            if (k === key) {
                return v;
            }
        }
        
        return undefined;
    }
    
    // Check if key exists
    has(key) {
        const index = this.hash(key);
        const bucket = this.buckets[index];
        
        return bucket.some(([k]) => k === key);
    }
    
    // Delete key-value pair
    delete(key) {
        const index = this.hash(key);
        const bucket = this.buckets[index];
        
        for (let i = 0; i < bucket.length; i++) {
            if (bucket[i][0] === key) {
                bucket.splice(i, 1);
                this.size--;
                return true;
            }
        }
        
        return false;
    }
    
    // Resize hash map
    resize() {
        const oldBuckets = this.buckets;
        this.capacity *= 2;
        this.buckets = new Array(this.capacity).fill(null).map(() => []);
        this.size = 0;
        
        // Rehash all existing entries
        for (const bucket of oldBuckets) {
            for (const [key, value] of bucket) {
                this.set(key, value);
            }
        }
    }
    
    // Get all keys
    keys() {
        const keys = [];
        for (const bucket of this.buckets) {
            for (const [key] of bucket) {
                keys.push(key);
            }
        }
        return keys;
    }
    
    // Get all values
    values() {
        const values = [];
        for (const bucket of this.buckets) {
            for (const [, value] of bucket) {
                values.push(value);
            }
        }
        return values;
    }
    
    // Get all entries
    entries() {
        const entries = [];
        for (const bucket of this.buckets) {
            for (const entry of bucket) {
                entries.push([...entry]);
            }
        }
        return entries;
    }
    
    // Clear all entries
    clear() {
        this.buckets = new Array(this.capacity).fill(null).map(() => []);
        this.size = 0;
    }
    
    // Iterator implementation
    *[Symbol.iterator]() {
        for (const bucket of this.buckets) {
            for (const [key, value] of bucket) {
                yield [key, value];
            }
        }
    }
    
    // Get load factor
    getLoadFactor() {
        return this.size / this.capacity;
    }
    
    // Get statistics
    getStats() {
        const bucketSizes = this.buckets.map(bucket => bucket.length);
        const maxBucketSize = Math.max(...bucketSizes);
        const emptyBuckets = bucketSizes.filter(size => size === 0).length;
        
        return {
            size: this.size,
            capacity: this.capacity,
            loadFactor: this.getLoadFactor(),
            maxBucketSize,
            emptyBuckets,
            averageBucketSize: this.size / this.capacity
        };
    }
}

// Object Problem-Solving Utilities
class ObjectUtils {
    // Deep clone object
    static deepClone(obj) {
        if (obj === null || typeof obj !== 'object') {
            return obj;
        }
        
        if (obj instanceof Date) {
            return new Date(obj);
        }
        
        if (obj instanceof Array) {
            return obj.map(item => ObjectUtils.deepClone(item));
        }
        
        if (obj instanceof Set) {
            return new Set([...obj].map(item => ObjectUtils.deepClone(item)));
        }
        
        if (obj instanceof Map) {
            const clonedMap = new Map();
            for (const [key, value] of obj) {
                clonedMap.set(ObjectUtils.deepClone(key), ObjectUtils.deepClone(value));
            }
            return clonedMap;
        }
        
        if (typeof obj === 'object') {
            const cloned = {};
            for (const key in obj) {
                if (obj.hasOwnProperty(key)) {
                    cloned[key] = ObjectUtils.deepClone(obj[key]);
                }
            }
            return cloned;
        }
        
        return obj;
    }
    
    // Deep merge objects
    static deepMerge(target, ...sources) {
        if (!sources.length) return target;
        const source = sources.shift();
        
        if (ObjectUtils.isObject(target) && ObjectUtils.isObject(source)) {
            for (const key in source) {
                if (ObjectUtils.isObject(source[key])) {
                    if (!target[key]) Object.assign(target, { [key]: {} });
                    ObjectUtils.deepMerge(target[key], source[key]);
                } else {
                    Object.assign(target, { [key]: source[key] });
                }
            }
        }
        
        return ObjectUtils.deepMerge(target, ...sources);
    }
    
    // Check if value is object
    static isObject(item) {
        return item && typeof item === 'object' && !Array.isArray(item);
    }
    
    // Get value by dot notation path
    static get(obj, path, defaultValue = undefined) {
        const keys = path.split('.');
        let current = obj;
        
        for (const key of keys) {
            if (current === null || current === undefined || !(key in current)) {
                return defaultValue;
            }
            current = current[key];
        }
        
        return current;
    }
    
    // Set value by dot notation path
    static set(obj, path, value) {
        const keys = path.split('.');
        let current = obj;
        
        for (let i = 0; i < keys.length - 1; i++) {
            const key = keys[i];
            
            if (!(key in current) || !ObjectUtils.isObject(current[key])) {
                current[key] = {};
            }
            
            current = current[key];
        }
        
        current[keys[keys.length - 1]] = value;
        return obj;
    }
    
    // Flatten nested object
    static flatten(obj, prefix = '', separator = '.') {
        const flattened = {};
        
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                const newKey = prefix ? `${prefix}${separator}${key}` : key;
                
                if (ObjectUtils.isObject(obj[key])) {
                    Object.assign(flattened, ObjectUtils.flatten(obj[key], newKey, separator));
                } else {
                    flattened[newKey] = obj[key];
                }
            }
        }
        
        return flattened;
    }
    
    // Unflatten object
    static unflatten(obj, separator = '.') {
        const result = {};
        
        for (const key in obj) {
            if (obj.hasOwnProperty(key)) {
                ObjectUtils.set(result, key.replace(new RegExp(separator, 'g'), '.'), obj[key]);
            }
        }
        
        return result;
    }
    
    // Compare objects for equality
    static isEqual(obj1, obj2) {
        if (obj1 === obj2) return true;
        
        if (obj1 == null || obj2 == null) return obj1 === obj2;
        
        if (typeof obj1 !== typeof obj2) return false;
        
        if (typeof obj1 !== 'object') return obj1 === obj2;
        
        if (Array.isArray(obj1) !== Array.isArray(obj2)) return false;
        
        const keys1 = Object.keys(obj1);
        const keys2 = Object.keys(obj2);
        
        if (keys1.length !== keys2.length) return false;
        
        for (const key of keys1) {
            if (!keys2.includes(key)) return false;
            if (!ObjectUtils.isEqual(obj1[key], obj2[key])) return false;
        }
        
        return true;
    }
    
    // Group array of objects by key
    static groupBy(array, key) {
        return array.reduce((groups, item) => {
            const group = typeof key === 'function' ? key(item) : item[key];
            groups[group] = groups[group] || [];
            groups[group].push(item);
            return groups;
        }, {});
    }
    
    // Pick specific keys from object
    static pick(obj, keys) {
        const result = {};
        for (const key of keys) {
            if (key in obj) {
                result[key] = obj[key];
            }
        }
        return result;
    }
    
    // Omit specific keys from object
    static omit(obj, keys) {
        const result = {};
        for (const key in obj) {
            if (obj.hasOwnProperty(key) && !keys.includes(key)) {
                result[key] = obj[key];
            }
        }
        return result;
    }
}

// Usage Examples
const hashMap = new HashMap();

// Basic operations
hashMap.set('name', 'John');
hashMap.set('age', 30);
hashMap.set('city', 'New York');

console.log(hashMap.get('name')); // 'John'
console.log(hashMap.has('age')); // true
console.log(hashMap.size); // 3

// Iteration
for (const [key, value] of hashMap) {
    console.log(`${key}: ${value}`);
}

// Object utilities
const obj1 = { a: 1, b: { c: 2, d: 3 } };
const obj2 = { b: { e: 4 }, f: 5 };

const merged = ObjectUtils.deepMerge({}, obj1, obj2);
console.log(merged); // { a: 1, b: { c: 2, d: 3, e: 4 }, f: 5 }

const flattened = ObjectUtils.flatten(obj1);
console.log(flattened); // { a: 1, 'b.c': 2, 'b.d': 3 }
```

### 🎯 Sets & Maps

> **Interview Key Point:** Sets and Maps provide efficient ways to store unique values and key-value pairs respectively. Understanding their methods, iteration patterns, and use cases is essential for solving problems involving uniqueness and fast lookups.

#### **Advanced Set Implementation & Operations**

```javascript
// Enhanced Set with additional functionality
class EnhancedSet {
    constructor(iterable = []) {
        this.data = new Map();
        this.size = 0;
        
        if (iterable) {
            for (const value of iterable) {
                this.add(value);
            }
        }
    }
    
    // Add value to set
    add(value) {
        if (!this.data.has(value)) {
            this.data.set(value, true);
            this.size++;
        }
        return this;
    }
    
    // Check if value exists
    has(value) {
        return this.data.has(value);
    }
    
    // Delete value from set
    delete(value) {
        if (this.data.has(value)) {
            this.data.delete(value);
            this.size--;
            return true;
        }
        return false;
    }
    
    // Clear all values
    clear() {
        this.data.clear();
        this.size = 0;
    }
    
    // Convert to array
    toArray() {
        return Array.from(this.data.keys());
    }
    
    // Set operations
    
    // Union with another set
    union(otherSet) {
        const result = new EnhancedSet(this);
        for (const value of otherSet) {
            result.add(value);
        }
        return result;
    }
    
    // Intersection with another set
    intersection(otherSet) {
        const result = new EnhancedSet();
        const smaller = this.size <= otherSet.size ? this : otherSet;
        const larger = this.size > otherSet.size ? this : otherSet;
        
        for (const value of smaller) {
            if (larger.has(value)) {
                result.add(value);
            }
        }
        return result;
    }
    
    // Difference (values in this set but not in other)
    difference(otherSet) {
        const result = new EnhancedSet();
        for (const value of this) {
            if (!otherSet.has(value)) {
                result.add(value);
            }
        }
        return result;
    }
    
    // Symmetric difference (values in either set but not in both)
    symmetricDifference(otherSet) {
        const result = new EnhancedSet();
        
        for (const value of this) {
            if (!otherSet.has(value)) {
                result.add(value);
            }
        }
        
        for (const value of otherSet) {
            if (!this.has(value)) {
                result.add(value);
            }
        }
        
        return result;
    }
    
    // Check if this is a subset of another set
    isSubsetOf(otherSet) {
        if (this.size > otherSet.size) return false;
        
        for (const value of this) {
            if (!otherSet.has(value)) {
                return false;
            }
        }
        return true;
    }
    
    // Check if this is a superset of another set
    isSupersetOf(otherSet) {
        return otherSet.isSubsetOf(this);
    }
    
    // Check if sets are disjoint (no common elements)
    isDisjointFrom(otherSet) {
        const smaller = this.size <= otherSet.size ? this : otherSet;
        const larger = this.size > otherSet.size ? this : otherSet;
        
        for (const value of smaller) {
            if (larger.has(value)) {
                return false;
            }
        }
        return true;
    }
    
    // Filter set based on predicate
    filter(predicate) {
        const result = new EnhancedSet();
        for (const value of this) {
            if (predicate(value)) {
                result.add(value);
            }
        }
        return result;
    }
    
    // Map set values to new set
    map(mapper) {
        const result = new EnhancedSet();
        for (const value of this) {
            result.add(mapper(value));
        }
        return result;
    }
    
    // Reduce set to single value
    reduce(reducer, initialValue) {
        let accumulator = initialValue;
        let isFirst = arguments.length < 2;
        
        for (const value of this) {
            if (isFirst) {
                accumulator = value;
                isFirst = false;
            } else {
                accumulator = reducer(accumulator, value);
            }
        }
        
        return accumulator;
    }
    
    // Check if any value satisfies predicate
    some(predicate) {
        for (const value of this) {
            if (predicate(value)) {
                return true;
            }
        }
        return false;
    }
    
    // Check if all values satisfy predicate
    every(predicate) {
        for (const value of this) {
            if (!predicate(value)) {
                return false;
            }
        }
        return true;
    }
    
    // Find first value that satisfies predicate
    find(predicate) {
        for (const value of this) {
            if (predicate(value)) {
                return value;
            }
        }
        return undefined;
    }
    
    // Iterator implementation
    *[Symbol.iterator]() {
        for (const value of this.data.keys()) {
            yield value;
        }
    }
    
    // String representation
    toString() {
        return `EnhancedSet(${this.size}) {${Array.from(this).join(', ')}}`;
    }
}

// Enhanced Map with additional functionality
class EnhancedMap {
    constructor(iterable = []) {
        this.data = new Map();
        this.size = 0;
        
        if (iterable) {
            for (const [key, value] of iterable) {
                this.set(key, value);
            }
        }
    }
    
    // Set key-value pair
    set(key, value) {
        if (!this.data.has(key)) {
            this.size++;
        }
        this.data.set(key, value);
        return this;
    }
    
    // Get value by key
    get(key) {
        return this.data.get(key);
    }
    
    // Check if key exists
    has(key) {
        return this.data.has(key);
    }
    
    // Delete key-value pair
    delete(key) {
        if (this.data.has(key)) {
            this.data.delete(key);
            this.size--;
            return true;
        }
        return false;
    }
    
    // Clear all entries
    clear() {
        this.data.clear();
        this.size = 0;
    }
    
    // Get all keys
    keys() {
        return this.data.keys();
    }
    
    // Get all values
    values() {
        return this.data.values();
    }
    
    // Get all entries
    entries() {
        return this.data.entries();
    }
    
    // Advanced operations
    
    // Get value with default if key doesn't exist
    getWithDefault(key, defaultValue) {
        return this.has(key) ? this.get(key) : defaultValue;
    }
    
    // Set value only if key doesn't exist
    setIfAbsent(key, value) {
        if (!this.has(key)) {
            this.set(key, value);
            return true;
        }
        return false;
    }
    
    // Update value using function
    update(key, updateFunction, defaultValue) {
        const currentValue = this.has(key) ? this.get(key) : defaultValue;
        const newValue = updateFunction(currentValue);
        this.set(key, newValue);
        return newValue;
    }
    
    // Merge with another map
    merge(otherMap, mergeFunction) {
        for (const [key, value] of otherMap) {
            if (this.has(key) && mergeFunction) {
                this.set(key, mergeFunction(this.get(key), value));
            } else {
                this.set(key, value);
            }
        }
        return this;
    }
    
    // Filter map based on predicate
    filter(predicate) {
        const result = new EnhancedMap();
        for (const [key, value] of this) {
            if (predicate(key, value)) {
                result.set(key, value);
            }
        }
        return result;
    }
    
    // Map values to new map
    mapValues(mapper) {
        const result = new EnhancedMap();
        for (const [key, value] of this) {
            result.set(key, mapper(value, key));
        }
        return result;
    }
    
    // Map keys to new map
    mapKeys(mapper) {
        const result = new EnhancedMap();
        for (const [key, value] of this) {
            result.set(mapper(key, value), value);
        }
        return result;
    }
    
    // Reduce map to single value
    reduce(reducer, initialValue) {
        let accumulator = initialValue;
        let isFirst = arguments.length < 2;
        
        for (const [key, value] of this) {
            if (isFirst) {
                accumulator = value;
                isFirst = false;
            } else {
                accumulator = reducer(accumulator, value, key);
            }
        }
        
        return accumulator;
    }
    
    // Group values by key function
    groupBy(keyFunction) {
        const result = new EnhancedMap();
        for (const [key, value] of this) {
            const groupKey = keyFunction(key, value);
            if (!result.has(groupKey)) {
                result.set(groupKey, []);
            }
            result.get(groupKey).push([key, value]);
        }
        return result;
    }
    
    // Convert to object (if keys are strings)
    toObject() {
        const obj = {};
        for (const [key, value] of this) {
            obj[key] = value;
        }
        return obj;
    }
    
    // Convert to array of entries
    toArray() {
        return Array.from(this.data.entries());
    }
    
    // Find entry that satisfies predicate
    find(predicate) {
        for (const [key, value] of this) {
            if (predicate(key, value)) {
                return [key, value];
            }
        }
        return undefined;
    }
    
    // Check if any entry satisfies predicate
    some(predicate) {
        for (const [key, value] of this) {
            if (predicate(key, value)) {
                return true;
            }
        }
        return false;
    }
    
    // Check if all entries satisfy predicate
    every(predicate) {
        for (const [key, value] of this) {
            if (!predicate(key, value)) {
                return false;
            }
        }
        return true;
    }
    
    // Iterator implementation
    *[Symbol.iterator]() {
        for (const entry of this.data.entries()) {
            yield entry;
        }
    }
    
    // String representation
    toString() {
        const entries = Array.from(this).map(([k, v]) => `${k} => ${v}`).join(', ');
        return `EnhancedMap(${this.size}) {${entries}}`;
    }
}

// Set and Map Problem-Solving Utilities
class SetMapUtils {
    // Find unique elements in array
    static findUnique(arr) {
        return [...new Set(arr)];
    }
    
    // Find duplicates in array
    static findDuplicates(arr) {
        const seen = new Set();
        const duplicates = new Set();
        
        for (const item of arr) {
            if (seen.has(item)) {
                duplicates.add(item);
            } else {
                seen.add(item);
            }
        }
        
        return [...duplicates];
    }
    
    // Count frequency of elements
    static countFrequency(arr) {
        const frequencyMap = new Map();
        
        for (const item of arr) {
            frequencyMap.set(item, (frequencyMap.get(item) || 0) + 1);
        }
        
        return frequencyMap;
    }
    
    // Find most frequent element
    static findMostFrequent(arr) {
        const frequencyMap = SetMapUtils.countFrequency(arr);
        let maxCount = 0;
        let mostFrequent = null;
        
        for (const [item, count] of frequencyMap) {
            if (count > maxCount) {
                maxCount = count;
                mostFrequent = item;
            }
        }
        
        return { element: mostFrequent, count: maxCount };
    }
    
    // Check if arrays have common elements
    static hasCommonElements(arr1, arr2) {
        const set1 = new Set(arr1);
        return arr2.some(item => set1.has(item));
    }
    
    // Find common elements between arrays
    static findCommonElements(arr1, arr2) {
        const set1 = new Set(arr1);
        const common = new Set();
        
        for (const item of arr2) {
            if (set1.has(item)) {
                common.add(item);
            }
        }
        
        return [...common];
    }
    
    // Check if one array is subset of another
    static isSubset(subset, superset) {
        const supersetSet = new Set(superset);
        return subset.every(item => supersetSet.has(item));
    }
    
    // Create LRU Cache using Map
    static createLRUCache(capacity) {
        const cache = new Map();
        
        return {
            get(key) {
                if (cache.has(key)) {
                    const value = cache.get(key);
                    cache.delete(key);
                    cache.set(key, value);
                    return value;
                }
                return undefined;
            },
            
            set(key, value) {
                if (cache.has(key)) {
                    cache.delete(key);
                } else if (cache.size >= capacity) {
                    const firstKey = cache.keys().next().value;
                    cache.delete(firstKey);
                }
                cache.set(key, value);
            },
            
            has(key) {
                return cache.has(key);
            },
            
            delete(key) {
                return cache.delete(key);
            },
            
            clear() {
                cache.clear();
            },
            
            get size() {
                return cache.size;
            }
        };
    }
}

// Usage Examples
const set1 = new EnhancedSet([1, 2, 3, 4]);
const set2 = new EnhancedSet([3, 4, 5, 6]);

console.log(set1.union(set2)); // {1, 2, 3, 4, 5, 6}
console.log(set1.intersection(set2)); // {3, 4}
console.log(set1.difference(set2)); // {1, 2}

const map = new EnhancedMap([['a', 1], ['b', 2], ['c', 3]]);
const doubledValues = map.mapValues(value => value * 2);
console.log(doubledValues); // {a => 2, b => 4, c => 6}

// LRU Cache example
const lruCache = SetMapUtils.createLRUCache(3);
lruCache.set('a', 1);
lruCache.set('b', 2);
lruCache.set('c', 3);
lruCache.set('d', 4); // 'a' gets evicted
console.log(lruCache.has('a')); // false
console.log(lruCache.get('b')); // 2
```

### 🎯 Stacks & Queues

> **Interview Key Point:** Stacks (LIFO) and Queues (FIFO) are fundamental data structures that form the basis for many algorithms. Understanding their implementations and use cases is essential for solving problems involving order, backtracking, and breadth-first operations.

#### **Advanced Stack Implementation**

```javascript
// Enhanced Stack with additional functionality
class EnhancedStack {
    constructor(maxSize = Infinity) {
        this.items = [];
        this.maxSize = maxSize;
        this.minStack = []; // For O(1) min operations
    }
    
    // Push item to stack
    push(item) {
        if (this.items.length >= this.maxSize) {
            throw new Error('Stack overflow');
        }
        
        this.items.push(item);
        
        // Update min stack
        if (this.minStack.length === 0 || item <= this.getMin()) {
            this.minStack.push(item);
        }
        
        return this.size();
    }
    
    // Pop item from stack
    pop() {
        if (this.isEmpty()) {
            throw new Error('Stack underflow');
        }
        
        const item = this.items.pop();
        
        // Update min stack
        if (item === this.getMin()) {
            this.minStack.pop();
        }
        
        return item;
    }
    
    // Peek at top item without removing
    peek() {
        if (this.isEmpty()) {
            return undefined;
        }
        return this.items[this.items.length - 1];
    }
    
    // Get minimum element in O(1)
    getMin() {
        if (this.minStack.length === 0) {
            return undefined;
        }
        return this.minStack[this.minStack.length - 1];
    }
    
    // Check if stack is empty
    isEmpty() {
        return this.items.length === 0;
    }
    
    // Get stack size
    size() {
        return this.items.length;
    }
    
    // Check if stack is full
    isFull() {
        return this.items.length >= this.maxSize;
    }
    
    // Clear all items
    clear() {
        this.items = [];
        this.minStack = [];
    }
    
    // Convert to array
    toArray() {
        return [...this.items];
    }
    
    // Search for item (returns position from top, -1 if not found)
    search(item) {
        for (let i = this.items.length - 1; i >= 0; i--) {
            if (this.items[i] === item) {
                return this.items.length - 1 - i;
            }
        }
        return -1;
    }
    
    // Filter stack based on predicate
    filter(predicate) {
        const result = new EnhancedStack(this.maxSize);
        for (let i = 0; i < this.items.length; i++) {
            if (predicate(this.items[i], i)) {
                result.push(this.items[i]);
            }
        }
        return result;
    }
    
    // Map stack items to new stack
    map(mapper) {
        const result = new EnhancedStack(this.maxSize);
        for (let i = 0; i < this.items.length; i++) {
            result.push(mapper(this.items[i], i));
        }
        return result;
    }
    
    // Reverse stack
    reverse() {
        const result = new EnhancedStack(this.maxSize);
        for (let i = 0; i < this.items.length; i++) {
            result.push(this.items[i]);
        }
        return result;
    }
    
    // Iterator implementation
    *[Symbol.iterator]() {
        for (let i = this.items.length - 1; i >= 0; i--) {
            yield this.items[i];
        }
    }
    
    // String representation
    toString() {
        return `Stack(${this.size()}) [${this.items.join(', ')}] (top: ${this.peek()})`;
    }
}

// Enhanced Queue with additional functionality
class EnhancedQueue {
    constructor(maxSize = Infinity) {
        this.items = [];
        this.front = 0;
        this.rear = 0;
        this.maxSize = maxSize;
    }
    
    // Enqueue item to rear
    enqueue(item) {
        if (this.size() >= this.maxSize) {
            throw new Error('Queue overflow');
        }
        
        this.items[this.rear] = item;
        this.rear++;
        return this.size();
    }
    
    // Dequeue item from front
    dequeue() {
        if (this.isEmpty()) {
            throw new Error('Queue underflow');
        }
        
        const item = this.items[this.front];
        delete this.items[this.front];
        this.front++;
        
        // Reset pointers when queue becomes empty
        if (this.front === this.rear) {
            this.front = 0;
            this.rear = 0;
            this.items = [];
        }
        
        return item;
    }
    
    // Peek at front item without removing
    peek() {
        if (this.isEmpty()) {
            return undefined;
        }
        return this.items[this.front];
    }
    
    // Peek at rear item
    peekRear() {
        if (this.isEmpty()) {
            return undefined;
        }
        return this.items[this.rear - 1];
    }
    
    // Check if queue is empty
    isEmpty() {
        return this.front === this.rear;
    }
    
    // Get queue size
    size() {
        return this.rear - this.front;
    }
    
    // Check if queue is full
    isFull() {
        return this.size() >= this.maxSize;
    }
    
    // Clear all items
    clear() {
        this.items = [];
        this.front = 0;
        this.rear = 0;
    }
    
    // Convert to array (from front to rear)
    toArray() {
        const result = [];
        for (let i = this.front; i < this.rear; i++) {
            result.push(this.items[i]);
        }
        return result;
    }
    
    // Search for item (returns position from front, -1 if not found)
    search(item) {
        for (let i = this.front; i < this.rear; i++) {
            if (this.items[i] === item) {
                return i - this.front;
            }
        }
        return -1;
    }
    
    // Filter queue based on predicate
    filter(predicate) {
        const result = new EnhancedQueue(this.maxSize);
        for (let i = this.front; i < this.rear; i++) {
            if (predicate(this.items[i], i - this.front)) {
                result.enqueue(this.items[i]);
            }
        }
        return result;
    }
    
    // Map queue items to new queue
    map(mapper) {
        const result = new EnhancedQueue(this.maxSize);
        for (let i = this.front; i < this.rear; i++) {
            result.enqueue(mapper(this.items[i], i - this.front));
        }
        return result;
    }
    
    // Reverse queue
    reverse() {
        const result = new EnhancedQueue(this.maxSize);
        for (let i = this.rear - 1; i >= this.front; i--) {
            result.enqueue(this.items[i]);
        }
        return result;
    }
    
    // Iterator implementation (front to rear)
    *[Symbol.iterator]() {
        for (let i = this.front; i < this.rear; i++) {
            yield this.items[i];
        }
    }
    
    // String representation
    toString() {
        return `Queue(${this.size()}) [${this.toArray().join(', ')}] (front: ${this.peek()}, rear: ${this.peekRear()})`;
    }
}

// Priority Queue implementation
class PriorityQueue {
    constructor(compareFunction) {
        this.items = [];
        this.compare = compareFunction || ((a, b) => a.priority - b.priority);
    }
    
    // Enqueue with priority
    enqueue(item, priority = 0) {
        const element = { item, priority };
        
        if (this.isEmpty()) {
            this.items.push(element);
        } else {
            let added = false;
            for (let i = 0; i < this.items.length; i++) {
                if (this.compare(element, this.items[i]) < 0) {
                    this.items.splice(i, 0, element);
                    added = true;
                    break;
                }
            }
            if (!added) {
                this.items.push(element);
            }
        }
        
        return this.size();
    }
    
    // Dequeue highest priority item
    dequeue() {
        if (this.isEmpty()) {
            throw new Error('Priority queue is empty');
        }
        return this.items.shift().item;
    }
    
    // Peek at highest priority item
    peek() {
        if (this.isEmpty()) {
            return undefined;
        }
        return this.items[0].item;
    }
    
    // Check if queue is empty
    isEmpty() {
        return this.items.length === 0;
    }
    
    // Get queue size
    size() {
        return this.items.length;
    }
    
    // Clear all items
    clear() {
        this.items = [];
    }
    
    // Convert to array of items
    toArray() {
        return this.items.map(element => element.item);
    }
    
    // String representation
    toString() {
        const itemsStr = this.items.map(el => `${el.item}(${el.priority})`).join(', ');
        return `PriorityQueue(${this.size()}) [${itemsStr}]`;
    }
}

// Deque (Double-ended queue) implementation
class Deque {
    constructor() {
        this.items = [];
    }
    
    // Add to front
    addFront(item) {
        this.items.unshift(item);
        return this.size();
    }
    
    // Add to rear
    addRear(item) {
        this.items.push(item);
        return this.size();
    }
    
    // Remove from front
    removeFront() {
        if (this.isEmpty()) {
            throw new Error('Deque is empty');
        }
        return this.items.shift();
    }
    
    // Remove from rear
    removeRear() {
        if (this.isEmpty()) {
            throw new Error('Deque is empty');
        }
        return this.items.pop();
    }
    
    // Peek at front
    peekFront() {
        if (this.isEmpty()) {
            return undefined;
        }
        return this.items[0];
    }
    
    // Peek at rear
    peekRear() {
        if (this.isEmpty()) {
            return undefined;
        }
        return this.items[this.items.length - 1];
    }
    
    // Check if empty
    isEmpty() {
        return this.items.length === 0;
    }
    
    // Get size
    size() {
        return this.items.length;
    }
    
    // Clear all items
    clear() {
        this.items = [];
    }
    
    // Convert to array
    toArray() {
        return [...this.items];
    }
    
    // String representation
    toString() {
        return `Deque(${this.size()}) [${this.items.join(', ')}]`;
    }
}

// Stack and Queue Problem-Solving Utilities
class StackQueueUtils {
    // Check if parentheses are balanced
    static isBalanced(str) {
        const stack = new EnhancedStack();
        const pairs = { '(': ')', '[': ']', '{': '}' };
        
        for (const char of str) {
            if (char in pairs) {
                stack.push(char);
            } else if (Object.values(pairs).includes(char)) {
                if (stack.isEmpty() || pairs[stack.pop()] !== char) {
                    return false;
                }
            }
        }
        
        return stack.isEmpty();
    }
    
    // Evaluate postfix expression
    static evaluatePostfix(expression) {
        const stack = new EnhancedStack();
        const tokens = expression.split(' ');
        
        for (const token of tokens) {
            if (!isNaN(token)) {
                stack.push(parseFloat(token));
            } else {
                const b = stack.pop();
                const a = stack.pop();
                
                switch (token) {
                    case '+': stack.push(a + b); break;
                    case '-': stack.push(a - b); break;
                    case '*': stack.push(a * b); break;
                    case '/': stack.push(a / b); break;
                    default: throw new Error(`Unknown operator: ${token}`);
                }
            }
        }
        
        return stack.pop();
    }
    
    // Convert infix to postfix
    static infixToPostfix(infix) {
        const stack = new EnhancedStack();
        const result = [];
        const precedence = { '+': 1, '-': 1, '*': 2, '/': 2, '^': 3 };
        
        for (const char of infix) {
            if (!isNaN(char) || char.match(/[a-zA-Z]/)) {
                result.push(char);
            } else if (char === '(') {
                stack.push(char);
            } else if (char === ')') {
                while (!stack.isEmpty() && stack.peek() !== '(') {
                    result.push(stack.pop());
                }
                stack.pop(); // Remove '('
            } else if (char in precedence) {
                while (!stack.isEmpty() && 
                       stack.peek() !== '(' && 
                       precedence[stack.peek()] >= precedence[char]) {
                    result.push(stack.pop());
                }
                stack.push(char);
            }
        }
        
        while (!stack.isEmpty()) {
            result.push(stack.pop());
        }
        
        return result.join(' ');
    }
    
    // Implement stack using queues
    static createStackUsingQueues() {
        const queue1 = new EnhancedQueue();
        const queue2 = new EnhancedQueue();
        
        return {
            push(item) {
                queue1.enqueue(item);
            },
            
            pop() {
                if (queue1.isEmpty()) {
                    throw new Error('Stack is empty');
                }
                
                // Move all but last element to queue2
                while (queue1.size() > 1) {
                    queue2.enqueue(queue1.dequeue());
                }
                
                const item = queue1.dequeue();
                
                // Swap queues
                [queue1, queue2] = [queue2, queue1];
                
                return item;
            },
            
            peek() {
                if (queue1.isEmpty()) {
                    return undefined;
                }
                
                // Move all but last element to queue2
                while (queue1.size() > 1) {
                    queue2.enqueue(queue1.dequeue());
                }
                
                const item = queue1.peek();
                queue2.enqueue(queue1.dequeue());
                
                // Swap queues
                [queue1, queue2] = [queue2, queue1];
                
                return item;
            },
            
            isEmpty() {
                return queue1.isEmpty();
            },
            
            size() {
                return queue1.size();
            }
        };
    }
    
    // Implement queue using stacks
    static createQueueUsingStacks() {
        const stack1 = new EnhancedStack();
        const stack2 = new EnhancedStack();
        
        return {
            enqueue(item) {
                stack1.push(item);
            },
            
            dequeue() {
                if (stack2.isEmpty()) {
                    while (!stack1.isEmpty()) {
                        stack2.push(stack1.pop());
                    }
                }
                
                if (stack2.isEmpty()) {
                    throw new Error('Queue is empty');
                }
                
                return stack2.pop();
            },
            
            peek() {
                if (stack2.isEmpty()) {
                    while (!stack1.isEmpty()) {
                        stack2.push(stack1.pop());
                    }
                }
                
                if (stack2.isEmpty()) {
                    return undefined;
                }
                
                return stack2.peek();
            },
            
            isEmpty() {
                return stack1.isEmpty() && stack2.isEmpty();
            },
            
            size() {
                return stack1.size() + stack2.size();
            }
        };
    }
    
    // Next greater element
    static nextGreaterElement(arr) {
        const stack = new EnhancedStack();
        const result = new Array(arr.length).fill(-1);
        
        for (let i = 0; i < arr.length; i++) {
            while (!stack.isEmpty() && arr[stack.peek()] < arr[i]) {
                const index = stack.pop();
                result[index] = arr[i];
            }
            stack.push(i);
        }
        
        return result;
    }
    
    // Sliding window maximum
    static slidingWindowMaximum(arr, k) {
        const deque = new Deque();
        const result = [];
        
        for (let i = 0; i < arr.length; i++) {
            // Remove elements outside window
            while (!deque.isEmpty() && deque.peekFront() <= i - k) {
                deque.removeFront();
            }
            
            // Remove smaller elements from rear
            while (!deque.isEmpty() && arr[deque.peekRear()] <= arr[i]) {
                deque.removeRear();
            }
            
            deque.addRear(i);
            
            // Add maximum to result when window is complete
            if (i >= k - 1) {
                result.push(arr[deque.peekFront()]);
            }
        }
        
        return result;
    }
}

// Usage Examples
const stack = new EnhancedStack(5);
stack.push(10);
stack.push(5);
stack.push(15);
stack.push(3);

console.log(stack.getMin()); // 3
console.log(stack.pop()); // 3
console.log(stack.getMin()); // 5

const queue = new EnhancedQueue();
queue.enqueue('first');
queue.enqueue('second');
queue.enqueue('third');

console.log(queue.dequeue()); // 'first'
console.log(queue.peek()); // 'second'

// Priority queue example
const pq = new PriorityQueue();
pq.enqueue('low priority task', 1);
pq.enqueue('high priority task', 10);
pq.enqueue('medium priority task', 5);

console.log(pq.dequeue()); // 'high priority task'

// Check balanced parentheses
console.log(StackQueueUtils.isBalanced('({[]})')); // true
console.log(StackQueueUtils.isBalanced('({[}])')); // false

// Evaluate postfix
console.log(StackQueueUtils.evaluatePostfix('3 4 + 2 *')); // 14
```

---

## 2. Advanced Data Structures

> **Interview Explanation:** Advanced data structures provide efficient solutions for complex problems. Understanding their implementations, time complexities, and use cases is crucial for solving challenging algorithmic problems and system design questions.

### 🎯 Linked Lists

> **Interview Key Point:** Linked Lists provide dynamic memory allocation and efficient insertion/deletion operations. Understanding different types of linked lists and their operations is essential for many interview problems.

#### **Comprehensive Linked List Implementation**

```javascript
// Node class for linked list
class ListNode {
    constructor(data, next = null) {
        this.data = data;
        this.next = next;
    }
    
    toString() {
        return `Node(${this.data})`;
    }
}

// Enhanced Singly Linked List
class LinkedList {
    constructor() {
        this.head = null;
        this.tail = null;
        this.size = 0;
    }
    
    // Add element to the beginning
    prepend(data) {
        const newNode = new ListNode(data, this.head);
        this.head = newNode;
        
        if (!this.tail) {
            this.tail = newNode;
        }
        
        this.size++;
        return this;
    }
    
    // Add element to the end
    append(data) {
        const newNode = new ListNode(data);
        
        if (!this.head) {
            this.head = newNode;
            this.tail = newNode;
        } else {
            this.tail.next = newNode;
            this.tail = newNode;
        }
        
        this.size++;
        return this;
    }
    
    // Insert at specific index
    insert(index, data) {
        if (index < 0 || index > this.size) {
            throw new Error('Index out of bounds');
        }
        
        if (index === 0) {
            return this.prepend(data);
        }
        
        if (index === this.size) {
            return this.append(data);
        }
        
        const newNode = new ListNode(data);
        const prevNode = this.getAt(index - 1);
        
        newNode.next = prevNode.next;
        prevNode.next = newNode;
        
        this.size++;
        return this;
    }
    
    // Remove first element
    removeFirst() {
        if (!this.head) {
            return null;
        }
        
        const removedData = this.head.data;
        this.head = this.head.next;
        
        if (!this.head) {
            this.tail = null;
        }
        
        this.size--;
        return removedData;
    }
    
    // Remove last element
    removeLast() {
        if (!this.head) {
            return null;
        }
        
        if (this.head === this.tail) {
            const removedData = this.head.data;
            this.head = null;
            this.tail = null;
            this.size--;
            return removedData;
        }
        
        let current = this.head;
        while (current.next !== this.tail) {
            current = current.next;
        }
        
        const removedData = this.tail.data;
        current.next = null;
        this.tail = current;
        this.size--;
        
        return removedData;
    }
    
    // Remove at specific index
    removeAt(index) {
        if (index < 0 || index >= this.size) {
            throw new Error('Index out of bounds');
        }
        
        if (index === 0) {
            return this.removeFirst();
        }
        
        if (index === this.size - 1) {
            return this.removeLast();
        }
        
        const prevNode = this.getAt(index - 1);
        const removedData = prevNode.next.data;
        prevNode.next = prevNode.next.next;
        
        this.size--;
        return removedData;
    }
    
    // Remove by value
    remove(data) {
        if (!this.head) {
            return false;
        }
        
        if (this.head.data === data) {
            this.removeFirst();
            return true;
        }
        
        let current = this.head;
        while (current.next && current.next.data !== data) {
            current = current.next;
        }
        
        if (current.next) {
            if (current.next === this.tail) {
                this.tail = current;
            }
            current.next = current.next.next;
            this.size--;
            return true;
        }
        
        return false;
    }
    
    // Get element at index
    getAt(index) {
        if (index < 0 || index >= this.size) {
            throw new Error('Index out of bounds');
        }
        
        let current = this.head;
        for (let i = 0; i < index; i++) {
            current = current.next;
        }
        
        return current;
    }
    
    // Find index of element
    indexOf(data) {
        let current = this.head;
        let index = 0;
        
        while (current) {
            if (current.data === data) {
                return index;
            }
            current = current.next;
            index++;
        }
        
        return -1;
    }
    
    // Check if list contains element
    contains(data) {
        return this.indexOf(data) !== -1;
    }
    
    // Get first element
    first() {
        return this.head ? this.head.data : null;
    }
    
    // Get last element
    last() {
        return this.tail ? this.tail.data : null;
    }
    
    // Check if list is empty
    isEmpty() {
        return this.size === 0;
    }
    
    // Get list size
    getSize() {
        return this.size;
    }
    
    // Clear the list
    clear() {
        this.head = null;
        this.tail = null;
        this.size = 0;
    }
    
    // Convert to array
    toArray() {
        const result = [];
        let current = this.head;
        
        while (current) {
            result.push(current.data);
            current = current.next;
        }
        
        return result;
    }
    
    // Reverse the list
    reverse() {
        if (!this.head || !this.head.next) {
            return this;
        }
        
        this.tail = this.head;
        let prev = null;
        let current = this.head;
        
        while (current) {
            const next = current.next;
            current.next = prev;
            prev = current;
            current = next;
        }
        
        this.head = prev;
        return this;
    }
    
    // Find middle element (Floyd's algorithm)
    findMiddle() {
        if (!this.head) {
            return null;
        }
        
        let slow = this.head;
        let fast = this.head;
        
        while (fast && fast.next) {
            slow = slow.next;
            fast = fast.next.next;
        }
        
        return slow.data;
    }
    
    // Detect cycle in list
    hasCycle() {
        if (!this.head) {
            return false;
        }
        
        let slow = this.head;
        let fast = this.head;
        
        while (fast && fast.next) {
            slow = slow.next;
            fast = fast.next.next;
            
            if (slow === fast) {
                return true;
            }
        }
        
        return false;
    }
    
    // Get nth node from end
    getNthFromEnd(n) {
        if (n <= 0 || n > this.size) {
            throw new Error('Invalid position');
        }
        
        let first = this.head;
        let second = this.head;
        
        // Move first pointer n steps ahead
        for (let i = 0; i < n; i++) {
            first = first.next;
        }
        
        // Move both pointers until first reaches end
        while (first) {
            first = first.next;
            second = second.next;
        }
        
        return second.data;
    }
    
    // Merge with another sorted list
    mergeSorted(otherList) {
        const dummy = new ListNode(0);
        let current = dummy;
        let p1 = this.head;
        let p2 = otherList.head;
        
        while (p1 && p2) {
            if (p1.data <= p2.data) {
                current.next = p1;
                p1 = p1.next;
            } else {
                current.next = p2;
                p2 = p2.next;
            }
            current = current.next;
        }
        
        current.next = p1 || p2;
        
        const result = new LinkedList();
        result.head = dummy.next;
        
        // Update tail and size
        let temp = result.head;
        result.size = 0;
        while (temp) {
            result.tail = temp;
            result.size++;
            temp = temp.next;
        }
        
        return result;
    }
    
    // Remove duplicates from sorted list
    removeDuplicates() {
        if (!this.head) {
            return this;
        }
        
        let current = this.head;
        
        while (current && current.next) {
            if (current.data === current.next.data) {
                current.next = current.next.next;
                this.size--;
                
                if (!current.next) {
                    this.tail = current;
                }
            } else {
                current = current.next;
            }
        }
        
        return this;
    }
    
    // Iterator implementation
    *[Symbol.iterator]() {
        let current = this.head;
        while (current) {
            yield current.data;
            current = current.next;
        }
    }
    
    // String representation
    toString() {
        return `LinkedList(${this.size}) [${this.toArray().join(' -> ')}]`;
    }
}

// Doubly Linked List Node
class DoublyListNode {
    constructor(data, prev = null, next = null) {
        this.data = data;
        this.prev = prev;
        this.next = next;
    }
}

// Doubly Linked List
class DoublyLinkedList {
    constructor() {
        this.head = null;
        this.tail = null;
        this.size = 0;
    }
    
    // Add to beginning
    prepend(data) {
        const newNode = new DoublyListNode(data, null, this.head);
        
        if (this.head) {
            this.head.prev = newNode;
        } else {
            this.tail = newNode;
        }
        
        this.head = newNode;
        this.size++;
        return this;
    }
    
    // Add to end
    append(data) {
        const newNode = new DoublyListNode(data, this.tail, null);
        
        if (this.tail) {
            this.tail.next = newNode;
        } else {
            this.head = newNode;
        }
        
        this.tail = newNode;
        this.size++;
        return this;
    }
    
    // Insert at index
    insert(index, data) {
        if (index < 0 || index > this.size) {
            throw new Error('Index out of bounds');
        }
        
        if (index === 0) {
            return this.prepend(data);
        }
        
        if (index === this.size) {
            return this.append(data);
        }
        
        const current = this.getAt(index);
        const newNode = new DoublyListNode(data, current.prev, current);
        
        current.prev.next = newNode;
        current.prev = newNode;
        
        this.size++;
        return this;
    }
    
    // Remove first
    removeFirst() {
        if (!this.head) {
            return null;
        }
        
        const removedData = this.head.data;
        this.head = this.head.next;
        
        if (this.head) {
            this.head.prev = null;
        } else {
            this.tail = null;
        }
        
        this.size--;
        return removedData;
    }
    
    // Remove last
    removeLast() {
        if (!this.tail) {
            return null;
        }
        
        const removedData = this.tail.data;
        this.tail = this.tail.prev;
        
        if (this.tail) {
            this.tail.next = null;
        } else {
            this.head = null;
        }
        
        this.size--;
        return removedData;
    }
    
    // Get element at index
    getAt(index) {
        if (index < 0 || index >= this.size) {
            throw new Error('Index out of bounds');
        }
        
        let current;
        
        // Choose direction based on index
        if (index < this.size / 2) {
            current = this.head;
            for (let i = 0; i < index; i++) {
                current = current.next;
            }
        } else {
            current = this.tail;
            for (let i = this.size - 1; i > index; i--) {
                current = current.prev;
            }
        }
        
        return current;
    }
    
    // Convert to array (forward)
    toArray() {
        const result = [];
        let current = this.head;
        
        while (current) {
            result.push(current.data);
            current = current.next;
        }
        
        return result;
    }
    
    // Convert to array (backward)
    toArrayReverse() {
        const result = [];
        let current = this.tail;
        
        while (current) {
            result.push(current.data);
            current = current.prev;
        }
        
        return result;
    }
    
    // Reverse iterator
    *reverseIterator() {
        let current = this.tail;
        while (current) {
            yield current.data;
            current = current.prev;
        }
    }
    
    // String representation
    toString() {
        return `DoublyLinkedList(${this.size}) [${this.toArray().join(' <-> ')}]`;
    }
}

// Linked List Problem-Solving Utilities
class LinkedListUtils {
    // Merge two sorted linked lists
    static mergeTwoSortedLists(list1, list2) {
        const dummy = new ListNode(0);
        let current = dummy;
        let p1 = list1.head;
        let p2 = list2.head;
        
        while (p1 && p2) {
            if (p1.data <= p2.data) {
                current.next = new ListNode(p1.data);
                p1 = p1.next;
            } else {
                current.next = new ListNode(p2.data);
                p2 = p2.next;
            }
            current = current.next;
        }
        
        while (p1) {
            current.next = new ListNode(p1.data);
            current = current.next;
            p1 = p1.next;
        }
        
        while (p2) {
            current.next = new ListNode(p2.data);
            current = current.next;
            p2 = p2.next;
        }
        
        const result = new LinkedList();
        result.head = dummy.next;
        
        // Update size and tail
        let temp = result.head;
        result.size = 0;
        while (temp) {
            result.tail = temp;
            result.size++;
            temp = temp.next;
        }
        
        return result;
    }
    
    // Remove duplicates from unsorted list
    static removeDuplicatesUnsorted(list) {
        if (!list.head) {
            return list;
        }
        
        const seen = new Set();
        let current = list.head;
        let prev = null;
        
        while (current) {
            if (seen.has(current.data)) {
                prev.next = current.next;
                if (current === list.tail) {
                    list.tail = prev;
                }
                list.size--;
            } else {
                seen.add(current.data);
                prev = current;
            }
            current = current.next;
        }
        
        return list;
    }
    
    // Partition list around value
    static partition(list, x) {
        let beforeHead = null, beforeTail = null;
        let afterHead = null, afterTail = null;
        
        let current = list.head;
        
        while (current) {
            const next = current.next;
            current.next = null;
            
            if (current.data < x) {
                if (!beforeHead) {
                    beforeHead = current;
                    beforeTail = current;
                } else {
                    beforeTail.next = current;
                    beforeTail = current;
                }
            } else {
                if (!afterHead) {
                    afterHead = current;
                    afterTail = current;
                } else {
                    afterTail.next = current;
                    afterTail = current;
                }
            }
            
            current = next;
        }
        
        const result = new LinkedList();
        
        if (!beforeHead) {
            result.head = afterHead;
            result.tail = afterTail;
        } else if (!afterHead) {
            result.head = beforeHead;
            result.tail = beforeTail;
        } else {
            beforeTail.next = afterHead;
            result.head = beforeHead;
            result.tail = afterTail;
        }
        
        // Recalculate size
        let temp = result.head;
        result.size = 0;
        while (temp) {
            result.size++;
            temp = temp.next;
        }
        
        return result;
    }
    
    // Add two numbers represented as linked lists
    static addTwoNumbers(list1, list2) {
        const result = new LinkedList();
        let p1 = list1.head;
        let p2 = list2.head;
        let carry = 0;
        
        while (p1 || p2 || carry) {
            const sum = (p1?.data || 0) + (p2?.data || 0) + carry;
            carry = Math.floor(sum / 10);
            result.append(sum % 10);
            
            p1 = p1?.next;
            p2 = p2?.next;
        }
        
        return result;
    }
    
    // Check if linked list is palindrome
    static isPalindrome(list) {
        if (!list.head) {
            return true;
        }
        
        // Find middle
        let slow = list.head;
        let fast = list.head;
        
        while (fast && fast.next) {
            slow = slow.next;
            fast = fast.next.next;
        }
        
        // Reverse second half
        let prev = null;
        let current = slow;
        
        while (current) {
            const next = current.next;
            current.next = prev;
            prev = current;
            current = next;
        }
        
        // Compare both halves
        let left = list.head;
        let right = prev;
        
        while (right) {
            if (left.data !== right.data) {
                return false;
            }
            left = left.next;
            right = right.next;
        }
        
        return true;
    }
    
    // Find intersection of two linked lists
    static findIntersection(list1, list2) {
        if (!list1.head || !list2.head) {
            return null;
        }
        
        let p1 = list1.head;
        let p2 = list2.head;
        
        // Calculate lengths
        let len1 = 0, len2 = 0;
        let temp = p1;
        while (temp) {
            len1++;
            temp = temp.next;
        }
        
        temp = p2;
        while (temp) {
            len2++;
            temp = temp.next;
        }
        
        // Align pointers
        const diff = Math.abs(len1 - len2);
        
        if (len1 > len2) {
            for (let i = 0; i < diff; i++) {
                p1 = p1.next;
            }
        } else {
            for (let i = 0; i < diff; i++) {
                p2 = p2.next;
            }
        }
        
        // Find intersection
        while (p1 && p2) {
            if (p1 === p2) {
                return p1.data;
            }
            p1 = p1.next;
            p2 = p2.next;
        }
        
        return null;
    }
}

// Usage Examples
const list = new LinkedList();
list.append(1).append(2).append(3).append(4).append(5);

console.log(list.toString()); // LinkedList(5) [1 -> 2 -> 3 -> 4 -> 5]
console.log(list.findMiddle()); // 3
console.log(list.getNthFromEnd(2)); // 4

list.reverse();
console.log(list.toString()); // LinkedList(5) [5 -> 4 -> 3 -> 2 -> 1]

// Doubly linked list
const doublyList = new DoublyLinkedList();
doublyList.append(1).append(2).append(3);

console.log(doublyList.toString()); // DoublyLinkedList(3) [1 <-> 2 <-> 3]
console.log([...doublyList.reverseIterator()]); // [3, 2, 1]

// Check palindrome
const palindromeList = new LinkedList();
palindromeList.append(1).append(2).append(3).append(2).append(1);
console.log(LinkedListUtils.isPalindrome(palindromeList)); // true
```

### 🎯 Trees & Binary Trees

> **Interview Key Point:** Trees are hierarchical data structures that are fundamental for many algorithms and system designs. Understanding tree traversals, binary search trees, and balanced trees is essential for solving complex problems efficiently.

#### **Comprehensive Tree Implementation**

```javascript
// Binary Tree Node
class TreeNode {
    constructor(data, left = null, right = null) {
        this.data = data;
        this.left = left;
        this.right = right;
    }
    
    toString() {
        return `TreeNode(${this.data})`;
    }
}

// Binary Tree
class BinaryTree {
    constructor(root = null) {
        this.root = root;
    }
    
    // Insert node (level order for complete tree)
    insert(data) {
        const newNode = new TreeNode(data);
        
        if (!this.root) {
            this.root = newNode;
            return this;
        }
        
        const queue = [this.root];
        
        while (queue.length > 0) {
            const current = queue.shift();
            
            if (!current.left) {
                current.left = newNode;
                return this;
            } else if (!current.right) {
                current.right = newNode;
                return this;
            } else {
                queue.push(current.left);
                queue.push(current.right);
            }
        }
        
        return this;
    }
    
    // Search for value
    search(data) {
        return this._searchRecursive(this.root, data);
    }
    
    _searchRecursive(node, data) {
        if (!node) return false;
        if (node.data === data) return true;
        
        return this._searchRecursive(node.left, data) || 
               this._searchRecursive(node.right, data);
    }
    
    // Tree traversals
    
    // Inorder traversal (left, root, right)
    inorderTraversal() {
        const result = [];
        this._inorderRecursive(this.root, result);
        return result;
    }
    
    _inorderRecursive(node, result) {
        if (node) {
            this._inorderRecursive(node.left, result);
            result.push(node.data);
            this._inorderRecursive(node.right, result);
        }
    }
    
    // Preorder traversal (root, left, right)
    preorderTraversal() {
        const result = [];
        this._preorderRecursive(this.root, result);
        return result;
    }
    
    _preorderRecursive(node, result) {
        if (node) {
            result.push(node.data);
            this._preorderRecursive(node.left, result);
            this._preorderRecursive(node.right, result);
        }
    }
    
    // Postorder traversal (left, right, root)
    postorderTraversal() {
        const result = [];
        this._postorderRecursive(this.root, result);
        return result;
    }
    
    _postorderRecursive(node, result) {
        if (node) {
            this._postorderRecursive(node.left, result);
            this._postorderRecursive(node.right, result);
            result.push(node.data);
        }
    }
    
    // Level order traversal (breadth-first)
    levelOrderTraversal() {
        if (!this.root) return [];
        
        const result = [];
        const queue = [this.root];
        
        while (queue.length > 0) {
            const current = queue.shift();
            result.push(current.data);
            
            if (current.left) queue.push(current.left);
            if (current.right) queue.push(current.right);
        }
        
        return result;
    }
    
    // Get tree height
    getHeight() {
        return this._getHeightRecursive(this.root);
    }
    
    _getHeightRecursive(node) {
        if (!node) return -1;
        
        const leftHeight = this._getHeightRecursive(node.left);
        const rightHeight = this._getHeightRecursive(node.right);
        
        return Math.max(leftHeight, rightHeight) + 1;
    }
    
    // Get tree depth (same as height)
    getDepth() {
        return this.getHeight();
    }
    
    // Count total nodes
    countNodes() {
        return this._countNodesRecursive(this.root);
    }
    
    _countNodesRecursive(node) {
        if (!node) return 0;
        return 1 + this._countNodesRecursive(node.left) + this._countNodesRecursive(node.right);
    }
    
    // Count leaf nodes
    countLeaves() {
        return this._countLeavesRecursive(this.root);
    }
    
    _countLeavesRecursive(node) {
        if (!node) return 0;
        if (!node.left && !node.right) return 1;
        return this._countLeavesRecursive(node.left) + this._countLeavesRecursive(node.right);
    }
    
    // Check if tree is balanced
    isBalanced() {
        return this._isBalancedRecursive(this.root) !== -1;
    }
    
    _isBalancedRecursive(node) {
        if (!node) return 0;
        
        const leftHeight = this._isBalancedRecursive(node.left);
        if (leftHeight === -1) return -1;
        
        const rightHeight = this._isBalancedRecursive(node.right);
        if (rightHeight === -1) return -1;
        
        if (Math.abs(leftHeight - rightHeight) > 1) return -1;
        
        return Math.max(leftHeight, rightHeight) + 1;
    }
    
    // Check if tree is complete
    isComplete() {
        if (!this.root) return true;
        
        const queue = [this.root];
        let foundNull = false;
        
        while (queue.length > 0) {
            const current = queue.shift();
            
            if (current.left) {
                if (foundNull) return false;
                queue.push(current.left);
            } else {
                foundNull = true;
            }
            
            if (current.right) {
                if (foundNull) return false;
                queue.push(current.right);
            } else {
                foundNull = true;
            }
        }
        
        return true;
    }
    
    // Find maximum value
    findMax() {
        if (!this.root) return null;
        return this._findMaxRecursive(this.root);
    }
    
    _findMaxRecursive(node) {
        if (!node) return -Infinity;
        
        const leftMax = this._findMaxRecursive(node.left);
        const rightMax = this._findMaxRecursive(node.right);
        
        return Math.max(node.data, leftMax, rightMax);
    }
    
    // Find minimum value
    findMin() {
        if (!this.root) return null;
        return this._findMinRecursive(this.root);
    }
    
    _findMinRecursive(node) {
        if (!node) return Infinity;
        
        const leftMin = this._findMinRecursive(node.left);
        const rightMin = this._findMinRecursive(node.right);
        
        return Math.min(node.data, leftMin, rightMin);
    }
    
    // Mirror/Invert the tree
    mirror() {
        this._mirrorRecursive(this.root);
        return this;
    }
    
    _mirrorRecursive(node) {
        if (!node) return;
        
        [node.left, node.right] = [node.right, node.left];
        
        this._mirrorRecursive(node.left);
        this._mirrorRecursive(node.right);
    }
    
    // Check if two trees are identical
    isIdentical(otherTree) {
        return this._areIdentical(this.root, otherTree.root);
    }
    
    _areIdentical(node1, node2) {
        if (!node1 && !node2) return true;
        if (!node1 || !node2) return false;
        
        return node1.data === node2.data &&
               this._areIdentical(node1.left, node2.left) &&
               this._areIdentical(node1.right, node2.right);
    }
    
    // Get all paths from root to leaves
    getAllPaths() {
        const paths = [];
        if (this.root) {
            this._getAllPathsRecursive(this.root, [], paths);
        }
        return paths;
    }
    
    _getAllPathsRecursive(node, currentPath, allPaths) {
        currentPath.push(node.data);
        
        if (!node.left && !node.right) {
            allPaths.push([...currentPath]);
        } else {
            if (node.left) {
                this._getAllPathsRecursive(node.left, currentPath, allPaths);
            }
            if (node.right) {
                this._getAllPathsRecursive(node.right, currentPath, allPaths);
            }
        }
        
        currentPath.pop();
    }
    
    // Print tree structure
    printTree() {
        this._printTreeRecursive(this.root, '', true);
    }
    
    _printTreeRecursive(node, prefix, isLast) {
        if (node) {
            console.log(prefix + (isLast ? '└── ' : '├── ') + node.data);
            
            const children = [];
            if (node.left) children.push(node.left);
            if (node.right) children.push(node.right);
            
            children.forEach((child, index) => {
                const isLastChild = index === children.length - 1;
                this._printTreeRecursive(
                    child,
                    prefix + (isLast ? '    ' : '│   '),
                    isLastChild
                );
            });
        }
    }
}

// Binary Search Tree
class BinarySearchTree extends BinaryTree {
    constructor() {
        super();
    }
    
    // Insert value maintaining BST property
    insert(data) {
        this.root = this._insertRecursive(this.root, data);
        return this;
    }
    
    _insertRecursive(node, data) {
        if (!node) {
            return new TreeNode(data);
        }
        
        if (data < node.data) {
            node.left = this._insertRecursive(node.left, data);
        } else if (data > node.data) {
            node.right = this._insertRecursive(node.right, data);
        }
        
        return node;
    }
    
    // Search in BST (optimized)
    search(data) {
        return this._searchBST(this.root, data);
    }
    
    _searchBST(node, data) {
        if (!node || node.data === data) {
            return node !== null;
        }
        
        if (data < node.data) {
            return this._searchBST(node.left, data);
        } else {
            return this._searchBST(node.right, data);
        }
    }
    
    // Delete node from BST
    delete(data) {
        this.root = this._deleteRecursive(this.root, data);
        return this;
    }
    
    _deleteRecursive(node, data) {
        if (!node) return null;
        
        if (data < node.data) {
            node.left = this._deleteRecursive(node.left, data);
        } else if (data > node.data) {
            node.right = this._deleteRecursive(node.right, data);
        } else {
            // Node to be deleted found
            
            // Case 1: No children (leaf node)
            if (!node.left && !node.right) {
                return null;
            }
            
            // Case 2: One child
            if (!node.left) return node.right;
            if (!node.right) return node.left;
            
            // Case 3: Two children
            // Find inorder successor (smallest in right subtree)
            const successor = this._findMin(node.right);
            node.data = successor.data;
            node.right = this._deleteRecursive(node.right, successor.data);
        }
        
        return node;
    }
    
    _findMin(node) {
        while (node.left) {
            node = node.left;
        }
        return node;
    }
    
    _findMax(node) {
        while (node.right) {
            node = node.right;
        }
        return node;
    }
    
    // Find minimum value in BST
    findMin() {
        if (!this.root) return null;
        return this._findMin(this.root).data;
    }
    
    // Find maximum value in BST
    findMax() {
        if (!this.root) return null;
        return this._findMax(this.root).data;
    }
    
    // Check if tree is valid BST
    isValidBST() {
        return this._isValidBSTRecursive(this.root, -Infinity, Infinity);
    }
    
    _isValidBSTRecursive(node, min, max) {
        if (!node) return true;
        
        if (node.data <= min || node.data >= max) {
            return false;
        }
        
        return this._isValidBSTRecursive(node.left, min, node.data) &&
               this._isValidBSTRecursive(node.right, node.data, max);
    }
    
    // Find kth smallest element
    kthSmallest(k) {
        const result = { count: 0, value: null };
        this._kthSmallestHelper(this.root, k, result);
        return result.value;
    }
    
    _kthSmallestHelper(node, k, result) {
        if (!node || result.value !== null) return;
        
        this._kthSmallestHelper(node.left, k, result);
        
        result.count++;
        if (result.count === k) {
            result.value = node.data;
            return;
        }
        
        this._kthSmallestHelper(node.right, k, result);
    }
    
    // Find lowest common ancestor
    findLCA(data1, data2) {
        return this._findLCARecursive(this.root, data1, data2);
    }
    
    _findLCARecursive(node, data1, data2) {
        if (!node) return null;
        
        if (data1 < node.data && data2 < node.data) {
            return this._findLCARecursive(node.left, data1, data2);
        }
        
        if (data1 > node.data && data2 > node.data) {
            return this._findLCARecursive(node.right, data1, data2);
        }
        
        return node.data;
    }
    
    // Convert BST to sorted array
    toSortedArray() {
        return this.inorderTraversal();
    }
    
    // Range sum query
    rangeSumBST(low, high) {
        return this._rangeSumRecursive(this.root, low, high);
    }
    
    _rangeSumRecursive(node, low, high) {
        if (!node) return 0;
        
        let sum = 0;
        
        if (node.data >= low && node.data <= high) {
            sum += node.data;
        }
        
        if (node.data > low) {
            sum += this._rangeSumRecursive(node.left, low, high);
        }
        
        if (node.data < high) {
            sum += this._rangeSumRecursive(node.right, low, high);
        }
        
        return sum;
    }
}

// AVL Tree (Self-balancing BST)
class AVLTree extends BinarySearchTree {
    constructor() {
        super();
    }
    
    // Get height of node
    getNodeHeight(node) {
        if (!node) return -1;
        return node.height || 0;
    }
    
    // Update height of node
    updateHeight(node) {
        if (node) {
            node.height = Math.max(
                this.getNodeHeight(node.left),
                this.getNodeHeight(node.right)
            ) + 1;
        }
    }
    
    // Get balance factor
    getBalance(node) {
        if (!node) return 0;
        return this.getNodeHeight(node.left) - this.getNodeHeight(node.right);
    }
    
    // Right rotate
    rotateRight(y) {
        const x = y.left;
        const T2 = x.right;
        
        x.right = y;
        y.left = T2;
        
        this.updateHeight(y);
        this.updateHeight(x);
        
        return x;
    }
    
    // Left rotate
    rotateLeft(x) {
        const y = x.right;
        const T2 = y.left;
        
        y.left = x;
        x.right = T2;
        
        this.updateHeight(x);
        this.updateHeight(y);
        
        return y;
    }
    
    // Insert with balancing
    insert(data) {
        this.root = this._insertAVL(this.root, data);
        return this;
    }
    
    _insertAVL(node, data) {
        // Step 1: Perform normal BST insertion
        if (!node) {
            const newNode = new TreeNode(data);
            newNode.height = 0;
            return newNode;
        }
        
        if (data < node.data) {
            node.left = this._insertAVL(node.left, data);
        } else if (data > node.data) {
            node.right = this._insertAVL(node.right, data);
        } else {
            return node; // Duplicate values not allowed
        }
        
        // Step 2: Update height
        this.updateHeight(node);
        
        // Step 3: Get balance factor
        const balance = this.getBalance(node);
        
        // Step 4: Perform rotations if needed
        
        // Left-Left case
        if (balance > 1 && data < node.left.data) {
            return this.rotateRight(node);
        }
        
        // Right-Right case
        if (balance < -1 && data > node.right.data) {
            return this.rotateLeft(node);
        }
        
        // Left-Right case
        if (balance > 1 && data > node.left.data) {
            node.left = this.rotateLeft(node.left);
            return this.rotateRight(node);
        }
        
        // Right-Left case
        if (balance < -1 && data < node.right.data) {
            node.right = this.rotateRight(node.right);
            return this.rotateLeft(node);
        }
        
        return node;
    }
}

// Tree Problem-Solving Utilities
class TreeUtils {
    // Build tree from preorder and inorder
    static buildTreeFromPreorderInorder(preorder, inorder) {
        if (preorder.length === 0 || inorder.length === 0) {
            return null;
        }
        
        const rootVal = preorder[0];
        const root = new TreeNode(rootVal);
        
        const rootIndex = inorder.indexOf(rootVal);
        
        const leftInorder = inorder.slice(0, rootIndex);
        const rightInorder = inorder.slice(rootIndex + 1);
        
        const leftPreorder = preorder.slice(1, leftInorder.length + 1);
        const rightPreorder = preorder.slice(leftInorder.length + 1);
        
        root.left = TreeUtils.buildTreeFromPreorderInorder(leftPreorder, leftInorder);
        root.right = TreeUtils.buildTreeFromPreorderInorder(rightPreorder, rightInorder);
        
        return root;
    }
    
    // Serialize tree to string
    static serialize(root) {
        if (!root) return 'null';
        
        return `${root.data},${TreeUtils.serialize(root.left)},${TreeUtils.serialize(root.right)}`;
    }
    
    // Deserialize string to tree
    static deserialize(data) {
        const values = data.split(',');
        let index = 0;
        
        function deserializeHelper() {
            if (index >= values.length || values[index] === 'null') {
                index++;
                return null;
            }
            
            const node = new TreeNode(parseInt(values[index]));
            index++;
            
            node.left = deserializeHelper();
            node.right = deserializeHelper();
            
            return node;
        }
        
        return deserializeHelper();
    }
    
    // Find diameter of tree
    static findDiameter(root) {
        let diameter = 0;
        
        function dfs(node) {
            if (!node) return 0;
            
            const leftHeight = dfs(node.left);
            const rightHeight = dfs(node.right);
            
            diameter = Math.max(diameter, leftHeight + rightHeight);
            
            return Math.max(leftHeight, rightHeight) + 1;
        }
        
        dfs(root);
        return diameter;
    }
    
    // Convert sorted array to BST
    static sortedArrayToBST(nums) {
        if (nums.length === 0) return null;
        
        function buildBST(left, right) {
            if (left > right) return null;
            
            const mid = Math.floor((left + right) / 2);
            const node = new TreeNode(nums[mid]);
            
            node.left = buildBST(left, mid - 1);
            node.right = buildBST(mid + 1, right);
            
            return node;
        }
        
        return buildBST(0, nums.length - 1);
    }
    
    // Find path sum
    static hasPathSum(root, targetSum) {
        if (!root) return false;
        
        if (!root.left && !root.right) {
            return root.data === targetSum;
        }
        
        const remainingSum = targetSum - root.data;
        
        return TreeUtils.hasPathSum(root.left, remainingSum) ||
               TreeUtils.hasPathSum(root.right, remainingSum);
    }
    
    // Zigzag level order traversal
    static zigzagLevelOrder(root) {
        if (!root) return [];
        
        const result = [];
        const queue = [root];
        let leftToRight = true;
        
        while (queue.length > 0) {
            const levelSize = queue.length;
            const currentLevel = [];
            
            for (let i = 0; i < levelSize; i++) {
                const node = queue.shift();
                
                if (leftToRight) {
                    currentLevel.push(node.data);
                } else {
                    currentLevel.unshift(node.data);
                }
                
                if (node.left) queue.push(node.left);
                if (node.right) queue.push(node.right);
            }
            
            result.push(currentLevel);
            leftToRight = !leftToRight;
        }
        
        return result;
    }
}

// Usage Examples
const bst = new BinarySearchTree();
bst.insert(50).insert(30).insert(70).insert(20).insert(40).insert(60).insert(80);

console.log('Inorder:', bst.inorderTraversal()); // [20, 30, 40, 50, 60, 70, 80]
console.log('Is Valid BST:', bst.isValidBST()); // true
console.log('Height:', bst.getHeight()); // 2
console.log('3rd smallest:', bst.kthSmallest(3)); // 40

// AVL Tree
const avl = new AVLTree();
avl.insert(10).insert(20).insert(30).insert(40).insert(50).insert(25);

console.log('AVL Inorder:', avl.inorderTraversal());
console.log('AVL Height:', avl.getHeight()); // Should be balanced

// Tree utilities
const preorder = [3, 9, 20, 15, 7];
const inorder = [9, 3, 15, 20, 7];
const tree = TreeUtils.buildTreeFromPreorderInorder(preorder, inorder);

const serialized = TreeUtils.serialize(tree);
console.log('Serialized:', serialized);

const deserialized = TreeUtils.deserialize(serialized);
console.log('Path sum exists:', TreeUtils.hasPathSum(deserialized, 24));
```

### 🕸️ Graphs

> **Interview Key Point:** Graphs are essential for modeling relationships and networks. Understanding graph representations, traversals (DFS/BFS), and shortest path algorithms is crucial for solving complex problems in social networks, routing, and optimization.

#### **Comprehensive Graph Implementation**

```javascript
// Graph Node for adjacency list representation
class GraphNode {
    constructor(value) {
        this.value = value;
        this.neighbors = [];
    }
    
    addNeighbor(node) {
        if (!this.neighbors.includes(node)) {
            this.neighbors.push(node);
        }
    }
    
    removeNeighbor(node) {
        this.neighbors = this.neighbors.filter(neighbor => neighbor !== node);
    }
    
    toString() {
        return `GraphNode(${this.value})`;
    }
}

// Undirected Graph
class Graph {
    constructor() {
        this.vertices = new Map(); // value -> GraphNode
        this.adjacencyList = new Map(); // value -> Set of connected values
    }
    
    // Add vertex
    addVertex(value) {
        if (!this.vertices.has(value)) {
            const node = new GraphNode(value);
            this.vertices.set(value, node);
            this.adjacencyList.set(value, new Set());
        }
        return this;
    }
    
    // Remove vertex
    removeVertex(value) {
        if (this.vertices.has(value)) {
            // Remove all edges to this vertex
            for (const neighbor of this.adjacencyList.get(value)) {
                this.adjacencyList.get(neighbor).delete(value);
            }
            
            // Remove the vertex
            this.vertices.delete(value);
            this.adjacencyList.delete(value);
        }
        return this;
    }
    
    // Add edge (undirected)
    addEdge(value1, value2) {
        this.addVertex(value1);
        this.addVertex(value2);
        
        this.adjacencyList.get(value1).add(value2);
        this.adjacencyList.get(value2).add(value1);
        
        return this;
    }
    
    // Remove edge
    removeEdge(value1, value2) {
        if (this.adjacencyList.has(value1)) {
            this.adjacencyList.get(value1).delete(value2);
        }
        if (this.adjacencyList.has(value2)) {
            this.adjacencyList.get(value2).delete(value1);
        }
        return this;
    }
    
    // Check if edge exists
    hasEdge(value1, value2) {
        return this.adjacencyList.has(value1) && 
               this.adjacencyList.get(value1).has(value2);
    }
    
    // Get all vertices
    getVertices() {
        return Array.from(this.vertices.keys());
    }
    
    // Get neighbors of a vertex
    getNeighbors(value) {
        return this.adjacencyList.has(value) ? 
               Array.from(this.adjacencyList.get(value)) : [];
    }
    
    // Get vertex count
    getVertexCount() {
        return this.vertices.size;
    }
    
    // Get edge count
    getEdgeCount() {
        let count = 0;
        for (const neighbors of this.adjacencyList.values()) {
            count += neighbors.size;
        }
        return count / 2; // Undirected graph, so divide by 2
    }
    
    // Depth-First Search (DFS)
    dfs(startValue, visited = new Set()) {
        const result = [];
        
        const dfsHelper = (value) => {
            visited.add(value);
            result.push(value);
            
            for (const neighbor of this.adjacencyList.get(value) || []) {
                if (!visited.has(neighbor)) {
                    dfsHelper(neighbor);
                }
            }
        };
        
        if (this.vertices.has(startValue)) {
            dfsHelper(startValue);
        }
        
        return result;
    }
    
    // Breadth-First Search (BFS)
    bfs(startValue) {
        if (!this.vertices.has(startValue)) return [];
        
        const result = [];
        const visited = new Set();
        const queue = [startValue];
        
        visited.add(startValue);
        
        while (queue.length > 0) {
            const current = queue.shift();
            result.push(current);
            
            for (const neighbor of this.adjacencyList.get(current) || []) {
                if (!visited.has(neighbor)) {
                    visited.add(neighbor);
                    queue.push(neighbor);
                }
            }
        }
        
        return result;
    }
    
    // Find path between two vertices (BFS)
    findPath(start, end) {
        if (!this.vertices.has(start) || !this.vertices.has(end)) {
            return null;
        }
        
        if (start === end) return [start];
        
        const visited = new Set();
        const queue = [[start]];
        visited.add(start);
        
        while (queue.length > 0) {
            const path = queue.shift();
            const current = path[path.length - 1];
            
            for (const neighbor of this.adjacencyList.get(current) || []) {
                if (!visited.has(neighbor)) {
                    const newPath = [...path, neighbor];
                    
                    if (neighbor === end) {
                        return newPath;
                    }
                    
                    visited.add(neighbor);
                    queue.push(newPath);
                }
            }
        }
        
        return null; // No path found
    }
    
    // Check if graph is connected
    isConnected() {
        if (this.vertices.size === 0) return true;
        
        const startVertex = this.vertices.keys().next().value;
        const visited = this.dfs(startVertex);
        
        return visited.length === this.vertices.size;
    }
    
    // Detect cycle (for undirected graph)
    hasCycle() {
        const visited = new Set();
        
        const hasCycleHelper = (current, parent) => {
            visited.add(current);
            
            for (const neighbor of this.adjacencyList.get(current) || []) {
                if (!visited.has(neighbor)) {
                    if (hasCycleHelper(neighbor, current)) {
                        return true;
                    }
                } else if (neighbor !== parent) {
                    return true;
                }
            }
            
            return false;
        };
        
        for (const vertex of this.vertices.keys()) {
            if (!visited.has(vertex)) {
                if (hasCycleHelper(vertex, null)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    // Get all connected components
    getConnectedComponents() {
        const visited = new Set();
        const components = [];
        
        for (const vertex of this.vertices.keys()) {
            if (!visited.has(vertex)) {
                const component = this.dfs(vertex, visited);
                components.push(component);
            }
        }
        
        return components;
    }
    
    // Print graph
    printGraph() {
        for (const [vertex, neighbors] of this.adjacencyList) {
            console.log(`${vertex} -> [${Array.from(neighbors).join(', ')}]`);
        }
    }
}

// Directed Graph
class DirectedGraph extends Graph {
    constructor() {
        super();
    }
    
    // Add directed edge
    addEdge(from, to) {
        this.addVertex(from);
        this.addVertex(to);
        
        this.adjacencyList.get(from).add(to);
        
        return this;
    }
    
    // Remove directed edge
    removeEdge(from, to) {
        if (this.adjacencyList.has(from)) {
            this.adjacencyList.get(from).delete(to);
        }
        return this;
    }
    
    // Get edge count for directed graph
    getEdgeCount() {
        let count = 0;
        for (const neighbors of this.adjacencyList.values()) {
            count += neighbors.size;
        }
        return count;
    }
    
    // Topological sort (DFS-based)
    topologicalSort() {
        const visited = new Set();
        const stack = [];
        
        const topSortHelper = (vertex) => {
            visited.add(vertex);
            
            for (const neighbor of this.adjacencyList.get(vertex) || []) {
                if (!visited.has(neighbor)) {
                    topSortHelper(neighbor);
                }
            }
            
            stack.unshift(vertex);
        };
        
        for (const vertex of this.vertices.keys()) {
            if (!visited.has(vertex)) {
                topSortHelper(vertex);
            }
        }
        
        return stack;
    }
    
    // Detect cycle in directed graph (DFS-based)
    hasCycle() {
        const WHITE = 0; // Unvisited
        const GRAY = 1;  // Visiting
        const BLACK = 2; // Visited
        
        const color = new Map();
        
        // Initialize all vertices as WHITE
        for (const vertex of this.vertices.keys()) {
            color.set(vertex, WHITE);
        }
        
        const hasCycleHelper = (vertex) => {
            color.set(vertex, GRAY);
            
            for (const neighbor of this.adjacencyList.get(vertex) || []) {
                if (color.get(neighbor) === GRAY) {
                    return true; // Back edge found
                }
                
                if (color.get(neighbor) === WHITE && hasCycleHelper(neighbor)) {
                    return true;
                }
            }
            
            color.set(vertex, BLACK);
            return false;
        };
        
        for (const vertex of this.vertices.keys()) {
            if (color.get(vertex) === WHITE) {
                if (hasCycleHelper(vertex)) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    // Get strongly connected components (Kosaraju's algorithm)
    getStronglyConnectedComponents() {
        // Step 1: Get finish times using DFS
        const visited = new Set();
        const finishStack = [];
        
        const dfsFirst = (vertex) => {
            visited.add(vertex);
            
            for (const neighbor of this.adjacencyList.get(vertex) || []) {
                if (!visited.has(neighbor)) {
                    dfsFirst(neighbor);
                }
            }
            
            finishStack.unshift(vertex);
        };
        
        for (const vertex of this.vertices.keys()) {
            if (!visited.has(vertex)) {
                dfsFirst(vertex);
            }
        }
        
        // Step 2: Create transpose graph
        const transpose = new DirectedGraph();
        for (const vertex of this.vertices.keys()) {
            transpose.addVertex(vertex);
        }
        
        for (const [vertex, neighbors] of this.adjacencyList) {
            for (const neighbor of neighbors) {
                transpose.addEdge(neighbor, vertex);
            }
        }
        
        // Step 3: DFS on transpose in reverse finish time order
        const visitedTranspose = new Set();
        const components = [];
        
        for (const vertex of finishStack) {
            if (!visitedTranspose.has(vertex)) {
                const component = transpose.dfs(vertex, visitedTranspose);
                components.push(component);
            }
        }
        
        return components;
    }
}

// Weighted Graph
class WeightedGraph extends DirectedGraph {
    constructor() {
        super();
        this.weights = new Map(); // "from,to" -> weight
    }
    
    // Add weighted edge
    addEdge(from, to, weight = 1) {
        super.addEdge(from, to);
        this.weights.set(`${from},${to}`, weight);
        return this;
    }
    
    // Get edge weight
    getWeight(from, to) {
        return this.weights.get(`${from},${to}`) || Infinity;
    }
    
    // Dijkstra's shortest path algorithm
    dijkstra(start) {
        const distances = new Map();
        const previous = new Map();
        const visited = new Set();
        const pq = new PriorityQueue((a, b) => a.distance - b.distance);
        
        // Initialize distances
        for (const vertex of this.vertices.keys()) {
            distances.set(vertex, Infinity);
            previous.set(vertex, null);
        }
        
        distances.set(start, 0);
        pq.enqueue({ vertex: start, distance: 0 });
        
        while (!pq.isEmpty()) {
            const { vertex: current } = pq.dequeue();
            
            if (visited.has(current)) continue;
            visited.add(current);
            
            for (const neighbor of this.adjacencyList.get(current) || []) {
                const weight = this.getWeight(current, neighbor);
                const newDistance = distances.get(current) + weight;
                
                if (newDistance < distances.get(neighbor)) {
                    distances.set(neighbor, newDistance);
                    previous.set(neighbor, current);
                    pq.enqueue({ vertex: neighbor, distance: newDistance });
                }
            }
        }
        
        return { distances, previous };
    }
    
    // Get shortest path between two vertices
    getShortestPath(start, end) {
        const { distances, previous } = this.dijkstra(start);
        
        if (distances.get(end) === Infinity) {
            return null; // No path exists
        }
        
        const path = [];
        let current = end;
        
        while (current !== null) {
            path.unshift(current);
            current = previous.get(current);
        }
        
        return {
            path,
            distance: distances.get(end)
        };
    }
    
    // Bellman-Ford algorithm (handles negative weights)
    bellmanFord(start) {
        const distances = new Map();
        const previous = new Map();
        
        // Initialize distances
        for (const vertex of this.vertices.keys()) {
            distances.set(vertex, Infinity);
            previous.set(vertex, null);
        }
        
        distances.set(start, 0);
        
        // Relax edges V-1 times
        for (let i = 0; i < this.vertices.size - 1; i++) {
            for (const [edgeKey, weight] of this.weights) {
                const [from, to] = edgeKey.split(',');
                
                if (distances.get(from) !== Infinity) {
                    const newDistance = distances.get(from) + weight;
                    
                    if (newDistance < distances.get(to)) {
                        distances.set(to, newDistance);
                        previous.set(to, from);
                    }
                }
            }
        }
        
        // Check for negative cycles
        for (const [edgeKey, weight] of this.weights) {
            const [from, to] = edgeKey.split(',');
            
            if (distances.get(from) !== Infinity) {
                const newDistance = distances.get(from) + weight;
                
                if (newDistance < distances.get(to)) {
                    throw new Error('Graph contains negative cycle');
                }
            }
        }
        
        return { distances, previous };
    }
    
    // Floyd-Warshall algorithm (all pairs shortest path)
    floydWarshall() {
        const vertices = Array.from(this.vertices.keys());
        const dist = new Map();
        
        // Initialize distance matrix
        for (const i of vertices) {
            for (const j of vertices) {
                if (i === j) {
                    dist.set(`${i},${j}`, 0);
                } else if (this.hasEdge(i, j)) {
                    dist.set(`${i},${j}`, this.getWeight(i, j));
                } else {
                    dist.set(`${i},${j}`, Infinity);
                }
            }
        }
        
        // Floyd-Warshall main algorithm
        for (const k of vertices) {
            for (const i of vertices) {
                for (const j of vertices) {
                    const ikDist = dist.get(`${i},${k}`);
                    const kjDist = dist.get(`${k},${j}`);
                    const ijDist = dist.get(`${i},${j}`);
                    
                    if (ikDist + kjDist < ijDist) {
                        dist.set(`${i},${j}`, ikDist + kjDist);
                    }
                }
            }
        }
        
        return dist;
    }
}

// Priority Queue for Dijkstra's algorithm
class PriorityQueue {
    constructor(compareFn = (a, b) => a - b) {
        this.items = [];
        this.compare = compareFn;
    }
    
    enqueue(item) {
        this.items.push(item);
        this.bubbleUp();
    }
    
    dequeue() {
        if (this.items.length === 0) return null;
        
        const min = this.items[0];
        const end = this.items.pop();
        
        if (this.items.length > 0) {
            this.items[0] = end;
            this.bubbleDown();
        }
        
        return min;
    }
    
    bubbleUp() {
        let index = this.items.length - 1;
        
        while (index > 0) {
            const parentIndex = Math.floor((index - 1) / 2);
            
            if (this.compare(this.items[index], this.items[parentIndex]) >= 0) {
                break;
            }
            
            [this.items[index], this.items[parentIndex]] = 
            [this.items[parentIndex], this.items[index]];
            
            index = parentIndex;
        }
    }
    
    bubbleDown() {
        let index = 0;
        
        while (true) {
            let minIndex = index;
            const leftChild = 2 * index + 1;
            const rightChild = 2 * index + 2;
            
            if (leftChild < this.items.length && 
                this.compare(this.items[leftChild], this.items[minIndex]) < 0) {
                minIndex = leftChild;
            }
            
            if (rightChild < this.items.length && 
                this.compare(this.items[rightChild], this.items[minIndex]) < 0) {
                minIndex = rightChild;
            }
            
            if (minIndex === index) break;
            
            [this.items[index], this.items[minIndex]] = 
            [this.items[minIndex], this.items[index]];
            
            index = minIndex;
        }
    }
    
    isEmpty() {
        return this.items.length === 0;
    }
}

// Graph Problem-Solving Utilities
class GraphUtils {
    // Clone graph (deep copy)
    static cloneGraph(node, visited = new Map()) {
        if (!node) return null;
        
        if (visited.has(node)) {
            return visited.get(node);
        }
        
        const clone = new GraphNode(node.value);
        visited.set(node, clone);
        
        for (const neighbor of node.neighbors) {
            clone.neighbors.push(GraphUtils.cloneGraph(neighbor, visited));
        }
        
        return clone;
    }
    
    // Find minimum spanning tree (Kruskal's algorithm)
    static kruskalMST(graph) {
        const edges = [];
        const visited = new Set();
        
        // Get all edges with weights
        for (const [edgeKey, weight] of graph.weights || new Map()) {
            const [from, to] = edgeKey.split(',');
            edges.push({ from, to, weight });
        }
        
        // Sort edges by weight
        edges.sort((a, b) => a.weight - b.weight);
        
        // Union-Find data structure
        const parent = new Map();
        const rank = new Map();
        
        const find = (x) => {
            if (!parent.has(x)) {
                parent.set(x, x);
                rank.set(x, 0);
            }
            
            if (parent.get(x) !== x) {
                parent.set(x, find(parent.get(x)));
            }
            
            return parent.get(x);
        };
        
        const union = (x, y) => {
            const rootX = find(x);
            const rootY = find(y);
            
            if (rootX !== rootY) {
                if (rank.get(rootX) < rank.get(rootY)) {
                    parent.set(rootX, rootY);
                } else if (rank.get(rootX) > rank.get(rootY)) {
                    parent.set(rootY, rootX);
                } else {
                    parent.set(rootY, rootX);
                    rank.set(rootX, rank.get(rootX) + 1);
                }
                return true;
            }
            
            return false;
        };
        
        const mst = [];
        let totalWeight = 0;
        
        for (const edge of edges) {
            if (union(edge.from, edge.to)) {
                mst.push(edge);
                totalWeight += edge.weight;
            }
        }
        
        return { mst, totalWeight };
    }
    
    // Check if graph is bipartite
    static isBipartite(graph) {
        const color = new Map();
        
        const bfsCheck = (start) => {
            const queue = [start];
            color.set(start, 0);
            
            while (queue.length > 0) {
                const current = queue.shift();
                const currentColor = color.get(current);
                
                for (const neighbor of graph.getNeighbors(current)) {
                    if (!color.has(neighbor)) {
                        color.set(neighbor, 1 - currentColor);
                        queue.push(neighbor);
                    } else if (color.get(neighbor) === currentColor) {
                        return false;
                    }
                }
            }
            
            return true;
        };
        
        for (const vertex of graph.getVertices()) {
            if (!color.has(vertex)) {
                if (!bfsCheck(vertex)) {
                    return false;
                }
            }
        }
        
        return true;
    }
    
    // Find bridges in graph (Tarjan's algorithm)
    static findBridges(graph) {
        const visited = new Set();
        const disc = new Map();
        const low = new Map();
        const parent = new Map();
        const bridges = [];
        let time = 0;
        
        const bridgeUtil = (u) => {
            visited.add(u);
            disc.set(u, time);
            low.set(u, time);
            time++;
            
            for (const v of graph.getNeighbors(u)) {
                if (!visited.has(v)) {
                    parent.set(v, u);
                    bridgeUtil(v);
                    
                    low.set(u, Math.min(low.get(u), low.get(v)));
                    
                    if (low.get(v) > disc.get(u)) {
                        bridges.push([u, v]);
                    }
                } else if (v !== parent.get(u)) {
                    low.set(u, Math.min(low.get(u), disc.get(v)));
                }
            }
        };
        
        for (const vertex of graph.getVertices()) {
            if (!visited.has(vertex)) {
                bridgeUtil(vertex);
            }
        }
        
        return bridges;
    }
}

// Usage Examples
const graph = new Graph();
graph.addEdge('A', 'B')
     .addEdge('B', 'C')
     .addEdge('C', 'D')
     .addEdge('D', 'A')
     .addEdge('B', 'D');

console.log('DFS from A:', graph.dfs('A')); // ['A', 'B', 'C', 'D']
console.log('BFS from A:', graph.bfs('A')); // ['A', 'B', 'D', 'C']
console.log('Path A to C:', graph.findPath('A', 'C')); // ['A', 'B', 'C']
console.log('Has cycle:', graph.hasCycle()); // true
console.log('Is connected:', graph.isConnected()); // true

// Directed graph
const digraph = new DirectedGraph();
digraph.addEdge('A', 'B')
       .addEdge('B', 'C')
       .addEdge('C', 'D')
       .addEdge('D', 'B');

console.log('Topological sort:', digraph.topologicalSort());
console.log('Has cycle:', digraph.hasCycle()); // true

// Weighted graph
const weightedGraph = new WeightedGraph();
weightedGraph.addEdge('A', 'B', 4)
            .addEdge('A', 'C', 2)
            .addEdge('B', 'C', 1)
            .addEdge('B', 'D', 5)
            .addEdge('C', 'D', 8)
            .addEdge('C', 'E', 10)
            .addEdge('D', 'E', 2);

const shortestPath = weightedGraph.getShortestPath('A', 'E');
console.log('Shortest path A to E:', shortestPath);

console.log('Is bipartite:', GraphUtils.isBipartite(graph));
```

### 🔐 Hash Tables & Advanced Hashing

> **Interview Key Point:** Hash tables provide O(1) average-case operations and are fundamental for solving optimization problems. Understanding collision resolution, load factors, and hash functions is crucial for system design and algorithm optimization.

#### **Advanced Hash Table Implementation**

```javascript
// Custom Hash Table with collision resolution
class HashTable {
    constructor(initialSize = 16) {
        this.size = initialSize;
        this.buckets = new Array(this.size);
        this.count = 0;
        this.loadFactorThreshold = 0.75;
        
        // Initialize buckets as arrays for chaining
        for (let i = 0; i < this.size; i++) {
            this.buckets[i] = [];
        }
    }
    
    // Simple hash function (djb2 algorithm)
    hash(key) {
        let hash = 5381;
        for (let i = 0; i < key.length; i++) {
            hash = ((hash << 5) + hash) + key.charCodeAt(i);
        }
        return Math.abs(hash) % this.size;
    }
    
    // Set key-value pair
    set(key, value) {
        const index = this.hash(key.toString());
        const bucket = this.buckets[index];
        
        // Check if key already exists
        for (let i = 0; i < bucket.length; i++) {
            if (bucket[i].key === key) {
                bucket[i].value = value;
                return this;
            }
        }
        
        // Add new key-value pair
        bucket.push({ key, value });
        this.count++;
        
        // Check if resize is needed
        if (this.getLoadFactor() > this.loadFactorThreshold) {
            this.resize();
        }
        
        return this;
    }
    
    // Get value by key
    get(key) {
        const index = this.hash(key.toString());
        const bucket = this.buckets[index];
        
        for (const item of bucket) {
            if (item.key === key) {
                return item.value;
            }
        }
        
        return undefined;
    }
    
    // Check if key exists
    has(key) {
        return this.get(key) !== undefined;
    }
    
    // Delete key-value pair
    delete(key) {
        const index = this.hash(key.toString());
        const bucket = this.buckets[index];
        
        for (let i = 0; i < bucket.length; i++) {
            if (bucket[i].key === key) {
                bucket.splice(i, 1);
                this.count--;
                return true;
            }
        }
        
        return false;
    }
    
    // Get all keys
    keys() {
        const keys = [];
        for (const bucket of this.buckets) {
            for (const item of bucket) {
                keys.push(item.key);
            }
        }
        return keys;
    }
    
    // Get all values
    values() {
        const values = [];
        for (const bucket of this.buckets) {
            for (const item of bucket) {
                values.push(item.value);
            }
        }
        return values;
    }
    
    // Get all entries
    entries() {
        const entries = [];
        for (const bucket of this.buckets) {
            for (const item of bucket) {
                entries.push([item.key, item.value]);
            }
        }
        return entries;
    }
    
    // Get current load factor
    getLoadFactor() {
        return this.count / this.size;
    }
    
    // Resize hash table when load factor exceeds threshold
    resize() {
        const oldBuckets = this.buckets;
        this.size *= 2;
        this.buckets = new Array(this.size);
        this.count = 0;
        
        // Initialize new buckets
        for (let i = 0; i < this.size; i++) {
            this.buckets[i] = [];
        }
        
        // Rehash all existing items
        for (const bucket of oldBuckets) {
            for (const item of bucket) {
                this.set(item.key, item.value);
            }
        }
    }
    
    // Clear all items
    clear() {
        this.buckets = new Array(this.size);
        this.count = 0;
        
        for (let i = 0; i < this.size; i++) {
            this.buckets[i] = [];
        }
        
        return this;
    }
    
    // Get statistics
    getStats() {
        const stats = {
            size: this.size,
            count: this.count,
            loadFactor: this.getLoadFactor(),
            collisions: 0,
            maxChainLength: 0,
            emptyBuckets: 0
        };
        
        for (const bucket of this.buckets) {
            if (bucket.length === 0) {
                stats.emptyBuckets++;
            } else if (bucket.length > 1) {
                stats.collisions += bucket.length - 1;
            }
            
            stats.maxChainLength = Math.max(stats.maxChainLength, bucket.length);
        }
        
        return stats;
    }
    
    // Iterator support
    *[Symbol.iterator]() {
        for (const bucket of this.buckets) {
            for (const item of bucket) {
                yield [item.key, item.value];
            }
        }
    }
}

// Hash Table with Open Addressing (Linear Probing)
class OpenAddressingHashTable {
    constructor(initialSize = 16) {
        this.size = initialSize;
        this.keys = new Array(this.size);
        this.values = new Array(this.size);
        this.deleted = new Array(this.size).fill(false);
        this.count = 0;
        this.loadFactorThreshold = 0.5; // Lower for open addressing
    }
    
    hash(key) {
        let hash = 5381;
        for (let i = 0; i < key.length; i++) {
            hash = ((hash << 5) + hash) + key.charCodeAt(i);
        }
        return Math.abs(hash) % this.size;
    }
    
    // Find slot for key (linear probing)
    findSlot(key) {
        let index = this.hash(key.toString());
        
        while (this.keys[index] !== undefined && 
               this.keys[index] !== key && 
               !this.deleted[index]) {
            index = (index + 1) % this.size;
        }
        
        return index;
    }
    
    set(key, value) {
        if (this.getLoadFactor() >= this.loadFactorThreshold) {
            this.resize();
        }
        
        const index = this.findSlot(key);
        
        if (this.keys[index] === undefined || this.deleted[index]) {
            this.count++;
        }
        
        this.keys[index] = key;
        this.values[index] = value;
        this.deleted[index] = false;
        
        return this;
    }
    
    get(key) {
        let index = this.hash(key.toString());
        
        while (this.keys[index] !== undefined) {
            if (this.keys[index] === key && !this.deleted[index]) {
                return this.values[index];
            }
            index = (index + 1) % this.size;
        }
        
        return undefined;
    }
    
    delete(key) {
        let index = this.hash(key.toString());
        
        while (this.keys[index] !== undefined) {
            if (this.keys[index] === key && !this.deleted[index]) {
                this.deleted[index] = true;
                this.count--;
                return true;
            }
            index = (index + 1) % this.size;
        }
        
        return false;
    }
    
    getLoadFactor() {
        return this.count / this.size;
    }
    
    resize() {
        const oldKeys = this.keys;
        const oldValues = this.values;
        const oldDeleted = this.deleted;
        
        this.size *= 2;
        this.keys = new Array(this.size);
        this.values = new Array(this.size);
        this.deleted = new Array(this.size).fill(false);
        this.count = 0;
        
        for (let i = 0; i < oldKeys.length; i++) {
            if (oldKeys[i] !== undefined && !oldDeleted[i]) {
                this.set(oldKeys[i], oldValues[i]);
            }
        }
    }
}

// LRU Cache using Hash Table + Doubly Linked List
class LRUCache {
    constructor(capacity) {
        this.capacity = capacity;
        this.cache = new Map();
        
        // Create dummy head and tail nodes
        this.head = { key: 0, value: 0, prev: null, next: null };
        this.tail = { key: 0, value: 0, prev: null, next: null };
        this.head.next = this.tail;
        this.tail.prev = this.head;
    }
    
    // Add node right after head
    addNode(node) {
        node.prev = this.head;
        node.next = this.head.next;
        
        this.head.next.prev = node;
        this.head.next = node;
    }
    
    // Remove an existing node
    removeNode(node) {
        const prevNode = node.prev;
        const nextNode = node.next;
        
        prevNode.next = nextNode;
        nextNode.prev = prevNode;
    }
    
    // Move node to head
    moveToHead(node) {
        this.removeNode(node);
        this.addNode(node);
    }
    
    // Remove tail node
    popTail() {
        const lastNode = this.tail.prev;
        this.removeNode(lastNode);
        return lastNode;
    }
    
    get(key) {
        const node = this.cache.get(key);
        
        if (node) {
            // Move accessed node to head
            this.moveToHead(node);
            return node.value;
        }
        
        return -1;
    }
    
    put(key, value) {
        const node = this.cache.get(key);
        
        if (node) {
            // Update existing node
            node.value = value;
            this.moveToHead(node);
        } else {
            const newNode = { key, value, prev: null, next: null };
            
            if (this.cache.size >= this.capacity) {
                // Remove tail node
                const tail = this.popTail();
                this.cache.delete(tail.key);
            }
            
            // Add new node
            this.addNode(newNode);
            this.cache.set(key, newNode);
        }
    }
}

// Consistent Hashing (for distributed systems)
class ConsistentHashing {
    constructor(replicas = 3) {
        this.replicas = replicas;
        this.ring = new Map(); // hash -> server
        this.servers = new Set();
        this.sortedHashes = [];
    }
    
    hash(key) {
        let hash = 5381;
        for (let i = 0; i < key.length; i++) {
            hash = ((hash << 5) + hash) + key.charCodeAt(i);
        }
        return Math.abs(hash);
    }
    
    addServer(server) {
        this.servers.add(server);
        
        for (let i = 0; i < this.replicas; i++) {
            const hash = this.hash(`${server}:${i}`);
            this.ring.set(hash, server);
            this.sortedHashes.push(hash);
        }
        
        this.sortedHashes.sort((a, b) => a - b);
    }
    
    removeServer(server) {
        this.servers.delete(server);
        
        for (let i = 0; i < this.replicas; i++) {
            const hash = this.hash(`${server}:${i}`);
            this.ring.delete(hash);
            const index = this.sortedHashes.indexOf(hash);
            if (index > -1) {
                this.sortedHashes.splice(index, 1);
            }
        }
    }
    
    getServer(key) {
        if (this.sortedHashes.length === 0) {
            return null;
        }
        
        const hash = this.hash(key);
        
        // Find first server hash >= key hash
        for (const serverHash of this.sortedHashes) {
            if (serverHash >= hash) {
                return this.ring.get(serverHash);
            }
        }
        
        // Wrap around to first server
        return this.ring.get(this.sortedHashes[0]);
    }
}

// Usage Examples for Hash Tables
const hashTable = new HashTable();
hashTable.set('name', 'John')
         .set('age', 30)
         .set('city', 'New York');

console.log('Get name:', hashTable.get('name')); // 'John'
console.log('Has age:', hashTable.has('age')); // true
console.log('Keys:', hashTable.keys()); // ['name', 'age', 'city']
console.log('Stats:', hashTable.getStats());

// LRU Cache example
const lruCache = new LRUCache(2);
lruCache.put(1, 1);
lruCache.put(2, 2);
console.log('Get 1:', lruCache.get(1)); // 1
lruCache.put(3, 3); // Evicts key 2
console.log('Get 2:', lruCache.get(2)); // -1 (not found)

// Consistent Hashing example
const consistentHash = new ConsistentHashing();
consistentHash.addServer('server1');
consistentHash.addServer('server2');
consistentHash.addServer('server3');

console.log('Key "user123" -> Server:', consistentHash.getServer('user123'));
console.log('Key "data456" -> Server:', consistentHash.getServer('data456'));
```

### 🧮 Common Algorithms

> **Interview Key Point:** Mastering fundamental algorithms like sorting, searching, and dynamic programming is essential. These patterns appear in 70%+ of coding interviews and form the foundation for solving complex problems.

#### **Sorting Algorithms**

```javascript
class SortingAlgorithms {
    // Bubble Sort - O(n²) time, O(1) space
    static bubbleSort(arr) {
        const result = [...arr];
        const n = result.length;
        
        for (let i = 0; i < n - 1; i++) {
            let swapped = false;
            
            for (let j = 0; j < n - i - 1; j++) {
                if (result[j] > result[j + 1]) {
                    [result[j], result[j + 1]] = [result[j + 1], result[j]];
                    swapped = true;
                }
            }
            
            if (!swapped) break; // Already sorted
        }
        
        return result;
    }
    
    // Selection Sort - O(n²) time, O(1) space
    static selectionSort(arr) {
        const result = [...arr];
        const n = result.length;
        
        for (let i = 0; i < n - 1; i++) {
            let minIndex = i;
            
            for (let j = i + 1; j < n; j++) {
                if (result[j] < result[minIndex]) {
                    minIndex = j;
                }
            }
            
            if (minIndex !== i) {
                [result[i], result[minIndex]] = [result[minIndex], result[i]];
            }
        }
        
        return result;
    }
    
    // Insertion Sort - O(n²) time, O(1) space, good for small arrays
    static insertionSort(arr) {
        const result = [...arr];
        
        for (let i = 1; i < result.length; i++) {
            const key = result[i];
            let j = i - 1;
            
            while (j >= 0 && result[j] > key) {
                result[j + 1] = result[j];
                j--;
            }
            
            result[j + 1] = key;
        }
        
        return result;
    }
    
    // Merge Sort - O(n log n) time, O(n) space
    static mergeSort(arr) {
        if (arr.length <= 1) return arr;
        
        const mid = Math.floor(arr.length / 2);
        const left = SortingAlgorithms.mergeSort(arr.slice(0, mid));
        const right = SortingAlgorithms.mergeSort(arr.slice(mid));
        
        return SortingAlgorithms.merge(left, right);
    }
    
    static merge(left, right) {
        const result = [];
        let i = 0, j = 0;
        
        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                result.push(left[i]);
                i++;
            } else {
                result.push(right[j]);
                j++;
            }
        }
        
        return result.concat(left.slice(i)).concat(right.slice(j));
    }
    
    // Quick Sort - O(n log n) average, O(n²) worst, O(log n) space
    static quickSort(arr, low = 0, high = arr.length - 1) {
        const result = [...arr];
        
        if (low < high) {
            const pivotIndex = SortingAlgorithms.partition(result, low, high);
            
            SortingAlgorithms.quickSort(result, low, pivotIndex - 1);
            SortingAlgorithms.quickSort(result, pivotIndex + 1, high);
        }
        
        return result;
    }
    
    static partition(arr, low, high) {
        const pivot = arr[high];
        let i = low - 1;
        
        for (let j = low; j < high; j++) {
            if (arr[j] < pivot) {
                i++;
                [arr[i], arr[j]] = [arr[j], arr[i]];
            }
        }
        
        [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
        return i + 1;
    }
    
    // Heap Sort - O(n log n) time, O(1) space
    static heapSort(arr) {
        const result = [...arr];
        const n = result.length;
        
        // Build max heap
        for (let i = Math.floor(n / 2) - 1; i >= 0; i--) {
            SortingAlgorithms.heapify(result, n, i);
        }
        
        // Extract elements from heap
        for (let i = n - 1; i > 0; i--) {
            [result[0], result[i]] = [result[i], result[0]];
            SortingAlgorithms.heapify(result, i, 0);
        }
        
        return result;
    }
    
    static heapify(arr, n, i) {
        let largest = i;
        const left = 2 * i + 1;
        const right = 2 * i + 2;
        
        if (left < n && arr[left] > arr[largest]) {
            largest = left;
        }
        
        if (right < n && arr[right] > arr[largest]) {
            largest = right;
        }
        
        if (largest !== i) {
            [arr[i], arr[largest]] = [arr[largest], arr[i]];
            SortingAlgorithms.heapify(arr, n, largest);
        }
    }
    
    // Radix Sort - O(d * (n + k)) time, good for integers
    static radixSort(arr) {
        if (arr.length === 0) return arr;
        
        const max = Math.max(...arr);
        const maxDigits = Math.floor(Math.log10(Math.abs(max))) + 1;
        
        let result = [...arr];
        
        for (let digit = 0; digit < maxDigits; digit++) {
            result = SortingAlgorithms.countingSortByDigit(result, digit);
        }
        
        return result;
    }
    
    static countingSortByDigit(arr, digit) {
        const output = new Array(arr.length);
        const count = new Array(10).fill(0);
        
        // Count occurrences of each digit
        for (const num of arr) {
            const digitValue = Math.floor(num / Math.pow(10, digit)) % 10;
            count[digitValue]++;
        }
        
        // Calculate positions
        for (let i = 1; i < 10; i++) {
            count[i] += count[i - 1];
        }
        
        // Build output array
        for (let i = arr.length - 1; i >= 0; i--) {
            const digitValue = Math.floor(arr[i] / Math.pow(10, digit)) % 10;
            output[count[digitValue] - 1] = arr[i];
            count[digitValue]--;
        }
        
        return output;
    }
}

// Searching Algorithms
class SearchingAlgorithms {
    // Linear Search - O(n) time
    static linearSearch(arr, target) {
        for (let i = 0; i < arr.length; i++) {
            if (arr[i] === target) {
                return i;
            }
        }
        return -1;
    }
    
    // Binary Search - O(log n) time, requires sorted array
    static binarySearch(arr, target) {
        let left = 0;
        let right = arr.length - 1;
        
        while (left <= right) {
            const mid = Math.floor((left + right) / 2);
            
            if (arr[mid] === target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return -1;
    }
    
    // Binary Search (recursive)
    static binarySearchRecursive(arr, target, left = 0, right = arr.length - 1) {
        if (left > right) return -1;
        
        const mid = Math.floor((left + right) / 2);
        
        if (arr[mid] === target) {
            return mid;
        } else if (arr[mid] < target) {
            return SearchingAlgorithms.binarySearchRecursive(arr, target, mid + 1, right);
        } else {
            return SearchingAlgorithms.binarySearchRecursive(arr, target, left, mid - 1);
        }
    }
    
    // Find first occurrence
    static findFirst(arr, target) {
        let left = 0;
        let right = arr.length - 1;
        let result = -1;
        
        while (left <= right) {
            const mid = Math.floor((left + right) / 2);
            
            if (arr[mid] === target) {
                result = mid;
                right = mid - 1; // Continue searching left
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
    
    // Find last occurrence
    static findLast(arr, target) {
        let left = 0;
        let right = arr.length - 1;
        let result = -1;
        
        while (left <= right) {
            const mid = Math.floor((left + right) / 2);
            
            if (arr[mid] === target) {
                result = mid;
                left = mid + 1; // Continue searching right
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        
        return result;
    }
    
    // Find peak element
    static findPeak(arr) {
        let left = 0;
        let right = arr.length - 1;
        
        while (left < right) {
            const mid = Math.floor((left + right) / 2);
            
            if (arr[mid] < arr[mid + 1]) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        
        return left;
    }
    
    // Search in rotated sorted array
    static searchRotated(arr, target) {
        let left = 0;
        let right = arr.length - 1;
        
        while (left <= right) {
            const mid = Math.floor((left + right) / 2);
            
            if (arr[mid] === target) {
                return mid;
            }
            
            // Check which half is sorted
            if (arr[left] <= arr[mid]) {
                // Left half is sorted
                if (target >= arr[left] && target < arr[mid]) {
                    right = mid - 1;
                } else {
                    left = mid + 1;
                }
            } else {
                // Right half is sorted
                if (target > arr[mid] && target <= arr[right]) {
                    left = mid + 1;
                } else {
                    right = mid - 1;
                }
            }
        }
        
        return -1;
    }
}

// Usage Examples for Algorithms
const unsorted = [64, 34, 25, 12, 22, 11, 90];

console.log('Bubble Sort:', SortingAlgorithms.bubbleSort(unsorted));
console.log('Merge Sort:', SortingAlgorithms.mergeSort(unsorted));
console.log('Quick Sort:', SortingAlgorithms.quickSort(unsorted));

const sorted = [1, 3, 5, 7, 9, 11, 13, 15];
console.log('Binary Search for 7:', SearchingAlgorithms.binarySearch(sorted, 7)); // 3
console.log('Linear Search for 11:', SearchingAlgorithms.linearSearch(sorted, 11)); // 5

const rotated = [4, 5, 6, 7, 0, 1, 2];
console.log('Search in rotated array:', SearchingAlgorithms.searchRotated(rotated, 0)); // 4
```

### 🧵 String & Array Problems

> **Interview Key Point:** String and array manipulation problems are the most common in coding interviews. Mastering patterns like sliding window, two pointers, and string processing will solve 60%+ of interview problems.

#### **String Problem Patterns**

```javascript
class StringProblems {
    // Check if string is palindrome
    static isPalindrome(s) {
        const cleaned = s.toLowerCase().replace(/[^a-z0-9]/g, '');
        let left = 0;
        let right = cleaned.length - 1;
        
        while (left < right) {
            if (cleaned[left] !== cleaned[right]) {
                return false;
            }
            left++;
            right--;
        }
        
        return true;
    }
    
    // Longest palindromic substring
    static longestPalindrome(s) {
        if (!s || s.length < 2) return s;
        
        let start = 0;
        let maxLength = 1;
        
        const expandAroundCenter = (left, right) => {
            while (left >= 0 && right < s.length && s[left] === s[right]) {
                const currentLength = right - left + 1;
                if (currentLength > maxLength) {
                    start = left;
                    maxLength = currentLength;
                }
                left--;
                right++;
            }
        };
        
        for (let i = 0; i < s.length; i++) {
            expandAroundCenter(i, i);     // Odd length palindromes
            expandAroundCenter(i, i + 1); // Even length palindromes
        }
        
        return s.substring(start, start + maxLength);
    }
    
    // Valid anagram
    static isAnagram(s, t) {
        if (s.length !== t.length) return false;
        
        const charCount = {};
        
        for (const char of s) {
            charCount[char] = (charCount[char] || 0) + 1;
        }
        
        for (const char of t) {
            if (!charCount[char]) return false;
            charCount[char]--;
        }
        
        return true;
    }
    
    // Group anagrams
    static groupAnagrams(strs) {
        const anagramGroups = new Map();
        
        for (const str of strs) {
            const sortedStr = str.split('').sort().join('');
            
            if (!anagramGroups.has(sortedStr)) {
                anagramGroups.set(sortedStr, []);
            }
            
            anagramGroups.get(sortedStr).push(str);
        }
        
        return Array.from(anagramGroups.values());
    }
    
    // Longest substring without repeating characters
    static lengthOfLongestSubstring(s) {
        const charSet = new Set();
        let left = 0;
        let maxLength = 0;
        
        for (let right = 0; right < s.length; right++) {
            while (charSet.has(s[right])) {
                charSet.delete(s[left]);
                left++;
            }
            
            charSet.add(s[right]);
            maxLength = Math.max(maxLength, right - left + 1);
        }
        
        return maxLength;
    }
    
    // Minimum window substring
    static minWindow(s, t) {
        if (s.length < t.length) return '';
        
        const tCount = {};
        for (const char of t) {
            tCount[char] = (tCount[char] || 0) + 1;
        }
        
        const windowCount = {};
        let left = 0;
        let minStart = 0;
        let minLength = Infinity;
        let formed = 0;
        const required = Object.keys(tCount).length;
        
        for (let right = 0; right < s.length; right++) {
            const char = s[right];
            windowCount[char] = (windowCount[char] || 0) + 1;
            
            if (tCount[char] && windowCount[char] === tCount[char]) {
                formed++;
            }
            
            while (left <= right && formed === required) {
                if (right - left + 1 < minLength) {
                    minLength = right - left + 1;
                    minStart = left;
                }
                
                const leftChar = s[left];
                windowCount[leftChar]--;
                if (tCount[leftChar] && windowCount[leftChar] < tCount[leftChar]) {
                    formed--;
                }
                left++;
            }
        }
        
        return minLength === Infinity ? '' : s.substring(minStart, minStart + minLength);
    }
    
    // String to integer (atoi)
    static myAtoi(s) {
        let i = 0;
        let sign = 1;
        let result = 0;
        const INT_MAX = Math.pow(2, 31) - 1;
        const INT_MIN = -Math.pow(2, 31);
        
        // Skip whitespace
        while (i < s.length && s[i] === ' ') {
            i++;
        }
        
        // Check sign
        if (i < s.length && (s[i] === '+' || s[i] === '-')) {
            sign = s[i] === '-' ? -1 : 1;
            i++;
        }
        
        // Convert digits
        while (i < s.length && s[i] >= '0' && s[i] <= '9') {
            const digit = parseInt(s[i]);
            
            // Check overflow
            if (result > Math.floor(INT_MAX / 10) || 
                (result === Math.floor(INT_MAX / 10) && digit > INT_MAX % 10)) {
                return sign === 1 ? INT_MAX : INT_MIN;
            }
            
            result = result * 10 + digit;
            i++;
        }
        
        return result * sign;
    }
    
    // Regular expression matching
    static isMatch(s, p) {
        const dp = Array(s.length + 1).fill(null).map(() => Array(p.length + 1).fill(false));
        dp[0][0] = true;
        
        // Handle patterns like a* or a*b* at beginning
        for (let j = 1; j <= p.length; j++) {
            if (p[j - 1] === '*') {
                dp[0][j] = dp[0][j - 2];
            }
        }
        
        for (let i = 1; i <= s.length; i++) {
            for (let j = 1; j <= p.length; j++) {
                if (p[j - 1] === '*') {
                    // Check if we can match zero occurrences
                    dp[i][j] = dp[i][j - 2];
                    
                    // Check if we can match one or more occurrences
                    if (s[i - 1] === p[j - 2] || p[j - 2] === '.') {
                        dp[i][j] = dp[i][j] || dp[i - 1][j];
                    }
                } else if (s[i - 1] === p[j - 1] || p[j - 1] === '.') {
                    dp[i][j] = dp[i - 1][j - 1];
                }
            }
        }
        
        return dp[s.length][p.length];
    }
    
    // KMP string matching algorithm
    static strStr(haystack, needle) {
        if (needle.length === 0) return 0;
        if (haystack.length < needle.length) return -1;
        
        // Build failure function (LPS array)
        const lps = new Array(needle.length).fill(0);
        let len = 0;
        let i = 1;
        
        while (i < needle.length) {
            if (needle[i] === needle[len]) {
                len++;
                lps[i] = len;
                i++;
            } else {
                if (len !== 0) {
                    len = lps[len - 1];
                } else {
                    lps[i] = 0;
                    i++;
                }
            }
        }
        
        // KMP search
        i = 0; // Index for haystack
        let j = 0; // Index for needle
        
        while (i < haystack.length) {
            if (haystack[i] === needle[j]) {
                i++;
                j++;
            }
            
            if (j === needle.length) {
                return i - j;
            } else if (i < haystack.length && haystack[i] !== needle[j]) {
                if (j !== 0) {
                    j = lps[j - 1];
                } else {
                    i++;
                }
            }
        }
        
        return -1;
    }
}

// Array Problem Patterns
class ArrayProblems {
    // Two sum
    static twoSum(nums, target) {
        const numMap = new Map();
        
        for (let i = 0; i < nums.length; i++) {
            const complement = target - nums[i];
            
            if (numMap.has(complement)) {
                return [numMap.get(complement), i];
            }
            
            numMap.set(nums[i], i);
        }
        
        return [];
    }
    
    // Three sum
    static threeSum(nums) {
        const result = [];
        nums.sort((a, b) => a - b);
        
        for (let i = 0; i < nums.length - 2; i++) {
            if (i > 0 && nums[i] === nums[i - 1]) continue;
            
            let left = i + 1;
            let right = nums.length - 1;
            
            while (left < right) {
                const sum = nums[i] + nums[left] + nums[right];
                
                if (sum === 0) {
                    result.push([nums[i], nums[left], nums[right]]);
                    
                    while (left < right && nums[left] === nums[left + 1]) left++;
                    while (left < right && nums[right] === nums[right - 1]) right--;
                    
                    left++;
                    right--;
                } else if (sum < 0) {
                    left++;
                } else {
                    right--;
                }
            }
        }
        
        return result;
    }
    
    // Maximum subarray (Kadane's algorithm)
    static maxSubArray(nums) {
        let maxSoFar = nums[0];
        let maxEndingHere = nums[0];
        
        for (let i = 1; i < nums.length; i++) {
            maxEndingHere = Math.max(nums[i], maxEndingHere + nums[i]);
            maxSoFar = Math.max(maxSoFar, maxEndingHere);
        }
        
        return maxSoFar;
    }
    
    // Container with most water
    static maxArea(height) {
        let left = 0;
        let right = height.length - 1;
        let maxWater = 0;
        
        while (left < right) {
            const water = Math.min(height[left], height[right]) * (right - left);
            maxWater = Math.max(maxWater, water);
            
            if (height[left] < height[right]) {
                left++;
            } else {
                right--;
            }
        }
        
        return maxWater;
    }
    
    // Rotate array
    static rotate(nums, k) {
        k = k % nums.length;
        
        const reverse = (start, end) => {
            while (start < end) {
                [nums[start], nums[end]] = [nums[end], nums[start]];
                start++;
                end--;
            }
        };
        
        reverse(0, nums.length - 1);
        reverse(0, k - 1);
        reverse(k, nums.length - 1);
        
        return nums;
    }
    
    // Product of array except self
    static productExceptSelf(nums) {
        const result = new Array(nums.length);
        
        // Calculate left products
        result[0] = 1;
        for (let i = 1; i < nums.length; i++) {
            result[i] = result[i - 1] * nums[i - 1];
        }
        
        // Calculate right products and final result
        let rightProduct = 1;
        for (let i = nums.length - 1; i >= 0; i--) {
            result[i] *= rightProduct;
            rightProduct *= nums[i];
        }
        
        return result;
    }
    
    // Find minimum in rotated sorted array
    static findMin(nums) {
        let left = 0;
        let right = nums.length - 1;
        
        while (left < right) {
            const mid = Math.floor((left + right) / 2);
            
            if (nums[mid] > nums[right]) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        
        return nums[left];
    }
    
    // Sliding window maximum
    static maxSlidingWindow(nums, k) {
        const result = [];
        const deque = []; // Store indices
        
        for (let i = 0; i < nums.length; i++) {
            // Remove elements outside window
            while (deque.length > 0 && deque[0] <= i - k) {
                deque.shift();
            }
            
            // Remove smaller elements from back
            while (deque.length > 0 && nums[deque[deque.length - 1]] <= nums[i]) {
                deque.pop();
            }
            
            deque.push(i);
            
            // Add to result if window is complete
            if (i >= k - 1) {
                result.push(nums[deque[0]]);
            }
        }
        
        return result;
    }
    
    // Merge intervals
    static merge(intervals) {
        if (intervals.length <= 1) return intervals;
        
        intervals.sort((a, b) => a[0] - b[0]);
        const merged = [intervals[0]];
        
        for (let i = 1; i < intervals.length; i++) {
            const current = intervals[i];
            const lastMerged = merged[merged.length - 1];
            
            if (current[0] <= lastMerged[1]) {
                lastMerged[1] = Math.max(lastMerged[1], current[1]);
            } else {
                merged.push(current);
            }
        }
        
        return merged;
    }
}

// Usage Examples for String & Array Problems
console.log('Palindrome check:', StringProblems.isPalindrome("A man, a plan, a canal: Panama"));
console.log('Longest palindrome:', StringProblems.longestPalindrome("babad"));
console.log('Group anagrams:', StringProblems.groupAnagrams(["eat","tea","tan","ate","nat","bat"]));

console.log('Two sum:', ArrayProblems.twoSum([2, 7, 11, 15], 9));
console.log('Max subarray:', ArrayProblems.maxSubArray([-2,1,-3,4,-1,2,1,-5,4]));
console.log('Container water:', ArrayProblems.maxArea([1,8,6,2,5,4,8,3,7]));
```

### 🎯 Dynamic Programming

> **Interview Key Point:** Dynamic Programming is about breaking down complex problems into simpler subproblems. Master the patterns: optimal substructure, overlapping subproblems, and memoization vs tabulation.

#### **Classic DP Problems**

```javascript
class DynamicProgramming {
    // Fibonacci with memoization
    static fibonacci(n, memo = {}) {
        if (n in memo) return memo[n];
        if (n <= 1) return n;
        
        memo[n] = DynamicProgramming.fibonacci(n - 1, memo) + 
                  DynamicProgramming.fibonacci(n - 2, memo);
        return memo[n];
    }
    
    // Fibonacci with tabulation
    static fibonacciTabulation(n) {
        if (n <= 1) return n;
        
        const dp = new Array(n + 1);
        dp[0] = 0;
        dp[1] = 1;
        
        for (let i = 2; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];
        }
        
        return dp[n];
    }
    
    // Climbing stairs
    static climbStairs(n) {
        if (n <= 2) return n;
        
        let prev2 = 1;
        let prev1 = 2;
        
        for (let i = 3; i <= n; i++) {
            const current = prev1 + prev2;
            prev2 = prev1;
            prev1 = current;
        }
        
        return prev1;
    }
    
    // House robber
    static rob(nums) {
        if (nums.length === 0) return 0;
        if (nums.length === 1) return nums[0];
        
        let prev2 = nums[0];
        let prev1 = Math.max(nums[0], nums[1]);
        
        for (let i = 2; i < nums.length; i++) {
            const current = Math.max(prev1, prev2 + nums[i]);
            prev2 = prev1;
            prev1 = current;
        }
        
        return prev1;
    }
    
    // Coin change
    static coinChange(coins, amount) {
        const dp = new Array(amount + 1).fill(amount + 1);
        dp[0] = 0;
        
        for (let i = 1; i <= amount; i++) {
            for (const coin of coins) {
                if (coin <= i) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }
        
        return dp[amount] > amount ? -1 : dp[amount];
    }
    
    // Longest increasing subsequence
    static lengthOfLIS(nums) {
        if (nums.length === 0) return 0;
        
        const dp = new Array(nums.length).fill(1);
        
        for (let i = 1; i < nums.length; i++) {
            for (let j = 0; j < i; j++) {
                if (nums[j] < nums[i]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
        }
        
        return Math.max(...dp);
    }
    
    // Longest common subsequence
    static longestCommonSubsequence(text1, text2) {
        const m = text1.length;
        const n = text2.length;
        const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
        
        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (text1[i - 1] === text2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                } else {
                    dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
                }
            }
        }
        
        return dp[m][n];
    }
    
    // 0/1 Knapsack
    static knapsack(weights, values, capacity) {
        const n = weights.length;
        const dp = Array(n + 1).fill(null).map(() => Array(capacity + 1).fill(0));
        
        for (let i = 1; i <= n; i++) {
            for (let w = 1; w <= capacity; w++) {
                if (weights[i - 1] <= w) {
                    dp[i][w] = Math.max(
                        dp[i - 1][w],
                        dp[i - 1][w - weights[i - 1]] + values[i - 1]
                    );
                } else {
                    dp[i][w] = dp[i - 1][w];
                }
            }
        }
        
        return dp[n][capacity];
    }
    
    // Edit distance (Levenshtein distance)
    static minDistance(word1, word2) {
        const m = word1.length;
        const n = word2.length;
        const dp = Array(m + 1).fill(null).map(() => Array(n + 1).fill(0));
        
        // Initialize base cases
        for (let i = 0; i <= m; i++) dp[i][0] = i;
        for (let j = 0; j <= n; j++) dp[0][j] = j;
        
        for (let i = 1; i <= m; i++) {
            for (let j = 1; j <= n; j++) {
                if (word1[i - 1] === word2[j - 1]) {
                    dp[i][j] = dp[i - 1][j - 1];
                } else {
                    dp[i][j] = Math.min(
                        dp[i - 1][j] + 1,     // Delete
                        dp[i][j - 1] + 1,     // Insert
                        dp[i - 1][j - 1] + 1  // Replace
                    );
                }
            }
        }
        
        return dp[m][n];
    }
    
    // Maximum sum subarray (2D - Kadane's extension)
    static maxSumSubmatrix(matrix) {
        const rows = matrix.length;
        const cols = matrix[0].length;
        let maxSum = -Infinity;
        
        for (let top = 0; top < rows; top++) {
            const temp = new Array(cols).fill(0);
            
            for (let bottom = top; bottom < rows; bottom++) {
                // Add current row to temp
                for (let col = 0; col < cols; col++) {
                    temp[col] += matrix[bottom][col];
                }
                
                // Apply Kadane's algorithm to temp
                const currentMax = ArrayProblems.maxSubArray(temp);
                maxSum = Math.max(maxSum, currentMax);
            }
        }
        
        return maxSum;
    }
    
    // Word break
    static wordBreak(s, wordDict) {
        const wordSet = new Set(wordDict);
        const dp = new Array(s.length + 1).fill(false);
        dp[0] = true;
        
        for (let i = 1; i <= s.length; i++) {
            for (let j = 0; j < i; j++) {
                if (dp[j] && wordSet.has(s.substring(j, i))) {
                    dp[i] = true;
                    break;
                }
            }
        }
        
        return dp[s.length];
    }
}

// Usage Examples for DP
console.log('Fibonacci(10):', DynamicProgramming.fibonacci(10));
console.log('Climb stairs(5):', DynamicProgramming.climbStairs(5));
console.log('Coin change:', DynamicProgramming.coinChange([1, 3, 4], 6));
console.log('LIS:', DynamicProgramming.lengthOfLIS([10,9,2,5,3,7,101,18]));
```

### ⏱️ Time & Space Complexity Analysis

> **Interview Key Point:** Understanding Big O notation is crucial for evaluating algorithm efficiency. Focus on worst-case scenarios and how input size affects performance.

#### **Comprehensive Complexity Guide**

```javascript
class ComplexityAnalysis {
    // O(1) - Constant Time
    static constantTime(arr) {
        // Always takes same time regardless of input size
        return arr[0]; // Accessing array element
    }
    
    // O(log n) - Logarithmic Time
    static logarithmicTime(arr, target) {
        // Binary search - cuts problem in half each time
        let left = 0, right = arr.length - 1;
        
        while (left <= right) {
            const mid = Math.floor((left + right) / 2);
            if (arr[mid] === target) return mid;
            arr[mid] < target ? left = mid + 1 : right = mid - 1;
        }
        return -1;
    }
    
    // O(n) - Linear Time
    static linearTime(arr) {
        // Process each element once
        let sum = 0;
        for (const num of arr) {
            sum += num; // Single pass through array
        }
        return sum;
    }
    
    // O(n log n) - Linearithmic Time
    static linearithmicTime(arr) {
        // Merge sort, heap sort
        return arr.sort((a, b) => a - b);
    }
    
    // O(n²) - Quadratic Time
    static quadraticTime(arr) {
        // Nested loops over same data
        const pairs = [];
        for (let i = 0; i < arr.length; i++) {
            for (let j = i + 1; j < arr.length; j++) {
                pairs.push([arr[i], arr[j]]);
            }
        }
        return pairs;
    }
    
    // O(2^n) - Exponential Time
    static exponentialTime(n) {
        // Naive fibonacci - each call spawns 2 more calls
        if (n <= 1) return n;
        return this.exponentialTime(n - 1) + this.exponentialTime(n - 2);
    }
    
    // Space Complexity Examples
    
    // O(1) Space - Constant Space
    static constantSpace(arr) {
        let sum = 0; // Only using fixed amount of extra space
        for (const num of arr) {
            sum += num;
        }
        return sum;
    }
    
    // O(n) Space - Linear Space
    static linearSpace(arr) {
        const doubled = []; // Creating new array of same size
        for (const num of arr) {
            doubled.push(num * 2);
        }
        return doubled;
    }
    
    // O(log n) Space - Logarithmic Space (Recursion)
    static logarithmicSpace(n) {
        // Binary search recursion - call stack depth is log n
        if (n <= 1) return 1;
        return this.logarithmicSpace(Math.floor(n / 2));
    }
    
    // Analysis of common data structure operations
    static getComplexityChart() {
        return {
            "Data Structure Operations": {
                "Array": {
                    "Access": "O(1)",
                    "Search": "O(n)",
                    "Insertion": "O(n)",
                    "Deletion": "O(n)",
                    "Space": "O(n)"
                },
                "Hash Table": {
                    "Access": "N/A",
                    "Search": "O(1) avg, O(n) worst",
                    "Insertion": "O(1) avg, O(n) worst",
                    "Deletion": "O(1) avg, O(n) worst",
                    "Space": "O(n)"
                },
                "Binary Search Tree": {
                    "Access": "O(log n) avg, O(n) worst",
                    "Search": "O(log n) avg, O(n) worst",
                    "Insertion": "O(log n) avg, O(n) worst",
                    "Deletion": "O(log n) avg, O(n) worst",
                    "Space": "O(n)"
                },
                "AVL Tree": {
                    "Access": "O(log n)",
                    "Search": "O(log n)",
                    "Insertion": "O(log n)",
                    "Deletion": "O(log n)",
                    "Space": "O(n)"
                },
                "Stack": {
                    "Access": "O(n)",
                    "Search": "O(n)",
                    "Insertion": "O(1)",
                    "Deletion": "O(1)",
                    "Space": "O(n)"
                },
                "Queue": {
                    "Access": "O(n)",
                    "Search": "O(n)",
                    "Insertion": "O(1)",
                    "Deletion": "O(1)",
                    "Space": "O(n)"
                }
            },
            "Sorting Algorithms": {
                "Bubble Sort": "O(n²) time, O(1) space",
                "Selection Sort": "O(n²) time, O(1) space",
                "Insertion Sort": "O(n²) time, O(1) space",
                "Merge Sort": "O(n log n) time, O(n) space",
                "Quick Sort": "O(n log n) avg, O(n²) worst, O(log n) space",
                "Heap Sort": "O(n log n) time, O(1) space",
                "Radix Sort": "O(d(n + k)) time, O(n + k) space"
            },
            "Search Algorithms": {
                "Linear Search": "O(n) time, O(1) space",
                "Binary Search": "O(log n) time, O(1) space",
                "DFS": "O(V + E) time, O(V) space",
                "BFS": "O(V + E) time, O(V) space"
            }
        };
    }
    
    // Performance optimization tips
    static optimizationTips() {
        return {
            "Time Optimization": [
                "Use hash tables for O(1) lookups",
                "Apply binary search on sorted data",
                "Use two pointers technique for arrays",
                "Implement sliding window for subarray problems",
                "Cache results with memoization",
                "Use early termination in loops",
                "Choose appropriate data structures"
            ],
            "Space Optimization": [
                "Reuse variables instead of creating new ones",
                "Use iterative instead of recursive approaches",
                "Process data in-place when possible",
                "Use bit manipulation for boolean arrays",
                "Stream large datasets instead of loading all",
                "Use primitive types over objects when possible",
                "Clean up references to avoid memory leaks"
            ],
            "Common Patterns": {
                "Sliding Window": "For subarray/substring problems - O(n)",
                "Two Pointers": "For sorted array problems - O(n)",
                "Fast & Slow Pointers": "For cycle detection - O(n)",
                "Merge Intervals": "For interval problems - O(n log n)",
                "Cyclic Sort": "For missing number problems - O(n)",
                "Tree DFS": "For tree path problems - O(n)",
                "Tree BFS": "For level order problems - O(n)",
                "Dynamic Programming": "For optimization problems - varies",
                "Backtracking": "For permutation/combination - exponential",
                "Binary Search": "For sorted data - O(log n)"
            }
        };
    }
}

// Performance testing utility
class PerformanceTester {
    static measureTime(fn, ...args) {
        const start = performance.now();
        const result = fn(...args);
        const end = performance.now();
        
        return {
            result,
            timeMs: end - start,
            timeFormatted: `${(end - start).toFixed(2)}ms`
        };
    }
    
    static compareAlgorithms(algorithms, input) {
        const results = {};
        
        for (const [name, fn] of Object.entries(algorithms)) {
            const measurement = PerformanceTester.measureTime(fn, input);
            results[name] = measurement;
        }
        
        return results;
    }
    
    static memoryUsage() {
        if (typeof process !== 'undefined' && process.memoryUsage) {
            const usage = process.memoryUsage();
            return {
                rss: `${Math.round(usage.rss / 1024 / 1024)}MB`,
                heapTotal: `${Math.round(usage.heapTotal / 1024 / 1024)}MB`,
                heapUsed: `${Math.round(usage.heapUsed / 1024 / 1024)}MB`,
                external: `${Math.round(usage.external / 1024 / 1024)}MB`
            };
        }
        return "Memory usage not available in browser environment";
    }
}

// Final usage examples
console.log('\n=== COMPLEXITY ANALYSIS ===');
console.log('Complexity Chart:', ComplexityAnalysis.getComplexityChart());
console.log('Optimization Tips:', ComplexityAnalysis.optimizationTips());

// Performance comparison example
const testArray = Array.from({length: 1000}, (_, i) => Math.floor(Math.random() * 1000));

const sortingComparison = PerformanceTester.compareAlgorithms({
    'Bubble Sort': (arr) => SortingAlgorithms.bubbleSort(arr.slice(0, 100)), // Smaller array for bubble sort
    'Merge Sort': (arr) => SortingAlgorithms.mergeSort(arr),
    'Quick Sort': (arr) => SortingAlgorithms.quickSort(arr),
    'Native Sort': (arr) => [...arr].sort((a, b) => a - b)
}, testArray);

console.log('\nSorting Performance Comparison:', sortingComparison);
console.log('Memory Usage:', PerformanceTester.memoryUsage());

// End of guide
console.log('\n🎉 Data Structures & Algorithms Guide Complete!');
console.log('📚 This comprehensive guide covers all essential topics for JavaScript interviews.');
console.log('🚀 Practice these implementations and patterns to excel in coding interviews!');
```

---

## 🎓 Interview Preparation Checklist

### **Must-Know Concepts** ✅
- [ ] **Arrays & Objects**: Enhanced operations, problem-solving methods
- [ ] **Hash Maps & Sets**: Collision resolution, load factor optimization  
- [ ] **Stacks & Queues**: Priority queues, deques, practical applications
- [ ] **Linked Lists**: Singly/doubly linked, cycle detection, merge operations
- [ ] **Trees & BSTs**: Traversals, balancing (AVL), search optimizations
- [ ] **Graphs**: DFS/BFS, shortest paths, topological sort, MST
- [ ] **Hash Tables**: Advanced hashing, LRU cache, consistent hashing
- [ ] **Sorting**: Merge, Quick, Heap sort implementations and analysis
- [ ] **Searching**: Binary search variants, pattern matching (KMP)
- [ ] **String/Array Problems**: Two pointers, sliding window, common patterns
- [ ] **Dynamic Programming**: Memoization, tabulation, classic problems
- [ ] **Time/Space Complexity**: Big O analysis, optimization strategies

### **Practice Strategy** 🎯
1. **Understand the Pattern** - Learn the underlying algorithm pattern
2. **Implement from Scratch** - Don't just memorize, understand the logic
3. **Analyze Complexity** - Always discuss time/space trade-offs
4. **Test Edge Cases** - Empty inputs, single elements, large datasets
5. **Optimize Iteratively** - Start with brute force, then optimize
6. **Explain Your Approach** - Practice verbalizing your thought process

---

*Happy coding! This guide provides enterprise-level implementations and interview-ready solutions for all major data structures and algorithms topics. Use it as your comprehensive reference for technical interviews.* 🚀
