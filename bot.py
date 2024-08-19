from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import re

# اطلاعات ربات
api_id = "29500143"  # از My Telegram API دریافت کنید
api_hash = "be70b8bc68ca833b61ccc5011157c5a4"  # از My Telegram API دریافت کنید
bot_token = "6479209094:AAGA0nhnWrFIKowXUItKQXCZaoOgy54oiFQ"  # از BotFather دریافت کنید

app = Client("anti_link_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# متغیرهای وضعیت
activation_code = None
group_username = None  # متغیر برای ذخیره نام کاربری گروه تلگرام

# الگوی Regex برای شناسایی لینک‌ها
link_pattern = re.compile(
    r'(?:http|https|ftp):\/\/[^\s/$.?#].[^\s]*'
    r'|(?:www\.)[^\s/$.?#].[^\s]*'
    r'|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}(?:\/[^\s]*)?'
)

# دکمه برای مشاهده تعرفه‌ها
def get_pricing_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("تعرفه‌ها", callback_data="show_pricing")]
    ])

# دکمه‌های تعرفه‌ها
def get_pricing_options():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("1 ماهه - 30 هزار تومان", callback_data="pricing_1_month")],
        [InlineKeyboardButton("2 ماهه - 55 هزار تومان", callback_data="pricing_2_months")],
        [InlineKeyboardButton("3 ماهه - 80 هزار تومان", callback_data="pricing_3_months")],
        [InlineKeyboardButton("4 ماهه - 110 هزار تومان", callback_data="pricing_4_months")],
        [InlineKeyboardButton("5 ماهه - 140 هزار تومان", callback_data="pricing_5_months")]
    ])

# دکمه "فرستادن رسید"
def get_receipt_button():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("فرستادن رسید", url="https://t.me/Sepi_North")]
    ])

# اطلاعات تعرفه‌ها
pricing_info = {
    "pricing_1_month": "تعرفه 1 ماهه: 30 هزار تومان\n\n"
                        "شماره کارت: 6037998256366898\n"
                        "نام صاحب کارت: سپنتا زارع",
    "pricing_2_months": "تعرفه 2 ماهه: 55 هزار تومان\n\n"
                         "شماره کارت: 6037998256366898\n"
                         "نام صاحب کارت: سپنتا زارع",
    "pricing_3_months": "تعرفه 3 ماهه: 80 هزار تومان\n\n"
                         "شماره کارت: 6037998256366898\n"
                         "نام صاحب کارت: سپنتا زارع",
    "pricing_4_months": "تعرفه 4 ماهه: 110 هزار تومان\n\n"
                         "شماره کارت: 6037998256366898\n"
                         "نام صاحب کارت: سپنتا زارع",
    "pricing_5_months": "تعرفه 5 ماهه: 140 هزار تومان\n\n"
                         "شماره کارت: 6037998256366898\n"
                         "نام صاحب کارت: سپنتا زارع"
}

@app.on_message(filters.command("start"))
def start_command(client, message):
    welcome_text = "سلام! من یک ربات ضد لینک هستم. برای مشاهده تعرفه‌ها، لطفاً دکمه زیر را فشار دهید."
    app.send_message(
        chat_id=message.chat.id,
        text=welcome_text,
        reply_markup=get_pricing_button()
    )

@app.on_message(filters.command("set_activation_code"))
def set_activation_code(client, message):
    global activation_code
    if message.chat.type == "private":
        code = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
        if code == "sepanta":
            activation_code = code
            app.send_message(
                chat_id=message.chat.id,
                text="کد فعال‌سازی با موفقیت تنظیم شد."
            )
        else:
            app.send_message(
                chat_id=message.chat.id,
                text="کد فعال‌سازی نادرست است."
            )

@app.on_message(filters.command("set_group_username"))
def set_group_username(client, message):
    global group_username
    if message.chat.type == "private":
        link = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else ""
        if link.startswith("@"):
            group_username = link
            app.send_message(
                chat_id=message.chat.id,
                text="نام کاربری گروه با موفقیت تنظیم شد."
            )
        else:
            app.send_message(
                chat_id=message.chat.id,
                text="لطفاً نام کاربری گروه را به صورت @username وارد کنید."
            )

@app.on_callback_query(filters.regex("show_pricing"))
def show_pricing(client, callback_query):
    message = callback_query.message
    app.edit_message_text(
        chat_id=message.chat.id,
        message_id=message.id,
        text="تعرفه‌های موجود:",
        reply_markup=get_pricing_options()
    )
    app.answer_callback_query(callback_query.id)

@app.on_callback_query(filters.regex("pricing_"))
def handle_pricing_selection(client, callback_query):
    global activation_code
    callback_data = callback_query.data
    pricing_text = pricing_info.get(callback_data, "اطلاعات تعرفه در دسترس نیست.")
    
    # ارسال اطلاعات تعرفه و شماره کارت
    app.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.id,
        text=pricing_text,
        reply_markup=get_receipt_button()  # اضافه کردن دکمه "فرستادن رسید"
    )
    
    # ارسال پیام تایید رسید
    user_id = callback_query.from_user.id
    app.send_message(
        chat_id=user_id,
        text="بعد از فرستادن رسید صبر کنید تا رسیدتون تایید شه."
    )
    
    app.answer_callback_query(callback_query.id)

@app.on_callback_query(filters.regex("https://t.me/Sepi_North"))
def handle_receipt_button(client, callback_query):
    # ارسال پیام جدید بعد از کلیک روی دکمه "فرستادن رسید"
    user_id = callback_query.from_user.id
    app.send_message(
        chat_id=user_id,
        text="لطفاً صبر کنید، رسید شما در حال بررسی است."
    )
    
    app.answer_callback_query(callback_query.id)

@app.on_message(filters.text)
def anti_link(client, message):
    global activation_code, group_username
    if activation_code == "sepanta" and group_username:
        if message.chat.username != group_username.lstrip("@"):
            return  # اگر پیام در گروه نادرست است، به هیچ کاری نپردازید
        if link_pattern.search(message.text):
            try:
                message.delete()
                print("Link deleted")
            except Exception as e:
                print(f"Failed to delete message: {e}")

if __name__ == "__main__":
    app.run()
