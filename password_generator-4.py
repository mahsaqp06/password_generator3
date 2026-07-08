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


# ---------- رنگ‌های کنسول (برای زیباسازی خروجی) ----------
class Color:
    RESET = "\033[0m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"


def print_banner():
    width = 46
    print(Color.CYAN + "╔" + "═" * width + "╗")
    print("║" + " مولد رمز عبور تصادفی و امن ".center(width) + "║")
    print("╚" + "═" * width + "╝" + Color.RESET)


def print_line():
    print(Color.CYAN + "-" * 48 + Color.RESET)


def get_valid_length():
    """طول رمز را از کاربر می‌گیرد و تا زمانی که معتبر نباشد دوباره می‌پرسد."""
    while True:
        raw = input(f"{Color.BOLD}طول رمز عبور (حداقل 4، پیش‌فرض 12): {Color.RESET}").strip()
        if raw == "":
            return 12
        if raw.isdigit() and int(raw) >= 4:
            return int(raw)
        print(f"{Color.RED}✗ لطفاً عددی صحیح و حداقل 4 وارد کنید.{Color.RESET}")


def get_yes_no(question, default=True):
    """سؤال بله/خیر با مقدار پیش‌فرض، تا کاربر بدون تایپ فقط Enter هم بزند کار کند."""
    hint = "Y/n" if default else "y/N"
    raw = input(f"{question} ({hint}): ").strip().lower()
    if raw == "":
        return default
    return raw == "y"


def strength_color(strength):
    return {
        "ضعیف": Color.RED,
        "متوسط": Color.YELLOW,
        "قوی": Color.GREEN,
    }.get(strength, Color.RESET)


def show_password_result(password, strength):
    print_line()
    print(f"{Color.BOLD}رمز عبور تولید شده:{Color.RESET}  {Color.BOLD}{password}{Color.RESET}")
    color = strength_color(strength)
    print(f"{Color.BOLD}سطح امنیت:{Color.RESET}          {color}{strength}{Color.RESET}")
    print_line()


# ---------- بخش اصلی برنامه (منوی تعاملی) ----------
def main():
    print_banner()

    while True:
        print()
        length = get_valid_length()
        use_upper = get_yes_no("حروف بزرگ استفاده شود؟")
        use_digits = get_yes_no("عدد استفاده شود؟")
        use_symbols = get_yes_no("نماد (!@#...) استفاده شود؟")

        generator = PasswordGenerator()
        generator.set_length(length)
        generator.set_use_upper(use_upper)
        generator.set_use_digits(use_digits)
        generator.set_use_symbols(use_symbols)

        password = generator.generate()
        strength = PasswordStrengthChecker.check(password)
        show_password_result(password, strength)

        if not get_yes_no("\nیک رمز دیگر هم بسازیم؟", default=False):
            print(f"\n{Color.CYAN}به امید دیدار! 👋{Color.RESET}")
            break


if __name__ == "__main__":
    main()
