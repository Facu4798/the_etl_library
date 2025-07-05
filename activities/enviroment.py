class Env:
    def __init__(self):
        self.items = []
        self.activities = []
        import numpy as np
        self.matrix = np.array([])

    def show(self,fig_scale=1.5,node_scale=1000):
        """
        Plot a DAG of the environment's activities.
        The nodes are the activities, and the edges are data transfers between them.
        - **fig_scale:** scale of the matplotlib figure
        - **node_scale:** scale of the nodes in the graph
        """
        import networkx as nx
        import matplotlib.pyplot as plt
        import numpy as np

        # Create DAG from adjacency matrix
        G = nx.from_numpy_array(self.matrix, create_using=nx.DiGraph)
        
        labels = {i: self.items[i] for i in range(len(self.items))}
        
        node_size = max(len(node) for node in self.items) * node_scale
        print(node_size)

        plt.figure(figsize=(node_size/1000*fig_scale, node_size/1000*fig_scale))
        # Plot with hierarchical layout
        pos = nx.planar_layout(G)  # or nx.planar_layout(G) for DAGs
        nx.draw(G, 
                pos,
                labels=labels, 
                with_labels=True,
                node_color='lightblue',
                node_size=node_size,
                arrows=True,
                arrowsize=20)
        plt.show()

    def _add_item(self,item,parent=None):
        
        import numpy as np
        if item.id in self.items:
            raise ValueError(f"Item with id {item.id} already exists in the environment.")
        self.activities.append(item)
        self.items.append(item.id)
        if self.matrix.shape[0] == 0:
            # Initialize the matrix with a single item
            self.matrix = np.array([[0]])
        else:
            # add a new column for the item
            self.matrix = np.append(self.matrix, np.zeros((self.matrix.shape[0], 1)), axis=1)
            # add a new row for the item
            self.matrix = np.append(self.matrix, np.zeros((1, self.matrix.shape[1])), axis=0)
        # set the parent-item relationship
        if parent != None:
            parent_index = self.items.index(parent.id)
            self.matrix[parent_index, -1] = 1
        

    def run(self):
        """
        Execute all activities in the DAG based on topological order.
        Returns a dictionary mapping activity IDs to their outputs.
        """
        import numpy as np
        from collections import deque, defaultdict
        
        if len(self.activities) == 0:
            return {}
        
        # Create adjacency list from matrix for easier traversal
        n = len(self.items)
        adj_list = defaultdict(list)
        in_degree = [0] * n
        
        # Build adjacency list and calculate in-degrees
        for i in range(n):
            for j in range(n):
                if self.matrix[i, j] == 1:
                    adj_list[i].append(j)
                    in_degree[j] += 1
        
        # Topological sort using Kahn's algorithm
        queue = deque()
        for i in range(n):
            if in_degree[i] == 0:
                queue.append(i)
        
        execution_order = []
        while queue:
            current = queue.popleft()
            execution_order.append(current)
            
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
        
        for activity_idx in execution_order:
            activity = self.activities[activity_idx]
            
            # Collect inputs from parent activities
            parent_outputs = []
            for parent_idx in range(n):
                if self.matrix[parent_idx, activity_idx] == 1:
                    if parent_idx in activity_outputs:
                        parent_outputs.append(activity_outputs[parent_idx])
            
            # Determine input for current activity
            if len(parent_outputs) == 0:
                # No parents, use activity's predefined input
                activity_input = None
            elif len(parent_outputs) == 1:
                # Single parent, pass its output directly
                activity_input = parent_outputs[0]
            else:
                # Multiple parents, pass list of outputs
                activity_input = parent_outputs
            
            # Run the activity
            output = activity.run(activity_input)
            activity_outputs[activity_idx] = output
            outputs[activity.id] = output
        
        return outputs

    def __str__(self):
        return "ETL enviroment"
    

