import pygame
import os

pygame.init()

# ความละเอียดอ้างอิง (Base Resolution)
BASE_WIDTH, BASE_HEIGHT = 1280, 720
window_width, window_height = BASE_WIDTH, BASE_HEIGHT

# สร้างหน้าต่างแบบ resizable
screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
pygame.display.set_caption("RealOrCake - Decoration State with Sub-States")

def load_image(path, size=None):
    """โหลดภาพจาก path และปรับขนาดตาม size (ถ้ามี)"""
    if os.path.exists(path):
        try:
            image = pygame.image.load(path).convert_alpha()
            if size:
                image = pygame.transform.scale(image, size)
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")
    else:
        print(f"File not found: {path}")
    return pygame.Surface((1, 1), pygame.SRCALPHA)

# ตัวแปร global สำหรับ layout
background = None

# พาเลต (palette)
palette_bg = None
palette_pos = (0, 0)

# ชั้นวาง (shelve)
shelve = None
shelve_pos = (0, 0)

# ปุ่ม reset/show/back
reset_button = None
reset_rect = None
finish_button = None
show_rect = None
back_button = None
back_rect = None

# ไอคอนสีในพาเลต
color_icons = {}
color_positions = []

# ไอคอนเปลี่ยน sub-state
mode_icons = {}
icon_positions = {}

# ตำแหน่ง thumbnail บนชั้นวาง
shelf_positions = []

font = None

# รายการสี
color_names = [
    "none", "grape", "bluberry", "mint", "vanilla", "milk",
    "carrot", "redvelvet", "strawberry", "charcole", "chocolate", "coffee"
]

# รายการ sub-state
states = ["base", "behindcream", "lowercream", "middlecream", "topcream", "topping"]

def update_layout():
    """อัปเดตตำแหน่งและขนาดขององค์ประกอบต่าง ๆ เมื่อหน้าจอเปลี่ยนขนาด"""
    global background
    global palette_bg, palette_pos
    global shelve, shelve_pos
    global reset_button, reset_rect
    global finish_button, show_rect
    global back_button, back_rect
    global color_icons, color_positions
    global mode_icons, icon_positions
    global shelf_positions
    global font

    scale = window_height / BASE_HEIGHT  # คำนวณสเกลจากความสูงเป็นหลัก

    # โหลดพื้นหลังให้เต็มหน้าจอ
    background = load_image("Elements/shop_background_720.png", (window_width, window_height))

    # -------------------------------
    # โหลดภาพพาเลตและชั้นวาง
    # -------------------------------
    palette_bg = load_image("Elements/Color/painttray.png", (int(90 * scale), int(234 * scale)))
    shelve = load_image("Elements/shelve.png", (int(465 * scale), int(484 * scale)))

    palette_w = palette_bg.get_width() if palette_bg else 0
    palette_h = palette_bg.get_height() if palette_bg else 0
    shelve_w = shelve.get_width() if shelve else 0
    shelve_h = shelve.get_height() if shelve else 0

    # -------------------------------
    # กำหนด "กลุ่ม" พาเลต + ชั้นวาง ชิดขวา
    # -------------------------------
    margin_right = int(20 * scale)   # ระยะห่างจากขอบขวา
    spacing = int(20 * scale)        # ระยะห่างระหว่าง palette กับ shelve
    group_top = int(88 * scale)      # ตำแหน่ง Y เริ่มต้น (ตามดีไซน์เดิม)
    
    # ความกว้างทั้งหมด = ความกว้างพาเลต + spacing + ความกว้างชั้นวาง
    group_width = palette_w + spacing + shelve_w
    group_left = window_width - group_width - margin_right

    # palette ทางซ้าย, shelve ทางขวา
    palette_pos = (group_left, group_top)
    shelve_pos = (group_left + palette_w + spacing, group_top)

    # -------------------------------
    # ปุ่ม Reset, Show - วางด้านล่างของชั้นวาง (ชิดขวา)
    # -------------------------------
    reset_button = load_image("Elements/reset_button.png", (int(134 * scale), int(75 * scale)))
    finish_button = load_image("Elements/finish_button.png", (int(134 * scale), int(75 * scale)))

    if shelve:
        # เอา y ด้านล่างของ shelve + margin (เล็กน้อย)
        bottom_of_shelve = shelve_pos[1] + shelve_h
        margin_under_shelve = int(20 * scale)  # ระยะห่างใต้ชั้นวาง
        btn_y = bottom_of_shelve + margin_under_shelve
    else:
        # ถ้า shelve ไม่มี ก็กำหนด fallback
        btn_y = int(window_height * 0.7)

    # จัดปุ่ม Show อยู่ขวาสุด, ปุ่ม Reset อยู่ถัดมาทางซ้าย
    if finish_button:
        show_w, show_h = finish_button.get_width(), finish_button.get_height()
        show_x = window_width - show_w - margin_right
        show_rect = finish_button.get_rect(topleft=(show_x, btn_y))
    else:
        show_rect = None

    if reset_button and show_rect:
        reset_w, reset_h = reset_button.get_width(), reset_button.get_height()
        spacing_btn = int(10 * scale)  # ระยะห่างระหว่างปุ่ม
        reset_x = show_rect.left - reset_w - spacing_btn
        reset_rect = reset_button.get_rect(topleft=(reset_x, btn_y))
    else:
        reset_rect = None

    # -------------------------------
    # ปุ่ม Back - ซ้ายบนตามเดิม
    # -------------------------------
    back_button = load_image("Elements/back_button.png", (int(134 * scale), int(75 * scale)))
    if back_button:
        back_rect = back_button.get_rect(topleft=(int(70 * scale), int(40 * scale)))
    else:
        back_rect = None

    # -------------------------------
    # ไอคอนสีในพาเลต
    # -------------------------------
    new_color_icons = {}
    for color in color_names:
        new_color_icons[color] = load_image(f"Elements/Color/{color}.png", (int(30 * scale), int(30 * scale)))
    color_icons.clear()
    color_icons.update(new_color_icons)

    color_positions.clear()
    for i, color in enumerate(color_names):
        col = i % 2
        row = i // 2
        x_pos = palette_pos[0] + int(12 * scale) + col * int(36 * scale)
        y_pos = palette_pos[1] + int(12 * scale) + row * int(36 * scale)
        color_positions.append((x_pos, y_pos))

    # -------------------------------
    # ไอคอนเปลี่ยน sub-state - ชิดขวาด้านบน
    # (เรียงจากซ้ายไปขวาหรือขวาไปซ้ายได้ตามชอบ; ตัวอย่างนี้เรียงจากซ้าย→ขวา)
    # -------------------------------
    icon_size = int(66 * scale)
    gap_x = int(10 * scale)
    # นับจำนวน states
    num_states = len(states)
    total_icons_width = num_states * icon_size + (num_states - 1) * gap_x

    # วางแถวนี้ชิดขวา: row_left = window_width - total_icons_width - margin_right
    row_left = window_width - total_icons_width - margin_right
    row_top = int(15 * scale)

    new_mode_icons = {}
    new_icon_positions = {}
    current_x = row_left

    for st in states:
        icon_img = load_image(f"Elements/{st}_button.png", (icon_size, icon_size))
        new_mode_icons[st] = icon_img
        new_icon_positions[st] = (current_x, row_top)
        current_x += (icon_size + gap_x)  # ถัดไปทางขวา

    mode_icons.clear()
    mode_icons.update(new_mode_icons)
    icon_positions.clear()
    icon_positions.update(new_icon_positions)

    # -------------------------------
    # ตำแหน่ง thumbnail บนชั้นวาง
    # เดิม (814,106) ... แต่ตอนนี้เราจะอิงจาก shelve_pos + offset
    # -------------------------------
    shelf_positions.clear()
    # กำหนด offset ภายใน shelve (ตามดีไซน์เดิม)
    # เช่น (24,18), (154,18) ... 
    shelf_offsets = [
        (24, 18), (154, 18), (284, 18),
        (24, 159), (154, 159), (284, 159),
        (24, 304), (154, 304), (284, 304)
    ]
    for off_x, off_y in shelf_offsets:
        shelf_positions.append((
            shelve_pos[0] + int(off_x * scale),
            shelve_pos[1] + int(off_y * scale)
        ))

    # -------------------------------
    # ฟอนต์
    # -------------------------------
    font_size = int(50 * scale)
    if font_size < 10:
        font_size = 10
    font = pygame.font.Font(None, font_size)

# เรียก update_layout ครั้งแรก
update_layout()

# ----------------------------------------------------------------------------
# 2) กำหนดข้อมูลตัวเลือก sub-state และตัวแปรสำหรับเก็บการเลือก
# ----------------------------------------------------------------------------
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
selected_color_global = None
show_cakes = True

def load_cake_part(state_name, cake_type, color):
    """โหลดภาพเค้ก (part) ตาม state, type, color"""
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

def draw_scene():
    screen.blit(background, (0, 0))

    # พาเลต
    if palette_bg:
        screen.blit(palette_bg, palette_pos)

    # ชั้นวาง
    if shelve:
        screen.blit(shelve, shelve_pos)

    # ปุ่ม Back (ซ้ายบน)
    if back_button and back_rect:
        screen.blit(back_button, back_rect.topleft)

    # ไอคอนเปลี่ยน sub-state
    for st in states:
        icon_img = mode_icons.get(st)
        if icon_img:
            screen.blit(icon_img, icon_positions[st])

    # ไอคอนสี
    for i, color in enumerate(color_names):
        if color in color_icons:
            screen.blit(color_icons[color], color_positions[i])

    # ข้อความหัวข้อ
    scale = window_height / BASE_HEIGHT
    text = font.render("RealOrCake - Decoration State with Sub-States", True, (0, 0, 0))
    screen.blit(text, (window_width // 2 - text.get_width() // 2, int(70 * scale)))

    # ตัวเลือกบนชั้นวาง
    if show_cakes:
        types_for_this_state = state_options[current_mode]
        for i, cake_type in enumerate(types_for_this_state):
            if i < len(shelf_positions):
                thumb_path = f"Elements/thumbnail/{current_mode}_{cake_type}.png"
                thumb_img = load_image(thumb_path, (int(156 * scale), int(156 * scale)))
                if thumb_img:
                    screen.blit(thumb_img, shelf_positions[i])

        # ปุ่ม Reset, Show
        if reset_button and reset_rect:
            screen.blit(reset_button, reset_rect.topleft)
        if finish_button and show_rect:
            screen.blit(finish_button, show_rect.topleft)

    # วาดเค้ก
    cake_draw_order = ["base", "topcream", "lowercream", "middlecream", "behindcream", "topping"]
    final_cake_x, final_cake_y = int(170 * scale), int(189 * scale)

    for st in cake_draw_order:
        t = selected_type[st]
        c = selected_color[st]
        part_img = load_cake_part(st, t, c)
        if part_img:
            part_img = pygame.transform.scale(part_img, (int(509 * scale), int(509 * scale)))
            screen.blit(part_img, (final_cake_x, final_cake_y))

def handle_events():
    global running, current_mode, selected_color_global
    global window_width, window_height, screen, show_cakes

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            # ปรับขนาดหน้าต่าง
            window_width, window_height = event.size
            screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
            update_layout()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            # ไอคอนเปลี่ยน sub-state
            for st in states:
                icon_img = mode_icons.get(st)
                if icon_img:
                    rect_icon = pygame.Rect(
                        icon_positions[st][0],
                        icon_positions[st][1],
                        icon_img.get_width(),
                        icon_img.get_height()
                    )
                    if rect_icon.collidepoint(x, y):
                        current_mode = st
                        print(f"Switched to sub-state: {current_mode}")
                        break

            # ปุ่ม Reset
            if reset_rect and reset_rect.collidepoint(x, y):
                for st in states:
                    selected_type[st] = None
                    selected_color[st] = None
                selected_color_global = None
                print("Reset selection")

            # ปุ่ม Show
            if show_rect and show_rect.collidepoint(x, y):
                show_cakes = not show_cakes
                print(f"Show cakes: {show_cakes}")

            # ปุ่ม Back
            if back_rect and back_rect.collidepoint(x, y):
                print("Back to Home")

            # ไอคอนสีในพาเลต
            scale = window_height / BASE_HEIGHT
            icon_size = int(30 * scale)
            for i, pos in enumerate(color_positions):
                rect_color = pygame.Rect(pos[0], pos[1], icon_size, icon_size)
                if rect_color.collidepoint(x, y):
                    selected_color_global = color_names[i]
                    selected_color[current_mode] = selected_color_global
                    print(f"Selected color for [{current_mode}]: {selected_color_global}")

            # Thumbnail บนชั้นวาง
            if show_cakes:
                thumb_size = int(156 * scale)
                types_for_this_state = state_options[current_mode]
                for i, cake_type in enumerate(types_for_this_state):
                    if i < len(shelf_positions):
                        rect_thumb = pygame.Rect(
                            shelf_positions[i][0],
                            shelf_positions[i][1],
                            thumb_size,
                            thumb_size
                        )
                        if rect_thumb.collidepoint(x, y):
                            selected_type[current_mode] = cake_type
                            print(f"Selected type for [{current_mode}]: {cake_type}")

running = True

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
