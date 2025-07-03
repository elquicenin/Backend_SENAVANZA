from rest_framework_simplejwt.authentication import JWTAuthentication

class CookiesJWTAuthentication(JWTAuthentication): #custom jwt authentication class es la clase que se encarga de autenticar el usuario a traves del token jwt, y que se utiliza en las vistas de la API VIEW, que son para las peticion http, en este caso GET, POST, PUT, DELETE
    
    def authenticate(self, request): 
        access_token = request.COOKIES.get('access_token')
        
        if not access_token:
            return {"error": "None"}
        
        validate_token = self.get_validated_token(access_token)

        try:
            user = self.get_user(validate_token)
        except:
            return None
        
        return (user, validate_token)