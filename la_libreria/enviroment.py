class Env:
    def __init__(self):
        self.items = []
        self.activities = []
        import numpy as np
        self.matrix = np.array([])

    def show(self,plot=True):
        """
        Plot a DAG of the environment's activities.
        The nodes are the activities, and the edges are data transfers between them.
        - **fig_scale:** scale of the matplotlib figure
        - **node_scale:** scale of the nodes in the graph
        """
        import graphviz
        import numpy as np
        from graphviz import Digraph
        from collections import defaultdict
        import matplotlib.pyplot as plt

        # Create adjacency list from matrix for easier traversal
        n = len(self.items)
        adj_list = defaultdict(list)
        in_degree = [0] * n # left vicinity

        # Build adjacency list and calculate in-degrees
        for i in range(n):
            for j in range(n):
                if self.matrix[i, j] == 1:
                    adj_list[i].append(j) # add right vicinity to i
                    in_degree[j] += 1 # increase left vicinity of j
        
        dot = Digraph()
        for node, neighbors in adj_list.items():
            dot.node(self.items[node])
            for n in neighbors:
                dot.edge(self.items[node], self.items[n])
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dot.render(f'dag_{timestamp}',format='png')
        if plot:
            img = plt.imread(f'dag_{timestamp}.png')
            plt.imshow(img)
            # Get resolution from image metadata if available
            height, width = img.shape[:2]
            dpi = 30
            width_inch = width / dpi
            height_inch = height / dpi
            plt.gcf().set_size_inches(width_inch, height_inch)
            plt.axis('off')
            plt.show()


    def _add_item(self,item,parent=None):
        
        import numpy as np
        if item.id in self.items:
            raise ValueError(f"Item with id {item.id} already exists in the environment.")
        self.activities.append(item)
        self.items.append(item.id)
        if self.matrix.shape[0] == 0:#for root activity(empty matrix)
            # Initialize the matrix with a single item
            self.matrix = np.array([[0]])
        else:
            # add a new column for the item
            self.matrix = np.append(self.matrix, np.zeros((self.matrix.shape[0], 1)), axis=1)
            # add a new row for the item
            self.matrix = np.append(self.matrix, np.zeros((1, self.matrix.shape[1])), axis=0)
        # set the parent-item relationship
        if parent != None:
            if type(parent) == list:
                for p in parent:
                    parent_index = self.items.index(p.id)
                    self.matrix[parent_index, -1] = 1
            else:
                parent_index = self.items.index(parent.id)
                self.matrix[parent_index, -1] = 1
        

    def run(self,input=None,log_path = None):
        """
        Execute all activities in the DAG based on topological order.
        Returns a dictionary mapping activity IDs to their outputs.
        """
        if log_path is not None:
            logger_obj = logger(path=log_path)
        else:
            logger_obj = None
        
        import polars as pl
        ctx = pl.SQLContext()

        import numpy as np
        from collections import deque, defaultdict
        
        if len(self.activities) == 0:
            return {}
        
        # Create adjacency list from matrix for easier traversal
        n = len(self.items)
        adj_list = defaultdict(list)
        in_degree = [0] * n # left vicinity

        # Build adjacency list and calculate in-degrees
        for i in range(n):
            for j in range(n):
                if self.matrix[i, j] == 1:
                    adj_list[i].append(j) # add right vicinity to i
                    in_degree[j] += 1 # increase left vicinity of j
                    
        # Topological sort using Kahn's algorithm
        num_roots = 0
        queue = deque()
        for i in range(n):
            if in_degree[i] == 0: # no left vicinity(root nodes)
                queue.append(i)
                num_roots += 1
                
        execution_order = []
        while queue: # while queue has elements
            current = queue.popleft() # get first element
            execution_order.append(current) # add it to execution order
            
            for neighbor in adj_list[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        # Check for cycles
        if len(execution_order) != n:
            raise ValueError("Cycle detected in the DAG. Cannot execute.")
        
        # Execute activities in topological order
        outputs = {}
        activity_outputs = {}  # Map activity index to output
        
        count = 0
        for activity_idx in execution_order:
            activity = self.activities[activity_idx] # get activity object
            
            # Get input from parent activities
            inputs = {}
            if activity.parent is None:
                inputs = None
            else:
                if type(activity.parent) == list:
                    for parent in activity.parent:
                        inputs.update({parent.output_name: parent.output})
                        parent.output = None  # Clear parent's output to release memory
                else:
                    inputs = {activity.parent.output_name : activity.parent.output}
                    activity.parent.output = None  # Clear parent's output to release memory
            
            #update activity input
            activity.input = inputs
            
            # Run the activity
            if count < num_roots:
                activity.run(input, logger=logger_obj)
            else:
                activity.run(logger=logger_obj)

        return None

    def __str__(self):
        return "ETL environment"
    

class logger:
    def __init__(self,path=""):
        import os 
        self.path = path
        if path != "":
            if not os.path.exists(path):
                os.makedirs(path)
        from datetime import datetime
        self.logfile = os.path.join(path,f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
    
    def log(self,msg):
        fh = open(self.logfile,'a')
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        fh.write(f"[{timestamp}] {msg}\n")
        fh.close()