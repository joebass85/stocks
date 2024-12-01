import requests,time,sys#,smtplib,os
from bs4 import BeautifulSoup

# variable setups
stocks = []
fileName = "log-stock.txt"
DSTr = "EST"
#EMAIL = os.environ.get('EMAILADDR')
#PASS = os.environ.get('EMAILPASSWD')

# Adding arguments from command line to the stocks list
num_args = len(sys.argv)
for i in range(1,num_args):
    stocks.append(sys.argv[i])

# Parsing out today's date
year = str(time.localtime()).split('(')[1].split(',')[0].split('=')[1]
month = str(time.localtime()).split('(')[1].split(',')[1].split('=')[1]
day = str(time.localtime()).split('(')[1].split(',')[2].split('=')[1]
current_day = f"Today's Date: {month}/{day}/{year}."

for stock in stocks:
    # Getting the web data for each stock
    stock_link = f'https://finance.yahoo.com/quote/{stock}?p={stock}'
    source = requests.get(stock_link,timeout=10).text
    soup = BeautifulSoup(source,'lxml')

    # This try-except block helps keep the script moving through errors.
    # Parsing out the stock_num tends to break a lot. Idk why.
    try:
        stock_num = soup.find("fin-streamer",class_="livePrice yf-1tejb6").text
    except:
        stock_num = f'Could not get data point. Check {stock_link} for current price per share.'

    # Parsing out the current time
    tH = str(time.localtime()).split('(')[1].split(',')[3].split('=')[1]
    tM = str(time.localtime()).split('(')[1].split(',')[4].split('=')[1]
    tS = str(time.localtime()).split('(')[1].split(',')[5].split('=')[1]
    isDST = time.localtime()[-1]

    # More formatting bits. If the hour/minute/second is 0-9, this will add a leading 0 so that it is always 2 digits long
    tHint = int(tH)
    if tHint < 10:
        tH = "0" + tH
    tMint = int(tM)
    if tMint < 10:
        tM = "0" + tM
    tSint = int(tS)
    if tSint < 10:
        tS = "0" + tS
    if isDST == True:
        DSTr = "EDT"

    current_time = f'\tCurrent time is {tH}:{tM}:{tS} {DSTr}.'

    # The if-elif-else statement here is really just for formatting in the log file
    # It could just be a single block of the 'with open...' code
    with open(fileName,"a") as f:
        if stock == stocks[0]:
            f.write(current_day)
            f.write("\n\n")
            f.write(stock)
            f.write("\n")
            f.write(current_time)
            f.write("\n\tCurrent price per share is: $")
            f.write(stock_num)
            f.write("\n\n")
        elif stock == stocks[-1]:
            f.write(stock)
            f.write("\n")
            f.write(current_time)
            f.write("\n\tCurrent price per share is: $")
            f.write(stock_num)
            f.write("\n\n")
        else:
            f.write(stock)
            f.write("\n")
            f.write(current_time)
            f.write("\n\tCurrent price per share is: $")
            f.write(stock_num)
            f.write("\n\n")
        #print(stock,stock_num)

# Setting up the email connection.
# This is set up for use with Gmail, but can be configured to any mail server
'''with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL,PASS)

    with open(fileName,'r') as f:
        attachment = f.read()

    subject = "Stock Prices are in!"
    body = "You have new stock prices to check. Go check them out!"
    msg = f'Subject: {subject}\n\n{attachment}'

    smtp.sendmail(EMAIL,EMAIL,msg)'''
