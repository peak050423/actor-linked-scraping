from apify import Actor
from datetime import datetime
import platform
from .company_follower import getfollowers

def get_current_timestamp():
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime('%#m-%d-%Y_%#I-%M-%p')

    return formatted_datetime

async def main():
    async with Actor:
        # Get the value of the actor input
        actor_input = await Actor.get_input() or {}

        # Structure of input is defined in .actor/input_schema.json
        company_url = actor_input.get('company_url')
        follower_number = actor_input.get('follower_number')
        linkedin_cookies = actor_input.get('cookies')

        if follower_number is None:
            raise ValueError('followerNumber parameter is required')
        if company_url is None:
            raise ValueError('companyUrl parameter is required')
        if linkedin_cookies is None:
            raise ValueError("Cookies parameter is required")


        current_timestamp = get_current_timestamp()
        cookies = {cookie['name']: cookie['value'] for cookie in linkedin_cookies}
        result = []

        if not company_url or not follower_number:
            raise ValueError('Missing required parameters for company scraper')

        company_id = company_url.split('/')[4]
        followers_info = getfollowers(company_id, follower_number, current_timestamp, cookies)


        if not followers_info:
            raise ValueError('No data found')

        result = followers_info

        # Structure of output is defined in .actor/actor.json
        print(f'Company_url: {company_url}')
        print(f'Follower number: {follower_number}')

        for row in result:
            await Actor.push_data(
            {
                "fullName": row.get('fullName'),
                "jobTitle": row.get('jobTitle'),
                "profileUrl": row.get('profileUrl'),
                "imageUrl": row.get('imageUrl'),
                "connectionDegree": row.get('connectionDegree'),
                "timestamp": current_timestamp,
                "followedAt": row.get('followedAt'),
                "positionTitle": row.get('positionTitle'),
                "companyLogo": row.get('companyLogo'),
                "companyName": row.get('companyName'),
                "locationName": row.get('locationName')
            }
        )
