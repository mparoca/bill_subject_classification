import configparser
from neo4j import GraphDatabase
import time

class CreateBillGDB:
    def __init__(self, config_path):
        self.neo4j_driver = None
        
        # Connect to Neo4j on initialization
        self.connect_to_neo4j(config_path)
    
    def load_data(self, path, data_name):
        key = os.path.join(path, data_name)
        return pd.read_csv(key, encoding='utf-8', low_memory=False)
    
    def connect_to_neo4j(self, config_path):
        # Load configuration
        config = configparser.ConfigParser()
        config.read(config_path)

        # Extract Neo4j credentials
        uri = config.get('Neo4j', 'uri')
        user = config.get('Neo4j', 'user')
        password = config.get('Neo4j', 'password')
        
        # Initialize Neo4j driver
        try:
            self.neo4j_driver = GraphDatabase.driver(uri, auth=(user, password))
        except Exception as e:
            print("Failed to create the driver:", e)
    
    def query(self, query, parameters=None, db=None):
        assert self.neo4j_driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.neo4j_driver.session(database=db) if db is not None else self.neo4j_driver.session() 
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response
    
    def create_constraints(self):
        constraints_queries = [
            "CREATE CONSTRAINT unique_legislator IF NOT EXISTS FOR (l:Legislator) REQUIRE l.name IS UNIQUE",
            "CREATE CONSTRAINT unique_bill IF NOT EXISTS FOR (b:Bill) REQUIRE b.id IS UNIQUE",
            "CREATE CONSTRAINT unique_subject IF NOT EXISTS FOR (s:Subject) REQUIRE s.name IS UNIQUE",
        ]
        
        list(map(self.query, constraints_queries))
        print('Constraints created successfully!')
        
    def create_bills(self, data):
        #data = data[data['Bill_id'].notna() & data['sponsor_name'].notna()]
        
        bill_query = '''
            UNWIND $rows AS row
            MERGE (b:Bill {id: row.bill_id})
            ON CREATE SET b.name = row.bill_name, b.title = row.title
            MERGE (s:subject {id: row.subject})
            MERGE (b)-[:HAS_SUBJECT]->(s)
        '''
        self.query(bill_query, parameters = {'rows': data.to_dict('records')})
    
        
    def process_bills_in_batches(self, data_path, data_name, batch_size = 1000):
        print("Creating Bills and Subjects...")
            # Load the data
        data = self.load_data(data_path, data_name)
    
        # Create a new column 'batch' to divide the data into batches
        data['batch'] = data.index // batch_size
        
        # Process each batch separately
        for batch, batch_data in data.groupby('batch'):
            self.create_bills(batch_data)
        print("Bill and subjects created successfully!")
    
    
    def create_legislators(self, data):
        legislator_query = '''
            UNWIND $rows AS row
            MERGE (l:Legislator {name: row.sponsor_name})
            WITH row, l
            OPTIONAL MATCH (b:Bill {id: row.bill_id})
            MERGE (l)-[:IS_SPONSOR]->(b)
        '''
        self.query(legislator_query, parameters = {'rows': data.to_dict('records')})
    
    def process_legislators_in_batches(self, data_path, data_name, batch_size = 1000):
        print("Creating Sponsors...")
            # Load the data
        data = self.load_data(data_path, data_name)
    
        # Create a new column 'batch' to divide the data into batches
        data['batch'] = data.index // batch_size
        
        # Process each batch separately
        for batch, batch_data in data.groupby('batch'):
            self.create_legislators(batch_data)
        print("Bill sponsors created successfully!")
        
        
def main():
    start_time = time.time()
    
    # Get the path to the config file. #!Change this to your own path where the config file is located
    current_script_directory = os.path.dirname(os.path.realpath(__file__))
    #current directory in juptyer notebook
    #current_script_directory = os.getcwd()
    parent_directory = os.path.dirname(current_script_directory)

    # Build the path to the config file assuming the config file is in the parent directory
    config_path = os.path.join(parent_directory, 'config.ini')
    #config_path = os.path.join(current_script_directory, 'config.ini')
    
    # Create an instance of the class
    gdb = CreateBillGDB(config_path)
    
    # Test the connection
    #query = "MATCH (n) RETURN count(n)"
    #print("Number of nodes in the database:", gdb.query(query)[0][0])
    
    # Create constraints
    gdb.create_constraints()
    
    path_to_data = 'data/processed/'
    
    gdb.process_legislators_in_batches(path_to_data, 'NY_Assembly_bill_sponsors.csv', batch_size = 2000)
    gdb.process_bills_in_batches(path_to_data, 'NY_Assembly_bills.csv', batch_size = 2000)
    
if __name__ == '__main__':
    main()