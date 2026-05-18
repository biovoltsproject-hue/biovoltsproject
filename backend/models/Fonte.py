class Fonte:
    def __init__(self, voltagem, corrente):
        self.voltagem = voltagem
        self.corrente = corrente

    @property
    def potencia(self):
        """Potência em Watts (P = V × I)."""
        return self.voltagem * self.corrente

    def __repr__(self):
        return f"Fonte(voltagem={self.voltagem}V, corrente={self.corrente}A, potencia={self.potencia}W)"