from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
from PyPDF2 import PdfFileMerger, PdfFileReader
import pdfkit
import pandas as pd
import matplotlib.pyplot as plt
from jinja2 import Template
from io import BytesIO
import binascii
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

host = "cit29.ru"
smtp_port = 25
user = "testmail@cit29.ru"
password = "Bycnherwbz@!!"


SUBJECT = "Test email from Python"
TO = "support@ittensive.com"
fr = "Артем "
FROM = "testmail@cit29.ru"


data = pd.read_csv("https://video.ittensive.com/python-advanced/data-9722-2019-10-14.utf.csv", na_values="NA", delimiter=";")
data = data.drop(columns=["Unnamed: 8"], axis=1)

dist = pd.DataFrame({"AdmArea": data["AdmArea"], "EDU_NAME" :data["EDU_NAME"], "PASSES_OVER_220" : data['PASSES_OVER_220']})
summ = dist["PASSES_OVER_220"].sum()
dist["AdmArea"] = dist["AdmArea"].str.replace(" административный округ", "")

groun_area = dist.drop(columns=["EDU_NAME"], axis=1).groupby(["AdmArea"]).agg("sum")

plt.rc('xtick', labelsize=9)
fig = plt.figure(figsize=(10, 10))

area = fig.add_subplot(1, 1, 1)
groun_area.plot.bar(ax=area, label="Распределение отличников по округам Москвы")
area.legend()
plt.xticks(range(0,len(groun_area.index)), groun_area.index, rotation=45, horizontalalignment='right')
#plt.show()
img = BytesIO()
plt.savefig(img)
group_school = dist.drop(columns=["AdmArea"], axis=1).sort_values(by=['PASSES_OVER_220'], ascending=False).reset_index()
school = group_school[0:1]["EDU_NAME"][0]
img = 'data:image/png;base64,' + binascii.b2a_base64(img.getvalue(), newline=False).decode("UTF-8")

html_template = '''<html>\r\n
<head>\r\n
    <title>Отчет</title>\r\n
    <charset meta="utf-8"/>\r\n
    <style>\r\n
        div {font-size: 17px;}\r\n
    </style>\r\n
</head>\r\n
<body>\r\n
    <h2>Распределение отличников по округам Москвы</h2>\r\n
    <img src="''' + img + '''">\r\n
    <div >общее число отличников (учеников, получивших более 220 баллов по ЕГЭ в Москве): {{data.summ}}</div>\r\n
    <div >название школы с лучшими результатами по ЕГЭ в Москве: {{data.school}}</div>\r\n
</body>\r\n
</html>'''


html = Template(html_template).render(data = {
    "summ": summ,
    "school": school})

with open ('result.html', 'w', encoding='utf-8') as result:
	result.write (html)

config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
options = {
    'page-size': 'A4',
    'header-right': '[page]',
    'encoding': "UTF-8",
}
pdfkit.from_string(html, 'result.pdf', configuration=config, options=options)

letter = MIMEMultipart()
letter["From"] = "testmail@cit29.ru"
letter["Subject"] = "ДЗ Артем, отчет по результатам ЕГЭ в 2018-2019 году"
letter["Content-Type"] = "text/html; charset=utf-8"
letter["To"] = TO

letter.attach(MIMEText(open("result.html", "r", encoding="UTF-8").read(), 'html'))

attachment = MIMEBase('application', "pdf")
attachment.set_payload(open("result.pdf", "rb").read())

attachment.add_header('Content-Disposition', 'attachment; filename="result.pdf"')
encoders.encode_base64(attachment)
letter.attach(attachment)

server = smtplib.SMTP(host, smtp_port)
server.ehlo()
server.starttls()
server.login(user, password)
server.sendmail(FROM, [TO], letter.as_string())
server.quit()


print(summ, school)
input()