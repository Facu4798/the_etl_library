class Env:
    def __init__(self):
        self.items = []
        self.activities = []
        import numpy as np
        self.matrix = np.array([])

    def show(self,fig_scale=1.5,node_scale=1000):
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
        pass

    def __str__(self):
        return "ETL enviroment"
    

