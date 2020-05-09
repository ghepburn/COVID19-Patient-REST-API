# Authentication
API includes a full user login system that was built without any third-party libraries. Upon login, the website session will hold the user information for a few hours.  During that time, the user is recognized by the server and can access the stored data.

# Authorization
URL route access permissions are managed via various Python decorators. If the user does not meet the decorator requirements they are redirected to the login page. There are three permission levels in effect, admin privileges, the manual session required, and login required.  These permission levels restrict data from being accessed from unknown website users, confine remote API calls to JSON pages only, and restrict management pages to admin users only.

# Payment Platform and API Key Call Limits
Upon registration, users can choose to register for free, or for a monthly fee.  Free users are restricted to 3 API calls per month while paid users have unlimited access.  Stripe's third party library is used for the payment platform.

# API Details
API calls available include GET, POST, DELETE, and PUT. JSON data is returned for these calls and very basic documentation is provided for more information on API endpoints.  Logged in users also have the option to POST data one at a time via an HTML form, or upload data in a larger quantity via a CSV file.  Pandas data library is used to manage the file upload.  A text file template is available to download for users to receive the correct column format.

# Database
An SQLite database and SQLAlchemy library are currently used for the data storage and ORM requirements.  The database aimed to be upgraded to Postgress in the near future. 
