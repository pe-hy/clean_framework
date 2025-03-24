import numpy as np

class VectorTransformations:
    def __init__(self, num_values):
        self.num_values = num_values
    
    def get_increment_by_index(self, index,cond_index):
        def transform1(vec):
            """Increment first component by value of third component"""
            result = vec.copy()
            result[index] = (result[index] + result[cond_index]) % self.num_values
            return result
        return transform1
    def get_increment_by_index_and_odd(self, index,cond):
        def transform2(vec):
            """Increment second component based on first component (odd/even)"""
            result = vec.copy()
            if vec[cond] % 2 == 0:
                result[index] = (result[index] + 1) % self.num_values
            else:
                result[index] = (result[index] + 2) % self.num_values
            return result
        return transform2
    
    def transform3(self, vec):
        """Make all odd numbers even by incrementing"""
        result = vec.copy()
        for i in range(len(result)):
            if result[i] % 2 == 1:
                result[i] = (result[i] + 1) % self.num_values
        return result
    
    def transform4(self, vec):
        """Sort the vector"""
        return np.sort(vec) % self.num_values
    
    def transform5(self, vec):
        """Swap first with fifth and second with fourth components"""
        result = vec.copy()
        result[0], result[4] = result[4], result[0]
        result[1], result[3] = result[3], result[1]
        return result
    
    def transform6(self, vec):
        """Circular shift right by 1"""
        result = np.roll(vec, 1)
        return result % self.num_values
    
    def transform7(self, vec):
        """Circular shift left by 2"""
        result = np.roll(vec, -2)
        return result % self.num_values
    
    def transform8(self, vec):
        """Multiply each component by its index+1"""
        result = vec.copy()
        for i in range(len(result)):
            result[i] = (result[i] * (i + 1)) % self.num_values
        return result
    
    def transform9(self, vec):
        """Add component i to component i+1"""
        result = vec.copy()
        for i in range(len(result)-1):
            result[i+1] = (result[i+1] + result[i]) % self.num_values
        return result
    
    def transform10(self, vec):
        """Replace each number with its square"""
        return (vec * vec) % self.num_values
    
    def transform11(self, vec):
        """Increment third component by sum of first two"""
        result = vec.copy()
        result[2] = (result[2] + result[0] + result[1]) % self.num_values
        return result
    
    def transform12(self, vec):
        """Reverse the vector"""
        return vec[::-1]
    
    def transform13(self, vec):
        """Replace each number with the maximum of itself and its next neighbor"""
        result = vec.copy()
        for i in range(len(result)-1):
            result[i] = max(vec[i], vec[i+1]) % self.num_values
        return result
    
    def transform14(self, vec):
        """Add the first element to all others"""
        result = vec.copy()
        for i in range(1, len(result)):
            result[i] = (result[i] + result[0]) % self.num_values
        return result
    
    def transform15(self, vec):
        """Multiply each even-indexed element by 2"""
        result = vec.copy()
        for i in range(0, len(result), 2):
            result[i] = (result[i] * 2) % self.num_values
        return result
    
    def transform16(self, vec):
        """Replace each element with the sum of its neighbors"""
        result = vec.copy()
        temp = vec.copy()
        for i in range(len(result)):
            left = temp[(i-1) % len(temp)]
            right = temp[(i+1) % len(temp)]
            result[i] = (left + right) % self.num_values
        return result
    
    def transform17(self, vec):
        """Increment components where the next component is larger"""
        result = vec.copy()
        for i in range(len(result)-1):
            if vec[i+1] > vec[i]:
                result[i] = (result[i] + 1) % self.num_values
        return result
    
    def transform18(self, vec):
        " zero out the last component"
        result = vec.copy()
        result[-1] = 0
        return result
    
    def transform19(self, vec):
        " zero out the last three components"
        result = vec.copy()
        result[-3:] = 0
        return result
    
 


    def get_all_transformations(self):
        """Return a list of all transformation functions"""
        return [
            (self.get_increment_by_index(0,1), "Increment first component by value of second component"),
            (self.get_increment_by_index_and_odd(1,2), "Increment second component based on first component (odd/even)"),
            (self.get_increment_by_index(2,1), "Increment third component by value of first component"),
            (self.get_increment_by_index_and_odd(3,4), "Increment fourth component based on fifth component (odd/even)"),
            (self.get_increment_by_index(4,0), "Increment fifth component by value of first component"),
            (self.transform3, "Make all odd numbers even by incrementing"),
            (self.transform4, "Sort the vector"),
            (self.transform5, "Swap first with fifth and second with fourth components"),
            (self.transform6, "Circular shift right by 1"),
            (self.transform7, "Circular shift left by 2"),
            (self.transform8, "Multiply each component by its index+1"),
            (self.transform9, "Add component i to component i+1"),
            (self.transform10, "Replace each number with its square"),
            (self.transform11, "Increment third component by sum of first two"),
            (self.transform12, "Reverse the vector"),
            (self.transform13, "Replace each number with the maximum of itself and its next neighbor"),
            (self.transform14, "Add the first element to all others"),
            (self.transform15, "Multiply each even-indexed element by 2"),
            (self.transform16, "Replace each element with the sum of its neighbors"),
            (self.transform17, "Increment components where the next component is larger")
        ]
