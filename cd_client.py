import requests
import logging
from rest_framework.response import Response

logger = logging.getLogger(__name__)
# Inserir todas as chamadas
# Intermediador entre HUB <-> CD
# Trazer validação e checagem de status dos CDs
# O HUB tem controle em cima dos CDs? Ele define CDs válidos? Como ele conhece o IP do CD? 
# Como fazer para o HUB conseguir encontrar os CDs?
class HUBClient:

    def send_request(self, endpoint):
        try: 
            response = requests.get( 
            url = f"{endpoint}", 
            timeout=5 
            )
            return response
        except Exception as e: 
            logger.debug(e)
