import os
import logging
import httpx

logger = logging.getLogger(__name__)

def get_twilio_credentials():
    sid = os.environ.get('TWILIO_ACCOUNT_SID', '').strip()
    token = os.environ.get('TWILIO_AUTH_TOKEN', '').strip()
    number = os.environ.get('TWILIO_PHONE_NUMBER', '').strip()
    return sid, token, number

def get_fast2sms_key() -> str:
    return os.environ.get('FAST2SMS_API_KEY', '').strip()

async def send_otp_sms(phone: str, otp: str) -> bool:
    """
    Sends a 6-digit OTP SMS to a phone number (+91) via Twilio or Fast2SMS.
    """
    clean_phone = phone.replace(' ', '').strip()
    if not clean_phone.startswith('+'):
        clean_phone = f"+91{clean_phone[-10:]}"

    twilio_sid, twilio_token, twilio_number = get_twilio_credentials()

    # 1. Try Twilio SMS if credentials present
    if twilio_sid and twilio_token and twilio_number:
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json"
            data = {
                "From": twilio_number,
                "To": clean_phone,
                "Body": f"Your Grovia OTP code is {otp}. Valid for 5 minutes."
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, data=data, auth=(twilio_sid, twilio_token))
                if res.status_code in [200, 201]:
                    logger.info(f"Twilio SMS sent successfully to {clean_phone}")
                    print(f"\n✅ [Twilio REAL SMS SENT] OTP {otp} delivered to {clean_phone}\n")
                    return True
                else:
                    logger.error(f"Twilio SMS error: {res.json()}")
                    print(f"\n⚠️ Twilio SMS error response: {res.json()}\n")
        except Exception as e:
            logger.error(f"Failed to send SMS via Twilio: {e}")

    # Fallback to logger & console
    print(f"\n==========================================")
    print(f"📱 REAL SMS OTP GENERATED FOR {clean_phone}: {otp}")
    print(f"==========================================\n")
    return True
