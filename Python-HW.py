def quicksort(arr, key=lambda x: x):  # default key is the identity function
    def partition(low, high):
        pivot = key(arr[high])  # pivot element
        i = low - 1  # index of smaller element
        for j in range(low, high):  # traverse through all elements
            if (
                key(arr[j]) <= pivot
            ):  # if current element is smaller than or equal to pivot
                i += 1
                arr[i], arr[j] = arr[j], arr[i]  # swap elements
        arr[i + 1], arr[high] = arr[high], arr[i + 1]  # swap elements
        return i + 1  # return the partitioning index

    def quick_sort_recursive(low, high):
        if low < high:
            pi = partition(low, high)  # pi is the partitioning index
            quick_sort_recursive(low, pi - 1)  # sort the left side of pivot
            quick_sort_recursive(pi + 1, high)  # sort the right side of pivot

    quick_sort_recursive(0, len(arr) - 1)  # sort the entire array


# Example usage:
arr = [10, 7, 8, 9, 1, 5]
quicksort(arr)
print("Sorted array in ascending order:", arr)

# For descending order
quicksort(arr, key=lambda x: -x)
print("Sorted array in descending order:", arr)


def group_names_by_initial(names):
    grouped_names = {}

    for name in names:  # iterate over the list
        name_lower = name.lower()  # convert to lowercase
        first_letter = name_lower[0]  # get the first letter

        if first_letter not in grouped_names:  # if the key doesn't exist
            grouped_names[first_letter] = set()  # create a new set

        grouped_names[first_letter].add(name)  # add the name to the set

    # Convert sets to lists
    for key in grouped_names:
        grouped_names[key] = list(grouped_names[key])  # convert the set to a list

    return grouped_names


# Example usage
names = ["Alice", "Bob", "alice", "bob", "Charlie", "charlie", "David"]
print(group_names_by_initial(names))


def foldl(func, acc, lst):
    for elem in lst:  # iterate over the list
        acc = func(acc, elem)  # apply the function
    return acc  # return the accumulator


def foldr(func, acc, lst):
    for elem in reversed(lst):  # reverse the list
        acc = func(elem, acc)  # swap the order of the arguments
    return acc  # return the accumulator


# Example usage
lst = [1, 2, 3, 4]
print(foldl(lambda x, y: x + y, 0, lst))  # Output: 10
print(foldr(lambda x, y: x + y, 0, lst))  # Output: 10


# applies a function to each pair of elements from two lists
def zip_with(func, list1, list2):
    result = []
    for elem1, elem2 in zip(list1, list2):  # zip stops at the shortest list
        result.append(func(elem1, elem2))
    return result


# Example usage
list1 = [1, 2, 3]
list2 = [4, 5, 6, 7]
print(zip_with(lambda x, y: x + y, list1, list2))  # Output: [5, 7, 9]


class NoDuplicateStack:
    def __init__(self):
        self.stack = []

    # pushes an item onto stack if it is not a duplicate of the top item
    def push(self, item):
        if not self.stack or self.stack[-1] != item:
            self.stack.append(item)

    # pops the top item from stack
    def pop(self):
        if not self.stack:
            raise IndexError("pop from empty stack")
        return self.stack.pop()

    # returns the top item from stack
    def peek(self):
        if not self.stack:
            raise IndexError("peek from empty stack")
        return self.stack[-1]


class NoDuplicateQueue:
    def __init__(self):
        self.queue = []

    # enqueues an item into queue if it is not a duplicate of the last item
    def enqueue(self, item):
        if not self.queue or self.queue[0] != item:
            self.queue.append(item)

    # dequeues the first item from queue
    def dequeue(self):
        if not self.queue:
            raise IndexError("dequeue from empty queue")
        return self.queue.pop(0)

    # returns the first item from queue
    def peek(self):
        if not self.queue:
            raise IndexError("peek from empty queue")
        return self.queue[0]


# Example usage
stack = NoDuplicateStack()
stack.push(1)
stack.push(1)  # Duplicate, won't be added
stack.push(2)
print(stack.pop())  # Output: 2
print(stack.peek())  # Output: 1

queue = NoDuplicateQueue()
queue.enqueue(1)
queue.enqueue(1)  # Duplicate, won't be added
queue.enqueue(2)
print(queue.dequeue())  # Output: 1
print(queue.peek())  # Output: 2
