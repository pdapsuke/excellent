from fastapi_cloudauth.cognito import CognitoCurrentUser

from env import Environment

env = Environment()

get_current_user = CognitoCurrentUser(
    region=env.aws_region, 
    userPoolId=env.cognito_userpool_id,
    client_id=env.cognito_client_id
)
