from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname:str
    database_username:str
    database_name:str
    database_password:str
    secret_key:str
    algorithm:str
    access_token_expire_minutes:int 
    
settings=Settings()