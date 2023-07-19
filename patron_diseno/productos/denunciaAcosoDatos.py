
from patron_diseno.productos.denunciaAcoso import denunciaAcoso
from warmikuna_app.models import Denuncia, Imagen


class denunciaAcosoDatos(denunciaAcoso):
    def __init__(self):
        super().__init__()

    def guardarDenuncia(self, user, descripcion, denunciado, fecha,departamento):
        denuncia = Denuncia(user=user,descripcion=descripcion,denunciado=denunciado,fecha=fecha,motivo=self.motivo,departamento=departamento)
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