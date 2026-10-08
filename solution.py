import os
import requests
import folium


URL_BASE = "https://api.olhovivo.sptrans.com.br/v2.1"

# Código da linha escolhida
CODIGO_LINHA = 35274


def autenticar(sessao):
    token = os.environ["SPTRANS_TOKEN"]

    url = f"{URL_BASE}/Login/Autenticar"

    resposta = sessao.post(
        url,
        params={"token": token}
    )

    resposta.raise_for_status()

    return resposta.json()


def buscar_paradas(sessao):
    url = f"{URL_BASE}/Parada/BuscarParadasPorLinha"

    resposta = sessao.get(
        url,
        params={"codigoLinha": CODIGO_LINHA}
    )

    resposta.raise_for_status()

    return resposta.json()


def buscar_onibus(sessao):
    url = f"{URL_BASE}/Posicao/Linha"

    resposta = sessao.get(
        url,
        params={"codigoLinha": CODIGO_LINHA}
    )

    resposta.raise_for_status()

    dados = resposta.json()

    return dados.get("vs", [])


def criar_mapa(paradas, onibus):

    # Centraliza o mapa na primeira parada
    latitude = paradas[0]["py"]
    longitude = paradas[0]["px"]

    mapa = folium.Map(
        location=[latitude, longitude],
        zoom_start=13
    )

    # PINS DAS PARADAS
    for parada in paradas:

        folium.Marker(
            location=[
                parada["py"],
                parada["px"]
            ],
            popup=parada["np"],
            tooltip="Parada de ônibus",
            icon=folium.Icon(
                color="blue"
            )
        ).add_to(mapa)

    # PINS DOS ÔNIBUS
    for onibus_item in onibus:

        folium.Marker(
            location=[
                onibus_item["py"],
                onibus_item["px"]
            ],
            popup=f"Ônibus: {onibus_item['p']}",
            tooltip="Ônibus em tempo real",
            icon=folium.Icon(
                color="red"
            )
        ).add_to(mapa)

    mapa.save("mapa.html")


def main():

    sessao = requests.Session()

    print("Autenticando...")

    autenticado = autenticar(sessao)

    print("Autenticado:", autenticado)

    if not autenticado:
        raise Exception("Não foi possível autenticar.")

    print("Buscando paradas...")

    paradas = buscar_paradas(sessao)

    print("Paradas encontradas:", len(paradas))

    print("Buscando ônibus em tempo real...")

    onibus = buscar_onibus(sessao)

    print("Ônibus encontrados:", len(onibus))

    print("Criando mapa...")

    criar_mapa(paradas, onibus)

    print("Mapa criado com sucesso!")


if __name__ == "__main__":
    main()