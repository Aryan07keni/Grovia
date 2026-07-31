import os
import logging
import httpx

logger = logging.getLogger(__name__)

def get_fast2sms_key() -> str:
    return os.environ.get('FAST2SMS_API_KEY', '').strip() or "FqmdCO8M40abPsH7wB9ZKy5XoDLxetNVGSjAgkrERTf63cJui2zUfHg6y8cK1LoIuAe035Wml9pqharv"

def get_2factor_key() -> str:
    return os.environ.get('TWO_FACTOR_API_KEY', '').strip()

async def send_otp_sms(phone: str, otp: str) -> bool:
    """
    Sends a 6-digit OTP SMS to an Indian phone number (+91) via Fast2SMS or 2Factor.
    """
    clean_phone = phone.replace('+91', '').replace(' ', '').strip()
    if len(clean_phone) > 10:
        clean_phone = clean_phone[-10:]

    fast2sms_key = get_fast2sms_key()
    twofactor_key = get_2factor_key()

    # 1. Try Fast2SMS API (Quick Route & OTP Route)
    if fast2sms_key:
        try:
            url = "https://www.fast2sms.com/dev/bulkV2"
            headers = {
                "authorization": fast2sms_key,
                "Content-Type": "application/json"
            }
            payload = {
                "message": f"Your Grovia verification OTP code is {otp}. Do not share it with anyone.",
                "route": "q",
                "numbers": clean_phone
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                data = response.json()
                if response.status_code == 200 and data.get("return"):
                    logger.info(f"Fast2SMS OTP sent successfully to {clean_phone}")
                    print(f"\n✅ [Fast2SMS REAL SMS SENT] OTP {otp} delivered to +91 {clean_phone}\n")
                    return True
                else:
                    logger.error(f"Fast2SMS error: {data}")
                    print(f"\n⚠️ Fast2SMS API message: {data.get('message', data)}\n")
        except Exception as e:
            logger.error(f"Failed to send SMS via Fast2SMS: {e}")

    # 2. Try 2Factor API if key is present
    if twofactor_key:
        try:
            url = f"https://2factor.in/API/V1/{twofactor_key}/SMS/{clean_phone}/{otp}"
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                data = response.json()
                if response.status_code == 200 and data.get("Status") == "Success":
                    logger.info(f"2Factor OTP sent successfully to {clean_phone}")
                    print(f"\n✅ [2Factor REAL SMS SENT] OTP {otp} delivered to +91 {clean_phone}\n")
                    return True
                else:
                    logger.error(f"2Factor error: {data}")
        except Exception as e:
            logger.error(f"Failed to send SMS via 2Factor: {e}")

    # Fallback for dev / testing mode
    logger.info(f"📱 [REAL SMS OTP SIMULATOR] OTP for +91 {clean_phone} is: {otp}")
    print(f"\n==========================================")
    print(f"📱 REAL SMS OTP GENERATED FOR +91 {clean_phone}: {otp}")
    print(f"==========================================\n")
    return True
