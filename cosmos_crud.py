from azure.cosmos import exceptions, CosmosClient, PartitionKey
import asyncio
import os
import config

url = config.settings['url']
key = config.settings['key']

DATABASE_ID ="dummy"
CONTAINER_ID ='todo-items'


#create database
async def create_database_container(client, id):
    try:
        database = client.create_database(id = DATABASE_ID)
        print('Database with id \'{0}\' created'.format(id))
    except exceptions.CosmosResourceExistsError:
        print('A database with id \'{0}\' already exists'.format(id))
    #create container
    database = client.get_database_client(DATABASE_ID)
    container = database.create_container_if_not_exists(id=CONTAINER_ID, partition_key=PartitionKey(path='/id'))

async def upsert_item(client):

    database = client.get_database_client(DATABASE_ID)
    container = database.get_container_client(CONTAINER_ID)
    
    for i in range(10):
                 container.upsert_item({
                'id': 'item{0}'.format(i),
                'productName': 'Widget',
                'productModel': 'Model {0}'.format(i)
            }
        )
#read database
async def read_database(client, id):
    print("Get a Database by id")

    try:
        database = client.get_database_client(id)
        database.read()
        print('Database with id \'{0}\' was found'.format(id))

    except exceptions.CosmosResourceNotFoundError:
        print('A database with id \'{0}\' does not exist'.format(id))

#list all the databases 
async def list_databases(client):
    print("List all Databases on an account")

    print('Databases:')
    list_databases_response = client.list_databases()
    databases = [database for database in list_databases_response]

    if len(databases) == 0:
        return

    for database in databases:
        print(database['id'])

#read item
def read_item(client,doc_id):
    database = client.get_database_client(DATABASE_ID)
    container = database.get_container_client(CONTAINER_ID)
    response = container.read_item(item=doc_id, partition_key=doc_id)
    print(response)
#delete database
async def delete_database(client, id):
    print("\n5. Delete Database")

    try:
        client.delete_database(id)
        print('Database with id \'{0}\' was deleted'.format(id))

    except exceptions.CosmosResourceNotFoundError:
        print('A database with id \'{0}\' does not exist'.format(id))

async def run_sample():

    with CosmosClient(url, key) as client:
        try:
        
            # create a database,container and insert items
            await create_database_container(client, DATABASE_ID)

            

            # get a database using its id
            await read_database(client, DATABASE_ID)

            # list all databases on an account
            await list_databases(client)

            #insert items

            await upsert_item(client)
            # read items in db
            read_item(client,"item7")
            read_item(client, "item8")
            # delete database by id
            await delete_database(client, DATABASE_ID)
            #
        except exceptions.CosmosHttpResponseError as e:
            print('\nrun_sample has caught an error. {0}'.format(e.message))

        finally:
            print("\nCRUD operations are completed")

if __name__ == '__main__':
    asyncio.run(run_sample())