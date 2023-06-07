import pygame, sys, random
from pygame.math import Vector2
import json
pygame.init()
import pygame.mixer
crash_sound = pygame.mixer.Sound('Sound/crash.wav')
class GameObject:
    """
    Base class for all game objects. Contains basic functionality for loading images and sounds.
    """

    def __init__(self):
        """
        Initializes GameObject with position set to None.
        """
        self.pos = None

    def load_image(self, name):
        """
        Loads an image from the Graphics folder with the given name.
        Args:
            name (str): Name of the image file without the extension.
        Returns:
            pygame.Surface: The loaded image.
        """
        return pygame.image.load(f'Graphics/{name}.png').convert_alpha()

    def load_sound(self, name):
        """
        Loads a sound from the Sound folder with the given name.
        Args:
            name (str): Name of the sound file without the extension.
        Returns:
            pygame.mixer.Sound: The loaded sound.
        """
        return pygame.mixer.Sound(f'Sound/{name}.wav')


class Obstacle(GameObject):
    """
    Represents an obstacle in the game. This obstacle is a specific GameObject that can collide with the snake.
    """

    def __init__(self, fruit, snake_body):
        """
        Initializes an Obstacle object.
        Args:
            fruit (GameObject): The fruit object in the game.
            snake_body (list): List of the snake body parts.
        """
        super().__init__()
        self.fruit = fruit
        self.snake_body = snake_body
        self.randomize()
        self.obstacle_image = self.load_image('obstacle')

    def draw_obstacle(self):
        """
        Draws the obstacle on the screen.
        """
        obstacle_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.obstacle_image, obstacle_rect)

    def randomize(self):
        """
        Randomizes the position of the obstacle.
        """
        while True:
            x = random.randint(0, cell_number - 1)
            y = random.randint(0, cell_number - 1)
            self.pos = pygame.Vector2(x, y)
            if (self.pos not in self.snake_body) and (self.pos != self.fruit.pos):
                break

    def check_collision(self, game_object):
        """
        Checks if the obstacle collides with another game object.
        Args:
            game_object (GameObject): The game object to check for collision.
        Returns:
            bool: True if the obstacle and the game object are at the same position, False otherwise.
        """
        return self.pos == game_object.pos


class Boom(Obstacle):
    """
    Represents a boom object in the game. This boom object is a specific Obstacle that can collide with the snake.
    """

    def __init__(self, fruit, snake_body):
        """
        Initializes a Boom object.
        Args:
            fruit (GameObject): The fruit object in the game.
            snake_body (list): List of the snake body parts.
        """
        super().__init__(fruit, snake_body)
        self.boom_image = pygame.image.load('Graphics/boom.png').convert_alpha()

    def draw_obstacle(self):
        """
        Draws the boom obstacle on the screen.
        """
        obstacle_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.boom_image, obstacle_rect)

    def check_collision(self, game_object):
        """
        Checks if the boom collides with another game object.
        Args:
            game_object (GameObject): The game object to check for collision.
        Returns:
            bool: True if the boom and the game object are at the same position, False otherwise.
        """
        return self.pos == game_object.pos

    def randomize(self):
        """
        Randomizes the position of the boom.
        """
        while True:
            x = random.randint(0, cell_number - 1)
            y = random.randint(0, cell_number - 1)
            self.pos = pygame.Vector2(x, y)
            if (self.pos not in self.snake_body) and (self.pos != self.fruit.pos):
                break



class SNAKE(GameObject):
    """
        Represents the snake in the game. The snake is a GameObject that can move around and collide with other objects.
    """
    def __init__(self):
        """
        Initializes the snake with a specific body and direction. It also preloads images and sounds.
        """
        super().__init__()
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False
        self.images = {name: self.load_image(name) for name in (
            'head_up', 'head_down', 'head_right', 'head_left',
            'tail_up', 'tail_down', 'tail_right', 'tail_left',
            'body_vertical', 'body_horizontal',
            'body_tr', 'body_tl', 'body_br', 'body_bl')}
        self.crunch_sound = self.load_sound('crunch')

    def draw_snake(self):
        """
        Draws the snake on the screen. It decides which image to use based on the snake's direction.
        """
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.images['body_vertical'], block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.images['body_horizontal'], block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.images['body_tl'], block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.images['body_bl'], block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.images['body_tr'], block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.images['body_br'], block_rect)

    def update_head_graphics(self):
        """
        Updates the head image of the snake based on its direction.
        """
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.images['head_left']
        elif head_relation == Vector2(-1, 0):
            self.head = self.images['head_right']
        elif head_relation == Vector2(0, 1):
            self.head = self.images['head_up']
        elif head_relation == Vector2(0, -1):
            self.head = self.images['head_down']

    def update_tail_graphics(self):
        """
        Updates the tail image of the snake based on its direction.
        """
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.images['tail_left']
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.images['tail_right']
        elif tail_relation == Vector2(0, 1):
            self.tail = self.images['tail_up']
        elif tail_relation == Vector2(0, -1):
            self.tail = self.images['tail_down']

    def move_snake(self):
        """
        Moves the snake in its current direction. If it's about to grow, it doesn't lose its tail.
        """
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self, num_blocks=1):
        """
        Adds a new block to the snake's body.
        Args:
            num_blocks (int, optional): Number of blocks to add. Defaults to 1.
        """
        for _ in range(num_blocks):
            self.body.append(self.body[-1])

    def play_crunch_sound(self):
        """
        Plays the crunch sound.
        """
        self.crunch_sound.play()

    def reset(self):
        """
        Resets the snake to its initial state.
        """
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

    def check_collision(self, game_object):
        """
       Checks if the snake's head collides with another game object.
       Args:
           game_object (GameObject): The game object to check for collision.
       Returns:
           bool: True if the snake's head and the game object are at the same position, False otherwise.
       """
        return self.body[0] == game_object.pos

    def check_self_collision(self):
        """
        Checks if the snake's head collides with its body.
        Returns:
            bool: True if the snake's head is in its body, False otherwise.
        """
        return self.body[0] in self.body[1:]


class FRUIT(GameObject):
    """
    Represents the fruit in the game. The fruit is a GameObject that can be eaten by the snake.
    """
    def __init__(self, obstacles, snake_body):
        """
        Initializes the fruit object. Places the fruit at a random location not occupied by the snake or obstacles.
        Args:
            obstacles (list): List of all obstacles in the game.
            snake_body (list): List of the snake body parts.
        """
        super().__init__()
        self.obstacles = obstacles
        self.snake_body = snake_body
        self.randomize()
        self.apple = self.load_image('apple')

    def draw_fruit(self):
        """
        Draws the fruit on the screen at its current position.
        """
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)
        # pygame.draw.rect(screen,(126,166,114),fruit_rect)

    def randomize(self):
        """
        Randomizes the position of the fruit. The fruit cannot be placed at a position occupied by the snake or obstacles.
        """
        while True:
            x = random.randint(0, cell_number - 1)
            y = random.randint(0, cell_number - 1)
            self.pos = pygame.Vector2(x, y)
            if (self.pos not in self.snake_body) and (self.pos not in [obstacle.pos for obstacle in self.obstacles]):
                break

    def check_collision(self, game_object):
        """
        Checks if the fruit collides with another game object.
        Args:
            game_object (GameObject): The game object to check for collision.
        Returns:
            bool: True if the fruit and the game object are at the same position, False otherwise.
        """
        return self.pos == game_object.pos

    def eaten(self):
        """
        Randomizes the fruit's position after it's eaten.
        """
        self.randomize()


class BigFruit(GameObject):
    """
    Represents a special type of fruit (Big Fruit) in the game. Big Fruit is a GameObject that can be eaten by the snake.
    """
    def __init__(self, obstacles, snake_body):
        """
        Initializes the BigFruit object. Places the Big Fruit at a random location not occupied by the snake or obstacles.
        Args:
            obstacles (list): List of all obstacles in the game.
            snake_body (list): List of the snake body parts.
        """
        super().__init__()
        self.obstacles = obstacles
        self.snake_body = snake_body
        self.pos = None
        self.randomize()
        self.image = self.load_image('banana')

    def randomize(self):
        """
        Randomizes the position of the Big Fruit. The Big Fruit cannot be placed at a position occupied by the snake or obstacles.
        """
        while True:
            x = random.randint(0, cell_number - 1)
            y = random.randint(0, cell_number - 1)
            self.pos = pygame.Vector2(x, y)
            if self.pos not in self.snake_body and self.pos not in self.obstacles:
                break

    def draw_big_fruit(self):
        """
        Draws the Big Fruit on the screen at its current position.
        """
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.image, fruit_rect)

class PowerUp(GameObject):
    """
        Represents a power-up object in the game of snake.

        When the snake collides with a power-up, it becomes invincible for a while.

        Attributes
        ----------
        x : int
            The x-coordinate of the power-up in the game grid.
        y : int
            The y-coordinate of the power-up in the game grid.
        pos : pygame.Vector2
            The position of the power-up in the game grid.
        power_up : pygame.Surface
            The image surface representing the power-up.
        """
    def __init__(self, snake_body):
        """
        Initializes the power-up at a random position not occupied by the snake.

        Parameters
        ----------
        snake_body : list of pygame.Vector2
            The blocks constituting the body of the snake.
        """
        super().__init__()
        self.snake_body = snake_body
        self.randomize(snake_body)
        self.power_up = self.load_image('power_up')

    def randomize(self, snake_body):
        """
                Randomly positions the power-up at a position not occupied by the snake.

                Parameters
                ----------
                snake_body : list of pygame.Vector2
                    The blocks constituting the body of the snake.
        """
        while True:
            self.x = random.randint(0, cell_number - 1)
            self.y = random.randint(0, cell_number - 1)
            self.pos = pygame.Vector2(self.x, self.y)
            if self.pos not in self.snake_body:
                break

    def draw_power_up(self):
        """
        Draws the power-up onto the screen at its current position.
        """
        power_up_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(self.power_up, power_up_rect)


class MAIN(GameObject):
    """
    Represents the main game logic. This class encompasses the game loop, handles user input,
    updates the game state, and renders the game state each frame to create a functioning game.
    """
    def __init__(self):
        """
       Initializes the game object, sets the initial game state, and starts the game loop.
       """
        super().__init__()
        self.power_up_timer = None
        self.power_up_active = None
        self.power_up = None
        self.boom_timer = None
        self.boom_disappear = None
        self.boom_appear = None
        self.boom_start_time = None
        self.boom_active = None
        self.boom = None
        self.start_time = None
        self.level = None
        self.obstacles = None
        self.fruit = None
        self.snake = None
        self.score = 0
        self.high_score = 0
        self.reset_game()
        self.first_game_over = False
        self.game_font = pygame.font.Font(None, 36)
        self.big_fruit = None
        self.big_fruit_timer = None
        self.big_fruit_active = False
        self.big_score = 0
        self.crash_sound = self.load_sound('crash')

    def reset_game(self):
        """
       Resets the game state to its initial configuration.
       """
        self.snake = SNAKE()
        self.fruit = FRUIT([], self.snake.body)
        self.obstacles = [Obstacle(self.fruit, self.snake.body) for _ in
                          range(5)]
        self.big_fruit = BigFruit([], self.snake.body)
        self.big_fruit_active = False
        self.big_fruit_timer = 0
        self.level = 1
        self.start_time = pygame.time.get_ticks()
        self.boom = Boom(self.fruit, self.snake.body)
        self.boom_active = False
        self.boom_start_time = pygame.time.get_ticks()
        self.boom_appear = False
        self.boom_disappear = False
        self.boom_timer = 0
        self.first_game_over = False
        self.power_up = PowerUp(self.snake.body)
        self.power_up_active = False
        self.power_up_timer = 0

    def get_boom_elapsed_time(self):
        """
        Returns the elapsed time since the last 'boom' in seconds.
        """
        return (pygame.time.get_ticks() - self.boom_start_time) // 1000

    def get_elapsed_time(self):
        """
        Returns the elapsed time since the game start in seconds.
        """
        return (pygame.time.get_ticks() - self.start_time) // 1000

    def update(self):
        """
        Updates the game state each frame.
        Handles snake movement, collisions, and game progression mechanics.
        """
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        if self.big_fruit is None:
            # Instantiate BigFruit here before calling its methods
            self.big_fruit = BigFruit(self.obstacles, self.snake.body)

        if self.power_up.pos == self.snake.body[0]:
            self.power_up.randomize(self.snake.body)
            self.power_up_active = True
            self.power_up_timer = pygame.time.get_ticks()
        if self.power_up_active and pygame.time.get_ticks() - self.power_up_timer > 10000:
            self.power_up_active = False

        if self.get_elapsed_time() - self.boom_timer >= 10 and not self.boom_active:
            self.boom.randomize()
            self.boom_active = True
            self.boom_timer = self.get_elapsed_time()
        if self.big_score % 5 == 0 and self.big_score != 0 and not self.big_fruit_active:
            self.big_fruit.randomize()
            self.big_fruit_active = True
            self.big_fruit_timer = pygame.time.get_ticks()
        if self.big_fruit_active and (pygame.time.get_ticks() - self.big_fruit_timer) >= 5000:
            self.big_fruit_active = False
        if self.boom_active and self.get_elapsed_time() - self.boom_timer >= 3:
            self.boom_active = False

        score = len(self.snake.body) - 3
        if score > 10:
            pygame.time.set_timer(SCREEN_UPDATE, 70)
            if len(self.obstacles) < 10:
                self.obstacles.append(Obstacle(self.fruit, self.snake.body))
        elif score > 5:
            pygame.time.set_timer(SCREEN_UPDATE, 100)
        else:
            pygame.time.set_timer(SCREEN_UPDATE, 150)

    def check_collision(self):
        """
       Checks for collisions between the snake,
       fruit, and boom. Updates the game state accordingly.
       """

        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.score += 1
            self.big_score += 1
        if self.power_up.pos == self.snake.body[0]:
            self.snake.play_crunch_sound()
        if self.boom_active and self.boom.pos == self.snake.body[0] and not self.power_up_active:
            self.crash_sound.play()
            self.game_over()
        for obstacle in self.obstacles:
            if obstacle.pos == self.snake.body[0] and not self.power_up_active:
                self.crash_sound.play()
                self.game_over()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()
            for obstacle in self.obstacles:
                if block == obstacle.pos:
                    obstacle.randomize()
            if self.boom_active and block == self.boom.pos:
                self.boom.randomize()
            if self.big_fruit_active and block == self.big_fruit.pos:
                self.big_fruit.randomize()
        if self.big_fruit_active and self.big_fruit.pos == self.snake.body[0]:
            self.big_fruit_active = False
            self.big_fruit.randomize()
            self.snake.add_block(0)
            self.snake.play_crunch_sound()
            self.score += 3
        score = len(self.snake.body) - 3
        if score > 10:
            self.level = 3
            pygame.time.set_timer(SCREEN_UPDATE, 70)
        elif score > 5:
            self.level = 2
            pygame.time.set_timer(SCREEN_UPDATE, 100)
        else:
            self.level = 1
            pygame.time.set_timer(SCREEN_UPDATE, 150)

    def draw_level(self):
        """
        Renders the current game level on the screen.
        """
        level_text = "Level: " + str(self.level)
        level_surface = game_font.render(level_text, True, (56, 74, 12))
        level_x = int(cell_size * cell_number - 120)
        level_y = 40
        level_rect = level_surface.get_rect(center=(level_x, level_y))
        bg_rect = pygame.Rect(level_rect.left, level_rect.top, level_rect.width + 6, level_rect.height)
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(level_surface, level_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def draw_elements(self):
        """
        Renders the game state each frame. This includes all game objects like the snake, fruit, and boom.
        """
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()
        self.draw_level()
        if self.boom_active:
            self.boom.draw_obstacle()
        if self.big_fruit_active:
            self.big_fruit.draw_big_fruit()
        if not self.power_up_active:
            self.power_up.draw_power_up()
        for obstacle in self.obstacles:
            obstacle.draw_obstacle()

    def check_fail(self):
        """
        Checks if the game has ended (either the snake has hit a wall or collided with itself).
        """
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.crash_sound.play()
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        """
        This function is triggered when the game is over.
        It resets the snake, resets the game start time,
        disables the boom feature,
        updates the high score if the current score is higher,
        resets the score to zero, resets the snake again,
        sets first_game_over to True and waits for player input.
        """
        self.snake.reset()
        self.start_time = pygame.time.get_ticks()
        self.boom_active = False
        if self.score > self.high_score:
            self.high_score = self.score
        self.display_message(f"Game Over! Press 'Q' to Quit or 'C' to New Game")
        self.score = 0
        self.snake.reset()
        self.first_game_over = True
        self.wait_for_player_input()

    def wait_for_player_input(self):
        """
        This function is an infinite loop that waits for the player's input. It listens for pygame events.
        If the event is QUIT, it exits the game. If the event is a key press, it checks if the key is 'C'
        and if this is the first game over event, in which case it resets the game and breaks the loop.
        If the key is an arrow key, it also breaks the loop. The function also includes a short delay to reduce CPU usage.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if self.first_game_over and event.key == pygame.K_c:
                        self.reset_game()
                        return
                    if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                        return
                pygame.time.delay(100)

    def display_message(self, message):
        """
        This function is used to display messages on the game screen. It renders the provided message and
        the current score and high score in white color, and blits them on the screen at the center position.
        """
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, (255, 255, 255))
        rect = text.get_rect(center=(win_size[0] // 2, win_size[1] // 2))
        screen.blit(text, rect)

        score_text = f'Score: {self.score}'
        high_score_text = f'High Score: {self.high_score}'

        score_surface = game_font.render(score_text, True, (255, 255, 255))  # brighter color for better visibility
        high_score_surface = game_font.render(high_score_text, True,
                                              (255, 255, 255))  # brighter color for better visibility

        score_rect = score_surface.get_rect(midtop=(win_size[0] // 2, rect.bottom + 40))
        high_score_rect = high_score_surface.get_rect(midtop=(win_size[0] // 2, score_rect.bottom + 20))

        screen.blit(score_surface, score_rect)
        screen.blit(high_score_surface, high_score_rect)

        pygame.display.flip()

    def draw_grass(self):
        """
        This function is used to draw a grass pattern on the game screen. It loops through all cells on the screen
        and colors them in a checkered pattern.
        """
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        """
        This function is used to draw the score and elapsed time on the game screen.
        It creates a surface for the score and elapsed time, renders them, and then blits them onto the screen.
        It also includes the apple icon next to the score. The scores are displayed in a rectangular box of contrasting color.
        """
        score_text = str(self.score)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = 60
        score_y = 40
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        apple_rect = apple.get_rect(midright=(score_rect.left, score_rect.centery))
        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, apple_rect.width + score_rect.width + 6,
                              apple_rect.height)
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)
        time_text = str(self.get_elapsed_time()) + "s"
        time_surface = game_font.render(time_text, True, (56, 74, 12))
        time_x = int(cell_size * cell_number - 40)
        time_y = 40
        time_rect = time_surface.get_rect(center=(time_x, time_y))
        bg_rect = pygame.Rect(time_rect.left, time_rect.top, time_rect.width + 6, time_rect.height)
        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(time_surface, time_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)


cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
main_game = MAIN()
win_size = (cell_number * cell_size, cell_number * cell_size)
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)



def show_help_screen():
    """
   This function is used to show a help screen with instructions for the player.
   It creates a title and a list of instructions, and renders them onto the screen.
   It also creates a 'Back' button that the player can click on to return to the previous screen.
   The function is an infinite loop that waits for player input to either quit the game or go back.
   """
    font_title = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 50)  # Use a custom font if available
    font_instructions = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30)

    title = font_title.render("Welcome to Snake Game!", True, (255, 255, 255))
    title_rect = title.get_rect(center=(win_size[0] // 2, win_size[1] // 10))  # Center the title

    instructions = [
        "How to Play:",
        "1. Navigate the snake to eat fruits.",
        "2. Use arrow keys for control.",
        "3. Press 'P' to pause/resume.",
        "4. 'H' Or 'Back' returns to the main menu.",
        "5. Eat start to invincible",
        "Enjoy and Good luck!"
    ]

    screen.fill((0, 0, 0))
    screen.blit(title, title_rect)

    for i, line in enumerate(instructions, start=1):
        if i == 1:
            color = (0, 255, 0)
        elif i == len(instructions):  # Change this line to specify the last instruction.
            color = (255, 0, 0)  # Change this to red.
        else:
            color = (255, 255, 255)
        text = font_instructions.render(line, True, color)
        text_rect = text.get_rect(center=(win_size[0] // 2, i * win_size[1] // (len(instructions) + 1)))  # Center the instructions
        screen.blit(text, text_rect)
    back_button_text = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 30).render('Back', True, (255, 255, 255))
    back_button_rect = pygame.draw.rect(screen, (50, 50, 50), (20, win_size[1] - 60, 100, 30))  # Draw a button
    screen.blit(back_button_text, (back_button_rect.x + 30, back_button_rect.y))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if back_button_rect.collidepoint(mouse_pos):
                    return



def save_game():
    """
        This function saves the game state and high scores.
        The game state includes the snake's body and direction, the fruit's position,
        the big fruit's position, the boom's position, the power's position, the obstacle's position, and the score.
        The game state is saved to a json file.
        The high scores are read from a json file, updated with the current score if it's higher,
        sorted in descending order, and saved back to the json file.
    """
    game_state = {
        'snake_body': [[segment.x, segment.y] for segment in main_game.snake.body],
        'snake_direction': [main_game.snake.direction.x, main_game.snake.direction.y],
        'fruit_position': [main_game.fruit.pos.x, main_game.fruit.pos.y],
        'big_fruit_position': [main_game.big_fruit.pos.x, main_game.big_fruit.pos.y] if main_game.big_fruit else None,
        'boom_position': [main_game.boom.pos.x, main_game.boom.pos.y] if main_game.boom else None,
        'power_position': [main_game.power_up.pos.x, main_game.power_up.pos.y] if main_game.power_up else None,
        # 'obstacle_position': [[obstacle.x, obstacle.y] for obstacle in main_game.obstacles],
        'score': main_game.score,
    }
    with open('savegame.json', 'w') as f:
        json.dump(game_state, f)

    try:
        with open('high_scores.json', 'r') as f:
            scores = json.load(f)
    except FileNotFoundError:
        scores = []

    scores.append(main_game.score)
    scores.sort(reverse=True)
    scores = scores[:5]

    with open('high_scores.json', 'w') as f:
        json.dump(scores, f)




def load_game():
    """
   This function loads the game state from a json file. It reads the snake's body and direction,
   the fruit's position, and the score from the json file and sets the state of the main_game object
   accordingly. It also sets the big_fruit's position if it exists in the game state.
   """
    with open('savegame.json', 'r') as f:
        game_state = json.load(f)
    main_game.snake.body = [Vector2(*segment) for segment in
                            game_state['snake_body']]
    main_game.snake.direction = Vector2(*game_state['snake_direction'])
    main_game.fruit.position = Vector2(*game_state['fruit_position'])
    main_game.score = game_state['score']
    # main_game.big_fruit.position = Vector2(*game_state['big_fruit_position'])  # Adding this line




def main_menu():
    """
    This function displays the main menu of the game. It shows a title and a list of options including
    'New Game', 'Continue', and 'Help'. These options are interactive and change color when hovered over.
    If the 'Continue' option is clicked, it loads a previously saved game. If the 'New Game' option is
    clicked, it resets the game. If the 'Help' option is clicked, it displays the help screen.
    """
    font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 60)  # change to a custom font
    title_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 100)  # game title font
    menu_options = ['New Game', 'Continue', 'Help']
    options_rects = []
    screen.fill((80, 60, 50))
    title_text = title_font.render("Snake Game", True, (255, 225, 0))  # game title
    title_rect = title_text.get_rect()
    title_rect.center = (win_size[0] // 2, win_size[1] //6)  # position game title
    screen.blit(title_text, title_rect)
    for i, option in enumerate(menu_options):
        text = font.render(option, True, (255, 255, 255))  # change text color to white
        rect = text.get_rect()
        rect.center = (win_size[0] // 2, (i + 1) * win_size[1] // (len(menu_options) + 1))
        options_rects.append(rect)
        screen.blit(text, rect)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                for i, rect in enumerate(options_rects):
                    if rect.collidepoint(pos):
                        text = font.render(menu_options[i], True, (255, 255, 255))
                        screen.blit(text, rect)
                    else:
                        text = font.render(menu_options[i], True,
                                           (0, 0, 0))
                        screen.blit(text, rect)
                pygame.display.flip()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for i, rect in enumerate(options_rects):
                    if rect.collidepoint(pos):
                        if menu_options[i] == 'Continue':
                            load_game()
                            return
                        elif menu_options[i] == 'New Game':
                            main_game.reset_game()
                            return
                        elif menu_options[i] == 'Help':
                            show_help_screen()
                            screen.fill((100, 100, 100))
                            main_menu()
                        return


def pause_game():
    """
    This function pauses the game and shows a message on the screen. It waits for the player to press 'P'
    to continue the game. If the player chooses to quit the game during the pause, it closes the game.
    """
    paused = True
    pause_text = game_font.render("Paused. Press P to continue...", True, (255, 0, 0)) # change color to red
    rect = pause_text.get_rect()
    rect.center = ((cell_number * cell_size) // 2, (cell_number * cell_size) // 2)
    screen.blit(pause_text, rect)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False



main_menu()
"""
Main game loop. It continuously checks for events like quitting the game, updating the game state, 
and key presses for controlling the snake. If the 'p' key is pressed, it pauses the game. 
If the 'q' key is pressed, it saves the game state and quits the game. It also draws the game 
elements and updates the screen at each iteration.
"""
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)
            elif event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_p:
                pause_game()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    save_game()
                    pygame.quit()
                    sys.exit()
    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
