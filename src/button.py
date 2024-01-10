import pygame, assets, json, assets, sys
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
LIGHT_GREY = (230, 230, 230)
HOVER_OVERLAY = (200, 200, 200, 255)

class Button:
    def __init__(self, text, x, y, action=None):
        self.text = text
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, assets.width * assets.height // 57600)
        self.color = WHITE  # Initial color of the text
        self.hover_color = GREY  # Color when mouse hovers over
        self.action = action

        # Load the button frame image
        self.frame_image = pygame.image.load('../graphics/menu/button.png').convert_alpha()
        self.frame_image = pygame.transform.scale(self.frame_image, (assets.width / 6, assets.height / 17))
        # Render the text
        self.rendered_text = self.font.render(self.text, True, self.color)
        self.text_rect = self.rendered_text.get_rect(center=(x, y))

        # Adjust the frame size and position based on the text size
        self.frame_rect = self.frame_image.get_rect(center=(x, y))

        self.greyed_frame_image = self.frame_image.copy()
        overlay = pygame.Surface(self.greyed_frame_image.get_size(), pygame.SRCALPHA)
        overlay.fill(HOVER_OVERLAY)
        self.greyed_frame_image.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        self.hovered = False

    def draw(self):
        # Decide which image to use based on hover state
        frame_image_to_use = self.greyed_frame_image if self.hovered else self.frame_image
        assets.screen.blit(frame_image_to_use, self.frame_rect.topleft)

        # Draw the text
        assets.screen.blit(self.rendered_text, self.text_rect)

    def is_hovered(self, position):
        if self.frame_rect.collidepoint(position):
            # Change to hover color and indicate the button is hovered
            self.rendered_text = self.font.render(self.text, True, self.hover_color)
            self.hovered = True
            return True
        else:
            # Change back to normal color and indicate the button is not hovered
            self.rendered_text = self.font.render(self.text, True, self.color)
            self.hovered = False
            return False

    def click(self):
        assets.buttonClickSound.play()
        if self.action:
            self.action()
    
    @staticmethod
    def quit_game():
        pygame.quit()
        sys.exit()

    @staticmethod
    def save_game():
        
        imp_dict = []
        for enemy in assets.enemies:
            if enemy.name == 'imp':
                imp_dict.append({'position': list(enemy.rect.topleft), 'health': enemy.health})
        game_state = {
            'level': assets.level,
            'player': {
                'player_position': list(assets.player.rect.topleft),
                'health': assets.player.health,
                'mana': assets.player.mana
            },
            'imps': imp_dict
        }
        with open('../saved/game_state.json', 'w') as f:
            json.dump(game_state, f, indent = 4)