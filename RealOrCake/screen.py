import math

ratios_dict = {"1080p": (1960, 1080),
                "720p": (1280, 720),
                "480p": (854, 480)}

def set_screen(screen_size):
    return ratios_dict['720p']

    # Version can change according to desktop size but ไม่ใช้เราไม่รู้ว่าจะเปลี่ยนตำแหน่งปุ่มให้ปรับตามขนาดจอยังไง
"""     screen_area = math.prod(screen_size)
    if screen_area >= math.prod(ratios_dict["1080p"]):
        return ratios_dict["1080p"]
    elif screen_area >= math.prod(ratios_dict["720p"]):
        return ratios_dict["720p"]
    else:
        return ratios_dict["480p"] """

# ใช้ปรับของนผ เพราะตอนแรกใช้ขนาด 1080p เปลี่ยนเป็น 720p
def change_ratio_1080_to_720(old):
    return round(old / 1.5)