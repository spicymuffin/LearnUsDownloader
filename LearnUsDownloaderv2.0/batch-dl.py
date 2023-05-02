from pyquery import PyQuery as pq
import os
import LearnUsDownloader as ld
import datetime
import requests

#proveide cookies! view them through element inspector in chrome
cookies = {

}

#set course ID
params = {
    'id': '235881', # course ID
}


course_response = requests.get(
    'https://ys.learnus.org/course/view.php', params=params, cookies=cookies)


# path
CURR_PATH = os.path.dirname(os.path.abspath(__file__))

# vod list
fldrs = []

# bunch of parsing
doc = pq(course_response.content)
curr_week = doc('#course-all-sections')
lst = curr_week('.weeks, .ubsweeks, .ubformat').children()

for week in lst:
    w = pq(week)
    fldr = [w('span').eq(0).html(), []]
    a = list(w.find('.activityinstance'))

    vod = None
    for i in a:
        j = pq(i).find('[href]')
        m = pq(i).find('.instancename')
        href = j.attr("href")
        title = m.remove("span").html()
        vod = [href, title]
        fldr[1].append(vod)
    fldrs.append(fldr)

# process folders
for i in range(len(fldrs)):
    for j in range(len(fldrs[i][1])):
        fldrs[i][1][j][0] = fldrs[i][1][j][0].replace(
            "https://ys.learnus.org/mod/vod/view.php?id=", "")

# make batch folder
now = datetime.datetime.now()
dt_string = now.strftime("%d %B, %Y %H-%M-%S")
wrkdir = CURR_PATH + '\\' + dt_string
os.mkdir(wrkdir)


def sanitize(s):
    """prevents invalid filenames

    Args:
        s (str): filename to sanitize

    Returns:
        str: sanitized filename
    """
    return "".join(x for x in s if not (x in ['\\', '/', ':', '*', '?', '"', '<', '>', '|']))


for i in range(len(fldrs)):
    week_folder_name = sanitize(fldrs[i][0])
    print(f"downloading: {week_folder_name}")
    week_folder_path = wrkdir + '\\' + week_folder_name
    os.mkdir(week_folder_path)
    for j in range(len(fldrs[i][1])):

        # set VOD ID
        params = {
            'id': fldrs[i][1][j][0]
        }

        vod_response = requests.get('https://ys.learnus.org/mod/vod/viewer.php',
                                    params=params, cookies=cookies)

        dc = vod_response.content.decode()
        ind = dc.find('<source src="') + len('<source src="')

        base_url = ""
        scan_i = ind
        while dc[scan_i] != '"':
            base_url += dc[scan_i]
            scan_i += 1

        # sorry, this is a mess but this gets rid of "/index.m3u8"
        base_url = "/".join(base_url.split("/")[:-1])

        file_absolute_path = week_folder_path + \
            '\\' + sanitize(fldrs[i][1][j][1]) + ".mp4"
        print(f"{fldrs[i][0]}: {fldrs[i][1][j][1]}")
        ld.download_video(base_url, file_absolute_path)
