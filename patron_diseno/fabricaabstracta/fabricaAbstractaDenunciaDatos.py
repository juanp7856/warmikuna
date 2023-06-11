from patron_diseno.fabricaabstracta.fabricaAbstractaDenuncia import FabricaAbstractaDenuncia
from patron_diseno.productos.denunciaAbusoDatos import denunciaAbusoDatos
from patron_diseno.productos.denunciaAcosoDatos import denunciaAcosoDatos
from patron_diseno.productos.denunciaMaltratoDatos import denunciaMaltratoDatos

class FabricaDenunciaDatos(FabricaAbstractaDenuncia):

    def crearDenunciaAcoso(self):
        return denunciaAcosoDatos()

    def crearDenunciaAbuso(self):
        return denunciaAbusoDatos()

    def crearDenunciaMaltrato(self):
        return denunciaMaltratoDatos()