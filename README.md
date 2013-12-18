orm.py
======

Simple object-relational mapping implementation.

Contains 2 parts:

1. Database singleton handler


        DB.init( db = "mysql" )
        db = DB.get()
        cur = db.currsor
        cur.execute( "SHOW TABLES" )

2. Abstract base class

        class User( Orm ):
            _definition = Definition( table = "user", keys = [ "id" ], incrementField = "id" )

            @staticmethod
            def fetch( login ):
                o = User()
                return o.fetchObject( "login = '" + o.escapeString( login ) + "'" )
        
        user = User.fetch( "admin" )
