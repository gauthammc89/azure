import asyncio
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import azure.cosmos.cosmos_client as cosmos_client

import os,config

url = config.settings['url']
key = config.settings['key']
DATABASE_ID ='demo_DB'

def create_items(container):
    
    item1 = {
    'id': '1',
    'customerId': 'A',
    # Expire  in 300 seconds
    'ttl': 300
    }
    container.create_item(body=item1)

    item2 = {
    'id': '2',
    'Name': 'A',
    # Expire  in 500 seconds
    'ttl': 500
    }
    container.create_item(body=item2)

    item3 = {
    'id': '3',
    'Name': 'B',
    # no expiry
    
    }
    container.create_item(body=item3)   
def list_Containers(db):
    print("List all Container in a Database")
    containers = list(db.list_containers())
    for container in containers:
        print(container['id'])
def run_sample():
    client = cosmos_client.CosmosClient(url,key)
    try:

        db = client.create_database_if_not_exists(id=DATABASE_ID)
        # setup container 
        #Set default_time_to_live 
        #contailer  items will expire in 3600 seconds. 
        # #items will be removed even if ttl is not set for that item
        #if ttl is set for items. ttl will override default_time_to_live
        container = db.create_container_if_not_exists(
            id="CONT_with_default_ttl", 
            partition_key=PartitionKey(path='/id'),
            default_ttl= 3600
            )
        create_items(container)
        # As default_ttl is not set, even if ttl for items are set. items will not expire
        container = db.create_container_if_not_exists(
            id="CONT_without_default_ttl", 
            partition_key=PartitionKey(path='/id'),
            
            )
        create_items(container)
        # infinite life of container. items will not expire by default
        #items in container will expire if ttl is set for that item
        container = db.create_container_if_not_exists(
            id="infinite_default_ttl", 
            partition_key=PartitionKey(path='/id'),
            default_ttl=-1
            )
        create_items(container)
        list_Containers(db)
    except exceptions.CosmosHttpResponseError as e:
        print('\nrun_sample has caught an error. {0}'.format(e.message))

    finally:
            print("\nrun_sample done")

if __name__ == '__main__':
    run_sample()