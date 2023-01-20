import requests
import re
from bs4 import BeautifulSoup

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
# header = {'User-Agent': user_agent, "Referer": "https://www.pixiv.net/"}
header = {'User-Agent': user_agent}

url = str(input("Enter url: "))

# download
response = requests.get(url, headers=header)

# for log
file_type = "txt"

if len(url.split(".")) == 4:
  file_type = url.split(".")[-1]

# remove special char
file_name = "_".join(url.split("/")[2:])
file_name = ".".join(file_name.split(".")[:3])

with open(f'{file_name}.{file_type}', mode="wb") as f:
  f.write(response.content)

if file_type == "txt":
  soup = BeautifulSoup(response.content, 'html.parser')

  links = soup.find_all("link")

  # download picture
  originalLink = re.search(
    "(https:\/\/i.pximg.net\/img-original/[\w\/:%#\$&\?\(\)~\.=\+\-]+)\.(png|jpg)",
    str(response.content))
  if originalLink:
    originalLink = originalLink.group()

    # save
    with open(f'{file_name}.{originalLink.split(".")[3]}', mode="wb") as f:
      f.write(requests.get(originalLink, headers=header).content)
      print("The picture is downloaded")
  else:
    originalLink = "null"

  # save links as yaml
  with open(f'links_{file_name}.yml', mode="w") as f:
    images = list(
      map(
        lambda t: ".".join(t),
        re.findall("(https:\/\/[\w\/:%#\$&\?\(\)~\.=\+\-]+)\.(jpg|png)",
                   str(response.content))))
    links = re.findall("(https:\/\/[\w\/:%#\$&\?\(\)~\.=\+\-]+)",
                       str(response.content))

    pad = '\n  - '

    f.write(
      f'original: {originalLink}\n\nimages: \n  - {pad.join(images)}\n\nlinks: \n  - {pad.join(links)}'
    )

    print("Links are in the yaml file")
