import matplotlib.pyplot as plt
import pygame
import math
import time
import sys
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

#normalne mase planeta
mSu = 1.98892 * 10**30
mMe = 3.30 * 10**23
mV = 4.8685 * 10**24
mZ = 5.9742 * 10**24
mMa = 6.39 * 10**23
mJ = 1898 * 10**24
mSa = 568 * 10**24
mU = 86.8 * 10**24
mN = 102 * 10**24



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

class Gumb: #Klasa za gumb
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color = base_color
        self.hovering_color = hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center = (self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center = (self.x_pos, self.y_pos))

    def update(self,screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self,position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False
    
    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)
    
    
    
udaljenost_merkur = []
udaljenost_venera = []
udaljenost_zemlja = []
udaljenost_mars = []
udaljenost_jupiter = []
udaljenost_saturn = []
udaljenost_uran = []
udaljenost_neptun = []
vremena = []

def main():							#glavna funkcija za prikaz orbita
	global mSu
	global mMe
	global mV
	global mZ
	global mMa
	global mJ
	global mSa
	global mU
	global mN
	
	global udaljenost_merkur
	global udaljenost_venera
	global udaljenost_zemlja
	global udaljenost_mars
	global udaljenost_jupiter
	global udaljenost_saturn
	global udaljenost_uran
	global udaljenost_neptun

	global vremena

	run = True
	clock = pygame.time.Clock()

	sunce = Planet(0, 0, 30, SUNCE, mSu)
	sunce.sun = True

	#podatci o svim planetima i njihovim pripadnim obodnim brzinama
	merkur = Planet(-0.387 * Planet.AU, 0, 8, MERKUR, mMe)
	merkur.y_vel = 47.87 * 1000

	venera = Planet(-0.723 * Planet.AU, 0, 14, VENERA, mV)
	venera.y_vel = 35.02 * 1000

	zemlja = Planet(-1 * Planet.AU, 0, 16, ZEMLJA, mZ)
	zemlja.y_vel = 29.78 * 1000 

	mars = Planet(-1.524 * Planet.AU, 0, 12, MARS, mMa)
	mars.y_vel = 24.07 * 1000

	jupiter = Planet(-5.205 * Planet.AU, 0, 20, JUPITER, mJ)
	jupiter.y_vel = 13.07 * 1000
 
	saturn = Planet(-9.582 * Planet.AU, 0, 18, SATURN, mSa)
	saturn.y_vel = 9.69 * 1000
 
	uran = Planet(-19.201 * Planet.AU, 0, 16, URAN, mU)
	uran.y_vel = 6.81 * 1000

	neptun = Planet(-30.047 * Planet.AU, 0, 16, NEPTUN, mN)
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
			time.sleep(0.1)
			promjeni_veličinu()
		elif keys[pygame.K_ESCAPE]:
			menu_1()
			

		for planet in planeti:
			planet.update_position(planeti)

            
			udaljenost_merkur.append(merkur.distance_to_sun/Planet.AU)
			udaljenost_venera.append(venera.distance_to_sun/Planet.AU)
			udaljenost_zemlja.append(zemlja.distance_to_sun/Planet.AU)
			udaljenost_mars.append(mars.distance_to_sun/Planet.AU)
			udaljenost_jupiter.append(jupiter.distance_to_sun/Planet.AU)
			udaljenost_saturn.append(saturn.distance_to_sun/Planet.AU)
			udaljenost_uran.append(uran.distance_to_sun/Planet.AU)
			udaljenost_neptun.append(neptun.distance_to_sun/Planet.AU)
   
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

def graf():					#funkcija za crtanje x/t grafova -> udaljenost planeta u AU po mjesecima
    global udaljenost_merkur
    global udaljenost_venera
    global udaljenost_zemlja
    global udaljenost_mars
    global udaljenost_jupiter
    global udaljenost_saturn
    global udaljenost_uran
    global udaljenost_neptun
    
    global vremena
    
    figure, axis = plt.subplots(8)
    
    axis[0].plot(vremena,udaljenost_merkur)
    axis[0].set_title("Merkur - udaljenost")
    axis[0].axis((0,max(vremena),0.30, 0.48))
    
    axis[1].plot(vremena,udaljenost_venera)
    axis[1].set_title("Venera - udaljenost")
    axis[1].axis((0,max(vremena),0.71, 0.74))
    
    axis[2].plot(vremena,udaljenost_zemlja)
    axis[2].set_title("Zemlja - udaljenost")
    axis[2].axis((0,max(vremena),0.97, 1.03))
    
    axis[3].plot(vremena,udaljenost_mars)
    axis[3].set_title("Mars - udaljenost")
    axis[3].axis((0,max(vremena),1.37, 1.67))
    
    axis[4].plot(vremena,udaljenost_jupiter)
    axis[4].set_title("Jupiter - udaljenost")
    axis[4].axis((0,max(vremena),4.94, 5.46))
    
    axis[5].plot(vremena,udaljenost_saturn)
    axis[5].set_title("Saturn - udaljenost")
    axis[5].axis((0,max(vremena),9.01, 10.12))
    
    axis[6].plot(vremena,udaljenost_uran)
    axis[6].set_title("Uran - udaljenost")
    axis[6].axis((0,max(vremena), 18.37, 20.11))
    
    axis[7].plot(vremena,udaljenost_neptun)
    axis[7].set_title("Neptun - udaljenost")
    axis[7].axis((0,max(vremena),29.81, 30.33))
    
    plt.show()
    
def menu_1():
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if START.checkForInput(MOUSE_POS):
                    main()

                if PARAMETRI.checkForInput(MOUSE_POS):
                    menu_2()

        WIN.blit(pygame.transform.scale(pygame.image.load("Pozadina.png").convert(), (1000, 1000)), (0,0))

        MOUSE_POS = pygame.mouse.get_pos()


        START = Gumb(pygame.image.load("Pozadina_gumb7.png").convert(), (500, 465),"Simulacija", font, "Black", "Gray")
        PARAMETRI = Gumb(pygame.image.load("Pozadina_gumb7.png").convert(), (500, 535),"Parametri", font, "Black", "Gray")
        
        PARAMETRI.changeColor(MOUSE_POS)
        PARAMETRI.update(WIN)
        START.changeColor(MOUSE_POS)
        START.update(WIN)    

        pygame.display.update()

def menu_2(): 	#menu za postavljanje novih masa planeta
    global mSu
    global mMe
    global mV
    global mZ
    global mMa
    global mJ
    global mSa
    global mU
    global mN
    
    
    Sunce = "1"
    input_box_1 = pygame.Rect(100,100,150,40)
    
    Merkur = "1"
    input_box_2 = pygame.Rect(100,200,150,40)
    
    Venera = "1"
    input_box_3 = pygame.Rect(100,300,150,40)
    
    Zemlja = "1"
    input_box_4 = pygame.Rect(100,400,150,40)
    
    Mars = "1"
    input_box_5 = pygame.Rect(100,500,150,40)
    
    Jupiter = "1"
    input_box_6 = pygame.Rect(100,600,150,40)
    
    Saturn = "1"
    input_box_7 = pygame.Rect(100,700,150,40)
    
    Uran = "1"
    input_box_8 = pygame.Rect(100,800,150,40)
    
    Neptun = "1"
    input_box_9 = pygame.Rect(100,900,150,40)
    
    active1 = False
    active2 = False
    active3 = False
    active4 = False
    active5 = False
    active6 = False
    active7 = False
    active8 = False
    active9 = False
    
    while True:
        MOUSE = pygame.mouse.get_pos()
        

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:	#definiranje gumba kojim se prenose nove mase planeta
                if START.checkForInput(MOUSE):
                    mSu = mSu * int(Sunce)
                    mMe = mMe * int(Merkur)
                    mV = mV * int(Venera)
                    mZ = mZ * int(Zemlja)
                    mMa = mMa * int(Mars)
                    mJ = mJ * int(Jupiter)
                    mSa = mSa * int(Saturn)
                    mU = mU * int(Uran)
                    mN = mN * int(Neptun)
                    main()
                
                if RESET.checkForInput(MOUSE):		#reset gumb
                    Sunce = "1"
                    Merkur = "1"
                    Venera = "1"
                    Zemlja = "1"
                    Mars = "1"
                    Jupiter = "1"
                    Saturn = "1"
                    Uran = "1"
                    Neptun = "1"
                    
                    
                if input_box_1.collidepoint(event.pos):			#provjeravanje koji je textbox aktivan
                    active1 = True
                    active2 = False
                    active3 = False
                    active4 = False
                    active5 = False
                    active6 = False
                    active7 = False
                    active8 = False
                    active9 = False
                elif input_box_2.collidepoint(event.pos):
                    active2 = True
                    active1 = False
                    active3 = False
                    active4 = False
                    active5 = False
                    active6 = False
                    active7 = False
                    active8 = False
                    active9 = False
                elif input_box_3.collidepoint(event.pos):
                    active3 = True
                    active2 = False
                    active1 = False
                    active4 = False
                    active5 = False
                    active6 = False
                    active7 = False
                    active8 = False
                    active9 = False
                elif input_box_4.collidepoint(event.pos):
                    active4 = True
                    active2 = False
                    active3 = False
                    active1 = False
                    active5 = False
                    active6 = False
                    active7 = False
                    active8 = False
                    active9 = False
                elif input_box_5.collidepoint(event.pos):
                    active5 = True
                    active2 = False
                    active3 = False
                    active4 = False
                    active1 = False
                    active6 = False
                    active7 = False
                    active8 = False
                    active9 = False
                elif input_box_6.collidepoint(event.pos):
                    active6 = True
                    active2 = False
                    active3 = False
                    active4 = False
                    active5 = False
                    active1 = False
                    active7 = False
                    active8 = False
                    active9 = False
                elif input_box_7.collidepoint(event.pos):
                    active7 = True
                    active2 = False
                    active3 = False
                    active4 = False
                    active5 = False
                    active6 = False
                    active1 = False
                    active8 = False
                    active9 = False
                elif input_box_8.collidepoint(event.pos):
                    active8 = True
                    active2 = False
                    active3 = False
                    active4 = False
                    active5 = False
                    active6 = False
                    active7 = False
                    active1 = False
                    active9 = False
                elif input_box_9.collidepoint(event.pos):
                    active9 = True
                    active2 = False
                    active3 = False
                    active4 = False
                    active5 = False
                    active6 = False
                    active7 = False
                    active8 = False
                    active1 = False
                else:
                    active1 = False
                    active2 = False
                    active3 = False
                    active4 = False
                    active5 = False
                    active6 = False
                    active7 = False
                    active8 = False
                    active9 = False
            
            if event.type == pygame.KEYDOWN:					#upisivanje u aktivan textbox
                if active1:
                    if event.key == pygame.K_BACKSPACE:
                        Sunce =  Sunce[0:-1]
                    else:
                        if len(Sunce) <= 10:
                            Sunce += event.unicode
                if active2:
                    if event.key == pygame.K_BACKSPACE:
                        Merkur =  Merkur[0:-1]
                    else:
                        if len(Merkur) <= 10:
                            Merkur += event.unicode
                if active3:
                    if event.key == pygame.K_BACKSPACE:
                        Venera =  Venera[0:-1]
                    else:
                        if len(Venera) <= 10:
                            Venera += event.unicode
                if active4:
                    if event.key == pygame.K_BACKSPACE:
                        Zemlja =  Zemlja[0:-1]
                    else:
                        if len(Zemlja) <= 10:
                            Zemlja += event.unicode
                if active5:
                    if event.key == pygame.K_BACKSPACE:
                        Mars =  Mars[0:-1]
                    else:
                        if len(Mars) <= 10:
                            Mars += event.unicode
                if active6:
                    if event.key == pygame.K_BACKSPACE:
                        Jupiter =  Jupiter[0:-1]
                    else:
                        if len(Jupiter) <= 10:
                            Jupiter += event.unicode
                if active7:
                    if event.key == pygame.K_BACKSPACE:
                        Saturn =  Saturn[0:-1]
                    else:
                        if len(Saturn) <= 10:
                            Saturn += event.unicode
                if active8:
                    if event.key == pygame.K_BACKSPACE:
                        Uran =  Uran[0:-1]
                    else:
                        if len(Uran) <= 10:
                            Uran += event.unicode
                if active9:
                    if event.key == pygame.K_BACKSPACE:
                        Neptun=  Neptun[0:-1]
                    else:
                        if len(Neptun) <= 10:
                            Neptun += event.unicode
        
        WIN.blit(pygame.transform.scale(pygame.image.load("Pozadina 2.png").convert(), (1000, 1000)), (0,0))
        START = Gumb(pygame.image.load("Pozadina_gumb7.png").convert(), (800, 465),"Pokerni", font, "Black", "Gray")
        RESET = Gumb(pygame.image.load("Pozadina_gumb7.png").convert(), (800, 535),"Reset", font, "Black", "Gray")
        
        
        for gumb in [START, RESET]:
            gumb.changeColor(MOUSE)
            gumb.update(WIN)
            
        text_srurface1 = font.render(Sunce,True, "Black")					#prikaz svih textboxova
        WIN.blit(text_srurface1, (input_box_1.x +5,input_box_1.y +5))
        pygame.draw.rect(WIN,"Black",input_box_1, 2)
        tekst = font.render("SUNCE", True, "Black")
        tekst_rect = tekst.get_rect(topleft=(100,50))
        WIN.blit(tekst, tekst_rect)
        
        text_srurface2 = font.render(Merkur,True, "Black")
        WIN.blit(text_srurface2, (input_box_2.x +5,input_box_2.y +5))
        pygame.draw.rect(WIN,"Black",input_box_2, 2)
        tekst = font.render("MERKUR", True, "Black")
        tekst_rect = tekst.get_rect(topleft=(100,150))
        WIN.blit(tekst, tekst_rect)
        
        text_srurface3 = font.render(Venera,True, "Black")
        WIN.blit(text_srurface3, (input_box_3.x +5,input_box_3.y +5))
        pygame.draw.rect(WIN,"Black",input_box_3, 2)
        tekst = font.render("VENERA", True, "Black")
        tekst_rect = tekst.get_rect(topleft=(100,250))
        WIN.blit(tekst, tekst_rect)
        
        text_srurface4 = font.render(Zemlja,True, "Black")
        WIN.blit(text_srurface4, (input_box_4.x +5,input_box_4.y +5))
        pygame.draw.rect(WIN,"Black",input_box_4, 2)
        tekst = font.render("ZEMLJA", True, "Black")
        tekst_rect = tekst.get_rect(topleft=(100,350))
        WIN.blit(tekst, tekst_rect)
        
        text_srurface5 = font.render(Mars,True, "Black")
        WIN.blit(text_srurface5, (input_box_5.x +5,input_box_5.y +5))
        pygame.draw.rect(WIN,"Black",input_box_5, 2)
        tekst = font.render("MARS", True, "Black")
        tekst_rect = tekst.get_rect(topleft=(100,450))
        WIN.blit(tekst, tekst_rect)
        
        text_srurface6 = font.render(Jupiter,True, "Black")
        WIN.blit(text_srurface6, (input_box_6.x +5,input_box_6.y +5))
        pygame.draw.rect(WIN,"Black",input_box_6, 2)
        tekst = font.render("JUPITER", True, "Black")
        tekst_rect = tekst.get_rect(topleft=(100,550))
        WIN.blit(tekst, tekst_rect)
        
        text_srurface7 = font.render(Saturn,True, "Black")
        WIN.blit(text_srurface7, (input_box_7.x +5,input_box_7.y +5))
        pygame.draw.rect(WIN,"Black",input_box_7, 2)
        tekst = font.render("SATURN", True, "Black")
        tekst_rect = tekst.get_rect(topleft=(100,650))
        WIN.blit(tekst, tekst_rect)
        
        text_srurface8 = font.render(Uran,True, "Black")
        WIN.blit(text_srurface8, (input_box_8.x +5,input_box_8.y +5))
        pygame.draw.rect(WIN,"Black",input_box_8, 2)
        tekst = font.render("URAN", True, "Black")
        tekst_rect = tekst.get_rect(topleft=(100,750))
        WIN.blit(tekst, tekst_rect)
        
        text_srurface9 = font.render(Neptun,True, "Black")
        WIN.blit(text_srurface9, (input_box_9.x +5,input_box_9.y +5))
        pygame.draw.rect(WIN,"Black",input_box_9, 2)
        tekst = font.render("NEPTUN", True, "Black")
        tekst_rect = tekst.get_rect(topleft=(100,850))
        WIN.blit(tekst, tekst_rect)
        
        pygame.display.update()
                
                

menu_1()
