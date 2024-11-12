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


def transfer_data_to_csv(account_id, ad_currency, ga_currency):
    today = datetime.now()

    currency_response = requests.get(f'https://cdn.jsdelivr.net/npm/@fawazahmed0/'
                                     f'currency-api@{today.strftime("%Y-%m-%d")}/v1/currencies/{ad_currency}.json')
    exchange_rate = currency_response.json()[f'{ad_currency}'][f'{ga_currency}']

    user_a_id = os.getenv('fb_app_id')
    user_a_sec = os.getenv('fb_account_secret')
    user_a_token = os.getenv('fb_access_token')

    FacebookAdsApi.init(user_a_id, user_a_sec, user_a_token)

    # me = User(fbid='me')
    # my_accounts = list(me.get_ad_accounts(fields=[AdAccount.Field.name]))
    # print(my_accounts)

    account = AdAccount(f'act_{account_id}')
    insights = account.get_insights(fields=[
        # AdsInsights.Field.campaign_id,
        AdsInsights.Field.campaign_name,
        AdsInsights.Field.adset_id,
        AdsInsights.Field.adset_name,
        AdsInsights.Field.spend,
        AdsInsights.Field.impressions,
        AdsInsights.Field.clicks,
    ], params={
        'level': 'adset',
        'time_increment': 1,
        'date_preset': 'maximum'
        # 'time_range': {
        #     'since': val.strftime('%Y-%m-%d'),
        #     'until': yesterday.strftime('%Y-%m-%d')
        # },
    })
    campaign_data = []
    for i in insights:
        campaign_data.append([i['adset_id'], i['adset_name'], 'facebook', i['campaign_name'], i['date_stop'],
                              i['impressions'], i['clicks'],
                              format(float(i['spend']) * exchange_rate, '.2f')])

    keys = ['utm_id', 'utm_campaign', 'utm_source', 'utm_medium', 'date', 'impressions', 'clicks', 'cost']

    with open('cost.csv', 'w+') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(keys)
        writer.writerows(campaign_data)


transfer_data_to_csv('7984974584857372', 'usd', 'uah')