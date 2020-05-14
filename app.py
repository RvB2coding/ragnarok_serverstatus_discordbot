import os
import json
import time
import socket
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed


class Log:
    def message(self, message):
        message = "[{}] -> {}".format(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), message)
        return print(message)

class Config:
    def read_config(self, filename):
        with open(filename, encoding='utf-8') as File:
            self.config = json.load(File)


class Main(Config, Log):
    def __init__(self):
        self.read_config("config.json")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def check_socket(self, ip, port):
        result = self.socket.connect_ex((ip, port))
        if result:
            return False
        else:
            return True

    def send_discord(self, post_data):
        webhook = DiscordWebhook(url=self.config['discord-webhook-url'])
        
        embed = DiscordEmbed(color=242424)
        embed.set_author(name=self.config['server-name'], url=self.config['server-url'], icon_url=self.config['server-icon-url'])
        embed.set_footer(text='by sctnightcore')

        embed.set_timestamp()
        embed.add_embed_field(name='Login Server', 
            value= self.config['true-icon'] if post_data['Login'] else self.config['false-icon']
        )
        embed.add_embed_field(name='Char Server',
            value= self.config['true-icon'] if post_data['Char'] else self.config['false-icon']
        )
        embed.add_embed_field(name='Map Server',
            value= self.config['true-icon'] if post_data['Map'] else self.config['false-icon']
        )

        webhook.add_embed(embed)
        response = webhook.execute()
        self.message(response)
        self.message(post_data)
        assert response != 204

        
    def main_loop(self):
        while True:
            data = {}
            for i in self.config['data']:
                resulet = self.check_socket(i['Ip'], i['Port'])
                data[i['Name']] = resulet
            self.send_discord(data)
            time.sleep(self.config['time-sleep'])


if __name__ == "__main__":
    i = Main()
    i.main_loop()