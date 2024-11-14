from facebook_business.adobjects.adsinsights import AdsInsights
from facebook_business.adobjects.user import User
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import csv

load_dotenv()

"""Выбор начальной даты для выгрузки"""
since_year = 2024
since_month = 10
since_day = 4

"""Выбор конечной даты для выгрузки"""
until_year = 2024
until_month = 10
until_day = 5


def transfer_data_to_csv(account_id):
    """Получение токенов из переменных виртуального окружения"""
    user_a_id = os.getenv('fb_app_id')
    user_a_sec = os.getenv('fb_account_secret')
    user_a_token = os.getenv('fb_access_token')

    """Аутентификация Meta"""
    FacebookAdsApi.init(user_a_id, user_a_sec, user_a_token)

    """Получить список всех доступных рекламных аккаунтов"""
    # me = User(fbid='me')
    # my_accounts = list(me.get_ad_accounts(fields=[AdAccount.Field.name]))
    # print(my_accounts)

    account = AdAccount(f'act_{account_id}')
    insights = account.get_insights(fields=[
        AdsInsights.Field.campaign_name,
        AdsInsights.Field.adset_name,
        AdsInsights.Field.spend,
        AdsInsights.Field.impressions,
        AdsInsights.Field.clicks,
        AdsInsights.Field.ad_id
    ], params={
        'level': 'ad',
        'time_increment': 1,
        'time_range': {
            'since': datetime(since_year, since_month, since_day).strftime('%Y-%m-%d'),
            'until': datetime(until_year, until_month, until_day).strftime('%Y-%m-%d')
        },
    })
    campaign_data = []
    for i in insights:
        campaign_data.append(['facebook', i['campaign_name'], i['adset_name'],
                              i['ad_id'], i['impressions'], i['clicks'], i['spend'], i['date_stop']])

    keys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_id', 'impressions', 'clocks', 'cost', 'date']

    with open('cost.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keys)
        writer.writerows(campaign_data)


transfer_data_to_csv('859713097777393')