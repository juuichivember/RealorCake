import pygame
import os

# เริ่มต้น Pygame และกำหนดขนาดหน้าจอ
pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("RealOrCake - Decoration State with Sub-States")

# ----------------------------------------------------------------------------
# 1) ฟังก์ชันโหลดภาพ
# ----------------------------------------------------------------------------
def load_image(path, scale=None):
    if os.path.exists(path):
        try:
            image = pygame.image.load(path).convert_alpha()
            if scale:
                image = pygame.transform.scale(image, scale)
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")
    else:
        print(f"File not found: {path}")
    # คืน Surface เปล่า ๆ ถ้าโหลดไม่ได้ (ป้องกัน error)
    return pygame.Surface((1,1), pygame.SRCALPHA)

# ----------------------------------------------------------------------------
# 2) โหลดภาพพื้นหลัง / ปุ่ม / พาเลตต์สี ฯลฯ (โค้ดเดิม)
# ----------------------------------------------------------------------------
background = load_image("Elements/shop_background.png", (WIDTH, HEIGHT))

shelve = load_image("Elements/shelve.png", (775, 806))
shelve_pos = (1083, 138)

reset_button = load_image("Elements/reset_button.png", (212, 124))
reset_rect = reset_button.get_rect(topleft=(1240, 940)) if reset_button else None

finish_button = load_image("Elements/finish_button.png", (212, 124))
show_rect = finish_button.get_rect(topleft=(1540, 940)) if finish_button else None

back_button = load_image("Elements/back_button.png", (222, 122))
back_rect = back_button.get_rect(topleft=(50, 50)) if back_button else None

palette_bg = load_image("Elements/Color/painttray.png", (150, 390))
palette_pos = (930, 150)

# ----------------------------------------------------------------------------
# 3) จัดการ "สี" (color) ที่มีในพาเลตต์ (โค้ดเดิม)
# ----------------------------------------------------------------------------
color_names = [
    "none", "grape", "bluberry", "mint", "vanilla", "milk",
    "carrot", "redvelvet", "strawberry", "charcole", "chocolate", "coffee"
]

color_icons = {}
for color in color_names:
    img = load_image(f"Elements/Color/{color}.png", (50, 50))
    if img:
        color_icons[color] = img

# คำนวณตำแหน่งของไอคอนสีในพาเลตต์ (2 คอลัมน์)
color_positions = []
for i, _ in enumerate(color_names):
    col = i % 2
    row = i // 2
    x_pos = palette_pos[0] + 20 + (col * 60)
    y_pos = palette_pos[1] + 20 + (row * 60)
    color_positions.append((x_pos, y_pos))

# ----------------------------------------------------------------------------
# 4) สร้าง "sub-state" และข้อมูลตัวเลือก (type) ของแต่ละ sub-state
# ----------------------------------------------------------------------------
states = ["base", "behindcream", "lowercream", "middlecream", "topcream", "topping"]

state_options = {
    "base":        ["layered", "plain"],
    "behindcream": ["feather", "wave"],
    "lowercream":  ["feather", "wave"],
    "middlecream": ["ribbon",  "ruffle"],
    "topcream":    ["feather", "wave"],
    "topping":     ["bow", "crown", "floweredge", "flowertop", "pearl", "strawberry_3", "strawberry_4"]
}

# เก็บการเลือก (type และ color) ของผู้ใช้แยกตาม sub-state
selected_type = {s: None for s in states}
selected_color = {s: None for s in states}

# โหมด (sub-state) ปัจจุบัน
current_mode = "base"

# ----------------------------------------------------------------------------
# 5) โหลดไอคอนปุ่มด้านบนสำหรับเปลี่ยน sub-state
#    (ไฟล์ตัวอย่าง: 1Base_button.png, 2Topcream_button.png, ...)
# ----------------------------------------------------------------------------
mode_icons = {}
icon_positions = {}
start_x = 1100  # ตำแหน่ง x เริ่มต้นของไอคอน (ปรับตามดีไซน์)
gap_x = 125    # ระยะห่างระหว่างปุ่ม

for i, st in enumerate(states):
    # ตัวอย่างไฟล์: f"{st}_button.png" เช่น "base_button.png"
    icon_path = f"Elements/{st}_button.png"
    icon_img = load_image(icon_path, (110, 110))  # ปรับขนาดตามต้องการ
    mode_icons[st] = icon_img
    icon_positions[st] = (start_x + i*gap_x, 25)

# ----------------------------------------------------------------------------
# 6) ตำแหน่งของชั้นวาง (ตำแหน่งที่จะวางภาพตัวเลือก type)
# ----------------------------------------------------------------------------
shelf_positions = [
    (1122, 160), (1339, 160), (1556, 160),
    (1122, 394), (1339, 394), (1556, 394),
    (1122, 636), (1339, 636), (1556, 636)
]

# ----------------------------------------------------------------------------
# 7) ฟังก์ชันสำหรับโหลด "ภาพเค้กจริง" ที่ผู้ใช้เลือก
#    path = "Elements/{state}_{cake_type}/{state}_{cake_type}_{color}.png"
#
#   ปรับปรุง: เมื่อมีการเลือก type แล้วแต่ยังไม่เลือกสี
#   ให้ใช้สีเริ่มต้น "grape" แทน
# ----------------------------------------------------------------------------
def load_cake_part(state_name, cake_type, color):
    if not cake_type:
        return None  # หากยังไม่ได้เลือก type ไม่ต้องโหลดอะไร
    if not color:
        color = "grape"  # ใช้สี default เป็น "grape" หากยังไม่ถูกเลือก
    path = f"Elements/{state_name}_{cake_type}/{state_name}_{cake_type}_{color}.png"
    if os.path.exists(path):
        try:
            return pygame.image.load(path).convert_alpha()
        except Exception as e:
            print(f"Error loading cake part {path}: {e}")
    else:
        print(f"File not found: {path}")
    return None

# ----------------------------------------------------------------------------
# 8) ตัวแปรและฟอนต์อื่น ๆ
# ----------------------------------------------------------------------------
selected_color_global = None  # เก็บสีที่ผู้ใช้คลิกล่าสุด (หรือจะย้ายไปใช้ per-state ก็ได้)
show_cakes = True
font = pygame.font.Font(None, 50)

running = True

# ----------------------------------------------------------------------------
# 9) ฟังก์ชันวาดฉาก (draw_scene)
# ----------------------------------------------------------------------------
def draw_scene():
    screen.blit(background, (0, 0))
    screen.blit(palette_bg, palette_pos)

    # วาดชั้นวาง
    if shelve:
        screen.blit(shelve, shelve_pos)

    # วาดปุ่ม Back
    if back_button:
        screen.blit(back_button, back_rect.topleft)

    # วาดปุ่มเปลี่ยน sub-state (ไอคอนด้านบน)
    for st in states:
        icon_img = mode_icons[st]
        if icon_img:
            screen.blit(icon_img, icon_positions[st])

    # วาดพาเลตต์สี
    for i, color in enumerate(color_names):
        if color in color_icons:
            screen.blit(color_icons[color], color_positions[i])

    # วาดข้อความหัวข้อ
    text = font.render("RealOrCake - Decoration State with Sub-States", True, (0,0,0))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, 100))

    # วาดตัวเลือกบนชั้นวาง เฉพาะ sub-state ปัจจุบัน
    if show_cakes:
        types_for_this_state = state_options[current_mode]
        for i, cake_type in enumerate(types_for_this_state):
            if i < len(shelf_positions):
                # โหลด thumbnail สำหรับแต่ละ type
                thumb_path = f"Elements/thumbnail/{current_mode}_{cake_type}.png"
                thumb_img = load_image(thumb_path, (260, 260))
                if thumb_img:
                    screen.blit(thumb_img, shelf_positions[i])
        # วาดปุ่ม reset, show
        if reset_button:
            screen.blit(reset_button, reset_rect.topleft)
        if finish_button:
            screen.blit(finish_button, show_rect.topleft)

    # วาดเค้ก (รวมทุก sub-state) ทับซ้อนกันตามลำดับที่ต้องการ
    # ลำดับ: base -> topcream -> lowercream -> middlecream -> behindcream -> topping
    cake_draw_order = ["base", "topcream", "lowercream", "middlecream", "behindcream", "topping"]
    final_cake_x, final_cake_y = 100, 248

    for st in cake_draw_order:
        t = selected_type[st]      # type ที่ผู้ใช้เลือก
        c = selected_color[st]     # color ที่ผู้ใช้เลือก (หรือ default "none" ถ้ายังไม่เลือก)
        part_img = load_cake_part(st, t, c)
        if part_img:
            part_img = pygame.transform.scale(part_img, (847, 847))
            screen.blit(part_img, (final_cake_x, final_cake_y))

# ----------------------------------------------------------------------------
# 10) ฟังก์ชันจัดการเหตุการณ์ (handle_events)
# ----------------------------------------------------------------------------
def handle_events():
    global running, show_cakes, current_mode
    global selected_color_global

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # (1) ตรวจสอบการคลิกที่ปุ่มเปลี่ยน sub-state (ไอคอนด้านบน)
            for st in states:
                icon_img = mode_icons[st]
                if icon_img:
                    icon_rect = pygame.Rect(icon_positions[st][0],
                                            icon_positions[st][1],
                                            icon_img.get_width(),
                                            icon_img.get_height())
                    if icon_rect.collidepoint(x, y):
                        current_mode = st
                        print(f"Switched to sub-state: {current_mode}")
                        break

            # (2) ตรวจสอบการคลิกที่ปุ่ม Reset
            if reset_rect and reset_rect.collidepoint(x, y):
                for st in states:
                    selected_type[st] = None
                    selected_color[st] = None
                selected_color_global = None
                print("Reset selection")

            # (3) ตรวจสอบการคลิกที่ปุ่ม Show (สลับการแสดงผลตัวเลือกบนชั้น)
            if show_rect and show_rect.collidepoint(x, y):
                show_cakes = not show_cakes
                print(f"Show cakes: {show_cakes}")

            # (4) ตรวจสอบการคลิกที่ปุ่ม Back
            if back_rect and back_rect.collidepoint(x, y):
                print("Back to Home")
                # เพิ่มการทำงานกลับหน้าหลักหรือออกจากเกมตามต้องการ

            # (5) ตรวจสอบการคลิกที่พาเลตต์สี
            for i, pos in enumerate(color_positions):
                color_rect = pygame.Rect(pos[0], pos[1], 50, 50)
                if color_rect.collidepoint(x, y):
                    selected_color_global = color_names[i]
                    selected_color[current_mode] = selected_color_global
                    print(f"Selected color for [{current_mode}]: {selected_color_global}")

            # (6) ตรวจสอบการคลิกบน "ชั้นวาง" เพื่อเลือก type
            if show_cakes:
                types_for_this_state = state_options[current_mode]
                for i, cake_type in enumerate(types_for_this_state):
                    if i < len(shelf_positions):
                        rect = pygame.Rect(shelf_positions[i], (260, 260))
                        if rect.collidepoint(x, y):
                            selected_type[current_mode] = cake_type
                            print(f"Selected type for [{current_mode}]: {cake_type}")

# ----------------------------------------------------------------------------
# 11) ฟังก์ชันหลัก (main)
# ----------------------------------------------------------------------------
def main():
    global running
    clock = pygame.time.Clock()

    while running:
        handle_events()
        draw_scene()
        pygame.display.flip()
        clock.tick(60)  # จำกัดเฟรมเรตที่ 60 fps

    pygame.quit()

if __name__ == '__main__':
    main()
