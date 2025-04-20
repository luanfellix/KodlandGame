import pgzrun
from random import randint

WIDTH = 1000
HEIGHT = 600


class Heroi:
    def __init__(self):
        self.actor = Actor("player_idle")
        self.actor.pos = 40, HEIGHT - 70
        self.vy = 0
        self.walk = True
        self.no_chao = True
        self.double_jump_used = False
        self.idle_frames = ["player_idle00", "player_idle01", "player_idle02", "player_idle03", "player_idle04",
                            "player_idle05", "player_idle06", "player_idle07", "player_idle08", "player_idle09"]
        self.idle_frame_index = 0
        self.idle_frame_timer = 0
        self.moving = False
        self.running_frames = [
            "player_run00", "player_run01", "player_run02", "player_run03", "player_run04",
            "player_run05", "player_run06", "player_run07", "player_run08", "player_run09"
        ]
        self.run_frame_index = 0
        self.run_frame_timer = 0
        self.jump_frames = [
            "player_jump00", "player_jump01", "player_jump02", "player_jump03", "player_jump04",
            "player_jump05", "player_jump06", "player_jump07", "player_jump08", "player_jump09"
        ]
        self.jump_frame_index = 0
        self.jump_frame_timer = 0

    def update_animation(self):
        if self.moving:
            self.run_frame_timer += 1
            if self.run_frame_timer >= 2:
                self.run_frame_index = (
                    self.run_frame_index + 1) % len(self.running_frames)
                self.actor.image = self.running_frames[self.run_frame_index]
                self.run_frame_timer = 0
        elif not self.no_chao:
            self.jump_frame_timer += 1
            if self.jump_frame_timer >= 5:
                self.jump_frame_index = (
                    self.jump_frame_index + 1) % len(self.jump_frames)
                self.actor.image = self.jump_frames[self.jump_frame_index]
                self.jump_frame_timer = 0
        else:
            self.idle_frame_timer += 1
            if self.idle_frame_timer >= 6:
                self.idle_frame_index = (
                    self.idle_frame_index + 1) % len(self.idle_frames)
                self.actor.image = self.idle_frames[self.idle_frame_index]
                self.idle_frame_timer = 0

    def draw(self):
        self.actor.draw()

    def move(self, dx):
        novo_x = self.actor.x + dx
        metade_largura = self.actor.width // 2
        limite_esquerdo = metade_largura
        limite_direito = WIDTH - metade_largura
        if limite_esquerdo <= novo_x <= limite_direito:
            self.actor.x = novo_x
        self.moving = True
        self.update_animation()

    def stop(self):
        self.moving = False
        self.update_animation()

    def jump(self):
        if self.no_chao:
            self.vy = -25
            self.no_chao = False
            self.double_jump_used = False
        elif not self.double_jump_used:
            self.vy = -25
            self.double_jump_used = True

    def apply_gravity(self, chao_y):
        GRAVITY = 1
        self.vy += GRAVITY
        self.actor.y += self.vy
        if self.actor.top <= 0:
            self.actor.top = 0
            self.vy = 0
        if self.actor.y >= chao_y:
            self.actor.y = chao_y
            self.vy = 0
            self.no_chao = True

    def reset(self):
        self.actor.pos = 40, HEIGHT - 70
        self.actor.image = "player_idle"
        self.vy = 0
        self.no_chao = True
        self.double_jump_used = False

    def cheer(self):
        self.actor.image = "player_cheer2"


class Vilao:
    def __init__(self, level_y):
        self.actor = Actor("zombie_walk00")
        self.actor.pos = WIDTH - 100, level_y
        self.walking_frames = [
            "zombie_walk00", "zombie_walk01", "zombie_walk02", "zombie_walk03",
            "zombie_walk04", "zombie_walk05", "zombie_walk06", "zombie_walk07",
            "zombie_walk08", "zombie_walk09"
        ]
        self.walk_frame_index = 0
        self.walk_frame_timer = 0

    def update_animation(self):
        self.walk_frame_timer += 1
        if self.walk_frame_timer >= 5:
            self.walk_frame_index = (
                self.walk_frame_index + 1) % len(self.walking_frames)
            self.actor.image = self.walking_frames[self.walk_frame_index]
            self.walk_frame_timer = 0

    def draw(self):
        self.actor.draw()

    def move(self):
        self.actor.x -= 2
        self.update_animation()

    def reset_pos(self, y):
        self.actor.pos = WIDTH, y


level = 0
box_enemies = []
dead = False
won = False
created = False
menu_active = True
music_on = True

menu_buttons = {
    "start": Rect((WIDTH//2 - 100, 200), (200, 50)),
    "music": Rect((WIDTH//2 - 100, 270), (200, 50)),
    "exit": Rect((WIDTH//2 - 100, 340), (200, 50))
}

background = {
    0: ["maxresdefault", 15, 40, HEIGHT - 70],
    1: ["mountain_back", 80, 40, HEIGHT - 120],
    2: ["desertcity", 15, 40, HEIGHT - 70],
    3: ["night", 15, 40, HEIGHT - 70]
}

player = Heroi()
zombie = Vilao(background[level][3])


def draw():
    screen.clear()
    if menu_active:
        draw_menu()
    elif won:
        draw_won()
    elif dead:
        draw_dead()
    else:
        draw_game()


def draw_menu():
    screen.fill((0, 0, 0))
    screen.draw.text("Platformer Game", center=(
        WIDTH//2, 100), fontsize=50, color="white")
    screen.draw.filled_rect(menu_buttons["start"], "gray")
    screen.draw.text(
        "Start Game", center=menu_buttons["start"].center, color="black", fontsize=30)
    screen.draw.filled_rect(menu_buttons["music"], "gray")
    screen.draw.text("Music: ON" if music_on else "Music: OFF",
                     center=menu_buttons["music"].center, color="black", fontsize=30)
    screen.draw.filled_rect(menu_buttons["exit"], "gray")
    screen.draw.text(
        "Exit", center=menu_buttons["exit"].center, color="black", fontsize=30)
    screen.draw.text("Controles:", topleft=(
        20, 420), fontsize=28, color="white")
    screen.draw.text("- Andar: A / D ou Setinha(esquerda, direita)",
                     topleft=(40, 460), fontsize=24, color="white")
    screen.draw.text("- Pular: W ou Seta pra cima",
                     topleft=(40, 490), fontsize=24, color="white")
    screen.draw.text("- Restart: R (se morreu)",
                     topleft=(40, 520), fontsize=24, color="white")


def draw_dead():
    screen.blit(background[level][0], (0, 0))
    screen.draw.text("Você foi pego!!!", center=(
        WIDTH//2, HEIGHT//2), fontsize=30, color="white")
    screen.draw.text("Aperte R para jogar novamente.", center=(
        WIDTH//2, HEIGHT//2 + 50), fontsize=25, color="yellow")


def draw_game():
    screen.blit(background[level][0], (0, 0))
    player.draw()
    zombie.draw()
    draw_box_enemies()


def draw_won():
    screen.blit(background[level][0], (0, 0))
    screen.draw.text("You Won !!!", center=(
        WIDTH//2, HEIGHT//2), fontsize=30, color="white")
    player.actor.pos = (WIDTH//2)+100, HEIGHT//2
    player.cheer()
    player.draw()


def update():
    global level, dead, won, created
    if menu_active or won:
        return
    zombie.move()
    move_box_enemies()
    check_collisions()
    if not dead:
        chao_y = background[level][3]
        player.apply_gravity(chao_y)
        handle_level_progression()
    player.update_animation()


def handle_level_progression():
    global level, created, won
    if player.actor.left >= WIDTH:
        if level < 3:
            level += 1
            created = False
            player.actor.pos = background[level][2], background[level][3]
            zombie.reset_pos(background[level][3])
            sounds.maximize_004.play()
        else:
            player.actor.pos = WIDTH//2, HEIGHT//2
            player.cheer()
            won = True
            sounds.maximize_004.play()


def check_collisions():
    global dead, created
    if not created:
        generate_boxes(level)
        created = True
    if zombie.actor.right == 500:
        generate_boxes(level)
    if zombie.actor.right <= 0:
        zombie.reset_pos(background[level][3])
        created = False
        generate_boxes(level)
    if zombie.actor.colliderect(player.actor):
        dead = True
        sounds.minimize_004.play()
    for enemy in box_enemies:
        if player.actor.colliderect(enemy):
            dead = True


def generate_boxes(level):
    patterns = [
        [(30, 40, 200, 299)],
        [(30, 40, 200, 299), (0, 10, 300, 400)],
        [(30, 40, 200, 299), (0, 10, 300, 350), (20, 30, 350, 400)],
        [(30, 40, 200, 299), (0, 10, 300, 350),
         (20, 30, 350, 400), (20, 30, 400, 500)],
    ]
    for config in patterns[level]:
        create_box_enemy(randint(*config[:2]), randint(*config[2:]))


def create_box_enemy(width, height):
    colors = ["bluebox", "greenbox", "redbox", "yellowbox"]
    enemy = Actor(colors[randint(0, 3)])
    enemy.pos = WIDTH - width, background[level][3] - height
    box_enemies.append(enemy)


def draw_box_enemies():
    for enemy in box_enemies:
        enemy.draw()


def move_box_enemies():
    for enemy in box_enemies:
        enemy.x -= 3


def on_key_down(key):
    global dead, won
    if menu_active:
        return
    if key == keys.UP or key == keys.W or key == keys.SPACE:
        player.jump()
    elif key == keys.D or key == keys.RIGHT:
        player.move(50)
    elif key == keys.A or key == keys.LEFT:
        player.move(-50)
    elif key == keys.R and dead:
        restart_game()


def on_key_up(key):
    if key == keys.D or key == keys.A:
        player.stop()


def on_mouse_down(pos):
    global menu_active, music_on
    if not menu_active:
        return
    if menu_buttons["start"].collidepoint(pos):
        start_game()
    elif menu_buttons["music"].collidepoint(pos):
        music_on = not music_on
        if music_on:
            music.play("theme")
        else:
            music.stop()
    elif menu_buttons["exit"].collidepoint(pos):
        exit()


def start_game():
    global menu_active, level, box_enemies, dead, won
    menu_active = False
    level = 0
    player.reset()
    zombie.reset_pos(background[level][3])
    box_enemies.clear()
    dead = False
    won = False
    if music_on:
        music.play("theme")


def restart_game():
    start_game()


TITLE = "Kodland Game"
pgzrun.go()
