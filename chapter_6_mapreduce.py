import functools
from typing import Dict


def map_frequency(text: str) -> Dict[str, int]:
    words = text.split(' ')
    frequencies = {}
    for word in words:
        if word in frequencies:
            # Если слово уже есть в словаре частот, прибавить единицу к счетчику
            frequencies[word] = frequencies[word] + 1
        else:
            # Если слова еще нет в словаре частот, положить счетчик равным единице
            frequencies[word] = 1
    return frequencies


def merge_dictionaries(first: Dict[str, int],
                       second: Dict[str, int]) -> Dict[str, int]:
    merged = first
    for key in second:
        if key in merged:
            # Если слово встречается в обоих словарях, сложить счетчики
            merged[key] = merged[key] + second[key]
        else:
            # Если слово не встречается в обоих словарях, скопировать счетчик
            merged[key] = second[key]
    return merged


lines = ["I know what I know",
         "I know that I know",
         "I don't know much",
         "They don't know much"]

# Для каждой строки текста выполнить операцию map
mapped_results = [map_frequency(line) for line in lines]
for result in mapped_results:
    print(result)
# Редуцировать все промежуточные счетчики в окончательный результат
print(functools.reduce(merge_dictionaries, mapped_results))
