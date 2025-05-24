# Name:
# OSU Email:
# Course: CS261 - Data Structures
# Assignment:
# Due Date:
# Description:


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MinHeap with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MinHeap content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return "HEAP " + str(heap_data)

    def add(self, node: object) -> None:
        """
        TODO: Write this implementation
        """
        self._heap.append(node)
        curr_index = self._heap.length() - 1

        while curr_index > 0:
            parent_index = (curr_index - 1)//2
            parent_val = self._heap.get_at_index(parent_index)

            if parent_val > self._heap.get_at_index(curr_index):
                self._heap.set_at_index(parent_index, self._heap.get_at_index(curr_index))
                self._heap.set_at_index(curr_index, parent_val)
                curr_index = parent_index
            else:
                return








    def is_empty(self) -> bool:
        """
        TODO: Write this implementation
        """
        return self._heap.length() == 0



    def get_min(self) -> object:
        """
        TODO: Write this implementation
        """
        if self._heap.length() == 0:
            return None
        min = self._heap.get_at_index(0)
        return min

    def remove_min(self) -> object:
        """
        TODO: Write this implementation
        """
        if self._heap.length() == 0:
            raise MinHeapException("MinHeap is empty")

        parent = 0

        root_value = self._heap.get_at_index(0)
        last_value = self._heap.get_at_index(self._heap.length() - 1)
        self._heap.set_at_index(parent, last_value)
        self._heap.remove_at_index(self._heap.length() - 1)

        _percolate_down(self._heap, 0, self._heap.length())

        return root_value




    def build_heap(self, da: DynamicArray) -> None:
        """
        TODO: Write this implementation
        """
        self._heap = DynamicArray(da)
        last_index = self._heap.length() - 1
        first_parent = (last_index - 1) // 2
        for i in range(first_parent, -1, -1):
            _percolate_down(self._heap, i, last_index + 1)

    def size(self) -> int:
        """
        returns the size of the MinHeap
        """
        return self._heap.length()

    def clear(self) -> None:
        """
        clears the heap by setting it to a new dynamic array
        """
        self._heap = DynamicArray()


def heapsort(da: DynamicArray) -> None:
    """
    TODO: Write this implementation
    """
    last_index = da.length() - 1
    first_parent = (last_index - 1) // 2
    for i in range(first_parent, -1, -1):
        _percolate_down(da, i, last_index + 1)


    heap = da
    k = heap.length() - 1


    while k >= 0:
        k_val = heap.get_at_index(k)
        min_val = heap.get_at_index(0)
        heap.set_at_index(k, min_val)
        heap.set_at_index(0, k_val)


        _percolate_down(heap, 0, k)
        k -= 1





# It's highly recommended that you implement the following optional          #
# helper function for percolating elements down the MinHeap. You can call    #
# this from inside the MinHeap class. You may edit the function definition.  #

def _percolate_down(da: DynamicArray, parent: int, k:int) -> None:
    """
    TODO: Write your implementation
    """
    heap = da
    parent = parent

    #calculate index for left and right children for first given parent
    left_index = (2 * parent) + 1
    right_index = (2 * parent) + 2

    #while given parent has at least one child
    while left_index < k:

        #set smaller_val_index to left because if one child it would be left
        smaller_val_index = left_index

        #check if it has right child and compare right left values
        if right_index < k and heap.get_at_index(right_index) < heap.get_at_index(smaller_val_index):
            smaller_val_index = right_index


        #if parent val is greater than child val swap places in da
        if heap.get_at_index(smaller_val_index) < heap.get_at_index(parent):

            smaller_val = heap.get_at_index(smaller_val_index)
            heap.set_at_index(smaller_val_index, heap.get_at_index(parent))
            heap.set_at_index(parent, smaller_val)

            #update/recalc vals for parent, left, and right indices
            parent = smaller_val_index
            left_index = (2 * parent) + 1
            right_index = (2 * parent) + 2
        else:

            #no changes need to be made if parent is less than child val
            return






# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), h.get_min())

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")
