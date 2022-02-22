import pandas as pd
import numpy as np

class DSL():

    '''Domain Specific Language consisting of functions and relations'''

    def __init__(self):
        # Value to Attribute Converter
        self.val2attr = {'shape': ['circle', 'rectangle'], 'color': ['red', 'green', 'blue', 'orange', 'gray', 'yellow']}
        self.get_attr = lambda x: [k for k, v in self.val2attr.items() if x in v][0]
        self.ans2str = {0: 'Top Left', 1: 'Top Right', 2:'Bottom Left', 3:'Bottom Right'}

        # String to Function
        self.str2func = {'filter_different_shape': self.filter_different_shape, 
                         'filter_different_color': self.filter_different_color, 
                         'filter_same_shape': self.filter_same_shape, 
                         'filter_same_color': self.filter_same_color, 
                         'query_pair': self.query_pair, 
                         'generate_pair': self.generate_pair}

    def generate_pair(self, prev_out):
        # creat seaprate columns fro x and yposition
        prev_out['x_pos'] = [pos[0] for pos in list(prev_out['position'])]
        prev_out['y_pos'] = [pos[1] for pos in list(prev_out['position'])]

        #sort by x and y position
        prev_out = prev_out.sort_values(["y_pos", 'x_pos'], ascending = (True, True))

        # remove the extra columns and reset the index of the dataframe
        del prev_out['x_pos']
        del prev_out['y_pos']
        prev_out = prev_out.reset_index(drop=True)

        # Add a pair_ids colum
        pair_ids = list(range(int(len(prev_out)/2)))*2
        pair_ids.sort() 
        prev_out['pair'] = pair_ids
        
        return prev_out

    def relate(self, prev_out, attribute, relation):
        result = []
        for id in prev_out['pair']:
            pair = prev_out[prev_out['pair']==id]
            pair=pair.reset_index(drop=True)

            if relation == 'different':
                if pair[attribute][0] != pair[attribute][1] and id not in result:
                    result.append(id)

            elif relation == 'same':
                if pair[attribute][0] == pair[attribute][1] and id not in result:
                    result.append(id)

        return prev_out[prev_out['pair'].isin(result)]


    def filter_different_shape(self, prev_out):
        return self.relate(prev_out, attribute = 'shape', relation = 'different')

    def filter_different_color(self, prev_out):
        return self.relate(prev_out, attribute = 'color', relation = 'different')

    def filter_same_shape(self, prev_out):
        return self.relate(prev_out, attribute = 'shape', relation = 'same')

    def filter_same_color(self, prev_out):
        return self.relate(prev_out, attribute = 'color', relation = 'same')

    def query_pair(self, prev_out):
        return list(prev_out['pair'])[0]

        
class ProgramExecutor(DSL):

    '''Executes a given program'''
    def __init__(self):
        super().__init__()
        pass
    
    def func_executor(self, func, prev_out):
        '''Executes a given function with or without a parameter'''

        # Two arg functions
        prev_out = self.str2func[func](prev_out)
        return prev_out
    
    def __call__(self, scene, program):
        '''Executes a program on the scene'''
        self.scene = scene
        
        prev_out = None

        for func in program:
            func = func.lstrip()
            func = func.replace(" ", "_")

            if prev_out is None:
                prev_out = self.func_executor(func, self.scene)

            else:
                prev_out = self.func_executor(func, prev_out)


        
        return self.ans2str[prev_out]