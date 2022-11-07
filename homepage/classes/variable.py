from abc import ABC, abstractmethod

# abstract because all vars should be either binary or cont & should have these methods
class Variable(ABC):
    def __init__(self, name, prompt):
        self.name = name
        self.prompt = prompt
    
    @abstractmethod
    def check_input():
        pass

class Binary_Variable(Variable):
    
    def check_input(self):
    
        # allowed responses
        bools = ['Y', 'N']
        
        var_data = input(self.prompt + '\n')
        # only accept Y/N boolean response otherwise ask again
        while var_data not in bools:
            var_data = input(self.prompt + '\n')
        return var_data

class Continuous_Var(Variable):

    def check_input(self):

        var_data = input(self.prompt + '\n')
        # only accept digit response otherwise ask again
        while var_data.isdigit()==False:
            var_data = input(self.prompt + '\n')
        return var_data

class Categorical_Var(Variable):
    
    def __init__(self, name, prompt, choices):
        self.name = name
        self.prompt = prompt
        self.choices = choices

    def check_input(self):

        var_data = input(self.prompt + '\n')
        # only accept choices from the list otherwise ask again
        while var_data not in self.choices:
            var_data = input(self.prompt + '\n')
        return var_data