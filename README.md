# blnk-task
## Getting Started


1. Clone the repository:
  git clone https://github.com/your-username/project-name.git
  
  
  
For backend :
### Prerequisites
- Python 3.9
- Django 4.2.1

#
1. Change to the project directory:
2. Build or rebuild docker services
docker-compose build
3. run an entire app
docker-compose up
4. To create superuser
docker-compose run --rm django python3 manage.py createsuperuser
5. To create three different users: provider, customer and banker 
docker-compose run --rm django python3 create_default_users_and_groups
the users are
username: "banker"
password: "Ahmed1153"

username: "provider"
password: "Ahmed1153"

username: "customer"
password: "Ahmed1153"



For frontend :
### Prerequisites
- node 18.16.0

### Installation
1.Change to the frontend directory
npm install
npm run serve
