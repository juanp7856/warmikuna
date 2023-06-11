from patron_diseno.fabricaabstracta.fabricaAbstractaDenuncia import FabricaAbstractaDenuncia
from patron_diseno.productos.denunciaAbusoAnonimo import denunciaAbusoAnonimo
from patron_diseno.productos.denunciaAcosoAnonimo import denunciaAcosoAnonimo
from patron_diseno.productos.denunciaMaltratoAnonimo import denunciaMaltratoAnonimo


class FabricaDenunciaAnonima(FabricaAbstractaDenuncia):

    def crearDenunciaAcoso(self):
        return denunciaAcosoAnonimo()

    def crearDenunciaAbuso(self):
        return denunciaAbusoAnonimo()

    def crearDenunciaMaltrato(self):
        return denunciaMaltratoAnonimo()