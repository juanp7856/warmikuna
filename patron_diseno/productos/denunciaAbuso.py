

from patron_diseno.productos.denuncia import DenunciaA


class denunciaAbuso(DenunciaA):
    def __init__(self):
        self.motivo = 'Abuso'


    def guardarDenuncia(self, user, descripcion, denunciado, fecha, id_anonimo):
        return super().guardarDenuncia(user, descripcion, denunciado, fecha, id_anonimo)
    
    def guardarImagenes(self, imagenes):
        return super().guardarImagenes(imagenes)
