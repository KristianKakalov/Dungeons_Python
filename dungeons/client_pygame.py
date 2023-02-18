import pygame

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 400
BOARD_WIDTH = 400
BOARD_HEIGHT = 400

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

chat_history = ["hello", "hi","hello", "hi","hello", "hii"]


class ClientVisualization:

    def visualize(self):
        pygame.init()
        self.FONT = pygame.font.Font(None, 30)
        self.game_window = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("DUNGEONS")

        self.board_surface = pygame.Surface(
            (BOARD_WIDTH, BOARD_HEIGHT))
        self.board_surface.fill(GREEN)

        font = pygame.font.Font(None, 36)

        self.messages_surface = pygame.Surface(
            (WINDOW_WIDTH - BOARD_WIDTH, BOARD_HEIGHT))

        self.messages_surface.fill(GRAY)
        text_surface = font.render("Messages", True, BLACK)
        self.messages_surface.blit(text_surface, (10, 10))

    def start(self):
        self.display_messages()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update game state

            # Draw game elements
            # Set the game window background color to black
            self.game_window.fill((0, 0, 0))

            # Draw the board
            self.game_window.blit(self.board_surface, (0, 0))

            # Draw the messages
            self.game_window.blit(self.messages_surface,
                                  (BOARD_WIDTH, 0))

            # Update the display
            pygame.display.update()

        # Clean up Pygame
        pygame.quit()

    def display_messages(self):
        message = "\n".join(chat_history[:-15:-1])
        message_surface = self.FONT.render(message, True, BLACK)
        self.messages_surface.blit(message_surface, (10, 50))


if __name__ == '__main__':
    cv = ClientVisualization()
    cv.visualize()
    cv.start()
