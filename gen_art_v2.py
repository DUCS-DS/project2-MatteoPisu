import random, math, pygame

def radians(degrees):
    return math.pi / 180 * degrees

def blue(scale=0.8):
    assert 0 <= scale <= 1, f"scale must be between 0 and 1 inclusive, not {scale}"
    num = int(scale * 255)
    return (num // 2, 2 * num // 3, num)

class Node:
    def __init__(self, x, y, speed, angle):
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.dx = math.sin(self.angle) * self.speed
        self.dy = math.cos(self.angle) * self.speed

    def move(self):
        self.x += self.dx
        self.y += self.dy

    def reflect(self):
        if self.x > winwidth - node_radius:
            self.x = 2 * (winwidth - node_radius) - self.x
            self.angle = -self.angle
        elif self.x < node_radius:
            self.x = 2 * node_radius - self.x
            self.angle = -self.angle
        if self.y > winheight - node_radius:
            self.y = 2 * (winheight - node_radius) - self.y
            self.angle = math.pi - self.angle
        elif self.y < node_radius:
            self.y = 2 * node_radius - self.y
            self.angle = math.pi - self.angle
        self.dx = math.sin(self.angle) * self.speed
        self.dy = math.cos(self.angle) * self.speed

winwidth, winheight = 800, 600
background = (5, 5, 5)
num_nodes, node_radius, thresh = 400, 0, 1800

screen = pygame.display.set_mode((winwidth, winheight))
clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Optimized Triangles")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.KEYDOWN])

nodes = [Node(random.randint(0, winwidth), random.randint(0, winheight),
              random.randint(150, 200) / 600, radians(random.randint(0, 359)))
         for _ in range(num_nodes)]

quit = False
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            quit = True
            break
    if quit:
        break

    screen.fill(background)
    for node in nodes:
        node.move()
        node.reflect()
        pygame.draw.circle(screen, blue(), (int(node.x), int(node.y)), node_radius)

    nodes.sort(key=lambda n: n.x)
    for i, node1 in enumerate(nodes):
        x1, y1 = node1.x, node1.y
        for node2 in nodes[i + 1:]:
            if node2.x - x1 > math.sqrt(thresh):
                break
            x2, y2 = node2.x, node2.y
            d_squared = (x1 - x2) ** 2 + (y1 - y2) ** 2
            if d_squared < thresh:
                pygame.draw.aaline(screen, blue((thresh - d_squared) / thresh), (x1, y1), (x2, y2))

    clock.tick(60)
    pygame.display.flip()
    print(clock.get_fps())

pygame.quit()
