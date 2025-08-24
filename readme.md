# FarmHub

A farm management platform for an agritech company.


## Setup

-Clone: git clone <repo-url>

-Navigate: cd core

-Create venv: python -m venv venv

-Activate: venv\Scripts\activate (Windows) or source venv/bin/activate (macOS/Linux)

-Install: pip install -r requirements.txt

-Migrate: python manage.py makemigrations api && python manage.py migrate

-Create SuperAdmin: python manage.py createsuperuser (username: superadmin, password: pass123)

-Run: python manage.py runserver


## Build and start the Docker containers: (vs code bash terminal)

docker-compose up --build

Access the dockerize application at http://localhost:8001 
(http://127.0.0.1:8001)





## Data Model

-User: Custom model with roles (superadmin, agent, farmer), farmers linked to one farm.

-Farm: Name, linked to one agent (manager).

-Cow: Tag, breed, owned by one farmer.

-Activity: Vaccination, birth, health check for a cow.

-MilkProduction: Daily milk yield per cow.




## Roles
-SuperAdmin: Full access (Admin panel, all APIs).

-Agent: Manages assigned farms, onboards farmers, manages farm data via APIs.

-Farmer: Manages own cows, records activities and milk via APIs.





## Adding Data

# Django Admin (SuperAdmin Only)

-Access: http://127.0.0.1:8000/admin/ (login: admin/1234)

# Steps:

-Users: Add Agent (role=agent), Farmer (role=farmer, select farm).

-Example: Agent (username=agent1, email=agent1@farmhub.com, password=pass123, role=agent).

-Farmer (username=farmer1, email=farmer1@farmhub.com, password=pass123, role=farmer, select farm).

-Farms: Set name, select Agent. Or use inline in Agent form.

-Cows: Set tag, breed, select Farmer. Or use inline in User/Farmer form.

-Activities/Milk: Add via inlines in Cow form or separately.

-Features: Search (username, tag, details), filters (role, date, farm), inline editing (Farmers in Farms, Cows/Activities/Milk in Users/Cows).




## Postman APIs-Documentation link

https://documenter.getpostman.com/view/39770088/2sB3BLkTT1




## API Routes

/api/users/ (SuperAdmin: list, create)

/api/users/<pk>/ (SuperAdmin: retrieve, update, delete)

/api/farms/ (SuperAdmin, Agent: list, create)

/api/farms/<pk>/ (SuperAdmin, Agent: retrieve, update, delete)

/api/cows/ (SuperAdmin, Agent, Farmer: list, create)

/api/cows/<pk>/ (SuperAdmin, Farmer: retrieve, update, delete)

/api/activities/ (SuperAdmin, Agent, Farmer: list, create)

/api/activities/<pk>/ (SuperAdmin, Agent, Farmer: retrieve, update, delete)

/api/milk-productions/ (SuperAdmin, Agent, Farmer: list, create)

/api/milk-productions/<pk>/ (SuperAdmin, Agent, Farmer: retrieve, update, delete)

/api/milk-reports/ (SuperAdmin, Agent: list)




## Note
-Data added in Admin appears in Postman and vice versa.

-Ensure Agent exists before creating Farm, Farmer before Cow.

_If 403 errors, verify token/role in Postman.


