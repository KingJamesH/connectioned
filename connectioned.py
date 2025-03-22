import pygame
import random

pygame.init()

WIDTH, HEIGHT = 612, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connectioned")
BOX_SIZE = 85
MARGIN = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SELECTED_COLOR = (130, 16, 33)
DARK_GRAY = (100, 100, 100)
COLORS = [(200, 100, 100), (100, 200, 100), (100, 100, 200), (200, 200, 100)]

pygame.font.init()
font = pygame.font.SysFont(None, 36)
titlefont= pygame.font.SysFont(None, 64)
word_font = pygame.font.SysFont(None, 18)

sections = [(0, 0, WIDTH // 2, HEIGHT // 2),
            (WIDTH // 2, 0, WIDTH // 2, HEIGHT // 2),
            (0, HEIGHT // 2, WIDTH // 2, HEIGHT // 2),
            (WIDTH // 2, HEIGHT // 2, WIDTH // 2, HEIGHT // 2)]

boxes = []
box_colors = []
box_words = []
for sec_idx, (sx, sy, sw, sh) in enumerate(sections):
    start_x = sx + (sw - 2 * (BOX_SIZE + MARGIN)) // 2
    start_y = sy + (sh - 2 * (BOX_SIZE + MARGIN)) // 2
    
    for i in range(4):
        x = start_x + (i % 2) * (BOX_SIZE + MARGIN)
        y = start_y + (i // 2) * (BOX_SIZE + MARGIN)
        boxes.append(pygame.Rect(x, y, BOX_SIZE, BOX_SIZE))
        box_colors.append(COLORS[sec_idx])

correct_placements = {
    0: ['apple', 'kiwi', 'orange', 'grape'],
    1: ['c++', 'python', 'html', 'java'],
    2: ['Prettier', 'intelliJ', 'git', 'docker'],
    3: ['theme', 'creativity', 'polish', 'technicality']
}

box_words = [
    'apple', 'kiwi', 'orange', 'grape',
    'c++', 'python', 'html', 'java',
    'Prettier', 'intelliJ', 'git', 'docker',
    'theme', 'creativity', 'polish', 'technicality'
]

random.shuffle(boxes)
random.shuffle(box_words)

selected_box = None
offset_x = 0
offset_y = 0
attempts = 0

def check_correct_placement():
    for correct_words in correct_placements.values():
        found = False
        
        for section_idx, section_rect in enumerate(sections):
            current_box_words = set()
            
            for i, box in enumerate(boxes):
                if section_rect[0] <= box.centerx < section_rect[0] + section_rect[2] and section_rect[1] <= box.centery < section_rect[1] + section_rect[3]:
                    current_box_words.add(box_words[i])
            
            if current_box_words == set(correct_words):
                found = True
                break
        
        if not found:
            return False
    
    return True

def start_screen():
    running = True
    while running:
        screen.fill(WHITE)
        
        logo = pygame.image.load('logo.png')
        logo = pygame.transform.scale(logo, (int(200 * (logo.get_height() / logo.get_width())), 200))
        logo_rect = logo.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(logo, logo_rect)
        
        title_text = titlefont.render("Connectioned", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(title_text, title_rect)
        
        start_button = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 50, WIDTH // 2, 40)
        pygame.draw.rect(screen, DARK_GRAY, start_button)
        pygame.draw.rect(screen, BLACK, start_button, 2)
        start_button_text = font.render("Start", True, WHITE)
        start_button_text_rect = start_button_text.get_rect(center=start_button.center)
        screen.blit(start_button_text, start_button_text_rect)
        
        footer_text = font.render(":)", True, BLACK)
        footer_text_rect = footer_text.get_rect(bottomleft=(WIDTH - 100, HEIGHT - 10))
        screen.blit(footer_text, footer_text_rect)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return

        pygame.display.flip()

def end_screen():
    running = True
    while running:
        screen.fill(WHITE)

        title_text = font.render("Congratulations!", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        tries_text = font.render("Tries: {}".format(attempts), True, BLACK)
        tries_rect = tries_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(tries_text, tries_rect)
        
        quit_button = pygame.Rect(WIDTH // 4, HEIGHT - 90, WIDTH // 2, 40)
        pygame.draw.rect(screen, DARK_GRAY, quit_button)
        pygame.draw.rect(screen, BLACK, quit_button, 2)
        quit_button_text = font.render("Quit", True, WHITE)
        quit_button_text_rect = quit_button_text.get_rect(center=quit_button.center)
        screen.blit(quit_button_text, quit_button_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button.collidepoint(event.pos):
                    running = False
        
        pygame.display.flip()

def game():
    global attempts, selected_box, offset_x, offset_y
    selected_box = None
    running = True
    while running:
        screen.fill(WHITE)

        for i, (sx, sy, sw, sh) in enumerate(sections):
            pygame.draw.rect(screen, COLORS[i], (sx, sy, sw, sh))

        pygame.draw.line(screen, BLACK, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT - 50), 3)
        pygame.draw.line(screen, BLACK, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for idx, box in enumerate(boxes):
                    if box.collidepoint(event.pos):
                        selected_box = idx
                        offset_x = box.x - event.pos[0]
                        offset_y = box.y - event.pos[1]
                        break
            elif event.type == pygame.MOUSEBUTTONUP:
                selected_box = None
            elif event.type == pygame.MOUSEMOTION and selected_box is not None:
                new_x = event.pos[0] + offset_x
                new_y = event.pos[1] + offset_y

                new_x = max(0, min(WIDTH - BOX_SIZE, new_x))
                new_y = max(0, min(HEIGHT - 50 - BOX_SIZE, new_y))

                boxes[selected_box].x = new_x
                boxes[selected_box].y = new_y

            if event.type == pygame.MOUSEBUTTONDOWN:
                submit_rect = pygame.Rect(WIDTH // 4, HEIGHT - 50, WIDTH // 2, 40)
                if submit_rect.collidepoint(event.pos):
                    attempts += 1
                    if check_correct_placement():
                        end_screen()
                        running = False
                    else:
                        print("Wrong!")

        for i, box in enumerate(boxes):
            color = SELECTED_COLOR if selected_box == i else box_colors[i]
            text_color = WHITE if selected_box == i else BLACK
            pygame.draw.rect(screen, color, box)
            pygame.draw.rect(screen, BLACK, box, 2)
            word_text = word_font.render(box_words[i], True, text_color)
            word_text_rect = word_text.get_rect(center=box.center)
            screen.blit(word_text, word_text_rect)

        submit_rect = pygame.Rect(WIDTH // 4, HEIGHT - 50, WIDTH // 2, 40)
        pygame.draw.rect(screen, DARK_GRAY, submit_rect)
        pygame.draw.rect(screen, BLACK, submit_rect, 2)
        submit_text = font.render("Submit", True, WHITE)
        submit_text_rect = submit_text.get_rect(center=submit_rect.center)
        screen.blit(submit_text, submit_text_rect)

        pygame.display.flip()

start_screen()
game()

pygame.quit()
