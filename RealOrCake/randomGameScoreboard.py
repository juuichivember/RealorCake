import pygame, os
from decoModule import get_base_path
FULLSCORE = 12
PART_FULLSCORE = 2

# Scoreboard ใน Score State

class RandomGameScoreboard():
    def __init__(self, player_parts, random_parts):
        self.fontsize = 36
        base_path = get_base_path()
        self.font = pygame.font.Font(os.path.join(base_path, "assets", "font", "nura-wat-thin.ttf"), self.fontsize)
        self.fontcolor = (0, 0, 0)

        self.score = 0
        self.player_parts = player_parts
        self.random_parts = random_parts
        self.score_description = {}
    
    def calculate_score(self):
        # คำนวณคะแนน ถ้าใน part เดียวกัน type เดียวกัน +1 สีเหมือนกัน +1

        self.score = 0
        all_parts = ["base", "behindcream", "lowercream", "middlecream", "topcream", "topping"]

        # เช็กว่า parts เท่ากัน ถ้าไม่เท่ากันจะเติม none ใส่ใน parts
        if len(self.player_parts) != len(all_parts):
            for part in all_parts:
                if part not in self.player_parts:
                    self.player_parts[part] = ("none", "none")
        myKeys = list(self.player_parts.keys())
        myKeys.sort()
        self.player_parts = {i: self.player_parts[i] for i in myKeys} # Sorted Dictionary

        print("randomized cake", self.random_parts)
        print("player's cake", self.player_parts)

        # คำนวณคะแนน
        for p_part, (p_type, p_color) in self.player_parts.items():
            for r_part, (r_type, r_color) in self.random_parts.items():
                part_score = 0
                if p_part == r_part:
                    if p_type == r_type:
                        part_score += 1
                    if p_color == r_color:
                        part_score += 1
                    self.score_description[r_part] = (part_score, PART_FULLSCORE)
                self.score += part_score

        self.score_description["Final score"] = (self.score, FULLSCORE)
        return self.score
    
    def score_5star(self):
        # คำนวณคะแนนเต็มห้า แล้วปัดเลข

        star = round((self.get_score() / FULLSCORE) * 5)
        return star

    def set_score(self, score):
        self.score = score
    
    def get_score(self):
        return self.score

    def format_text(self):
        # บันทึกคะแนนเป็น dictionary

        label_text = []
        score_text = []
        for part, (score, full) in self.score_description.items():
            text = f"{part.capitalize()}"
            label_text.append(text)

            s_text = f"{score} / {full} points"
            score_text.append(s_text)
        return label_text, score_text
    
    def get_des_to_render(self):
        # สร้าง objetct ให้ text แต่ละบรรทัดที่ได้จาก format_text()

        l_position = 244, 150
        s_position = 520, 150
        label_text, score_text = self.format_text()
        label_obj = []
        score_obj = []
        for line in label_text: 
            label_obj.append(self.font.render(line, True, self.fontcolor))
        for line in score_text: 
            score_obj.append(self.font.render(line, True, self.fontcolor))
        return label_obj, score_obj, l_position, s_position

    def render(self, display):
        # display text, ใส่ใน run
        
        label_obj, score_obj, l_position, s_position = self.get_des_to_render()
        for line in range(len(label_obj)):
            x = l_position[0]
            y = l_position[1]+(line*self.fontsize)+(5*line)
            display.blit(label_obj[line],(x, y))
        for line in range(len(score_obj)):
            x = s_position[0]
            y = s_position[1]+(line*self.fontsize)+(5*line)
            display.blit(score_obj[line],(x, y))