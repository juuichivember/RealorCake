import pygame
import os

# กำหนดค่าพื้นฐาน
pygame.init()
WIDTH, HEIGHT = 1920, 1080  # ขนาดหน้าจอแบบ Full HD
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("RealOrCake - Select Your Cake Base")

# โหลดภาพพื้นหลัง
background = pygame.image.load("Elements/shop_background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# โหลดภาพชั้นวางเค้ก
shelve = pygame.image.load("Elements/shelve.png")
shelve = pygame.transform.scale(shelve, (762, 801))  # ปรับขนาดชั้นวาง
shelve_x, shelve_y = (1121, -292)  # เริ่มต้นอยู่นอกจอด้านบน
shelve_target_y = 108  # จุดที่ชั้นวางต้องหยุด
shelve_speed = 15  # ความเร็วในการเลื่อนลงมา

# โหลดภาพโต๊ะ
table = pygame.image.load("Elements/table.png")
table = pygame.transform.scale(table, (1303, 814))  # ปรับขนาดโต๊ะ
table_x, table_y = (-533, 796)  # เริ่มต้นอยู่นอกจอด้านซ้าย

# โหลดปุ่มรีเซ็ตและปุ่มเสร็จสิ้น
reset_button = pygame.image.load("Elements/reset_button.png")
reset_button = pygame.transform.scale(reset_button, (180, 60))
reset_button_pos = (1240, 950)

finish_button = pygame.image.load("Elements/finish_button.png")
finish_button = pygame.transform.scale(finish_button, (180, 60))
finish_button_pos = (1540, 950)

# กำหนดสี
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ฟังก์ชันโหลดรูปภาพจากโฟลเดอร์
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

# โหลดภาพเค้กจากโฟลเดอร์
cake_options = {cake: load_cake_image(cake) for cake in cake_types}

# ตำแหน่งของเค้ก
final_positions = {
    "vanilla": (1155, 209), "chocolate": (1377, 209), "strawberry": (1595, 209),
    "charcole": (1155, 440), "blueberry": (1377, 440), "grape": (1595, 440),
    "carrot": (1155, 666), "milk": (1377, 666), "mint": (1595, 666)
}

for key in cake_options:
    if cake_options[key]:  # ตรวจสอบว่ารูปโหลดสำเร็จ
        cake_options[key] = pygame.transform.scale(cake_options[key], (260, 260))

# ฐานเค้กที่ถูกเลือก
selected_cake = None

# ฟอนต์
font = pygame.font.Font(None, 50)

# ตัวแปรควบคุมการแสดงเค้ก
show_cakes = False

# วนลูปเกม
running = True
while running:
    screen.blit(background, (0, 0))  # วาดพื้นหลัง

    # เคลื่อนชั้นวางและโต๊ะเข้ามาพร้อมกัน
    if shelve_y < shelve_target_y:
        shelve_y += shelve_speed
    if table_x < -133:
        table_x += shelve_speed  # ใช้ความเร็วเดียวกับชั้นวาง
    else:
        show_cakes = True  # เมื่อชั้นวางถึงจุดสุดท้าย ให้แสดงเค้ก

    screen.blit(table, (table_x, table_y))
    screen.blit(shelve, (shelve_x, shelve_y))

    # แสดงข้อความ
    text = font.render("Select Your Cake Base", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))

    # แสดงฐานเค้กหลังจากชั้นวางถึงตำแหน่งสุดท้าย
    if show_cakes:
        for key, pos in final_positions.items():
            if cake_options[key]:
                screen.blit(cake_options[key], pos)
        screen.blit(reset_button, reset_button_pos)
        screen.blit(finish_button, finish_button_pos)

    # แสดงฐานเค้กที่ถูกเลือก
    if selected_cake:
        selected_cake_img = load_cake_image(selected_cake)
        if selected_cake_img:
            selected_cake_img = pygame.transform.scale(selected_cake_img, (847, 847))
            cake_x = 100
            cake_y = 248
            screen.blit(selected_cake_img, (cake_x, cake_y))

    # ตรวจจับเหตุการณ์
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # กด ESC เพื่อออกจากเกม
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN and show_cakes:
            x, y = event.pos
            # ตรวจจับการกดเลือกเค้ก
            for key, pos in final_positions.items():
                cake_rect = pygame.Rect(pos[0], pos[1], 260, 260)
                if cake_rect.collidepoint(x, y):
                    selected_cake = key  # กำหนดฐานเค้กที่เลือก
            
            # ตรวจจับการกดปุ่ม Reset
            reset_rect = pygame.Rect(reset_button_pos[0], reset_button_pos[1], 200, 100)
            if reset_rect.collidepoint(x, y):
                selected_cake = None
            
            # ตรวจจับการกดปุ่ม Finish
            finish_rect = pygame.Rect(finish_button_pos[0], finish_button_pos[1], 200, 100)
            if finish_rect.collidepoint(x, y):
                print("Cake selection finished!")  # สามารถเพิ่มการบันทึกผลหรือเปลี่ยนไปหน้าถัดไป

    pygame.display.flip()  # อัปเดตหน้าจอ

pygame.quit()
