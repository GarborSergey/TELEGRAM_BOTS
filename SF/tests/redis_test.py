import redis
import json

red = redis.Redis(host='localhost', port=6379)

dict1 = {'dictkey1': 'value_1', 'dictkey2': 'value_2'}

red.set('dict1', json.dumps(dict1))

converted_dict = json.loads(red.get('dict1'))

print(converted_dict)

red.delete('doct1')

print(red.get('dict1'))