Hello,

To tackle this challenge, I employed two tools: [ZAP](https://www.zaproxy.org/) for the initial website reconnaissance and Python for exploiting it.

The website's objective was to engage users in watching ads within videos, prompting them to redeem codes hidden within the videos to earn money. The obtained funds could be used to purchase gift cards from the website's shop. Redeeming one video code yielded 0.1 €.

To redeem a video code, it was necessary to do so within 20 seconds of starting the video to prevent exploitation. Redemption beyond 30 seconds was rejected. Each video was identified by a random UUID, and the code had to be redeemed along with this UUID, with the video filename being the corresponding UUID.

The challenge instance reset every hour. The shop offered various gift cards, with the last one, priced at 500 €, revealing the code. Registering a new account provided a 90% discount on the final gift code for 15 minutes.

To address the challenge, I automated the registration and authentication process before progressing to downloading videos. During this stage, I discovered that although video names changed, the videos were not unique. After downloading 1500 videos, I calculated the hash for each video, identified unique keys, and found only 50 unique hashes.

Faced with the choice of manually retrieving codes for each video or utilizing smart OpenCV techniques, I opted for the manual approach to save time. Once I built a map of hash/code pairs, I automated the process of downloading a video, calculating its hash, identifying the corresponding code, and submitting it after 20 seconds—repeating this 500 times in under 15 minutes.

The provided Python code, along with the hash array, executed this automation. To optimize time, I initiated a new thread after each video identification to submit the video code after 21 seconds, preventing the program from being idle during this period.

I believe several options could have expedited the process:
- Employing multiple processes to download videos and redeem codes in parallel.
- Downloading only a small part of the videos instead of the whole video to calculate the hash of it and don't waste internet bandwitdth. I'm not sure if this is good because some video were looking to be the same, aside of the code emmbeded in it.

I overlooked the 90% reduction information until purchasing the last gift code, leaving me with 450 € and the flag !

With my code, it took approximately 20 minutes to redeem 5000 codes and around 2 minutes and 30 seconds for 500.
