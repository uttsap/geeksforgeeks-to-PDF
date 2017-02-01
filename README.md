## geeksforgeeks.org to PDF

The python script crawls the URL provided and downloads the webpages as PDF basd on keywords provided in the script.

#### To Use

- Add your own [PDFCROWD](https://pdfcrowd.com) *username* and *API KEY* within `.env` file!
- Install dependencies using `pip install -r requirements.txt`
- Modify the code based on URL and keyword required to target a category
- Run the script using `python geeksforgeeks2pdf.py`
- Wait till download finishes

**Note :** The PDFCROWD API is valid for 100 conversions only. An error is thrown when the API exceeds the conversion limit.
