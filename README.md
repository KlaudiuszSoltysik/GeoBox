# GeoBox
## About 
GeoBox is my version of a geocaching website. I designed it mobile first so it could be downloaded as a PWA. I put the visual aspects aside and focused on technical aspects.
## Functions
An user can:    
- sign up (email, password and nickname) or log in (website is running localy with SQLite database) 
- use remember me button   
- use show password button    
- receive email with token to activate account (token expires after 4h)
- reset password (via email with token)
- check his coordinates and position on the map (location and map are refreshed automatically) (Google Maps API)
- all boxes are marked on the same map  
- if he uses a browser he can download PWA    
- navigate on the website and use links to other websites   
- browse all boxes (with pagination) (box card contains distance-meter and compas to every box made using geolocation in JS) (box card is the same color as box image dominant color)
- filter nerby boxes (city and radius) (AJAX is used to get autocomplete options for city field)
- sort boxes
Additionally, a logged in user can:
- log out
- add boxes (find me button automatically complete latitude and longitude form fields)
## Presentation
Video-presentation link:
