KAPASITEETTI = 5
OLETUSKASVATUS = 5


class IntJoukko:
    # tämä metodi on ainoa tapa luoda listoja
    def _luo_lista(self, koko):
        return [0] * koko
    
    def __init__(self, kapasiteetti=None, kasvatuskoko=None):
        self.kapasiteetti = self.tarkista_kapasiteetti(kapasiteetti, KAPASITEETTI)
        self.kasvatuskoko = self.tarkista_kapasiteetti(kasvatuskoko, OLETUSKASVATUS)
        self.ljono = self._luo_lista(self.kapasiteetti)
        self.alkioiden_lkm = 0
    
    def tarkista_kapasiteetti(self, koko, oletus):
        if koko is None:
            return oletus
        if not isinstance(koko, int) or koko < 0:
            raise ValueError("Kapasiteetin tai kasvatuskoon tulee olla positiivinen kokonaisluku.")
        return koko

    def kuuluu(self, luku):
        return luku in self.ljono[:self.alkioiden_lkm]

    def lisaa(self, luku):
        if not self.kuuluu(luku):
            if self.alkioiden_lkm >= len(self.ljono):
                self.kasvata_taulukkoa()
            self.ljono[self.alkioiden_lkm] = luku
            self.alkioiden_lkm += 1
            return True
        return False
    
    def kasvata_taulukkoa(self):
        uusi_ljono = self._luo_lista(len(self.ljono) + self.kasvatuskoko)
        self._kopioi_lista(self.ljono, uusi_ljono)
        self.ljono = uusi_ljono

    def poista(self, luku):
        for i in range(self.alkioiden_lkm):
            if self.ljono[i] == luku:
                self.siirra_vasemmalle(i)
                self.alkioiden_lkm -= 1
                return True
        return False
    
    def siirra_vasemmalle(self, indeksi):
        for i in range(indeksi, self.alkioiden_lkm - 1):
            self.ljono[i] = self.ljono[i + 1]
        self.ljono[self.alkioiden_lkm - 1] = 0

    def _kopioi_lista(self, lahde, kohde):
        for i in range(len(lahde)):
            kohde[i] = lahde[i]

    def mahtavuus(self):
        return self.alkioiden_lkm

    def to_int_list(self):
        return self.ljono[:self.alkioiden_lkm]

    @staticmethod
    def yhdiste(joukko1, joukko2):
        tulos = IntJoukko()
        for luku in joukko1.to_int_list() + joukko2.to_int_list():
            tulos.lisaa(luku)
        return tulos

    @staticmethod
    def leikkaus(joukko1, joukko2):
        tulos = IntJoukko()
        for luku in joukko1.to_int_list():
            if joukko2.kuuluu(luku):
                tulos.lisaa(luku)
        return tulos

    @staticmethod
    def erotus(joukko1, joukko2):
        tulos = IntJoukko()
        for luku in joukko1.to_int_list():
            if not joukko2.kuuluu(luku):
                tulos.lisaa(luku)
        return tulos

    def __str__(self):
        alkiot = ", ".join(map(str, self.to_int_list()))
        return f"{{{alkiot}}}"
