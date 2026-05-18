# sensor_backend.py
import time
import threading
import queue

# Bibliotecas para o Hardware (Você precisará instalar: pip install adafruit-circuitpython-ads1x15)
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

class BioVoltsBackend:
    def __init__(self, data_queue):
        self.data_queue = data_queue
        self.running = False
        self.hardware_ready = False
        
        # 1. Inicializa o barramento I2C e o conversor ADS1115
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.ads = ADS.ADS1115(i2c)
            
            # 2. Define onde os sensores estão plugados no ADS1115
            # Vamos assumir: Sensor de Tensão no pino A0 | Sensor de Corrente no pino A1
            self.chan_voltage = AnalogIn(self.ads, ADS.P0)
            self.chan_current = AnalogIn(self.ads, ADS.P1)
            
            self.hardware_ready = True
            print("[SISTEMA] Sensores I2C conectados com sucesso.")
        except Exception as e:
            print(f"[ERRO] Falha ao comunicar com o ADS1115: {e}")
            print("[SISTEMA] Rodando em modo de falha (bateria zerada).")

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False

    def _run_loop(self):
        """Loop contínuo de leitura do hardware via I2C."""
        while self.running:
            if self.hardware_ready:
                # 1. Lê a voltagem bruta do ADS1115 (A0 e A1)
                raw_voltage = self.chan_voltage.voltage
                raw_current = self.chan_current.voltage
                
                # 2. Conversão da Tensão (Módulo 0-25V)
                # Multiplica por 5 devido ao divisor de tensão do módulo
                real_voltage = raw_voltage * 5.0 
                
                # 3. Conversão da Corrente (ACS712)
                # Tensão de repouso é ~2.5V. Subtraímos 2.5 para achar a diferença.
                # ALERTA: Mude a sensibilidade abaixo de acordo com seu módulo:
                # 5A = 0.185 | 20A = 0.100 | 30A = 0.066
                sensibilidade = 0.100 
                real_current = (raw_current - 2.5) / sensibilidade
                
                # Filtro de ruído: o ACS712 costuma flutuar um pouco perto do zero
                if abs(real_current) < 0.05: 
                    real_current = 0.0
                # 4. Configurações da Bateria: Chumbo-Ácido 12V 7Ah
                tensao_min = 10.5  # 0% - Nunca deixe cair abaixo disso para não danificar
                tensao_max = 12.7  # 100% - Tensão nominal de bateria cheia em repouso
                capacidade_ah = 7.0 # Capacidade total da sua bateria

                # Cálculo da Porcentagem da Bateria
                battery_pct = ((real_voltage - tensao_min) / (tensao_max - tensao_min)) * 100
                battery_pct = max(0.0, min(100.0, battery_pct)) # Trava estritamente entre 0 e 100%
                
                # 5. Cálculo do Tempo Restante para Carga Total (em minutos)
                tempo_minutos = 0
                if real_current > 0.1: # Só calcula se estiver carregando de verdade
                    status = "CARREGANDO PELO MODULO SOLAR"
                    # Descobre quantos Ah faltam para encher a bateria
                    ah_faltantes = capacidade_ah * (1.0 - (battery_pct / 100.0))
                    # Tempo (horas) = Ah / Corrente. Multiplicamos por 60 para ter minutos
                    tempo_horas = ah_faltantes / real_current
                    tempo_minutos = int(tempo_horas * 60)
                    
                elif real_current < -0.1:
                    status = "EM USO - DESCARREGANDO"
                else:
                    status = "SISTEMA EM REPOUSO"
                
                payload = {
                    "battery": battery_pct,
                    "status": status,
                    "time_to_full": tempo_minutos,
                    "raw_v": real_voltage,
                    "raw_i": real_current
                }
            # Envia para a Interface
            while not self.data_queue.empty():
                try: self.data_queue.get_nowait()
                except: pass
            
            self.data_queue.put(payload)
            time.sleep(1) # Atualiza a cada 1 segundo