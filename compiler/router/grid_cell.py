class grid_cell:
    """
    A single cell that can be occupied in a given layer, blocked,
    visited, etc.
    """
    def __init__(self):
        self.path = False
        self.blocked = False
        self.source = False
        self.target = False
        # -1 means it isn't visited yet
        self.min_cost = -1 

    def reset(self):
        """ 
        Reset the dynamic info about routing. The pins/blockages are not reset so
        that they can be reused.
        """
        self.min_cost=-1
        self.min_path=None
        self.blocked=False
        self.source=False
        self.target=False

        
    def get_type(self):
        if self.blocked:
            return "X"

        if self.source:
            return "S"

        if self.target:
            return "T"

        if self.path:
            return "P"

        # We can display the cost of the frontier
        if self.min_cost > 0:
            return self.min_cost
        
        return None
