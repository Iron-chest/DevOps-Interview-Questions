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
print(solution([1, 3, 6, 4, 1, 2]))  # Output: 5
print(solution([1, 2, 3]))            # Output: 4
print(solution([-1, -3]))             # Output: 1