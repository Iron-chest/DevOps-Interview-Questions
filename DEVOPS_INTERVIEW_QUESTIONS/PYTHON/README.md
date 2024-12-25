# Smallest Missing Positive Integer

This project contains a solution to the problem of finding the smallest missing positive integer from a given array of integers. The solution is implemented in Python, using an efficient algorithm designed to handle large arrays within given constraints.

## Problem Statement

Write a function:

```python
def solution(A):
```

that, given an array `A` of `N` integers, returns the smallest positive integer (greater than 0) that does not occur in `A`.

### Examples:

1. **Input:** `A = [1, 3, 6, 4, 1, 2]`\
   **Output:** `5`

2. **Input:** `A = [1, 2, 3]`\
   **Output:** `4`

3. **Input:** `A = [-1, -3]`\
   **Output:** `1`

### Constraints:

- `N` is an integer within the range `[1..100,000]`
- Each element of array `A` is an integer within the range `[-1,000,000..1,000,000]`

## Solution Description

The algorithm is designed to work efficiently within the constraints, using the following steps:

1. **Clean up the input array:** Replace non-positive numbers and numbers larger than `N` with a value of `N + 1`. This ensures only relevant values remain in the range `[1..N]`.

2. **Mark presence:** Iterate through the array, marking the presence of integers by negating the value at the corresponding index (using `index = number - 1`).

3. **Identify the missing integer:** Iterate through the array again to find the first index where the value is positive. The missing integer is `index + 1`.

4. **Handle edge cases:** If all numbers from `1` to `N` are present, return `N + 1`.

## Implementation

Here is the Python implementation:

```python
def solution(A):
    N = len(A)

    # Step 1: Clean up the input array
    for i in range(N):
        if A[i] <= 0 or A[i] > N:
            A[i] = N + 1  # Replace non-positive numbers and numbers larger than N

    # Step 2: Mark presence
    for i in range(N):
        num = abs(A[i])  # Get the absolute value
        if 1 <= num <= N:
            # Mark as negative to indicate presence
            if A[num - 1] > 0:
                A[num - 1] = -A[num - 1]

    # Step 3: Identify the first missing positive integer
    for i in range(N):
        if A[i] > 0:  # The index + 1 is missing
            return i + 1

    # Step 4: If all are present, return N + 1
    return N + 1

# Example usage:
print(solution([1, 3, 6, 4, 1, 2]))   # Output: 5
print(solution([1, 2, 3]))            # Output: 4
print(solution([-1, -3]))             # Output: 1
```

## Performance Analysis

- **Time Complexity:** `O(N)`

  - The algorithm iterates through the array a constant number of times.

- **Space Complexity:** `O(1)`

  - The solution uses the input array itself for marking presence, requiring no additional space.

## Repository Structure

The repository contains the following files:

- `solution.py`: Python file containing the implementation.
- `README.md`: Documentation of the project.

## How to Run

1. Clone the repository:

   ```bash
   git clone https://github.com/Iron-chest/smallest-missing-positive.git
   ```

2. Navigate to the project directory:

   ```bash
   cd smallest-missing-positive
   ```

3. Run the solution:

   ```bash
   python solution.py
   ```

## Testing

Test cases are provided in the `tests/` directory. You can run the tests using:

```bash
pytest tests/
```

 

