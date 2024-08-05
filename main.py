import requests
import random
import time
import os
from keep_alive import keep_alive
keep_alive()

DISCORD_WEBHOOK_URL = os.environ.get('webhook')


def get_random_group():
    group_id = random.randint(5000000, 17400000)
    url = f'https://groups.roblox.com/v1/groups/{group_id}'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    return None

def send_to_discord(group):
    group_link = f"https://www.roblox.com/groups/{group['id']}"
    data = {
        "content": f"**Group Name:** {group['name']}\n**Description:** {group['description']}\n**Link:** {group_link}",
    },
    headers = {
        "User-Agent": "Roblox Group Finder 6.9"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data, headers=headers)
    if response.status_code == 204:
        print("Sent to Discord successfully.")
    else:
        print(f"Failed to send to Discord. Status code: {response.status_code}, Response: {response.content}")

def main():
    while True:
        group = get_random_group()
        
        if group:
            if group['owner'] is None and group['publicEntryAllowed']:
                print(f"Group found: {group['name']} (ID: {group['id']})")
                send_to_discord(group)
            else:
                print(f"Group does not meet criteria: {group['name']} (ID: {group['id']})")
        else:
            print("No valid group found, trying again.")

        time.sleep(1)

if __name__ == "__main__":
    main()
