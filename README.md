# OpenDevOps Message Center

#### Scenarios

- Message Robot

  Event | Title
  ----|----
  Jira user creates an issue | Attention! Jira @you
  Jira user assign an issue | Attention! Jira `@ASSIGNEE`
  Jira user change issue status to fixed | Attention! Jira `@REPORTER` 
  Jira issue comment @you | Attention! Jira `@YOU`
  New image pushed into Harbor | Great! Harbor @you
  Automation test complete and 100% PASS | Wonderful! CI/CD @you
  Automation test complete but NOT 100% PASS | Oops! CI/CD @you
  Daily issue status | Issue Daily Report
  Daily test case execution process | Testing Daily Report

  - Message format specification

    Robot | Type
    ----|----
    Work WeiXin | [Markdown](https://work.weixin.qq.com/api/doc/90000/90136/91770#markdown类型)
    DingTalk | [Markdown](https://developers.dingtalk.com/document/app/custom-robot-access/li-p7l-mkl-y1g)
    FeiShu | [Post](https://open.feishu.cn/document/ukTMukTMukTM/uMDMxEjLzATMx4yMwETM?op_tracking=hc#c48c9c2a)


- PM Automation

  Event | Action
  ----|----
  CI/CD pipeline complete | Add Jira issue comment

[comment]: <> (  CI/CD pipeline complete | Change Jira issue status )

- CI/CD Trigger

  Event | Trigger
  ----|----
  Image pushed into Harbor | Jenkins pipeline
  Code pushed into GitLab | Jenkins pipeline

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
      - ./config:/workspace/config
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
