import asyncio
import aiohttp
import time
import datetime

print(""" S)ssss    C)ccc  R)rrrrr  I)iiii P)ppppp  T)tttttt    K)   kk  I)iiii T)tttttt T)tttttt I)iiii E)eeeeee  S)ssss  
S)    ss  C)      R)    rr   I)   P)    pp    T)       K)  kk     I)      T)       T)      I)   E)       S)    ss 
 S)ss    C)       R)  rrr    I)   P)ppppp     T)       K)kkk      I)      T)       T)      I)   E)eeeee   S)ss    
     S)  C)       R) rr      I)   P)          T)       K)  kk     I)      T)       T)      I)   E)            S)  
S)    ss  C)      R)   rr    I)   P)          T)       K)   kk    I)      T)       T)      I)   E)       S)    ss 
 S)ssss    C)ccc  R)    rr I)iiii P)          T)       K)    kk I)iiii    T)       T)    I)iiii E)eeeeee  S)ssss  
                                                                                                                  
                                                                                                                  """)

async def questions():
    with open("token.txt", "r") as file:
        token = file.readline().strip()

    if token == "":
        print("Empty token in token.txt")
        print("Ignore the error below i dont know how to fix it if you know how to fix it create a pull request")
        return None

    headers = {'Authorization': f'{token}',
               'Content-Type': 'application/json'}

    return headers

async def get_dm_channel_ids(headers):
    url = "https://discord.com/api/v9/users/@me/channels"

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                dm_channel_ids = [channel["id"] for channel in data if channel["type"] == 1]
                return dm_channel_ids
            elif response.status == 429:
                print("Rate limited. Waiting 10 seconds...")
                await asyncio.sleep(10)
                return await get_dm_channel_ids(headers)
            else:
                print("Failed to retrieve DM channel IDs.")
                return None

async def send_messages(dm_channel_ids, headers):
    message = ""

    async with aiohttp.ClientSession() as session:
        for channel_id in dm_channel_ids:
            data = {
                "content": message
            }
            async with session.post(f"https://discord.com/api/v9/channels/{channel_id}/messages", headers=headers, json=data) as response:
                if response.status == 200:
                    print(f"Message sent successfully to channel {channel_id}: {message}")
                elif response.status == 429:
                    print("Rate limited. Waiting 10 seconds...")
                    await asyncio.sleep(10)
                else:
                    print(f"Failed to send message to channel {channel_id}: {message}")

async def main():
    headers = await questions()
    if headers is None:
        return

    dm_channel_ids = await get_dm_channel_ids(headers)
    if dm_channel_ids is not None:
        await send_messages(dm_channel_ids, headers)

if __name__ == "__main__":
    asyncio.run(main())
