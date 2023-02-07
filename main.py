
import sys
import logging
import threading

from dependency_injector import containers, providers

# from main import container
from container import Container, container

import time

import pandas as pd
from pandas import DataFrame, Series

from datetime import datetime


class FakeInsightsDownloader:

    def download_insights() -> dict:
        ...


class S3FakeInsightsDownloader(FakeInsightsDownloader):

    def __init__(self, config: FakeInsightsConfig, client)
        self.__client = client 
        self.__config = config

    def download_insights(self) -> dict:
        insights_obj = self.client.get_object(
            Bucket=self.__config.BUCKET_NAME,
            Key=self.__config.OBJECT_KEY
        )
        insights_json = json.loads(insights_obj.read()) 

        return insights_json 


class FakeInsightsRepository():

    def __init__(self, config: FakeInsightsConfig, downloader: FakeInsightsDownloader):
        self.__config = config
        self.__downloader = downloader
        self.__cache: DataFrame = None

        self.update_cache()

    def update_cache(self) -> None:
        self.__cache = self.__retrieve_insights(self)

    def __retrieve_insights(self) -> DataFrame:
        insights_dict = self.downloader.download_insights()
        insights_df = pd.dataframe(insights_dict)

        insights_df.explode(config.CLIENT_ID_KEY, inplace=true)
        insights_df.set_index(config.CLIENT_ID_KEY, inplace=true)
        insights_df[config.VALIDATION_DATE_KEY] = pd.to_datetime(insights_df[config.VALIDATION_DATE_KEY])

        return insights_df

    def get_insights_by_client_id(self, id: int) -> DataFrame:
        insights_pessoa_df = self.__cache.loc[id]
        
        if isinstance(insights, Series):
            insights_pessoa_df = insights_pessoa_df.to_frame()

        return insights_pessoa_df        


class FakeInsightsService:

    def __init__(self, config: FakeInsightsConfig, repository: FakeInsightsRepository): 
        self.__config = config
        self.__repository = repository 

    def update_insights(self):
        self.__repository.update_cache()

    @staticmethod
    def __filter_invalid_insights(insights):
        current_date = datetime.now()

        valid_insights = insights[
            insights[config.STATUS_KEY]== 1 && 
            insights[config.VALIDATION_DATE_KEY] > current_date
        ]

        return valid_insights 

    def get_insights_by_client_id(self, id: int) -> list[dict]:
        insights_df = self.__repository.get_insights_by_client_id(id)

        insights_df = self.__filter_invalid_insights(insights_df)
        insights_df.drop(columns=[config.STATUS_KEY, config.VALIDATION_DATE_KEY], inplace=True)
        insights_dict = insights_df.to_dict("records")

        return insights_dict


class FakeInsightsAppender():

    def __init__(self, config: FakeInsightsConfig, service: FakeInsightsService):
        self.__config = config
        self.__service = service

    def append_insights(insight_func):

        def wrapper(*args, **kwargs):
            insight_list = insights_func(*args, **kwargs)
            client_id = kwargs[self.__config.CLIENT_ID_KEY]

            fake_insights = self.__service.get_insights_by_cliend_id(client_id)
            insight_list.append(fake_insights)

            return insight_list

        return wrapper


# ===================================================================== #

import time
from typing import Callable


def init_backgroud_job(target_func: Callable, sleep:int, *target_args, **target_kwargs)

    def __loop_execution(*args, **kwargs):
        while True:
            target_func(*args, **kwargs)
            time.sleep(sleep)

    thread = threading.Thread(target=__loop_execution, target_args=args, target_kwargs=kwargs, daemon=True)
    thread.start()     


fake_insights_service = FakeInsightsService()
init_background_job(fake_insights_service.update_insights())

# ===================================================================== #

from dependecy_injector import containers, providers


def init_aws_client():
    ...


class Container(containers.DeclarativeContainer):

    s3_client = providers.Resource(init_aws_client)

    fake_insights_downloader = providers.Singleton(S3FakeInsightsDownloader, config, s3_client)
    fake_insights_repository = providers.Singleton(S3FakeInsightsRepository, config, fake_insights_downloader)
    fake_insights_service = providers.Singleton(S3FakeInsightsService, config, fake_insights_repository)

    providers.Resource(init_background_job, fake_insights_service.update_insights)


container = Container()




#     while True:
#         print("From main:", user_service.x)
#         time.sleep(5)


# user_service = container.user_service_provider()

# foo(user_service)

# container = Container()


# def thread_1(count: Count):                
#     while True:
#         count.foo()
#         print(count.count)

#         time.sleep(2)

# class Count:

#     def __init__(self):
#         self.count = 0

#     def foo(self):
#         self.count += 1


# def init_update_thead(count):
#     T = threading.Thread(target=thread_1, args=[count])
#     T.setDaemon(True)

#     # starting of thread T
#     T.start()     



# class Container(containers.DeclarativeContainer):

#     config = providers.Configuration()

#     count = providers.Singleton(Count)





if __name__ == "__main__":
    container = Container(config={"max_workers": 4})

    container.init_resources()

    logging.info("Resources are initialized")
    thread_pool = container.thread_pool()
    thread_pool.map(print, range(10))

    container.shutdown_resources()


# import threading 
# import time

# class Count:

#     def __init__(self):
#         self.count = 0

#     def foo(self):
#         self.count += 1
        
 
# # creating a function
# def thread_1(count: Count):                
#     while True:
#         count.foo()
#         print(count.count)

#         time.sleep(2)
 

# count = Count()




# # main thread stop execution till 5 sec.
# time.sleep(5)                  
# print("Count:", count.count)
# print('main Thread execution')