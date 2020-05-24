# Currying

単にアロー関数のチェーンを使ってください:

```typescript
// A curried function
let add = (x: number) => (y: number) => x + y;

// Simple usage
add(123)(456);

// partially applied
let add123 = add(123);

// fully apply the function
add123(456);
```

