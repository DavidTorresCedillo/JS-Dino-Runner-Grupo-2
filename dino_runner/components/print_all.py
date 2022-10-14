class Print_All:
    def __init__(self) -> None:
        pass

    def printall(self,screen,opcion,posX,posY,contenido):
        if opcion == 0:
            text = contenido
            text_rect = text.get_rect()
            text_rect.center = (posX,posY)
            screen.blit(text,text_rect)
        elif opcion == 1:
            self.image = contenido
            self.img_rect = self.image.get_rect()
            self.img_rect.x=posX
            self.img_rect.y=posY
            screen.blit(self.image,(self.img_rect.x,self.img_rect.y))
        else:
            img_rect= contenido.get_rect()
            img_rect.center=(posX,posY)
            screen.blit(contenido,img_rect)