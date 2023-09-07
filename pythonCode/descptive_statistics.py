from data_fetching import *
import matplotlib.pyplot as plt


def avg_price_sqm_scatter_plot(client):
    """
    Diese Funktion erstellt ein Diagramm, dass die durchschnittlichen Kaufpreise für jede Quadratmeterzahl ausgibt.
    Die Daten stammen dabei aus einer Datenbank.
    """
    # Daten holen
    data = fetch_data(client, size=20000)

    price_sqm_dict = {}

    for hit in data:
        if 0 < hit['_source']['squareMeter'] < 500 \
                and 0 < hit['_source']['buyingPrice'] < 2500000 \
                and 0 < hit['_source']['buyingPrice'] / hit['_source']['squareMeter'] < 20000:

            # Daten nach Quadratmeterzahl sortieren
            if price_sqm_dict.keys().__contains__(hit['_source']['squareMeter']):
                price_sqm_dict[round(hit['_source']['squareMeter'])].append(hit['_source']['buyingPrice'])
            else:
                price_sqm_dict[round(hit['_source']['squareMeter'])] = [hit['_source']['buyingPrice']]

    # Durchschnitt für jede Quadratmeterzahl berechnen
    for key in price_sqm_dict.keys():
        price_sqm_dict[key] = sum(price_sqm_dict[key]) / len(price_sqm_dict[key])

    # Ergebnis als Diagramm darstellen
    plt.scatter(list(price_sqm_dict.keys()), list(price_sqm_dict.values()), s=10)

    # Hilfslinie
    plt.plot([155, 155], [0, 680000], 'k-')
    plt.plot([0, 155], [680000, 680000], 'k-')

    plt.ticklabel_format(style='plain')
    plt.xlabel('Quadratmeter')
    plt.ylabel('Durchschnittlicher Kaufpreis')
    plt.tight_layout()
    plt.show()
