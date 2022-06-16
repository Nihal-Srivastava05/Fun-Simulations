import pygame

class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width*scale), int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, screen):
        action = False

        pos = pygame.mouse.get_pos()
        if(self.rect.collidepoint(pos)):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

class TextButton():
    def __init__(self, x, y, content, font_family='freesansbold.ttf', font_size=32, bg_color=(235, 235, 235)):
        self.font_family = font_family
        self.font_size = font_size
        font = pygame.font.Font(font_family, font_size)
        self.content = content
        self.text = font.render(content, True, (0, 0, 0), bg_color)
        self.rect = self.text.get_rect()
        self.rect.center = (x, y)
        self.clicked = False

    def change_bg_color(self, bg_color):
        # self.bg_color = bg_color
        font = pygame.font.Font(self.font_family, self.font_size)
        self.text = font.render(self.content, True, (0, 0, 0), bg_color)

    def draw(self, screen):
        action = False

        pos = pygame.mouse.get_pos()
        if(self.rect.collidepoint(pos)):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True


        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.text, self.rect)

        return action