# collaborative-project-tracker
Project management web app where users can collaborate on projects, add tasks, assign them to team members and track them

## Keycloak setup

Run the following command to install keycloak image:

```sh
docker run -p 127.0.0.1:8080:8080 -e KC_BOOTSTRAP_ADMIN_USERNAME=admin -e KC_BOOTSTRAP_ADMIN_PASSWORD=admin quay.io/keycloak/keycloak:26.3.3 start-dev
```
