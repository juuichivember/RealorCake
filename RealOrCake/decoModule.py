import os, pygame, sys

# เก็บ module ที่ใช้โหลดรูปภาพ
# ใช้ os.path.join ในการเรียก path เท่านั้น 

def load_image(folder, filename, scale=None, smooth=True):
    # โหลดรูปทั่วไป โดยใช้ os.path.join
    # ใช่้ได้แค่รูปที่อยู่ใน assets และ folder แค่ 1 อัน เช่น assets/buttob/next_button.png แต่ 
    # assets/decoration_elements/base_layered/base_layered_carrot.png จะใช้ไม่ได้

    base_path = get_base_path()
    path = os.path.join(base_path, "assets", folder, filename)
    if os.path.exists(path):
        try:
            image = pygame.image.load(path).convert_alpha()
            if scale:
                if smooth:
                    image = pygame.transform.smoothscale(image, scale)
                image = pygame.transform.scale(image, scale)
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")
    else:
        print(f"File not found: {path}")
    return pygame.Surface((1, 1), pygame.SRCALPHA)

def load_cake_part(state_name, cake_type, color):
    # โหลดรูป decoration_elemnents ยกเว้น thumbnail และ Color
    
    if not cake_type:
        return None
    if not color:
        color = "grape"
    base_path = get_base_path()
    path = os.path.join(base_path, "assets", "decoration_elements", f"{state_name}_{cake_type}", f"{state_name}_{cake_type}_{color}.png")
    if os.path.exists(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except Exception as e:
            print(f"Error loading cake part {path}: {e}")
    else:
        pass
        #print(f"File not found: {path}")
    return None

def get_base_path():
    # หา absolute path ปจบ

    if getattr(sys, 'frozen', False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))