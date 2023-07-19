import uuid
from patron_diseno.productos.denunciaMaltrato import denunciaMaltrato

from warmikuna_app.models import Denuncia, Imagen

class denunciaMaltratoAnonimo(denunciaMaltrato):

    def __init__(self):
        self.id_anonimo = None
        super().__init__()

    def crearID(self):
        self.id_anonimo = str(uuid.uuid4())

    def getID(self):
        return self.id_anonimo

    def guardarDenuncia(self, user, descripcion, denunciado, fecha,departamento):
        denuncia = Denuncia(descripcion=descripcion,denunciado=denunciado,fecha=fecha,motivo=self.motivo, id_anonimo=self.id_anonimo,departamento=departamento)
        denuncia.save()

        return denuncia
    
    def guardarImagenes(self, imagenes, denuncia):
        if imagenes is not None:
            tamano_max = 5
            MEGABYTE = 1024 * 1024

            for i in imagenes:
                if i.size > tamano_max * MEGABYTE:
                    return 'Excede'
                
                nuevaImagen = Imagen(denuncia=denuncia, imagen=i)
                nuevaImagen.save()