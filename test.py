import pygame
import sys

# เริ่มต้น pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# โหลดรูป
image = pygame.image.load("img/event_sukuna.png").convert_alpha()

# ปรับตำแหน่งให้อยู่กลางจอ
image_rect = image.get_rect(center=(400, 300))

# เริ่มที่ alpha 0 (มองไม่เห็น)
alpha = 0
image.set_alpha(alpha)

# กำหนดสถานะ
fading_in = True
fading_out = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30, 30, 30))  # สีพื้นหลังเข้มๆ

    if fading_in:
        alpha += 3  # เพิ่มทีละนิด
        if alpha >= 255:
            alpha = 255
            fading_in = False
            fading_out = True  # พอ fade in เสร็จเริ่ม fade out ต่อ
    elif fading_out:
        alpha -= 3
        if alpha <= 0:
            alpha = 0
            fading_out = False  # จบการ fade

    image.set_alpha(alpha)
    screen.blit(image, image_rect)

    pygame.display.update()
    clock.tick(60)
