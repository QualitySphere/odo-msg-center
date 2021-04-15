# OpenDevOps Message Center

#### Scenarios

- Message Robot
  - Jira tell you someone creates an issue
  - Jira tell you an issue has been fixed
  - Harbor tell you new image pushed
  - CI/CD tell you automation test complete
  - Webhook tell you something start/complete
  
- PM Automation
  - Webhook add jira issue comment 
  - Webhook trigger jira issue status transition
  
- CI/CD Trigger
  - Harbor trigger jenkins pipeline
  - GitLab trigger jenkins pipeline

#### OpenAPI Doc

- /oapi/ui

#### Deployment

- docker-compose
```yaml
version: "2"
services:
  odo-msg:
    container_name: odo-msg
    image: bxwill/odo-msg
    restart: always
    ports:
      - 80:80
    volumes:
      - ./template:/workspace/template
    environment:
      JIRA_URL: ''
      JIRA_USER: ''
      JIRA_PASS: ''
      JENKINS_URL: ''
      JENKINS_USER: ''
      JENKINS_TOKEN: ''
      WWX_ROBOT_KEY: ''
      DT_TOKEN: ''
      DT_SECRET: ''
      FS_TOKEN: ''
      FS_SECRET: ''
```
