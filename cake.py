class Cake:
    def __init__(self):
        # Dictionary to store each part of the cake
        # Example: {"base": ("layered", "grape"), "topcream": ("feather", "vanilla")}
        self.parts = {}

    def add_part(self, part, type, color):
        """Add or update a cake part with a specific type and color."""
        self.parts[part] = (type, color)
        print(f"Updated {part} with {type} in {color}")

    def reset(self):
        """Reset the cake to an empty state."""
        self.parts = {}
        print("Cake reset!")

    def get_parts(self):
        return self.parts
        
