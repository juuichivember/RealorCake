from cake import Cake
import random 

# สร้าง randomize cake โดยทำการ inherit คลาส Cake มา
class RandomizeCake(Cake):
    def __init__(self, gsm):
        super().__init__()
        self.gsm = gsm  # รับ GameStateManager ที่ส่งเข้ามาในตัวสร้าง
        self.filling = None  # ตัวแปรเพื่อเก็บ filling ที่สุ่ม

    def random_parts(self):
        # ตัวเลือกสำหรับแต่ละ part
        random_options = {
            "filling":     ["vanilla","chocolate","strawberry","orange","blueberry"],
            "base":        ["layered", "plain"],
            "behindcream": ["feather", "wave", "none"],
            "lowercream":  ["feather", "wave", "none"],
            "middlecream": ["ribbon",  "ruffle", "none"],
            "topcream":    ["feather", "wave", "none"],
            "topping":     ["bow", "crown", "floweredge", "flowertop", "pearl",
                            "strawberry_3", "strawberry_4", "none"]
        }
        color_names = [
            "mint", "carrot", "charcole", "grape", "bluberry", "coffee",
            "vanilla", "milk", "strawberry", "chocolate", "redvelvet", "none"
        ]

        for part, options in random_options.items():
            # 1) กรณี filling: ไม่มีชนิดอื่น ใช้ type="none" และ color = ชื่อรส
            if part == "filling":
                flavor = random.choice(options)  # กำหนดค่าให้ flavor (ไม่มี 'none' ในตัวเลือก)
                self.add_part(part, "none", flavor)  # ค่าของ filling จะเป็น flavor ที่สุ่มมา
                continue

            # 2) กรณีอื่น ๆ: แบบเดิม
            rand_type = random.choice(options)
            if rand_type == "none":
                rand_color = "none"
            else:
                if part == "base":
                    # สำหรับฐาน เลือกสีจาก color_names ยกเว้น 'none'
                    rand_color = random.choice(color_names[:-1])
                else:
                    rand_color = random.choice(color_names)
            self.add_part(part, rand_type, rand_color)


    def random_filling(self):
        random_filling = random.choice(["vanilla", "chocolate", "strawberry", "orange", "blueberry"])
        self.add_part('filling', 'none', random_filling)
        # เก็บรสชาติที่สุ่มไว้ใน GameStateManager
        self.gsm.set_flavor(random_filling)  # เชื่อมโยงกับ GameStateManager
        return random_filling

    def reset(self):
        super().reset()  # เรียก reset ของ Cake
        # รีเซ็ตการสุ่มไส้เค้กใหม่
        self.random_parts()

    def get_filling(self):
        return self.filling  # คืนค่า filling ที่สุ่ม
