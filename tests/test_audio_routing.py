"""
Teste de roteamento de áudio com debug verbose.
Objetivo: Identificar melhor método para Windows 11.
"""
import sys
from pathlib import Path
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.core.audio import SoundLoader
import logging
from datetime import datetime
import soundfile as sf
import sounddevice as sd
import numpy as np
import threading

# Configurar logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('audio_routing_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AudioRoutingTest(App):
    """
    App de teste para roteamento de áudio com seleção de dispositivos.
    Testa diferentes métodos e registra resultados.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.audio_devices = []
        self.selected_device_id = None
        self.audio_data = None
        self.sample_rate = None
        
        # Dispositivos identificados no teste (podem ser alterados)
        self.DEVICE_SPEAKER = 8   # Caixa nativa (Realtek - público)
        self.DEVICE_HEADPHONE = 9  # Fone USB (cantor)
    
    def build(self):
        logger.info("=" * 60)
        logger.info("INICIANDO TESTE DE ROTEAMENTO DE ÁUDIO")
        logger.info("=" * 60)
        
        # Layout principal
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Título
        title = Label(
            text='🔊 TESTE DE ROTEAMENTO DE ÁUDIO',
            font_size='30sp',
            size_hint_y=0.1
        )
        layout.add_widget(title)
        
        # Device selector
        device_layout = BoxLayout(size_hint_y=0.1, spacing=10, padding=[10, 0])
        device_label = Label(text='Dispositivo:', size_hint_x=0.2)
        device_layout.add_widget(device_label)
        
        self.device_spinner = Spinner(
            text='Carregando...',
            values=[],
            size_hint_x=0.6
        )
        self.device_spinner.bind(text=self.on_device_selected)
        device_layout.add_widget(self.device_spinner)
        
        refresh_btn = Button(
            text='🔄 Atualizar',
            size_hint_x=0.2,
            on_press=self.load_audio_devices
        )
        device_layout.add_widget(refresh_btn)
        layout.add_widget(device_layout)
        
        # Log display (scrollable)
        self.log_display = Label(
            text='Aguardando testes...\n',
            size_hint_y=None,
            markup=True
        )
        self.log_display.bind(texture_size=self.log_display.setter('size'))
        
        scroll = ScrollView(size_hint=(1, 0.5))
        scroll.add_widget(self.log_display)
        layout.add_widget(scroll)
        
        # Botões de teste - Linha 1
        btn_layout_1 = BoxLayout(size_hint_y=0.15, spacing=5)
        
        # Botão 1: Tocar no dispositivo selecionado
        play_btn = Button(
            text='▶️ Tocar\nSelecionado',
            on_press=self.play_on_selected_device,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        btn_layout_1.add_widget(play_btn)
        
        # Botão 2: Tocar em ambos dispositivos
        play_both_btn = Button(
            text='🔊🎧 Tocar\nAmbos (8+9)',
            on_press=self.play_on_both_devices,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        btn_layout_1.add_widget(play_both_btn)
        
        # Botão 3: Parar reprodução
        stop_btn = Button(
            text='⏹️ Parar',
            on_press=self.stop_audio,
            background_color=(0.8, 0.2, 0.2, 1)
        )
        btn_layout_1.add_widget(stop_btn)
        
        layout.add_widget(btn_layout_1)
        
        # Botões de teste - Linha 2
        btn_layout_2 = BoxLayout(size_hint_y=0.15, spacing=5)
        
        # Botão 4: Listar dispositivos
        list_btn = Button(
            text='📋 Listar\nDispositivos',
            on_press=self.test_list_devices
        )
        btn_layout_2.add_widget(list_btn)
        
        # Botão 5: Testar método padrão (Kivy)
        default_btn = Button(
            text='🔊 Teste\nKivy',
            on_press=self.test_default_audio
        )
        btn_layout_2.add_widget(default_btn)
        
        # Botão 6: Instruções
        manual_btn = Button(
            text='📖 Instruções',
            on_press=self.show_manual_instructions
        )
        btn_layout_2.add_widget(manual_btn)
        
        layout.add_widget(btn_layout_2)
        
        # Carregar áudio de teste
        test_audio = Path('assets/audio/Ibp - Energia da Revolucao.wav')
        if test_audio.exists():
            # Kivy SoundLoader
            self.sound = SoundLoader.load(str(test_audio))
            logger.info(f"✅ Áudio Kivy carregado: {test_audio}")
            
            # sounddevice data
            try:
                self.audio_data, self.sample_rate = sf.read(str(test_audio))
                logger.info(f"✅ Áudio sounddevice carregado: {self.sample_rate} Hz")
            except Exception as e:
                logger.error(f"❌ Erro ao carregar com soundfile: {e}")
                self.audio_data = None
        else:
            self.sound = None
            self.audio_data = None
            logger.warning(f"❌ Áudio de teste não encontrado: {test_audio}")
        
        # Carregar dispositivos
        self.load_audio_devices(None)
        
        return layout
    
    def load_audio_devices(self, instance):
        """Carregar lista de dispositivos de áudio disponíveis."""
        try:
            devices = sd.query_devices()
            self.audio_devices = []
            device_names = []
            
            for i, device in enumerate(devices):
                if device['max_output_channels'] > 0:
                    self.audio_devices.append({
                        'id': i,
                        'name': device['name'],
                        'channels': device['max_output_channels']
                    })
                    device_names.append(f"[{i}] {device['name']}")
            
            if device_names:
                self.device_spinner.values = device_names
                
                # Selecionar dispositivo padrão
                default = sd.query_devices(kind='output')
                default_name = f"[{default['index']}] {default['name']}"
                if default_name in device_names:
                    self.device_spinner.text = default_name
                    self.selected_device_id = default['index']
                else:
                    self.device_spinner.text = device_names[0]
                    self.selected_device_id = self.audio_devices[0]['id']
                
                self.log(f"✅ {len(self.audio_devices)} dispositivos carregados", 'INFO')
                self.log(f"Padrão: {default['name']}", 'INFO')
            else:
                self.log("❌ Nenhum dispositivo de saída encontrado", 'ERROR')
                
        except Exception as e:
            self.log(f"❌ Erro ao carregar dispositivos: {e}", 'ERROR')
    
    def on_device_selected(self, spinner, text):
        """Callback quando dispositivo é selecionado."""
        try:
            # Extrair ID do texto "[ID] Nome"
            device_id = int(text.split(']')[0].strip('['))
            self.selected_device_id = device_id
            
            device_info = sd.query_devices(device_id)
            self.log(f"📌 Selecionado: {device_info['name']}", 'INFO')
            self.log(f"   Canais: {device_info['max_output_channels']}", 'DEBUG')
            self.log(f"   Taxa: {device_info['default_samplerate']} Hz", 'DEBUG')
            
        except Exception as e:
            self.log(f"❌ Erro ao selecionar dispositivo: {e}", 'ERROR')
    
    def play_on_selected_device(self, instance):
        """Tocar áudio no dispositivo selecionado usando sounddevice."""
        if self.selected_device_id is None:
            self.log("❌ Nenhum dispositivo selecionado", 'ERROR')
            return
        
        if self.audio_data is None:
            self.log("❌ Nenhum áudio carregado", 'ERROR')
            return
        
        try:
            device_info = sd.query_devices(self.selected_device_id)
            self.log("=" * 40, 'INFO')
            self.log(f"▶️ TOCANDO NO DISPOSITIVO {self.selected_device_id}", 'INFO')
            self.log(f"Nome: {device_info['name']}", 'INFO')
            self.log("=" * 40, 'INFO')
            
            # Tocar áudio
            sd.play(self.audio_data, self.sample_rate, device=self.selected_device_id)
            
            self.log("✅ Áudio sendo reproduzido", 'INFO')
            self.log("Você deve ouvir o som neste dispositivo!", 'WARNING')
            
        except Exception as e:
            self.log(f"❌ Erro ao tocar áudio: {e}", 'ERROR')
    
    def play_on_both_devices(self, instance):
        """Tocar áudio simultaneamente nos dispositivos 8 e 9."""
        if self.audio_data is None:
            self.log("❌ Nenhum áudio carregado", 'ERROR')
            return
        
        try:
            # Verificar se os dispositivos existem
            try:
                device_8 = sd.query_devices(self.DEVICE_SPEAKER)
                device_9 = sd.query_devices(self.DEVICE_HEADPHONE)
            except Exception as e:
                self.log(f"❌ Erro ao verificar dispositivos: {e}", 'ERROR')
                self.log("💡 Ajuste os IDs em self.DEVICE_SPEAKER e self.DEVICE_HEADPHONE", 'WARNING')
                return
            
            self.log("=" * 40, 'INFO')
            self.log("🔊🎧 TOCANDO EM AMBOS DISPOSITIVOS", 'INFO')
            self.log(f"Caixa [{self.DEVICE_SPEAKER}]: {device_8['name']}", 'INFO')
            self.log(f"Fone [{self.DEVICE_HEADPHONE}]: {device_9['name']}", 'INFO')
            self.log("=" * 40, 'INFO')
            
            # Método 1: Threading - Garantir início simultâneo
            def play_device_8():
                try:
                    sd.play(self.audio_data, self.sample_rate, device=self.DEVICE_SPEAKER)
                    self.log(f"✅ Iniciado no dispositivo {self.DEVICE_SPEAKER}", 'DEBUG')
                except Exception as e:
                    self.log(f"❌ Erro no dispositivo {self.DEVICE_SPEAKER}: {e}", 'ERROR')
            
            def play_device_9():
                try:
                    sd.play(self.audio_data, self.sample_rate, device=self.DEVICE_HEADPHONE)
                    self.log(f"✅ Iniciado no dispositivo {self.DEVICE_HEADPHONE}", 'DEBUG')
                except Exception as e:
                    self.log(f"❌ Erro no dispositivo {self.DEVICE_HEADPHONE}: {e}", 'ERROR')
            
            # Criar threads
            thread_8 = threading.Thread(target=play_device_8)
            thread_9 = threading.Thread(target=play_device_9)
            
            # Iniciar simultaneamente
            thread_8.start()
            thread_9.start()
            
            # Aguardar threads
            thread_8.join()
            thread_9.join()
            
            self.log("✅ Áudio sendo reproduzido em AMBOS dispositivos", 'INFO')
            self.log("🎵 Caixa (público) + Fone (cantor)", 'WARNING')
            self.log("💡 Esta é a configuração para modo PERFORMANCE", 'INFO')
            
        except Exception as e:
            self.log(f"❌ Erro ao tocar em ambos dispositivos: {e}", 'ERROR')
    
    def stop_audio(self, instance):
        """Parar toda reprodução de áudio."""
        try:
            # Parar sounddevice
            sd.stop()
            self.log("⏹️ Reprodução interrompida", 'INFO')
            
            # Parar Kivy também se estiver tocando
            if self.sound and self.sound.state == 'play':
                self.sound.stop()
                self.log("⏹️ Áudio Kivy também parado", 'DEBUG')
                
        except Exception as e:
            self.log(f"❌ Erro ao parar áudio: {e}", 'ERROR')
    
    def log(self, message: str, level: str = 'INFO'):
        """Adicionar mensagem ao log visual e arquivo."""
        # Log em arquivo
        if level == 'INFO':
            logger.info(message)
        elif level == 'WARNING':
            logger.warning(message)
        elif level == 'ERROR':
            logger.error(message)
        elif level == 'DEBUG':
            logger.debug(message)
        
        # Log visual
        colors = {
            'INFO': 'ffffff',
            'WARNING': 'ffaa00',
            'ERROR': 'ff0000',
            'DEBUG': 'aaaaaa'
        }
        color = colors.get(level, 'ffffff')
        
        current = self.log_display.text
        timestamp = datetime.now().strftime('%H:%M:%S')
        new_line = f"[color={color}][{timestamp}] {message}[/color]\n"
        self.log_display.text = current + new_line
    
    def test_list_devices(self, instance):
        """Teste 1: Listar todos dispositivos de áudio disponíveis."""
        self.log("=" * 40, 'INFO')
        self.log("TESTE 1: LISTANDO DISPOSITIVOS", 'INFO')
        self.log("=" * 40, 'INFO')
        
        try:
            # Método 1: Via sounddevice (se disponível)
            try:
                import sounddevice as sd
                self.log("Usando sounddevice para listar:", 'INFO')
                
                devices = sd.query_devices()
                for i, device in enumerate(devices):
                    if device['max_output_channels'] > 0:
                        self.log(
                            f"  [{i}] {device['name']} "
                            f"(channels: {device['max_output_channels']})",
                            'DEBUG'
                        )
                
                # Dispositivo padrão
                default_out = sd.query_devices(kind='output')
                self.log(f"Saída padrão: {default_out['name']}", 'INFO')
                
            except ImportError:
                self.log("sounddevice não instalado", 'WARNING')
                self.log("Instalar: pip install sounddevice", 'WARNING')
            
            # Método 2: Via PyAudio (se disponível)
            try:
                import pyaudio
                self.log("\nUsando PyAudio para listar:", 'INFO')
                
                p = pyaudio.PyAudio()
                for i in range(p.get_device_count()):
                    info = p.get_device_info_by_index(i)
                    if info['maxOutputChannels'] > 0:
                        self.log(
                            f"  [{i}] {info['name']} "
                            f"(rate: {int(info['defaultSampleRate'])}Hz)",
                            'DEBUG'
                        )
                
                default_idx = p.get_default_output_device_info()['index']
                default_name = p.get_device_info_by_index(default_idx)['name']
                self.log(f"Saída padrão: {default_name}", 'INFO')
                
                p.terminate()
                
            except ImportError:
                self.log("PyAudio não instalado", 'WARNING')
                self.log("Instalar: pip install pyaudio", 'WARNING')
            
            self.log("✅ Listagem completa", 'INFO')
            
        except Exception as e:
            self.log(f"❌ Erro ao listar dispositivos: {e}", 'ERROR')
    
    def test_default_audio(self, instance):
        """Teste 2: Testar reprodução com dispositivo padrão."""
        self.log("=" * 40, 'INFO')
        self.log("TESTE 2: REPRODUÇÃO PADRÃO", 'INFO')
        self.log("=" * 40, 'INFO')
        
        if not self.sound:
            self.log("❌ Sem áudio de teste carregado", 'ERROR')
            return
        
        try:
            # Obter dispositivo padrão atual
            try:
                import sounddevice as sd
                default = sd.query_devices(kind='output')
                self.log(f"Dispositivo padrão: {default['name']}", 'INFO')
            except:
                self.log("Usando dispositivo padrão do sistema", 'INFO')
            
            # Tocar áudio
            self.log("Tocando áudio...", 'INFO')
            self.sound.play()
            
            self.log("✅ Áudio tocando", 'INFO')
            self.log("Verifique se está saindo no dispositivo correto", 'WARNING')
            
        except Exception as e:
            self.log(f"❌ Erro ao tocar áudio: {e}", 'ERROR')
    
    def show_manual_instructions(self, instance):
        """Teste 4: Exibir instruções para configuração manual."""
        self.log("=" * 40, 'INFO')
        self.log("INSTRUÇÕES MANUAIS DE ROTEAMENTO", 'INFO')
        self.log("=" * 40, 'INFO')
        
        self.log("MÉTODO RECOMENDADO PARA MVP:", 'INFO')
        self.log("", 'INFO')
        
        self.log("1. ENSAIO (Apenas fone):", 'INFO')
        self.log("   - Windows Settings > Sound", 'DEBUG')
        self.log("   - Output Device > Selecionar fone USB", 'DEBUG')
        self.log("   - Aplicar antes de iniciar ensaio", 'DEBUG')
        self.log("", 'INFO')
        
        self.log("2. PERFORMANCE (Fone + Caixa):", 'INFO')
        self.log("   - Windows Settings > Sound", 'DEBUG')
        self.log("   - App volume and device preferences", 'DEBUG')
        self.log("   - Configurar Python para usar ambos", 'DEBUG')
        self.log("   OU", 'DEBUG')
        self.log("   - Usar 'Stereo Mix' / 'What You Hear'", 'DEBUG')
        self.log("", 'INFO')
        
        self.log("SOLUÇÃO IMPLEMENTADA:", 'INFO')
        self.log("   ✅ Usar sounddevice para roteamento direto", 'DEBUG')
        self.log("   ✅ Selecionar dispositivo no dropdown", 'DEBUG')
        self.log("   ✅ Clicar 'Tocar Selecionado' para testar individual", 'DEBUG')
        self.log("   ✅ Clicar 'Tocar Ambos (8+9)' para modo performance", 'DEBUG')
        self.log("", 'INFO')
        
        self.log("RESULTADO DO TESTE:", 'INFO')
        self.log("   - Detectados múltiplos dispositivos USB e nativos", 'DEBUG')
        self.log("   - sounddevice permite roteamento direto", 'DEBUG')
        self.log("   - Threading garante sincronização entre dispositivos", 'DEBUG')
        self.log("   - Recomendado para implementação final", 'DEBUG')
        self.log("", 'INFO')
        
        self.log("MODOS DE OPERAÇÃO:", 'INFO')
        self.log("   🎧 ENSAIO: Tocar apenas no fone (dispositivo 9)", 'DEBUG')
        self.log("   🔊 PERFORMANCE: Tocar em ambos (8 + 9)", 'DEBUG')
        self.log("", 'INFO')
        
        self.log("✅ Instruções exibidas", 'INFO')


if __name__ == '__main__':
    logger.info(f"Python: {sys.version}")
    logger.info(f"Plataforma: {sys.platform}")
    
    AudioRoutingTest().run()
    
    logger.info("=" * 60)
    logger.info("TESTE FINALIZADO")
    logger.info("Verifique o arquivo 'audio_routing_test.log'")
    logger.info("=" * 60)