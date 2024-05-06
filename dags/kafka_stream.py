from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator


default_args = {
    'owner': 'aidasow',
    'start_date': datetime(2024, 4, 19, 16, 30)

}

def get_data():
    import requests
    res = requests.get('https://randomuser.me/api/')
    return res.json()['results'][0]


def format_data(res):
    data = {}
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(res['location']['street']['number'])} {str(res['location']['street']['name'])}"+" "+\
                        f"{str(res['location']['city'])} {str(res['location']['state'])} {str(res['location']['country'])}"
    data['postcode'] = res['location']['postcode']
    data['email'] = res['email']
    data['username'] = res['login']['username']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    return data


def stream_data():
    import json
    from kafka import KafkaProducer
    import time
    import logging
    
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'], max_block_ms=5000)
    #print(json.dumps(res), indent=3))

    current_time = time.time()
    while True:
        if time.time() > current_time + 60:
            break
        try:

            res = format_data(get_data()) 
            print(res)
            producer.send('users_created', json.dumps(res).encode('utf-8'))

        except Exception as e:
            logging.error(f"An error occurs: {e}")
            continue






with DAG(
    'user_automation',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:
    streaming_task = PythonOperator(
        task_id = "stream_data_from_api",
        python_callable= stream_data
    )



if __name__ == '__main__':
    #pass
    stream_data()
