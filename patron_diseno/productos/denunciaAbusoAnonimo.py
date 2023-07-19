import uuid
from patron_diseno.productos.denunciaAbuso import denunciaAbuso
from warmikuna_app.models import Denuncia, Imagen


class denunciaAbusoAnonimo(denunciaAbuso):
    def __init__(self):
        super().__init__()
        self.id_anonimo = None

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