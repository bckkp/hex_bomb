import redis
import hashlib


def SETUP_redis():
     CLEAR_DB_redis()
     SET_redis('counter', 1)
     SET_redis('counter_hash', sha256(GET_redis('counter')))
     SET_login_redis('1', 'admin')
     SET_password_redis('1', 'qwerty123')


# --------------------------- REDIS FUNCTIONS ---------------------------------



# очистить базу данных

def CLEAR_DB_redis():
    redis_client = redis.Redis() 
    redis_client.flushdb()
    redis_client.close()
    return 1



# добавить данные (ключ: данные)
    # SET_redis('ключ', 'значение')

def SET_redis(key="key", value="value"):
    redis_client = redis.Redis() 
    result = redis_client.set(key, value)
    redis_client.close()
    return result



# получить данные (по ключу)
    # GET_redis('ключ')

def GET_redis(key="key"):
    redis_client = redis.Redis() 
    value = redis_client.get(key).decode("utf-8")
    redis_client.close()
    return value



# получить список ключей (по данным)
    # GET_KEY_redis('данные') или GET_KEY_redis('данные', 'True') - точное совпадение
    # GET_KEY_redis('данные', 'False') - неточное совпадение 
        # пояснение: для GET_KEY_redis('НОУТБУК', 'False') подойдёт пара key123: 123НОУТБУК456

def GET_KEYS_redis(value="value", accuracy="True"):
    redis_client = redis.Redis() 
    all = []
    for i in KEY_redis():
        if accuracy=="True":
            if GET_redis(i) == value:
                all.append(i)
        else:
            if value in GET_redis(i):
                all.append(i)
    redis_client.close()
    return all



# получить список ключей (базовый параметр -> '*' получить все ключи)
    # KEYS_redis('ключ') или KEYS_redis('ключ*') - получить все ключи, начинающиеся с 'ключ'
    # KEYS_redis('*ключ') - получить все ключи, заканчивающиеся на 'ключ'

def KEY_redis(key="*"):
    redis_client = redis.Redis() 
    if '*' not in key: key += '*'
    value = [ i.decode("utf-8") for i in redis_client.keys(key) ]
    redis_client.close()
    return value



# добавить логин (ключ: логин)
    # примечание: данные добавятся в формате -> login.ключ: логин

def SET_login_redis(key="key", value="value"):
    redis_client = redis.Redis() 
    result = redis_client.set("login." + key, value)
    redis_client.close()
    return result



# добавить пароль (ключ: пароль)
    # примечание: данные добавятся в формате -> password.ключ: пароль

def SET_password_redis(key="key", value="value"):
    redis_client = redis.Redis() 
    result = redis_client.set("password." + key, value)
    redis_client.close()
    return result



# получить логин по ключу
    # GET_login_redis('ключ')

def GET_login_redis(key="key"):
    redis_client = redis.Redis() 
    value = redis_client.get("login." + key).decode("utf-8")
    redis_client.close()
    return value



# получить пароль по ключу
    # GET_password_redis('ключ')

def GET_password_redis(key="key"):
    redis_client = redis.Redis() 
    value = redis_client.get("password." + key).decode("utf-8")
    redis_client.close()
    return value



# увеличить значение по ключу
    # (базовые параметры -> [counter, 1] )
    # примечание: можно использовать для операций сложения/вычитания
    # INC_redis('что меняем', на сколько)

def INC_redis(counter='counter', increment=1):
    redis_client = redis.Redis() 
    result = redis_client.incrby(counter, increment)
    redis_client.close()
    return result



# Получить словарь по ключу
    # работает как KEYS_redis(), только ещё выводит все данные по этим ключам

def KEYS_VALUE_redis(key='*'):
    all = {}
    for i in KEY_redis(key):
        all[i] = GET_redis(i)
    return all



# получить словарь по данным
    # GET_KEY_redis('данные') или GET_KEY_redis('данные', 'True') - точное совпадение
    # GET_KEY_redis('данные', 'False') - неточное совпадение 
        # пояснение: для GET_KEY_redis('НОУТБУК', 'False') подойдёт пара key123: 123НОУТБУК456

def VALUE_KEYS_redis(value="value", accuracy="True"):
    redis_client = redis.Redis() 
    all = {}
    for i in KEY_redis():
        if accuracy=="True":
            if GET_redis(i) == value:
                all[i] = GET_redis(i)
        else:
            if value in GET_redis(i):
                all[i] = GET_redis(i)
    redis_client.close()
    return all



# --------------------------- HASH FUNCTIONS ---------------------------------



def sha256(str):
    res_hash = hashlib.sha256(str.encode()) 
    return res_hash.hexdigest() 

def sha512(str):
    res_hash = hashlib.sha512(str.encode()) 
    return res_hash.hexdigest() 