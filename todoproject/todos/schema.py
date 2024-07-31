import graphene
from graphene_django.types import DjangoObjectType
from .models import Todo

class TodoType(DjangoObjectType):
    class Meta:
        model = Todo

class Query(graphene.ObjectType):
    all_todos = graphene.List(TodoType)
    get_todo = graphene.Field(TodoType, id=graphene.Int())

    def resolve_all_todos(self, info):
        return Todo.objects.all()

    def resolve_get_todo(self, info, id):
        try:
            return Todo.objects.get(pk=id)
        except Todo.DoesNotExist:
            return None

class CreateTodo(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String()
        completed = graphene.Boolean()

    todo = graphene.Field(TodoType)

    def mutate(self, info, title, description=None, completed=False):
        todo = Todo(title=title, description=description, completed=completed)
        todo.save()
        return CreateTodo(todo=todo)

class UpdateTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        description = graphene.String()
        completed = graphene.Boolean()

    todo = graphene.Field(TodoType)

    def mutate(self, info, id, title=None, description=None, completed=None):
        todo = Todo.objects.get(pk=id)
        if title:
            todo.title = title
        if description:
            todo.description = description
        if completed is not None:
            todo.completed = completed
        todo.save()
        return UpdateTodo(todo=todo)

class DeleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        todo = Todo.objects.get(pk=id)
        todo.delete()
        return DeleteTodo(success=True)

class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
