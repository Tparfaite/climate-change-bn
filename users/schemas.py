import graphene
from .models import CustomUser
from graphene_django.types import DjangoObjectType
from graphql_jwt.shortcuts import get_token

# Define the DjangoObjectType for CustomUser
class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ("id", "first_name", "last_name", "email", "country", "city", "user_type")

# Mutation for creating a user
class CreateUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        country = graphene.String(required=True)
        city = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        user_type = graphene.String(required=True)  

    user = graphene.Field(UserType)
    token = graphene.String()

    def mutate(self, info, first_name, last_name, country, city, email, password, user_type):
        if user_type not in ["admin", "data_collector", "school_admin"]:
            raise Exception("Invalid user type provided.")
        if CustomUser.objects.filter(email=email).exists():
            raise Exception("Email is already registered.")
        user = CustomUser.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            country=country,
            city=city,
            email=email,
            password=password,
            user_type=user_type,
        )
        token = get_token(user)
        return CreateUser(user=user, token=token)

# Define a Query class
class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self, info):
        return CustomUser.objects.all()

# Define a Mutation class
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()

# Create the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
