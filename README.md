# COVID19 REST API
Using Pythons Flask, a robust REST API is built around COVID19 patient data. The motivation of this API was to increase my skills of building a microservice while demonstrating my knowledge of REST API’s through a project.

# Details
Without the use of third-party libraries, a full authentication and authorization system has been built. Users of the service ca manually login or use a provided Json web token to get access remotely.  The login system is used along with Python decorator functions for route access control. Custom API endpoint are used for authorized users to access manually or programmatically through GET, POST, DELETE, and PUT HTTP requests.  

# Improvements
-	Due to the project not being pushed to production a SQLlite in-memory database is used. This could be upgraded to a professional database.
