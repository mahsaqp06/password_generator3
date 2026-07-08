# -*- coding: utf-8 -*-
"""
مولد رمز عبور تصادفی با معیارهای امنیتی
درس: برنامه‌سازی پیشرفته - پیاده‌سازی شیءگرا (کپسوله‌سازی، getter/setter)
"""

import random
import string


class PasswordGenerator:
    """
    این کلاس مسئول ساخت رمز عبور تصادفی بر اساس تنظیمات کاربر است.
    از کپسوله‌سازی استفاده شده: ویژگی‌ها خصوصی هستند و فقط از طریق
    متدهای get/set قابل دسترسی و تغییرند.
    """

    def __init__(self, length=12, use_upper=True, use_digits=True, use_symbols=True):
        self._length = length
        self._use_upper = use_upper
        self._use_digits = use_digits
        self._use_symbols = use_symbols

    # ---------- Getterها و Setterها ----------
    def get_length(self):
        return self._length

    def set_length(self, length):
        if length < 4:
            raise ValueError("طول رمز عبور نباید کمتر از 4 باشد.")
        self._length = length

    def set_use_upper(self, value):
        self._use_upper = value

    def set_use_digits(self, value):
        self._use_digits = value

    def set_use_symbols(self, value):
        self._use_symbols = value

    # ---------- ساخت مجموعه کاراکترهای مجاز ----------
    def _build_char_pool(self):
        pool = list(string.ascii_lowercase)
        if self._use_upper:
            pool += list(string.ascii_uppercase)
        if self._use_digits:
            pool += list(string.digits)
        if self._use_symbols:
            pool += list("!@#$%^&*()-_=+")
        return pool

    # ---------- تولید رمز عبور ----------
    def generate(self):
        pool = self._build_char_pool()

        # ابتدا حداقل یک کاراکتر از هر دسته فعال را تضمین می‌کنیم
        password_chars = [random.choice(string.ascii_lowercase)]
        if self._use_upper:
            password_chars.append(random.choice(string.ascii_uppercase))
        if self._use_digits:
            password_chars.append(random.choice(string.digits))
        if self._use_symbols:
            password_chars.append(random.choice("!@#$%^&*()-_=+"))

        # بقیه کاراکترها را به صورت تصادفی از کل مجموعه پر می‌کنیم
        while len(password_chars) < self._length:
            password_chars.append(random.choice(pool))

        random.shuffle(password_chars)
        return "".join(password_chars[:self._length])


class PasswordStrengthChecker:
    """
    کلاسی جداگانه برای بررسی قدرت رمز عبور (تفکیک مسئولیت‌ها).
    """

    @staticmethod
    def check(password):
        score = 0
        if len(password) >= 8:
            score += 1
        if any(c.isupper() for c in password):
            score += 1
        if any(c.isdigit() for c in password):
            score += 1
        if any(c in "!@#$%^&*()-_=+" for c in password):
            score += 1

        if score <= 1:
            return "ضعیف"
        elif score in (2, 3):
            return "متوسط"
        else:
            return "قوی"


# ---------- بخش اصلی برنامه (منوی ساده) ----------
def main():
    print("=== مولد رمز عبور تصادفی ===")

    try:
        length = int(input("طول رمز عبور را وارد کنید (حداقل 4): "))
    except ValueError:
        length = 12
        print("ورودی نامعتبر بود، طول پیش‌فرض 12 در نظر گرفته شد.")

    use_upper = input("حروف بزرگ استفاده شود؟ (y/n): ").lower() == "y"
    use_digits = input("عدد استفاده شود؟ (y/n): ").lower() == "y"
    use_symbols = input("نماد (!@#...) استفاده شود؟ (y/n): ").lower() == "y"

    generator = PasswordGenerator()
    try:
        generator.set_length(length)
    except ValueError as e:
        print(e)
        return

    generator.set_use_upper(use_upper)
    generator.set_use_digits(use_digits)
    generator.set_use_symbols(use_symbols)

    password = generator.generate()
    strength = PasswordStrengthChecker.check(password)

    print(f"\nرمز عبور تولید شده: {password}")
    print(f"سطح امنیت: {strength}")


if __name__ == "__main__":
    main()
