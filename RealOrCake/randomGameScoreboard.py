import pygame
FULLSCORE = 12
PART_FULLSCORE = 2

class RandomGameScoreboard():
    def __init__(self, player_parts, random_parts):
        self.fontsize = 36
        self.font = pygame.font.Font('font/nura-wat-thin.ttf', self.fontsize)
        self.fontcolor = (0, 0, 0)

        self.score = 0
        self.player_parts = player_parts
        self.random_parts = random_parts
        self.score_description = {}
    
    def calculate_score(self):
        self.score = 0
        all_parts = ["base", "behindcream", "lowercream", "middlecream", "topcream", "topping"]

        if len(self.player_parts) != len(all_parts):
            for part in all_parts:
                if part not in self.player_parts:
                    self.player_parts[part] = ("none", "none")
        myKeys = list(self.player_parts.keys())
        myKeys.sort()
        self.player_parts = {i: self.player_parts[i] for i in myKeys} # Sorted Dictionary

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
        #for part in all_parts:
            #if part not in self.random_parts:
                #self.score_description[part] = (PART_FULLSCORE, PART_FULLSCORE)
                #score += PART_FULLSCORE

        self.score_description["Final score"] = (self.score, FULLSCORE)
        return self.score
    
    def score_5star(self):
        star = round((self.get_score() / FULLSCORE) * 5)
        return star

    def set_score(self, score):
        self.score = score
    
    def get_score(self):
        return self.score

    def format_text(self):
        label_text = []
        score_text = []
        for part, (score, full) in self.score_description.items():
            text = f"{part.capitalize()}"
            label_text.append(text)

            s_text = f"{score} / {full} points"
            score_text.append(s_text)
        return label_text, score_text
    
    def get_des_to_render(self):
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
        label_obj, score_obj, l_position, s_position = self.get_des_to_render()
        for line in range(len(label_obj)):
            x = l_position[0]
            y = l_position[1]+(line*self.fontsize)+(5*line)
            display.blit(label_obj[line],(x, y))
        for line in range(len(score_obj)):
            x = s_position[0]
            y = s_position[1]+(line*self.fontsize)+(5*line)
            display.blit(score_obj[line],(x, y))