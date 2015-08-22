import os
from time import sleep
import xml.etree.ElementTree as ET
import requests
from envs import get_env


class Yamaha():
    HOST = "http://54.64.108.46/vdc/vws_t2s.php"
    TEMPLATE = os.path.join(os.path.dirname(__file__), "./yamaha_template.xml")

    def __init__(self):
        self.key = get_env("yamaha_key")
        self.ver = get_env("yamaha_ver")

    def _create_xml(self, lyrics):
        tree = ET.parse(self.TEMPLATE)
        root = tree.getroot()
        lyrics_el = root.find("./Compose/LyricsBlock")
        for ly in lyrics:
            ET.SubElement(lyrics_el, "Lyrics").text = ly
        xml = ET.tostring(root, encoding="utf-8", method="xml")
        return xml

    def create_song(self, lyrics):
        # crete request
        url = self.HOST
        params = {
            "ope": "request",
            "ver": self.ver,
            "key": self.key
        }
        headers = {
            "Content-type": "application/octet-stream"
        }

        xml = self._create_xml(lyrics)
        accepted = requests.post(url, headers=headers, params=params, data=xml)

        ticket_id = -1
        retry_after = -1
        cookies = []
        if accepted.ok:
            accepted_xml = ET.fromstring(accepted.text)
            if accepted_xml.find("status").text != "ok":
                print("request error")
            else:
                ticket_id = accepted_xml.find("ticketId").text
                retry_after = float(accepted_xml.find("retryAfter").text)
                cookies = accepted.cookies

        mp3_url = ""
        if retry_after > 0:
            url = self.HOST
            params = {
                "ope": "query",
                "ver": self.ver,
                "id": ticket_id
            }
            sleep(retry_after)
            obserbed = requests.get(url, params=params, cookies=cookies)

            if obserbed.ok:
                obserbed_xml = ET.fromstring(obserbed.text)
                status = obserbed_xml.find("status").text

                if status == "done":
                    mp3_url = obserbed_xml.find("url").text
                elif status == "working":
                    retry_after = obserbed_xml.find("retry_after").text
                    retry_after = float(retry_after)
                elif status == "error":
                    retry_after = -1

        return mp3_url
