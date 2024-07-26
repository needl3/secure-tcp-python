# A python implementation for secure tcp with chained certificates

## How to run

1. Install the requirements using `pip install -r requirements.txt` (Preferably on your virtual environment)
2. Spin up frontend server using `python app_improved.py`
3. Spin up backend server using `python srv_single.py localhost -p 3000`
4. Test the app by going to `https://localhost:5000` or using the test script as `python test.py --url https://localhost:5000 --username u1234567 --password csc2330a3`
