import pygame
import os

# เริ่มต้น Pygame และกำหนดขนาดหน้าจอ
pygame.init()
WIDTH, HEIGHT = 1920, 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("RealOrCake - Select Your Cake Base")

# ฟังก์ชันโหลดภาพ พร้อมปรับขนาด (ถ้ามี) และแจ้ง error หากไม่พบไฟล์
def load_image(path, scale=None):
    if os.path.exists(path):
        try:
            image = pygame.image.load(path)
            if scale:
                image = pygame.transform.scale(image, scale)
            return image
        except Exception as e:
            print(f"Error loading image {path}: {e}")
    else:
        print(f"File not found: {path}")
    return None

# โหลดภาพพื้นหลัง
background = load_image("Elements/shop_background.png", (WIDTH, HEIGHT))

# โหลดภาพชั้นวางเค้กและปุ่มต่าง ๆ
shelve = load_image("Elements/shelve.png", (775, 806))
shelve_pos = (1083, 138)

reset_button = load_image("Elements/reset_button.png", (212, 124))
reset_rect = reset_button.get_rect(topleft=(1240, 940)) if reset_button else None

show_button = load_image("Elements/show_button.png", (212, 124))
show_rect = show_button.get_rect(topleft=(1540, 940)) if show_button else None

back_button = load_image("Elements/back_button.png", (222, 122))
back_rect = back_button.get_rect(topleft=(50, 50)) if back_button else None

# โหลดถาดสี (Palette)
palette_bg = load_image("Elements/Color/painttray.png", (150, 390))
palette_pos = (930, 150)

# รายชื่อสีในพาเลตต์
color_names = ["none", "grape", "bluberry", "mint", "vanilla", "milk",
               "carrot", "redvelvet", "strawberry", "charcole", "chocolate", "coffee"]

# โหลดไอคอนสีและปรับขนาด
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

selected_color = None

# กำหนดค่าสีพื้นฐาน
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ฟังก์ชันโหลดภาพเค้ก
def load_cake_image(cake_type):
    path = f"Elements/layer7_base_1/layer7_base_1{cake_type}.png"
    return load_image(path)

# รายการประเภทของเค้ก
cake_types = [
    "vanilla", "chocolate", "strawberry",
    "charcole", "blueberry", "grape",
    "carrot", "milk", "mint"
]

# โหลดภาพเค้กและปรับขนาดให้เหมาะสมกับการแสดงเป็นตัวเลือก
cake_options = {}
final_positions = {
    "vanilla": (1122, 160), "chocolate": (1339, 160), "strawberry": (1556, 160),
    "charcole": (1122, 394), "blueberry": (1339, 394), "grape": (1556, 394),
    "carrot": (1122, 636), "milk": (1339, 636), "mint": (1556, 636)
}

for cake in cake_types:
    img = load_cake_image(cake)
    if img:
        cake_options[cake] = pygame.transform.scale(img, (260, 260))
    else:
        cake_options[cake] = None

selected_cake = None

# กำหนดฟอนต์
font = pygame.font.Font(None, 50)

# ตัวแปรควบคุมการแสดงฐานเค้กในหน้าจอ
show_cakes = True

# ฟังก์ชันวาดฉากทั้งหมด
def draw_scene():
    screen.blit(background, (0, 0))
    screen.blit(palette_bg, palette_pos)
    
    # วาดชั้นวางและปุ่มกลับ
    if shelve:
        screen.blit(shelve, shelve_pos)
    if back_button:
        screen.blit(back_button, (50, 50))
    
    # วาดไอคอนสีในพาเลตต์
    for i, color in enumerate(color_names):
        if color in color_icons:
            screen.blit(color_icons[color], color_positions[i])
    
    # วาดข้อความหัวข้อตรงกลางด้านบน
    text = font.render("Select Your Cake Base", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))
    
    # วาดตัวเลือกฐานเค้กและปุ่ม reset, show
    if show_cakes:
        for cake, pos in final_positions.items():
            if cake_options.get(cake):
                screen.blit(cake_options[cake], pos)
        if reset_button:
            screen.blit(reset_button, (1240, 940))
        if show_button:
            screen.blit(show_button, (1540, 940))
    
    # วาดฐานเค้กที่ถูกเลือกในส่วนแสดงผลใหญ่ (ถ้ามี)
    if selected_cake:
        img = load_cake_image(selected_cake)
        if img:
            img = pygame.transform.scale(img, (847, 847))
            screen.blit(img, (100, 248))

# ฟังก์ชันจัดการเหตุการณ์ (Event Handling)
def handle_events():
    global running, selected_color, selected_cake, show_cakes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            # ตรวจสอบการคลิกเลือกสีในพาเลตต์
            for i, pos in enumerate(color_positions):
                rect = pygame.Rect(pos[0], pos[1], 50, 50)
                if rect.collidepoint(x, y):
                    selected_color = color_names[i]
                    print(f"Selected color: {selected_color}")
            # ตรวจสอบการคลิกที่ปุ่ม reset
            if reset_rect and reset_rect.collidepoint(x, y):
                selected_color = None
                selected_cake = None
                print("Reset selection")
            # ตรวจสอบการคลิกที่ปุ่ม show เพื่อสลับการแสดงผลของเค้ก
            if show_rect and show_rect.collidepoint(x, y):
                show_cakes = not show_cakes
                print(f"Show cakes: {show_cakes}")
            # ตรวจสอบการคลิกที่ปุ่ม back
            if back_rect and back_rect.collidepoint(x, y):
                print("Back to Home")
                # เพิ่มการทำงานกลับหน้าหลักหรือออกจากเกมตามที่ต้องการ

# ฟังก์ชันหลักของเกม
def main():
    global running
    running = True
    clock = pygame.time.Clock()
    
    while running:
        handle_events()
        draw_scene()
        pygame.display.flip()
        clock.tick(60)  # จำกัดเฟรมเรตที่ 60 fps
        
    pygame.quit()

if __name__ == '__main__':
    main()
