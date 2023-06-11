from abc import ABC, abstractmethod


class FabricaAbstractaDenuncia(ABC):

    @abstractmethod
    def crearDenunciaAcoso():
        pass

    @abstractmethod
    def crearDenunciaAbuso():
        pass

    @abstractmethod
    def crearDenunciaMaltrato():
        pass