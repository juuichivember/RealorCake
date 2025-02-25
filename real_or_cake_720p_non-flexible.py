import pygame
import os

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
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
    return pygame.Surface((1, 1), pygame.SRCALPHA)

# ----------------------------------------------------------------------------
# 2) โหลดภาพพื้นหลัง / ปุ่ม / พาเลตต์สี ฯลฯ โดยปรับตำแหน่ง x ให้ขยับไปด้านขวา 100px
# ----------------------------------------------------------------------------
background = load_image("Elements/shop_background_720.png", (WIDTH, HEIGHT))
# ในกรณี background ถ้าอยากให้ขยับ ก็ให้ blit ด้วยตำแหน่ง (100, 0) ใน draw_scene

shelve = load_image("Elements/shelve.png", (465, 484))
shelve_pos = (790, 88)         # เดิม (650, 78) -> +100

reset_button = load_image("Elements/reset_button.png", (134, 75))
reset_rect = reset_button.get_rect(topleft=(884, 574))  # เดิม (744, 564) -> +100

show_button = load_image("Elements/show_button.png", (134, 75))
show_rect = show_button.get_rect(topleft=(1064, 574))     # เดิม (924, 564) -> +100

back_button = load_image("Elements/back_button.png", (134, 75))
back_rect = back_button.get_rect(topleft=(70, 40))         # เดิม (30, 30) -> +100

palette_bg = load_image("Elements/Color/painttray.png", (90, 234))
palette_pos = (698, 100)        # เดิม (558, 90) -> +100

# ----------------------------------------------------------------------------
# 3) จัดการ "สี" (color) และตำแหน่งไอคอนในพาเลตต์ โดยปรับ x เพิ่ม 100px
# ----------------------------------------------------------------------------
color_names = [
    "none", "grape", "bluberry", "mint", "vanilla", "milk",
    "carrot", "redvelvet", "strawberry", "charcole", "chocolate", "coffee"
]

color_icons = {}
for color in color_names:
    img = load_image(f"Elements/Color/{color}.png", (30, 30))
    if img:
        color_icons[color] = img

# คำนวณตำแหน่งของไอคอนสีในพาเลตต์ (2 คอลัมน์)
color_positions = []
for i, _ in enumerate(color_names):
    col = i % 2
    row = i // 2
    # เริ่มต้น x ใช้ palette_pos[0] ที่ปรับแล้ว
    x_pos = palette_pos[0] + 12 + (col * 36)
    y_pos = palette_pos[1] + 12 + (row * 36)
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

selected_type = {s: None for s in states}
selected_color = {s: None for s in states}
current_mode = "base"

# ----------------------------------------------------------------------------
# 5) โหลดไอคอนปุ่มด้านบนสำหรับเปลี่ยน sub-state พร้อมปรับตำแหน่ง x (+100)
# ----------------------------------------------------------------------------
mode_icons = {}
icon_positions = {}
start_x = 800  # เดิม 660 -> +100
gap_x = 75
for i, st in enumerate(states):
    icon_path = f"Elements/{st}_button.png"
    icon_img = load_image(icon_path, (66, 66))
    mode_icons[st] = icon_img
    icon_positions[st] = (start_x + i * gap_x, 15)

# ----------------------------------------------------------------------------
# 6) ตำแหน่งของชั้นวาง (shelf) สำหรับวางภาพตัวเลือก type (แก้ x +100)
# ----------------------------------------------------------------------------
shelf_positions = [
    (814, 106), (944, 106), (1074, 106),
    (814, 247), (944, 247), (1074, 247),
    (814, 422), (904, 422), (1074, 422)
]

# ----------------------------------------------------------------------------
# 7) ฟังก์ชันสำหรับโหลด "ภาพเค้กจริง" ที่ผู้ใช้เลือก
# ----------------------------------------------------------------------------
def load_cake_part(state_name, cake_type, color):
    if not cake_type:
        return None
    if not color:
        color = "grape"
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
selected_color_global = None
show_cakes = True
font = pygame.font.Font(None, 50)

running = True

# ----------------------------------------------------------------------------
# 9) ฟังก์ชันวาดฉาก (draw_scene)
# ----------------------------------------------------------------------------
def draw_scene():
    # หากต้องการขยับ background ไปด้านขวา 100px ให้ blit ที่ (100, 0)
    screen.blit(background, (0, 0))
    screen.blit(palette_bg, palette_pos)

    if shelve:
        screen.blit(shelve, shelve_pos)

    if back_button:
        screen.blit(back_button, back_rect.topleft)

    for st in states:
        icon_img = mode_icons[st]
        if icon_img:
            screen.blit(icon_img, icon_positions[st])

    for i, color in enumerate(color_names):
        if color in color_icons:
            screen.blit(color_icons[color], color_positions[i])

    text = font.render("RealOrCake - Decoration State with Sub-States", True, (0, 0, 0))
    # ปรับตำแหน่งข้อความให้ขยับไปด้านขวา 100px (เพิ่ม 100 ในแกน x)
    screen.blit(text, ((WIDTH // 2 - text.get_width() // 2), 70))

    if show_cakes:
        types_for_this_state = state_options[current_mode]
        for i, cake_type in enumerate(types_for_this_state):
            if i < len(shelf_positions):
                thumb_path = f"Elements/thumbnail/{current_mode}_{cake_type}.png"
                thumb_img = load_image(thumb_path, (156, 156))
                if thumb_img:
                    screen.blit(thumb_img, shelf_positions[i])
        if reset_button:
            screen.blit(reset_button, reset_rect.topleft)
        if show_button:
            screen.blit(show_button, show_rect.topleft)

    cake_draw_order = ["base", "topcream", "lowercream", "middlecream", "behindcream", "topping"]
    # ปรับตำแหน่งของเค้กให้ x +100 (จาก 60 เป็น 160)
    final_cake_x, final_cake_y = 170, 189

    for st in cake_draw_order:
        t = selected_type[st]
        c = selected_color[st]
        part_img = load_cake_part(st, t, c)
        if part_img:
            part_img = pygame.transform.scale(part_img, (509, 509))
            screen.blit(part_img, (final_cake_x, final_cake_y))

# ----------------------------------------------------------------------------
# 10) ฟังก์ชันจัดการเหตุการณ์ (handle_events)
# ----------------------------------------------------------------------------
def handle_events():
    global running, show_cakes, current_mode, selected_color_global

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

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

            if reset_rect and reset_rect.collidepoint(x, y):
                for st in states:
                    selected_type[st] = None
                    selected_color[st] = None
                selected_color_global = None
                print("Reset selection")

            if show_rect and show_rect.collidepoint(x, y):
                global show_cakes
                show_cakes = not show_cakes
                print(f"Show cakes: {show_cakes}")

            if back_rect and back_rect.collidepoint(x, y):
                print("Back to Home")

            for i, pos in enumerate(color_positions):
                color_rect = pygame.Rect(pos[0], pos[1], 30, 30)
                if color_rect.collidepoint(x, y):
                    selected_color_global = color_names[i]
                    selected_color[current_mode] = selected_color_global
                    print(f"Selected color for [{current_mode}]: {selected_color_global}")

            if show_cakes:
                types_for_this_state = state_options[current_mode]
                for i, cake_type in enumerate(types_for_this_state):
                    if i < len(shelf_positions):
                        rect = pygame.Rect(shelf_positions[i], (156, 156))
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
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
