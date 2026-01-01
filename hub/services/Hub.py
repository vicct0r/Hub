from cd_client import HUBClient
from ..models import CD


class HubService:
    # Definir corretamente o que o método faz
    def trade_request(self, client: CD, product: str, quantity: int) -> dict:
        # Os CDs devem ter um endpoint para buscar operações? O HUB deve ter o mapa de endpoints dos CDs?
        # CDs precisam de um intermediário para dizer ao HUB as rotas corretas?
        endpoint = f"http://{cd.ip}/cd/v1/product/request/{product}/{quantity}/" # endpoint que o HUB tem que saber
        cds = CD.objects.exclude(client)
        # trazer um metodo para buscar todos os CDs candidatos (aqueles que tem o produto requisitado)
        # os CDs candidatos podem ser pré-computados talvez no nível de cache para facilitar e adiantar respostas.
     
        for cd in cds:
            response = HUBClient.send_request(endpoint=endpoint)

            data = response.json()
            if data['available'] != "true":
                    continue

            if seller:
                if data['price'] < seller['price']:
                    seller = {"cd": cd.name, "price": data['price'], "quantity": data['quantity']}
            else:
                seller = {"cd": cd.name, "price": data['price'], "quantity": data['quantity']}

            # precisamos pensar no que este método devolve como resposta
            # Devolve o que? O CD fornecedor? A resposta em cima da operação de troca?
            transaction_price = seller['price'] * quantity

            transaction_data = {
                "product": product,
                "quantity": quantity
            }

        return transaction_data