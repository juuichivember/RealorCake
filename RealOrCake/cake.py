# สร้าง object cake ทั้ง random cake และ player's cake

class Cake:
    def __init__(self):
        # Dictionary to store each part of the cake
        # Example: {"base": ("plain", "grape"), "topcream": ("feather", "vanilla")}
        self.parts = {"base": ("plain", "milk")}  # have a base as plain milk as a default

    def add_part(self, part, type, color):
        # Add or update a cake part with a specific type and color.
        self.parts[part] = (type, color)
        print(f"Updated {part} with {type} in {color}")

    def reset(self):
        # Reset the cake to have a base as plain milk as a default.
        self.parts = {"base": ("plain", "milk")}
        print("Cake reset!")

    def get_parts(self):
        return self.parts

    def remove_part(self, part):
        # remove a decoration when press none button
        if part in self.get_parts():
            print(f"Removing {part}: {self.parts}")
            self.parts.pop(part)
            print(f"{part} is removed: {self.parts}")
        else:
            print(f"There is no {part} in the cake.")

    def set_flavor(self, flavor):
        # สร้างหรืออัปเดตส่วน filling
        self.parts['filling'] = ('none', flavor)

    def get_flavor(self):
        # คืนแค่ชื่อรสชาติ
        return self.parts.get('filling', (None, None))[1]
