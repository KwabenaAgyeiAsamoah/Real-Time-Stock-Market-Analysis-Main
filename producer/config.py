import logging
import os

from dotenv import load_dotenv

load_dotenv()

#configure logging
logging.basicConfig(
    filename='stock_data_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


BASEURL = "alpha-vantage.p.rapidapi.com"
url = "https://alpha-vantage.p.rapidapi.com/query"

api_key = os.getenv("API_KEY")

headers = {
    "X-RapidAPI-Key": api_key,
    "X-RapidAPI-Host": BASEURL
}




