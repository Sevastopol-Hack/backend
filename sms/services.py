from smsaero import SmsAero
from config import SMS_EMAIL, SMS_KEY

class SmsAeroService:
    async def send_sms(self, username: int, message: str):
        api = SmsAero(SMS_EMAIL, SMS_KEY)
        res = api.send(username, message)
        assert res.get('success'), res.get('message')
        return res.get('data')