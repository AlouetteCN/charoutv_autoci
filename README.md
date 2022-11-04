# CharouTV Auto Checkin script

Here is a general script for auto checkin charoutv bot on telegram. It runs over Telethon, a 3rd telegram python-base package.

## Usage

- STEP 1. Execute the `charoutv_autoci` on your terminal, then an config file named `config.ini` should be generated automatically.

- STEP 2. Edit the config file.
  
  ```
  [telegram_api]
  # Here is your telegram api id and hash,
  # it can be found at https://my.telegram.org/auth?to=apps
  api_id = xxx
  api_hash = xxx

  [captcha_api]
  # Decrypt the code inside the image that the bot send to you,
  # you can use it for free 100 times/day
  # visit: https://truecaptcha.org/
  id = 
  apikey = 
  
  [base]
  retry_times = 10          # use captcha to decrypt the code for limit times
  use_system_env = False    # if you export the value to your enviroment, instead of file.
  client_name =             # let telethon specify your app client name
  ```

- STEP 3. Run the executable program again, your phone number and varify code is excepted. (Rememer don't leak your *.session file, anyone with it can do some sensitive operation to harm you telegram account)

- [Optional] Run it as schadule, just use corn, you may need to install cron in different way depending on your operating system.
  
  On `Ubuntu`, I set 10am to run the script by editing crontab: `* * 10 * * ? /path/to/charoutv_autoci`, using `crontab -e`.
