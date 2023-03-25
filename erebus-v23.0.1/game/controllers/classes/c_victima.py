class victima:

    ## definicion de las propiedades de la clase y asignación de valores por omisión
    def __init__(self, tipo, valor, camara, posX, posZ):
        self.tipo   = tipo
        self.valor  = valor
        self.camara = camara
        self.posX   = posX
        self.posZ   = posZ

    # Definición de metodos de asignación para las propiedades de la clase
    def setTipo  (self, tipo):
        self.tipo     = tipo
    def setValor (self, valor):
        self.valor    = valor
    def setCamara(self, camara):
        self.camara   = camara
    def setPosX  (self, posX):
        self.posX     = posX
    def setPosZ  (self, posZ):
        self.posZ     = posZ

    # Definción del metodo que ejecuta la operación y guarda la operación y resultado a la memoria
    def getgetTipo(self):
        return self.tipo
    def getValor(self):
        return self.valor
    def getCamara(self):
        return self.camara
    def getPosX(self):
        return self.posX
    def getPosZ(self):
        return self.posZ