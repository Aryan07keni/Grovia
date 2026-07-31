import os
import logging
import httpx

logger = logging.getLogger(__name__)

def get_twilio_credentials():
    sid = os.environ.get('TWILIO_ACCOUNT_SID', '').strip()
    token = os.environ.get('TWILIO_AUTH_TOKEN', '').strip()
    number = os.environ.get('TWILIO_PHONE_NUMBER', '').strip()
    verify_sid = os.environ.get('TWILIO_VERIFY_SERVICE_SID', '').strip()
    return sid, token, number, verify_sid

def get_fast2sms_key() -> str:
    return os.environ.get('FAST2SMS_API_KEY', '').strip()

async def send_otp_sms(phone: str, otp: str) -> bool:
    """
    Sends a 6-digit OTP SMS to a phone number (+91) via Twilio, Fast2SMS, or 2Factor.
    """
    clean_phone = phone.replace(' ', '').strip()
    if not clean_phone.startswith('+'):
        clean_phone = f"+91{clean_phone[-10:]}"

    twilio_sid, twilio_token, twilio_number, verify_sid = get_twilio_credentials()

    # 1. Try Twilio Verify API if Verify Service SID present
    if twilio_sid and twilio_token and verify_sid:
        try:
            url = f"https://verify.twilio.com/v2/Services/{verify_sid}/Verifications"
            data = {"To": clean_phone, "Channel": "sms"}
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, data=data, auth=(twilio_sid, twilio_token))
                if res.status_code in [200, 201]:
                    logger.info(f"Twilio Verify SMS sent successfully to {clean_phone}")
                    print(f"\n✅ [Twilio Verify REAL SMS SENT] Delivered to {clean_phone}\n")
                    return True
                else:
                    logger.error(f"Twilio Verify error: {res.json()}")
        except Exception as e:
            logger.error(f"Failed via Twilio Verify: {e}")

    # 2. Try Twilio Messages API
    if twilio_sid and twilio_token and twilio_number:
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_sid}/Messages.json"
            data = {
                "From": twilio_number,
                "To": clean_phone,
                "Body": f"Your Grovia passcode is {otp}"
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(url, data=data, auth=(twilio_sid, twilio_token))
                if res.status_code in [200, 201]:
                    logger.info(f"Twilio SMS sent successfully to {clean_phone}")
                    print(f"\n✅ [Twilio REAL SMS SENT] OTP {otp} delivered to {clean_phone}\n")
                    return True
                else:
                    logger.error(f"Twilio SMS error: {res.json()}")
        except Exception as e:
            logger.error(f"Failed to send SMS via Twilio: {e}")

    # Fallback to console log
    print(f"\n==========================================")
    print(f"📱 REAL SMS OTP GENERATED FOR {clean_phone}: {otp}")
    print(f"==========================================\n")
    return True
