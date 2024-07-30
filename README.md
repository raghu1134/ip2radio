# ip2radio

The `ip2radio` Python script retrieves detailed IP information and identifies the nearest radio towers using the OpenCellID API. It provides comprehensive geolocation data and uses latitude and longitude to find nearby radio towers. Results, including Google Maps links, are saved to a text file for easy visualization and analysis.

[![Watch the video](https://i.imgur.com/iFf6wWQ.jpg)](https://i.imgur.com/iFf6wWQ.mp4)

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/ip2radio.git
    cd ip2radio
    ```

2. **Install required libraries:**

    ```bash
    pip install requests
    pip install beautifulsoup4
    ```

## Usage

1. **Open a terminal and navigate to the project directory:**

    ```bash
    cd /path/to/ip2radio
    ```

2. **Run the Python script:**

    ```bash
    python ip2radio.py
    ```

3. **Configure the script:**

    - When prompted, Do you want to use a proxy? (`yes`/`no`):
    - Enter IP address:
    - Then it will fetch all the data regarding the Ip also with Googlemaps coordinates
    - then will head to website https://opencellid.org/#zoom=16&lat=52.30578&lon=4.94538 and find the live radio towers which is connected to the IP.

4. **Proceed:**

    Follow the on-screen instructions to fetch IP details and find the nearest radio towers. The results will be saved to a file named `{ip_address}.txt` with Google Maps links for visualization.

## Example

```bash
$ python ip2radio.py
Do you want to use a proxy? (yes/no):
Enter IP address: 8.8.8.8
Fetching data...
Results saved to Radios-data.txt
