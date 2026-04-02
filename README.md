# URL's shortcutter
A backend service for creating and managing shortened URLs with analytics and user authentication.
## API Endpoints
### Auth
- POST api/users/registration/registration_user/
- POST api/users/login/
- POST api/users/logout/
- GET api/users/user/{username}
### ShortURLs
- POST api/shortcutter/short_url — create short URL
- GET api/shortcutter/short_url
- GET api/shortcutter/click_statistics/get_genetal_statistics
### Redirect
- GET /<str:short_code>
## Installation
```
git clone https://github.com/YourMoonFlower/url_shortcutter.git
cd url_shortcutter
python -m venv venv
source venv/bin/activate
pip install poetry
poetry install
```
## Run project
```
python manage.py migrate
python manage.py runserver
```
