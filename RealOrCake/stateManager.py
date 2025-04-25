from cake import Cake
from randomizeCake import RandomizeCake

# State Manager ของ State หลัก ใน state.py
class GameStateManager():
    # Constructor
    def __init__(self, currentState, gsm=None):
        self.currentState = currentState
        self.cake = Cake()

        # หากไม่ได้ส่ง gsm เข้ามา ให้สร้างตัวใหม่
        if gsm:
            self.gsm = gsm  # ใช้ gsm ที่ส่งเข้ามา
        else:
            self.gsm = self  # ถ้าไม่มี gsm ให้ใช้ตัวเองเป็น gsm (ใช้ self เป็นค่า default)

        # สร้าง RandomizeCake โดยส่ง gsm ไป
        self.random_cake = RandomizeCake(self.gsm)  # ส่ง gsm ให้ RandomizeCake
        
        self.event = None
        self.alert = None
        self.alert_active = False
        self.mode = 'random'  # เพิ่ม attribute สำหรับเก็บ mode (default: random)
        self.flavor = None  # เพิ่มการเก็บ flavor ที่เลือก

    # Accessor สำหรับ state
    def get_state(self):
        return self.currentState
    
    # Mutator สำหรับ state
    def set_state(self, state):
        self.currentState = state

    def get_cake(self):
        return self.cake
    
    def set_cake(self, cake):
        self.cake = cake
    
    def get_event(self):
        return self.event
    
    def set_event(self, event):
        self.event = event

    def get_alert(self):
        return self.alert
    
    def set_alert(self, alert):
        self.alert = alert

    def get_alert_active(self):
        return self.alert_active
    
    def set_alert_active(self, alert_active):
        self.alert_active = alert_active

    def reset(self):
        # สร้าง Cake ใหม่ แทนการตั้ง None
        self.cake = Cake()

    def get_randomcake(self):
        return self.random_cake
    
    def set_randomcake(self, random_cake):
        self.random_cake = random_cake
    
    def reset_randomcake(self):
        # สร้าง RandomizeCake ใหม่ แทนการตั้ง None
        self.random_cake = RandomizeCake(self.gsm)

    # ฟังก์ชันเพื่อเก็บ flavor ที่เลือก
    def set_flavor(self, f):
        self.flavor = f
        print(f"[Debug] Flavor set to: {self.flavor}")  # Debug เพื่อยืนยันการตั้งค่า flavor

    # ฟังก์ชันเพื่อดึงค่า flavor ที่เก็บไว้
    def get_flavor(self):
        return self.flavor
    
    # Accessor และ Mutator สำหรับ mode
    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode
