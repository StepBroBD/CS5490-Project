import random
import json
import socket
import uuid
import time
import os
from pathlib import Path
from typing import Tuple
from project.common import send_all, recv_all
from rich import print


class Attack:
    def __init__(self, host: str, port: int, n: int) -> None:
        self.host = host
        self.port = port
        self.n = n

        self.true_positives = 0
        self.false_positives = 0
        self.true_negatives = 0
        self.false_negatives = 0

        # ["PUT", "DELETE", "PATCH", "HEAD"]
        self.http_methods = ["GET", "POST"]
        self.http_versions = ["HTTP/1.0", "HTTP/1.1", "HTTP/2.0"]
        self.http_endpoints = [
            "/",
            "/login",
            "/register",
            "/logout",
            "/dashboard"
        ]

        self.required_headers = [
            "Accept",
            "User-Agent",
            "sec-ch-ua",
        ]
        self.possible_headers = [
            "Cache-Control",
            "Connection",
            "Content-Length",
            "Content-Type",
            "Accept-Encoding",
            "Accept-Language",
            "Host",
            "Origin",
            "Referer",
            "Upgrade-Insecure-Requests",
        ]

    def run(self) -> None:
        # save start time
        start = time.time()

        # generate a random number from 0 to 1
        # if the number is less than 0.5, then send a genuine request
        # otherwise, send a malicious request
        # genuine will only decrement counter by 1
        # malicious will decrement counter by 51
        schedule = []  # 1 for genuine, 51 for malicious
        while sum(schedule) < self.n:
            r = random.random()
            if r < 0.5:
                schedule.append(1)
            else:
                schedule.append(51)
        random.shuffle(schedule)

        for unit in schedule:
            if unit == 1:
                self.genuine()
            else:
                self.malicious()

        # end timer
        end = time.time()
        self.time = end - start

        self.report()

    def form_request(self) -> bytes:
        method = random.choice(self.http_methods)
        version = random.choice(self.http_versions)
        endpoint = random.choice(self.http_endpoints)
        request = f"{method} {endpoint} {version}\r\n".encode()

        headers = {}
        for header in self.required_headers:
            headers[header] = "".join(
                [chr(random.randint(32, 126))
                 for _ in range(random.randint(1, 10))]
            )
        for header in self.possible_headers:
            if random.random() > 0.5:
                headers[header] = "".join(
                    [chr(random.randint(32, 126))
                     for _ in range(random.randint(1, 10))]
                )

        for header in headers.keys():
            request += f"{header}: {headers[header]}\r\n".encode()
        request += b"\r\n"

        if method == "POST":
            headers["Content-Type"] = "application/json"
            body = json.dumps(
                {
                    "".join(
                        [chr(random.randint(32, 126))
                         for _ in range(random.randint(1, 10))]
                    ): "".join(
                        [chr(random.randint(32, 126))
                         for _ in range(random.randint(1, 10))]
                    )
                    for _ in range(random.randint(1, 10))
                }
            )
            headers["Content-Length"] = len(body)
            request += body.encode()

        return request

    def print_traffic(self, sockname: Tuple, request: bytes, response: bytes) -> None:
        print(
            f"[{sockname[0]}:{sockname[1]} -> {self.host}:{self.port}] {request.decode().splitlines()[0]} Response: {response.decode().splitlines()}"
        )

    def genuine(self) -> None:
        request = self.form_request()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            info = s.getsockname()
            send_all(s, request)
            response = recv_all(s)
            s.close()
            self.print_traffic(info, request, response)

        if b"200 OK" in response:
            self.true_positives += 1
        else:
            self.false_positives += 1

    def malicious(self) -> None:
        request = self.form_request()

        for i in range(51):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                info = s.getsockname()
                send_all(s, request)
                response = recv_all(s)
                s.close()
                self.print_traffic(info, request, response)

            if b"200 OK" in response:
                self.true_negatives += 1
            else:
                self.false_negatives += 1

    def report(self) -> None:
        accuracy = (self.true_positives + self.true_negatives) / (
            self.true_negatives + self.true_positives +
            self.false_negatives + self.false_positives
        )

        detection_rate = self.true_positives / (
            self.true_positives + self.false_negatives
        )

        false_positive_rate = self.false_positives / (
            self.false_positives + self.true_negatives
        )

        print(
            "Report:\n"
            f"Total Requests: {self.true_positives + self.false_positives + self.true_negatives + self.false_negatives}\n"
            f"True Positives: {self.true_positives}\n"
            f"False Positives: {self.false_positives}\n"
            f"True Negatives: {self.true_negatives}\n"
            f"False Negatives: {self.false_negatives}\n"
            f"Accuracy: {accuracy}\n"
            f"Detection Rate: {detection_rate}\n"
            f"False Positive Rate: {false_positive_rate}"
        )

    def save_results(self) -> None:
        id = str(uuid.uuid4())

        accuracy = (self.true_positives + self.true_negatives) / (
            self.true_negatives + self.true_positives +
            self.false_negatives + self.false_positives
        )

        detection_rate = self.true_positives / (
            self.true_positives + self.false_negatives
        )

        false_positive_rate = self.false_positives / (
            self.false_positives + self.true_negatives
        )

        json_data = {
            "id": id,
            "time": self.time,
            "n": self.true_positives + self.false_positives + self.true_negatives + self.false_negatives,
            "true_positives": self.true_positives,
            "false_positives": self.false_positives,
            "true_negatives": self.true_negatives,
            "false_negatives": self.false_negatives,
            "accuracy": accuracy,
            "detection_rate": detection_rate,
            "false_positive_rate": false_positive_rate,
        }

        file = Path(f"result/{id}.json")
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(json.dumps(json_data))
