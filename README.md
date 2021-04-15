# OpenDevOps Message Center

#### OpenAPI Doc

- /oapi/ui

#### Deploy

##### docker-compose
```yaml
version: "2"
services:
  odo-msg:
    container_name: odo-msg
    image: bxwill/odo-msg
    ports:
    - 80:80
    environment:
      JENKINS_URL: ''
      JENKINS_USER: ''
      JENKINS_TOKEN: ''
      WWX_ROBOT_KEY: ''
      DT_TOKEN: ''
      DT_SECRET: ''
      FS_TOKEN: ''
      FS_SECRET: ''
```
