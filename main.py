import requests
import time
import re
from urllib.parse import urlencode

def mask_email_or_phone(text):
    if '@' in text:
        user, domain = text.split('@')
        length = len(user)
        if length <= 2:
            masked = user[0] + '*' * (length - 1) if length > 1 else user[0]
        else:
            masked = user[0] + '*' * (length - 2) + user[-1]
        return masked + '@' + domain
    else:
        length = len(text)
        if length <= 4:
            return '*' * length
        return '*' * (length - 4) + text[-4:]

def send_reset_request(username_or_email):
    url = "https://www.instagram.com/api/v1/web/accounts/account_recovery_send_ajax/"
    
    headers = {
        'authority': 'www.instagram.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://www.instagram.com',
        'priority': 'u=1, i',
        'referer': 'https://www.instagram.com/accounts/password/reset/',
        'sec-ch-prefers-color-scheme': 'light',
        'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
        'sec-ch-ua-full-version-list': '"Not)A;Brand";v="8.0.0.0", "Chromium";v="138.0.7204.158", "Google Chrome";v="138.0.7204.158"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'x-asbd-id': '359341',
        'x-csrftoken': 'YRxXETtYbbIcq2laTt8HaE9ileMLiLCl',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': 'hmac.AR3GYR6M7qkLF-ksuxVbQaC5cJUvY9DzOkKYK6YQ2-rsBIyz',
        'x-instagram-ajax': '1024956690',
        'x-requested-with': 'XMLHttpRequest',
        'x-web-session-id': 'fobjs7:pnhchd:bkfwo9',
        'cookie': 'datr=bSFDaFquU8O5Bthtj0VgVHA-; ig_did=D64F9750-706C-46CB-A1AA-874F3CC1B56F; mid=aEMhbQALAAFsGgbk_Uh9b9MvWrwx; ds_user_id=74837220727; ps_l=1; ps_n=1; csrftoken=YRxXETtYbbIcq2laTt8HaE9ileMLiLCl; sessionid=74837220727%3AfzyYEE5bT1dl5b%3A10%3AAYeSFZDP33gmIT1KJZ6HKwIb8drIiEd_jnUz0cCbRVo; wd=811x633; rur="VLL\\05474837220727\\0541784640652:01fe096849e77065d07f1c281dcbbd574a1f430a746a8d184a99d26ca2e897cfdd845cef"'
    }
    
    data = {
        'email_or_username': username_or_email,
        'flow': 'fxcal'
    }
    
    start_time = time.time()
    
    try:
        response = requests.post(url, headers=headers, data=data)
        json_data = response.json()
        
        time_taken = round(time.time() - start_time, 2)
        
        masked_contact = mask_email_or_phone(username_or_email)
        
        if json_data.get('status') == 'ok' and json_data.get('message'):
            # Try to extract the actual email/phone from the response
            email_match = re.search(r'email to ([^ ]+) with', json_data['message'])
            phone_match = re.search(r'phone number ([^ ]+) with', json_data['message'])
            
            if email_match:
                masked_contact = email_match.group(1)
            elif phone_match:
                masked_contact = phone_match.group(1)
            
            print("\n[✓] Success!")
            print(f"Message: {json_data['message']}")
            print(f"Time Taken: {time_taken} seconds")
            print(f"Password Reset Sent To: {masked_contact}")
            print("\nBot By: OxksTools")
        else:
            print("\n[✗] Failed to send reset link")
            print(f"Reason: {json_data.get('message', 'Unknown error')}")
            print(f"Time Taken: {time_taken} seconds")
            
    except Exception as e:
        print(f"\n[!] Error occurred: {str(e)}")

def main():
    print("""
    ██╗███╗   ██╗███████╗████████╗ █████╗     ██████╗  █████╗ ███████╗███████╗
    ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗    ██╔══██╗██╔══██╗██╔════╝██╔════╝
    ██║██╔██╗ ██║███████╗   ██║   ███████║    ██║  ██║███████║███████╗█████╗  
    ██║██║╚██╗██║╚════██║   ██║   ██╔══██║    ██║  ██║██╔══██║╚════██║██╔══╝  
    ██║██║ ╚████║███████║   ██║   ██║  ██║    ██████╔╝██║  ██║███████║███████╗
    ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
                                                                              
    Instagram Password Reset Tool - Terminal Version
    """)
    
    while True:
        print("\nOptions:")
        print("1. Send password reset link")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1/2): ").strip()
        
        if choice == '1':
            username_or_email = input("\nEnter Instagram username or email: ").strip()
            if not username_or_email:
                print("[!] Please enter a username or email")
                continue
                
            print("\n[~] Sending password reset request...")
            send_reset_request(username_or_email)
            
        elif choice == '2':
            print("\nGoodbye!")
            break
            
        else:
            print("\n[!] Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
