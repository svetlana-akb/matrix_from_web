import sys
import asyncio, aiohttp
import re

# Получить веб-страницу (текстовая информация)
async def fetch(session, url):
    try:
        async with session.get(url) as response:
            data = await response.text(encoding='utf-8')
            status = response.status
            if (status == 200):
                if re.match('[0-9\-\+\s\|]*$', data):
                    return [data, None]
                else:
                    return [None, 'ERROR: Data is in wrong format.']
            else:
                return [None, "ERROR: Response status is %s." % status]
    except aiohttp.client_exceptions.InvalidURL:
        return [None, 'ERROR: Invalid URL.']
    except Exception as ex:
        return [None, "ERROR: %s" % ex]
        
def generate_result_list(g_matrix, right_top_x, right_top_y, left_down_x, left_down_y, result_list):
    if not((right_top_x <= left_down_x)and(right_top_y >= left_down_y)):
        return result_list
    i = right_top_x
    while(i <= left_down_x):
        result_list.append(g_matrix[i][right_top_y])
        i+= 1
    j = right_top_y-1
    while(j >= left_down_y):
        result_list.append(g_matrix[left_down_x][j])
        j-= 1
    i = left_down_x-1
    while(i >= right_top_x):
        result_list.append(g_matrix[i][left_down_y])
        i-= 1
    j = left_down_y+1
    while(j < right_top_y):
        result_list.append(g_matrix[right_top_x][j])
        j+= 1
    return generate_result_list(g_matrix, right_top_x+1, right_top_y-1, left_down_x-1, left_down_y+1, result_list)
    
def matrix_retriever(data):
    matrix=[]
    lines = data.split('\n')
    m = lines[0].count('+') - 1
    n = 0
    for i in range(len(lines)):
        if i%2:
            line_with_numbers = lines[i].split('|')[1:m+1]
            matrix.append([int(item) for item in line_with_numbers])
            n+= 1
    return [n,m,matrix]
    
async def get_matrix(url):
    print("Downloading matrix from %s ...\n" % url)
    async with aiohttp.ClientSession() as session:
        [data, error] = await fetch(session, url)
    if (error):
        print(error)
    else:
        [n,m,matrix] = matrix_retriever(data)
        result_matrix = generate_result_list(matrix, 0, m-1, n-1, 0, [])
        print(result_matrix)
    await asyncio.sleep(1)

url = sys.argv[1] if len(sys.argv)>1 else input("Please input url:\n")
matrix = asyncio.run(get_matrix(url))
input("")