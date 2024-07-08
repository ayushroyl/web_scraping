import os
import telebot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Function to scrape information based on roll number
def scrape_info(roll_number):
    # Set Chrome options for headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    
    # Instantiate Chrome WebDriver with headless mode
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        #  Rest of the code remains the same
        driver.get("https://lnmuniversity.com/LNMU_ERP/SearchResultFirstPart_22_25.aspx")
        roll_number_input = driver.find_element(By.ID, "txtRollNo")
        submit_button = driver.find_element(By.ID, "btnSearch")
        roll_number_input.send_keys(roll_number)
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "lbltotmarks")))
        student_name = driver.find_element(By.ID, "lblcname").text.strip()
        roll_num = driver.find_element(By.ID, "lblrollno").text.strip()
        college_name = driver.find_element(By.ID, "lblcollegename").text.strip()
        course_name = driver.find_element(By.ID, "lblcoursename").text.strip()
        com_sub = driver.find_element(By.ID, "lblcompsub").text.strip()
        com_mark = driver.find_element(By.ID, "lblcompmarks").text.strip()
        alt_sub = ""
        try:
            alt_sub = driver.find_element(By.ID, "lblaltsub").text.strip()
        except:
            pass
        alt_mark = ""
        try:
            alt_mark = driver.find_element(By.ID, "lblaltmarks").text.strip()
        except:
            pass
        hon_sub = driver.find_element(By.ID, "lblhonsub").text.strip()
        hon_mark = driver.find_element(By.ID, "lblhonmarks").text.strip()
        hon_prac = driver.find_element(By.ID, "lblhonprac").text.strip()
        hon2_sub = driver.find_element(By.ID, "lblhonsub3").text.strip()
        hon2_mark = driver.find_element(By.ID, "lblhonmarks3").text.strip()
        subsid_sub = driver.find_element(By.ID, "lblsubsidsub").text.strip()
        subsid_mark = driver.find_element(By.ID, "lblsubsidmarks").text.strip()
        subsid_prac = driver.find_element(By.ID, "lblsubsidprac").text.strip()
        subsid2_sub = driver.find_element(By.ID, "lblsubsidsub2").text.strip()
        subsid2_mark = driver.find_element(By.ID, "lblsubsidmark2").text.strip()
        subsid2_prac = driver.find_element(By.ID, "lblsubsidprac2").text.strip()
        status = driver.find_element(By.ID, "lblstatus").text.strip()
        total_mark = driver.find_element(By.ID, "lbltotmarks").text.strip()
        response_message = f"LNMU - Statement of Marks\n\n"\
            f"Student Name:     {student_name}\n"\
            f"College Name:     {college_name}\n"\
            f"Roll Number:        {roll_num}\n"\
            f"Course Name:      {course_name}\n\n"\
            f"~Subjects~                               ~Marks~\n\n"\
            f"{com_sub}:                                    {com_mark}\n"
        if alt_sub:
            response_message += f"{alt_sub}:                                 {alt_mark}\n"
        response_message += f"{hon_sub}:               {hon_mark} + {hon_prac}\n"\
            f"{hon2_sub}:              {hon2_mark}\n"\
            f"{subsid_sub}:                                   {subsid_mark} + {subsid_prac}\n"\
            f"{subsid2_sub}:                       {subsid2_mark} + {subsid2_prac}\n\n"\
            f"Total Marks :                              {total_mark}\n"\
            f"Status :                                       {status}\n\n"\
            f"Note: (+) if you have practical sub. then only show marks after '+'\n Build by ~ @ayushroyl"
         
         # Send 'output' to Telegram
        return response_message
    except Exception as e:
        print(e)
        return "Invalid roll number\nPlease enter correct one"
    finally:
        # Make sure to quit the WebDriver instance after use
        driver.quit()

# Initialize Telegram bot
bot = telebot.TeleBot("BOT_TOKEN")

# Command handler for the /start command
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Welcome! Send me a roll number to get the Result.')

# Message handler for all messages
@bot.message_handler(func=lambda message: True)
def echo(message):
    wait_message = bot.send_message(message.chat.id, f"Hey, {message.chat.first_name}! Please wait while I fetch the result...")
    roll_number = message.text
    info = scrape_info(roll_number)
    bot.delete_message(message.chat.id, wait_message.message_id)
    bot.reply_to(message, info)

# Start the bot
print("Bot is running")
bot.polling()
