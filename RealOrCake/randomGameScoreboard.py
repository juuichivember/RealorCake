import pygame, os
from decoModule import get_base_path

# Scoreboard สำหรับ Random Mode (รองรับ filling)
FULLSCORE = 14        # 7 parts x 2 points
PART_FULLSCORE = 2

class RandomGameScoreboard:
    def __init__(self, player_parts, random_parts, gsm):
        self.fontsize = 36
        base_path = get_base_path()
        font_path = os.path.join(base_path, "assets", "font", "nura-wat-thin.ttf")
        self.font = pygame.font.Font(font_path, self.fontsize)
        self.fontcolor = (0, 0, 0)

        self.score = 0
        self.player_parts = player_parts
        self.random_parts = random_parts
        self.score_description = {}
        self.gsm = gsm  # รับ GameStateManager เพื่อใช้ในการดึงค่า flavor (filling)
        self.debug_printed = False  # Flag to control debug printing

    def calculate_score(self):
        if self.debug_printed:
            return self.score  # Return score if already calculated

        # ดึงค่า filling ที่ผู้เล่นเลือกจาก GameStateManager
        player_filling = self.gsm.get_flavor()

        # เตรียมลิสต์ parts ที่ต้องตรวจ ทั้ง decoration + รสไส้
        all_parts = [
            "base", "behindcream", "lowercream",
            "middlecream", "topcream", "topping",
            "filling"
        ]

        # เติม "none" ให้ครบทุก part ทั้งสองชุด
        for part in all_parts:
            if part not in self.player_parts:
                self.player_parts[part] = ("none", "none")
            if part not in self.random_parts:
                self.random_parts[part] = ("none", "none")

        # เรียงคีย์เพื่อ deterministic output และคำนวณคะแนน
        self.score = 0
        for part in sorted(all_parts):
            p_type, p_color = self.player_parts[part]
            r_type, r_color = self.random_parts[part]
            
            # Debug แสดงผลการเปรียบเทียบ
            print(f"Comparing {part}:")
            print(f"  Player selected {part} -> Type: {p_type}, Color: {p_color}")
            print(f"  Random (target) {part} -> Type: {r_type}, Color: {r_color}")

            # กรณี filling: ให้ 2 คะแนนเมื่อรส (color) ตรงเท่านั้น
            if part == "filling":
                # เทียบค่าที่ผู้เล่นเลือกกับที่สุ่มออกมา
                part_score = 2 if player_filling == r_color else 0
                print(f"  Filling score: {part_score} (Player selected {player_filling}, Random was {r_color})")
            else:
                # decoration: type + color ปกติ
                part_score = (1 if p_type == r_type else 0) + (1 if p_color == r_color else 0)
                print(f"  Score for {part}: {part_score} (Type match: {1 if p_type == r_type else 0}, Color match: {1 if p_color == r_color else 0})")

            self.score_description[part] = (part_score, PART_FULLSCORE)
            self.score += part_score

        # สรุปคะแนนรวม
        self.score_description["Final score"] = (self.score, FULLSCORE)
        print(f"Final score: {self.score}/{FULLSCORE}")
        
        self.debug_printed = True  # Mark debug as printed
        return self.score

    # คำนวณดาว 5 คะแนน
    def score_5star(self):
        return round((self.score / FULLSCORE) * 5)

    def set_score(self, score):
        self.score = score

    def get_score(self):
        return self.score

    def format_text(self):
        # สร้างข้อความแสดงคะแนนแต่ละ part
        labels = []
        scores = []
        for part, (sc, full) in self.score_description.items():
            labels.append(part.capitalize())
            scores.append(f"{sc} / {full} points")
        return labels, scores

    def get_des_to_render(self):
        l_pos = (244, 150)
        s_pos = (520, 150)
        labels, scores = self.format_text()
        label_surfs = [self.font.render(t, True, self.fontcolor) for t in labels]
        score_surfs = [self.font.render(t, True, self.fontcolor) for t in scores]
        return label_surfs, score_surfs, l_pos, s_pos

    def render(self, display):
        labels, scores, (lx, ly), (sx, sy) = self.get_des_to_render()
        for idx, surf in enumerate(labels):
            display.blit(surf, (lx, ly + idx * (self.fontsize + 5)))
        for idx, surf in enumerate(scores):
            display.blit(surf, (sx, sy + idx * (self.fontsize + 5)))
