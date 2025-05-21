# Name: Grace Meyer
# OSU Email: meyerg3@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 2
# Due Date: 04/28/2025
# Description: implementation of a dynamic array built on top of a static array with methods resize,
# append, insert_at_index, remove_at_index, slice, map, filter and reduce. Two additional functions using
# the dynamic array chunk and find_mode.


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Resizes array capacity to a new number when needed

        :param new_capacity: new capacity for array will be positive integer

        :return: None
        """
        #if proposed new_capacity is invalid return early Might DElete
        if new_capacity <= 0 or new_capacity < self._size:
            return
        #create new array with new capacity
        new_array = StaticArray(new_capacity)

       #copy old values into new array of new capacity
        for i in range(self._size):
           index_value = self._data.get(i)
           new_array.set(i, index_value)

        #overwrite old array data with new resized array
        self._data = new_array
        self._capacity = new_capacity


    def append(self, value: object) -> None:
        """
        add new value at the end of the array

        :param value: value to be added to the array

        :return: None
        """
        #check if capacity is to be expanded
        if self._size == self._capacity:
            self.resize(self._capacity*2)

        #append value at end of array
        self._data.set(self._size, value)

        #add 1 to size
        self._size += 1



    def insert_at_index(self, index: int, value: object) -> None:
        """
        add new value at the given index of the array

        :param index: int, index of the value to be added to the array
        :param value: obj, value to be added to the array at index

        :return: None
        """
        #error cases check
        if index < 0 or index > self._size:
            raise DynamicArrayException("Index out of bounds")

        #check if index = self._size if so append val
        if self._size == index:
            self.append(value)
            return

        if self._size == self._capacity:
            self.resize(self._capacity*2)

        #in range from first none val down to index val shift vals to right
        for i in range(self._size, index, -1):
            self._data.set(i,self._data.get(i-1))

        #increase array size and insert value
        self._size += 1
        self._data.set(index,value)




    def remove_at_index(self, index: int) -> None:
        """
        Remove a value at a given index from the array

        :param index: int, index of the value to be removed

        :return: None
        """
        #edge cases if needed might already be implemented in class
        if index < 0 or index >= self._size:
            raise DynamicArrayException("index out of range")

        #shift values over to the left overwriting the index given
        for i in range(index+1, self._size):
            self._data.set(i-1,self._data.get(i))

        #reduce capacity with min of 10 to be either 10 or twice self._size
        if self._size < self._capacity/4 and self._capacity > 10:
            new_capacity = self._size*2
            if new_capacity < 10:
                new_capacity = 10
            self.resize(new_capacity)


        #decrease array size
        self._size -= 1

    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Remove portions of an array outside of the given range start to end of size

        :param start_index: int, index to start slice
        :param size: int, size of the slice

        :return: new DynamicArray with portions removed
        """
        #if start index and end index out of bounds or size is 0 or less raise error exceptopn
        if start_index < 0 or start_index >= self._size or size <0 or start_index + size > self._size:
            raise DynamicArrayException("Index out of bounds or invalid size")

        #create array to copy values into
        dynamic_array = DynamicArray()

        for i in range(start_index, start_index+size):
            dynamic_array.append(self._data.get(i))

        return dynamic_array




    def map(self, map_func) -> "DynamicArray":
        """
        Maps any given function to indices of static array returns those values in dynamic array

        :param map_func: function to be mapped to array indices

        :return: new DynamicArray with map_func applied
        """
        dynamic_array = DynamicArray()

        #loop through each array value and apply map_func
        for i in range(self._size):
            map_val = map_func(self._data.get(i))
            dynamic_array.append(map_val)

        return dynamic_array

    def filter(self, filter_func) -> "DynamicArray":
        """
         Returns a dynamic array with values that return true when filter_func is applied

        :param filter_func: a function that returns boolean value

        :return: new dynamic array with values that return true
        """
        dynamic_array = DynamicArray()
        #applies filter to all array values to receive boolean values

        for i in range(self._size):
            filter_val = filter_func(self._data.get(i))
            #checks if value returns true/filters for true
            if filter_val:
                dynamic_array.append(self._data.get(i))

        return dynamic_array


    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Accumulates values of the array using reduce_func iteratively to return a single object the total

        :param reduce_func: function that accumulates values of the array
        :param initializer: initial value to start accumulation optional

        :return: new object from reduce_func operations total
        """
        #returns none when array is empty and no initializer
        if self._size == 0 and initializer is None:
            return None

        #dealing with optional initializer/setting start index and initial val
        if initializer is None:
            running_total = self._data.get(0)
            start_index = 1
        else:
            running_total = initializer
            start_index = 0

        #for all array values apply reduce_func to each index_val to get total
        for i in range(start_index, self._size):
           running_total = reduce_func(running_total, self._data.get(i))

        #returns total which is a singular val/object
        return running_total





def chunk(arr: DynamicArray) -> "DynamicArray":
    """
    chunks non-ascending subsequent values into arrays and adds them to a dynamic array

    :param arr: DynamicArray to be chunked

    :return: new DynamicArray of dynamic arrays with chunked values
    """
    #create array to hold chunk arrays and initiate chunk_array with first val
    dynamic_array = DynamicArray()

    if arr.length() == 0:
        return dynamic_array

    chunk_array = DynamicArray()
    chunk_array.append(arr.get_at_index(0))

    #loop through array comparing previous val to current val to determine chunk breaks
    for i in range(1,arr.length()):
        if arr.get_at_index(i-1) <= arr.get_at_index(i):
            chunk_array.append(arr.get_at_index(i))
        #restart chunking array after appending one to main array when ascending done
        else:
            dynamic_array.append(chunk_array)
            chunk_array = DynamicArray()
            chunk_array.append(arr.get_at_index(i))

    #add final chunk to main dynamic array because loop excludes it
    dynamic_array.append(chunk_array)
    return dynamic_array



def find_mode(arr: DynamicArray) -> tuple[DynamicArray, int]:
    """

    """
    #initialize variables such as counters and mode pointer + initialize array to hold mode
    possible_mode = arr.get_at_index(0)
    current_count = 1
    mode_count = 0
    mode_array = DynamicArray()

    for i in range(1,arr.length()):
        current_value = arr.get_at_index(i)
        if current_value == possible_mode:
            current_count +=1
        else:
            if current_count == mode_count:
                mode_array.append(possible_mode)
            elif current_count > mode_count:
                mode_array = DynamicArray()
                mode_array.append(possible_mode)
                mode_count = current_count
          

            current_count = 1
            possible_mode = current_value


    if current_count == mode_count and mode_count > 0:
        mode_array.append(possible_mode)
    elif current_count > mode_count:
        mode_array = DynamicArray()
        mode_array.append(possible_mode)
        mode_count = current_count

    return mode_array,mode_count








# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    def print_chunked_da(arr: DynamicArray):
        if len(str(arr)) <= 100:
            print(arr)
        else:
            print(f"DYN_ARR Size/Cap: {arr.length()}/{arr.get_capacity()}")
            print('[\n' + ',\n'.join(f'\t{chunk}' for chunk in arr) + '\n]')

    print("\n# chunk example 1")
    test_cases = [
        [10, 20, 30, 30, 5, 10, 1, 2, 3, 4],
        ['App', 'Async', 'Cloud', 'Data', 'Deploy',
         'C', 'Java', 'Python', 'Git', 'GitHub',
         'Class', 'Method', 'Heap']
    ]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# chunk example 2")
    test_cases = [[], [261], [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]]

    for case in test_cases:
        da = DynamicArray(case)
        chunked_da = chunk(da)
        print(da)
        print_chunked_da(chunked_da)

    print("\n# find_mode example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
