
class AuthHeaders:
    
    def __init__(self, headers: dict):
        self.auth_headers = headers
    
    def get_auth_headers(self):
        '''
        Returns the auth headers. 
        '''
        return self.auth_headers
    
    def set_auth_headers(self, headers: dict):
        '''
        Allows auth_headers to be set.
        '''
        self.auth_headers = headers
        
        
        