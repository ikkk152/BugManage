import re

from django_redis import get_redis_connection


def is_valid(phone):
    pattern = r"^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$"
    return bool(re.match(pattern, phone))


class RedisPhoneVerification:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(RedisPhoneVerification, cls).__new__(cls, *args, **kwargs)
            cls._instance.init_redis()
        return cls._instance

    def init_redis(self):
        self.redis = get_redis_connection("default")

    def set_verification_code(self, phone, code, expire=60):
        """
        存储验证码，并设置过期时间。

        :param phone: 电话号码
        :param code: 验证码
        :param expire: 验证码的过期时间（秒）
        """
        self.redis.setex(phone, expire, code)

    def get_verification_code(self, phone):
        """
        获取验证码。

        :param phone: 电话号码
        :return: 如果找到验证码，则返回验证码，否则返回None。
        """
        return self.redis.get(phone)

    def verify_code(self, phone, code):
        """
        校验验证码。

        :param phone: 电话号码
        :param code: 待校验的验证码
        :return: 如果验证码正确，则返回True，否则返回False。
        """
        stored_code = self.get_verification_code(phone).decode()
        return stored_code == code

    def delete_code(self, phone):
        """
        删除验证码。

        :param phone: 电话号码
        """
        self.redis.delete(phone)


redis_phone_verification = RedisPhoneVerification()
