# tratamientos_descentralizados
Plugin para geração desenhos esquemáticos de Sistemas Descentralizados

# Wiki do projeto
- [veja a wiki do projeto](https://gitlab.com/sanibid/tratamientos_descentralizados/-/wikis/home)

Plugin SaniHUB DWATS

Orientação para instalação:

- Fazer download do arquivo compactado (.zip) no repositório do plugin;
- Com o QGIS aberto, ir em Complementos e clicar em Gerenciar e Instalar complementos;
- Clique em Instalar a partir do ZIP;
- Selecione o arquivo do plugin e clique em Instalar Complemento;
- Pronto plugin instalado!

Para acessar o plugin:
- No menu Complementos vá até SaniHUB DWATS e, em seguida clique em SaniHUB DWATS.

## Como trabalhar com as traduções no projeto.
### Preparando o ambiente de desenvolvimento para a tradução.
Um bom tutorial demonstrando como funciona o processo de tradução utilizado nesse projeto encontra-se em [Python Application Translation With Qt Linguist](https://blog.finxter.com/python-application-translation-with-qt-linguist/).

Para gerar as traduções, deve-se primeiramente dirigir-se ao arquivo encontrado em `i18n/SaniBidS‎tarSD.pro`, que no momento da escrita dessa guia, está dessa maneira:
```
CODECFORTR = UTF-8
SOURCES += ../gui/dock_tabs/view/ui_dock_tab_costs_base.py \
           ../gui/dock_tabs/view/ui_dock_tab_sedimentation_tank_base.py \
           ../gui/dock_tabs/view/ui_dock_tab_rac_base.py \
           ../gui/dock_tabs/view/ui_dock_tab_home_head_layout.py \
           ../gui/dock_tabs/view/ui_dock_tab_home_base.py \
           ../gui/dock_tabs/view/ui_dock_tab_general_base.py \
           ../gui/dock_tabs/ui_dock_tab_about.py \
           ../gui/dock_tabs/ui_dock_tab_costs.py \
           ../gui/dock_tabs/ui_dock_tab_general.py \
           ../gui/dock_tabs/ui_dock_tab_home.py \
           ../gui/dock_tabs/ui_dock_tab_rac.py \
           ../gui/dock_tabs/ui_dock_tab_sedimentation_tank.py \
           ../gui/ui_dock.py \
           ../gui/ui_entrance_data.py \
           ../gui/ui_rep_entrance_data.py \
           ../gui/ui_rep_out_costs.py \
           ../gui/ui_rep_out_data.py
TRANSLATIONS += en.ts \
                es.ts
RESOURCES = ../resources.qrc
```
A primeira variável, `CODECFORTR` é colocada como UTF-8, pois estamos trabalhando com o texto fonte em português, e o encoding padrão ascii não suporta todos os caracteres do português

em `SOURCES`, você deve colocar todos os arquivos .py ou .ui que contém textos fontes para tradução, um por linha, com o caractere `\` depois de cada caminho de arquivo.

em `TRANSLATIONS`, você deve colocar todos os arquivos de saída de tradução, nesse caso, colocamos como saída os arquivos en.ts e es.ts (Tradução espanhol/inglês)

em `RESOURCES`, colocamos o caminho para o arquivo de recursos utilizado pelo PyQt5

Depois de adicionar e modificar de acordo com o projeto atual o arquivo .pro, devemos executar o arquivo batch `i18n/_Generat‎e_TS.bat`
```bat
@echo off
Rem para classes que usam o método tr()
pylupdate5 SaniBidStarSD.pro

Rem para classes que não herdam de QObject, ou precisaram criar o método translate por outro motivo.
pylupdate5 -verbose -tr-function translate SaniBidStarSD.pro
pause
```

Como descrito nos comentários do arquivo, o comando procura funções definidas no python do tipo `tr()` e `translate()`, porém ignorará outras funções que podem até se comunicar com o PyQt5 de tradução.

Então, caso a classe que você utilize não derive de QObject, você deverá criar um método dentro da classe como a seguir: 
```python
def translate(self, msg, disambiguation=None, n=-1):
    return QCoreApplication.translate(NomeDaSuaClasse.__name__, msg, disambiguation, n)
```
Definindo o contexto da tradução a partir do nome da classe. Outra maneira seria chamando o método `QCoreApplication.translate` diretamente e escrevendo o contexto em todas as chamadas.

### Inserindo os arquivos de tradução no projeto.
Após gerar os arquivos ".ts" de tradução, deveremos mandá-los à um profissional para o traduzir no QtLinguist. 

Esse profissional gerará um arquivo de tradução ".qm", e você deverá colocá-lo em `resources/translations/linguagem.qm`. Após isso, colocar essa referência em `resources.qrc`, e compilar o projeto QGIS com o arquivo `compile.bat`.

Para compreender como esses arquivos são utilizados em código, aqui está a implementação atual da instalação das traduções no plugin:

Definimos primeiramente o comportamento do carregamento de traduções da nossa classe que herda de QTranslator.

O comportamento atual trata-se de definir um método load() que carrega diferentes arquivos dependendo da linguagem atual do QGIS.
#### **`core/translators/sanibid_translator.py`**
```python
class SanibidTranslator(QTranslator):
    DEFAULT_LANGUAGE = 'pt'

    def __init__(self):
        super().__init__()

    # noinspection PyMethodOverriding
    def load(self):
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]

        # Adicione aqui as traduções possíveis
        if locale.startswith('en'):
            super().load(r':/plugins/tratamientos_descentralizados/resources/translations/en.qm')
        elif locale.startswith('es'):
            super().load(r':/plugins/tratamientos_descentralizados/resources/translations/es.qm')
        elif locale.startswith('pt'):
            super().load(fr':/plugins/tratamientos_descentralizados/resources/translations/pt.qm')
        else:  # Nosso plugin por padrão é em português, então não carregamos nada no tradutor.
            super().load(fr':/plugins/tratamientos_descentralizados/resources/translations/{self.DEFAULT_LANGUAGE}.qm')
```

E simplesmente carregamos a tradução em um tradutor na classe principal e instalamos o tradutor
#### **`SaniBidStarSD.py`**
```python
class SaniBidStarSD:
    translator = SanibidTranslator()

    # ...

    def __init__(self, iface):
        # ...
        self.translator.load()
        QCoreApplication.installTranslator(self.translator)
```
