from cash_flow import *
from descptive_statistics import *


def app_flow(client):
    """
    Diese Funktion erstellt einen Dialog für den Nutzer, damit dieser auf die Funktionen des Programms zugreifen kann.
    """
    print('Geben Sie zunächst folgende Daten ein:')
    equity_capital = float(input('Eigenkapital: '))
    interest = float(input('Zinssatz Fremdkapital (%): '))
    repayment = float(input('Tilgungsrate Fremdkapital (%): '))
    opportunity_cost = input('Sollen Opportunitätskosten berechnet werden? (Ja/Nein): ')
    opportunity_cost = True if opportunity_cost.lower() == 'ja' else False

    print('\nSie können im Folgenden eigene Immobilien verwenden, oder die der Datenbank.\n'
          'Alternativ kann auch eine Statistik über die Daten der Datenbank ausgegeben werden.\n')

    choice = input('Eigene Daten / Datenbank / Statistik: ')

    match choice.lower():
        case 'eigene daten':

            print('\nFür eigene Immobilien sind zusätzliche Eingaben nötig:')
            buying_price = float(input('Kaufpreis: '))
            sqm = float(input('Anzahl Quadratmeter (m²): '))
            rent_pa = float(input('Jährliche Kaltmiete: '))

            cashflow = calc_cashflow(buying_price, equity_capital, sqm, rent_pa, interest, repayment,
                                     opportunity_cost=opportunity_cost)
            plot_variable_buying_price(buying_price, equity_capital, sqm, rent_pa, interest, repayment,
                                       opportunity_cost=opportunity_cost)
            print(f'\nDer Cashflow ohne Anpassung der Variablen beträgt: {cashflow} €.\n'
                  f'Den Cashflow mit Anpassung des Kaufpreises und des Zinssatzes können Sie dem Diagramm entnehmen.')

        case 'datenbank':
            print('\nGeben Sie bitte folgende Daten für die Simulation ein:')
            zip = input('Postleitzahl: ')
            rent_pa = float(input('Durchschnittliche jährliche Kaltmiete/m² der Postleitzahl: '))

            print(f'\nDer Cashflow ohne Veränderung von Variablen sieht für diese Postleitzahl wie folgt aus:')
            calc_cashflow_for_zip(client, zip, equity_capital, rent_pa, interest, repayment,
                                  opportunity_cost=opportunity_cost)

            print(f'\nDer Cashflow bei Veränderung von Kaufpreis und Zinssatz sieht wie folgt aus:')
            plot_variable_buying_price_for_zip(client, zip, equity_capital, rent_pa, interest, repayment,
                                               opportunity_cost=opportunity_cost)

        case 'statistik':
            avg_price_sqm_scatter_plot(client)

        case _:
            print('Falsche Eingabe!')
