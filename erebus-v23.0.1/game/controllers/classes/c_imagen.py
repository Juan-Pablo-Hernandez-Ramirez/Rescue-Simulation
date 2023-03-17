class imagen_ref:

    ## definicion de las propiedades de la clase y asignación de valores por omisión
    def __init__(self, imagen, tipo, camara, color, nominacion):
        self.imagen = imagen
        self.tipo   = tipo
        self.camara = camara
        self.color  = color
        self.nomim  = nominacion


    # Definición de metodos de asignación para las propiedades de la clase
    def setNombre(self, imagen):
        self.imagen   = imagen

    def setTipo  (self, tipo):
        self.tipo     = tipo

    def setCamara(self, camara):
        self.camara   = camara

    def setColor (self, color):
        self.color    = color

    def setNomim (self, nominacion):
        self.nomim    = nominacion


    # Definción del metodo que ejecuta la operación y guarda la operación y resultado a la memoria
    def getImagen(self):
        return self.imagen

    def getTipo(self):
        return self.tipo

    def getCamara(self):
        return self.camara

    def getColor(self):
        return self.color

    def getNomim(self):
        return self.nominacion