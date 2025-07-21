# plant_disease_detection
this is backend for plant disease detection in python and django

🧠 App Summary
This is an authenticated plant disease detection app with:

User account features (register/login/logout/update)

Disease prediction

History tracking (with retrieval and deletion)

JWT authentication (with refresh and blacklist/logout support)

🔐 Authentication APIs
Method	Endpoint	Purpose
POST	/api/account/login/	Log in user using credentials → returns access & refresh JWT tokens
POST	/api/account/logout/	Logs out the user by blacklisting the refresh token
POST	/api/account/refresh/	Provides a new access token using the refresh token
POST	/api/account/register/	Registers a new user
PUT	/api/account/update_profile/	Allows authenticated user to update profile info
GET	/api/account/user_detail/	Gets currently logged-in user’s profile details

🌱 Plant Disease Detection APIs
Method	Endpoint	Purpose
POST	/api/detection/predict/	Accepts an image, returns disease prediction
GET	/api/detection/history/	Retrieves list of past predictions made by the user
GET	/api/detection/history/{id}/	Retrieves detailed info about a specific prediction
DELETE	/api/detection/history/{id}/delete/	Deletes a specific prediction from history
DELETE	/api/detection/history/clear/	Deletes all prediction history for the current user

🧪 Other Endpoint
Method	Endpoint	Purpose
GET	/api/schema/	OpenAPI schema (used by Swagger UI)
