---
layout: post
title: "Aws Cloudformation Example Part 1 Sam Template For Rest Api Lambda Function"
date: 2021-08-02 14:45:39 +0100
tags: API Gateway, AWS, Cloudformation, Lambda
---

# AWS Cloudformation Example Part 1 - SAM Template for REST API + Lambda Function

![scenic photo of clouds during daytime]({{ "images/pexels-photo-2909083.jpeg" | relative_url }})

The goal of this example is to show how to use a Cloudformation SAM (serverless application management) template and the SAM CLI to deploy a simple REST API backed by a lambda function. All the code below is available in [this repo](https://github.com/DavidBartram/cloudformation-api-lambda).

In this post, I'm going to explain the use case and various parts of the SAM template. In [Part 2](https://david-bartram.com/2021/08/12/aws-cloudformation-example-part-2-deploy-and-test-a-rest-api-lambda-function/), I will talk through how to deploy this template and test the API using Postman.

Use Case - Coloured Widget Sales
--------------------------------

The Davros Company sells red, blue and green widgets at multiple locations. They want to be able to post daily sales stats (date, location, red widgets sold, blue widgets sold, green widgets sold) to a database through an API.

This post focuses on setting up the API and connecting it with a lambda function. Database integration has been left out - instead the lambda function is a glorified "hello world" script that sends back a response confirming the stats that have been received.

It would be relatively easy to take this lambda and add integration to DynamoDB, RDS etc. but that would go beyond the scope of this post.

1. Request Body Schema
----------------------

Firstly it would be useful to establish how the stats will be sent to the API. I've chosen to do this by sending the stats in JSON form in the body of a POST request. A correct request body should look like the below.
```json
{
    "date": "2021-07-28",
    "location": "Manchester",
    "red_sold": "2051",
	"blue_sold": "37",
	"green_sold": "588"
}
```

In the marvellous hypothetical world of this example, we will assume that whoever provides this data can be relied upon to provide a valid date in YYYY-MM-DD format and a valid location of a Davros Company widget shop.

Request bodies that don't match the above should be rejected. For this, we will need a [JSON schema](https://json-schema.org/) against which to validate the request body. For a simple case like this, the schema isn't hard to write:

```json
{
      "$schema": "http://json-schema.org/draft-04/schema#",
      "title": "Stats",
      "type": "object",
      "properties": {
          "blue_sold": {
              "type": "string"
          },
          "red_sold": {
              "type": "string"
          },
          "green_sold": {
              "type": "string"
          },
          "location": {
              "type": "string"
          },
          "date": {
              "type": "string"
          }
      },
      "required": ["blue_sold", "red_sold", "green_sold", "date", "location"]
 }
```

2. Lambda Function Code
-----------------------

The Python 3.7 code below just takes in the request (the "event" variable) and sends a response recapitulating what the lambda received. This is not of any practical use, but it shows how to access data from the request body and construct a simple response.

```python
def lambda_handler(event, context):
    message = f"Thank you for submitting data. You submitted the following. Date {event['date']} at location {event['location']}, number of red widgets sold was {event['red_sold']}, number of blue widgets sold was {event['blue_sold']}, number of green widgets sold was {event['green_sold']}."
    return {"Notes": message}
```
3. Anatomy of an AWS REST API
-----------------------------

Now let's start building our SAM template. Rather than start at the top of the file with the preamble and parameters, lets jump in and start making the components of a REST API. This will be done using standard Cloudformation code (objects of the form `AWS::ApiGateway::*`) rather than the SAM extension(objects of the form AWS`::Serverless::*`). Defining an API using the SAM extension of the Cloudformation language requires a Swagger template for the API, and for this example I wanted to build up the components of the API in a way similar to how you might create it in the console.

Remember that SAM is a superset of Cloudformation - any Cloudformation code will work in SAM, but SAM allows more options.

### REST API

The API itself, with a [regional endpoint](https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-api-endpoint-types.html), will be created according to the following Cloudformation snippet.

ApiName is a parameter which will be specified near the beginning of the template, and is referenced here with the !Ref operator. The actual name will be passed into the template when it is deployed.

```yaml
  RestApi:
    Type: AWS::ApiGateway::RestApi
    Properties:
      ApiKeySourceType: HEADER
      EndpointConfiguration:
        Types:
          - REGIONAL
      Name: !Ref ApiName
```

### Stage, Resource & Deployment

To execute this API, the user will need to send their POST request to:

`https://<API ID>.execute-api.<AWS Region>.amazonaws.com/<Stage>/<Resource>`

Stages and resources help you organise the methods in your API. For example you might have separate stages for Dev, Test and Prod, or you might use stages to separate out versions of the API. The resource should probably be named after what the API request does - such as "submitstats" for our use case of submitting widget sales data.

We also want to deploy the API so it can be immediately, used, so we include a Deployment as well. The deployment depends on the POST method (see below), meaning the method must be created first. This is just because we want to deploy the API with the method already in place!

In the snippet below, the stage name (e.g. "v0") and resource path (e.g. "submitstats") are passed into the template as parameters.

```yaml
  ApiStage:
    Type: AWS::ApiGateway::Stage
    Properties:
      DeploymentId: !Ref ApiDeployment
      RestApiId: !Ref RestApi
      StageName: !Ref StageName
  ApiResource:
    Type: AWS::ApiGateway::Resource
    Properties:
      ParentId: !GetAtt RestApi.RootResourceId
      PathPart: !Ref ResourcePath
      RestApiId: !Ref RestApi
  ApiDeployment:
    Type: AWS::ApiGateway::Deployment
    DependsOn: PostMethod
    Properties:
      RestApiId: !Ref RestApi
```

Now we're at the stage where the template references resources defined elsewhere. `!GetAtt RestApi.RootResourceId` gets the root resource ID from the object named RestApi. The names you use (RestApi, ApiStage, ApiResource) for resources are arbitrary and do not affect the name that the resource will have in AWS once deployed. Normally that is set via one of the object's properties.

### Request Model & Request Validator

We want the JSON body of the API request to be validated, as discussed above. Two resources are needed to make that happen - a request validator and a model. The model contains the scheme we discussed earlier on, requiring that every request contains a location, date, and figures for red, green and blue widgets sold.

```yaml
  ApiRequestValidator:
    Type: AWS::ApiGateway::RequestValidator
    Properties:
      Name: !Ref ValidatorName
      RestApiId: !Ref RestApi
      ValidateRequestBody: True
      ValidateRequestParameters: False
  RequestModel:
    Type: AWS::ApiGateway::Model
    Properties:
      ContentType: 'application/json'
      RestApiId: !Ref RestApi
      Schema: {"$schema": "http://json-schema.org/draft-04/schema#",
      "title": "Stats",
      "type": "object",
      "properties": {
          "blue_sold": {
              "type": "string"
          },
          "red_sold": {
              "type": "string"
          },
          "green_sold": {
              "type": "string"
          },
          "location": {
              "type": "string"
          },
          "date": {
              "type": "string"
          }
      },
      "required": ["blue_sold", "red_sold", "green_sold", "date", "location"] }
```

### POST Method

We'd like to be able to make a POST request, so we need a method to handle this.

I won't discuss all the properties in detail, but to summarise this is a POST method integrated with a lambda function specified elsewhere in the template under the imaginative title "LambdaFunction".

Note the authorization type: AWS_IAM. This means that requests to this API will be rejected unless they are [properly signed](https://docs.aws.amazon.com/general/latest/gr/signing_aws_api_requests.html) using the Access Key and Secret Key of an IAM user with permission to execute the API.

```yaml
  PostMethod:
    Type: AWS::ApiGateway::Method
    Properties:
      ApiKeyRequired: false
      AuthorizationType: AWS_IAM
      HttpMethod: POST
      Integration:
        ConnectionType: INTERNET
        Credentials: !GetAtt ApiRole.Arn
        IntegrationHttpMethod: POST
        IntegrationResponses:
          - StatusCode: 200
        PassthroughBehavior: WHEN_NO_MATCH
        TimeoutInMillis: 29000
        Type: AWS
        Uri: !Sub 'arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${LambdaFunction.Arn}/invocations'
      RequestValidatorId: !Ref ApiRequestValidator
      RequestModels:
        application/json:
          !Ref RequestModel
      MethodResponses:
        - StatusCode: 200
      OperationName: 'lambda'
      ResourceId: !Ref ApiResource
      RestApiId: !Ref RestApi
```

4. Lambda Function
------------------

Our SAM template needs to create a Lambda function based on the code in the lambda_code folder in the repo.

The Handler property determines what the "main" function for the lambda will be. In this case we're saying that the function `lambda_handler` in the file `lambda_function.py` is the function that we want to run when the lambda is triggered.

The `Fn::Join` operator at the bottom performs a string join which will construct the ARN of the IAM execution role for the lambda.

```yaml
  LambdaFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Ref LambdaName
      Handler: lambda_function.lambda_handler
      Runtime: python3.7
      CodeUri: ./lambda_code/
      MemorySize: 128
      Timeout: 300
      Role:
        Fn::Join:
          - ''
          - - "arn:aws:iam::"
            - Ref: AWS::AccountId
            - ":role/"
            - Ref: LambdaFunctionRole
```

5. IAM Roles & Policies
-----------------------

### API Execution Role

Firstly we want to create an execution role for the REST API, which will allow the API to trigger the specific lambda function that gets created. Here the policy is specified in the role template, with a single Allow statement restricted to the lambda function created by this template.

```yaml
  ApiRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Sid: ''
            Effect: 'Allow'
            Principal:
              Service:
                - 'apigateway.amazonaws.com'
            Action:
              - 'sts:AssumeRole'
      Path: '/'
      Policies:
        - PolicyName: !Ref ApiPolicyName
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: 'Allow'
                Action: 'lambda:*'
                Resource: !GetAtt LambdaFunction.Arn
```
### Lambda Function execution role

We also want to create an execution role for the lambda function, and a matching policy with the permissions it needs. Since the lambda for this example is barely more than hello-world, the only permissions it needs are for logging. For a serious use case, make sure this policy contains the permissions your lambda will need to access AWS services such as Dynamo tables, RDS instances, etc.

```yaml
  LambdaFunctionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: 'Allow'
            Principal:
              Service:
                - 'lambda.amazonaws.com'
            Action:
              - 'sts:AssumeRole'
      Path: '/'
  LambdaExecutionPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyName: !Ref LambdaPolicyName
      Roles:
        - !Ref LambdaFunctionRole
      PolicyDocument:
        Version: 2012-10-17
        Statement:
          - Effect: Allow
            Action:
              - logs:CreateLogGroup
              - logs:CreateLogStream
              - logs:PutLogEvents
            Resource:
              - "*"
```
### IAM Policy for API User

Our API will have IAM authorisation, so we will need our API requests to be signed using the Access Key and Secret Key of an IAM user. However, we don't want to create that user as part of the stack - creating the user separately ensures the Access Key and Secret Key won't change just because the Cloudformation stack for the API and lambda has been updated/deleted/etc.

What we _do_ want as part of the stack is a Managed Policy granting access to the API.

Once the stack has been deployed, we'll attach this policy to the IAM user we've manually created, granting access to execute the API.

```yaml
  ApiUserPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
      Description: Allows user to trigger the stats import API
      ManagedPolicyName: !Ref UserPolicyName
      PolicyDocument:
        Version: 2012-10-17
        Statement:
          - Effect: Allow
            Action:
              - execute-api:Invoke
              - execute-api:ManageConnections
            Resource:
              - !Join ['',[!Sub 'arn:aws:execute-api:${AWS::Region}:${AWS::AccountId}:',!Ref RestApi, '*']]
```

6. Complete Template
--------------------

If you combine all the ingredients above with some preamble to start the template and define the parameters which will be passed in by the user, the result is a complete Cloudformation SAM template for this example stack. Join me in Part 2 where I will discuss how to deploy and test the stack!

For now, here's the full template:
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Description: AWS API Gateway with a Lambda Integration
Parameters:
  ApiName:
    Type: String
    Default: my-stats-api
    Description: name for the REST API
  ResourcePath:
    Type: String
    Default: submitstats
    Description: path for the API resource
  StageName:
    Type: String
    Default: v0
    Description: name for API Stage
  ValidatorName:
    Type: String
    Default: request-body-validator
    Description: name for API request validator
  ApiPolicyName:
    Type: String
    Default: my-stats-api-policy
    Description: name for API execution policy
  
  LambdaName:
    Type: String
    Default: my-stats-lambda
    Description: name for lambda function
  LambdaPolicyName:
    Type: String
    Default: my-stats-lambda-policy
    Description: name for lambda execution policy
  
  UserPolicyName:
    Type: String
    Default: my-stats-api-user-policy
    Description: name for API user policy
    
Resources:
  RestApi:
    Type: AWS::ApiGateway::RestApi
    Properties:
      ApiKeySourceType: HEADER
      EndpointConfiguration:
        Types:
          - REGIONAL
      Name: !Ref ApiName
  ApiResource:
    Type: AWS::ApiGateway::Resource
    Properties:
      ParentId: !GetAtt RestApi.RootResourceId
      PathPart: !Ref ResourcePath
      RestApiId: !Ref RestApi
  PostMethod:
    Type: AWS::ApiGateway::Method
    Properties:
      ApiKeyRequired: false
      AuthorizationType: AWS_IAM
      HttpMethod: POST
      Integration:
        ConnectionType: INTERNET
        Credentials: !GetAtt ApiRole.Arn
        IntegrationHttpMethod: POST
        IntegrationResponses:
          - StatusCode: 200
        PassthroughBehavior: WHEN_NO_MATCH
        TimeoutInMillis: 29000
        Type: AWS
        Uri: !Sub 'arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${LambdaFunction.Arn}/invocations'
      RequestValidatorId: !Ref ApiRequestValidator
      RequestModels:
        application/json:
          !Ref RequestModel
      MethodResponses:
        - StatusCode: 200
      OperationName: 'lambda'
      ResourceId: !Ref ApiResource
      RestApiId: !Ref RestApi
  RequestModel:
    Type: AWS::ApiGateway::Model
    Properties:
      ContentType: 'application/json'
      RestApiId: !Ref RestApi
      Schema: {"$schema": "http://json-schema.org/draft-04/schema#",
      "title": "Stats",
      "type": "object",
      "properties": {
          "blue_sold": {
              "type": "string"
          },
          "red_sold": {
              "type": "string"
          },
          "green_sold": {
              "type": "string"
          },
          "location": {
              "type": "string"
          },
          "date": {
              "type": "string"
          }
      },
      "required": ["blue_sold", "red_sold", "green_sold", "date", "location"] }
  ApiStage:
    Type: AWS::ApiGateway::Stage
    Properties:
      DeploymentId: !Ref ApiDeployment
      Description: API Stage v0
      RestApiId: !Ref RestApi
      StageName: !Ref StageName
  
  ApiRequestValidator:
    Type: AWS::ApiGateway::RequestValidator
    Properties:
      Name: !Ref ValidatorName
      RestApiId: !Ref RestApi
      ValidateRequestBody: True
      ValidateRequestParameters: False
  ApiDeployment:
    Type: AWS::ApiGateway::Deployment
    DependsOn: PostMethod
    Properties:
      RestApiId: !Ref RestApi
  ApiRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Sid: ''
            Effect: 'Allow'
            Principal:
              Service:
                - 'apigateway.amazonaws.com'
            Action:
              - 'sts:AssumeRole'
      Path: '/'
      Policies:
        - PolicyName: !Ref ApiPolicyName
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: 'Allow'
                Action: 'lambda:*'
                Resource: !GetAtt LambdaFunction.Arn
  LambdaFunction:
    Type: AWS::Serverless::Function
    Properties:
      FunctionName: !Ref LambdaName
      Handler: lambda_function.lambda_handler
      Runtime: python3.7
      CodeUri: ./lambda_code/
      MemorySize: 128
      Timeout: 300
      Role:
        Fn::Join:
          - ''
          - - "arn:aws:iam::"
            - Ref: AWS::AccountId
            - ":role/"
            - Ref: LambdaFunctionRole
  LambdaFunctionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: 'Allow'
            Principal:
              Service:
                - 'lambda.amazonaws.com'
            Action:
              - 'sts:AssumeRole'
      Path: '/'
  LambdaExecutionPolicy:
    Type: AWS::IAM::Policy
    Properties:
      PolicyName: !Ref LambdaPolicyName
      Roles:
        - !Ref LambdaFunctionRole
      PolicyDocument:
        Version: 2012-10-17
        Statement:
          - Effect: Allow
            Action:
              - logs:CreateLogGroup
              - logs:CreateLogStream
              - logs:PutLogEvents
            Resource:
              - "*"
  ApiUserPolicy:
    Type: AWS::IAM::ManagedPolicy
    Properties:
      Description: Allows user to trigger the stats import API
      ManagedPolicyName: !Ref UserPolicyName
      PolicyDocument:
        Version: 2012-10-17
        Statement:
          - Effect: Allow
            Action:
              - execute-api:Invoke
              - execute-api:ManageConnections
            Resource:
              - !Join ['',[!Sub 'arn:aws:execute-api:${AWS::Region}:${AWS::AccountId}:',!Ref RestApi, '*']]
```