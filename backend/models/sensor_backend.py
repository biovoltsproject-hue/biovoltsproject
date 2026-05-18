# sensor_backend.py — Modo simulado (mock) para testes sem hardware
import time
import threading
import queue
import math
import random


class BioVoltsBackend:
    def __init__(self, data_queue):
        self.data_queue = data_queue
        self.running = False
        print("[SISTEMA] Rodando em modo SIMULADO (mock).")

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _run_loop(self):
        """Simula leituras realistas de bateria solar ao longo do tempo."""
        t = 0
        battery = 45.0  # começa em 45%

        while self.running:
            # Simula corrente variando como um painel solar real
            # (sobe de manhã, pico ao meio-dia, cai à tarde)
            corrente_solar = max(0.0, 2.5 * math.sin(t / 60) + random.uniform(-0.1, 0.1))
            corrente_carga  = 0.8  # consumo constante do dispositivo

            corrente_liquida = corrente_solar - corrente_carga

            # Atualiza bateria gradualmente
            battery += corrente_liquida * 0.02
            battery = max(0.0, min(100.0, battery))

            # Tensão simulada com base na porcentagem (12V chumbo-ácido)
            tensao = 10.5 + (battery / 100.0) * 2.2 + random.uniform(-0.05, 0.05)

            # Status e tempo
            if corrente_liquida > 0.1:
                status = "CARREGANDO PELO MODULO SOLAR"
                capacidade_ah = 7.0
                ah_faltantes = capacidade_ah * (1.0 - battery / 100.0)
                tempo_minutos = int((ah_faltantes / corrente_liquida) * 60)
            elif corrente_liquida < -0.1:
                status = "EM USO - DESCARREGANDO"
                tempo_minutos = 0
            else:
                status = "SISTEMA EM REPOUSO"
                tempo_minutos = 0

            payload = {
                "battery": round(battery, 1),
                "status": status,
                "time_to_full": tempo_minutos,
                "raw_v": round(tensao, 2),
                "raw_i": round(corrente_liquida, 3),
            }

            print(
                f"[MOCK] V={tensao:.2f}V  I={corrente_liquida:.3f}A  "
                f"Bat={battery:.1f}%  Status={status}"
            )

            while not self.data_queue.empty():
                try:
                    self.data_queue.get_nowait()
                except Exception:
                    pass

            self.data_queue.put(payload)
            t += 1
            time.sleep(1)