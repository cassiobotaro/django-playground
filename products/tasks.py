import dramatiq
import httpx


@dramatiq.actor(max_retries=3)
def count_words(url):
    if url == 'https://example.com/':
        raise ValueError('I refuse to work on this URL!')
    response = httpx.get(url)
    count = len(response.text.split(' '))
    print(f'There are {count} words at {url!r}.')
