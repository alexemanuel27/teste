from dependency_injector import containers, providers


class UserService:

    def __init__(self):
        self.x = 0


class Container(containers.DeclarativeContainer):

    user_service_provider = providers.Singleton(UserService)



container = Container()


print("Called by", __name__)