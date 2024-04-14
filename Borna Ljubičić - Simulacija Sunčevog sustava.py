import matplotlib.pyplot as plt
import pygame
import math
import time
pygame.init()

WIDTH, HEIGHT =  1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

bijelo = (255, 255, 255)
font = pygame.font.Font(None, 50)

#slike planeta
SUNCE = pygame.image.load("sunce.png").convert_alpha()
MERKUR = pygame.image.load("merkur.png").convert_alpha()
VENERA = pygame.image.load("venera.png").convert_alpha()
ZEMLJA = pygame.image.load("zemlja.png").convert_alpha()
MARS = pygame.image.load("mars.png").convert_alpha()
JUPITER = pygame.image.load("jupiter.png").convert_alpha()
SATURN = pygame.image.load("saturn.png").convert_alpha()
URAN = pygame.image.load("uran.png").convert_alpha()
NEPTUN = pygame.image.load("neptun.png").convert_alpha()


#klasa za izradu planeta
class Planet:
	AU = 149.6e6 * 1000 #astronomska jedinica -> puta 1000 kako bi iz kilometara dobili metre
	G = 6.67428e-11 #gravitacijska konstanta
	SCALE = 200 / AU #broj pikesla po astronomskoj jedinici
	TIMESTEP = 3600*24 #1 dan

	def __init__(self, x, y, radius, slika, masa):
		self.x = x
		self.y = y
		self.radius = radius * 3.5
		self.slika = slika
		self.masa = masa

		self.orbit = []
		self.sun = False
		self.distance_to_sun = 0

		self.x_vel = 0
		self.y_vel = 0

	def draw(self, win): 						#funkcija za crtanje planeta i prilagodbu pozicija prema SCALE-u
		x = self.x * self.SCALE + WIDTH / 2
		y = self.y * self.SCALE + HEIGHT / 2
  
		slika = pygame.transform.scale(self.slika, (self.radius,self.radius)).convert_alpha()

		if len(self.orbit) > 2:
			updated_points = []
			for point in self.orbit:
				x, y = point
				x = x * self.SCALE + WIDTH / 2
				y = y * self.SCALE + HEIGHT / 2
				updated_points.append((x, y))

			pygame.draw.lines(win, bijelo, False, updated_points, 1)

		slika_rect = slika.get_rect(center=(x,y))
		WIN.blit(slika, slika_rect)
		

	def privlačnost(self, drugi): 				#funkcija za gravitacijsku silu
		drugi_x, drugi_y = drugi.x, drugi.y
		udaljenost_x = drugi_x - self.x
		udaljenost_y = drugi_y - self.y
		udaljenost = math.sqrt(udaljenost_x ** 2 + udaljenost_y ** 2)

		if drugi.sun:
			self.distance_to_sun = udaljenost

		sila = self.G * self.masa * drugi.masa / udaljenost**2
		theta = math.atan2(udaljenost_y, udaljenost_x)
		sila_x = math.cos(theta) * sila
		sila_y = math.sin(theta) * sila
		return sila_x, sila_y

	def update_position(self, planeti): 			#funkcija za updateanje pozicija na način da se računaju X i Y komponente obodne brzine
		total_fx = total_fy = 0
		for planet in planeti:
			if self == planet:
				continue

			fx, fy = self.privlačnost(planet)
			total_fx += fx
			total_fy += fy

		self.x_vel += total_fx / self.masa * self.TIMESTEP
		self.y_vel += total_fy / self.masa * self.TIMESTEP

		self.x += self.x_vel * self.TIMESTEP
		self.y += self.y_vel * self.TIMESTEP
		self.orbit.append((self.x, self.y))



udaljenost_zemlja = []
vremena = []
def main():							#glavna funkcija za prikaz orbita
	global udaljenost_zemlja
	global vremena
	global camera_offset_x
	run = True
	clock = pygame.time.Clock()

	sunce = Planet(0, 0, 30, SUNCE, 1.98892 * 10**30)
	sunce.sun = True

	#podatci o svim planetima i njihovim pripadnim obodnim brzinama
	merkur = Planet(-0.387 * Planet.AU, 0, 8, MERKUR, 3.30 * 10**23)
	merkur.y_vel = 47.87 * 1000

	venera = Planet(-0.723 * Planet.AU, 0, 14, VENERA, 4.8685 * 10**24)
	venera.y_vel = 35.02 * 1000

	zemlja = Planet(-1 * Planet.AU, 0, 16, ZEMLJA, 5.9742 * 10**24)
	zemlja.y_vel = 29.78 * 1000 

	mars = Planet(-1.524 * Planet.AU, 0, 12, MARS, 6.39 * 10**23)
	mars.y_vel = 24.07 * 1000

	jupiter = Planet(-5.205 * Planet.AU, 0, 20, JUPITER, 1898 * 10**24)
	jupiter.y_vel = 13.07 * 1000
 
	saturn = Planet(-9.582 * Planet.AU, 0, 18, SATURN, 568 * 10**24)
	saturn.y_vel = 9.69 * 1000
 
	uran = Planet(-19.201 * Planet.AU, 0, 16, URAN, 86.8 * 10**24)
	uran.y_vel = 6.81 * 1000

	neptun = Planet(-30.047 * Planet.AU, 0, 16, NEPTUN, 102 * 10**24)
	neptun.y_vel = 5.43 * 1000

	planeti = [sunce, merkur, venera, zemlja, mars, jupiter, saturn, uran, neptun]

	time1 = time.time()
	omjer = 6.1/31538000 			#omjer vremena u simulaciji i pravog vremena
 	
	while run:
		clock.tick(60)
		WIN.fill((0, 0, 0))
  
     
		for event in pygame.event.get():			#kad se zatvori prozor pygame-a pokaže se graf
			if event.type == pygame.QUIT:
				run = False
				graf()
		t1 = 0
		keys = pygame.key.get_pressed()						#provjera je li pritisnut SPACEBAR da se promijeni SCALE simulacije
		if keys[pygame.K_SPACE] and time.time()-t1 > 2.5:
			t1 =time.time()
			promjeni_veličinu()
			

		for planet in planeti:
			planet.update_position(planeti)
			udaljenost_zemlja.append(zemlja.distance_to_sun/Planet.AU)
			time2 = (time.time()-time1)/omjer		#pretvorba u sekunde
			time2 = time2/2628000 					#pretvorba u mjesece
			vremena.append(time2)
			planet.draw(WIN)

		pygame.display.update()

	pygame.quit()

brojac = 0
def promjeni_veličinu():  #funkcija za promjenu veličine kako bi se mogli vidjeti daljnji planeti
    global brojac
    if brojac%2 ==0:
        Planet.SCALE = 15/Planet.AU
        brojac +=1
    else:
        Planet.SCALE = 200/Planet.AU
        brojac += 1

def graf():					#funkcija za crtanje x/t grafa -> udaljenost zemlje u AU po mjesecima
    global udaljenost_zemlja
    global vremena
    udaljenost_zemlja.pop(0)
    vremena.pop(0)
    plt.plot(vremena, udaljenost_zemlja)
    plt.xlabel("vrijeme / mjeseci")
    plt.ylabel("udaljenost / 149.6*10^6 km")
    plt.axis((0,24,0.99,1.01))
    plt.show()


main()