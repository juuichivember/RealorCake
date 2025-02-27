from PIL import Image

def crop_transparent_area(image_path, output_path):
    # เปิดภาพ
    img = Image.open(image_path).convert("RGBA")
    pixdata = img.getdata()

    # หา bounding box ของพิกเซลที่ไม่โปร่งใส
    left, top, right, bottom = img.width, img.height, 0, 0
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixdata[y * img.width + x]
            if a > 0:  # พิกเซลที่ไม่โปร่งใส
                left = min(left, x)
                top = min(top, y)
                right = max(right, x)
                bottom = max(bottom, y)
    
    # ตรวจสอบว่าเจอขอบหรือไม่
    if left < right and top < bottom:
        cropped_img = img.crop((left, top, right + 1, bottom + 1))
        cropped_img.save(output_path)
        print(f"Cropped image saved as: {output_path}")
    else:
        print("No non-transparent pixels found.")

# ใช้งาน
files = []
for i in range(89, 97):
    file = f'[UI04] Random Page/IMG_72{i}.png'
    files.append(file)
new_names = ['t_eight', 't_seven', 't_six', 't_five', 't_four', 't_three', 't_two', 't_one']
for i in range(len(files)):
    crop_transparent_area(files[i], new_names[i] + '.png')
