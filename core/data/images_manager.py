from typing import Dict


class ImagesPathManager:
    def __init__(self, n_compart, has_sedimentation_tank):
        self.n_compart = n_compart
        self.has_sedimentation_tank = has_sedimentation_tank

    def get_dock_images(self) -> Dict[str, str]:
        root = ':/plugins/tratamientos_descentralizados/resources/pt/images/dock/'
        if self.has_sedimentation_tank:
            root += f'with_st/'
        else:
            root += f'without_st/'

        # TODO No futuro teremos versão de 4+ também
        if self.n_compart == 4:
            root += '4/'
        else:
            root += '4/'

        return {
            'corteAA': root + 'corteAA.png',
            'corteBB': root + 'corteBB.png',
            'corteCC': root + 'corteCC.png',
            'vista_superior': root + 'vista_superior.png',
            'planta_baixa': root + 'planta_baixa.png'
        }

    def get_report_images(self):
        root = ':/plugins/tratamientos_descentralizados/resources/pt/images/report/'
        if self.has_sedimentation_tank:
            root += f'with_st/'
        else:
            root += f'without_st/'
        root += f'{self.n_compart}/'

        return {
            'planta_baixa': root + 'planta_baixa.png',
            'corteAA': root + 'corteAA.png',
            'corteBB': root + 'corteBB.png',
            'corteCC': root + 'corteCC.png',
        }
