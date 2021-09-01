import m3u8
import requests
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
import requests
from tqdm import tqdm
import binascii


def get_input():
    """
    get url, video file name from user
    :return: raw_url(ends with ".mp4" or ".ts"), file_name(ends with ".mp4")
    """
    raw_url = input("enter the url you copied from the browser (ex. https://.../segment-1-v1-a1.ts) : ")
    file_name = input("enter the name of the video file will be downloaded (ex. video.mp4) : ")
    if file_name[-4:] != ".mp4":
        file_name += ".mp4"
    return raw_url, file_name


def get_base_url(raw_url):
    """
    truncate .ts segment
    :param raw_url: input url from user
    :return: base_url(ends with "mp4")
    """
    if ".ts" in raw_url:
        raw_url = "/".join(raw_url.split("/")[:-1])
    print(raw_url)
    return raw_url


def get_playlist(base_url):
    """
    fetch a playlist from base_url
    :param base_url: truncated url
    :return: m3u8 playlist object
    """
    tmp_playlist = m3u8.load(uri=base_url+"/index.m3u8")
    return tmp_playlist


def decrypt_video(encrypted_data, key, iv):
    """
    as a .ts file is encrypted with AES-128 (CBC) algorithm, decrypt it using pycryptodome
    :param encrypted_data: .ts file data
    :param key: fetched .key file
    :param iv: sequence number (iv is not specified)
    :return: decrypted segment
    """
    encrypted_data = pad(data_to_pad=encrypted_data, block_size=AES.block_size)
    aes = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
    decrypted_data = aes.decrypt(encrypted_data)
    return decrypted_data


def binify(x):
    """
    convert sequence number(int) to 128bit representation for AES-128 decryption
    """
    h = hex(x)[2:].rstrip('L')
    return binascii.unhexlify('0'*(32-len(h))+h)


def download_video():
    """
    download video (runner)
    """
    raw_url, file_name = get_input()
    base_url = get_base_url(raw_url)
    playlist = get_playlist(base_url)
    key = requests.get(playlist.keys[-1].absolute_uri).content
    seq_len = len(playlist.segments)
    for i in tqdm(range(seq_len)):
        seg = playlist.segments[i]
        data = requests.get(seg.absolute_uri).content
        iv = binify(i+1)
        data = decrypt_video(data, key, iv)
        with open(file_name,"ab" if i != 0 else "wb") as f:
            f.write(data)


if __name__ == "__main__":
    download_video()

