# Simple Receipt Generator

## Difficulty
Easy

## Description
Write a C++ program that reads the name of an item, its unit price, and the quantity purchased. Calculate the subtotal, a fixed sales tax (8%), and the total amount. Finally, print a simple receipt displaying all the information with appropriate labels and formatting.

## Constraints
*   The item name will be a single word (no spaces).
*   The unit price will be a positive floating-point number.
*   The quantity will be a positive integer.
*   The sales tax rate is fixed at 8% (0.08).
*   All monetary output values (unit price, subtotal, sales tax, total) must be displayed with exactly two decimal places.

## Test Cases

### Test Case 1
#### Input
```
Apple
1.25
3
```
#### Output
```
Item: Apple
Unit Price: 1.25
Quantity: 3
Subtotal: 3.75
Sales Tax (8.00%): 0.30
Total: 4.05
```

### Test Case 2
#### Input
```
Laptop
999.99
1
```
#### Output
```
Item: Laptop
Unit Price: 999.99
Quantity: 1
Subtotal: 999.99
Sales Tax (8.00%): 80.00
Total: 1079.99
```

### Test Case 3
#### Input
```
Book
15.00
2
```
#### Output
```
Item: Book
Unit Price: 15.00
Quantity: 2
Subtotal: 30.00
Sales Tax (8.00%): 2.40
Total: 32.40
```

### Test Case 4
#### Input
```
Pen
0.75
10
```
#### Output
```
Item: Pen
Unit Price: 0.75
Quantity: 10
Subtotal: 7.50
Sales Tax (8.00%): 0.60
Total: 8.10
```

### Test Case 5
#### Input
```
Milk
3.49
1
```
#### Output
```
Item: Milk
Unit Price: 3.49
Quantity: 1
Subtotal: 3.49
Sales Tax (8.00%): 0.28
Total: 3.77
```