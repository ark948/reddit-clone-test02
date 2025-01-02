# Reddit Clone in FastAPI

### Features:
    . Create and join communities
    . Make posts
    . Like or dislike other users' posts
    . Comment on users' posts (Comments can also be liked and disliked)
    . Other features comming...
    
    
### Tech Stack:
    . Backend Framework: FastAPI
    . ORM: SQLAlchemy 2.0 + SQLModel
    . Database: PostgresSQL (Async Connection)
    . Token Authentication
    . Redis for caching
    . Celery (With Redis as message broker)
    . Async compatible tests (with pytest fixtures)
    

### How is this project structured:
    . Project has 3 main parts:
        . apps
        . configs
        . sections
        
#### Apps:
        This is where project specific-features exist.
        by "project-specific" i mean parts that different platforms do not share...
        for example, an e-commerce platform will almost definitely have a "cart" feature where users can review the items they wish to purchase and the total price, before they confirm and pay for their purchase.
        But a social/forum platform like Reddit does not have that. Instead it has dedicated parts that users can view posts and search for communities of their interest.
        
#### Configs:
        Just where i keep global-level variables.
        (May not be the best, you're encouraged to change this according to your own preference)
        
#### Sections:
        This is where common backend parts of the application exist.
        Essential parts that almost all projects will comprise, such as Database and Authentication.
        

    
(this file will be updated...)