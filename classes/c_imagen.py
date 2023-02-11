class imagen_ref:
    ## definicion de las propiedades de la clase y asignación de valores por omisión
    def __init__(self, im, ti, ca, co, no):
        self.imagen = im
        self.tipo = ti
        self.camara = ca
        self.color = co
        self.nomim = no

    ## Definición de metodos de asignación para las propiedades de la clase
    def setNombre(self, im):
        self.imagen = im

    def setTipo(self, ti):
        self.tipo = ti

    def setCamara(self, ca):
        self.camara = ca

    def setColor(self, co):
        self.color = co

    def setNomim(self, no):
        self.nomim = no

    ##definción del metodo que ejecuta la operación y guarda la operación y resultado a la memoria
    def getImagen(self):
        return self.imagen

    def getTipo(self):
        return self.tipo

    def getCamara(self):
        return self.camara

    def getColor(self):
        return self.color

    def getNomim(self):
        return self.nomim