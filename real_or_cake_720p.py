import pygame
import os

# กำหนดค่าพื้นฐาน
pygame.init()
WIDTH, HEIGHT = 1280, 720  # ขนาดหน้าจอที่ปรับใหม่
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RealOrCake - Select Your Cake Base")

# โหลดภาพพื้นหลังและปรับขนาดให้พอดีกับหน้าจอ
background = pygame.image.load("Elements/shop_background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# คำนวณสเกลแฟกเตอร์จาก Full HD (1920,1080) เป็น (1280,720)
scale_factor = 1280 / 1920  # เท่ากับประมาณ 0.6667

# โหลดภาพชั้นวางเค้กและปรับขนาดและตำแหน่ง
shelve = pygame.image.load("Elements/shelve.png")
shelve_width = int(762 * scale_factor)
shelve_height = int(801 * scale_factor)
shelve = pygame.transform.scale(shelve, (shelve_width, shelve_height))
shelve_x = int(1121 * scale_factor)
shelve_y = int(-292 * scale_factor)  # เริ่มต้นอยู่นอกจอด้านบน
shelve_target_y = int(108 * scale_factor)  # จุดที่ชั้นวางต้องหยุด
shelve_speed = int(15 * scale_factor)  # ความเร็วในการเลื่อนลง

# โหลดภาพโต๊ะและปรับขนาดและตำแหน่ง
table = pygame.image.load("Elements/table.png")
table_width = int(1303 * scale_factor)
table_height = int(814 * scale_factor)
table = pygame.transform.scale(table, (table_width, table_height))
table_x = int(-533 * scale_factor)
table_y = int(796 * scale_factor)

# โหลดปุ่มรีเซ็ตและปุ่มเสร็จสิ้น พร้อมปรับขนาดและตำแหน่ง
reset_button = pygame.image.load("Elements/reset_button.png")
reset_button = pygame.transform.scale(reset_button, (int(180 * scale_factor), int(60 * scale_factor)))
reset_button_pos = (int(1240 * scale_factor), int(950 * scale_factor))

finish_button = pygame.image.load("Elements/finish_button.png")
finish_button = pygame.transform.scale(finish_button, (int(180 * scale_factor), int(60 * scale_factor)))
finish_button_pos = (int(1540 * scale_factor), int(950 * scale_factor))

# กำหนดสี
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ฟังก์ชันโหลดรูปภาพเค้ก
def load_cake_image(cake_type):
    path = f"Elements/layer7_base_1/{cake_type}.png"
    if os.path.exists(path):
        return pygame.image.load(path)
    return None

# รายการชนิดเค้ก
cake_types = [
    "vanilla", "chocolate", "strawberry",
    "charcole", "blueberry", "grape",
    "carrot", "milk", "mint"
]

# โหลดภาพเค้กและปรับขนาด
cake_options = {cake: load_cake_image(cake) for cake in cake_types}

# ตำแหน่งเค้ก (ปรับสเกล)
final_positions = {
    "vanilla": (int(1155 * scale_factor), int(209 * scale_factor)),
    "chocolate": (int(1377 * scale_factor), int(209 * scale_factor)),
    "strawberry": (int(1595 * scale_factor), int(209 * scale_factor)),
    "charcole": (int(1155 * scale_factor), int(440 * scale_factor)),
    "blueberry": (int(1377 * scale_factor), int(440 * scale_factor)),
    "grape": (int(1595 * scale_factor), int(440 * scale_factor)),
    "carrot": (int(1155 * scale_factor), int(666 * scale_factor)),
    "milk": (int(1377 * scale_factor), int(666 * scale_factor)),
    "mint": (int(1595 * scale_factor), int(666 * scale_factor))
}

for key in cake_options:
    if cake_options[key]:
        # ปรับขนาดภาพเค้กให้เหมาะสมกับสเกล
        cake_options[key] = pygame.transform.scale(cake_options[key], (int(260 * scale_factor), int(260 * scale_factor)))

# ตัวแปรเก็บฐานเค้กที่ถูกเลือก
selected_cake = None

# กำหนดฟอนต์ (ปรับขนาดตามสเกล)
font = pygame.font.Font(None, int(50 * scale_factor))

# ตัวแปรควบคุมการแสดงเค้ก
show_cakes = False

# วนลูปเกม
running = True
while running:
    screen.blit(background, (0, 0))  # วาดพื้นหลัง

    # เคลื่อนชั้นวางและโต๊ะเข้ามาพร้อมกัน
    if shelve_y < shelve_target_y:
        shelve_y += shelve_speed
    if table_x < int(-533 * scale_factor + 200):  # เลื่อนโต๊ะเข้ามา
        table_x += shelve_speed
    else:
        show_cakes = True  # เมื่อชั้นวางถึงตำแหน่ง ให้แสดงเค้ก

    screen.blit(table, (table_x, table_y))
    screen.blit(shelve, (shelve_x, shelve_y))

    # แสดงข้อความตรงกลางด้านบน
    text = font.render("Select Your Cake Base", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, int(100 * scale_factor)))

    # แสดงฐานเค้กหลังจากชั้นวางถึงตำแหน่ง
    if show_cakes:
        for key, pos in final_positions.items():
            if cake_options[key]:
                screen.blit(cake_options[key], pos)
        screen.blit(reset_button, reset_button_pos)
        screen.blit(finish_button, finish_button_pos)

    # แสดงฐานเค้กที่ถูกเลือกถ้ามี
    if selected_cake:
        selected_cake_img = load_cake_image(selected_cake)
        if selected_cake_img:
            selected_cake_img = pygame.transform.scale(selected_cake_img, (int(847 * scale_factor), int(847 * scale_factor)))
            cake_x = int(100 * scale_factor)
            cake_y = int(248 * scale_factor)
            screen.blit(selected_cake_img, (cake_x, cake_y))

    # ตรวจจับเหตุการณ์
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN and show_cakes:
            x, y = event.pos
            # ตรวจจับการกดเลือกฐานเค้ก
            for key, pos in final_positions.items():
                cake_rect = pygame.Rect(pos[0], pos[1], int(260 * scale_factor), int(260 * scale_factor))
                if cake_rect.collidepoint(x, y):
                    selected_cake = key
            # ตรวจจับการกดปุ่ม Reset
            reset_rect = pygame.Rect(reset_button_pos[0], reset_button_pos[1], int(180 * scale_factor), int(60 * scale_factor))
            if reset_rect.collidepoint(x, y):
                selected_cake = None
            # ตรวจจับการกดปุ่ม Finish
            finish_rect = pygame.Rect(finish_button_pos[0], finish_button_pos[1], int(180 * scale_factor), int(60 * scale_factor))
            if finish_rect.collidepoint(x, y):
                print("Cake selection finished!")

    pygame.display.flip()

pygame.quit()
