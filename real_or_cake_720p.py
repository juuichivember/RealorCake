import pygame
import os

pygame.init()

# กำหนดความละเอียดหน้าจอใหม่ และคำนวณ SCALE (1280/1920 = 2/3)
NEW_WIDTH, NEW_HEIGHT = 1280, 720
OLD_WIDTH, OLD_HEIGHT = 1920, 1080
SCALE = NEW_WIDTH / OLD_WIDTH  # ประมาณ 0.6667

screen = pygame.display.set_mode((NEW_WIDTH, NEW_HEIGHT))
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
# 2) โหลดภาพพื้นหลัง / ปุ่ม / พาเลตต์สี โดยปรับขนาดและตำแหน่งตาม SCALE
# ----------------------------------------------------------------------------
background = load_image("Elements/shop_background.png", (NEW_WIDTH, NEW_HEIGHT))

shelve = load_image("Elements/shelve.png", (int(775 * SCALE), int(806 * SCALE)))
shelve_pos = (int(1083 * SCALE), int(138 * SCALE))

reset_button = load_image("Elements/reset_button.png", (int(212 * SCALE), int(124 * SCALE)))
reset_rect = reset_button.get_rect(topleft=(int(1240 * SCALE), int(940 * SCALE))) if reset_button else None

show_button = load_image("Elements/show_button.png", (int(212 * SCALE), int(124 * SCALE)))
show_rect = show_button.get_rect(topleft=(int(1540 * SCALE), int(940 * SCALE))) if show_button else None

back_button = load_image("Elements/back_button.png", (int(222 * SCALE), int(122 * SCALE)))
back_rect = back_button.get_rect(topleft=(int(50 * SCALE), int(50 * SCALE))) if back_button else None

palette_bg = load_image("Elements/Color/painttray.png", (int(150 * SCALE), int(390 * SCALE)))
palette_pos = (int(930 * SCALE), int(150 * SCALE))

# ----------------------------------------------------------------------------
# 3) จัดการ "สี" (color) และตำแหน่งไอคอนในพาเลตต์
# ----------------------------------------------------------------------------
color_names = [
    "none", "grape", "bluberry", "mint", "vanilla", "milk",
    "carrot", "redvelvet", "strawberry", "charcole", "chocolate", "coffee"
]

color_icons = {}
for color in color_names:
    img = load_image(f"Elements/Color/{color}.png", (int(50 * SCALE), int(50 * SCALE)))
    if img:
        color_icons[color] = img

color_positions = []
for i, _ in enumerate(color_names):
    col = i % 2
    row = i // 2
    # ปรับ offset ด้วย SCALE
    x_pos = palette_pos[0] + int(20 * SCALE) + (col * int(60 * SCALE))
    y_pos = palette_pos[1] + int(20 * SCALE) + (row * int(60 * SCALE))
    color_positions.append((x_pos, y_pos))

# ----------------------------------------------------------------------------
# 4) กำหนด sub-states และข้อมูลตัวเลือก
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
# 5) โหลดไอคอนปุ่มด้านบนสำหรับเปลี่ยน sub-state และกำหนดตำแหน่ง
# ----------------------------------------------------------------------------
mode_icons = {}
icon_positions = {}
start_x = int(1100 * SCALE)  # ตำแหน่ง x เริ่มต้นปรับด้วย SCALE
gap_x = int(125 * SCALE)     # ระยะห่างระหว่างปุ่ม
for i, st in enumerate(states):
    icon_path = f"Elements/{st}_button.png"
    # ปรับขนาดไอคอนด้วย SCALE
    icon_img = load_image(icon_path, (int(110 * SCALE), int(110 * SCALE)))
    mode_icons[st] = icon_img
    icon_positions[st] = (start_x + i * gap_x, int(25 * SCALE))

# ----------------------------------------------------------------------------
# 6) กำหนดตำแหน่งชั้นวาง (shelf) สำหรับวางตัวเลือก type
# ----------------------------------------------------------------------------
shelf_positions = [
    (int(1122 * SCALE), int(160 * SCALE)), (int(1339 * SCALE), int(160 * SCALE)), (int(1556 * SCALE), int(160 * SCALE)),
    (int(1122 * SCALE), int(394 * SCALE)), (int(1339 * SCALE), int(394 * SCALE)), (int(1556 * SCALE), int(394 * SCALE)),
    (int(1122 * SCALE), int(636 * SCALE)), (int(1339 * SCALE), int(636 * SCALE)), (int(1556 * SCALE), int(636 * SCALE))
]

# ----------------------------------------------------------------------------
# 7) ฟังก์ชันโหลดภาพเค้กส่วนต่าง ๆ
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
font = pygame.font.Font(None, int(50 * SCALE))

running = True

# ----------------------------------------------------------------------------
# 9) ฟังก์ชันวาดฉาก (draw_scene)
# ----------------------------------------------------------------------------
def draw_scene():
    screen.blit(background, (0, 0))
    screen.blit(palette_bg, palette_pos)

    if shelve:
        screen.blit(shelve, shelve_pos)

    if back_button:
        screen.blit(back_button, back_rect.topleft)

    # วาดไอคอนเปลี่ยน sub-state
    for st in states:
        icon_img = mode_icons[st]
        if icon_img:
            screen.blit(icon_img, icon_positions[st])

    # วาดพาเลตต์สี
    for i, color in enumerate(color_names):
        if color in color_icons:
            screen.blit(color_icons[color], color_positions[i])

    # วาดหัวข้อ
    text = font.render("RealOrCake - Decoration State with Sub-States", True, (0, 0, 0))
    screen.blit(text, (NEW_WIDTH // 2 - text.get_width() // 2, int(100 * SCALE)))

    # วาดตัวเลือกบนชั้นวาง (เฉพาะ sub-state ปัจจุบัน)
    if show_cakes:
        types_for_this_state = state_options[current_mode]
        for i, cake_type in enumerate(types_for_this_state):
            if i < len(shelf_positions):
                thumb_path = f"Elements/thumbnail/{current_mode}_{cake_type}.png"
                thumb_img = load_image(thumb_path, (int(260 * SCALE), int(260 * SCALE)))
                if thumb_img:
                    screen.blit(thumb_img, shelf_positions[i])
        if reset_button:
            screen.blit(reset_button, reset_rect.topleft)
        if show_button:
            screen.blit(show_button, show_rect.topleft)

    # วาดเค้ก (รวมทุก sub-state)
    cake_draw_order = ["base", "topcream", "lowercream", "middlecream", "behindcream", "topping"]
    final_cake_x, final_cake_y = int(100 * SCALE), int(248 * SCALE)

    for st in cake_draw_order:
        t = selected_type[st]
        c = selected_color[st]
        part_img = load_cake_part(st, t, c)
        if part_img:
            part_img = pygame.transform.scale(part_img, (int(847 * SCALE), int(847 * SCALE)))
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

            # ตรวจสอบการคลิกที่ไอคอนเปลี่ยน sub-state
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

            # ตรวจสอบปุ่ม Reset
            if reset_rect and reset_rect.collidepoint(x, y):
                for st in states:
                    selected_type[st] = None
                    selected_color[st] = None
                selected_color_global = None
                print("Reset selection")

            # ตรวจสอบปุ่ม Show
            if show_rect and show_rect.collidepoint(x, y):
                show_cakes = not show_cakes
                print(f"Show cakes: {show_cakes}")

            # ตรวจสอบปุ่ม Back
            if back_rect and back_rect.collidepoint(x, y):
                print("Back to Home")
                # เพิ่มการทำงานกลับหน้าหลักหรือออกจากเกม

            # ตรวจสอบการคลิกในพาเลตต์สี
            for i, pos in enumerate(color_positions):
                color_rect = pygame.Rect(pos[0], pos[1], int(50 * SCALE), int(50 * SCALE))
                if color_rect.collidepoint(x, y):
                    selected_color_global = color_names[i]
                    selected_color[current_mode] = selected_color_global
                    print(f"Selected color for [{current_mode}]: {selected_color_global}")

            # ตรวจสอบการคลิกบนชั้นวางเพื่อเลือก type
            if show_cakes:
                types_for_this_state = state_options[current_mode]
                for i, cake_type in enumerate(types_for_this_state):
                    if i < len(shelf_positions):
                        rect = pygame.Rect(shelf_positions[i], (int(260 * SCALE), int(260 * SCALE)))
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
