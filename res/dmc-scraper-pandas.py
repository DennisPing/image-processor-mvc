import pandas as pd

# A script that scrapes the DMC Color table from the URL link.
# def main():
# 	scrape_colors()
# 	print("Scraping completed!")

def scrape_colors():
    url = 'http://my.crazyartzone.com/dmc.asp'
    print('\nRequesting page ' + url + '...')

    # Let Pandas find the table, parse it, and extract columns 1 thru 5.
    df = pd.read_html(url) 
    df = df[0].iloc[:,[1,2,3,4,5]]
    df.to_csv("dmc-colors.csv")

# if __name__ == '__main__':
# 	main()