ABOUT THIS PROJECT:

- This project uses Flask, marshmallow, sqlalchemy and Mysql.


INSTALLATION:

- This Project has support to Docker and since we use MySQL, it's much easier to setup and run with this approach 
  (RECOMMENDED).
    
    - Installing MySQL client or Psycopg (Postgres) is always a very hard task if you don't have those systems already
    installed on your environment, thus I reinforce the preference for this approach.
    
    - go to project's root directory
    
    - run `docker-compose up` and it'll start both containers (dashboard and mysql).
  
- If you don't want to use `docker-compose`, then you'll have to:
    - install requirements into your virtual environment: `pip install requirements.txt`
    
    - change bank_api/config/common.py and update `SQLALCHEMY_DATABASE_URI` to point to your Mysql or Sqlite database.


TESTS:

- run: 
    - `pip install -r requirements-dev.txt`
      
    - `coverage run --source bank_api -m pytest -s`
      
    - `coverage report` in order to get the coverage.


RUNNING:

- If you are using docker-compose approach and it's your first time running the project, then you need to create the database.
    
  - simply run `docker-compose exec dashboard python manage.py create_tables`
    
  - One alternative is also to run the sql script located in the migrations directory.
    
  - Once the database is created, you'll be ready to start to make requests to the API.

- If you are not using docker-compose approach, run:
    - `python manage.py create_tables`
      
    - `python manage.py run -p 8089`


- the base path is: http://127.0.0.1:8089/

- Please, refer to the [API documentation](http://dkspinheiro.com/bank_api/index.html) as per to know how to consume it.


USAGE

- The easiest way to use the API is by Downloading and importing the [postman collection](http://dkspinheiro.com/bank_api/bank_api.postman_collection.json)


- More detailed information can be found in the [swagger documentation](http://dkspinheiro.com/bank_api/index.html).


- The swagger documentation is included in the project and the main idea is to have it "deployed" to a s3 bucket during the deployent process.


ARCHITECTURE

  The project was designed thinking about future expansion. This way the factory app concept was used in order to
  make it flexible to modularization and facilitate testing. With such things in mind, the bank_api was created with the 
  following structure:

  ![Database and Entity structure](http://dkspinheiro.com/bank_api/component_diagram.png)
  <center>Component diagram</center>

  - The API component holds all resources and has a very simple and generic organization with the following structure: 
    - resource
      - __ini__.py (endpoint)
      - failures.py
      - schema.py
      - service.py
      - validators.py

  This is very generic and there will be resources missing one or two of these modules.

  Currently the API is focused on Account and Transactions and for this reason two enums were created in order to
  differentiate between Account and Transaction types. I believe this will come in handy if we need to add support
  to different account types (ex: savings) and operations (ex: transference). That said, the 
  entity structure will look like this:

  ![Database and Entity structure](http://dkspinheiro.com/bank_api/bank_api.png)
  <center>Database and entity structure</center>

  In terms of general architecture, we may consider having different types of actors such as desktop, mobile apps or 
  even internal or third party services. These components will reach DNS load balancers leading to a group of path based
  load balancers. With this approach we can have two different server groups, one for handling account endpoints and 
  another for handling transactions. Those server groups will run docker containers, facilitating scalability and 
  deployment.

  I believe it's important to have a rate limiting approach to help us prevent abusive calls and even DDoS attempts. It's
  very safe to do such things, cause it's unlike that someone will make a huge number of consecutive balance checks or
  other similar things. Redis is a good fit to the job. 

  Another very important point is to have active database redundancy, thus sharing the load among them.

  Last but not least, it'd be nice to have events propagated to kinesis. We could use that to generate valuable insights 
  and offer tailored services to our clients.
  
  The general architecture would look like this:

  ![General Architecture](http://dkspinheiro.com/bank_api/general_architecture.png)
  <center>General Architecture</center>
  
  

IMPROVEMENTS
    
    - implement endpoint to unblock an account
    
    - mark failing transactions and actually store them in the db, so that we can audit them.
    
    - have a single endpoint to handle both `balance` and `statement`. Since they were implemented as Account resource, 
      it makes more sense to have them together in the same resource as per REST best practices.
      
    - Implement sorting for statement endpoint.
    
    - Add more logs and have them propagated to ELK or datadog.
    
    - make adjustments in order to accept more transaction types such as transference.
    
    - support overdraw limit.
  
    - integration with sonarqube for code analysis.
  
    - integration with newrelic for monitoring
  
    - integration with AWS System Manager for loading secret keys and credentials.
    

ADDITIONAL INFORMATION

- Code coverage can be found [here](http://dkspinheiro.com/bank_api/coverage/index.html)
