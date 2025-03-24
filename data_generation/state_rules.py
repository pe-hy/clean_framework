import numpy as np

class StateRules:
    
    def rule1(self, vec):
        """First component cannot be even if the second is odd"""
        return not (vec[0] % 2 == 0 and vec[1] % 2 == 1)
    
    def rule2(self, vec):
        """Not all components can be odd"""
        return not all(x % 2 == 1 for x in vec)
    
    def rule3(self, vec):
        """Fifth cannot be a multiple of the second"""
        if vec[1] == 0:  # Handle division by zero case
            return True
        return vec[4] % vec[1] != 0
    
    def rule4(self, vec):
        """Third cannot be greater than the fifth"""
        return vec[2] <= vec[4]
    
    def rule5(self, vec):
        """Not all elements can be distinct"""
        return len(set(vec)) < len(vec)
    
    def get_all_rules(self):
        """Return a list of all rules with their descriptions"""
        return [
            (self.rule1, "First component cannot be even if the second is odd"),
            (self.rule2, "Not all components can be odd"),
            (self.rule3, "Fifth cannot be a multiple of the second"),
            (self.rule4, "Third cannot be greater than the fifth"),
            (self.rule5, "Not all elements can be distinct")
        ]
    
    def check_all_rules(self, vec):
        """Check if a vector satisfies all rules
        Returns: 
            - bool: whether all rules are satisfied
            - list: descriptions of violated rules
        """
        violations = []
        for rule, description in self.get_all_rules():
            if not rule(vec):
                violations.append(description)
        return len(violations) == 0, violations

