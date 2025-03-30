1. Run: "pip install -r requirements.txt" in the base folder
2. Add file called "botToken.py" in the base folder.
    - Add the following line of code to the file:
    ```
    botToken = "your_token_goes_here"
    ```
    - replace your_token_goes_here with your discord bot token


3. Run bot: "python -m bot"


Trouble shooting:
    - If you get audioop error when running bot in step 3, it might work to run the following command: "pip install audioop-lts"

    - To be able to play music from youtube using ".play <url>" command you need to use have ffmpeg install on the computer you're running the bot from
        so far I have only been able to run this successfully on linux (ubuntu):
        - sudo apt update
        - sudo apt install ffmpeg

