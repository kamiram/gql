import graphene
from django.contrib.auth import get_user_model

from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth import mutations
from graphene_django.types import DjangoObjectType
from posts.models import Post
from graphene_django_optimizer import OptimizedDjangoObjectType

User = get_user_model()


class UserType(OptimizedDjangoObjectType):
    name = graphene.String()
    resolve_name = lambda root, info: root.username

    data_reg = graphene.DateTime()
    resolve_data_reg = lambda root, info: root.date_joined

    enable = graphene.Boolean()
    resolve_enable = lambda root, info: root.is_active

    class Meta:
        model = User


class PostType(DjangoObjectType):
    class Meta:
        model = Post
        filter_fields = {
            'owner': ['exact', 'in'],
            'title': ['icontains', 'istartwith'],
            'descr': ['icontains', 'istartwith'],
        }


class AuthMutation(graphene.ObjectType):
    register = mutations.Register.Field()


class Query(UserQuery, MeQuery, graphene.ObjectType):
    get_user = graphene.Field(UserType, id=graphene.Int())
    get_post = graphene.Field(PostType, id=graphene.Int())
    get_posts = graphene.List(
        PostType,
        owner=graphene.Int(),
        title=graphene.String(),
        descr=graphene.String(),
    )

    def resolve_get_user(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            user = User.objects.get(pk=id)
            return user
        return None

    def resolve_get_post(self, info, **kwargs):
        id = kwargs.get('id')
        if id is not None:
            return Post.objects.get(pk=id)
        return None

    def resolve_get_posts(self, info, **kwargs):
        posts = Post.objects
        return posts.all()


class PostInput(graphene.InputObjectType):
    id = graphene.ID()
    owner = graphene.ID()
    title = graphene.String()
    descr = graphene.String()


class CreatePost(graphene.Mutation):
    class Arguments:
        input = PostInput(required=True)

    ok = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        post_instance = Post(title=input.title, descr=input.descr, owner_id=input.owner)
        post_instance.save()
        return CreatePost(ok=ok, post=post_instance)


class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = PostInput(required=True)

    ok = graphene.Boolean()
    post = graphene.Field(PostType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        post_instance = Post.objects.get(pk=id)
        if post_instance:
            ok = True
            post_instance.title = input.title
            post_instance.descr = input.descr
            post_instance.owner_id = input.owner
            post_instance.save()
            return UpdatePost(ok=ok, post=post_instance)
        return UpdatePost(ok=ok, post=None)


class Mutation(AuthMutation, graphene.ObjectType):
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()


schema = graphene.Schema(query=Query, mutation=Mutation, )
