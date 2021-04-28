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

    Robot | Type | More 
    ----|----|----
    Work WeiXin | [Markdown](https://work.weixin.qq.com/api/doc/90000/90136/91770#markdown类型) | [GET access token](https://work.weixin.qq.com/api/doc/90000/90135/91039) <br> [GET users](https://work.weixin.qq.com/api/doc/90000/90135/90200)
    DingTalk | [Markdown](https://developers.dingtalk.com/document/app/custom-robot-access/li-p7l-mkl-y1g) | [GET access token](https://developers.dingtalk.com/document/app/obtain-orgapp-token) <br> [GET users](https://developers.dingtalk.com/document/app/obtains-the-list-of-people-under-a-department)
    FeiShu | [Post](https://open.feishu.cn/document/ukTMukTMukTM/uMDMxEjLzATMx4yMwETM?op_tracking=hc#c48c9c2a) | [POST app_access_token](https://open.feishu.cn/document/ukTMukTMukTM/uADN14CM0UjLwQTN) <br> [POST tenant_access_token](https://open.feishu.cn/document/ukTMukTMukTM/uIjNz4iM2MjLyYzM) <br> [GET users](https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/contact-v3/user/list) <br> [GET userid](https://open.feishu.cn/document/ukTMukTMukTM/uUzMyUjL1MjM14SNzITN)


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
    networks:
      - odo
    ports:
      - 80:80
    volumes:
      - ./template:/workspace/template
      - ./config:/workspace/config

networks:
  odo:
    driver: bridge
```
