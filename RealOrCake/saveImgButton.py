from button import Button
import pygame
import os
import re

# https://stackoverflow.com/questions/68804453/save-created-image-to-file-system-python-and-pygame/68805404

class SaveImgButton(Button):
    def __init_subclass__(cls):
        return super().__init_subclass__()

    def save_cake_img(self, screen, x, y, width, height):
        number = self.get_last_highest_screenshot_number()
        if number:
            id = int(number) + 1
        else:
            id = 1
        rect_area = pygame.Rect(x, y, width, height)
        area_surf = screen.subsurface(rect_area)
        pygame.image.save(area_surf, f"Screenshots/shots{id}.png")

    def get_last_highest_screenshot_number(self, directory="Screenshots"):
        try:
            filenames = os.listdir(directory)
        except FileNotFoundError:
            os.makedirs(directory)
            return None  # Return None if directory not found

        numbers = []
        pattern = re.compile(r"shots(\d+)\.png")

        for filename in filenames:
            match = pattern.match(filename)
            if match:
                numbers.append(int(match.group(1)))

        if numbers:  # Check if the list is not empty
            return max(numbers)  # Return the highest number
        else:
            return None