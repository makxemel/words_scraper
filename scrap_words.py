import os
import requests
import psycopg2
from bs4 import BeautifulSoup


def clear_data_to_db(data):
    conn = psycopg2.connect(dbname='eng_words', user='postgres', password="postgres", host="127.0.0.1")

    cursor = conn.cursor()

    for (key, value) in data.items():
        # key - eng word | value[0] - translation | value[1] - transcription
        image = f'media/{key}/{key}.jpg'
        cursor.execute("INSERT INTO public.words_word (word, translate, image, transcription) VALUES (%s, %s, %s, %s)", [key, value[0], image, value[1]])

    conn.commit()
    print("Данные добавлены")
    cursor.close()
    conn.close()


def collect_data_with_pics():
    cookies = {
        # YOUR COOKIES
    }

    headers = {
        # YOUR HEADERS
    }

    # response = requests.get('http://www.kreekly.com/lists/5000-samyh-populyarnyh-angliyskih-slov/', headers=headers)
    # with open(f'index.html', 'w') as file:
    #     file.write(response.text)

    with open('index.html', 'r') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')


    eng_words = [i.text.strip() for i in soup.find_all('span', class_='eng')]
    ru_words = [i.text.strip() for i in soup.find_all('span', class_='rus')]
    transcription = [i.text for i in soup.find_all('span', class_='no-mobile transcript')]

    res = {eng_words[i]: [ru_words[i], transcription[i]] for i in range(len(eng_words))}
    
    # scrap pics of words

    # count = 0
    # for word in eng_words:
    #     response = requests.get(f'https://www.kreekly.com/img/words/{word}.jpg', cookies=cookies, headers=headers, stream=True)
    #     if response.status_code == 200:
    #         filename = f'pics/{word}/{word}.jpg'
    #         os.makedirs(os.path.dirname(filename), exist_ok=True)
    #         with open(filename, 'wb') as file:
    #             file.write(response.content)
    #         count += 1
    #         print(count)
    #     elif response.status_code == 404:
    #         response = requests.get('https://media.istockphoto.com/id/1047570732/ru/%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%BD%D0%B0%D1%8F/%D0%B0%D0%BD%D0%B3%D0%BB%D0%B8%D0%B9%D1%81%D0%BA%D0%B8%D0%B9.jpg?s=1024x1024&w=is&k=20&c=bUK9pt8VkKGv1cQDfDNIOUIMC3cmAt7fHB8i0iVND6s=')
    #         filename = f'pics/{word}/{word}.jpg'
    #         os.makedirs(os.path.dirname(filename), exist_ok=True)
    #         with open(filename, 'wb') as file:
    #             file.write(response.content)
    #         count += 1
    #         print(count)

    clear_data_to_db(res)


def main():
    collect_data_with_pics()


if __name__ == '__main__':
    main()
