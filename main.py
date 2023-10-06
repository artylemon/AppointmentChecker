import telebot
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BOT_TOKEN = ''  # Here goes the bot token from the BotFather
bot = telebot.TeleBot(BOT_TOKEN)


def bookings_available():
    booking_site_url: str = (
        "https://terminvereinbarung.leipzig.de/m/leipzig-ba/extern/calendar/session_expired?uid=b76cab25-49bd-44e3"
        "-950d-aab715881ea7&wsid=db409d9b-ed62-47a9-94b7-9fcec525a6ac&lang=de"
    )
    driver = webdriver.Chrome()
    driver.get(booking_site_url)
    driver.implicitly_wait(10)

    # Start appointment check
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'Neue Terminsuche beginnen'))
    ).click()

    # set appointment priority with js
    element = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="service_81c1868f-30d3-4aef-b1df-5ce29d6a6158"]'))
    )
    driver.execute_script("arguments[0].value = 1", element)

    # click on the button to get to the next page
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/main/form/div/div/button'))
    ).click()

    # check the desired location with js (normal selenium click was not working)
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div/main/form/div/section[1]/fieldset/div[2]/div[2]/input'))
    ).click()
    # driver.execute_script("arguments[0].checked = true", element)

    # go to the next page
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div[1]/main/form/div/div/button'))
    ).click()

    # testing if there is a div present with the error of no appointments
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, 'error_no_appointment_found'))
        )
    except TimeoutException:
        # if it is not the case, there are appointments
        driver.quit()
        return True

    # if we found the div, no appointments present
    driver.quit()
    return False


# Method to check if the bot is active
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Active")


# Will use this method to add users to the checking list
@bot.message_handler(commands=['add'])
def send_welcome(message):
    f = open("users.txt", "a")
    f.write(str(message.from_user.id))
    f.write('\n')
    f.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    user_id = ''
    # bot.infinity_polling()
    # bot = telebot.TeleBot(BOT_TOKEN)
    if bookings_available():
        bot.send_message(chat_id=user_id, text='Some booking slots available!')
