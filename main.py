import csv
import pandas as pd
import matplotlib.pyplot as plt

result_rows = []
pairs_count = {}


def read_and_change_date(old_path_files, new_path_files):
    # Открыть CSV-файл
    with open(old_path_files, newline='') as csvfile:
        # Создать объект reader для чтения CSV-файла
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)

        # Обработать каждую строку
        for row in reader:
            # Получить значение первой колонки
            name, date, strategy, price = row[0], row[2], row[4], row[7]
            if strategy.startswith('Close'):
                filtered_parts = [name, date, strategy, price]
                result_rows.append(filtered_parts)
                # Добавляем в словарь название пар и количество повторений этих пар
                if name not in pairs_count:
                    pairs_count[name] = 1
                else:
                    pairs_count[name] += 1

    # Записать измененные данные в новый файл CSV
    with open(new_path_files, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Название пары', 'Дата сделки', 'Стратегия сделки', 'Цена сделки'])
        writer.writerows(result_rows)


def analyze_file():
    # Создать объект DataFrame из списка строк
    df = pd.DataFrame(result_rows, columns=['Название пары', 'Дата сделки', 'Стратегия сделки', 'Цена сделки'])

    # Вывести статистику по данным в консоль
    print('Статистика по данным:')
    print(f'Количество сделок: {len(df)}')
    print(f'Количество уникальных пар: {len(df["Название пары"].unique())}')
    print(f'Количество сделок "Close Long": {len(df[df["Стратегия сделки"].str.startswith("Close Long")])}')
    print(f'Количество сделок "Close Short": {len(df[df["Стратегия сделки"].str.startswith("Close Short")])}')

    # Сортируем словарь с количеством пар по значениям
    pairs_count_sorted = {k: v for k, v in sorted(pairs_count.items(), key=lambda item: item[1], reverse=True)}

    # Получаем списки значений для осей графика
    pair_names = list(pairs_count_sorted.keys())
    pair_counts = list(pairs_count_sorted.values())

    # Строим график
    plt.figure(figsize=(10, 10))
    plt.bar(range(len(pairs_count_sorted)), pair_counts, align='center')
    plt.xticks(range(len(pairs_count_sorted)), pair_names, rotation=35)
    plt.xlabel('Название пары')
    plt.ylabel('Количество сделок')
    plt.show()


if __name__ == '__main__':
    read_and_change_date('Bybit-Derivatives-TradeHistory-20221130-20230215.csv', 'result_with_filters.csv')
    analyze_file()
