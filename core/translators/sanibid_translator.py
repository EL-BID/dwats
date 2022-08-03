from PyQt5.QtCore import QTranslator, QSettings


class SanibidTranslator(QTranslator):
    DEFAULT_LANGUAGE = 'pt'

    def __init__(self):
        super().__init__()

    # noinspection PyMethodOverriding
    def load(self):
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]

        # Add here all available translations
        if locale.startswith('en'):
            super().load(r':/plugins/tratamientos_descentralizados/resources/translations/en.qm')
        elif locale.startswith('es'):
            super().load(r':/plugins/tratamientos_descentralizados/resources/translations/es.qm')
        elif locale.startswith('pt'):
            super().load(fr':/plugins/tratamientos_descentralizados/resources/translations/pt.qm')
        else:  # Nosso plugin por padrão é em português, então não carregamos nada no tradutor.
            super().load(fr':/plugins/tratamientos_descentralizados/resources/translations/{self.DEFAULT_LANGUAGE}.qm')
