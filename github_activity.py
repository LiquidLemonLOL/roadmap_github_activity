import argparse
import requests
import json

parser = argparse.ArgumentParser(prog='GitHub Activity Tracker', description='Fetches activity for the specified user on GitHub', epilog='CLI Command: python github_activity.py -u <username>')

parser.add_argument('-u', '--user', help='Specify the user to check activity for', required=True)

args = parser.parse_args()
username = str(args.user)

def get_user_events(username):
    url = f"https://api.github.com/users/{username}/events/public"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            events_data = response.json()
            event_list = events_data
            print(f"Listing latest 30 events for {username}:")
            for events in event_list:
                if events['type'] == 'CreateEvent':
                    print(f"{username} created a {events['payload']['ref_type']} with the name {events['payload']['ref']}")
                elif events['type'] == 'PushEvent':
                    print(f"{username} pushed {events['payload']['size']} commit(s) to repository {events['repo']['name']}")
                elif events['type'] == 'DeleteEvent':
                    print(f"{username} deleted a {events['payload']['ref_type']} with the name {events['payload']['ref']}")
                elif events['type'] == 'ForkEvent':
                    print(f"{username} forked {events['repo']['name']}")
                elif events['type'] == 'IssueEvent':
                    print(f"{username} {events['payload']['action']} issue {events['payload']['issue']['title']}")
                elif events['type'] == 'WatchEvent':
                    print(f"{username} starred the repo {events['repo']['name']}")

    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
if __name__ == "__main__":
    get_user_events(args.user)



