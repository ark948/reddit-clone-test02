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
        backend:
                . apps          --> (Project specific features)
                        . a bunch of apps... --> (dedicated folders for each app)
                        . endpoints.py       --> (all apps routers will be connected to one router to keep things tidy)
                        . utils.py           --> (global level utility functions)
                . configs       --> (Configuration variables)
                . sections      --> (Common backend functionalities)
                main.py         --> (main application instance)
            runserver.py     --> (uvicorn server entry point)


        
#### Apps:
        This is where project specific-features exist.
        by "project-specific" i mean parts that different platforms do not share...
        e.g. an e-commerce platform will have a "cart" feature with which users can review their selected items and the total price, 
        before they confirm the purchase.
        But a social/forum platform (like reddit) does not have that. 
        Instead it has dedicated parts that users can view posts and search for communities that ineterests them.
        
#### Configs:
        Just where i keep global-level variables.
        (May not be the best. change this according to your own preference)
        
#### Sections:
        This is where common backend parts of the application exist.
        Essential parts that almost all projects will comprise, e.g. Database and Authentication....
        

    
(this file will be updated...)