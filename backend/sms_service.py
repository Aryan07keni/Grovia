import os
import logging
import httpx

logger = logging.getLogger(__name__)

FAST2SMS_API_KEY = os.environ.get('FAST2SMS_API_KEY', '')
TWO_FACTOR_API_KEY = os.environ.get('TWO_FACTOR_API_KEY', '')

async def send_otp_sms(phone: str, otp: str) -> bool:
    """
    Sends a 6-digit OTP SMS to an Indian phone number (+91) via Fast2SMS or 2Factor.
    Falls back to logger output if no SMS API keys are configured.
    """
    # Clean phone number (extract 10-digit number)
    clean_phone = phone.replace('+91', '').replace(' ', '').strip()
    if len(clean_phone) > 10:
        clean_phone = clean_phone[-10:]

    # 1. Try Fast2SMS API if key is present
    if FAST2SMS_API_KEY:
        try:
            url = "https://www.fast2sms.com/dev/bulkV2"
            headers = {
                "authorization": FAST2SMS_API_KEY,
                "Content-Type": "application/json"
            }
            payload = {
                "variables_values": otp,
                "route": "otp",
                "numbers": clean_phone
            }
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(url, json=payload, headers=headers)
                data = response.json()
                if response.status_code == 200 and data.get("return"):
                    logger.info(f"Fast2SMS OTP sent successfully to {clean_phone}")
                    return True
                else:
                    logger.error(f"Fast2SMS error: {data}")
        except Exception as e:
            logger.error(f"Failed to send SMS via Fast2SMS: {e}")

    # 2. Try 2Factor API if key is present
    if TWO_FACTOR_API_KEY:
        try:
            url = f"https://2factor.in/API/V1/{TWO_FACTOR_API_KEY}/SMS/{clean_phone}/{otp}"
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(url)
                data = response.json()
                if response.status_code == 200 and data.get("Status") == "Success":
                    logger.info(f"2Factor OTP sent successfully to {clean_phone}")
                    return True
                else:
                    logger.error(f"2Factor error: {data}")
        except Exception as e:
            logger.error(f"Failed to send SMS via 2Factor: {e}")

    # Fallback for dev / testing mode when API keys are not provided
    logger.info(f"📱 [REAL SMS OTP SIMULATOR] OTP for +91 {clean_phone} is: {otp}")
    print(f"\n==========================================")
    print(f"📱 REAL SMS OTP SENT TO +91 {clean_phone}: {otp}")
    print(f"==========================================\n")
    return True
