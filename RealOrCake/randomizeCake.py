from cake import Cake
import random 

# สร้าง randomzie cake โดยทำการ inherit คลาส Cake มา

class RandomizeCake(Cake):
    def __init_subclass__(cls):
        return super().__init_subclass__()
    def add_part(self, part, type, color):
        return super().add_part(part, type, color)
    def reset(self):
        return super().reset()
    
    def random_parts(self):
        # เพิ่ม function เพื่อสุ่มเค้ก

        random_options = {
            "base":        ["layered", "plain"],
            "behindcream": ["feather", "wave", "none"],
            "lowercream":  ["feather", "wave", "none"],
            "middlecream": ["ribbon",  "ruffle", "none"],
            "topcream":    ["feather", "wave", "none"],
            "topping":     ["bow", "crown", "floweredge", "flowertop", "pearl", "strawberry_3", "strawberry_4", "none"]
        }
        color_names = [
            "mint", "carrot", "charcole", "grape", "bluberry", "coffee",
            "vanilla", "milk", "strawberry", "chocolate", "redvelvet", "none"
        ]
        for part, type in random_options.items():
            rand_type = random.choice(type)
            if rand_type == "none":
                rand_color = "none"
            else:
                if part == "base":
                    rand_color = random.choice(color_names[:len(color_names) - 1])
                else:
                    rand_color = random.choice(color_names)
            self.add_part(part, rand_type, rand_color)


