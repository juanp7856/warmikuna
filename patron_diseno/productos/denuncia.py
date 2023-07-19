from abc import abstractmethod, ABC

class DenunciaA(ABC):

    @abstractmethod
    def guardarDenuncia(self, user, descripcion, denunciado, fecha, id_anonimo,departamento):        
        pass

    @abstractmethod
    def guardarImagenes(self, imagenes):
        pass