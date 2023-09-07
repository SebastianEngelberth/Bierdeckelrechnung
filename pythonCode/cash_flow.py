import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
import seaborn as sns
import pandas as pd
from IPython.display import display

from data_fetching import fetch_data, get_query_for_zip


def calc_cashflow(buying_price, equity_capital, sqm, rent_pa, interest_rate, repayment_rate, opportunity_cost=False):
    """
    Diese Funktion berechnet den Cashflow einer Immobilie mithilfe der gegebenen Parameter.
    """
    # Kaufpreis mit Kaufnebenkosten
    total_buying_price = buying_price * 1.115

    # Jährliche Kreditkosten
    dept_capital = total_buying_price - equity_capital
    interest = dept_capital * (interest_rate / 100)
    repayment = dept_capital * (repayment_rate / 100)

    total_bank_payment = interest + repayment

    # Rücklagen und Verwaltung
    sqm_upkeep = 12 * sqm

    rental_losses = rent_pa * 0.04

    property_management = 300

    total_reserves = sqm_upkeep + rental_losses + property_management

    # Opportunitätskosten
    opportunity_cost_val = equity_capital * (6.54 / 100)

    # Cashflow

    if opportunity_cost:
        cash_flow = rent_pa - total_reserves - total_bank_payment - opportunity_cost_val

    else:
        cash_flow = rent_pa - total_reserves - total_bank_payment

    return round(cash_flow, 2)


def calc_cashflow_for_zip(client, zip, equity_capital, rent_pa, interest, repayment, opportunity_cost=False):
    """
        Diese Funktion berechnet den Cashflow für Immobilien einer Postleitzahl und gibt diese aus.
        Die Daten stammen dabei aus einer Datenbank.
    """
    # Daten holen
    data = fetch_data(client, get_query_for_zip(zip))

    # Strukturierter Aufbau für die nötigen Attribute
    data_dict = {
        'ID': [],
        'Kaufpreis': [],
        'Quadratmeter': [],
        'Cashflow': []
    }

    # Cashflows berechnen und diese speichern
    for hit in data:
        if not (40000 <= hit['_source']['buyingPrice'] <= 680000 and 20 <= hit['_source']['squareMeter'] <= 155):
            continue

        cash_flow = calc_cashflow(hit['_source']['buyingPrice'], equity_capital, hit['_source']['squareMeter'],
                                  rent_pa * hit['_source']['squareMeter'], interest, repayment,
                                  opportunity_cost=opportunity_cost)

        data_dict['ID'].append(hit['_id'])
        data_dict['Kaufpreis'].append(f'{hit["_source"]["buyingPrice"]:.2f}')
        data_dict['Quadratmeter'].append(f'{hit["_source"]["squareMeter"]:.2f}')
        data_dict['Cashflow'].append(cash_flow)

    # Ergebnis ausgeben
    df = pd.DataFrame(data_dict).sort_values('Cashflow', ascending=False)
    display(df)

    if opportunity_cost:
        print(f'\nDie Opportunitätskosten betragen {(equity_capital * (6.54 / 100)):.2f}€')


def plot_variable_buying_price(buying_price, equity_capital, sqm, rent_pa, interest, repayment,
                               price_steps=None, interest_steps=0.2, steps=10, show_plot=True, opportunity_cost=False):
    """
    Diese Funktion erstellt ein Diagramm, in dem für mehrere Kaufpreise und Zinssätze für eine gegebene Immobilie
    der Cashflow berechnet wird.
    Rückgabewert ist die Anzahl der negativen Cashflows
    """
    # Leere Liste für die Daten und die Labels erstellen
    tmp_plot_data = [[0 for x in range(steps)] for y in range(steps)]
    xlabel = []
    ylabel = []

    # Schrittgröße für den Kaufpreis festlegen
    if price_steps is None:
        price_steps = buying_price * 0.05

    below_zero = 0

    i = 0
    j = 0

    # Cashflow für alle Szenarien berechnen
    while i < steps:
        while j < steps:
            cashflow = calc_cashflow(buying_price - price_steps * i, equity_capital, sqm, rent_pa,
                                     interest - interest_steps * j, repayment, opportunity_cost=opportunity_cost)

            if cashflow < 0:
                below_zero += 1
            tmp_plot_data[steps - j - 1][i] = cashflow
            j += 1

        xlabel.append(f'{(buying_price - price_steps * i):.2f}')
        ylabel.append(f'{(interest - interest_steps * i):.2f}')
        i += 1
        j = 0

    plot_data = np.array(tmp_plot_data)
    ylabel.reverse()

    if show_plot:
        # Diagramm erstellen
        c = ["darkred", "red", "lightcoral", "white", "palegreen", "green", "darkgreen"]
        v = [0, .15, .4, .5, 0.6, .9, 1.]
        l = list(zip(v, c))
        cmap = mcolors.LinearSegmentedColormap.from_list('rg', l, N=256)
        sns.heatmap(plot_data, annot=True, annot_kws={'size': 7}, fmt='.0f', linewidths=.5, xticklabels=xlabel,
                    yticklabels=ylabel, cmap=cmap, center=-9, cbar=False, square=True)

        plt.xlabel('Preis in €')
        plt.ylabel('Fremdkapital Zinssatz in %')
        plt.xticks(rotation=45, horizontalalignment='right')
        plt.yticks(rotation=0)

        plt.title(f'Kaufpreis: {buying_price:.2f} €, {sqm:.2f} m², Kaltmiete: {rent_pa:.2f} €')

        plt.tight_layout()
        plt.show()

    return below_zero


def plot_variable_buying_price_for_zip(client, zip, equity_capital, rent_pa, interest, repayment,
                                       opportunity_cost=False):
    """
    Diese Funktion berechnet mögliche Cashflows für Immobilien einer gegebenen Postleitzahl und gibt diese aus.
    Die Daten stammen dabei aus einer Datenbank. Die fünf besten Immobilen werden in einem Diagramm dargestellt.
    """
    # Daten holen
    data = fetch_data(client, get_query_for_zip(zip))

    # Strukturierter Aufbau für die nötigen Attribute
    data_dict = {
        'ID': [],
        'Kaufpreis': [],
        'Quadratmeter': [],
        'Anzahl Positiv': []
    }

    # Variable Cashflows berechnen und diese speichern
    for hit in data:
        if not (40000 <= hit['_source']['buyingPrice'] <= 680000 and 20 <= hit['_source']['squareMeter'] <= 155):
            continue

        below_zero = plot_variable_buying_price(hit['_source']['buyingPrice'], equity_capital,
                                                hit['_source']['squareMeter'], rent_pa * hit['_source']['squareMeter'],
                                                interest, repayment, show_plot=False, opportunity_cost=opportunity_cost)

        data_dict['ID'].append(hit['_id'])
        data_dict['Kaufpreis'].append(f'{hit["_source"]["buyingPrice"]:.2f}')
        data_dict['Quadratmeter'].append(f'{hit["_source"]["squareMeter"]:.2f}')
        data_dict['Anzahl Positiv'].append(100 - below_zero)

    df = pd.DataFrame(data_dict).sort_values('Anzahl Positiv', ascending=False)

    # Beste fünf als Diagramm erstellen & ausgeben

    for index, row in df.head(5).iterrows():
        plot_variable_buying_price(float(row['Kaufpreis']), equity_capital, float(row['Quadratmeter']),
                                   rent_pa * float(row['Quadratmeter']), interest, repayment,
                                   opportunity_cost=opportunity_cost)
    # Ergebnis ausgeben
    display(df)

    print(f'\nDie Top 5 der Liste sind in den Diagrammen dargestellt.')
    if opportunity_cost:
        print(f'\nDie Opportunitätskosten betragen {(equity_capital * (6.54 / 100)):.2f}€')
