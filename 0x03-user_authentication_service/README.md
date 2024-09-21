# User Authentication Service

This project contains all the tasks for implementing user authentication services.

## Learning Objectives
- How to declare API routes in a Flask app
- How to get and set cookies
- How to retrieve request form data
- How to return various HTTP status codes

## Requirements
- Python 3.7
- bycrypt
- pycodestyle 2.5
- SQLAlchemy 1.3.x

## Tasks

- [] **0. User Model**<br >In [user.py](user.py),
    - Create a SQLAlchemy model named `User` for a database table named `users` (by using the [mapping declaration](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping) of SQLAlchemy).
    - The model will have the following attributes:

        - `id`, the integer primary key
        - `email`, a non-nullable string
        - `hashed_password`, a non-nullable string
        - `session_id`, a nullable string
        - `reset_token`, a nullable string

- [] **1. Create User**<br >In [db.py](db.py),
    - Complete the `DB` class provided below to implement the `add_user` method
    ```python
    """DB module
    """
    #!/usr/bin/env python3
    from sqlalchemy import create_engine
    from sqlalchemy.ext.declarative import declarative_base
    from sqlalchemy.orm import sessionmaker
    from sqlalchemy.orm.session import Session

    from user import Base


    class DB:
        """DB class
        """

        def __init__(self) -> None:
            """Initialize a new DB instance
            """
            self._engine = create_engine("sqlite:///a.db", echo=True)
            Base.metadata.drop_all(self._engine)
            Base.metadata.create_all(self._engine)
            self.__session = None

        @property
        def _session(self) -> Session:
            """Memoized session object
            """
            if self.__session is None:
                DBSession = sessionmaker(bind=self._engine)
                self.__session = DBSession()
            return self.__session
    ```
    - Note that `DB._session` is a private property and hence should **NEVER** be used from outside the `DB` class.

    - Implement the `add_user` method, which has two required string arguments: `email` and `hashed_password`, and returns a `User` object. The method should save the user to the database. No validations are required at this stage.

- [] **2. Find User**<br >In [db.py](db.py),
    - Implement the `DB.find_user_by` method. This method takes in arbitrary keyword arguments and returns the first row found in the `users` table as filtered by the method’s input arguments. No validation of input arguments required at this point.

    - Make sure that SQLAlchemy’s NoResultFound and InvalidRequestError are raised when no results are found, or when wrong query arguments are passed, respectively.<br >
    **Warning:**<br >
        - `NoResultFound` has been moved from `sqlalchemy.orm.exc` to `sqlalchemy.exc` between the version 1.3.x and 1.4.x of SQLAchemy - please make sure you are importing it from `sqlalchemy.orm.exc`.

- [] **3. Update User**<br>In [db.py](db.py),
    - Implement the `DB.update_user` method that takes as argument a required `user_id` integer and arbitrary keyword arguments, and returns `None`.

    - The method will use `find_user_by` to locate the user to update, then will update the user’s attributes as passed in the method’s arguments then commit changes to the database.

    - If an argument that does not correspond to a user attribute is passed, raise a `ValueError`.

- [] **4. Hash Password**<br >In [auth.py](auth.py),
    - Define a `_hash_password` method that takes in a `password` string arguments and returns bytes.

    - The returned bytes is a salted hash of the input password, hashed with `bcrypt.hashpw`.

- [] **5. Register User**<br >In [auth.py](auth.py),
    - Implement the `Auth.register_user` in the `Auth` class provided below:
    ```python
    #!/usr/bin/env python3
    from db import DB


    class Auth:
        """Auth class to interact with the authentication database.
        """

        def __init__(self):
            self._db = DB()
    ```
    - Note that `Auth._db` is a private property and should NEVER be used from outside the class.

    - `Auth.register_user` should take mandatory `email` and `password` string arguments and return a `User` object.

    - If a user already exist with the passed email, raise a `ValueError` with the message `User <user's email> already exists`.

    - If not, hash the password with `_hash_password`, save the user to the database `using self._db` and return the `User` object.

- [] **6. Basic Flask app**<br >In [app.py](app.py),
    - Set up a basic Flask app.

    - Create a Flask app that has a single `GET` route (`"/"`) and use `flask.jsonify` to return a JSON payload of the form:

    ```json
    {"message": "Bienvenue"}
    ```
    - Add the following code at the end of the module:

    ```python
    if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
    ```
