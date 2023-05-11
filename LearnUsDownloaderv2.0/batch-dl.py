from pyquery import PyQuery as pq
import os
import LearnUsDownloader as ld
import datetime
import time
import threading
import sys
import queue
import requests

MULTITHREADED = True
MAX_ACTIVE_THREAD_COUNT = 7

# provide cookies. i used https://curlconverter.com/ to do that!
# just copy any request that has cookies in it and copy the request as curl (bash)
cookies = {

}

params = {
    'id': '228313',  # course ID
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
        if vod[0] != None and "/vod/" in vod[0]:
            fldr[1].append(vod)
    fldrs.append(fldr)

# print(*fldrs, sep="\n")

# process folders
for i in range(len(fldrs)):
    for j in range(len(fldrs[i][1])):
        fldrs[i][1][j][0] = fldrs[i][1][j][0].replace(
            "https://ys.learnus.org/mod/vod/view.php?id=", "")


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


# the reporting thread
def reporter(q):
    status = {}
    while threading.active_count() != MAX_ACTIVE_THREAD_COUNT+2:
        time.sleep(0.25)

    while threading.active_count() > 2:
        msg = q.get()
        if msg[0] == "update":
            path, total, size = msg[1:]
            status[path] = (total, size)
            # update the screen here
            show_progress(status)
        elif msg[0] == "done":
            del status[path]
    print("")


def show_progress(status):
    line = ""
    for path in status:
        (total, size) = status[path]
        line = line + \
            f"  {path}: {format(size, f' >{len(str(total))}')}/{total}({format(size/total*100, ' >6.2f')}%)"
    sys.stdout.write("\r"+line)
    sys.stdout.flush()


if MULTITHREADED == False:
    for i in range(len(fldrs)):
        week_folder_name = sanitize(fldrs[i][0])
        print(f"downloading: {week_folder_name}")
        week_folder_path = wrkdir + '\\' + week_folder_name
        os.mkdir(week_folder_path)
        for j in range(len(fldrs[i][1])):

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
else:
    q = queue.Queue()

    reporter_thread = threading.Thread(target=reporter, args=(q, ))
    reporter_thread.start()
    for i in range(len(fldrs)):
        week_folder_name = sanitize(fldrs[i][0])
        # print(f"downloading: {week_folder_name}")
        week_folder_path = wrkdir + '\\' + week_folder_name
        os.mkdir(week_folder_path)
        for j in range(len(fldrs[i][1])):

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
            # print(f"{fldrs[i][0]}: {fldrs[i][1][j][1]}")

            while threading.active_count() >= MAX_ACTIVE_THREAD_COUNT+2:
                time.sleep(0.25)

            tr = threading.Thread(target=ld.download_video_multithread, args=(
                base_url, file_absolute_path, f"{i+1}/{j+1}", q))
            tr.start()
